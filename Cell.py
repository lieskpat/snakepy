import numpy
import abc
import pygame


class Cell(object):

    def __init__(self, x_position, y_position, cellType):
        self.x_position = x_position
        self.y_position = y_position
        self.cellType = cellType

    def get_position(self):
        return "x= " + format(self.x_position) + " " + "y= " + format(self.y_position)

    def get_cell_type(self):
        return self.cellType

    def set_cell_type(self, cellType):
        self.cellType = cellType

    def get_position_with_cell_type(self):
        return self.get_position() + " CellType:" + format(self.get_cell_type())


class SnakeCell(Cell):

    def __init__(self, x_position, y_position):
        Cell.__init__(self, x_position, y_position, CellType.SNAKE)


class SnakeHead(SnakeCell):

    def __init__(self, x_position, y_position):
        SnakeCell.__init__(self, x_position, y_position)
        Cell.cellType = CellType.HEAD
        self.direction = Direction.UP

    def new_head_position(self):
        if self.direction == Direction.DOWN:
            self.y_position = self.y_position + 1
        elif self.direction == Direction.UP:
            self.y_position = self.y_position - 1
        elif self.direction == Direction.LEFT:
            self.x_position = self.x_position - 1
        elif self.direction == Direction.RIGHT:
            self.x_position = self.x_position + 1

    def move_down(self):
        if self.direction != Direction.UP:
            self.direction = Direction.DOWN

    def move_up(self):
        if self.direction != Direction.DOWN:
            self.direction = Direction.UP

    def move_left(self):
        if self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT

    def move_right(self):
        if self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT


class Snake(object):

    def __init__(self, snakeHead):
        self.snakeHead = snakeHead
        self.snakeCellList = numpy.zeros(shape=1, dtype=SnakeCell)
        numpy.append(self.snakeCellList, self.snakeHead)

    def move(self):
        pass


class Direction(enumerate):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3


class CellType(enumerate):
    EMPTY = 0
    SNAKE = 1
    HEAD = 2


class GameField(object):

    def __init__(self, rows, cols):
        self.cols = cols
        self.rows = rows
        self.game_field = numpy.zeros(shape=(self.rows, self.cols), dtype=Cell)
        for i in range(self.rows):
            for j in range(self.cols):
                self.game_field[i][j] = Cell(i, j, CellType.EMPTY)

    def get_cell(self, row, col):
        return self.game_field[row][col]

    def show_game_field(self):
        s = ""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.get_cell(i, j).get_cell_type() == CellType.EMPTY:
                    s += "+"
                elif self.get_cell(i, j).get_cell_type() == CellType.SNAKE:
                    s += "*"
                elif self.get_cell(i, j).get_cell_type() == CellType.HEAD:
                    s += "#"
                else:
                    s += "-"
            s += "\n"
        return s


class Game(object):
    # start timer
    # in any interval play_a_round
    def __init__(self, game_field, snake):
        self.snake = snake
        self.game_field = game_field

    def play_a_round(self):
        self.move_snake_head()
        # inform the controller and view to show updated GameField

    def move_snake_head(self):
        # old Head position
        self.game_field.get_cell(snake.snakeHead.x_position,
                                 snake.snakeHead.y_position).set_cell_type(CellType.EMPTY)
        # new Head position first and then update the GameField
        self.snake.snakeHead.new_head_position()
        self.game_field.get_cell(snake.snakeHead.x_position,
                                 snake.snakeHead.y_position).set_cell_type(CellType.HEAD)


class SnakeController(object):
    # maybe start here the timer task and play a round
    def __init__(self, game, view):
        self.game = game
        self.view = view

    def key_listener(self):
        pass

    def move_up(self):
        self.game.snake.snakeHead.move_up()

    def move_down(self):
        self.game.snake.snakeHead.move_down()

    def move_left(self):
        self.game.snake.snakeHead.move_left()

    def move_right(self):
        self.game.snake.snakeHead.move_right()


class View(object):
    pass


field = GameField(5, 15)
snake = Snake(SnakeHead(3, 14))
game = Game(field, snake)
view = View()
controller = SnakeController(game, view)

field.get_cell(4, 14).set_cell_type(CellType.HEAD)
print(field.show_game_field())
# for x in range(field.rows):
#    for y in range(field.cols):
#        cell = field.get_cell(x, y)
#        print(cell.get_position_with_cell_type())
# print(cell.cellType)
# print(field.get_cell(0, 3))
# print(field.get_cell(4, 4))
