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
