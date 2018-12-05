# TODO: Find and add relevant imports
import math
import queue
from Controller import *
from View import *


# TODO: Populate model with methods

class MapPath:

    # Constructor, sets all user input variables to 0.
    # The __ makes them private
    def __init__(self):
        self.__startLongitude = 0
        self.__endLongitude   = 0
        self.__startLatitude  = 0
        self.__endLatitude    = 0
        self.__difficulty     = 0

    # set methods to be used in View.py when navigate() is called
    def setStartLongitude(self, userInput):
        self.__startLongitude = userInput

    def setEndLongitude(self, userInput):
        self.__endLongitude = userInput

    def setStartLatitude(self, userInput):
        self.__startLatitude = userInput

    def setEndLatitude(self, userInput):
        self.__endLatitude = userInput

    def setDifficulty(self, difficulty):
        self.__difficulty = difficulty

    # get methods for our private variables
    def getStartLongitude(self):
        return self.__startLongitude

    def getEndLongitude(self):
        return self.__endLongitude

    def getStartLatitude(self):
        return self.__startLatitude

    def getEndLatitude(self):
        return self.__endLatitude

    def getDifficulty(self):
        return self.__difficulty

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