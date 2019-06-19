from tkinter import *
import Popup as p

class backButton:

    def __init__(self, parent):
        self.parent = parent

        self.image = PhotoImage(file="Back.gif")
        self.button = Button(parent, command=self.behavior)
        self.button.config(image=self.image)
        self.button.place(relx=0, rely=0)

    def behavior(self):
        self.parent.destroy()

class yesButton:

    def __init__(self, parent, x, y):
        self.parent = parent

        self.image = PhotoImage(file="yes.gif")
        self.button = Button(parent.popUpFrame, command=self.behavior)
        self.button.config(image=self.image)
        self.button.place(relx=x, rely=y)

    def behavior(self):
        pass

class noButton:

    def __init__(self, parent, x, y):
        self.parent = parent

        self.image = PhotoImage(file="no.gif")
        self.button = Button(parent.popUpFrame, command=self.behavior)
        self.button.config(image=self.image)
        self.button.place(relx=x, rely=y)

    def behavior(self):
        self.parent.popUpFrame.destroy()


