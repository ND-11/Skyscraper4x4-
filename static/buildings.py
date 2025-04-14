# Skyscraper Puzzle Solver
# This program solves a 4x4 skyscraper puzzle where the user provides clues for the visibility of buildings from each side.
# The program uses backtracking to find all valid arrangements of buildings.
# This is the raw implementation without any web framework or GUI.
# It can be run in a console or terminal.
# Updated to match the functionality of app.py (finds all solutions)

from typing import List, Dict, Tuple


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


def get_yes_no_input(prompt: str) -> bool:
    """Get yes/no input from the user."""
    while True:
        response = input(prompt).strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        else:
            print("Please enter 'y' or 'n'.")


def count_visible(buildings: List[int]) -> int:
    """Count the number of visible buildings from a given perspective."""
    max_height = 0
    visible = 0
    for height in buildings:
        if height > max_height:
            visible += 1
            max_height = height
    return visible


def is_valid(grid: List[List[int]], row: int, col: int, num: int,
             clues: Dict[str, List[int]]) -> bool:
    """Check if placing a number in the grid is valid."""
    if num in grid[row] or num in [grid[i][col] for i in range(4)]:
        return False

    grid[row][col] = num

    if all(grid[row]):
        left, right = clues['left'][row], clues['right'][row]
        if left and count_visible(grid[row]) != left:
            grid[row][col] = 0
            return False
        if right and count_visible(grid[row][::-1]) != right:
            grid[row][col] = 0
            return False

    col_vals = [grid[r][col] for r in range(4)]
    if all(col_vals):
        top, bottom = clues['top'][col], clues['bottom'][col]
        if top and count_visible(col_vals) != top:
            grid[row][col] = 0
            return False
        if bottom and count_visible(col_vals[::-1]) != bottom:
            grid[row][col] = 0
            return False

    grid[row][col] = 0
    return True


def solve_all(grid: List[List[int]], clues: Dict[str, List[int]],
              row: int = 0, col: int = 0, solutions: List[List[List[int]]] = None) -> List[List[List[int]]]:
    """Find all solutions to the skyscraper puzzle using backtracking."""
    if solutions is None:
        solutions = []

    if row == 4:
        # Make a deep copy of the grid to store as a solution
        solutions.append([row[:] for row in grid])
        return solutions

    next_row, next_col = (row, col + 1) if col < 3 else (row + 1, 0)

    for num in range(1, 5):
        if is_valid(grid, row, col, num, clues):
            grid[row][col] = num
            solutions = solve_all(grid, clues, next_row, next_col, solutions)
            grid[row][col] = 0

    return solutions


def main():
    """Main function to run the skyscraper solver."""
    # Initialize the grid
    grid = [[0 for _ in range(4)] for _ in range(4)]

    # Get clues from the user
    print("Enter clues (0 if no clue):")
    clues = {
        'top': [get_clue_input(f"Enter top clue for column {i+1}: ") for i in range(4)],
        'bottom': [get_clue_input(f"Enter bottom clue for column {i+1}: ") for i in range(4)],
        'left': [get_clue_input(f"Enter left clue for row {i+1}: ") for i in range(4)],
        'right': [get_clue_input(f"Enter right clue for row {i+1}: ") for i in range(4)]
    }

    # Solve the puzzle and find all solutions
    solutions = solve_all(grid, clues)

    # Display results
    if not solutions:
        print("\nNo solution exists.")
    elif len(solutions) == 1:
        print("\nUnique solution found:")
        for row in solutions[0]:
            print(" ".join(map(str, row)))
    else:
        print(f"\nFound {len(solutions)} possible solutions.")
        if get_yes_no_input("Would you like to print all solutions? (y/n): "):
            print("\nAll solutions:")
            for i, solution in enumerate(solutions, 1):
                print(f"\nSolution {i}:")
                for row in solution:
                    print(" ".join(map(str, row)))
        else:
            print("\nFirst solution:")
            for row in solutions[0]:
                print(" ".join(map(str, row)))


if __name__ == "__main__":
    main()
