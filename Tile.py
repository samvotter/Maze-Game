'''
0 = North
1 = East
2 = South
3 = West
'''

# individual tile locations on the board
class Tile:

    def __init__(self, **kwargs):
        # is it the starting tile?
        if "start" in kwargs:
            self.start = kwargs["start"]
        else:
            self.start = False

        # is it the target?
        if "target" in kwargs:
            self.target = kwargs["target"]
        else:
            self.target = False

        # has the player already visited?
        if "visited" in kwargs:
            self.visited = kwargs["visited"]
        else:
            self.visited = False

        # is the target holding anything special?
        if "holding" in kwargs:
            self.holding = kwargs["holding"]
        else:
            self.holding = None

        # what are the connections to this tile?
        self.connections = {0: None,
                            1: None,
                            2: None,
                            3: None,
                            4: None}

        # does this tile have any borders in the associated direction?
        self.borders = {0: None,
                        1: None,
                        2: None,
                        3: None}

        self.X = None
        self.Y = None

        self.image = None

    def createImage(self, frame, BLOCKx, BLOCKy):

        # if the start
        if self.start:
            self.image = frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, (self.X + 1) * BLOCKx, (self.Y + 1) * BLOCKy,
                                   fill="blue")
            frame.pack()

        # if the target
        elif self.target:
            self.image = frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, (self.X + 1) * BLOCKx, (self.Y + 1) * BLOCKy,
                                   fill="red")
            frame.pack()

        # if normal
        else:
            self.image = frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, (self.X + 1) * BLOCKx, (self.Y + 1) * BLOCKy,
                                   fill="white")
            frame.pack()

        # tile borders
        if self.borders[0]:
            frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, (self.X + 1) * BLOCKx, self.Y * BLOCKy + BLOCKy / 10,
                                   fill="black")
            frame.pack()
        if self.borders[1]:
            frame.create_rectangle(self.X * BLOCKx + BLOCKx * (9 / 10), self.Y * BLOCKy, (self.X + 1) * BLOCKx,
                                   (self.Y + 1) * BLOCKy,
                                   fill="black")
            frame.pack()
        if self.borders[2]:
            frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy + BLOCKy * (9 / 10), (self.X + 1) * BLOCKx,
                                   (self.Y + 1) * BLOCKy,
                                   fill="black")
            frame.pack()
        if self.borders[3]:
            frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, self.X * BLOCKx + BLOCKx / 10, (self.Y + 1) * BLOCKy,
                                   fill="black")
            frame.pack()

    def updateImage(self, frame):
        frame.itemconfig(self.image, fill='blue')





