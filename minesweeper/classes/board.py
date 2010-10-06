from minesweeper.classes.create_board import CreateBoard

CLEAR_SPOT = 0
MINED_SPOT = 1

class Board:
    def __init__(self, board):
        self._board = board.get_board()
        self._flags_left = board.get_num_mines()
        self._flags = []

    def is_mined(self, row, column):
        if self._board[row][column]:
            return True
        return False

    def is_flag_at(self, row, column):
        for flag in self._flags:
            if (row,column) == flag:
                return True

        return False

    def place_flag(self, row, column):
        if self._flags_left and not self.is_flag_at(row, column):
            self._flags.append((row, column))
            self._flags_left -= 1
                               
    def flags_left(self):
        return self._flags_left

    def has_won(self):
        if (self._flags_left == 0) and self._all_flags_on_mines():
            return True
        return False

    def _all_flags_on_mines(self):
        for flag in self._flags:
            if self._board[flag[0]][flag[1]] == CLEAR_SPOT:
                return False
        return True

    def get_num_surronding_mines(self, row, column):
        num_mines = 0

        for point in self._get_surronding_spots(row, column):
            if self._board[point[0]][point[1]] == MINED_SPOT:
                num_mines += 1

        return num_mines

    def _get_surronding_spots(self, row, column):
        surronding_spots = []
        for test_row in range(row - 1, row + 2):
            for test_column in range(column - 1, column + 2):
                if test_row == row and test_column == column:
                    continue

                if test_row < 0 or test_column < 0:
                    continue

                try:
                    self._board[test_row][test_column]
                except IndexError:
                    continue
                
                surronding_spots.append((test_row, test_column))

        return surronding_spots

    def get_clear_area(self, row, column, clear_area):
        "You should initially pass in [] to clear_area, it will recursively build"
        if self.get_num_surronding_mines(row, column) > 0:
            return clear_area

        clear_area.append((row, column))
        for point in self._get_surronding_spots(row, column):
            if point not in clear_area:
                clear_area = self.get_clear_area(point[0], point[1], clear_area)

        return clear_area
