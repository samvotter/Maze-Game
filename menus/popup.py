from tkinter import Canvas
from buttons import buttons as b


class PopUp:

    def __init__(self, parent):
        self.parent = parent
        self.width = parent.winfo_width()
        self.height = parent.winfo_height()

        self.popUpFrame = Canvas(self.parent, width=self.width * (3 / 4), height=self.height * (3 / 4), bg="black")
        self.popUpFrame.pack_propagate(False)
        b.BackButton(self.popUpFrame)
        self.popUpFrame.place(relx=.5, rely=.5, anchor="center")


class Confirmation:

    def __init__(self, parent, message):
        self.parent = parent
        self.width = parent.winfo_width()
        self.height = parent.winfo_height()
        self.message = message

        self.popUpFrame = Canvas(self.parent, width=self.width * (3 / 4), height=self.height * (3 / 4), bg="black")
        b.YesButton(self.popUpFrame, relx=.25, rely=.8)
        b.NoButton(self.popUpFrame, relx=.75, rely=.8)

