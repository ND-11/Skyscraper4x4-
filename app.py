from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from typing import List, Dict

app = Flask(__name__)
CORS(app)

app = Flask(__name__, static_folder='static')


def count_visible(buildings: List[int]) -> int:
    max_height = 0
    visible = 0
    for height in buildings:
        if height > max_height:
            visible += 1
            max_height = height
    return visible


def is_valid(grid: List[List[int]], row: int, col: int, num: int,
             clues: Dict[str, List[int]]) -> bool:
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


def solve(grid: List[List[int]], clues: Dict[str, List[int]],
          row: int = 0, col: int = 0) -> bool:
    if row == 4:
        return True

    next_row, next_col = (row, col + 1) if col < 3 else (row + 1, 0)

    for num in range(1, 5):
        if is_valid(grid, row, col, num, clues):
            grid[row][col] = num
            if solve(grid, clues, next_row, next_col):
                return True
            grid[row][col] = 0

    return False


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/solve', methods=['POST'])
def solve_puzzle():
    try:
        data = request.json
        clues = {
            'top': [int(data.get('top', [0, 0, 0, 0])[i]) for i in range(4)],
            'bottom': [int(data.get('bottom', [0, 0, 0, 0])[i]) for i in range(4)],
            'left': [int(data.get('left', [0, 0, 0, 0])[i]) for i in range(4)],
            'right': [int(data.get('right', [0, 0, 0, 0])[i]) for i in range(4)]
        }

        grid = [[0 for _ in range(4)] for _ in range(4)]

        if solve(grid, clues):
            return jsonify({'status': 'success', 'solution': grid})
        return jsonify({'status': 'error', 'message': 'No solution exists'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
