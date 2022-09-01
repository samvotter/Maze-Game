from tkinter import Canvas, BOTTOM

from menus import maze_menu as mm, store as s
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
                self.terrain.random_path()
                self.terrain.randomize_pickups()
                self.terrain.place_money()
                self.terrain.check_start_exit()
                self.terrain.check_barriers()

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
                        self.spawn_enemy()
                    self.terrain.expand_map(4)
                    self.placeTarget()
                    for enemy in self.terrain.enemies:
                        if enemy.dead:
                            enemy.loc = self.terrain.random_spot(0, self.terrain.rows, 0, self.terrain.cols)
                            enemy.loc.evisited = True
                            enemy.dead = False
                            enemy.X = enemy.loc.X
                            enemy.Y = enemy.loc.Y
                            enemy.updateTile(self.frame)
                            enemy.redraw(self.frame, self.BLOCKx, self.BLOCKy)
                    for i in range(self.level):
                        self.terrain.place_money()
                    self.updateBlocks()
                    self.redraw()
                self.parent.update()
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
        self.terrain.create_image(self.frame, self.BLOCKx, self.BLOCKy)

    def redraw(self):
        self.terrain.redraw(self.frame, self.BLOCKx, self.BLOCKy)

    def placeTarget(self):
        self.terrain.place_target(self.frame)

    def left(self):
        self.frame.move(self.player.image, -self.BLOCKx, 0)

    def right(self):
        self.frame.move(self.player.image, self.BLOCKx, 0)

    def up(self):
        self.frame.move(self.player.image, 0, -self.BLOCKy)

    def down(self):
        self.frame.move(self.player.image, 0, self.BLOCKy)

    def player_update(self):
        self.player.updateTile(self.frame)

    def enemy_update(self):
        for enemy in self.enemies:
            if not enemy.dead:
                enemy.move(self.frame, self.BLOCKx, self.BLOCKy)

    def spawn_enemy(self):
        self.terrain.spawn_enemy()
        self.enemies = self.terrain.enemies
        for enemy in self.enemies:
            enemy.updateTile(self.frame)

    def leftKey(self, event):
        if self.player.active:
            if self.player.move(3):
                self.left()
                self.player_update()
                self.enemy_update()
                if self.terrain.detect_collision():
                    print("Dead")

    def rightKey(self, event):
        if self.player.active:
            if self.player.move(1):
                self.right()
                self.player_update()
                self.enemy_update()
                if self.terrain.detect_collision():
                    print("Dead")

    def upKey(self, event):
        if self.player.active:
            if self.player.move(0):
                self.up()
                self.player_update()
                self.enemy_update()
                if self.terrain.detect_collision():
                    print("Dead")

    def downKey(self, event):
        if self.player.active:
            if self.player.move(2):
                self.down()
                self.player_update()
                self.enemy_update()
                if self.terrain.detect_collision():
                    print("Dead")
