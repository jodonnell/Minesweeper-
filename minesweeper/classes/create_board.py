import random

# An object that is responsible for creating a new board data structure and placing the mines

class AbstractBoard:
    def __init__(self):
        raise "Abstract class"

    def _create_board(self, rows, columns, mines):
        self._board = []
        self._rows = rows
        self._columns = columns
        self._total_mines = mines

        for i in range(self._rows):
            row = []
            for j in range(self._columns):
                row.append(0)
            self._board.append(row)

        self._place_mines(mines)

    def get_board(self):
        return self._board

    def get_num_mines(self):
        return self._total_mines

class CreateBoard(AbstractBoard):
    def __init__(self, rows, columns, mines):
        self._create_board(rows, columns, mines)

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


class CreateTestBoard(AbstractBoard):
    "Expects that there will be 10 mines and at least 8 columns"
    def __init__(self, rows, columns, mines):
        self._create_board(rows, columns, mines)

    def _place_mines(self, mines):
        for column in range(self._columns - 1):
            self._board[0][column] = 1

        for column in range(5, self._columns):
            self._board[1][column] = 1
