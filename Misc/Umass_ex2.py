
# coding: utf-8

# In[1]:


import numpy as np
import osmnx as ox
import networkx as nx
from sklearn.neighbors import KDTree

import folium

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


umass = (42.38, -72.52)
G = ox.graph_from_point(umass, distance=1000)
# quick pflot
ox.plot_graph(G, fig_height=10, fig_width=10, edge_color='black')


# In[3]:


route = nx.shortest_path(G, np.random.choice(G.nodes), 
                         np.random.choice(G.nodes))
ox.plot_graph_route(G, route, fig_height=10, fig_width=10)


# In[11]:


library = ox.geocode('154 Hicks Way, Amherst, MA 01003')
dining = ox.geocode('141 Southwest Cir, Amherst, MA 01003')


# In[12]:


fig, ax = ox.plot_graph(G, fig_height=10, fig_width=10, 
                        show=False, close=False, 
                        edge_color='black')
ax.scatter(library[1], library[0], c='red', s=100)
ax.scatter(dining[1], dining[0], c='blue',s=100)
plt.show()


# In[13]:


nodes, _ = ox.graph_to_gdfs(G)
nodes.head()


# In[16]:


tree = KDTree(nodes[['y', 'x']], metric='euclidean')
lib_idx = tree.query([library], k=1, return_distance=False)[0]
dining_idx = tree.query([dining], k=1, return_distance=False)[0]
closest_node_to_lib = nodes.iloc[lib_idx].index.values[0]
closest_node_to_dining = nodes.iloc[dining_idx].index.values[0]


# In[17]:


fig, ax = ox.plot_graph(G, fig_height=10, fig_width=10, 
                        show=False, close=False, 
                        edge_color='black')
ax.scatter(library[1], library[0], c='red', s=100)
ax.scatter(dining[1], dining[0], c='blue', s=100)
ax.scatter(G.node[closest_node_to_lib]['x'],
           G.node[closest_node_to_lib]['y'], 
           c='green', s=100)
ax.scatter(G.node[closest_node_to_dining]['x'],   
           G.node[closest_node_to_dining]['y'], 
           c='green', s=100)
plt.show()


# In[18]:


route = nx.shortest_path(G, closest_node_to_lib,
                         closest_node_to_dining)
fig, ax = ox.plot_graph_route(G, route, fig_height=10, 
                              fig_width=10, 
                              show=False, close=False, 
                              edge_color='black',
                              orig_dest_node_color='green',
                              route_color='green')
ax.scatter(library[1], library[0], c='red', s=100)
ax.scatter(dining[1], dining[0], c='blue', s=100)
plt.show()


# In[10]:


m = ox.plot_route_folium(G, route, route_color='green')
folium.Marker(location=library,
              icon=folium.Icon(color='red')).add_to(m)
folium.Marker(location=dining,
              icon=folium.Icon(color='blue')).add_to(m)
m

