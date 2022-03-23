from tkinter import PhotoImage, NW
from assets import terrain, maze, player
from menus import popup
import copy


class Tutorial:

    def __init__(self, parent):
        self.parent = parent
        self.width = parent.winfo_width()
        self.height = parent.winfo_height()

        self.bmImage = PhotoImage(file=r"menus\tutorial_art/tutorialbasicmovement.gif")
        self.tImage = PhotoImage(file=r"menus\tutorial_art/tutorialtele.gif")
        self.wImage = PhotoImage(file=r"menus\tutorial_art/tutorialwalls.gif")
        self.eImage = PhotoImage(file=r"menus\tutorial_art/tutorialenemies.gif")
        self.rImage = PhotoImage(file=r"menus\tutorial_art/tutorialreset.gif")

        self.moneyTracker = 0

        # images

    def blank(self):
        return terrain.Terrain(5, 10, player.Player(), [], barriers=0)

    def basicMovement(self):
        bm = maze.Maze(self.parent, self.blank())
        bm.player.loc = bm.terrain.land[0][0]
        bm.player.loc.start = True
        bm.terrain.land[4][9].target = True
        info = popup.PopUp(self.parent)
        info.popUpFrame.create_image(0, 0, image=self.bmImage, anchor=NW)

        for i in range(10):
            bm.terrain.placeMoney()

        bm.display(next=0)
        self.moneyTracker = copy.deepcopy(bm.player.debt)
        bm.unpack()

    def walls(self):
        w = maze.Maze(self.parent, self.blank())
        w.terrain.land[4][9].target = True

        # horizontal line
        for i in range(10):
            w.terrain.land[2][i].borders[0] = True

        w.terrain.land[1][3].holding = "phase"

        # vertical lines
        for i in range(5):
            w.terrain.land[i][3].borders[1] = True

        w.terrain.land[0][4].holding = "phase"
        w.terrain.land[4][3].holding = "phase"
        w.terrain.land[2][5].holding = "phase"

        for i in range(5):
            w.terrain.land[i][7].borders[1] = True

        w.terrain.land[0][9].holding = "phase"

        w.terrain.checkBarriers()
        w.player.loc = w.terrain.land[0][0]
        w.player.loc.start = True
        w.player.debt = self.moneyTracker

        info = popup.PopUp(self.parent)
        info.popUpFrame.create_image(0, 0, image=self.wImage, anchor=NW)

        w.display(next=0)
        self.moneyTracker = copy.deepcopy(w.player.debt)
        w.unpack()

    def teleporting(self):
        tp = maze.Maze(self.parent, self.blank())
        tp.terrain.land[0][9].target = True
        tp.player.loc = tp.terrain.land[4][0]
        tp.player.loc.start = True
        tp.player.debt = self.moneyTracker

        # vertical lines
        for i in range(5):
            tp.terrain.land[i][3].borders[1] = True

        info = popup.PopUp(self.parent)
        info.popUpFrame.create_image(0, 0, image=self.tImage, anchor=NW)

        tp.display(next=0)
        self.moneyTracker = copy.deepcopy(tp.player.debt)
        tp.unpack()

    def enemies(self):
        em = maze.Maze(self.parent, self.blank())
        em.spawnEnemy()
        for enemy in em.terrain.enemies:
            enemy.loc = em.terrain.land[3][5]
            enemy.X = enemy.loc.X
            enemy.Y = enemy.loc.Y

        em.player.loc = em.terrain.land[0][0]
        em.player.loc.start = True
        em.player.debt = self.moneyTracker
        em.terrain.land[4][9].target = True
        em.terrain.exit = em.terrain.land[4][9]

        # box around enemy
        # vertical lines
        for i in range(3):
            em.terrain.land[i+1][5].borders[1] = True
            em.terrain.land[i+1][4].borders[1] = True
        # horizontal lines
        em.terrain.land[4][5].borders[0] = True

        em.terrain.checkBarriers()

        info = popup.PopUp(self.parent)
        info.popUpFrame.create_image(0, 0, image=self.eImage, anchor=NW)

        em.display(next=0)
        self.moneyTracker = copy.deepcopy(em.player.debt)
        em.unpack()

    def tails(self):
        ts = maze.Maze(self.parent, self.blank())
        ts.player.teleport = False
        ts.player.loc = ts.terrain.land[0][9]
        ts.player.loc.start = True
        ts.player.debt = self.moneyTracker
        ts.terrain.land[4][0].target = True

        ts.spawnEnemy()
        ts.spawnEnemy()
        ts.terrain.enemies[0].loc = ts.terrain.land[3][0]
        ts.terrain.enemies[0].X = ts.terrain.enemies[0].loc.X
        ts.terrain.enemies[0].Y = ts.terrain.enemies[0].loc.Y
        ts.terrain.enemies[1].loc = ts.terrain.land[4][1]
        ts.terrain.enemies[1].X = ts.terrain.enemies[1].loc.X
        ts.terrain.enemies[1].Y = ts.terrain.enemies[1].loc.Y

        info = popup.PopUp(self.parent)
        info.popUpFrame.create_image(0, 0, image=self.rImage, anchor=NW)

        ts.display(next=0)
        ts.unpack()

    def tutorialSeries(self):
        self.basicMovement()
        self.teleporting()
        self.walls()
        self.enemies()
        self.tails()
        del self
