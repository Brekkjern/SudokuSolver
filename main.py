from SudokuSolver import board


if __name__ == "__main__":
    board = board.Board()
    board.print_board()
    board.solve_board()