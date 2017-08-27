import math
from SudokuSolver.cell import Cell

class Board(object):
    """The board object. It does Sudoku things"""

    def __init__(self, boardstring, super_cell_size=3):
        self.cells = list()
        self.SUPERCELL_SIZE = super_cell_size
        self.load_board(boardstring)

        for cell in self.cells:
            self.set_neighbouring_cells(cell)

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

    @property
    def line_length(self):
        return self.SUPERCELL_SIZE ** 2

    def load_board(self, boardstring):
        """Loads a board from a string.

        Example board strings:
        200070038000006070300040600008020700100000006007030400004080009060400000910060002
        002980500400070013039604070200056400840300201907001086600705130091400005020030608
        """

        for index, char in enumerate(boardstring):
            char = int(char)
            x = index % self.line_length
            y = math.floor(index / self.line_length)

            self.cells.append(Cell(self, x, y, char))

        print("Loaded board:")

    def print_board(self):
        """Prints the board in a 9x9 grid."""

        line = self.__str__()
        print_line = ""

        # Split the line into
        for i in range(self.line_length):

            print_line += line[i*self.line_length:(i+1)*self.line_length] + "\n"

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

        cell.neighbours = self.get_cells_where(supercell=cell.supercell, y=cell.y, x=cell.x)

        while cell in cell.neighbours:
            cell.neighbours.remove(cell)

    def solve_board(self):
        """Container method to solve the board"""

        while True:
            # Store the previous version of the board
            prev_board = str(self)

            for cell in self.cells:
                cell.solve()

            self.print_board()

            if str(self) == prev_board:
                if "0" not in prev_board:
                    print("Solved!")

                break
