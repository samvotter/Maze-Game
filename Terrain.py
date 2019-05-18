import Tile as t

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

    def __init__(self, rows, cols, player):
        self.player = player
        self.rows = rows
        self.cols = cols

        # create player image
        self.playerImage = None

        # create list of tiles
        self.land = []
        for i in range(0, rows):
            self.land.append([])
            for j in range(0, cols):
                self.land[i].append(t.Tile())

        # connect tiles in a dictionary
        for i in range(0, rows):
            for j in range(0, cols):
                self.land[i][j].X = j
                self.land[i][j].Y = i
                if i > 0:
                    self.land[i][j].connections[0] = self.land[i-1][j]
                if i < rows-1:
                    self.land[i][j].connections[2] = self.land[i+1][j]
                if j > 0:
                    self.land[i][j].connections[3] = self.land[i][j-1]
                if j < cols-1:
                    self.land[i][j].connections[1] = self.land[i][j+1]

    def nextMap(self, player):
        return Terrain(self.rows+1, self.cols+1, player)

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
        self.land[targetx][targety].target = True

        # place starting player
        self.player.loc = self.land[startx][starty]

        # set barriers
        for i in range(self.rows):
            for j in range(self.cols):
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

    def textPrint(self):
        for row in self.land:
            for col in row:
                if col.start:
                    print("[S]", end=" ")
                elif col.target:
                    print("[T]", end=" ")
                elif self.player.loc == col and not self.player.loc.start:
                    print("[P]", end=" ")
                else:
                    print("[ ]", end=" ")
            print()

    def createImage(self, frame, WIDTH, HEIGHT):
        # draw maze
        BLOCKx = WIDTH/self.rows
        BLOCKy = HEIGHT/self.cols
        for row in range(self.rows):
            for col in range(self.cols):
                # draw tiles
                self.land[row][col].createImage(frame, BLOCKx, BLOCKy)
        self.player.createImage(frame, BLOCKx, BLOCKy)



















