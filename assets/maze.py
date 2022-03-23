from tkinter import Canvas, BOTTOM

from menus import maze_menu as mm
import Store as s
import time as t


class Maze:

    def __init__(self, parent, terrain, **kwargs):
        self.parent = parent
        self.width = parent.winfo_width()
        self.height = parent.winfo_height()*(8/9)

        self.frame = Canvas(parent, width=self.width, height=self.height)
        self.terrain = terrain
        self.player = terrain.player
        self.enemies = terrain.enemies
        self.level = 1

        self.store = s.Store(self.player, self)

        self.BLOCKy = self.height/terrain.rows
        self.BLOCKx = self.width/terrain.cols

        # display
        self.active = True
        if "path" in kwargs:
            if kwargs["path"] == "random":
                self.terrain.randomPath()
                self.terrain.randomizePickups()
                self.terrain.placeMoney()
                self.terrain.checkStartExit()
                self.terrain.checkBarriers()

        self.menu = mm.MazeMenu(parent, self)

        # key bindings
        self.parent.bind('<Left>', self.leftKey)
        self.parent.bind('<Right>', self.rightKey)
        self.parent.bind('<Up>', self.upKey)
        self.parent.bind('<Down>', self.downKey)

        self.parent.bind('<a>', self.leftKey)
        self.parent.bind('<d>', self.rightKey)
        self.parent.bind('<w>', self.upKey)
        self.parent.bind('<s>', self.downKey)

    def unpack(self):
        self.frame.destroy()
        self.menu.frame.destroy()
        del self

    def display(self, **kwargs):
        self.menu.display()
        self.createImage()
        self.frame.pack(side=BOTTOM)
        if kwargs["next"] == "expand":
            while self.active:
                if self.player.loc.target:
                    self.level += 1
                    if self.level % 5 == 0:
                        self.spawnEnemy()
                    self.terrain.expandMap(4)
                    self.placeTarget()
                    for enemy in self.terrain.enemies:
                        if enemy.dead:
                            enemy.loc = self.terrain.randomSpot(0, self.terrain.rows, 0, self.terrain.cols)
                            enemy.loc.evisited = True
                            enemy.dead = False
                            enemy.X = enemy.loc.X
                            enemy.Y = enemy.loc.Y
                            enemy.updateTile(self.frame)
                            enemy.redraw(self.frame, self.BLOCKx, self.BLOCKy)
                    for i in range(self.level):
                        self.terrain.placeMoney()
                    self.updateBlocks()
                    self.redraw()
                self.parent.update()
                t.sleep(.01)
        else:
            while self.active:
                if self.player.loc.target:
                    return True
                else:
                    self.parent.update()

    def updateBlocks(self):
        self.BLOCKy = self.height / self.terrain.rows
        self.BLOCKx = self.width / self.terrain.cols

    def createImage(self):
        self.terrain.createImage(self.frame, self.BLOCKx, self.BLOCKy)

    def redraw(self):
        self.terrain.redraw(self.frame, self.BLOCKx, self.BLOCKy)

    def placeTarget(self):
        self.terrain.placeTarget(self.frame)

    def left(self):
        self.frame.move(self.player.image, -self.BLOCKx, 0)

    def right(self):
        self.frame.move(self.player.image, self.BLOCKx, 0)

    def up(self):
        self.frame.move(self.player.image, 0, -self.BLOCKy)

    def down(self):
        self.frame.move(self.player.image, 0, self.BLOCKy)

    def playerUpdate(self):
        self.player.updateTile(self.frame)

    def enemyUpdate(self):
        for enemy in self.enemies:
            if not enemy.dead:
                enemy.move(self.frame, self.BLOCKx, self.BLOCKy)

    def spawnEnemy(self):
        self.terrain.spawnEnemy()
        self.enemies = self.terrain.enemies
        for enemy in self.enemies:
            enemy.updateTile(self.frame)

    def leftKey(self, event):
        if self.player.active:
            if self.player.move(3):
                self.left()
                self.playerUpdate()
                self.enemyUpdate()
                if self.terrain.detectCollision():
                    print("Dead")

    def rightKey(self, event):
        if self.player.active:
            if self.player.move(1):
                self.right()
                self.playerUpdate()
                self.enemyUpdate()
                if self.terrain.detectCollision():
                    print("Dead")

    def upKey(self, event):
        if self.player.active:
            if self.player.move(0):
                self.up()
                self.playerUpdate()
                self.enemyUpdate()
                if self.terrain.detectCollision():
                    print("Dead")

    def downKey(self, event):
        if self.player.active:
            if self.player.move(2):
                self.down()
                self.playerUpdate()
                self.enemyUpdate()
                if self.terrain.detectCollision():
                    print("Dead")
