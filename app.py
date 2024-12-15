import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
import random
import time

# --- Constants ---
BASE = 3  # Base size of the Sudoku grid (3x3 sub-grids)
SIZE = BASE**2  # Total size of the grid (9x9)
CELL_SIZE = 50  # Size of each cell in pixels
WIDTH = CELL_SIZE * 20  # Window width
HEIGHT = WIDTH // 16 * 9  # Window height (16:9 aspect ratio)
TITLE = "Sudoku"  # App title

# --- Styles ---
ctk.set_default_color_theme("assets/custom_theme.json")
ctk.set_appearance_mode("light")

# Color Palette
PALETTE = {
    "bg": "#ffffff",
    "fg": "#344861",
    "border": "#344861",
    "primary": "#325aaf",
    "primary-hover": "#7091d5",
    "primary-bg": "#e2ebf3",
    "primary-bg-hover": "#dce3ed",
    "highlight": "#bbdefb",
    "highlight-muted": "#c3d7ea",
    "success": "#6d8265",
    "success-bg": "#def2d6",
    "error": "#b0444f",
    "error-bg": "#ebc8c4",
    "warning": "#baa57c",
    "warning-bg": "#f8f3d6",
}

# --- Application Window ---
root = ctk.CTk()
root.title(TITLE)

# Set window size and center it on the screen
window_width = root.winfo_screenwidth()
window_heigth = root.winfo_screenheight()

root.geometry(
    f"{WIDTH}x{HEIGHT}+{(window_width - WIDTH) // 2}+{(window_heigth - HEIGHT) // 2}"
)

root.minsize(WIDTH, HEIGHT)


# --- Model ---


