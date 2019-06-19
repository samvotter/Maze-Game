from tkinter import *
import math
import Popup as p
import Buttons as b
import Store as s


class MazeMenu:

    def __init__(self, parent, WIDTH, HEIGHT, maze):
        # values
        self.width = WIDTH
        self.height = HEIGHT
        self.parent = parent
        self.maze = maze

        # images
        self.giveUpImage = PhotoImage(file="giveup.gif")
        self.storeImage = PhotoImage(file="store.gif")
        self.teleportImage = PhotoImage(file="teleport.gif")
        self.noteleportImage = PhotoImage(file="notele.gif")
        self.resetImage = PhotoImage(file="reset tails.gif")
        self.noresetImage = PhotoImage(file="noreset.gif")

        self.confirmQuit = PhotoImage(file="confirmQuit.gif")

        self.frame = Canvas(self.parent, width=self.width, height=self.height/9, bg="black")

    def display(self):
        self.giveUp = Button(self.frame, command=self.giveUpPU)
        self.giveUp.config(image=self.giveUpImage)
        self.giveUp.place(relx=0, rely=0)

        self.store = Button(self.frame, command=self.storePU)
        self.store.config(image=self.storeImage)
        self.store.place(relx=0.1621, rely=0)

        if self.maze.player.teleport:
            self.tele = Button(self.frame, command=self.tele)
            self.tele.config(image=self.teleportImage)
            self.tele.place(relx=0.702, rely=0)
            self.frame.pack(side=TOP)
        else:
            self.tele = Button(self.frame, command=self.tele)
            self.tele.config(image=self.noteleportImage)
            self.tele.place(relx=0.702, rely=0)
            self.frame.pack(side=TOP)

        if self.maze.player.resetTail:
            self.resetb = Button(self.frame, command=self.resetTails)
            self.resetb.config(image=self.resetImage)
            self.resetb.place(relx=0.481, rely=0)
            self.frame.pack(side=TOP)
        else:
            self.resetb = Button(self.frame)
            self.resetb.config(image=self.noresetImage)
            self.resetb.place(relx=0.481, rely=0)
            self.frame.pack(side=TOP)

    def giveUpPU(self):
        giveupScreen = p.popUp(self.maze.frame, self.width, self.height)
        giveupScreen.popUpFrame.create_image(0, 0, image=self.confirmQuit, anchor=NW)
        confirmQuitYes(giveupScreen, self.maze, .125, .75)
        b.noButton(giveupScreen, .75, .75)


    def storePU(self):
        self.maze.store.createImage(self.maze.frame, self.width, self.height)

    def tele(self):
        if self.maze.player.teleport:
            self.maze.player.teleport -= 1
            if self.maze.player.teleport <= 0:
                self.maze.player.teleport = 0
                self.teleportImage = PhotoImage(file="notele.gif")
                self.tele.config(image=self.teleportImage)
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
                self.resetImage = PhotoImage(file="noreset.gif")
                self.resetb.config(image=self.resetImage)
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


class confirmQuitYes(b.yesButton):

    def __init__(self, parent, maze, x, y):
        super().__init__(parent, x, y)

        self.maze = maze
        self.new = None

        self.store = None

    def behavior(self):
        self.new = PhotoImage(file="cqf.gif")
        cfirm = p.popUp(self.parent.popUpFrame, self.parent.width, self.parent.height)
        cfirm.popUpFrame.create_image(0, 0, image=self.new, anchor=NW)
        failQuitYes(cfirm, self.maze, .125, .75)
        self.store = Button(cfirm.popUpFrame, command=self.maze.menu.storePU)
        self.store.config(image=self.maze.menu.storeImage)
        self.store.place(relx=.275, rely=.75)
        b.noButton(cfirm, .75, .75)

class failQuitYes(b.yesButton):

    def __init__(self, parent, maze, x, y):
        super().__init__(parent, x, y)

        self.maze = maze

    def behavior(self):
        print("Level: ", self.maze.level)
        print("Debt: ", self.maze.player.debt)
        self.maze.unpack()
        self.maze.active = False
        del self.maze

