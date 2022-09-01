import random as r
from tkinter import PhotoImage, StringVar, E, NW, W, LEFT, RIGHT, TOP, BOTTOM, BOTH, X, Y, Canvas, Label, Frame, Button


class Store:

    def __init__(self, player, maze):
        self.player = player
        self.maze = maze
        self.gems = 0
        self.phase = PhaseItem()
        self.tele = TeleItem()
        self.reset = ResetItem()

        self.cart = None

        self.storeFrame = None
        self.cartFrame = None
        self.ucartFrame = None
        self.lcartFrame = None
        self.totalLabel = None
        self.totalVar = StringVar()

        self.pbi = PhotoImage(file=r"menus\store_art\PhaseButton.gif")
        self.pbone = PhotoImage(file=r"menus\store_art\phase1.gif")
        self.pbthree = PhotoImage(file=r"menus\store_art\phase3.gif")
        self.pbfive = PhotoImage(file=r"menus\store_art\phase5.gif")

        self.tbi = PhotoImage(file=r"menus\store_art\telestore.gif")
        self.tbone = PhotoImage(file=r"menus\store_art\tele1.gif")
        self.tbthree = PhotoImage(file=r"menus\store_art\tele3.gif")
        self.tbfive = PhotoImage(file=r"menus\store_art\tele5.gif")

        self.rbi = PhotoImage(file=r"menus\store_art\reset.gif")
        self.rbone = PhotoImage(file=r"menus\store_art\reset1.gif")
        self.rbthree = PhotoImage(file=r"menus\store_art\reset3.gif")
        self.rbfive = PhotoImage(file=r"menus\store_art\reset5.gif")

        self.buyi = PhotoImage(file=r"menus\store_art\buy.gif")
        self.closei = PhotoImage(file=r"menus\store_art\Close.gif")

        self.teletoggle = PhotoImage(file=r"menus\maze_menu_art/teleport.gif")
        self.resettoggle = PhotoImage(file=r"menus\maze_menu_art/reset tails.gif")

    def add_label(self, item, number):
        if self.cart.itemLimit < 24:
            self.cart.itemLimit += 1
            text = f"{item.name} x{str(number)}: {str(item.costDict[number])}"
            Label(self.ucartFrame, text=text, anchor=E).pack(side=TOP, fill=X)
            amount = self.cart.total + item.costDict[number]
            amount = round(amount, 2)
            self.cart.total = amount
            self.totalVar.set("Total: "+str(self.cart.total))

            self.cart.dict[item.name] = self.cart.dict[item.name] + number

    def buy_gem(self):
        self.player.debt += 1
        self.gems += 1

    def create_image(self, parent, WIDTH, HEIGHT):

        self.cart = Cart()
        numGems = StringVar()
        numGems.set("Your Money: " + str(self.player.debt))

        self.storeFrame = Canvas(parent, width=WIDTH*(3/4), height=HEIGHT*(3/4), bg="light grey")
        self.storeFrame.pack_propagate(False)
        self.storeFrame.place(relx=.5, rely=.5, anchor="center")

        pFrame = Frame(master=self.storeFrame, width=WIDTH*(3/4), height=HEIGHT*(3/4)/3, bg="#30F630")
        pFrame.place(relx=0, rely=0, anchor=NW)
        pFrame.pack_propagate(False)
        tFrame = Frame(master=self.storeFrame, width=WIDTH * (3 / 4), height=HEIGHT * (3 / 4) / 3, bg="white")
        tFrame.place(relx=0, rely=0.33, anchor=NW)
        tFrame.pack_propagate(False)
        rFrame = Frame(master=self.storeFrame, width=WIDTH * (3 / 4), height=HEIGHT * (3 / 4) / 3, bg="black")
        rFrame.place(relx=0, rely=0.66, anchor=NW)
        rFrame.pack_propagate(False)

        Label(pFrame, image=self.pbi).pack(side=LEFT)
        Button(pFrame, image=self.pbone, command=lambda: self.add_label(self.phase, 1)).pack(side=LEFT)
        Label(pFrame, text="Cost: " + str(self.phase.cost), bg="#30F630").place(relx=.33, rely=.725)
        Button(pFrame, image=self.pbthree, command=lambda: self.add_label(self.phase, 3)).pack(side=LEFT)
        Label(pFrame, text="Cost: " + str(self.phase.three), bg="#30F630").place(relx=.445, rely=.725)
        Button(pFrame, image=self.pbfive, command=lambda: self.add_label(self.phase, 5)).pack(side=LEFT)
        Label(pFrame, text="Cost: " + str(self.phase.five), bg="#30F630").place(relx=.56, rely=.725)
        Label(tFrame, image=self.tbi).pack(side=LEFT)
        Button(tFrame, image=self.tbone, command=lambda: self.add_label(self.tele, 1)).pack(side=LEFT)
        Label(tFrame, text="Cost: " + str(self.tele.cost)).place(relx=.33, rely=.725)
        Button(tFrame, image=self.tbthree, command=lambda: self.add_label(self.tele, 3)).pack(side=LEFT)
        Label(tFrame, text="Cost: " + str(self.tele.three)).place(relx=.445, rely=.725)
        Button(tFrame, image=self.tbfive, command=lambda: self.add_label(self.tele, 5)).pack(side=LEFT)
        Label(tFrame, text="Cost: " + str(self.tele.five)).place(relx=.56, rely=.725)
        Label(rFrame, image=self.rbi).pack(side=LEFT)
        Button(rFrame, image=self.rbone, command=lambda: self.add_label(self.reset, 1)).pack(side=LEFT)
        Label(rFrame, text="Cost: " + str(self.reset.cost), bg="black", fg="white").place(relx=.33, rely=.725)
        Button(rFrame, image=self.rbthree, command=lambda: self.add_label(self.reset, 3)).pack(side=LEFT)
        Label(rFrame, text="Cost: " + str(self.reset.three), bg="black", fg="white").place(relx=.445, rely=.725)
        Button(rFrame, image=self.rbfive, command=lambda: self.add_label(self.reset, 5)).pack(side=LEFT)
        Label(rFrame, text="Cost: " + str(self.reset.five), bg="black", fg="white").place(relx=.56, rely=.725)

        self.cartFrame = Frame(self.storeFrame, width=WIDTH/6, bg="light grey")
        self.cartFrame.pack_propagate(False)
        self.cartFrame.pack(side=RIGHT, fill=Y)
        self.ucartFrame = Frame(self.cartFrame)
        self.ucartFrame.pack(side=TOP, fill=BOTH)
        Label(self.ucartFrame, text="Your cart:", anchor=W).pack(side=TOP, fill=X)
        Label(self.ucartFrame, textvariable=numGems, anchor=W).pack(side=BOTTOM, fill=X)
        self.totalVar.set("Total: 0")
        self.totalLabel = Label(self.ucartFrame, textvariable=self.totalVar, anchor=W)
        self.totalLabel.pack(side=BOTTOM, fill=X)
        self.lcartFrame = Frame(self.cartFrame)
        self.lcartFrame.pack(side=BOTTOM, fill=X)
        Button(self.lcartFrame, image=self.buyi, command=self.buyStore).pack(side=LEFT)
        Button(self.lcartFrame, image=self.closei, command=self.closeStore).pack(side=RIGHT)

    def closeStore(self):
        self.cartFrame.destroy()
        self.storeFrame.destroy()
        self.cart = Cart()
        self.totalVar.set("Total: " + str(self.cart.total))

    def buyStore(self):
        self.cartFrame.destroy()
        self.storeFrame.destroy()
        self.player.phase += self.cart.dict["Phase"]
        self.player.teleport += self.cart.dict["Teleport"]
        self.player.resetTail += self.cart.dict["Reset Tails"]
        self.player.debt -= self.cart.total
        self.player.debt = round(self.player.debt, 2)
        self.player.updateTile(self.maze.frame)
        if self.cart.dict["Teleport"] > 0:
            self.maze.menu.tele.config(image=self.teletoggle)
        if self.cart.dict["Reset Tails"] > 0:
            self.maze.menu.resetb.config(image=self.resettoggle)
        self.cart = Cart()
        self.totalVar.set("Total: " + str(self.cart.total))


