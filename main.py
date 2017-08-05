import math

SUPERCELL_SIZE = 3
LINE_LENGTH = 9

class Cell(object):
    """
    The cell object.
    Does this need more explaining?

    The X and Y are the respective coordinates.
    relevant_cells is a list of all cells that impact the current cell.
    value is the current value of the cell, or None if there is no value set.
    possibilities is a list of current possible numbers for the cell
    """
    def __init__(self, x, y, value=None):
        self.x = x
        self.y = y
        self.relevant_cells = None
        self._value = None

        if value == 0:
            self.value = None
        else:
            self.value = value

        self.possibilities = list(range(1, LINE_LENGTH + 1))

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

        if value is not None:
            self.possibilities = list()

        print("Changed cell. Value {} to cell {},{}".format(value, self.x, self.y))
        self._value = value

    @property
    def supercell(self):
        """Gets the coordinate of the parent supercell"""

        supercell_x = math.floor(self.x / SUPERCELL_SIZE)
        supercell_y = math.floor(self.y / SUPERCELL_SIZE)
        return (supercell_x, supercell_y)


class Board(object):
    """The board object. It does Sudoku things"""

    def __init__(self, cells=None):
        if cells:
            self.cells = cells
        else:
            self.cells = list()

    def __str__(self):
        """Returns a boardstring for the current board."""

        str_list = []
        for cell in self.cells:
            if cell.value:
                str_list.append(str(cell.value))
            else:
                str_list.append(str(0))

        return "".join(str_list)

    def load_board(self, boardstring):
        """Loads a board from a string.

        Example board string: 200070038000006070300040600008020700100000006007030400004080009060400000910060002
        """
        i = 0

        for char in boardstring:
            char = int(char)
            x = i % LINE_LENGTH
            y = math.floor(i / LINE_LENGTH)

            self.cells.append(Cell(x, y, char))

            i += 1

    def print_board(self):
        """Prints the board in a 9x9 grid."""

        line = self.__str__()
        print_line = ""

        # Split the line into
        for i in range(LINE_LENGTH):

            print_line += line[i*LINE_LENGTH:(i+1)*LINE_LENGTH] + "\n"

        # Print an extra line to separate previous prints
        print(print_line + "\n")

    def get_line_members(self, **kwargs):
        """"Returns a list of the cells matching each of the provided properties"""
        return_list = []

        for arg in kwargs:
            return_list += list([cell for cell in self.cells if getattr(cell, str(arg), None) == kwargs[arg]])

        return return_list

    def get_cell_values(self, cells):
        """Returns a list with the values of the cells that were input"""

        return [cell.value for cell in cells]

    def solve_last_in_sequence(self, sequence):
        """
        Attempts to find any cell that can only have that number.

        :param sequence:
        :return none:
        """

        # List of numbers
        nums = list(range(1, LINE_LENGTH + 1))

        # Remove numbers from numbers list if they are already in the sequence
        for cell in sequence:
            if cell.value in nums:
                nums.remove(cell.value)

        # Loops through the remaining numbers
        for num in nums:

            # Finds all cells with that possible number
            num_cells = [cell for cell in sequence if num in cell.possibilities]

            # If only one cell can have the number, set that cell to the number
            if len(num_cells) == 1:
                num_cells[0].value = num

    def set_impacting_cells(self, cell):
        """Finds all cells impacting the input cells and stores them in the cells list"""

        vertical_cells = self.get_line_members(x=cell.x)
        horizontal_cells = self.get_line_members(y=cell.y)
        supercell_cells = self.get_line_members(supercell = cell.supercell)

        cell.relevant_cells = horizontal_cells + vertical_cells + supercell_cells

    def find_cell_possibilities(self):
        """Finds all possible values for cells"""

        for cell in self.cells:
            if cell.value:
                continue

            cell.possibilities = [val for val in cell.possibilities if
                                  val not in self.get_cell_values(cell.relevant_cells)]

    def solve_last_possibility(self):
        """Finds all cells that have only a single possible value left"""

        for candidate_cell in self.cells:
            # Skip cells with values
            if candidate_cell.value:
                continue

            # If the cell has only one possibility left, set it to the last remaining value
            if len(candidate_cell.possibilities) == 1:
                candidate_cell.value = candidate_cell.possibilities[0]

    def solve_board(self):
        """Container method to solve the board"""

        while True:
            # Store the previous version of the board
            prev_board = self.__str__()

            self.find_cell_possibilities()
            self.solve_last_possibility()
            self.find_cell_possibilities()

            for x in range(0, 3):
                for y in range(0, 3):
                    self.solve_last_in_sequence(self.get_line_members(supercell=(x, y)))

            self.find_cell_possibilities()

            for i in range(LINE_LENGTH):
                self.solve_last_in_sequence(self.get_line_members(x=i))
                self.solve_last_in_sequence(self.get_line_members(y=i))

            self.find_cell_possibilities()

            self.print_board()

            if self.__str__() == prev_board:
                break

if __name__ == "__main__":
    board = Board()

    print("Input boardstring:")
    board.load_board(str(input()))
    board.print_board()

    # Set impact list
    for cell in board.cells:
        board.set_impacting_cells(cell)

    board.solve_board()

    board.print_board()