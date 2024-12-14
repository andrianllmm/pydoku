# CMSC11 Final Project: Sudoku

This project is a Python-based Sudoku game built using the **Tkinter** library.

## Getting Started

These instructions will help you set up the project on your local machine for development or testing purposes.

### Prerequisites

- **Python 3.x**
- **CustomTkinter** (for the GUI)
- **pytest** (for running tests)
- **black** (for code formatting)

## Installation

### Step 1: Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/andrianllmm/CMSC11-Final-Project.git
cd CMSC11-Final-Project
```

### Step 2: Create a Virtual Environment
You can use a virtual environment to manage dependencies by running:

```bash
# For Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# For Windows:
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Dependencies
You can install the required dependencies by running:

```bash
pip install -r requirements.txt
```

## Running the App
Once you've cloned the repository and installed the dependencies, you can run the app by running:

```bash
python app.py
```

## Directory Structure

```
CMSC11-Final-Project/
│
├── app.py             # Main file
├── test.py            # Test cases
├── requirements.txt   # List of dependencies
└── assets/            # Any image files or resources for the app (e.g., icons, fonts)
```


## Testing
To run tests for this project, we use `pytest`. You can run the tests by running:

```bash
pytest test.py
```

---

Happy coding! 🎮