class Cart:

    def __init__(self):
        self.numPhases = 0
        self.numTele = 0
        self.numReset = 0

        self.dict = {"Phase": self.numPhases,
                     "Teleport": self.numTele,
                     "Reset Tails": self.numReset}

        self.itemLimit = 0

        self.total = 0


class Item:

    def __init__(self, cost):
        self.name = None

        one = round(cost, 2)
        self.cost = one
        three = cost * (3 / 2)
        self.three = round(three, 2)
        five = cost * (5 / 3)
        self.five = round(five, 2)

        self.costDict = {1: self.cost,
                         3: self.three,
                         5: self.five}

    def halfOff(self):
        halfone = self.cost/2
        self.cost = round(halfone/2)
        halfthree = self.three/2
        self.three = round(halfthree, 2)
        halffive = self.five/2
        self.five = round(halffive, 2)

    def print(self):
        print("One:", self.cost)
        print("Three", self.three)
        print("Five", self.five)


class PhaseItem(Item):

    def __init__(self):
        super().__init__(cost=r.uniform(1, 2))

        self.name = "Phase"


class TeleItem(Item):

    def __init__(self):
        super().__init__(cost=r.uniform(2, 3))

        self.name = "Teleport"


class ResetItem(Item):

    def __init__(self):
        super().__init__(cost=r.uniform(3, 4))

        self.name = "Reset Tails"
