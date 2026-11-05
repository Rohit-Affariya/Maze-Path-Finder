
import csv
import os

from maze import load_maze
from solvers import (
    bfs,
    dfs,
    astar,
    bidirectional_bfs,
    dijkstra,
    bellman_ford
)


def run_benchmark(maze_file):
    """
    Run all six pathfinding algorithms on the same maze.
    """

    maze, start, end = load_maze(maze_file)

    algorithms = {
        "BFS": bfs,
        "DFS": dfs,
        "A*": astar,
        "Bidirectional BFS": bidirectional_bfs,
        "Dijkstra": dijkstra,
        "Bellman-Ford": bellman_ford
    }

    results = []

    print("\n" + "=" * 85)
    print("                         ALGORITHM BENCHMARK")
    print("=" * 85)

    print(f"Maze file  : {maze_file}")
    print(f"Start      : {start}")
    print(f"Destination: {end}")
    print(f"Maze size  : {len(maze)} x {len(maze[0])}")

    print("=" * 85)

    for name, algorithm in algorithms.items():

        print(f"\nRunning {name}...")

        path, visited, execution_time = algorithm(
            maze,
            start,
            end
        )

        nodes_visited = len(visited)

        if path:
            path_length = len(path)
            path_found = "Yes"
        else:
            path_length = 0
            path_found = "No"

        result = {
            "maze": os.path.basename(maze_file),
            "algorithm": name,
            "rows": len(maze),
            "columns": len(maze[0]),
            "path_found": path_found,
            "path_length": path_length,
            "nodes_visited": nodes_visited,
            "execution_time": execution_time
        }

        results.append(result)

        print(f"Path found     : {path_found}")
        print(f"Path length    : {path_length} cells")
        print(f"Nodes visited  : {nodes_visited}")
        print(f"Execution time : {execution_time:.6f} seconds")

    return results


def save_results(results, filename="results/results.csv"):
    """
    Save benchmark results to a CSV file.
    """

    if not results:
        print("\nNo results to save.")
        return

    directory = os.path.dirname(filename)

    if directory:
        os.makedirs(directory, exist_ok=True)

    fieldnames = [
        "maze",
        "algorithm",
        "rows",
        "columns",
        "path_found",
        "path_length",
        "nodes_visited",
        "execution_time"
    ]

    file_exists = (
        os.path.exists(filename)
        and os.path.getsize(filename) > 0
    )

    with open(filename, "a", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        if not file_exists:
            writer.writeheader()

        writer.writerows(results)

    print(f"\nResults saved to: {filename}")


def display_comparison(results):
    """
    Display a comparison table of all algorithms.
    """

    print("\n")
    print("=" * 85)
    print("                         ALGORITHM COMPARISON")
    print("=" * 85)

    print(
        f"{'Algorithm':<22}"
        f"{'Path Length':<16}"
        f"{'Nodes Visited':<18}"
        f"{'Time (sec)':<15}"
    )

    print("-" * 85)

    for result in results:

        print(
            f"{result['algorithm']:<22}"
            f"{result['path_length']:<16}"
            f"{result['nodes_visited']:<18}"
            f"{result['execution_time']:<15.6f}"
        )

    print("=" * 85)


def compare_algorithms(results):
    """
    Display observations based on benchmark results.
    """

    if not results:
        return

    successful_results = [
        result
        for result in results
        if result["path_found"] == "Yes"
    ]

    if not successful_results:
        print("\nNo algorithm found a path.")
        return

    shortest_path = min(
        successful_results,
        key=lambda result: result["path_length"]
    )

    fewest_nodes = min(
        successful_results,
        key=lambda result: result["nodes_visited"]
    )

    fastest = min(
        successful_results,
        key=lambda result: result["execution_time"]
    )

    print("\nDAA OBSERVATIONS")
    print("-" * 55)

    print(
        f"Shortest path : {shortest_path['algorithm']} "
        f"({shortest_path['path_length']} cells)"
    )

    print(
        f"Fewest nodes  : {fewest_nodes['algorithm']} "
        f"({fewest_nodes['nodes_visited']} nodes)"
    )

    print(
        f"Fastest       : {fastest['algorithm']} "
        f"({fastest['execution_time']:.6f} seconds)"
    )


def main():
    """
    Main function for benchmark.py.
    """

    print("\n" + "=" * 70)
    print("             MAZE ALGORITHM BENCHMARK")
    print("                    DAA PROJECT")
    print("=" * 70)

    maze_file = input(
        "\nEnter maze file path "
        "[sample_mazes/maze_01.txt]: "
    ).strip()

    if not maze_file:
        maze_file = "sample_mazes/maze_01.txt"

    try:

        results = run_benchmark(maze_file)

        display_comparison(results)

        compare_algorithms(results)

        save_results(results)

    except FileNotFoundError:

        print("\nError: Maze file not found.")

    except ValueError as error:

        print(f"\nError: {error}")

    except ImportError as error:

        print(f"\nImport error: {error}")


if __name__ == "__main__":
    main()
