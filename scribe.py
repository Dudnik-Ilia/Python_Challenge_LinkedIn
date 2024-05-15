from random import random
from termcolor import colored
import math
import time
from canvas import Canvas
from utils import InvalidInputException


class TerminalScribe:
    def __init__(self, canvas: Canvas, framerate: float = 0.1):
        if not issubclass(type(canvas), Canvas):
            raise InvalidInputException(f"canvas parameter should of class {Canvas}")
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = framerate
        self.pos: tuple[float, float] = (0., 0.)
        # x and y
        self.direction = (1, 0)

    @property
    def mark(self):
        return self._mark

    @mark.setter
    def mark(self, value):
        if not isinstance(value, str) or len(value) > 1:
            raise InvalidInputException(f"Invalid mark assignment: {value}")
        self._mark = value

    def change_direction(self, degree):
        if degree < 0 or degree > 360:
            raise InvalidInputException(f"Degree was not correctly specified: {degree}")
        x = math.sin(degree / 180 * math.pi)
        y = -math.cos(degree / 180 * math.pi)
        self.direction = (x, y)

    def step_forward(self, times: int = 1):
        """
        Take a step forward following the direction variable.
        Mark will bounce off the walls when encountered: we take one more step in this case
        :param times: how many times to make a step
        """
        if not isinstance(times, int) or times < 1:
            raise InvalidInputException(f"Times was not correctly specified: {times}")
        for _ in range(times):
            # Calculate new position with direction we have
            new_pos = self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]
            # Check whether we run out of bounds
            hits = self.canvas.hits_wall(new_pos)
            if not hits:
                self.draw(new_pos)
            else:
                if hits in ['up', 'down']:
                    # mirror direction by y-axis
                    self.direction = (self.direction[0], -self.direction[1])
                    # take a step back
                    new_pos = new_pos[0] - self.direction[0], new_pos[1] + self.direction[1]
                elif hits in ['left', 'right']:
                    # mirror direction by x-axis
                    self.direction = (-self.direction[0], self.direction[1])
                    # step back
                    new_pos = new_pos[0] + self.direction[0], new_pos[1] - self.direction[1]
                else:
                    raise Exception("direction of hitting was wrong specified")
                self.draw(new_pos)

    @staticmethod
    def _validate_input(times):
        if not isinstance(times, int) or times < 1:
            raise InvalidInputException(f"Times was not correctly specified: {times}")

    def up(self, times=1):
        self._validate_input(times)
        self.direction = (0, -1)
        self.step_forward(times=times)

    def down(self, times=1):
        self._validate_input(times)
        self.direction = (0, 1)
        self.step_forward(times=times)

    def right(self, times=1):
        self._validate_input(times)
        self.direction = (1, 0)
        self.step_forward(times=times)

    def left(self, times=1):
        self._validate_input(times)
        self.direction = (-1, 0)
        self.step_forward(times=times)

    def draw(self, pos: tuple):
        """
        Moves the mark to new position
        Changes the old one to trail mark
        """
        # check whether we are out of bounds of the canvas
        pos = self.canvas.cap_pos(pos)
        # Set the old position to the "trail" symbol
        self.canvas.set_pos(self.pos, self.trail)
        # Update position
        self.pos = pos
        # Set the new position to the "mark" symbol
        self.canvas.set_pos(self.pos, colored(self.mark, 'red'))
        # Print everything to the screen
        self.canvas.print()
        # Sleep for a little bit to create the animation
        time.sleep(self.framerate)

    def draw_square(self, size):
        func_order = [self.right, self.down, self.left, self.up]
        for func in func_order:
            for i in range(size):
                func()


class WobbleScribe(TerminalScribe):

    def __init__(self, canvas: Canvas, wobbly_proba: float = 0.5, fancy: bool = False):
        super().__init__(canvas)
        self.fancy = fancy
        self.wobbly_proba = wobbly_proba

    @staticmethod
    def wobble(proba):
        if proba > random.random():
            if random.random() > 0.5:
                return 1
            else:
                return -1
        return 0

    def draw(self, pos: tuple):
        """ Add random distortion with probability wobble_proba """
        new_pos = (pos[0]+self.wobble(self.wobbly_proba),
                   pos[1]+self.wobble(self.wobbly_proba))

        # check whether we are out of bounds of the canvas
        pos = self.canvas.cap_pos(new_pos)
        # Set the old position to the "trail" symbol
        if self.fancy:
            color = random.choice(['red', 'green', 'blue'])
            self.canvas.set_pos(self.pos, colored(self.trail, color))
        else:
            self.canvas.set_pos(self.pos, self.trail)
        # Update position
        self.pos = pos
        # Set the new position to the "mark" symbol
        self.canvas.set_pos(self.pos, colored(self.mark, 'red'))
        # Print everything to the screen
        self.canvas.print()
        time.sleep(self.framerate)
