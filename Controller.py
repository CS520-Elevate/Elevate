# TODO: Find and add relevant imports
import sys
from collections import defaultdict
from View import *
from Model import *


# TODO: Populate Controller class with methods
class Controller(object):
    def __init__(self):
        None


'''
if __name__ == '__main__':
	t = MapPath().get_elevation(42.3732, 72.5199, 42.3742, 72.5209, 10)
	print(t)
'''
if __name__ == '__main__':
    # map_path = MapPath()
    # map_path.get_elevation((0,0), (1,1), 10)

    # def create_map(start_lat, start_long, end_lat, end_long):

    # 	graph = defaultdict(list)
    # 	x = start_lat
    # 	y = start_long
	#  	#r1 = 10000*(end_lat - start_lat)

    # 	while x <= end_lat:
    # 		while y <= end_long:
    # 			cur = (x, y)
    # 			y += 0.0001
    # 			nex = (x, y)

    # 			elev = map_path.get_elevation(cur, nex, 20)

    # 			graph[cur].append((nex, elev[2]))
    # 			graph[nex].append((cur, elev[2]))
    # 		x += 0.0001

    # 	return graph
    # x = create_map(42.3732, 72.5199, 42.3742, 72.5203)
    # print(x.keys())
    # sample size wont bigger than 6 now working on a fix for this
    graph = build_graph((42.3732, 72.5199), (47.3742, 77.5209), samples=6)
    vertices, edges = graph

    print("vertices:")
    print(vertices)

    print()
    print("edges:")
    for p0, es in edges.items():
        print(str(p0) + " =============")
        for p1, diff in es.items():
            print("    " + str(p0) + ": " + str(diff))
