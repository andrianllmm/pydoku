import time
from PIL import Image

from constants import *
import model


def create_board_widget(master, board, selected):
    """Create a widget displaying the Sudoku board."""

    # Event handler when cell is clicked (selected)
    def on_select(r, c):
        model.select_index(selected, r, c),
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
                    r, c = k + i, l + j  # Global index
                    value = board[r][c]
                    modifiable = isinstance(value, ctk.StringVar)

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
    board_copy = model.get_board_copy(board)
    r, c = model.get_selected_index(selected)

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
        model.write_number(n, index, board)
        if model.is_board_solved(board):
            running.set(False)
            show_endgame_modal(root)

    frame = ctk.CTkFrame(master, fg_color="transparent")

    # Create buttons from 1-9
    for i in range(1, SIZE + 1):
        btn = ctk.CTkButton(
            frame,
            text=str(i),
            font=("", 28),
            command=lambda n=i: on_write(n, model.get_selected_index(selected), board),
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

    icon = ctk.CTkImage(Image.open("../assets/icons/erase.png"), size=(45, 40))
    btn = ctk.CTkButton(
        frame,
        text="",
        image=icon,
        width=CELL_SIZE * 1.5,
        corner_radius=100,
        command=lambda: model.erase_number(model.get_selected_index(selected), board),
    )
    btn.pack(padx=5, pady=5, ipadx=10, ipady=10)

    label = ctk.CTkLabel(frame, text="Erase", text_color=PALETTE["primary"])
    label.pack()

    return frame


def create_check_btn(master, board):
    """Create a button to check if the board is solved."""
    frame = ctk.CTkFrame(master)

    icon = ctk.CTkImage(Image.open("../assets/icons/check.png"), size=(40, 40))
    btn = ctk.CTkButton(
        frame,
        text="",
        image=icon,
        width=CELL_SIZE * 1.5,
        corner_radius=100,
        command=lambda: show_message(
            root,
            "Correct!" if model.is_board_solved(board) else "Incorrect!",
            type="success" if model.is_board_solved(board) else "error",
        ),
    )
    btn.pack(padx=5, pady=5, ipadx=10, ipady=10)

    label = ctk.CTkLabel(frame, text="Check", text_color=PALETTE["primary"])
    label.pack()

    return frame


def create_hint_btn(master, hints_left, board, solved_board, selected):
    """Create a button to show hint."""
    frame = ctk.CTkFrame(master)

    icon = ctk.CTkImage(Image.open("../assets/icons/lightbulb.png"), size=(30, 40))
    btn = ctk.CTkButton(
        frame,
        text="",
        image=icon,
        width=CELL_SIZE * 1.5,
        corner_radius=100,
        command=lambda: model.show_hint(
            hints_left, board, solved_board, model.get_selected_index(selected)
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
    board = model.generate_board(difficulty)
    solved_board = model.solve_board(model.get_board_copy(board))
    selected = (
        ctk.IntVar(root, value=-1),
        ctk.IntVar(root, value=-1),
    )
    running = ctk.BooleanVar(root, value=True)
    hints_left = ctk.IntVar(root, value=3)

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
