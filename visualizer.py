
import matplotlib.pyplot as plt


def visualize_maze(
    maze,
    start,
    end,
    path=None,
    visited=None,
    title="Maze"
):
    """Display the maze, explored nodes and final path."""

    rows = len(maze)
    cols = len(maze[0])

    grid = []

    for row in range(rows):
        grid_row = []

        for col in range(cols):
            if maze[row][col] == "#":
                grid_row.append(1)
            else:
                grid_row.append(0)

        grid.append(grid_row)

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.imshow(
        grid,
        cmap="gray_r",
        origin="upper"
    )

    # Display visited nodes
    if visited:
        visited_rows = []
        visited_cols = []

        for row, col in visited:
            if (row, col) != start and (row, col) != end:
                visited_rows.append(row)
                visited_cols.append(col)

        ax.scatter(
            visited_cols,
            visited_rows,
            marker=".",
            s=35,
            label="Visited Nodes"
        )

    # Display solution path
    if path:
        path_rows = [cell[0] for cell in path]
        path_cols = [cell[1] for cell in path]

        ax.plot(
            path_cols,
            path_rows,
            linewidth=3,
            label="Solution Path"
        )

    # Display start and destination
    ax.scatter(
        start[1],
        start[0],
        marker="o",
        s=120,
        label="Start"
    )

    ax.scatter(
        end[1],
        end[0],
        marker="X",
        s=120,
        label="Destination"
    )

    ax.set_title(title)
    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    ax.grid(
        True,
        linewidth=0.5,
        alpha=0.3
    )

    ax.legend()
    plt.tight_layout()

    # Keep the window open until the user closes it
    plt.show()


def visualize_path(
    maze,
    start,
    end,
    path,
    title="Solution Path"
):
    """Display only the final solution path."""

    visualize_maze(
        maze=maze,
        start=start,
        end=end,
        path=path,
        visited=None,
        title=title
    )


def visualize_search(
    maze,
    start,
    end,
    visited,
    path,
    algorithm="BFS"
):
    """Display the search process and final path."""

    title = f"{algorithm} - Maze Search"

    visualize_maze(
        maze=maze,
        start=start,
        end=end,
        path=path,
        visited=visited,
        title=title
    )
