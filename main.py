from SudokuSolver import board

SUPERCELL_SIZE = 3
LINE_LENGTH = 9


if __name__ == "__main__":
    board = board.Board()

    board.load_board(str(input("Input boardstring:")))

    board.print_board()

    # Set impact list
    for cell in board.cells:
        board.set_neighbouring_cells(cell)

    board.solve_board()