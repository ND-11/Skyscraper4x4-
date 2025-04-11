# Skyscraper Puzzle Solver
# This program solves a 4x4 skyscraper puzzle where the user provides clues for the visibility of buildings from each side.
# The program uses backtracking to find a valid arrangement of buildings.
# This is the raw implementation without any web framework or GUI.
# It can be run in a console or terminal.
# This version is the same as buildings.py it's just a copy of it for downloading purpose.

from typing import List, Dict


def get_clue_input(prompt: str) -> int:
    """Get a single clue input from the user."""
    while True:
        try:
            value = int(input(prompt))
            if 0 <= value <= 4:
                return value
            else:
                print("Please enter a number between 0 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 4.")


def count_visible(buildings: List[int]) -> int:
    """Count the number of visible buildings from a given perspective."""
    max_height = 0
    visible = 0
    for height in buildings:
        if height > max_height:
            visible += 1
            max_height = height
    return visible


def is_valid(grid: List[List[int]], row: int, col: int, num: int, clues: Dict[str, List[int]]) -> bool:
    """Check if placing a number in the grid is valid."""
    # Check uniqueness in row and column
    if num in grid[row] or num in [grid[i][col] for i in range(4)]:
        return False

    # Temporarily place the number
    grid[row][col] = num

    # Check row visibility if completed
    if all(grid[row]):
        left, right = clues['left'][row], clues['right'][row]
        if left and count_visible(grid[row]) != left:
            grid[row][col] = 0
            return False
        if right and count_visible(grid[row][::-1]) != right:
            grid[row][col] = 0
            return False

    # Check column visibility if completed
    col_vals = [grid[r][col] for r in range(4)]
    if all(col_vals):
        top, bottom = clues['top'][col], clues['bottom'][col]
        if top and count_visible(col_vals) != top:
            grid[row][col] = 0
            return False
        if bottom and count_visible(col_vals[::-1]) != bottom:
            grid[row][col] = 0
            return False

    # Restore and approve
    grid[row][col] = 0
    return True


def solve(grid: List[List[int]], clues: Dict[str, List[int]], row: int = 0, col: int = 0) -> bool:
    """Solve the skyscraper puzzle using backtracking."""
    if row == 4:  # If we've filled all rows
        return True

    next_row, next_col = (row, col + 1) if col < 3 else (row + 1, 0)

    for num in range(1, 5):  # Numbers 1 to 4
        if is_valid(grid, row, col, num, clues):
            grid[row][col] = num
            if solve(grid, clues, next_row, next_col):
                return True
            grid[row][col] = 0  # Backtrack

    return False  # No solution found


def main():
    """Main function to run the skyscraper solver."""
    # Initialize the grid
    grid = [[0 for _ in range(4)] for _ in range(4)]

    # Get clues from the user
    clues = {
        'top': [get_clue_input(f"Enter top clue for column {i}: ") for i in range(4)],
        'bottom': [get_clue_input(f"Enter bottom clue for column {i}: ") for i in range(4)],
        'left': [get_clue_input(f"Enter left clue for row {i}: ") for i in range(4)],
        'right': [get_clue_input(f"Enter right clue for row {i}: ") for i in range(4)]
    }

    # Solve the puzzle
    if solve(grid, clues):
        print("Solution:")
        for row in grid:
            print(" ".join(map(str, row)))
    else:
        print("No solution exists.")


if __name__ == "__main__":
    main()