def generate_board(difficulty=1):
    """Generate a Sudoku board with numbers pre-filled and empty cells."""

    def pattern(r, c):
        return (BASE * (r % BASE) + r // BASE + c) % SIZE

    def shuffle(s):
        return random.sample(s, len(s))

    # Create a complete board with shuffled rows, columns, and numbers
    rBase = range(BASE)
    rows = [g * BASE + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * BASE + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, SIZE + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # Remove some cells based on difficulty
    squares = SIZE**2
    difficulty_map = {0: 0.2, 1: 0.3, 2: 0.45, 3: 0.6, 4: 0.7}
    empties = int(squares * difficulty_map.get(difficulty, 0.2))

    for p in random.sample(range(squares), empties):
        board[p // SIZE][p % SIZE] = ctk.StringVar(root)

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
    r, c = index  # Row and column index
    if r < 0 or c < 0:  # Invalid if negative
        return
    value = board[r][c]
    if isinstance(value, ctk.StringVar):  # If modifiable
        value.set(str(n))


def erase_number(index, board):
    """Erase the number of the selected modifiable cell."""
    r, c = index  # Row and column index
    if r < 0 or c < 0:  # Invalid if negative
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

    # The indices reached the last cell, the board is fully solved
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

    # Check if there are any hints left
    if hints_left.get() <= 0:
        return

    r, c = index
    if r < 0 and c < 0:
        return

    if solved_board and isinstance(board[r][c], ctk.StringVar):
        # Update the board with the correct value from the solved board
        board[r][c].set(str(solved_board[r][c]))

        # Decrease the remaining hint count
        hints_left.set(hints_left.get() - 1)


# --- View ---


def create_board_widget(master, board, selected):
    """Create a widget displaying the Sudoku board."""

    # Event handler when cell is clicked (selected)
    def on_select(r, c):
        select_index(selected, r, c),
        update_highlights(selected, board, cell_labels)

    frame = ctk.CTkFrame(
        master, fg_color=PALETTE["border"], border_width=2, corner_radius=0
    )

    # 2d list to store references to cell labels
    cell_labels = [[None] * SIZE for _ in range(SIZE)]

    # Create 3x3 subgrid frames
    for i in range(0, SIZE, BASE):
        for j in range(0, SIZE, BASE):
            subgrid_frame = ctk.CTkFrame(
                frame, fg_color="white", border_width=3, corner_radius=0
            )

            # Create cells
            for k in range(BASE):
                for l in range(BASE):
                    r, c = k + i, l + j  # Calculate global index
                    value = board[r][c]
                    modifiable = isinstance(
                        value, ctk.StringVar
                    )  # Check if cell is modifiable

                    cell_frame = ctk.CTkFrame(
                        subgrid_frame,
                        fg_color="transparent",
                        border_width=1,
                        corner_radius=0,
                    )
                    label = ctk.CTkLabel(
                        cell_frame,
                        text=str(value.get()) if modifiable else str(value),
                        textvariable=value if modifiable else None,
                        anchor="center",
                        text_color=PALETTE["primary"] if modifiable else None,
                    )

                    cell_labels[r][c] = label

                    # Add click event listener for selection
                    label.bind(
                        "<Button-1>",
                        lambda event, r=r, c=c: on_select(r, c),
                    )

                    label.pack(expand=True, fill="both", padx=1, pady=1)
                    cell_frame.grid(row=k, column=l, sticky="news")

            for m in range(BASE):
                subgrid_frame.grid_rowconfigure(m, weight=1, minsize=CELL_SIZE)
                subgrid_frame.grid_columnconfigure(m, weight=1, minsize=CELL_SIZE)

            subgrid_frame.grid(
                row=i // BASE, column=j // BASE, padx=0.5, pady=0.5, sticky="news"
            )

    return frame


def update_highlights(selected, board, cell_labels):
    """Update the highlighting for the selected cell, row, column, and sub-grid."""
    board_copy = get_board_copy(board)
    r, c = get_selected_index(selected)

    for i in range(SIZE):
        for j in range(SIZE):
            # Highlight the selected cell
            if (i, j) == (r, c):
                cell_labels[i][j].configure(fg_color=PALETTE["highlight"])

            # Highlight cells with the same number
            elif (
                board_copy[r][c]
                and board_copy[i][j]
                and board_copy[r][c] == board_copy[i][j]
            ):
                cell_labels[i][j].configure(fg_color=PALETTE["highlight-muted"])

            # Highlight cells in the same row, column, or sub-grid
            elif (
                r == i
                or c == j
                or ((i // BASE == r // BASE) and (j // BASE == c // BASE))
            ):
                cell_labels[i][j].configure(fg_color=PALETTE["primary-bg"])

            # Reset unhighlighted cells
            else:
                cell_labels[i][j].configure(fg_color="transparent")


def create_numpad_widget(master, selected, board, running):
    """Create a widget for entering numbers into the board."""

    # Event handler when a number button is clicked
    def on_write(n, index, board):
        write_number(n, index, board)
        if is_board_solved(board):
            running.set(False)
            show_endgame_modal(root)

    frame = ctk.CTkFrame(master, fg_color="transparent")

    # Create buttons from 1-9
    for i in range(1, SIZE + 1):
        btn = ctk.CTkButton(
            frame,
            text=str(i),
            font=("", 28),
            command=lambda n=i: on_write(n, get_selected_index(selected), board),
        )
        btn.grid(
            row=(i - 1) // BASE, column=(i - 1) % BASE, sticky="news", padx=5, pady=5
        )

    for k in range(BASE):
        frame.grid_rowconfigure(k, weight=1, minsize=CELL_SIZE * 2)
        frame.grid_columnconfigure(k, weight=1, minsize=CELL_SIZE * 2)

    return frame


def create_erase_btn(master, selected, board):
    """Create an button to clear the number from a cell."""
    frame = ctk.CTkFrame(master)

    icon = ctk.CTkImage(Image.open("assets/icons/erase.png"), size=(45, 40))
    btn = ctk.CTkButton(
        frame,
        text="",
        image=icon,
        width=CELL_SIZE * 1.5,
        corner_radius=100,
        command=lambda: erase_number(get_selected_index(selected), board),
    )
    btn.pack(padx=5, pady=5, ipadx=10, ipady=10)

    label = ctk.CTkLabel(frame, text="Erase", text_color=PALETTE["primary"])
    label.pack()

    return frame


def create_check_btn(master, board):
    """Create a button to check if the board is solved."""
    frame = ctk.CTkFrame(master)

    icon = ctk.CTkImage(Image.open("assets/icons/check.png"), size=(40, 40))
    btn = ctk.CTkButton(
        frame,
        text="",
        image=icon,
        width=CELL_SIZE * 1.5,
        corner_radius=100,
        command=lambda: show_message(
            root,
            "Correct!" if is_board_solved(board) else "Incorrect!",
            type="success" if is_board_solved(board) else "error",
        ),
    )
    btn.pack(padx=5, pady=5, ipadx=10, ipady=10)

    label = ctk.CTkLabel(frame, text="Check", text_color=PALETTE["primary"])
    label.pack()

    return frame


def create_hint_btn(master, hints_left, board, solved_board, selected):
    """Create a button to show hint."""
    frame = ctk.CTkFrame(master)

    icon = ctk.CTkImage(Image.open("assets/icons/lightbulb.png"), size=(30, 40))
    btn = ctk.CTkButton(
        frame,
        text="",
        image=icon,
        width=CELL_SIZE * 1.5,
        corner_radius=100,
        command=lambda: show_hint(
            hints_left, board, solved_board, get_selected_index(selected)
        ),
    )
    btn.pack(padx=5, pady=5, ipadx=10, ipady=10)

    hints_left_label = ctk.CTkLabel(
        btn,
        fg_color=PALETTE["primary"],
        text_color=PALETTE["bg"],
        font=("", 14),
        width=12,
        height=12,
        corner_radius=12,
        textvariable=hints_left,
    )
    hints_left_label.place(relx=0.95, rely=0.05, anchor="ne")

    label = ctk.CTkLabel(frame, text="Hint", text_color=PALETTE["primary"])
    label.pack()

    return frame


def create_timer_widget(master, running):
    """Create a widget for the timer."""
    frame = ctk.CTkFrame(master, fg_color="transparent")

    timer_label = ctk.CTkLabel(
        frame,
        text="00:00",
        font=("", 20),
        anchor="center",
    )
    timer_label.pack(padx=10, pady=10)

    start_time = None
    elapsed_time = 0

    def update_timer():
        if not running.get():
            return

        nonlocal start_time, elapsed_time

        if start_time is None:
            start_time = time.time() - elapsed_time

        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_str = f"{minutes:02}:{seconds:02}"

        if timer_label.winfo_exists():
            timer_label.configure(text=time_str)
            frame.after(1000, update_timer)  # Recursively update every second

    update_timer()

    return frame


def create_home_btn(master):
    """Create a button to go back to the homepage."""
    btn = ctk.CTkButton(
        master,
        text="◄",
        font=("", 25),
        fg_color="transparent",
        hover_color=PALETTE["bg"],
        anchor="w",
        command=homepage,
    )
    return btn


def create_new_game_widget(master):
    """Create a widget for selecting a difficulty and starting a new game with a button."""
    # Select difficulty
    frame = ctk.CTkFrame(master)

    difficulties = ["Quickie", "Easy", "Medium", "Hard", "Expert"]
    selected_difficulty = ctk.IntVar(root, value=1)

    difficulty_combobox = ctk.CTkComboBox(
        frame,
        values=difficulties,
        command=lambda choice: selected_difficulty.set(difficulties.index(choice)),
    )
    difficulty_combobox.set("Easy")
    difficulty_combobox.pack(padx=5, pady=5)

    # New game button
    new_game_btn = ctk.CTkButton(
        frame,
        text="New Game",
        fg_color=PALETTE["primary"],
        hover_color=PALETTE["primary-hover"],
        text_color=PALETTE["bg"],
        command=lambda: start_game(selected_difficulty.get()),
    )
    new_game_btn.pack(padx=5, pady=5)

    return frame


def show_endgame_modal(master):
    """Show a window when the game ends."""
    modal = ctk.CTkToplevel(master)
    modal.attributes("-topmost", True)
    modal.title("Endgame")
    modal_width, modal_height = WIDTH // 2, HEIGHT // 2
    modal.geometry(
        f"{modal_width}x{modal_height}+{(window_width - modal_width) // 2}+{(window_heigth - modal_height) // 2}"
    )
    modal.overrideredirect(True)

    frame = ctk.CTkFrame(modal)
    frame.pack(expand=True, fill="both")
    message = ctk.CTkLabel(frame, text="You won!", font=("", 20, "bold"))
    message.pack(padx=10, pady=50)
    new_game_options = create_new_game_widget(frame)
    new_game_options.pack(padx=10, pady=10)


def show_message(master, text, type=None, duration=1000):
    """Display a temporary message (toast) on the screen."""
    message_label = ctk.CTkLabel(
        master,
        text=text,
        bg_color="transparent",
        fg_color=PALETTE.get(type + "-bg" if type else "primary-bg"),
        text_color=PALETTE.get(type if type else "primary"),
        padx=10,
        pady=10,
    )
    message_label.place(relx=0.5, rely=0.5, anchor="center")

    # Schedule the message to disappear
    master.after(duration, message_label.destroy)


def reset_ui(master):
    """Resets the UI by destroying all widgets inside master."""
    for widget in master.winfo_children():
        widget.destroy()


# --- Pages ---


def homepage():
    """Displays the homepage."""
    reset_ui(root)

    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Title
    title_label = ctk.CTkLabel(frame, text=TITLE, font=("", 36, "bold"))
    title_label.pack(padx=25, pady=25)

    new_game_options = create_new_game_widget(frame)
    new_game_options.pack()

    # Help button
    help_btn = ctk.CTkButton(
        frame,
        text="Help",
        command=help_page,
    )
    help_btn.pack(padx=5, pady=10)


def help_page():
    """Displays the help page."""
    reset_ui(root)

    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Home button
    home_btn = create_home_btn(frame)
    home_btn.pack(fill="x", anchor="w", padx=5, pady=5)

    # Title
    title_label = ctk.CTkLabel(frame, text="Help", font=("", 36, "bold"))
    title_label.pack(padx=25, pady=25)

    # Instructions
    instructions = (
        "Sudoku is a logic-based number puzzle game.\n\n"
        "Objective:\nFill the 9x9 grid so that each row, column, and 3x3 subgrid\ncontains the digits 1 to 9 without repetition.\n\n"
        "How to Play:\n"
        "- Click on an empty cell and enter a number (1-9).\n"
        "- Use the erase button to clear a cell.\n\n"
        "Features:\n"
        "- Difficulty: Start a fresh puzzle with your preferred level.\n"
        "- Check Solution: Validate your progress.\n"
        "- Hint: Reveal the correct number for a selected cell.\n\n"
    )
    instructions_label = ctk.CTkLabel(frame, text=instructions, anchor="w")
    instructions_label.pack(padx=25, pady=25)


def start_game(difficulty):
    """Starts a game."""
    reset_ui(root)

    # Initialize the Sudoku board and game state variables
    board = generate_board(
        difficulty
    )  # Initial Sudoku grid based on the chosen difficulty
    solved_board = solve_board(
        get_board_copy(board)
    )  # Fully solved version of the Sudoku grid
    selected = (
        ctk.IntVar(root, value=-1),
        ctk.IntVar(root, value=-1),
    )  # Coordinates of the currently selected cell (row, column)
    running = ctk.BooleanVar(root, value=True)  # Indicates if the game is ongoing
    hints_left = ctk.IntVar(root, value=3)  # Number of hints remaining

    # Create widgets
    header_frame = ctk.CTkFrame(root)
    home_btn = create_home_btn(header_frame)
    title_label = ctk.CTkLabel(header_frame, text=TITLE, font=("", 24, "bold"))
    timer_widget = create_timer_widget(header_frame, running)

    board_frame = ctk.CTkFrame(root)
    board_widget = create_board_widget(board_frame, board, selected)

    controls_frame = ctk.CTkFrame(root)
    actions_frame = ctk.CTkFrame(controls_frame)
    erase_btn = create_erase_btn(actions_frame, selected, board)
    check_btn = create_check_btn(actions_frame, board)
    hint_btn = create_hint_btn(actions_frame, hints_left, board, solved_board, selected)
    numpad_widget = create_numpad_widget(controls_frame, selected, board, running)

    # Place widgets
    # Header
    header_frame.grid_columnconfigure(0, weight=1)
    header_frame.grid_columnconfigure(1, weight=1)
    header_frame.grid_columnconfigure(2, weight=1)
    home_btn.grid(row=0, column=0, sticky="w")
    title_label.grid(row=0, column=1, sticky="nsew")
    timer_widget.grid(row=0, column=2, sticky="e")

    # Board
    board_widget.pack(anchor="e")

    # Controls
    actions_frame.grid(row=0, column=0)
    erase_btn.pack(side="left", padx=5, pady=5)
    check_btn.pack(side="left", padx=5, pady=5)
    hint_btn.pack(side="left", padx=5, pady=5)
    numpad_widget.grid(row=1, column=0, padx=10, pady=10)

    # All
    header_frame.pack(padx=10, pady=10, fill="x")
    board_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
    controls_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)


def main():
    homepage()
    root.mainloop()


if __name__ == "__main__":
    main()
