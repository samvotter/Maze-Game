import argparse
from tkinter import Tk
from menus.start_screen import StartScreen


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launches Maze Game!")
    parser.add_argument('-xr', '--x_resolution', type=int, default=1600, help='Resolution width')
    parser.add_argument('-yr', '--y_resolution', type=int, default=900,  help='Resolution height')
    args = parser.parse_args()

    window = Tk()

    StartScreen(window, args.x_resolution, args.y_resolution)

    window.mainloop()
