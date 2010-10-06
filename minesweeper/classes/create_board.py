import random

class CreateBoard:
    def __init__(self, rows, columns, mines):
        self._board = []
        self._rows = rows
        self._columns = columns

        for i in range(self._rows):
            row = []
            for j in range(self._columns):
                row.append(0)
            self._board.append(row)

        self._place_mines(mines)

    def _place_mines(self, mines):
        if mines == 0:
            return

        row = random.randint(0, self._rows - 1)
        column = random.randint(0, self._columns - 1)

        if self._board[row][column]:
            self._place_mines(mines)
        else:
            self._board[row][column] = 1
            self._place_mines(mines - 1)

    def get_board(self):
        return self._board
