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
        self.start = False
        if "start" in kwargs:
            self.start = kwargs["start"]

        # is it the target?
        self.target = False
        if "target" in kwargs:
            self.target = kwargs["target"]

        # has the player already visited?
        self.visited = False
        if "visited" in kwargs:
            self.visited = kwargs["visited"]

        # has an enemy already visited?
        self.evisited = False
        if "visited" in kwargs:
            self.evisited = kwargs["visited"]

        # is the target holding anything special?
        self.holding = None
        if "holding" in kwargs:
            self.holding = kwargs["holding"]

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

        self.teleported = False

        self.X = None
        self.Y = None

        self.image = None
        self.phaseImage = None
        self.phased = False

    def createImage(self, frame, BLOCKx, BLOCKy):

        frame.delete(self.image)

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

        # if the tile is holding
        if self.holding == "phase":
            self.phaseImage = frame.create_oval(self.X * BLOCKx + BLOCKx / 5, self.Y * BLOCKy + BLOCKy / 5,
                                           (self.X + 1) * BLOCKx - BLOCKx / 5, (self.Y + 1) * BLOCKy - BLOCKy / 5,
                                           fill="#66FF00")
        elif self.holding == "money":
            self.phaseImage = frame.create_rectangle(self.X * BLOCKx + BLOCKx / 8, self.Y * BLOCKy + BLOCKy / 3,
                                                (self.X + 1) * BLOCKx - BLOCKx / 8, (self.Y + 1) * BLOCKy - BLOCKy / 3,
                                                fill="green")

    def resetTile(self, frame):
        frame.itemconfig(self.image, fill="white")

    def resize(self, frame, BLOCKx, BLOCKy):
        # if target
        if self.target:
            self.image = frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, (self.X + 1) * BLOCKx,
                                                (self.Y + 1) * BLOCKy,
                                                fill="red")
            frame.pack()

        # if teleported
        elif self.teleported:
            self.image = frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, (self.X + 1) * BLOCKx,
                                                (self.Y + 1) * BLOCKy,
                                                fill="#944CDC")
            frame.pack()
        # if phased
        elif self.phased:
            self.image = frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, (self.X + 1) * BLOCKx,
                                                (self.Y + 1) * BLOCKy,
                                                fill="#00FF77")

        # if visited
        elif self.visited:
            self.image = frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, (self.X + 1) * BLOCKx,
                                                (self.Y + 1) * BLOCKy,
                                                fill="blue")
            frame.pack()
        # if evisited
        elif self.evisited:
            self.image = frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, (self.X + 1) * BLOCKx,
                                                (self.Y + 1) * BLOCKy,
                                                fill="orange")
            frame.pack()

        # if normal
        else:
            self.image = frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, (self.X + 1) * BLOCKx,
                                                (self.Y + 1) * BLOCKy,
                                                fill="white")
            frame.pack()

        # tile borders
        if self.borders[0]:
            frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, (self.X + 1) * BLOCKx,
                                   self.Y * BLOCKy + BLOCKy / 10,
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
            frame.create_rectangle(self.X * BLOCKx, self.Y * BLOCKy, self.X * BLOCKx + BLOCKx / 10,
                                   (self.Y + 1) * BLOCKy,
                                   fill="black")
            frame.pack()

        # if the tile is holding
        if self.holding == "phase":
            self.phaseImage = frame.create_oval(self.X * BLOCKx + BLOCKx / 5, self.Y * BLOCKy + BLOCKy / 5,
                                                (self.X + 1) * BLOCKx - BLOCKx / 5, (self.Y + 1) * BLOCKy - BLOCKy / 5,
                                                fill="#66FF00")

        elif self.holding == "money":
            self.phaseImage = frame.create_rectangle(self.X * BLOCKx + (BLOCKx / 8), self.Y * BLOCKy + BLOCKy / 3,
                                                (self.X + 1) * BLOCKx - (BLOCKx / 8), (self.Y + 1) * BLOCKy - BLOCKy / 3,
                                                fill="green")
