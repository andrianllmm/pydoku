import pytest
import customtkinter as ctk

import app


@pytest.fixture
def solved_board():
    return [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]


@pytest.fixture
def unsolved_board():
    return [
        [5, 3, ctk.StringVar(), 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, ctk.StringVar()],
    ]


@pytest.fixture
def invalid_board():
    return [
        [5, 5, 0, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]


def test_generate_board():
    board = app.generate_board()
    assert len(board) == app.SIZE
    assert all(len(row) == app.SIZE for row in board)
    assert all(
        0 <= cell <= app.SIZE for row in app.get_board_copy(board) for cell in row
    )


def test_is_solved(solved_board, unsolved_board):
    assert app.is_board_solved(solved_board)
    assert not app.is_board_solved(unsolved_board)


def test_write_number(unsolved_board):
    prev_value = unsolved_board[0][0]
    app.write_number(1, (0, 0), unsolved_board)
    assert unsolved_board[0][0] == prev_value

    value = 1
    r, c = 0, 2
    assert unsolved_board[0][2].get() == ""
    app.write_number(value, (r, c), unsolved_board)
    assert int(unsolved_board[r][c].get()) == value


def test_erase_number(unsolved_board):
    prev_value = unsolved_board[0][0]
    app.erase_number((0, 0), unsolved_board)
    assert unsolved_board[0][0] == prev_value

    value = 1
    r, c = 0, 2
    app.write_number(value, (r, c), unsolved_board)
    assert int(unsolved_board[r][c].get()) == value
    app.erase_number((r, c), unsolved_board)
    assert unsolved_board[r][c].get() == ""


def test_is_board_field(solved_board, unsolved_board):
    assert app.is_board_filled(solved_board)
    assert not app.is_board_filled(unsolved_board)


def test_is_board_valid(solved_board, unsolved_board, invalid_board):
    assert app.is_board_valid(solved_board)
    assert app.is_board_valid(unsolved_board)
    assert not app.is_board_valid(invalid_board)


def test_solve_board(unsolved_board):
    board = app.get_board_copy(unsolved_board)
    assert app.solve_board(board)
    assert app.is_board_solved(board)


def test_show_hint(unsolved_board):
    r, c = 0, 2
    solved_board = app.solve_board(app.get_board_copy(unsolved_board))
    app.show_hint(ctk.IntVar(value=3), unsolved_board, solved_board, (r, c))
    assert int(unsolved_board[r][c].get()) == solved_board[r][c]
