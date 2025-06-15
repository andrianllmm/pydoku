import random

from constants import *


def generate_board(difficulty=1):
    """Generate a Sudoku board with numbers pre-filled and empty cells."""

    def pattern(r, c):
        row_within_subgrid = r % BASE  # Row position within the subgrid
        row_block_index = r // BASE  # Subgrid index
        adjusted_row_position = (
            BASE * row_within_subgrid + row_block_index
        )  # Adjust row position
        adjusted_position_in_grid = adjusted_row_position + c  # Add the column index
        return adjusted_position_in_grid % SIZE  # Ensure the index stays within 0-8

    def shuffle(s):
        return random.sample(s, len(s))

    # Create a complete board with shuffled rows, columns, and numbers

    rBase = range(BASE)
    rows = [
        group * BASE + r for group in shuffle(rBase) for r in shuffle(rBase)
    ]  # -> Carefully shuffled row indices [0 to 8]
    cols = [
        group * BASE + c for group in shuffle(rBase) for c in shuffle(rBase)
    ]  # -> Carefully shuffled column indices [0 to 8]

    nums = shuffle(range(1, SIZE + 1))  # -> Randomly shuffled numbers [0 to 8]

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # Remove some cells based on difficulty

    difficulty_map = {0: 0.2, 1: 0.3, 2: 0.45, 3: 0.6, 4: 0.7}

    squares = SIZE**2
    empties = int(squares * difficulty_map.get(difficulty, 0.2))

    for p in random.sample(range(squares), empties):
        board[p // SIZE][p % SIZE] = ctk.StringVar(
            root
        )  # Set empty cells to a StringVar for mutability

    return board


def get_board_copy(board):
    """Convert a board with tk.StringVar into a plain 2D list with int."""
    return [
        [
            (
                int(cell.get())
                if isinstance(cell, ctk.StringVar) and cell.get() != ""
                else 0 if isinstance(cell, ctk.StringVar) else cell
            )
            for cell in row
        ]
        for row in board
    ]


def select_index(selected, r, c):
    """Update the current selected cell index."""
    selected[0].set(r)
    selected[1].set(c)


def get_selected_index(selected):
    """Get the current selected cell index."""
    return selected[0].get(), selected[1].get()


def write_number(n, index, board):
    """Write a number into the selected modifiable cell."""
    r, c = index
    if r < 0 or c < 0:
        return

    value = board[r][c]
    if isinstance(value, ctk.StringVar):  # If modifiable
        value.set(str(n))


def erase_number(index, board):
    """Erase the number of the selected modifiable cell."""
    r, c = index
    if r < 0 or c < 0:
        return

    value = board[r][c]
    if isinstance(value, ctk.StringVar):  # If modifiable
        value.set("")


def is_board_solved(board):
    """Check if the current Sudoku board is solvable."""
    return is_board_filled(board) and is_board_valid(board)


def is_board_filled(board):
    """Check if the current Sudoku board has no empty cells."""
    board_copy = get_board_copy(board)
    # Check if all cells are non-zero (no empty cells)
    return all(c != 0 for r in board_copy for c in r)


def is_board_valid(board):
    """Check if the current Sudoku board is has no duplicates."""
    board_copy = get_board_copy(board)

    # Helper function to check if a group (row, column, or subgrid) contains duplicates
    def is_valid_group(group):
        nums = [int(n) for n in group if n != 0]
        return len(nums) == len(set(nums))

    # Check each row
    for row in board_copy:
        if not is_valid_group(row):
            return False

    # Check each column
    for col in zip(*board_copy):  # Transpose board
        if not is_valid_group(col):
            return False

    # Check each subgrid
    for i in range(0, SIZE, BASE):
        for j in range(0, SIZE, BASE):
            # Flatten the subgrid into a list
            subgrid = [
                board_copy[r][c] for r in range(i, i + BASE) for c in range(j, j + BASE)
            ]
            if not is_valid_group(subgrid):
                return False

    return True


def solve_board(board, r=0, c=0):
    """Solve the current Sudoku board using a backtracking algorithm."""

    # The indices reached the last cell, hence the board is fully solved
    if r == SIZE - 1 and c == SIZE:
        return board

    # The column index reaches the end, move to the next row
    if c == SIZE:
        r += 1
        c = 0

    # Skip cells that already have a value (move to the next cell)
    if board[r][c] > 0:
        return solve_board(board, r, c + 1)

    # Try every number (1-9) in the current cell
    for num in range(1, SIZE + 1):
        board[r][c] = num

        # Placing the number results in a valid board state, continue solving
        if is_board_valid(board):
            result = solve_board(board, r, c + 1)
            if result:
                return board

        # The number didn't lead to a solution, reset and try the next one (backtrack)
        board[r][c] = 0

    # No solution is found
    return None


def show_hint(hints_left, board, solved_board, index):
    """Provide a hint for the selected cell by filling in the correct value."""

    # Check remaining hints
    if hints_left.get() <= 0:
        return

    r, c = index
    if r < 0 and c < 0:
        return

    if solved_board and isinstance(board[r][c], ctk.StringVar):
        # Update the board with the correct value from the solved board
        board[r][c].set(str(solved_board[r][c]))

        # Decrease remaining hints
        hints_left.set(hints_left.get() - 1)
