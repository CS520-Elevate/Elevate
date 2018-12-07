from ctypes.util import find_library
find_library('geos_c')
import osmnx as ox, networkx as nx, numpy as np
ox.config(log_console=True, use_cache=True)
from View import *
from math import sin, cos, sqrt, atan2, radians



# get the street network for Amherst
class OSMnx():

		
	def get_map(self, start_lat, start_long, end_lat, end_long, chosen_weight):
		print("123", start_lat, start_long, end_lat, end_long,)
		place = 'Amherst'
		place_query = {'city': 'Amherst', 'state': 'Massachusetts', 'country': 'USA'}
		G = ox.graph_from_place(place_query, network_type='drive')
		G = ox.add_node_elevations(G, api_key= 'AIzaSyB9DBYn2sdIznFbmBg4DHOTl54soDBkx2E')
		G = ox.add_edge_grades(G)
		edge_grades = [data['grade_abs'] for u, v, k, data in ox.get_undirected(G).edges(keys=True, data=True)]
		avg_grade = np.mean(edge_grades)
		#print('Average street grade in {} is {:.1f}%'.format(place, avg_grade*100))

		med_grade = np.median(edge_grades)
		#print('Median street grade in {} is {:.1f}%'.format(place, med_grade*100))
		# project the street network to UTM
		G_proj = ox.project_graph(G)
		# get one color for each node, by elevation, then plot the network
		nc = ox.get_node_colors_by_attr(G_proj, 'elevation', cmap='plasma', num_bins=20)
		#fig, ax = ox.plot_graph(G_proj, fig_height=6, node_color=nc, node_size=12, node_zorder=2, edge_color='#dddddd')
		# get a color for each edge, by grade, then plot the network
		ec = ox.get_edge_colors_by_attr(G_proj, 'grade_abs', cmap='plasma', num_bins=10)
		#fig, ax = ox.plot_graph(G_proj, fig_height=6, edge_color=ec, edge_linewidth=0.8, node_size=0)
		# select an origin and destination node and a bounding box around them
		origin = ox.get_nearest_node(G, (start_lat, start_long))
		destination = ox.get_nearest_node(G, (end_lat , end_long))
		bbox = ox.bbox_from_point(((start_lat + end_lat) / 2, (start_long + end_long) / 2), distance= 5 * self.get_distance(start_lat, start_long, end_lat, end_long), project_utm=True)
		
		for u, v, k, data in G_proj.edges(keys=True, data=True):
		    data['impedance'] = self.impedance(data['length'], data['grade_abs'])
		    data['rise'] = data['length'] * data['grade']	
		route = nx.shortest_path(G_proj, source=origin, target=destination, weight = chosen_weight)
		fig, ax = ox.plot_graph_route(G_proj, route, bbox=bbox, node_size=0)

		return fig, print_route_stats(route) 

		# route_by_impedance = nx.shortest_path(G_proj, source=origin, target=destination, weight='impedance')
		# fig, ax = ox.plot_graph_route(G_proj, route_by_impedance, bbox=bbox, node_size=0)


		# stats of route minimizing length
		# stats of route minimizing impedance (function of length and grade)
		#print_route_stats(route_by_impedance)


	def impedance(self, length, grade):
	    penalty = grade ** 2
	    return length * penalty
		# add impedance and elevation rise values to each edge in the projected graph
		# use absolute value of grade in impedance function if you want to avoid uphill and downhill

	def print_route_stats(self, route):
	    route_grades = ox.get_route_edge_attributes(G_proj, route, 'grade_abs')
	    msg = 'The average grade is {:.1f}% and the max is {:.1f}%'
	    #print(msg.format(np.mean(route_grades)*100, np.max(route_grades)*100))

	    route_rises = ox.get_route_edge_attributes(G_proj, route, 'rise')
	    ascent = np.sum([rise for rise in route_rises if rise >= 0])
	    descent = np.sum([rise for rise in route_rises if rise < 0])
	    msg = 'Total elevation change is {:.0f} meters: a {:.0f} meter ascent and a {:.0f} meter descent'
	    #print(msg.format(np.sum(route_rises), ascent, abs(descent)))

	    route_lengths = ox.get_route_edge_attributes(G_proj, route, 'length')
	    #print('Total trip distance: {:,.0f} meters'.format(np.sum(route_lengths)))
			
	def get_distance(self, sla, slo, ela, elo):
		R = 6373.0
		lat1 = radians(52.2296756)
		lon1 = radians(21.0122287)
		lat2 = radians(52.406374)
		lon2 = radians(16.9251681)

		dlon = lon2 - lon1
		dlat = lat2 - lat1

		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))

		distance = R * c
		return distance





