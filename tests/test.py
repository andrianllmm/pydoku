import pytest
import customtkinter as ctk

import sudoku.model as model


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
    board = model.generate_board()
    assert len(board) == model.SIZE
    assert all(len(row) == model.SIZE for row in board)
    assert all(
        0 <= cell <= model.SIZE for row in model.get_board_copy(board) for cell in row
    )


def test_write_number(unsolved_board):
    prev_value = unsolved_board[0][0]
    model.write_number(1, (0, 0), unsolved_board)
    assert unsolved_board[0][0] == prev_value

    value = 1
    r, c = 0, 2
    assert unsolved_board[0][2].get() == ""
    model.write_number(value, (r, c), unsolved_board)
    assert int(unsolved_board[r][c].get()) == value


def test_erase_number(unsolved_board):
    prev_value = unsolved_board[0][0]
    model.erase_number((0, 0), unsolved_board)
    assert unsolved_board[0][0] == prev_value

    value = 1
    r, c = 0, 2
    model.write_number(value, (r, c), unsolved_board)
    assert int(unsolved_board[r][c].get()) == value
    model.erase_number((r, c), unsolved_board)
    assert unsolved_board[r][c].get() == ""


def test_is_solved(solved_board, unsolved_board):
    assert model.is_board_solved(solved_board)
    assert not model.is_board_solved(unsolved_board)


def test_is_board_filled(solved_board, unsolved_board):
    assert model.is_board_filled(solved_board)
    assert not model.is_board_filled(unsolved_board)


def test_is_board_valid(solved_board, unsolved_board, invalid_board):
    assert model.is_board_valid(solved_board)
    assert model.is_board_valid(unsolved_board)
    assert not model.is_board_valid(invalid_board)


def test_solve_board(unsolved_board):
    board = model.get_board_copy(unsolved_board)
    assert model.solve_board(board)
    assert model.is_board_solved(board)


def test_show_hint(unsolved_board):
    r, c = 0, 2
    solved_board = model.solve_board(model.get_board_copy(unsolved_board))
    model.show_hint(ctk.IntVar(value=3), unsolved_board, solved_board, (r, c))
    assert int(unsolved_board[r][c].get()) == solved_board[r][c]
