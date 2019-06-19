import Tile as t
import Enemies as e
import Player as p

import math as m
import random as r
from tkinter import *


'''
0 = North
1 = East
2 = South
3 = West
'''

class Terrain:

    def __init__(self, rows, cols, player, enemies, **kwargs):
        self.player = player
        self.enemies = enemies
        self.rows = rows
        self.cols = cols
        self.start = None
        self.exit = None

        # create player image
        self.playerImage = None

        # create list of tiles
        self.land = []
        for i in range(0, rows):
            self.land.append([])
            for j in range(0, cols):
                self.land[i].append(t.Tile())

        # connect tiles in a dictionary
        self.connectDictionary()

        self.corners = [self.land[0][0],
                        self.land[0][self.cols-1],
                        self.land[self.rows-1][self.cols-1],
                        self.land[self.rows-1][0]]

        # should there be barriers?
        if "barriers" in kwargs:
            if kwargs["barriers"]:
                self.setBarriers(0, self.rows, 0, self.cols)
        else:
            self.setBarriers(0, self.rows, 0, self.cols)


    def setCorners(self):
        # corners of the map
        self.corners.clear()
        self.corners = [self.land[0][0],
                        self.land[0][self.cols-1],
                        self.land[self.rows-1][self.cols-1],
                        self.land[self.rows-1][0]]

    def closestCorner(self):
        min = m.sqrt((self.player.loc.X - self.corners[0].X) ** 2 + (self.player.loc.Y - self.corners[0].Y) ** 2)
        result = 0
        for i in range(len(self.corners)):
            if m.sqrt((self.player.loc.X - self.corners[i].X) ** 2 + (self.player.loc.Y - self.corners[i].Y) ** 2) < min:
                min = m.sqrt((self.player.loc.X - self.corners[i].X) ** 2 + (self.player.loc.Y - self.corners[i].Y) ** 2)
                result = i
        return result

    def nextMap(self, player, enemies):
        return Terrain(int(self.rows*1.2), int(self.cols*1.2), player, enemies)

    def randomPath(self):
        # place start and exit
        startx = 0
        starty = 0
        targetx = 0
        targety = 0
        while m.sqrt((startx - targetx) ** 2 + (starty - targety) ** 2) < m.sqrt(self.rows ** 2 + self.cols ** 2) * (2 / 3):
            startx = r.randint(0, self.rows - 1)
            starty = r.randint(0, self.cols - 1)
            targetx = r.randint(0, self.rows - 1)
            targety = r.randint(0, self.cols - 1)
        self.land[startx][starty].start = True
        self.land[startx][starty].visisted = True
        self.start = self.land[startx][starty]
        self.land[targetx][targety].target = True
        self.exit = self.land[targetx][targety]

        # place starting player
        self.player.loc = self.land[startx][starty]

    def connectDictionary(self):
        # connect the dictionary
        for i in range(self.rows):
            for j in range(self.cols):
                self.land[i][j].X = j
                self.land[i][j].Y = i
                if i > 0:
                    self.land[i][j].connections[0] = self.land[i-1][j]
                if i < self.rows-1:
                    self.land[i][j].connections[2] = self.land[i+1][j]
                if j > 0:
                    self.land[i][j].connections[3] = self.land[i][j-1]
                if j < self.cols-1:
                    self.land[i][j].connections[1] = self.land[i][j+1]

    def setBarriers(self, sr, er, sc, ec):
        # set barriers
        i = sr
        while i < er:
            j = sc
            while j < ec:
                roll = r.randint(0, 3)
                self.land[i][j].borders[roll] = 1
                if roll == 0 and i > 0:
                    self.land[i-1][j].borders[2] = 1
                elif roll == 1 and j < self.cols - 1:
                    self.land[i][j+1].borders[3] = 1
                elif roll == 2 and i < self.rows - 1:
                    self.land[i+1][j].borders[0] = 1
                elif roll == 3 and j > 0:
                    self.land[i][j-1].borders[1] = 1
                j += 1
            i += 1

    def checkBarriers(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.land[i][j].borders[0] and self.land[i][j].connections[0] is not None:
                    self.land[i][j].connections[0].borders[2] = True
                if self.land[i][j].borders[1] and self.land[i][j].connections[1] is not None:
                    self.land[i][j].connections[1].borders[3] = True
                if self.land[i][j].borders[2] and self.land[i][j].connections[2] is not None:
                    self.land[i][j].connections[2].borders[0] = True
                if self.land[i][j].borders[3] and self.land[i][j].connections[3] is not None:
                    self.land[i][j].connections[3].borders[1] = True

    def placeTarget(self, frame):
        diagonal = m.sqrt((self.rows**2) + (self.cols**2))
        self.exit.target = False
        self.exit.resetTile(frame)

        possible = self.randomSpot(0, self.rows, 0, self.cols)
        targetx = possible.Y
        targety = possible.X

        while m.sqrt(((self.player.Y - targetx) ** 2) + (self.player.X - targety) ** 2) < diagonal/4 \
                or self.land[targetx][targety].visited or self.land[targetx][targety].evisited:
                possible = self.randomSpot(0, self.rows, 0, self.cols)
                targetx = possible.Y
                targety = possible.X
        self.exit = possible
        self.exit.target = True

    def checkStartExit(self):
        # good start
        valids = []
        for i in range(4):
            self.start.borders[i] = False
            if self.start.connections[i] is not None:
                valids.append(i)
        dir = valids[r.randint(0, len(valids)-1)]
        self.start.connections[dir].holding = "phase"
        for dir in valids:
            self.start.connections[dir].borders[(dir+2) % 4] = False

        # good exit
        valids = []
        for i in range(4):
            self.exit.borders[i] = False
            if self.exit.connections[i] is not None:
                valids.append(i)
        for dir in valids:
            self.exit.connections[dir].borders[(dir+2) % 4] = False


    def randomizePickups(self):
        for i in range(int((self.rows*self.cols)/70)):
            self.randomSpot(0, self.rows, 0, self.cols).holding = "phase"

    def placeMoney(self):
        self.randomSpot(0, self.rows, 0, self.cols).holding = "money"

    def randomEnemies(self):
        # place start and exit
        for enemy in self.enemies:
            enemy.loc = self.randomSpot(0, self.rows, 0, self.cols)

    def spawnEnemy(self):
        new = e.Enemy()
        new.loc = self.randomSpot(0, self.rows, 0, self.cols)
        self.enemies.append(new)

    def randomSpot(self, sr, er, sc, ec):
        rollx = r.randint(sc, ec-1)
        rolly = r.randint(sr, er-1)
        while self.land[rolly][rollx].visited \
                or self.land[rolly][rollx].evisited \
                or self.land[rolly][rollx].target \
                or self.land[rolly][rollx].holding is not None:
            rollx = r.randint(sc, ec-1)
            rolly = r.randint(sr, er-1)
        return self.land[rolly][rollx]

    def textPrint(self):
        for row in self.land:
            for col in row:
                if col.start:
                    print("[S]", end=" ")
                elif col.target:
                    print("[T]", end=" ")
                elif col.holding == "phase":
                    print("[h]", end=" ")
                elif col.holding == "money":
                    print("[m]", end=" ")
                elif self.player.loc == col and not self.player.loc.start:
                    print("[P]", end=" ")
                else:
                    print("[ ]", end=" ")
            print()

    def createImage(self, frame, BLOCKx, BLOCKy):
        # draw maze
        for row in self.land:
            for col in row:
                # draw tiles
                col.createImage(frame, BLOCKx, BLOCKy)
        self.player.createImage(frame, BLOCKx, BLOCKy)
        for enemy in self.enemies:
            enemy.createImage(frame, BLOCKx, BLOCKy)

    def redraw(self, frame, BLOCKx, BLOCKy):
        # draw maze
        for row in self.land:
            for col in row:
                # draw tiles
                col.resize(frame, BLOCKx, BLOCKy)
        self.player.redraw(frame, BLOCKx, BLOCKy)
        for enemy in self.enemies:
            enemy.redraw(frame, BLOCKx, BLOCKy)

    def detectCollision(self):
        for enemy in self.enemies:
            if enemy.loc == self.player.loc:
                return True
        return False

    def expandMap(self, x):
        oldr = self.rows
        oldc = self.cols
        self.rows += x
        self.cols += x
        dir = self.closestCorner()
        if dir == 0:
            self.shiftNW(x)
        elif dir == 1:
            self.shiftNE(oldc, x)
        elif dir == 2:
            self.shiftSE(oldr, oldc, x)
        else:
            self.shiftSW(oldr, oldc, x)
        self.setCorners()

    def shiftNW(self, x):
        # redraw bounds of maze
        for i in range(x):
            self.land.insert(0, [])
        for i in range(0, self.rows):
            if i < x:
                for j in range(self.cols):
                    self.land[i].append(t.Tile())
            else:
                for j in range(x):
                    self.land[i].insert(0, t.Tile())
        self.connectDictionary()
        self.player.X = self.player.loc.X
        self.player.Y = self.player.loc.Y
        for enemy in self.enemies:
            enemy.X = enemy.loc.X
            enemy.Y = enemy.loc.Y
        self.setBarriers(0, x, 0, self.cols)
        self.setBarriers(x, self.rows, 0, x)

        self.checkBarriers()

        self.randomSpot(0, x, 0, self.cols).holding = "phase"
        self.randomSpot(0, self.rows, 0, x).holding = "phase"

    def shiftNE(self, oldc, x):
        # redraw bounds of maze
        for i in range(x):
            self.land.insert(0, [])
        for i in range(0, self.rows):
            if i < x:
                for j in range(self.cols):
                    self.land[i].append(t.Tile())
            else:
                for j in range(x):
                    self.land[i].append(t.Tile())
        self.connectDictionary()
        self.player.X = self.player.loc.X
        self.player.Y = self.player.loc.Y
        for enemy in self.enemies:
            enemy.X = enemy.loc.X
            enemy.Y = enemy.loc.Y
        self.setBarriers(0, x, 0, self.cols)
        self.setBarriers(x, self.rows, oldc, self.cols)

        self.checkBarriers()

        self.randomSpot(0, x, 0, self.cols).holding = "phase"
        self.randomSpot(x, self.rows, oldc, self.cols).holding = "phase"


    def shiftSW(self, oldr, oldc, x):
        for row in self.land:
            for i in range(0, x):
                row.insert(0, t.Tile())
        for i in range(0, x):
            self.land.append([])
            for j in range(0, self.cols):
                self.land[oldr+i].append(t.Tile())
        # connect the dictionary
        self.connectDictionary()
        self.player.X = self.player.loc.X
        self.player.Y = self.player.loc.Y
        for enemy in self.enemies:
            enemy.X = enemy.loc.X
            enemy.Y = enemy.loc.Y

        # set barriers
        self.setBarriers(0, oldr, 0, x)
        self.setBarriers(oldr, self.rows, 0, self.cols)

        self.checkBarriers()

        self.randomSpot(0, oldr, 0, x).holding = "phase"
        self.randomSpot(oldr, self.rows, 0, self.cols).holding = "phase"

    def shiftSE(self, oldr, oldc, x):
        # redraw bounds of maze
        for row in self.land:
            for i in range(0, x):
                row.append(t.Tile())
        for i in range(0, x):
            self.land.append([])
            for j in range(0, self.cols):
                self.land[oldr+i].append(t.Tile())
        # connect the dictionary
        self.connectDictionary()

        for enemy in self.enemies:
            enemy.X = enemy.loc.X
            enemy.Y = enemy.loc.Y

        # set barriers
        self.setBarriers(0, oldr, oldc, self.cols)
        self.setBarriers(oldr, self.rows, 0, self.cols)

        self.checkBarriers()

        self.randomSpot(0, oldr, oldc, self.cols).holding = "phase"
        self.randomSpot(oldr, self.rows, 0, self.cols).holding = "phase"

    def insertEnemies(self, enemies):
        self.enemies = enemies























