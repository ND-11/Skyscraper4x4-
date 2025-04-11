Skyscraper Puzzle Solver
========================

What is this?
------------
A web app that solves 4x4 Skyscraper puzzles. Enter clues around the edges and it will fill in the correct building heights (1-4) in the grid.

How to use:
-----------
1. Run the server:
   python app.py

2. Open in browser:
   http://localhost:5000

3. Enter numbers (1-4) in the edge boxes
4. Click "Solve Puzzle" to see the answer
5. Click "Reset Puzzle" to start over

Files included:
---------------
- app.py       (backend server)
- index.html   (web page)
- style.css    (styling)
- buildings.py (console version)

Requirements:
-------------
- Python 3
- Flask (install with: pip install flask flask-cors)

Console version:
python buildings.py

Demo: https://njood.pythonanywhere.com/

Tip: Smaller numbers mean fewer tall buildings are visible from that side!