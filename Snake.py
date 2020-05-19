import numpy
from abc import ABC
import os
import threading
import click
import sys


class Observable(ABC):
    observer_list = []

    def attach(self, observer):
        self.observer_list.append(observer)

    def detach(self, observer):
        self.observer_list.remove(observer)

    def notify(self, subject):
        for observer in self.observer_list:
            observer.update(subject)


class ObserverInterface(ABC):
    def update(self, subject):
        pass


class GameRoundTimer(Observable, threading.Thread):
    def __init__(self, time_to_run, event):
        threading.Thread.__init__(self)
        self.time_to_run = time_to_run
        self.stopped = event

    def run(self):
        while not self.stopped.wait(self.time_to_run):
            super().notify(self)


class KeyListener(Observable, threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.key = None
        self.stopped = event

    def run(self):
        while not self.stopped.wait(0):
            # self.key = click.getchar()
            # vim like steering
            if self.key == "h" or self.key == "j" or self.key == "k" or self.key == "l":
                super().notify(self)


class Cell(object):

    def __init__(self, row_position, col_position):
        self.row_position = row_position
        self.col_position = col_position
        self.cellType = CellType.EMPTY

    def get_position(self):
        return "row_item= " + format(self.row_position) + " " + "col_item= " + format(self.col_position)

    def get_cell_type(self):
        return self.cellType

    def set_cell_type(self, cellType):
        self.cellType = cellType

    def get_position_with_cell_type(self):
        return self.get_position() + " CellType:" + format(self.get_cell_type())


class SnakeCell(Cell):

    def __init__(self, row_position, col_position):
        super().__init__(row_position, col_position)
        self.set_cell_type(CellType.SNAKE)


class SnakeHead(SnakeCell):

    def __init__(self, row_position, col_position, direction):
        super().__init__(row_position, col_position)
        self.set_cell_type(CellType.HEAD)
        self.direction = direction

    def new_head_position(self):
        if self.direction == Direction.DOWN:
            self.row_position = self.row_position + 1
        elif self.direction == Direction.UP:
            self.row_position = self.row_position - 1
        elif self.direction == Direction.LEFT:
            self.col_position = self.col_position - 1
        elif self.direction == Direction.RIGHT:
            self.col_position = self.col_position + 1

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
                self.game_field[i][j] = Cell(i, j)

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
                    s += "*"
                else:
                    s += "-"
            s += "\n"
        return s


class Game(object):

    def __init__(self, game_field, snake):
        self.game_field = game_field
        self.snake = snake

    def play_a_round(self):
        os.system('clear')
        self.move_snake_head()

    def move_snake_head(self):
        # old Head position

        self.game_field.get_cell(self.snake.snakeHead.row_position,
                                 self.snake.snakeHead.col_position).set_cell_type(CellType.EMPTY)
        # new Head position first and then update the GameField
        self.snake.snakeHead.new_head_position()
        self.game_field.get_cell(self.snake.snakeHead.row_position,
                                 self.snake.snakeHead.col_position).set_cell_type(CellType.HEAD)

    def is_collision(self):
        if self.snake.snakeHead.row_position < 0 and \
                self.snake.snakeHead.row_position < self.game_field.rows:
            print("out of range" + " " + str(self.snake.snakeHead.row_position))
            return True


class View(ABC):
    def render(self):
        pass


class TerminalView(View):

    def render(self):
        pass


class SnakeController(ObserverInterface):
    # maybe start here the timer task and play a round
    def __init__(self, game):
        self.game = game
        # self.view = view
        self.stopFlag = threading.Event()
        self.game_round_timer = GameRoundTimer(0.25, self.stopFlag)
        self.game_round_timer.start()
        self.game_round_timer.attach(self)
        self.key_listener = KeyListener(self.stopFlag)
        # unresolved side effects when i used KeyListener thread
        self.key_listener.start()
        self.key_listener.attach(self)

    def which_next_direction(self, key):
        if key == "h":
            self.move_left()
        elif key == "j":
            self.move_down()
        elif key == "k":
            self.move_up()
        elif key == "l":
            self.move_right()

    def move_up(self):
        self.game.snake.snakeHead.move_up()

    def move_down(self):
        self.game.snake.snakeHead.move_down()

    def move_left(self):
        self.game.snake.snakeHead.move_left()

    def move_right(self):
        self.game.snake.snakeHead.move_right()

    def update(self, subject):
        if isinstance(subject, KeyListener):
            # print(subject.key)
            self.which_next_direction(subject.key)
        elif isinstance(subject, GameRoundTimer):
            self.game.play_a_round()
            sys.stdout.write(self.game.game_field.show_game_field())
            sys.stdout.flush()
            if self.game.is_collision():
                self.stopFlag.set()


def main():
    SnakeController(Game(GameField(20, 20), Snake(SnakeHead(19, 19, Direction.UP))))


if __name__ == '__main__':
    main()
