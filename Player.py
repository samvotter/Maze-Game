
'''
0 = North
1 = East
2 = South
3 = West
'''


class Player:

    def __init__(self):
        self.loc = None

        # can pass through 3x barriers
        self.phase = False

        # teleport to a random location
        self.teleport = False

        self.image = None
        self.X = None
        self.Y = None


    def lookup(self, NESW):
        # are there any spaces where the player can move?
        if self.loc.connections[NESW] is None:
            return False
        elif self.loc.connections[NESW].visited:
            return False
        elif self.loc.borders[NESW]:
            return False
        else:
            return True

    def move(self, dir):
        if self.lookup(dir):
            self.loc = self.loc.connections[dir]
            self.loc.visited = True
            return True
        else:
            return False

    def createImage(self, frame, BLOCKx, BLOCKy):
        self.X = self.loc.X
        self.Y = self.loc.Y
        self.image = frame.create_oval(self.X * BLOCKx + BLOCKx/5, self.Y * BLOCKy + BLOCKy/5,
                                       (self.X + 1) * BLOCKx - BLOCKx/5, (self.Y + 1) * BLOCKy - BLOCKy/5,
                                        fill="light blue")
        frame.pack()








