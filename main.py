import math

SUPERCELL_SIZE = 3
LINE_LENGTH = 9

class Cell(object):

    def __init__(self, x, y, value=None):
        self.x = x
        self.y = y

        if value == 0:
            self.value = None
            self.possibilities = list(range(1, LINE_LENGTH + 1))
        else:
            self.value = value
            self.possibilities = list()

    def get_supercell(self):
        supercell_x = math.floor(self.x / SUPERCELL_SIZE)
        supercell_y = math.floor(self.y / SUPERCELL_SIZE)
        return supercell_x, supercell_y

    def __str__(self):
        return "X: {}, Y: {}, Val: {}, Possibilities: {}".format(self.x, self.y, self.value, self.possibilities)

class Board(object):

    def __init__(self, cells=None):
        if cells:
            self.cells = cells
        else:
            self.cells = list()

    def load_board(self, boardstring):
        i = 0

        for char in boardstring:
            char = int(char)
            x = i % LINE_LENGTH
            y = math.floor(i / LINE_LENGTH)

            self.cells.append(Cell(x, y, char))

            i += 1

    def __str__(self):
        str_list = []
        for cell in self.cells:
            if cell.value:
                str_list.append(str(cell.value))
            else:
                str_list.append(str(0))

        return "".join(str_list)

    def print_board(self):
        for cell in self.cells:
            print(cell)

    def get_supercell_members(self, supercell):
        return [cell for cell in self.cells if cell.get_supercell() == supercell]

    def get_horizontal_members(self, y):
        return [cell for cell in self.cells if cell.y == y]

    def get_vertical_members(self, x):
        return [cell for cell in self.cells if cell.x == x]

    def get_cell_values(self, cells):
        return [cell.value for cell in cells]

    def solve_board(self):
        change = False

        while True:
            for cell in self.cells:
                if cell.value:
                    continue

                prev_possibilities = len(cell.possibilities.copy())

                horizontal_cells = self.get_horizontal_members(cell.y)
                horizontal_values = self.get_cell_values(horizontal_cells)

                vertical_cells = self.get_vertical_members(cell.x)
                vertical_values = self.get_cell_values(vertical_cells)

                supercell_cells = self.get_supercell_members(cell.get_supercell())
                supercell_values = self.get_cell_values(supercell_cells)

                cell.possibilities = [val for val in cell.possibilities if val not in horizontal_values]
                cell.possibilities = [val for val in cell.possibilities if val not in vertical_values]
                cell.possibilities = [val for val in cell.possibilities if val not in supercell_values]

                for i in cell.possibilities:
                    for l_cell in horizontal_cells:
                        if l_cell == cell:
                            continue
                        else:
                            if i in l_cell.possibilities:
                                break

                        cell.value = i

                for i in cell.possibilities:
                    for l_cell in vertical_cells:
                        if l_cell == cell:
                            continue
                        else:
                            if i in l_cell.possibilities:
                                break

                        cell.value = i

                for i in cell.possibilities:
                    for l_cell in supercell_cells:
                        if l_cell == cell:
                            continue
                        else:
                            if i in l_cell.possibilities:
                                break

                        cell.value = i

                if len(cell.possibilities) == 1:
                    cell.value = cell.possibilities[0]

                if prev_possibilities != len(cell.possibilities):
                    change = True

            print(self)
            if not change:
                break

    def return_boardstring(self):
        for cell in self.cells:
            if not cell.value:
                val = 0
            else:
                val = cell.value

            print(val, end='')
        print()

if __name__ == "__main__":
    board = Board()

    print("Input boardstring:")
    board.load_board(str(input()))

    board.solve_board()

    print(board)