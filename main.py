from graphics import *

def main():
    win = Window(1670, 770)
    # maze = Maze(50, 50, 12, 16, 44, 42, win)
    # maze = Maze(10, 10, 20, 26, 30, 29, win)
    maze = Maze(10, 10, 25, 55, 30, 30, win)
    win.wait_for_close()

main()