from django.test import TestCase

from minesweeper.classes.create_board import CreateBoard

BOARD_COLUMNS = 8
BOARD_ROWS = 8

TOTAL_MINES = 10

class CreateBoardTest(TestCase):
    def setUp(self):
        self.create_board = CreateBoard(BOARD_ROWS, BOARD_COLUMNS, TOTAL_MINES)
        self.board = self.create_board.get_board()

    def test_create_board(self):
        self.failUnlessEqual(len(self.board), BOARD_ROWS)
        self.failUnlessEqual(len(self.board[0]), BOARD_COLUMNS)

    def test_created_10_mines(self):
        mines = 0
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                mines += self.board[row][column]

        self.failUnlessEqual(mines, TOTAL_MINES)
