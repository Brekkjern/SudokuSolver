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
