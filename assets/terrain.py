from assets import tile, enemy

import math
import random


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
        self.land = [[tile.Tile() for j in range(cols)] for i in range(rows)]

        # connect tiles in a dictionary
        self.connect_dictionary()

        self.corners = [self.land[0][0],
                        self.land[0][self.cols-1],
                        self.land[self.rows-1][self.cols-1],
                        self.land[self.rows-1][0]]

        # should there be barriers?
        if "barriers" in kwargs:
            if kwargs["barriers"]:
                self.set_barriers(0, self.rows, 0, self.cols)
        else:
            self.set_barriers(0, self.rows, 0, self.cols)

    def set_corners(self):
        # corners of the map
        self.corners.clear()
        self.corners = [self.land[0][0],
                        self.land[0][self.cols-1],
                        self.land[self.rows-1][self.cols-1],
                        self.land[self.rows-1][0]]

    def closest_corner(self):
        minimum = math.sqrt((self.player.loc.X - self.corners[0].X) ** 2 + (self.player.loc.Y - self.corners[0].Y) ** 2)
        result = 0
        for i in range(len(self.corners)):
            if math.sqrt((self.player.loc.X - self.corners[i].X) ** 2 + (self.player.loc.Y - self.corners[i].Y) ** 2) < minimum:
                minimum = math.sqrt((self.player.loc.X - self.corners[i].X) ** 2 + (self.player.loc.Y - self.corners[i].Y) ** 2)
                result = i
        return result

    def next_map(self, player, enemies):
        return Terrain(int(self.rows*1.2), int(self.cols*1.2), player, enemies)

    def random_path(self):
        # place start and exit
        startx = 0
        starty = 0
        targetx = 0
        targety = 0
        while math.sqrt((startx - targetx) ** 2 + (starty - targety) ** 2) < math.sqrt(self.rows ** 2 + self.cols ** 2) * (2 / 3):
            startx = random.randint(0, self.rows - 1)
            starty = random.randint(0, self.cols - 1)
            targetx = random.randint(0, self.rows - 1)
            targety = random.randint(0, self.cols - 1)
        self.land[startx][starty].start = True
        self.land[startx][starty].visited = True
        self.start = self.land[startx][starty]
        self.land[targetx][targety].target = True
        self.exit = self.land[targetx][targety]

        # place starting player
        self.player.loc = self.land[startx][starty]

    def connect_dictionary(self):
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

    def set_barriers(self, sr, er, sc, ec):
        # set barriers
        i = sr
        while i < er:
            j = sc
            while j < ec:
                roll = random.randint(0, 3)
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

    def check_barriers(self):
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

    def place_target(self, frame):
        diagonal = math.sqrt((self.rows**2) + (self.cols**2))
        self.exit.target = False
        self.exit.reset_tile(frame)

        possible = self.random_spot(0, self.rows, 0, self.cols)
        targetx = possible.Y
        targety = possible.X

        while math.sqrt(((self.player.Y - targetx) ** 2) + (self.player.X - targety) ** 2) < diagonal/4 \
                or self.land[targetx][targety].visited or self.land[targetx][targety].evisited:
                possible = self.random_spot(0, self.rows, 0, self.cols)
                targetx = possible.Y
                targety = possible.X
        self.exit = possible
        self.exit.target = True

    def check_start_exit(self):
        # good start
        valids = []
        for i in range(4):
            self.start.borders[i] = False
            if self.start.connections[i] is not None:
                valids.append(i)
        directions = valids[random.randint(0, len(valids)-1)]
        self.start.connections[directions].holding = "phase"
        for directions in valids:
            self.start.connections[directions].borders[(directions+2) % 4] = False

        # good exit
        valids = []
        for i in range(4):
            self.exit.borders[i] = False
            if self.exit.connections[i] is not None:
                valids.append(i)
        for direction in valids:
            self.exit.connections[direction].borders[(direction+2) % 4] = False

    def randomize_pickups(self):
        for i in range(int((self.rows*self.cols)/70)):
            self.random_spot(0, self.rows, 0, self.cols).holding = "phase"

    def place_money(self):
        self.random_spot(0, self.rows, 0, self.cols).holding = "money"

    def random_enemies(self):
        # place start and exit
        for baddy in self.enemies:
            baddy.loc = self.random_spot(0, self.rows, 0, self.cols)

    def spawn_enemy(self):
        new = enemy.Enemy()
        new.loc = self.random_spot(0, self.rows, 0, self.cols)
        self.enemies.append(new)

    def random_spot(self, sr, er, sc, ec):
        rollx = random.randint(sc, ec-1)
        rolly = random.randint(sr, er-1)
        while self.land[rolly][rollx].visited \
                or self.land[rolly][rollx].evisited \
                or self.land[rolly][rollx].target \
                or self.land[rolly][rollx].holding is not None:
            rollx = random.randint(sc, ec-1)
            rolly = random.randint(sr, er-1)
        return self.land[rolly][rollx]

    def text_print(self):
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

    def create_image(self, frame, BLOCKx, BLOCKy):
        # draw maze
        for row in self.land:
            for col in row:
                # draw tiles
                col.create_image(frame, BLOCKx, BLOCKy)
        self.player.create_image(frame, BLOCKx, BLOCKy)
        for baddy in self.enemies:
            baddy.create_image(frame, BLOCKx, BLOCKy)

    def redraw(self, frame, BLOCKx, BLOCKy):
        # draw maze
        for row in self.land:
            for col in row:
                # draw tiles
                col.resize(frame, BLOCKx, BLOCKy)
        self.player.redraw(frame, BLOCKx, BLOCKy)
        for baddy in self.enemies:
            baddy.redraw(frame, BLOCKx, BLOCKy)

    def detect_collision(self):
        for baddy in self.enemies:
            if baddy.loc == self.player.loc:
                return True
        return False

    def expand_map(self, x):
        oldr = self.rows
        oldc = self.cols
        self.rows += x
        self.cols += x
        direction = self.closest_corner()
        if direction == 0:
            self.shiftNW(x)
        elif direction == 1:
            self.shiftNE(oldc, x)
        elif direction == 2:
            self.shiftSE(oldr, oldc, x)
        else:
            self.shiftSW(oldr, x)
        self.set_corners()

    def shiftNW(self, x):
        # redraw bounds of maze
        for i in range(x):
            self.land.insert(0, [])
        for i in range(self.rows):
            if i < x:
                for j in range(self.cols):
                    self.land[i].append(tile.Tile())
            else:
                for j in range(x):
                    self.land[i].insert(0, tile.Tile())

        self.connect_dictionary()
        self.player.X = self.player.loc.X
        self.player.Y = self.player.loc.Y

        for baddy in self.enemies:
            baddy.X = baddy.loc.X
            baddy.Y = baddy.loc.Y

        self.set_barriers(0, x, 0, self.cols)
        self.set_barriers(x, self.rows, 0, x)

        self.check_barriers()

        self.random_spot(0, x, 0, self.cols).holding = "phase"
        self.random_spot(0, self.rows, 0, x).holding = "phase"

    def shiftNE(self, oldc, x):
        # redraw bounds of maze
        for i in range(x):
            self.land.insert(0, [])
        for i in range(0, self.rows):
            if i < x:
                for j in range(self.cols):
                    self.land[i].append(tile.Tile())
            else:
                for j in range(x):
                    self.land[i].append(tile.Tile())

        self.connect_dictionary()
        self.player.X = self.player.loc.X
        self.player.Y = self.player.loc.Y

        for baddy in self.enemies:
            baddy.X = baddy.loc.X
            baddy.Y = baddy.loc.Y

        self.set_barriers(0, x, 0, self.cols)
        self.set_barriers(x, self.rows, oldc, self.cols)

        self.check_barriers()

        self.random_spot(0, x, 0, self.cols).holding = "phase"
        self.random_spot(x, self.rows, oldc, self.cols).holding = "phase"

    def shiftSW(self, oldr, x):
        for row in self.land:
            for i in range(x):
                row.insert(0, tile.Tile())
        for i in range(x):
            self.land.append([tile.Tile() for j in range(self.cols)])

        # connect the dictionary
        self.connect_dictionary()
        self.player.X = self.player.loc.X
        self.player.Y = self.player.loc.Y

        for baddy in self.enemies:
            baddy.X = baddy.loc.X
            baddy.Y = baddy.loc.Y

        # set barriers
        self.set_barriers(0, oldr, 0, x)
        self.set_barriers(oldr, self.rows, 0, self.cols)

        self.check_barriers()

        self.random_spot(0, oldr, 0, x).holding = "phase"
        self.random_spot(oldr, self.rows, 0, self.cols).holding = "phase"

    def shiftSE(self, oldr, oldc, x):
        # redraw bounds of maze
        for row in self.land:
            for i in range(x):
                row.append(tile.Tile())
        for i in range(x):
            self.land.append([tile.Tile() for j in range(self.cols)])
        # connect the dictionary
        self.connect_dictionary()

        for baddy in self.enemies:
            baddy.X = baddy.loc.X
            baddy.Y = baddy.loc.Y

        # set barriers
        self.set_barriers(0, oldr, oldc, self.cols)
        self.set_barriers(oldr, self.rows, 0, self.cols)

        self.check_barriers()

        self.random_spot(0, oldr, oldc, self.cols).holding = "phase"
        self.random_spot(oldr, self.rows, 0, self.cols).holding = "phase"

    def insertEnemies(self, enemies):
        self.enemies = enemies
