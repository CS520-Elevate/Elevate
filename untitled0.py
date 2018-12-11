# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 13:40:19 2018

@author: kaila
"""

import numpy as np
import osmnx as ox
import networkx as nx


import folium

import matplotlib.pyplot as plt
#%matplotlib inline

old_market = (41.255676, -95.931338)
G = ox.graph_from_point(old_market, distance=500)

ox.plot_graph(G, fig_height=10, fig_width=10, edge_color='black')
route = nx.shortest_path(G, np.random.choice(G.nodes), np.random.choice(G.nodes))
ox.plot_graph_route(G, route, fig_height=10, fig_width=10)

library = ox.geocode('215 S 15th St, Omaha, NE 68102')
museum = ox.geocode('801 S 10th St, Omaha, NE 68108')

fig, ax = ox.plot_graph(G, fig_height=10, fig_width=10, 
                        show=False, close=False, 
                        edge_color='black')

