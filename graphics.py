import random
import time
from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False
    
    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1, p2):
        self.point_one = p1
        self.point_two = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.point_one.x, self.point_one.y, self.point_two.x, self.point_two.y, fill=fill_color, width=2)

class Cell():
    def __init__(self, x1, y1, x2, y2, win, visited=False):
        self._left_wall = Line(Point(x1, y1), Point(x1, y2))
        self._top_wall = Line(Point(x1, y1), Point(x2, y1))
        self._right_wall = Line(Point(x2, y1), Point(x2, y2))
        self._bottom_wall = Line(Point(x1, y2), Point(x2, y2))
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._win = win
        self.visited = visited

    def draw(self):
        sides = [
            (self._left_wall, self.has_left_wall),
            (self._top_wall, self.has_top_wall),
            (self._right_wall, self.has_right_wall),
            (self._bottom_wall, self.has_bottom_wall)
            ]
        for side in sides:
            if side[1]:
                self._win.draw_line(side[0])
            else:
                self._win.draw_line(side[0], "white")

    def draw_move(self, to_cell, undo=False):
        center = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        target = Point((to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2)
        line = Line(center, target)
        if undo:
            self._win.draw_line(line, "gray")
        else:
            self._win.draw_line(line, "red")

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

    def _create_cells(self):
        for i in range(self._num_cols):
            row_builder = []
            for j in range(self._num_rows):
                row_builder.append(self._create_cell(i, j))
            self._cells.append(row_builder)

    def _create_cell(self, i, j):
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        cell = Cell(x1, y1, x2, y2, self._win)
        self._draw_cell(cell)
        return cell
    
    def _draw_cell(self, cell):
        cell.draw()
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.005)

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        exit = self._cells[self._num_cols - 1][self._num_rows - 1]
        entrance.has_top_wall = False
        entrance.draw()
        exit.has_bottom_wall = False
        exit.draw()

    def _break_walls_r(self, i, j):
        cell = self._cells[i][j]
        cell.visited = True
        while True:
            to_visit = []
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append((i, j - 1, "up"))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                to_visit.append((i + 1, j, "right"))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                to_visit.append((i, j + 1, "down"))
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append((i - 1, j, "left"))

            if not to_visit:
                self._draw_cell(cell)
                return
            
            rand_direction = random.randrange(len(to_visit))
            new_i, new_j, direction = to_visit[rand_direction]
            # print(to_visit[rand_direction])
            match direction:
                case "up":
                    cell.has_top_wall = False
                    self._cells[i][j - 1].has_bottom_wall = False
                case "right":
                    cell.has_right_wall = False
                    self._cells[i + 1][j].has_left_wall = False
                case "down":
                    cell.has_bottom_wall = False
                    self._cells[i][j + 1].has_top_wall = False
                case "left":
                    cell.has_left_wall = False
                    self._cells[i - 1][j].has_right_wall = False
            
            self._break_walls_r(new_i, new_j)
                