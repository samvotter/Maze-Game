import sys
from tkinter import PhotoImage, Checkbutton, LEFT, NW, Canvas
from buttons.buttons import MenuButton

from assets import terrain, maze, player
from menus import tutorial, popup


# start screen buttons
class StartButton(MenuButton):

    def __init__(self, parent, start_screen, art: str = r"menus\start_art\startb.gif", relx: float = 0, rely: float = 0):
        super().__init__(parent=parent, art=art, relx=relx, rely=rely)
        self.startScreen = start_screen

    def behavior(self):
        play_area = maze.Maze(
            self.parent,
            terrain.Terrain(10, 20, player.Player(), [], barriers=True), path="random"
        )
        play_area.terrain.spawn_enemy()
        play_area.display(next="expand")
        self.startScreen.rebuild()


class TutorialButton(MenuButton):

    def __init__(self, parent, start_screen, art: str = r"menus\start_art\tutorialb.gif", relx: float = 0, rely: float = 0):
        super().__init__(parent=parent, art=art, relx=relx, rely=rely)
        self.startScreen = start_screen

    def behavior(self):
        t = tutorial.Tutorial(self.parent)
        t.tutorialSeries()
        self.startScreen.rebuild()


class OptionsButton(MenuButton):

    def __init__(self, parent, art: str = r"menus\start_art\optionsb.gif", relx: float = 0, rely: float = 0):
        super().__init__(parent=parent, art=art, relx=relx, rely=rely)

    def behavior(self):
        options_screen = popup.PopUp(self.parent)
        options_screen.popUpFrame.configure(bg="#F0F0F0")
        Checkbutton(options_screen.popUpFrame, text="Do not automatically purchase more\n"
                                                    "gems from the store if you do not \n"
                                                    "have enough to complete purchase.", justify=LEFT).place(relx=.1, rely=.2)
        Checkbutton(options_screen.popUpFrame, text="Do not sell my account details.", justify=LEFT).place(relx=.1, rely=.3)
        Checkbutton(options_screen.popUpFrame, text="Do not automatically add suggested\n"
                                                    "purchases to my cart.", justify=LEFT).place(relx=.1, rely=.4)
        Checkbutton(options_screen.popUpFrame, text="Sign me up for warranty protection\n"
                                                    "with every purchase.", justify=LEFT).place(relx=.1, rely=.5)
        Checkbutton(options_screen.popUpFrame, text="Don't subscribe me to Super Fun Mazes,\n"
                                                    "a $9.99 monthly periodical.", justify=LEFT).place(relx=.1, rely=.6)
        Checkbutton(options_screen.popUpFrame, text="Email all of my email contacts\n"
                                                    "with the subject line: URGENT!\n"
                                                    "directing them to download this game.", justify=LEFT).place(relx=.1, rely=.7)
        Checkbutton(options_screen.popUpFrame, text="Store my credit card details\n"
                                                    "as plain text.", justify=LEFT).place(relx=.6, rely=.2)
        Checkbutton(options_screen.popUpFrame, text="Give me the option to rate this game\n"
                                                    "something other than 'five stars'.", justify=LEFT).place(relx=.6,
                                                                                                            rely=.3)
        Checkbutton(options_screen.popUpFrame, text="Restore default settings when leaving\n"
                                                    "this menu?", justify=LEFT).place(relx=.6, rely=.4)
        Checkbutton(options_screen.popUpFrame, text="Pay the full price, rather than the\n"
                                                    "listed sale price in the store.", justify=LEFT).place(relx=.6, rely=.5)
        Checkbutton(options_screen.popUpFrame, text="Do not automatically reinstall after\n"
                                                    "being deleted.", justify=LEFT).place(relx=.6, rely=.6)
        Checkbutton(options_screen.popUpFrame, text="Do not prompt me with conformation\n"
                                                    "when making a purchase.", justify=LEFT).place(relx=.6, rely=.7)


class ExitButton(MenuButton):

    def __init__(self, parent, art: str = r"menus\start_art\exitb.gif", relx: float = 0, rely: float = 0):
        super().__init__(parent=parent, art=art, relx=relx, rely=rely)

    def behavior(self):
        sys.exit()


class highButton(MenuButton):

    def __init__(self, parent, art: str = r"menus\start_art\highscoresb.gif", relx: float = 0, rely: float = 0):
        super().__init__(parent=parent, art=art, relx=relx, rely=rely)
        self.scores = PhotoImage(file=r"menus\start_art\scores.gif")

    def behavior(self):
        highscores = popup.PopUp(self.parent)
        highscores.popUpFrame.create_image(0, 0, image=self.scores, anchor=NW)


class StartScreen:

    def __init__(self, parent, width, height):
        self.parent = parent
        self.width = width
        self.height = height
        self.player = player.Player()
        self.image = PhotoImage(file=r"menus\start_art\startscreen.gif")

        self.startCanvas = Canvas(parent, width=self.width, height=self.height)

        self.startCanvas.create_image(0, 0, image=self.image, anchor=NW)

        self.startb = StartButton(self.startCanvas, self, relx=.15, rely=.6)
        self.optionsb = OptionsButton(self.startCanvas, relx=.4, rely=.6)
        self.exitb = ExitButton(self.startCanvas, relx=.7, rely=.6)
        self.highb = highButton(self.startCanvas, relx=.5, rely=.8)
        self.tutorb = TutorialButton(self.startCanvas, self, relx=.2, rely=.8)

        self.startCanvas.pack()

    def rebuild(self):
        self.startCanvas.destroy()
        self.image = PhotoImage(file=r"menus\start_art\startscreen.gif")
        self.startCanvas = Canvas(self.parent, width=self.width, height=self.height)
        self.startCanvas.create_image(0, 0, image=self.image, anchor=NW)

        self.startb = StartButton(self.startCanvas, self, relx=.15, rely=.6)
        self.optionsb = OptionsButton(self.startCanvas, relx=.4, rely=.6)
        self.exitb = ExitButton(self.startCanvas, relx=.7, rely=.6)
        self.highb = highButton(self.startCanvas, relx=.5, rely=.8)
        self.tutorb = TutorialButton(self.startCanvas, self, relx=.2, rely=.8)

        self.startCanvas.pack()
