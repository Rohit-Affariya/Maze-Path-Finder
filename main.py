from maze import load_maze, display_maze
from visualizer import visualize_maze
from solvers import (
    bfs,
    dfs,
    astar,
    bidirectional_bfs,
    dijkstra,
    bellman_ford
)


ALGORITHMS = {
    "1": ("Breadth-First Search (BFS)", bfs),
    "2": ("Depth-First Search (DFS)", dfs),
    "3": ("A* Search", astar),
    "4": ("Bidirectional BFS", bidirectional_bfs),
    "5": ("Dijkstra", dijkstra),
    "6": ("Bellman-Ford", bellman_ford)
}


def print_result(
    algorithm,
    path,
    visited,
    execution_time
):
    """
    Display results for one algorithm.
    """

    print("\n" + "=" * 60)
    print(f"{algorithm} RESULT")
    print("=" * 60)

    if path:

        print("Path found      : Yes")
        print("Path length     :", len(path))

    else:

        print("Path found      : No")
        print("Path length     : 0")

    print("Nodes visited   :", len(visited))

    print(
        f"Execution time  : "
        f"{execution_time:.6f} seconds"
    )

    print("=" * 60)


def run_algorithm(
    maze,
    start,
    end,
    algorithm_name,
    algorithm
):
    """
    Run one selected algorithm.
    """

    print(
        f"\nRunning {algorithm_name}..."
    )

    path, visited, execution_time = algorithm(
        maze,
        start,
        end
    )

    print_result(
        algorithm_name,
        path,
        visited,
        execution_time
    )

    visualize_maze(
        maze,
        start,
        end,
        path,
        visited,
        f"{algorithm_name} - Maze Visualization"
    )

    return path, visited, execution_time


def compare_all_algorithms(
    maze,
    start,
    end
):
    """
    Run all available algorithms and compare them.

    The shortest path is selected based on
    path length.

    If multiple algorithms produce the same
    shortest path, the one with fewer visited
    nodes is preferred.
    """

    results = []

    print("\n" + "=" * 90)
    print("                 ALL ALGORITHM COMPARISON")
    print("=" * 90)

    for number, (
        name,
        algorithm
    ) in ALGORITHMS.items():

        print(
            f"\nRunning {name}..."
        )

        path, visited, execution_time = algorithm(
            maze,
            start,
            end
        )

        result = {
            "algorithm": name,
            "path": path,
            "visited": visited,
            "path_length": len(path) if path else 0,
            "nodes_visited": len(visited),
            "execution_time": execution_time,
            "found": bool(path)
        }

        results.append(result)

    # --------------------------------------------------------
    # Display comparison table
    # --------------------------------------------------------

    print("\n")
    print(
        f"{'Algorithm':<30}"
        f"{'Path':<12}"
        f"{'Nodes':<15}"
        f"{'Time (sec)':<15}"
    )

    print("-" * 90)

    for result in results:

        path_value = (
            result["path_length"]
            if result["found"]
            else "No path"
        )

        print(
            f"{result['algorithm']:<30}"
            f"{str(path_value):<12}"
            f"{result['nodes_visited']:<15}"
            f"{result['execution_time']:<15.6f}"
        )

    print("-" * 90)

    successful = [
        result
        for result in results
        if result["found"]
    ]

    if not successful:

        print("\nNo algorithm found a path.")

        return

    # --------------------------------------------------------
    # Find shortest path
    # --------------------------------------------------------

    shortest_path = min(
        result["path_length"]
        for result in successful
    )

    shortest_results = [
        result
        for result in successful
        if result["path_length"] == shortest_path
    ]

    # Among algorithms producing the shortest path,
    # select the one exploring the fewest nodes.
    best_algorithm = min(
        shortest_results,
        key=lambda result: (
            result["nodes_visited"],
            result["execution_time"]
        )
    )

    print("\nBEST RESULT")
    print("-" * 60)

    print(
        "Shortest path length :",
        shortest_path
    )

    print(
        "Recommended algorithm:",
        best_algorithm["algorithm"]
    )

    print(
        "Nodes visited        :",
        best_algorithm["nodes_visited"]
    )

    print(
        f"Execution time       : "
        f"{best_algorithm['execution_time']:.6f} seconds"
    )

    print("\nNote:")
    print(
        "The recommended algorithm is selected "
        "from the algorithms that found the shortest "
        "path, using fewer visited nodes as the "
        "primary tie-breaker."
    )

    visualize_maze(
        maze,
        start,
        end,
        best_algorithm["path"],
        best_algorithm["visited"],
        f"{best_algorithm['algorithm']} - Best Result"
    )


def main():

    print("\n" + "=" * 65)
    print("          MAZE PATHFINDING - DAA PROJECT")
    print("          SHORTEST PATH ALGORITHM STUDY")
    print("=" * 65)

    maze_file = input(
        "\nEnter maze file path "
        "[sample_mazes/maze_01.txt]: "
    ).strip()

    if not maze_file:

        maze_file = (
            "sample_mazes/maze_01.txt"
        )

    try:

        maze, start, end = load_maze(
            maze_file
        )

    except FileNotFoundError:

        print(
            "\nError: Maze file not found."
        )

        return

    except ValueError as error:

        print(
            "\nError:",
            error
        )

        return

    print("\nMaze loaded successfully.")

    print("Start       :", start)
    print("Destination :", end)
    print("Rows        :", len(maze))
    print("Columns     :", len(maze[0]))

    while True:

        print("\n" + "-" * 65)
        print("SELECT OPTION")
        print("-" * 65)

        print("1. Breadth-First Search (BFS)")
        print("2. Depth-First Search (DFS)")
        print("3. A* Search")
        print("4. Bidirectional BFS")
        print("5. Dijkstra")
        print("6. Bellman-Ford")
        print("7. Compare All Algorithms")
        print("8. Display Maze")
        print("9. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if choice == "9":

            print(
                "\nExiting program..."
            )

            break

        # ----------------------------------------------------
        # Display maze
        # ----------------------------------------------------

        if choice == "8":

            display_maze(
                maze,
                start,
                end
            )

            continue

        # ----------------------------------------------------
        # Compare all
        # ----------------------------------------------------

        if choice == "7":

            compare_all_algorithms(
                maze,
                start,
                end
            )

            continue

        # ----------------------------------------------------
        # Individual algorithm
        # ----------------------------------------------------

        if choice in ALGORITHMS:

            name, algorithm = ALGORITHMS[
                choice
            ]

            run_algorithm(
                maze,
                start,
                end,
                name,
                algorithm
            )

            continue

        print(
            "\nInvalid choice."
            " Please select 1-9."
        )


if __name__ == "__main__":
    main()