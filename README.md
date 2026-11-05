# DAA Maze Path Finder

A Python-based maze pathfinding project developed for **Design and Analysis of Algorithms (DAA)**. It implements and compares six graph-search algorithms to find a route from a start cell to a destination in a grid maze.

The program can run one algorithm at a time, compare all six algorithms, display the explored cells and solution path, and record benchmark measurements.

## Features

- Loads mazes from plain-text (`.txt`) files.
- Supports six pathfinding algorithms:
  1. Breadth-First Search (BFS)
  2. Depth-First Search (DFS)
  3. A* Search
  4. Bidirectional BFS
  5. Dijkstra's Algorithm
  6. Bellman-Ford Algorithm
- Displays the maze, explored cells, start, destination, and resulting path using Matplotlib.
- Compares path length, number of visited nodes, and execution time.
- Includes sample mazes and a path-validation test script.
- Saves benchmark results in CSV format.

## Algorithms

| Algorithm | Search approach | Finds a shortest path in this project? |
|---|---|---|
| BFS | Explores the maze level by level using a queue | Yes, for equal-cost moves |
| DFS | Explores one branch deeply before backtracking | Not guaranteed |
| A* | Uses path cost and Manhattan-distance heuristic | Yes, with the implemented unit-cost grid and admissible heuristic |
| Bidirectional BFS | Searches from the start and destination | Yes, for equal-cost moves |
| Dijkstra | Expands the lowest-cost known position first | Yes, for non-negative movement costs |
| Bellman-Ford | Repeatedly relaxes graph edges | Yes, for this graph with unit, non-negative edge weights |

All legal moves currently have a cost of 1, and movement is allowed horizontally or vertically (not diagonally). Therefore, shortest-path comparisons are made using the number of cells in the returned path. DFS is included for comparison and may return a longer route.

## Project Structure

```text
Maze-Pathfinding-DAA/
├── main.py                 # Interactive menu and algorithm execution
├── maze.py                 # Maze loading, validation, and grid helpers
├── solvers.py              # Implementations of the six algorithms
├── visualizer.py           # Matplotlib maze and path visualizations
├── benchmark.py            # Runs and compares algorithm benchmarks
├── test_algorithms.py      # Validates paths and shortest-path results
├── requirements.txt        # Python dependencies
├── sample_mazes/
│   ├── maze_01.txt
│   ├── maze_easy.txt
│   ├── maze_medium.txt
│   └── maze_hard.txt
└── results/
    └── results.csv         # Recorded benchmark results
```

## Requirements

- Python 3.8 or later
- Matplotlib

Install the required package from the project directory:

```bash
python -m pip install -r requirements.txt
```

## How to Run

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Install the dependencies.
4. Start the main program:

```bash
python main.py
```

When prompted for a maze file, enter a path such as:

```text
sample_mazes/maze_01.txt
```

You can also press **Enter** to use the default maze, `sample_mazes/maze_01.txt`.

### Main Menu

| Option | Action |
|---|---|
| 1 | Run BFS |
| 2 | Run DFS |
| 3 | Run A* Search |
| 4 | Run Bidirectional BFS |
| 5 | Run Dijkstra |
| 6 | Run Bellman-Ford |
| 7 | Compare all algorithms |
| 8 | Display the maze |
| 9 | Exit |

The visualization window displays the maze and, when an algorithm is run, the explored cells and resulting path. Close the Matplotlib window to return to the terminal menu.

## Maze File Format

Each maze is a rectangular grid containing these characters:

| Symbol | Meaning |
|---|---|
| `#` | Wall (blocked cell) |
| `.` | Open cell |
| `S` | Starting position |
| `D` | Destination |

Example:

```text
#########
#S..#...#
#.#...#.#
#...#...#
###.#.#D#
#.......#
#########
```

Maze files must:
- Have the same number of characters in every row.
- Contain exactly one `S` and one `D`.
- Use only `#`, `.`, `S`, and `D`.

To try another maze, enter its file path when the program asks for one.

## Run Correctness Tests

Run the path-validation and shortest-path comparison tests with:

```bash
python test_algorithms.py
```

The test script checks that returned paths:
- Start at `S` and end at `D`.
- Stay inside the maze and do not cross walls.
- Move one cell at a time in a valid horizontal or vertical direction.
- Match BFS's path length for the algorithms expected to return an optimal path.

## Run Benchmarks

Run the benchmark program:

```bash
python benchmark.py
```

Enter a maze file path when prompted, or press **Enter** for the default maze.

The benchmark compares:
- Whether a path was found.
- Path length (number of cells in the returned path).
- Number of visited nodes.
- Measured execution time.

Results are appended to:

```text
results/results.csv
```

Execution time can vary between runs and computers. For a fair comparison, run the same maze and environment multiple times; do not treat a single timing result as a universal ranking of the algorithms.

## Current Sample Result

The repository includes recorded results for `maze_01.txt` (a 7 × 9 maze). In the recorded runs, BFS, A*, Bidirectional BFS, Dijkstra, and Bellman-Ford returned a path length of 15 cells, while DFS returned 19 cells.

These are sample measurements from the included CSV file, not guaranteed results for every maze or computer.

## Learning Outcomes

This project demonstrates:
- How a maze can be represented as a graph.
- How graph traversal and shortest-path algorithms work.
- The difference between finding a path and finding an optimal path.
- How visited-node counts and execution time can be used to compare algorithms.
- How to validate algorithm output through testing.

## Limitations

- The current implementation uses equal movement cost (1) for every valid move.
- Only four-directional movement is supported; diagonal movement is not included.
- The project is a command-line Python application with Matplotlib visualization.
- Performance measurements depend on maze size, maze layout, hardware, and runtime conditions.

## Technologies Used

- Python
- Matplotlib
- CSV (Python standard library)

## Author

**Rohit**

## Academic Context

Developed as an academic project for the **Design and Analysis of Algorithms (DAA)** subject.
