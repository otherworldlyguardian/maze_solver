from graphics import *

def main():
    win = Window(800, 600)
    maze = Maze(50, 50, 12, 16, 44, 42, win)
    win.wait_for_close()

main()