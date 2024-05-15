from typing import Callable
from threading import Thread
from termcolor import colored
from utils import InvalidInputException
from scribe import TerminalScribe
from canvas import Canvas

class Drawing:
    """
    Given starting position, direction and instructions --> can draw on the input scribe (which has a canvas)
    pos: tuple of x and y
    dir: int of degrees of angle
    """

    def __init__(self, pos: tuple = (0, 0), direction: int = 90):
        self.position = pos
        self.direction = direction

    @staticmethod
    def find_closest_ix(array: list, num: float):
        """
        Find the closest element (index of it) to the given number in the sorted array
        """
        i = 0
        diff = abs(array[i] - num)
        for i in range(1, len(array)):
            new_diff = abs(array[i] - num)
            if new_diff > diff:
                return i - 1
            elif new_diff == diff:
                return i
            else:
                diff = new_diff
        return i

    def paint(self, scribe: TerminalScribe, instructions: list = None):
        """
        instructions: list of (name, param) pairs
        scribe: where to draw the picture
        """
        # set the position in canvas
        scribe.canvas.set_pos(self.position, mark=colored(scribe.mark, 'red'))
        # set the position in scribe
        scribe.pos = self.position
        # execute instructions using scribe
        for instr in instructions:
            name, param = instr
            try:
                method = getattr(scribe, name)
            except AttributeError:
                raise InvalidInputException(f"Method with the name {name} is not present")
            else:
                method(param)

    def plot(self, scribe: TerminalScribe, func: Callable, range_x: tuple):
        """
        Plots the function from left to right
        :param range_x: range of the plot in x-axis
        :param func: callable that returns y given x
        :param scribe: where to draw the picture
        """
        min_x, max_x = range_x
        length_x, length_y = scribe.canvas.shape()
        # Ex: if x size is 5 then 4 jumps_x
        jumps_x = length_x - 1
        step_x = (max_x - min_x) / jumps_x
        assert min_x + jumps_x * step_x - max_x < 10 ** -5

        # Figure out what is the range of y to plot
        min_y = func(min_x)
        max_y = min_y
        for i in range(jumps_x):
            temp_y = func(min_x + step_x * i)
            min_y = min(temp_y, min_y)
            max_y = max(temp_y, max_y)

        jumps_y = length_y - 1
        step_y = (max_y - min_y) / jumps_y
        assert min_y + jumps_y * step_y - max_y < 10 ** -5

        # For each jump calculate what 'y' that would be
        reg_y_values = list()
        for i in range(jumps_y):
            reg_y_values.append(min_y + i * step_y)
        # Reverse because y-axis is inverted in the image
        reg_y_values = reg_y_values[::-1]

        # Plot the points from left to right
        for i in range(length_x):
            x_plot = i
            x = min_x + i * step_x
            y = func(x)
            y_plot = self.find_closest_ix(reg_y_values, y)
            if i == 0:
                scribe.pos = (x_plot, y_plot)
                scribe.canvas.set_pos((x_plot, y_plot), '.')
            else:
                scribe.draw((x_plot, y_plot))

class ParallelDrawing:
    def __init__(self, drawings: list):
        if not isinstance(drawings, list) or len(drawings) == 0:
            raise InvalidInputException("Scribes are not correctly input")
        self.drawings = drawings

    def execute(self, canvas: Canvas):
        threads = []
        for drawing in self.drawings:
            scribe = TerminalScribe(canvas, framerate=0.1)
            plot = Drawing()
            if isinstance(drawing,tuple) and isinstance(drawing[0], Callable):
                # function drawing
                func, range_x = drawing
                thread = Thread(target=plot.plot, args=(scribe, func, range_x))
            elif isinstance(drawing, list) and isinstance(drawing[0], tuple):
                # instructions list
                thread = Thread(target=plot.paint, args=(scribe,drawing))
            else:
                try:
                    raise InvalidInputException(f"Drawings should either be function of instructions."
                                                f"Provided: {type(drawing)} and inside {type(drawing[0])}")
                except KeyError:
                    raise InvalidInputException(f"drawing should be tuple/list, now: {type(drawing)}")
            threads.append(thread)

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]