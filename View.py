# TODO: Find and add relevant imports
import os
from Controller import *
from Model import *
from tkinter import ttk
from OSMnx import *
from tkinter import *
from PIL import Image, ImageTk
from sys import exit
import matplotlib.pyplot as plt
from tkinter import messagebox
import webbrowser

# Instance of MapPath, used to hold our user input privately.
# Navigation should use these variables (via get methods), as they are either 0 or will have been
# checked for validity before being set.
thisPath = MapPath()

def client_exit():
    exit()

# Very simple function to determine if string input is a valid decimal
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# The next 2 functions are used to validate user input. Returns true if input is valid
def validateLatitude(input):
    if is_number(input) and 90 >= float(input) >= -90:
        return True
    else:
        return False

def validateLongitude(input):
    if is_number(input) and 180 >= float(input) >= -180:
        return True
    else:
        return False

class View(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.difficulty = IntVar()
        self.master = master
        self.init_window()

    def init_window(self):

        # method which returns the user-input values of latitude and longitude
        def get_entry():
            return [self.start_lat.get(), self.start_long.get(), self.end_lat.get(), self.end_long.get()]

        # method to make sure user input is valid. Returns false if not valid, True if valid
        def validate():
            if (validateLatitude(self.start_lat.get()) and validateLongitude(self.start_long.get())
                and validateLatitude(self.end_lat.get()) and validateLongitude(self.end_long.get())):

                thisPath.setStartLatitude(float(self.start_lat.get()))
                thisPath.setStartLongitude(float(self.start_long.get()))
                thisPath.setEndLatitude(float(self.end_lat.get()))
                thisPath.setEndLongitude(float(self.end_long.get()))
                thisPath.setDifficulty(self.difficulty.get())

                return True
            else:
                return False

        # button call to navigate funtion (Should be modified to call Model.py's navigate
        def navigate():
            # validate populates thisPath variables if true
            if (validate()):
                
                osmnx = OSMnx()

                result=osmnx.get_map(thisPath.getStartLatitude(), thisPath.getStartLongitude(),
                    thisPath.getEndLatitude(), thisPath.getEndLongitude(), thisPath.getDifficulty())
                              
                self.dist = Label(self, text="Route Distance(m): " + str(result[1])).grid(row=7, column=1, columnspan=2)
                self.elev = Label(self, text="Ascent: " + str(result[0])).grid(row=7, column=3, columnspan=2)
                webbrowser.open_new_tab('routeff.html')
               
            else:
                # invalid input
                messagebox.showinfo("Error", "Invalid Input")

        self.master.title("Elevate")

        self.pack(fill=BOTH, expand=1)

        self.difficulty.set(0)

        # Start coordinates area
        Label(self, text="Start").grid(row=1, column=1, columnspan=2)
        Label(self, text="Latitude").grid(row=2, column=1)
        Label(self, text="Longitude").grid(row=3, column=1)
        self.start_lat = Entry(self, width=10)
        self.start_long = Entry(self, width=10)
        self.start_lat.grid(row=2, column=2)
        self.start_long.grid(row=3, column=2)

        # End coordinates area
        Label(self, text="End").grid(row=1, column=3, columnspan=2)
        Label(self, text="Latitude").grid(row=2, column=3)
        Label(self, text="Longitude").grid(row=3, column=3)
        self.end_lat = Entry(self, width=10)
        self.end_long = Entry(self, width=10)
        self.end_lat.grid(row=2, column=4)
        self.end_long.grid(row=3, column=4)

        #Stats
        dist = Label(self, text="Route Distance: ").grid(row=7, column=1, columnspan=2)
        elev = Label(self, text="Elevation change: ").grid(row=7, column=3, columnspan=2)

        # Navigate button which will execute the program
        Button(self, text="  Navigate  ", command=navigate).grid(row=2, column=5, rowspan=2)


        
        # Radio buttons for difficulty setting
        Radiobutton(self, text="Easy", variable=self.difficulty, value=0).grid(row=4, column=2)
        Radiobutton(self, text="Medium", variable=self.difficulty, value=1).grid(row=4, column=3)
        Radiobutton(self, text="Hard", variable=self.difficulty, value=2).grid(row=4, column=4)