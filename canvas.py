import json
import os


class Canvas:
    """
    This is the Canvas class. It defines some height and width, and a
    matrix of characters to keep track of where the TerminalScribes are moving
    """
    def __init__(self, width, height):
        self._x = width
        self._y = height
        # This is a grid that contains data about where the
        # TerminalScribes have visited
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    def to_dict(self):
        return {
            "_x": self._x,
            "_y": self._y,
            "canvas": self._canvas
        }

    def from_dict(self, dictionary: dict):
        self._canvas = dictionary["canvas"]
        self._x = dictionary['_x']
        self._y = dictionary['_y']

    def save(self, path):
        with open(path, 'w') as file:
            json.dump(self.to_dict(), file)

    def load(self, path):
        with open(path, 'r') as file:
            dictionary = json.load(file)
        self.from_dict(dictionary)

    def shape(self):
        return self._x, self._y

    def cap_pos(self, pos: tuple):
        """
        checks whether position is inside the canvas
        returns new position if out of bounds
        """
        pos = list(pos)
        pos[0] = min(max(0, pos[0]), self._x - 1)
        pos[1] = min(max(0, pos[1]), self._y - 1)
        return tuple(pos)

    def hits_wall(self, point):
        """
        Returns: str (up, left, down or right) if the given point is outside the boundaries of the Canvas
        Else --> False
        """
        # point = [round(x) for x in point]
        if point[0] < 0:
            return 'left'
        if point[0] > self._x - 1:
            return 'right'
        if point[1] < 0:
            return 'up'
        if point[1] > self._y - 1:
            return 'down'
        return False

    def set_pos(self, pos, mark):
        """
        Set the given position to the provided character on the canvas
        """
        pos = [round(x) for x in pos]
        self._canvas[pos[0]][pos[1]] = mark

    @staticmethod
    def clear():
        """
        Clear the terminal (used to create animation)
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self):
        """
        Clear the terminal and then print each line in the canvas
        """
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))
