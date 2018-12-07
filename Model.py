# TODO: Find and add relevant imports
import math
import queue
import urllib.request
import json
import math
from Controller import *
from View import *

DEFAULT_SAMPLES = 10


# TODO: Populate model with methods

class MapPath:

    # Constructor, sets all user input variables to 0.
    # The __ makes them private
    def __init__(self):
        self.__startLongitude = 0
        self.__endLongitude = 0
        self.__startLatitude = 0
        self.__endLatitude = 0
        self.__difficulty = 0
        self.__areaMap = {}

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

    # def setAreaMap():

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

    def getAreaMap(self):
        return self.__areaMap


def arrange_coords(coord0, coord1):
    """
    Takes two coordinates and arranges them to (xmin, ymin), (xmax, ymax)
    """
    (x0, y0) = coord0
    (x1, y1) = coord1

    return (min(x0, x1), min(y0, y1)), (max(x0, x1), max(y0, y1))


def get_box(coord0, coord1, samples=DEFAULT_SAMPLES):
    """
    coord0 and coord1 are corners of a box. this function
    returns the list of points contained within that box, with the given precision

    example:
    (0, 0), (1, 1), precision=10
    [(0,0), (0,0.1),...(0.1,0.1),...(1,1)]

    [(xlow-xhigh)/precision]
    """
    (xmin, ymin), (xmax, ymax) = arrange_coords(coord0, coord1)

    xdelta = (xmax - xmin) / (samples - 1)
    ydelta = (ymax - ymin) / (samples - 1)

    return [[(xmin + i * xdelta, ymin + j * ydelta)
             for i in range(samples)] for j in range(samples)]


def get_elevation_map(box):
    """
    Takes in a matrix of coordinates and queries the API to
    get the corresponding elevations, in the form {coord: elevation}
    """

    # build request
    locations = {"locations":
                     [{"longitude": y, "latitude": x} for row in box for (x, y) in row]}
    json_data = json.dumps(locations).encode('utf8')

    # send request
    url = "https://api.open-elevation.com/api/v1/lookup"
    response = urllib.request.Request(url, json_data, headers={'Content-Type': 'application/json'}, method='POST')
    fp = urllib.request.urlopen(response)

    # process response
    res_byte = fp.read()
    res_str = res_byte.decode("utf8")
    response = json.loads(res_str)
    fp.close()

    return {(entry['latitude'], entry['longitude']): entry['elevation']
            for entry in response['results']}


# samples cant be bigger than 6 for now
def build_graph(coord0, coord1, samples=DEFAULT_SAMPLES):
    def neighbors(loc, size):
        """
        Gets the neighboring for a 2D index in a matrix

        for example, neighbors((1,1), _)
        returns: [
            (1, 0), (2, 1), (0, 1), (1, 2)
        ]
        """
        (i, j) = loc
        res = []
        if i > 0:
            res.append((i - 1, j))  # left
        if j > 0:
            res.append((i, j - 1))  # up
        if i < size - 1:
            res.append((i + 1, j))  # right
        if j < size - 1:
            res.append((i, j + 1))  # down

        return res

    # get the matrix of points with coord0 and coord1 as corners
    box = get_box(coord0, coord1, samples=samples)

    # sample points in between the recorded points
    num_samples = samples ** 2  # numer of elevation samples to query
    # build  more precise coordinate matrix for elevation query
    sample_box = get_box(box[0][0], box[samples - 1][samples - 1], num_samples)
    elevation_map = get_elevation_map(sample_box)
    elevs_values = list(elevation_map.values())
    elevation_matrix = [[elevs_values[i * num_samples + j]
                         for j in range(num_samples)] for i in range(num_samples)]

    def get_elevation_delta(loc0, loc1):
        """
        Computes the elevation difference between two locations in the sample matrix
        """
        (xmin, ymin), (xmax, ymax) = arrange_coords(loc0, loc1)
        n = samples

        if xmin < xmax:
            # sum along x
            return sum(elevation_matrix[x][ymin * n] for x in range(xmin * n, xmax * n + 1))
        else:
            # sum along y
            return sum(elevation_matrix[xmin * n][y] for y in range(ymin * n, ymax * n + 1))

    # construct the graph
    vertices = [coord for row in box for coord in row]
    edges = {}
    for i, row in enumerate(box):
        for j, coord in enumerate(row):
            nbrs = neighbors((i, j), samples)
            edges[coord] = {box[nbr[0]][nbr[1]]: get_elevation_delta((i, j), nbr)
                            for nbr in nbrs}

    return (vertices, edges)


def dijkstra_search(map, starting_point, ending_point):
    q = queue.PriorityQueue()  # priority queue of items
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


def astar_search():
    None
