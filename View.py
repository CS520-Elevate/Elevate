# TODO: Find and add relevant imports
import os
from Controller import *
from Model import *
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk

difficulty = 0


# TODO: Link navigate function to Model
def navigate():
    None


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

    if(is_number(input) and float(input) <= 90 and float(input) >= -90):
        return True
    else:
        return False

def validateLongitude(input):

    if(is_number(input) and float(input) <= 180 and float(input) >= -180):
        return True
    else:
        return False


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

        # Radio buttons for difficulty setting
        Radiobutton(self, text="Easy", variable=difficulty, value=0).grid(row=4, column=2)
        Radiobutton(self, text="Medium", variable=difficulty, value=1).grid(row=4, column=3)
        Radiobutton(self, text="Hard", variable=difficulty, value=2).grid(row=4, column=4)

        # TODO: Have image area display the navigated map
        # Display area, currently static image
        image = Image.open("image.png")
        img = ImageTk.PhotoImage(image)
        img_label = Label(self, image=img)
        img_label.image = img
        # img_label.grid(row=5, column=1, columnspan=5)
        ROWS = 50
        COLS = 50
        tiles = [[None for _ in range(COLS)] for _ in range(ROWS)]

        def callback(event):
            # Get rectangle diameters
            col_width = c.winfo_width() / COLS
            row_height = c.winfo_height() / ROWS
            # Calculate column and row number
            col = int((event.x // col_width))
            row = int(event.y // row_height)
            # If the tile is not filled, create a circle
            if not tiles[row][col]:
                tiles[row][col] = c.create_oval(col * col_width, row * row_height, (col + 1) * col_width,
                                                (row + 1) * row_height, fill="red")
            # If the tile is filled, delete the circle and clear the reference
            else:
                c.delete(tiles[row][col])
                tiles[row][col] = None

        w = img.width()
        h = img.height()
        c = Canvas(self, width=w, height=h)
        c.grid(row=5, column=1, columnspan=5)
        c.create_image(0, 0, image=img, anchor='nw')
        c.bind("<Button-1>", callback)

        # Quit button
        Button(self, text="  Quit  ", command=client_exit).grid(row=6, column=5, pady=5)
