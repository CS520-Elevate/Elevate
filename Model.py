# TODO: Find and add relevant imports
import math
import queue
from Controller import *
from View import *


# TODO: Populate model with methods

def getelevation():
    None


def dijkstra_search(map, starting_point, ending_point):
    q = queue.PriorityQueue()     #priority queue of items
    parents = []
    dist = []

    for i in map.vertex():
        if i == starting_point:
            weight = 0
        dist.append(float("inf"))
        parents.append(None)

    q.put(([0, starting_point]))

    while not q.empty():
        tuple = q.get()
        v = tuple[1]

        for edge in map.get_edge(v):
            successor_dist = dist[v] + edge.get_weight()
            if dist[edge.vertex] > successor_dist:
                dist[edge.vertex] = successor_dist
                parents[edge.vertex] = v
                q.put(([dist[edge.vertex], edge.vertex]))
    shortest_path = []
    end = ending_point
    while end is not None:
        shortest_path.append(end)
        end = parents[end]


    shortest_path.reverse()

    return shortest_path, dist[ending_point]









    return path

def astar_search():
    None
