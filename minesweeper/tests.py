from django.test import TestCase

from minesweeper.classes.create_board import CreateBoard, CreateTestBoard
from minesweeper.classes.board import Board

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

class CreateTestBoardTest(TestCase):
    def test_testing_board(self):
        create_test_board = CreateTestBoard(BOARD_ROWS, BOARD_COLUMNS, TOTAL_MINES)
        self.failUnlessEqual(create_test_board.get_board(), self.get_test_board())

    def get_test_board(self):
        return [[1, 1, 1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]


class BoardTest(TestCase):
    def setUp(self):
        create_test_board = CreateTestBoard(BOARD_ROWS, BOARD_COLUMNS, TOTAL_MINES)
        self.board = Board(create_test_board)

    def test_click_mine(self):
        self.failUnlessEqual(self.board.is_mined(0,0), True, 'There was no mine at 0,0')
        self.failUnlessEqual(self.board.is_mined(1,0), False, 'There was no mine at 1,0')

    def test_place_flag(self):
        self.board.place_flag(0,0)
        self.failUnlessEqual(self.board.flags_left(), TOTAL_MINES - 1, 'A flag was not placed')

        self.board.place_flag(0,0)
        self.failUnlessEqual(self.board.flags_left(), TOTAL_MINES - 1, 'A flag was set on top of a flag')

    def test_win(self):
        for column in range(BOARD_COLUMNS - 1):
            self.board.place_flag(0, column)

        self.failUnlessEqual(self.board.has_won(), False, 'The player should not have won')

        for column in range(5, BOARD_COLUMNS):
            self.board.place_flag(1, column)
        self.failUnlessEqual(self.board.has_won(), True, 'The player should have won but did not')
