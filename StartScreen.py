from tkinter import *

import Terrain as t
import Player as p
import Enemies as e
import Maze as m
import Buttons as b
import Tutorial as tt
import Popup as pu

# start screen buttons
class startButton:

    def __init__(self, parent, WIDTH, HEIGHT, x, y, startScreen):
        # parent is startscreen canvas
        self.parent = parent
        self.width = WIDTH
        self.height = HEIGHT
        self.startScreen = startScreen

        self.image = PhotoImage(file="startb.gif")
        self.button = Button(parent, command=self.behavior)
        self.button.config(image=self.image)
        self.button.place(relx=x, rely=y)

    def behavior(self):
        self.parent.destroy()
        maze = m.Maze(window, self.width, self.height,
                      t.Terrain(10, 20, p.Player(), [], barriers=True), path="random")
        maze.terrain.spawnEnemy()
        maze.display(next="expand")
        self.startScreen.rebuild()

class tutorialButton:

    def __init__(self, parent, WIDTH, HEIGHT, x, y, startScreen):
        # parent is startscreen canvas
        self.parent = parent
        self.width = WIDTH
        self.height = HEIGHT
        self.startScreen = startScreen

        self.image = PhotoImage(file="tutorialb.gif")
        self.button = Button(parent, command=self.behavior)
        self.button.config(image=self.image)
        self.button.place(relx=x, rely=y)

    def behavior(self):
        self.parent.destroy()
        t = tt.Tutorial(window, self.width, self.height, self.startScreen.player)
        t.tutorialSeries()
        self.startScreen.rebuild()

class optionsButton:

    def __init__(self, parent, WIDTH, HEIGHT, x, y):
        self.parent = parent
        self.width = WIDTH
        self.height = HEIGHT

        self.image = PhotoImage(file="optionsb.gif")
        self.button = Button(parent, command=self.behavior)
        self.button.config(image=self.image)
        self.button.place(relx=x, rely=y)

    def behavior(self):
        optionsScreen = pu.popUp(self.parent, self.width, self.height)
        optionsScreen.popUpFrame.configure(bg="#F0F0F0")
        Checkbutton(optionsScreen.popUpFrame, text="Do not automatically purchase more\n"
                                                   "gems from the store if you do not \n"
                                                   "have enough to complete purchase.", justify=LEFT).place(relx=.1, rely=.2)
        Checkbutton(optionsScreen.popUpFrame, text="Do not sell my account details.", justify=LEFT).place(relx=.1, rely=.3)
        Checkbutton(optionsScreen.popUpFrame, text="Do not automatically add suggested\n"
                                                   "purchases to my cart.", justify=LEFT).place(relx=.1, rely=.4)
        Checkbutton(optionsScreen.popUpFrame, text="Sign me up for warranty protection\n"
                                                   "with every purchase.", justify=LEFT).place(relx=.1, rely=.5)
        Checkbutton(optionsScreen.popUpFrame, text="Don't subscribe me to Super Fun Mazes,\n"
                                                   "a $9.99 monthly periodical.", justify=LEFT).place(relx=.1, rely=.6)
        Checkbutton(optionsScreen.popUpFrame, text="Email all of my email contacts\n"
                                                   "with the subject line: URGENT!\n"
                                                   "directing them to download this game.", justify=LEFT).place(relx=.1, rely=.7)
        Checkbutton(optionsScreen.popUpFrame, text="Don't store my credit card details\n"
                                                   "as plain text.", justify=LEFT).place(relx=.6, rely=.2)
        Checkbutton(optionsScreen.popUpFrame, text="Give me the option to rate this game\n"
                                                   "something other than 'five stars'.", justify=LEFT).place(relx=.6,
                                                                                                            rely=.3)
        Checkbutton(optionsScreen.popUpFrame, text="Restore default settings when leaving\n"
                                                   "this menu?", justify=LEFT).place(relx=.6, rely=.4)
        Checkbutton(optionsScreen.popUpFrame, text="Pay the full price, rather than the\n"
                                                   "listed sale price in the store.", justify=LEFT).place(relx=.6, rely=.5)
        Checkbutton(optionsScreen.popUpFrame, text="Do not automatically reinstall after\n"
                                                   "being deleted.", justify=LEFT).place(relx=.6, rely=.6)
        Checkbutton(optionsScreen.popUpFrame, text="Do not prompt me with conformation\n"
                                                   "when making a purchase.", justify=LEFT).place(relx=.6, rely=.7)

class exitButton:

    def __init__(self, parent, x, y):
        self.parent = parent

        self.image = PhotoImage(file="exitb.gif")
        self.button = Button(parent, command=self.behavior)
        self.button.config(image=self.image)
        self.button.place(relx=x, rely=y)

    def behavior(self):
        sys.exit()

class highButton:

    def __init__(self, parent, WIDTH, HEIGHT, x, y):
        self.parent = parent
        self.width = WIDTH
        self.height = HEIGHT

        self.image = PhotoImage(file="highscoresb.gif")
        self.button = Button(parent, command=self.behavior)
        self.button.config(image=self.image)
        self.button.place(relx=x, rely=y)

        self.scores = PhotoImage(file="scores.gif")

    def behavior(self):
        highscores = pu.popUp(self.parent, self.width, self.height)
        highscores.popUpFrame.create_image(0, 0, image=self.scores, anchor=NW)

class startScreen:

    def __init__(self, parent, WIDTH, HEIGHT):
        self.parent = parent
        self.width = WIDTH
        self.height = HEIGHT
        self.player = p.Player()
        self.image = PhotoImage(file="startscreen.gif")

        self.startCanvas = Canvas(parent, width=self.width, height=self.height)

        self.startCanvas.create_image(0, 0, image=self.image, anchor=NW)

        self.startb = startButton(self.startCanvas, WIDTH, HEIGHT, .15, .6, self)
        self.optionsb = optionsButton(self.startCanvas, WIDTH, HEIGHT, .4, .6)
        self.exitb = exitButton(self.startCanvas, .7, .6)
        self.highb = highButton(self.startCanvas, WIDTH, HEIGHT, .5, .8)
        self.tutorb = tutorialButton(self.startCanvas, WIDTH, HEIGHT, .2, .8, self)

        self.startCanvas.pack()

    def rebuild(self):
        self.image = PhotoImage(file="startscreen.gif")
        self.startCanvas = Canvas(self.parent, width=self.width, height=self.height)
        self.startCanvas.create_image(0, 0, image=self.image, anchor=NW)

        self.startb = startButton(self.startCanvas, self.width, self.height, .15, .6, self)
        self.optionsb = optionsButton(self.startCanvas, self.width, self.height, .4, .6)
        self.exitb = exitButton(self.startCanvas, .7, .6)
        self.highb = highButton(self.startCanvas, self.width, self.height, .5, .8)
        self.tutorb = tutorialButton(self.startCanvas, self.width, self.height, .2, .8, self)

        self.startCanvas.pack()

width = 1600
height = 900

window = Tk()
startScreen(window, width, height)

window.mainloop()
