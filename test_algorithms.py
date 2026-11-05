
from maze import load_maze
from solvers import (
    bfs,
    dfs,
    astar,
    bidirectional_bfs,
    dijkstra,
    bellman_ford
)


def validate_path(maze, start, end, path):
    """
    Check whether a returned path is valid.
    """

    if not path:
        return False, "No path returned"

    if path[0] != start:
        return False, "Path does not start at S"

    if path[-1] != end:
        return False, "Path does not end at D"

    rows = len(maze)
    cols = len(maze[0])

    for row, col in path:

        if not (0 <= row < rows and 0 <= col < cols):
            return False, "Path contains an out-of-bounds cell"

        if maze[row][col] == "#":
            return False, "Path passes through a wall"

    for i in range(len(path) - 1):

        r1, c1 = path[i]
        r2, c2 = path[i + 1]

        distance = abs(r1 - r2) + abs(c1 - c2)

        if distance != 1:
            return False, "Path contains an invalid move"

    return True, "Valid path"


def run_tests(maze_file):
    """
    Test all six algorithms for path validity
    and shortest-path correctness.
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

    results = {}

    print("\n" + "=" * 75)
    print("              MAZE ALGORITHM CORRECTNESS TEST")
    print("=" * 75)

    print(f"Maze       : {maze_file}")
    print(f"Start      : {start}")
    print(f"Destination: {end}")

    print("-" * 75)

    for name, algorithm in algorithms.items():

        path, visited, execution_time = algorithm(
            maze,
            start,
            end
        )

        valid, message = validate_path(
            maze,
            start,
            end,
            path
        )

        path_length = len(path) if path else 0

        results[name] = {
            "path": path,
            "valid": valid,
            "path_length": path_length,
            "nodes_visited": len(visited)
        }

        status = "PASS" if valid else "FAIL"

        print(
            f"{name:<22}"
            f"{status:<10}"
            f"{path_length:<15}"
            f"{len(visited):<15}"
        )

        if not valid:
            print(f"  Reason: {message}")

    print("-" * 75)

    # Check shortest-path algorithms against BFS
    reference_length = results["BFS"]["path_length"]

    shortest_algorithms = [
        "A*",
        "Bidirectional BFS",
        "Dijkstra",
        "Bellman-Ford"
    ]

    print("\nSHORTEST-PATH COMPARISON")
    print("-" * 55)

    for name in shortest_algorithms:

        result = results[name]

        if not result["valid"]:
            print(f"{name:<22} FAIL - Invalid path")

        elif result["path_length"] == reference_length:
            print(f"{name:<22} PASS - Optimal path")

        else:
            print(
                f"{name:<22} FAIL - "
                f"Expected {reference_length}, "
                f"got {result['path_length']}"
            )

    # Final test summary
    all_valid = all(
        result["valid"]
        for result in results.values()
    )

    all_optimal = all(
        results[name]["valid"]
        and results[name]["path_length"] == reference_length
        for name in shortest_algorithms
    )

    print("\nFINAL TEST SUMMARY")
    print("-" * 55)

    print(
        f"Path validation : "
        f"{'PASS' if all_valid else 'FAIL'}"
    )

    print(
        f"Shortest paths  : "
        f"{'PASS' if all_optimal else 'FAIL'}"
    )

    if all_valid and all_optimal:
        print("\nAll correctness tests passed!")

    else:
        print("\nSome tests failed. Review the results above.")


def main():

    print("\nMAZE PATHFINDING - ALGORITHM TESTING")

    maze_file = input(
        "Enter maze file path "
        "[sample_mazes/maze_01.txt]: "
    ).strip()

    if not maze_file:
        maze_file = "sample_mazes/maze_01.txt"

    try:
        run_tests(maze_file)

    except FileNotFoundError:
        print("\nError: Maze file not found.")

    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
