import math
from typing import Union


class Cell(object):
    """
    The cell object.

    The x and y are the respective coordinates.
    neighbours is a list of all cells that impact the current cell.
    value is the current value of the cell, or None if there is no value set.
    possibilities is a list of current possible numbers for the cell
    """
    def __init__(self, board, x, y, value=None):
        self.x, self.y = x, y
        self.neighbours = None
        self._value = None
        self.board = board

        if value == 0:
            self._value = None
        else:
            self._value = value

    def __str__(self):
        return "X: {}, Y: {}, Val: {}, Possibilities: {}".format(self.x, self.y, self.value, self.possibilities)

    def __repr__(self):
        return "Cell({x}, {y}, {value})".format(x=self.x, y=self.y, value=self.value)

    def __add__(self, other):
        """Allows for adding the values of cells together"""
        try:
            return self.value + other.value
        except AttributeError:
            return self.value + other

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """Makes sure that you can't set the value of the cell twice"""
        if self.value:
            raise ValueError("Cell {},{}, value: {}. Tried to set value {}".format(self.x, self.y, self.value, value, ))

        print("Changed cell. Value {} to cell {},{}".format(value, self.x, self.y))

        self._value = value

    @property
    def supercell(self):
        """Gets the coordinate of the parent supercell"""

        supercell_x = math.floor(self.x / self.board.SUPERCELL_SIZE)
        supercell_y = math.floor(self.y / self.board.SUPERCELL_SIZE)
        return supercell_x, supercell_y

    @property
    def possibilities(self) -> list:
        """The current possible values for the cell"""
        non_possibilities = [
            cell.value
            for cell in self.neighbours
            if cell.value
        ]

        return [val for val in self.board.get_possible_cell_values() if val not in non_possibilities]

    def solve(self) -> Union[bool, None]:
        if not self.value:
            ret_value = self.solve_last_possibility()
            ret_value = ret_value if ret_value else self.solve_last_option()
            return ret_value

        return None

    def solve_last_possibility(self) -> bool:
        """Checks if there is only one possibility left for the cell"""

        if len(self.possibilities) == 1:
            self.value = self.possibilities[0]
            print("solve_last_possibility")
            return True

        return False

    def solve_last_option(self) -> bool:
        """Checks if any of the neighbouring cells have any of the remaining possibilities"""

        possibilities = set(self.possibilities.copy())

        for cell in self.neighbours:
            possibilities_for_neighbour = set([
                val
                for val in possibilities
                if val not in cell.possibilities
            ])
            possibilities -= possibilities_for_neighbour

        if len(possibilities) == 1:
            self.value = list(possibilities)[0]
            print("solve_last_option")
            return True

        return False