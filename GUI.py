from tkinter import *
import time

import Terrain as t
import Player as p

WIDTH = 900
HEIGHT = 600

ROWS = 15
COLS = 15

BLOCKx = WIDTH/COLS
BLOCKy = HEIGHT/ROWS

exp = t.Terrain(ROWS, COLS, p.Player())
exp.randomPath()

window = Tk()

def leftKey(event):
    if exp.player.move(3):
        exp.player.loc.updateImage(area)
        area.move(exp.player.image, -BLOCKx, 0)

def rightKey(event):
    if exp.player.move(1):
        exp.player.loc.updateImage(area)
        area.move(exp.player.image, BLOCKx, 0)

def upKey(event):
    if exp.player.move(0):
        exp.player.loc.updateImage(area)
        area.move(exp.player.image, 0, -BLOCKy)

def downKey(event):
    if exp.player.move(2):
        exp.player.loc.updateImage(area)
        area.move(exp.player.image, 0, BLOCKy)


window.bind('<Left>', leftKey)
window.bind('<Right>', rightKey)
window.bind('<Up>', upKey)
window.bind('<Down>', downKey)


area = Canvas(window, width=WIDTH, height=HEIGHT)
exp.createImage(area, WIDTH, HEIGHT)

while(True):
    if exp.player.loc.target:
        exp = exp.nextMap(exp.player)
        exp.randomPath()
        exp.createImage(area, WIDTH, HEIGHT)
        BLOCKx = WIDTH/exp.cols
        BLOCKy = HEIGHT/exp.rows
    window.update()
    time.sleep(.1)


window.mainloop()