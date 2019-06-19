from tkinter import *
import Buttons as b


class popUp:

    def __init__(self, parent, WIDTH, HEIGHT):
        self.parent = parent
        self.width = WIDTH
        self.height = HEIGHT

        self.popUpFrame = Canvas(self.parent, width=self.width*(3/4), height=self.height*(3/4), bg="black")
        self.popUpFrame.pack_propagate(0)
        b.backButton(self.popUpFrame)
        self.popUpFrame.place(relx=.5, rely=.5, anchor="center")

class confirmation:

    def __init__(self, parent, WIDTH, HEIGHT, message):
        self.parent = parent
        self.width = WIDTH
        self.height = HEIGHT
        self.message = message

        self.popUpFrame = Canvas(self.parent, width=self.width * (3 / 4), height=self.height * (3 / 4), bg="black")
        b.yesButton(self.popUpFrame, .25, .8)
        b.noButton(self.popUpFrame, .75, .8)

