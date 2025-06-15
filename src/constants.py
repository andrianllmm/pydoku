import os
import customtkinter as ctk


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Styles ---
THEME_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "assets", "custom_theme.json")
)
ctk.set_default_color_theme(THEME_PATH)
ctk.set_appearance_mode("light")

BASE = 3  # Base size of the Sudoku grid (3x3 sub-grids)
SIZE = BASE**2  # Total size of the grid (9x9)
CELL_SIZE = 50  # Size of each cell in pixels
WIDTH = CELL_SIZE * 20  # Window width
HEIGHT = WIDTH // 16 * 9  # Window height (16:9 aspect ratio)
TITLE = "Pydoku"  # App title

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

# Center and set window size
window_width = root.winfo_screenwidth()
window_heigth = root.winfo_screenheight()
root.geometry(
    f"{WIDTH}x{HEIGHT}+{(window_width - WIDTH) // 2}+{(window_heigth - HEIGHT) // 2}"
)
root.minsize(WIDTH, HEIGHT)
