import sys
from Controller import *
from View import *
from Model import *


class Main(object):
    def __init__(self):
        self.init_view()

    def init_view(self):
        root = Tk()
        root.resizable(0, 0)
        View(root)
        root.mainloop()

Main()
