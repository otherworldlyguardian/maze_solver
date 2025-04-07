from graphics import *

def main():
    # win = Window(800, 600)
    win = Window(1670, 770)
    # maze = Maze(50, 50, 12, 16, 44, 42, win)
    maze = Maze(10, 10, 25, 55, 30, 30, win)
    print("Maze Built")
    result = maze.solve(True)
    if result:
        print("Hurrah the maze was solved")
    else:
        print("Aww too bad, better luck next time")
    win.wait_for_close()

main()