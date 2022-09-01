import Colors as c

'''
0 = North
1 = East
2 = South
3 = West
'''


class Player:

    def __init__(self):
        # where is the player?
        self.loc = None
        self.previous = None

        # are they alive?
        self.alive = True

        # can pass through 1 barrier
        self.phase = False

        # teleport to a random location
        self.teleport = 1

        # leave tail?
        self.tail = True
        self.resetTail = 1

        # should the player be allowed to move?
        self.active = True

        # how much money does the player have?
        self.debt = 0

        self.image = None
        self.color = "light blue"
        self.X = None
        self.Y = None

    def lookup(self, NESW):
        # does the player have an ability?
        if self.phase:
            if self.loc.connections[NESW] is None:
                return False
            elif self.loc.connections[NESW].visited:
                return False
            elif self.loc.connections[NESW].evisited:
                return False
            elif self.loc.borders[NESW]:
                self.phase -= 1
                if self.phase < 0:
                    self.phase = 0
                return True
            return True
        else:
            # are there any spaces where the player can move?
            if self.loc.connections[NESW] is None:
                return False
            elif self.loc.connections[NESW].visited:
                return False
            elif self.loc.connections[NESW].evisited:
                return False
            elif self.loc.borders[NESW]:
                return False
            return True

    def move(self, dir):
        phase = self.phase
        if self.lookup(dir):
            self.previous = self.loc
            if phase > self.phase:
                self.loc.phased = True
                self.loc = self.loc.connections[dir]
                self.loc.phased = True
            else:
                self.loc = self.loc.connections[dir]
            if self.tail:
                self.loc.visited = True
            self.X = self.loc.X
            self.Y = self.loc.Y
            if self.loc.holding == "phase":
                self.phase += 1
            elif self.loc.holding == "money":
                self.debt += 1
            return True
        return False

    def create_image(self, frame, BLOCKx, BLOCKy):
        self.X = self.loc.X
        self.Y = self.loc.Y
        self.loc.visited = True
        self.image = frame.create_oval(self.X * BLOCKx + BLOCKx/5, self.Y * BLOCKy + BLOCKy/5,
                                       (self.X + 1) * BLOCKx - BLOCKx/5, (self.Y + 1) * BLOCKy - BLOCKy/5,
                                        fill="light blue")
        frame.pack()

    def redraw(self, frame, BLOCKx, BLOCKy):
        if self.phase:
            self.image = frame.create_oval(self.X * BLOCKx + BLOCKx / 5, self.Y * BLOCKy + BLOCKy / 5,
                                           (self.X + 1) * BLOCKx - BLOCKx / 5, (self.Y + 1) * BLOCKy - BLOCKy / 5,
                                           fill="#FF00FF")
        else:
            self.image = frame.create_oval(self.X * BLOCKx + BLOCKx/5, self.Y * BLOCKy + BLOCKy/5,
                                           (self.X + 1) * BLOCKx - BLOCKx/5, (self.Y + 1) * BLOCKy - BLOCKy/5,
                                            fill="light blue")
        frame.pack()

    def updateTile(self, frame):
        if self.phase:
            frame.itemconfig(self.image, fill="#FF00FF")
        else:
            frame.itemconfig(self.image, fill="light blue")
        if self.loc.phased:
            frame.itemconfig(self.previous.image, fill="#00FF77")
            frame.itemconfig(self.loc.image, fill="#00FF77")
        else:
            frame.itemconfig(self.loc.image, fill='blue')
        if self.loc.phaseImage:
            frame.delete(self.loc.phaseImage)
            self.loc.holding = None

