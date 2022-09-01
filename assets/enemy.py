from assets import player
import random as r


'''
0 = North
1 = East
2 = South
3 = West
'''


class Enemy(player.Player):

    def __init__(self):
        super().__init__()

        self.loc = None
        self.image = None
        self.dead = False

    def move(self, frame, BLOCKx, BLOCKy):
        options = []
        for direction in range(4):
            if self.lookup(direction):
                if self.loc.connections[direction].target is False:
                    options.append(direction)
        if options:
            direction = options[r.randint(0, len(options)-1)]
            self.loc = self.loc.connections[dir]
            self.loc.evisited = True
            self.X = self.loc.X
            self.Y = self.loc.Y
            if self.loc.holding == "phase":
                self.phase += 2
            if direction == 3:
                frame.move(self.image, -BLOCKx, 0)
            elif direction == 2:
                frame.move(self.image, 0, BLOCKy)
            elif direction == 1:
                frame.move(self.image, BLOCKx, 0)
            elif direction == 0:
                frame.move(self.image, 0, -BLOCKy)
            self.updateTile(frame)
            return True
        else:
            self.dead = True
            return False


    def create_image(self, frame, BLOCKx, BLOCKy):
        self.X = self.loc.X
        self.Y = self.loc.Y
        self.loc.evisited = True
        self.image = frame.create_oval(self.X * BLOCKx + BLOCKx/5, self.Y * BLOCKy + BLOCKy/5,
                                       (self.X + 1) * BLOCKx - BLOCKx/5, (self.Y + 1) * BLOCKy - BLOCKy/5,
                                        fill="yellow")
        frame.itemconfig(self.loc.image, fill='orange')
        frame.pack()

    def redraw(self, frame, BLOCKx, BLOCKy):
        frame.delete(self.image)
        self.image = frame.create_oval(self.X * BLOCKx + BLOCKx/5, self.Y * BLOCKy + BLOCKy/5,
                                       (self.X + 1) * BLOCKx - BLOCKx/5, (self.Y + 1) * BLOCKy - BLOCKy/5,
                                        fill="yellow")
        frame.pack()

    def updateTile(self, frame):
        frame.itemconfig(self.loc.image, fill='orange')
        if self.loc.phaseImage:
            frame.delete(self.loc.phaseImage)
            self.loc.holding = None