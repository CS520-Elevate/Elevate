# TODO: Find and add relevant imports
import sys
from Controller import *
from View import *
from Model import *


# TODO: Define __init__ and run in Main class
class Main(object):
    def __init__(self):
        self.init_view()

    def init_view(self):
        root = Tk()
        root.resizable(0, 0)
        View(root)
        root.mainloop()


Main()
