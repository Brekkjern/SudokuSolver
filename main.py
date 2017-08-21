import math
from typing import Union

SUPERCELL_SIZE = 3
LINE_LENGTH = 9


class Cell(object):
    """
    The cell object.

    The x and y are the respective coordinates.
    neighbours is a list of all cells that impact the current cell.
    value is the current value of the cell, or None if there is no value set.
    possibilities is a list of current possible numbers for the cell
    """
    def __init__(self, x, y, value=None):
        self.x = x
        self.y = y
        self.neighbours = None
        self._value = None

        if value == 0:
            self._value = None
        else:
            self._value = value

    def __str__(self):
        return "X: {}, Y: {}, Val: {}, Possibilities: {}".format(self.x, self.y, self.value, self.possibilities)

    def __repr__(self):
        return "Cell({x}, {y}, {value})".format(x=self.x, y=self.y, value=self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """Makes sure that you can't set the value of the cell twice"""
        if self.value:
            raise ValueError("Value is already set to {}. Attempted to set value {} to cell {},{}".format(self.value, value, self.x, self.y))

        print("Changed cell. Value {} to cell {},{}".format(value, self.x, self.y))

        self._value = value

    @property
    def supercell(self):
        """Gets the coordinate of the parent supercell"""

        supercell_x = math.floor(self.x / SUPERCELL_SIZE)
        supercell_y = math.floor(self.y / SUPERCELL_SIZE)
        return (supercell_x, supercell_y)

    @property
    def possibilities(self) -> list:
        """The current possible values for the cell"""
        non_possibilities = list()

        for cell in self.neighbours:
            if cell.value:
                non_possibilities.append(cell.value)

        possibilities = list(range(1, LINE_LENGTH + 1))

        return [val for val in possibilities if val not in non_possibilities]

    def solve(self) -> Union[bool, None]:
        if self.value:
            return None

        ret_value = self.solve_last_possibility()
        ret_value = ret_value if ret_value else self.solve_last_option()

        return ret_value


    def solve_last_possibility(self) -> bool:
        """Checks if there is only one possibility left for the cell"""

        if len(self.possibilities) == 1:
            self.value = self.possibilities[0]
            print("solve_last_possibility")
            return True

        return False

    def solve_last_option(self) -> bool:
        """Checks if any of the neighbouring cells have any of the remaining possibilities"""

        possibilities = self.possibilities.copy()

        for cell in self.neighbours:
            possibilities = [val for val in possibilities if val not in cell.possibilities]

        if len(possibilities) == 1:
            self.value = possibilities[0]
            print("solve_last_option")
            return True

        return False


class Board(object):
    """The board object. It does Sudoku things"""

    def __init__(self, cells=None):
        if cells:
            self.cells = cells
        else:
            self.cells = list()

    def __str__(self):
        """Returns a string representing the current board"""

        str_list = []
        for cell in self.cells:
            if cell.value:
                str_list.append(str(cell.value))
            else:
                str_list.append(str(0))

        return "".join(str_list)

    def __iter__(self):
        return self.cells

    def load_board(self, boardstring):
        """Loads a board from a string.

        Example board strings:
        200070038000006070300040600008020700100000006007030400004080009060400000910060002
        002980500400070013039604070200056400840300201907001086600705130091400005020030608
        """
        i = 0

        for char in boardstring:
            char = int(char)
            x = i % LINE_LENGTH
            y = math.floor(i / LINE_LENGTH)

            self.cells.append(Cell(x, y, char))

            i += 1

        print("Loaded board:")

    def print_board(self):
        """Prints the board in a 9x9 grid."""

        line = self.__str__()
        print_line = ""

        # Split the line into
        for i in range(LINE_LENGTH):

            print_line += line[i*LINE_LENGTH:(i+1)*LINE_LENGTH] + "\n"

        # Print an extra line to separate previous prints
        print(print_line + "\n")

    def get_cells_where(self, **kwargs):
        """"Returns a list of the cells matching each of the provided properties"""
        return_list = []

        for arg in kwargs:
            return_list += list([cell for cell in self.cells if getattr(cell, str(arg), None) == kwargs[arg]])

        return return_list

    def set_neighbouring_cells(self, cell):
        """Finds all cells impacting the input cells and stores them in the cells list"""

        vertical_cells = self.get_cells_where(x=cell.x)
        horizontal_cells = self.get_cells_where(y=cell.y)
        supercell_cells = self.get_cells_where(supercell=cell.supercell)

        cell.neighbours = horizontal_cells + vertical_cells + supercell_cells

        while cell in cell.neighbours:
            cell.neighbours.remove(cell)

    def solve_board(self):
        """Container method to solve the board"""

        while True:
            # Store the previous version of the board
            prev_board = self.__str__()

            for cell in self.cells:
                cell.solve()

            self.print_board()

            if self.__str__() == prev_board:
                if "0" not in prev_board:
                    print("Solved!")

                break

if __name__ == "__main__":
    board = Board()

    board.load_board(str(input("Input boardstring:")))

    board.print_board()

    # Set impact list
    for cell in board.cells:
        board.set_neighbouring_cells(cell)

    board.solve_board()