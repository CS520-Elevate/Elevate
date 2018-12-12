
# coding: utf-8

# In[2]:


import osmnx as ox


# In[8]:


import networkx as nx 
import numpy as np
ox.config(log_console=True, use_cache=True)


# In[4]:


google_elevation_api_key="AIzaSyCkCrJwj0gzVp1kGjo5lz6VKDyaFUEVbGk"


# In[20]:


place = 'Amherst'
place_query = {'city':'Amherst', 'state':'Massachusetts', 'country':'USA'}
G = ox.graph_from_place(place_query, network_type='drive')


# In[21]:


G = ox.add_node_elevations(G, api_key=google_elevation_api_key)
G = ox.add_edge_grades(G)


# In[22]:


edge_grades = [data['grade_abs'] for u, v, k, data in ox.get_undirected(G).edges(keys=True, data=True)]


# In[23]:


avg_grade = np.mean(edge_grades)
print('Average street grade in {} is {:.1f}%'.format(place, avg_grade*100))

med_grade = np.median(edge_grades)
print('Median street grade in {} is {:.1f}%'.format(place, med_grade*100))


# In[24]:


G_proj = ox.project_graph(G)


# In[25]:


nc = ox.get_node_colors_by_attr(G_proj, 'elevation', cmap='plasma', num_bins=20)
fig, ax = ox.plot_graph(G_proj, fig_height=6, node_color=nc, node_size=12, node_zorder=2, edge_color='#dddddd')


# In[46]:


origin = ox.get_nearest_node(G, (42.3778, -72.5198))
destination = ox.get_nearest_node(G, (42.3898, -72.5283))
bbox = ox.bbox_from_point((42.384, -72.524), distance=1500, project_utm=True)


# In[47]:


def impedance(length, grade):
    penalty = grade ** 2
    return length * penalty

# add impedance and elevation rise values to each edge in the projected graph
# use absolute value of grade in impedance function if you want to avoid uphill and downhill
for u, v, k, data in G_proj.edges(keys=True, data=True):
    data['impedance'] = impedance(data['length'], data['grade_abs'])
    data['rise'] = data['length'] * data['grade']


# ## First find the shortest path that minimizes trip distance:¶
# 

# In[48]:


route_by_length = nx.shortest_path(G_proj, source=origin, target=destination, weight='length')
fig, ax = ox.plot_graph_route(G_proj, route_by_length, bbox=bbox, node_size=0)


# ## Now find the shortest path that avoids slopes by minimizing impedance (function of length and grade):¶
# 

# In[49]:


route_by_impedance = nx.shortest_path(G_proj, source=origin, target=destination, weight='impedance')
fig, ax = ox.plot_graph_route(G_proj, route_by_impedance, bbox=bbox, node_size=0)


# In[50]:


def print_route_stats(route):
    route_grades = ox.get_route_edge_attributes(G_proj, route, 'grade_abs')
    msg = 'The average grade is {:.1f}% and the max is {:.1f}%'
    print(msg.format(np.mean(route_grades)*100, np.max(route_grades)*100))

    route_rises = ox.get_route_edge_attributes(G_proj, route, 'rise')
    ascent = np.sum([rise for rise in route_rises if rise >= 0])
    descent = np.sum([rise for rise in route_rises if rise < 0])
    msg = 'Total elevation change is {:.0f} meters: a {:.0f} meter ascent and a {:.0f} meter descent'
    print(msg.format(np.sum(route_rises), ascent, abs(descent)))

    route_lengths = ox.get_route_edge_attributes(G_proj, route, 'length')
    print('Total trip distance: {:,.0f} meters'.format(np.sum(route_lengths)))


# In[51]:


print_route_stats(route_by_length)


# In[52]:


print_route_stats(route_by_impedance)


# In[1]:


##


# In[3]:


import numpy as np
import osmnx as ox
import networkx as nx
from sklearn.neighbors import KDTree

import folium

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[27]:


old_market = (42.38, -72.52)
G = ox.graph_from_point(old_market, distance=1000)
# quick plot
ox.plot_graph(G, fig_height=10, fig_width=10, edge_color='black')


# In[28]:


route = nx.shortest_path(G, np.random.choice(G.nodes), 
                         np.random.choice(G.nodes))
ox.plot_graph_route(G, route, fig_height=10, fig_width=10)


# In[29]:


library = ox.geocode('154 Hicks Way, Amherst, MA 01003')
museum = ox.geocode('141 Southwest Cir, Amherst, MA 01003')


# In[30]:


fig, ax = ox.plot_graph(G, fig_height=10, fig_width=10, 
                        show=False, close=False, 
                        edge_color='black')
ax.scatter(library[1], library[0], c='red', s=100)
ax.scatter(museum[1], museum[0], c='blue',s=100)
plt.show()


# In[31]:


nodes, _ = ox.graph_to_gdfs(G)
nodes.head()


# In[32]:


tree = KDTree(nodes[['y', 'x']], metric='euclidean')
lib_idx = tree.query([library], k=1, return_distance=False)[0]
museum_idx = tree.query([museum], k=1, return_distance=False)[0]
closest_node_to_lib = nodes.iloc[lib_idx].index.values[0]
closest_node_to_museum = nodes.iloc[museum_idx].index.values[0]


# In[33]:


fig, ax = ox.plot_graph(G, fig_height=10, fig_width=10, 
                        show=False, close=False, 
                        edge_color='black')
ax.scatter(library[1], library[0], c='red', s=100)
ax.scatter(museum[1], museum[0], c='blue', s=100)
ax.scatter(G.node[closest_node_to_lib]['x'],
           G.node[closest_node_to_lib]['y'], 
           c='green', s=100)
ax.scatter(G.node[closest_node_to_museum]['x'],   
           G.node[closest_node_to_museum]['y'], 
           c='green', s=100)
plt.show()


# In[34]:


route = nx.shortest_path(G, closest_node_to_lib,
                         closest_node_to_museum)
fig, ax = ox.plot_graph_route(G, route, fig_height=10, 
                              fig_width=10, 
                              show=False, close=False, 
                              edge_color='black',
                              orig_dest_node_color='green',
                              route_color='green')
ax.scatter(library[1], library[0], c='red', s=100)
ax.scatter(museum[1], museum[0], c='blue', s=100)
plt.show()


# In[35]:


m = ox.plot_route_folium(G, route, route_color='green')
folium.Marker(location=library,
              icon=folium.Icon(color='red')).add_to(m)
folium.Marker(location=museum,
              icon=folium.Icon(color='blue')).add_to(m)
m

