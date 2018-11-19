# TODO: Find and add relevant imports
import os
from Controller import *
from Model import *
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk


# TODO: create a GUI
class View(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master

        self.init_window()

    def init_window(self):
        self.master.title("Elevate")

        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="  Quit  ", command=self.client_exit)
        latitude_entry_start = Entry(self, width=10)
        longitude_entry_start = Entry(self, width=10)
        start = Label(self, text="Start")
        lat_label_start = Label(self, text="Latitude")
        long_label_start = Label(self, text="Longitude")
        latitude_entry_end = Entry(self, width=10)
        longitude_entry_end = Entry(self, width=10)

        end = Label(self, text="End")
        lat_label_end = Label(self, text="Latitude")
        long_label_end = Label(self, text="Longitude")
        navigate_button = Button(self, text="  Navigate  ", command=self.navigate)

        image = Image.open("image.png")
        img = ImageTk.PhotoImage(image)
        img_label = Label(self, image=img)
        img_label.image = img

        start.place(x=100, y=5)
        lat_label_start.place(x=20, y=40)
        latitude_entry_start.place(x=100, y=40)
        long_label_start.place(x=20, y=70)
        longitude_entry_start.place(x=100, y=70)

        end.place(x=320, y=5)
        lat_label_end.place(x=220, y=40)
        latitude_entry_end.place(x=300, y=40)
        long_label_end.place(x=220, y=70)
        longitude_entry_end.place(x=300, y=70)

        img_label.pack(padx=20, pady=100, anchor=CENTER)

        navigate_button.place(x=410, y=55)
        quitButton.place(x=400, y=450)

    def navigate(self):
        None

    def client_exit(self):
        exit()


root = Tk()
root.geometry("500x500")

app = View(root)

root.mainloop()
