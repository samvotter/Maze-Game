from tkinter import *
from menus import popup
from buttons import buttons


class MazeMenu:

    def __init__(self, parent, maze):
        # values
        self.parent = parent
        self.width = parent.winfo_width()
        self.height = parent.winfo_height()
        self.maze = maze

        # images
        self.giveUpImage = PhotoImage(file=r"menus\maze_menu_art\giveup.gif")
        self.storeImage = PhotoImage(file=r"menus\maze_menu_art\store.gif")
        self.teleportImage = PhotoImage(file=r"menus\maze_menu_art\teleport.gif")
        self.noteleportImage = PhotoImage(file=r"menus\maze_menu_art\notele.gif")
        self.resetImage = PhotoImage(file=r"menus\maze_menu_art\reset tails.gif")
        self.noresetImage = PhotoImage(file=r"menus\maze_menu_art\noreset.gif")
        self.confirmQuit = PhotoImage(file=r"menus\maze_menu_art\confirmQuit.gif")

        self.frame = Canvas(self.parent, width=self.width, height=self.height / 9, bg="black")

        # buttons
        self.give_up_button = Button(self.frame, command=self.giveUpPU)
        self.store_button = Button(self.frame, command=self.storePU)
        self.tele_button = Button(self.frame, command=self.tele)
        self.reset_button = Button(self.frame)

    def display(self):
        self.give_up_button.config(image=self.giveUpImage)
        self.give_up_button.place(relx=0, rely=0)

        self.store_button.config(image=self.storeImage)
        self.store_button.place(relx=0.1621, rely=0)

        if self.maze.player.teleport:
            self.tele_button = Button(self.frame, command=self.tele)
            self.tele_button.config(image=self.teleportImage)
            self.tele_button.place(relx=0.702, rely=0)
            self.frame.pack(side=TOP)
        else:
            self.tele_button.config(image=self.noteleportImage)
            self.tele_button.place(relx=0.702, rely=0)
            self.frame.pack(side=TOP)

        if self.maze.player.resetTail:
            self.reset_button = Button(self.frame, command=self.resetTails)
            self.reset_button.config(image=self.resetImage)
            self.reset_button.place(relx=0.481, rely=0)
            self.frame.pack(side=TOP)
        else:
            self.reset_button.config(image=self.noresetImage)
            self.reset_button.place(relx=0.481, rely=0)
            self.frame.pack(side=TOP)

    def giveUpPU(self):
        giveupScreen = popup.PopUp(self.maze.frame)
        giveupScreen.popUpFrame.create_image(0, 0, image=self.confirmQuit, anchor=NW)
        ConfirmQuitYes(giveupScreen, self.maze, relx=.125, rely=.75)
        buttons.NoButton(giveupScreen, relx=.75, rely=.75)

    def storePU(self):
        self.maze.store.createImage(self.maze.frame, self.width, self.height)

    def tele(self):
        if self.maze.player.teleport:
            self.maze.player.teleport -= 1
            if self.maze.player.teleport <= 0:
                self.maze.player.teleport = 0
                self.teleportImage = PhotoImage(file=r"menus\maze_menu_art\notele.gif")
                self.tele_button.config(image=self.teleportImage)
            self.maze.player.loc.teleported = True
            self.maze.frame.itemconfig(self.maze.player.loc.image, fill="#944CDC")
            self.maze.player.loc = self.maze.terrain.randomSpot(0, self.maze.terrain.rows, 0, self.maze.terrain.cols)
            self.maze.player.X = self.maze.player.loc.X
            self.maze.player.Y = self.maze.player.loc.Y
            self.maze.player.loc.visited = True
            self.maze.frame.delete(self.maze.player.image)
            self.maze.player.redraw(self.maze.frame, self.maze.BLOCKx, self.maze.BLOCKy)
            self.maze.player.loc.teleported = True
            self.maze.frame.itemconfig(self.maze.player.loc.image, fill="#944CDC")
            self.parent.update()

    def resetTails(self):
        if self.maze.player.resetTail:
            self.maze.player.resetTail -= 1
            if self.maze.player.resetTail <= 0:
                self.maze.player.resetTail = 0
                self.resetImage = PhotoImage(file=r"menus\maze_menu_art\noreset.gif")
                self.reset_button.config(image=self.resetImage)
            for row in self.maze.terrain.land:
                for tile in row:
                    tile.visited = False
                    tile.evisited = False
                    tile.phased = False
                    tile.teleported = False
            for enemy in self.maze.terrain.enemies:
                enemy.dead = False
            self.maze.player.loc.visited = True
            for enemy in self.maze.terrain.enemies:
                enemy.loc.evisited = True
            self.maze.redraw()


class ConfirmQuitYes(buttons.YesButton):

    def __init__(self, parent, maze, relx: float = 0, rely: float = 0):
        super().__init__(parent, relx=relx, rely=rely)
        self.maze = maze
        self.new = None
        self.store = None

    def behavior(self):
        self.new = PhotoImage(file=r"menus\maze_menu_art\cqf.gif")
        cfirm = popup.PopUp(self.parent.parent)
        cfirm.popUpFrame.create_image(0, 0, image=self.new, anchor=NW)
        failQuitYes(cfirm, self.maze, .125, .75)
        self.store = Button(cfirm.popUpFrame, command=self.maze.menu.storePU)
        self.store.config(image=self.maze.menu.storeImage)
        self.store.place(relx=.275, rely=.75)
        buttons.NoButton(cfirm, relx=.75, rely=.75)


class failQuitYes(buttons.YesButton):

    def __init__(self, parent, maze, x, y):
        super().__init__(parent, relx=x, rely=y)

        self.maze = maze

    def behavior(self):
        print("Level: ", self.maze.level)
        print("Debt: ", self.maze.player.debt)
        self.maze.unpack()
        self.maze.active = False
        del self.maze

