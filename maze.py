def load_maze(filename):
    """
    Load a maze from a text file.

    Symbols:
        # = Wall
        . = Open cell
        S = Start
        D = Destination

    Returns:
        maze  - 2D list representing the maze
        start - (row, column)
        end   - (row, column)
    """

    with open(filename, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    if not lines:
        raise ValueError("Maze file is empty.")

    # Check that all rows have the same length
    width = len(lines[0])

    for line in lines:
        if len(line) != width:
            raise ValueError("Invalid maze: all rows must have the same length.")

    maze = []
    start = None
    end = None

    for row in range(len(lines)):
        maze_row = []

        for col in range(width):
            cell = lines[row][col]

            # Check valid symbols
            if cell not in {"#", ".", "S", "D"}:
                raise ValueError(
                    f"Invalid character '{cell}' at position ({row}, {col})."
                )

            # Find start position
            if cell == "S":
                if start is not None:
                    raise ValueError("Maze contains more than one start position.")

                start = (row, col)

            # Find destination position
            if cell == "D":
                if end is not None:
                    raise ValueError(
                        "Maze contains more than one destination."
                    )

                end = (row, col)

            maze_row.append(cell)

        maze.append(maze_row)

    # Make sure start and destination exist
    if start is None:
        raise ValueError("Maze does not contain a start position 'S'.")

    if end is None:
        raise ValueError("Maze does not contain a destination 'D'.")

    return maze, start, end


def is_valid_cell(maze, row, col):
    """
    Check whether a cell is inside the maze and is not a wall.
    """

    rows = len(maze)
    cols = len(maze[0])

    if row < 0 or row >= rows:
        return False

    if col < 0 or col >= cols:
        return False

    return maze[row][col] != "#"


def get_neighbors(maze, row, col):
    """
    Return all walkable neighboring cells.

    Movement is allowed in four directions:
        Up
        Down
        Left
        Right
    """

    directions = [
        (-1, 0),   # Up
        (1, 0),    # Down
        (0, -1),   # Left
        (0, 1)     # Right
    ]

    neighbors = []

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        if is_valid_cell(maze, new_row, new_col):
            neighbors.append((new_row, new_col))

    return neighbors


def display_maze(maze, start=None, end=None):
    """
    Display the maze in the terminal.
    """

    print("\nMaze:")
    print("-" * (len(maze[0]) + 2))

    for row in range(len(maze)):

        line = ""

        for col in range(len(maze[row])):

            position = (row, col)

            if position == start:
                line += "S"

            elif position == end:
                line += "D"

            else:
                line += maze[row][col]

        print("|" + line + "|")

    print("-" * (len(maze[0]) + 2))


def display_path(maze, path, start, end):
    """
    Display the maze with the final path.

    Symbols:
        # = Wall
        . = Open cell
        S = Start
        D = Destination
        * = Solution path
    """

    path_set = set(path)

    print("\nSolved Maze:")
    print("-" * (len(maze[0]) + 2))

    for row in range(len(maze)):

        line = ""

        for col in range(len(maze[row])):

            position = (row, col)

            if position == start:
                line += "S"

            elif position == end:
                line += "D"

            elif position in path_set:
                line += "*"

            else:
                line += maze[row][col]

        print("|" + line + "|")

    print("-" * (len(maze[0]) + 2))