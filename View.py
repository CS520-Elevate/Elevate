# TODO: Find and add relevant imports
import os
from Controller import *
from Model import *
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk


# TODO: Link navigate function to Model
def navigate():
    None


def client_exit():
    exit()


class View(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master

        self.init_window()

    def init_window(self):
        self.master.title("Elevate")

        self.pack(fill=BOTH, expand=1)

        # Start coordinates area
        Label(self, text="Start").grid(row=1, column=1, columnspan=2)
        Label(self, text="Latitude").grid(row=2, column=1)
        Label(self, text="Longitude").grid(row=3, column=1)
        Entry(self, width=10).grid(row=2, column=2)
        Entry(self, width=10).grid(row=3, column=2)

        # End coordinates area
        Label(self, text="End").grid(row=1, column=3, columnspan=2)
        Label(self, text="Latitude").grid(row=2, column=3)
        Label(self, text="Longitude").grid(row=3, column=3)
        Entry(self, width=10).grid(row=2, column=4)
        Entry(self, width=10).grid(row=3, column=4)

        # Navigate button which will execute the program
        Button(self, text="  Navigate  ").grid(row=2, column=5, rowspan=2)

        # TODO: Have image area display the navigated map
        # Display area, currently static image
        image = Image.open("image.png")
        img = ImageTk.PhotoImage(image)
        img_label = Label(self, image=img)
        img_label.image = img
        img_label.grid(row=4, column=1, columnspan=5)

        # Quit button
        Button(self, text="  Quit  ", command=client_exit).grid(row=5, column=5, pady=5)

