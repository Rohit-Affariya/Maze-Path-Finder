from collections import deque
import heapq
import time

from maze import get_neighbors


def reconstruct_path(parent, start, end):
    """
    Reconstruct path from start to end using parent information.
    """

    if end not in parent:
        return []

    path = []
    current = end

    while current is not None:
        path.append(current)

        if current == start:
            break

        current = parent[current]

    path.reverse()

    if not path or path[0] != start:
        return []

    return path


# ============================================================
# 1. BREADTH-FIRST SEARCH
# ============================================================

def bfs(maze, start, end):
    """
    Breadth-First Search.

    BFS explores the maze level by level.

    For an unweighted maze, BFS guarantees
    the shortest path.

    Returns:
        path
        visited_order
        execution_time
    """

    start_time = time.perf_counter()

    queue = deque([start])

    visited_set = {start}
    visited_order = []

    parent = {
        start: None
    }

    while queue:

        current = queue.popleft()

        visited_order.append(current)

        if current == end:
            break

        for neighbor in get_neighbors(
            maze,
            current[0],
            current[1]
        ):

            if neighbor not in visited_set:

                visited_set.add(neighbor)
                parent[neighbor] = current

                queue.append(neighbor)

    path = reconstruct_path(
        parent,
        start,
        end
    )

    execution_time = (
        time.perf_counter() - start_time
    )

    return path, visited_order, execution_time


# ============================================================
# 2. DEPTH-FIRST SEARCH
# ============================================================

def dfs(maze, start, end):
    """
    Depth-First Search.

    DFS explores one branch deeply before backtracking.

    DFS does NOT guarantee the shortest path.

    Returns:
        path
        visited_order
        execution_time
    """

    start_time = time.perf_counter()

    stack = [start]

    visited_set = {start}
    visited_order = []

    parent = {
        start: None
    }

    while stack:

        current = stack.pop()

        visited_order.append(current)

        if current == end:
            break

        neighbors = get_neighbors(
            maze,
            current[0],
            current[1]
        )

        for neighbor in reversed(neighbors):

            if neighbor not in visited_set:

                visited_set.add(neighbor)
                parent[neighbor] = current

                stack.append(neighbor)

    path = reconstruct_path(
        parent,
        start,
        end
    )

    execution_time = (
        time.perf_counter() - start_time
    )

    return path, visited_order, execution_time


# ============================================================
# 3. A* SEARCH
# ============================================================

def manhattan_distance(current, goal):
    """
    Manhattan distance heuristic.

    h(n) = |x1 - x2| + |y1 - y2|
    """

    return (
        abs(current[0] - goal[0])
        + abs(current[1] - goal[1])
    )


def astar(maze, start, end):
    """
    A* Search.

    f(n) = g(n) + h(n)

    g(n) = actual cost from start
    h(n) = estimated cost to destination

    Uses Manhattan distance.
    """

    start_time = time.perf_counter()

    priority_queue = []

    counter = 0

    heapq.heappush(
        priority_queue,
        (
            manhattan_distance(start, end),
            counter,
            start
        )
    )

    g_score = {
        start: 0
    }

    parent = {
        start: None
    }

    closed = set()
    visited_order = []

    while priority_queue:

        _, _, current = heapq.heappop(
            priority_queue
        )

        if current in closed:
            continue

        closed.add(current)
        visited_order.append(current)

        if current == end:
            break

        for neighbor in get_neighbors(
            maze,
            current[0],
            current[1]
        ):

            if neighbor in closed:
                continue

            tentative_g = (
                g_score[current] + 1
            )

            if (
                neighbor not in g_score
                or tentative_g < g_score[neighbor]
            ):

                g_score[neighbor] = tentative_g
                parent[neighbor] = current

                h = manhattan_distance(
                    neighbor,
                    end
                )

                f = tentative_g + h

                counter += 1

                heapq.heappush(
                    priority_queue,
                    (
                        f,
                        counter,
                        neighbor
                    )
                )

    path = reconstruct_path(
        parent,
        start,
        end
    )

    execution_time = (
        time.perf_counter() - start_time
    )

    return path, visited_order, execution_time


# ============================================================
# 4. BIDIRECTIONAL BFS
# ============================================================


def bidirectional_bfs(maze, start, end):
    """
    Bidirectional BFS using complete BFS levels.

    Searches simultaneously from the start and destination.
    Returns an optimal shortest path for an unweighted maze.
    """

    start_time = time.perf_counter()

    if start == end:
        return [start], [start], (
            time.perf_counter() - start_time
        )

    queue_start = deque([start])
    queue_end = deque([end])

    parent_start = {start: None}
    parent_end = {end: None}

    distance_start = {start: 0}
    distance_end = {end: 0}

    visited_start = {start}
    visited_end = {end}

    visited_order = []
    visited_order_set = set()

    meeting_point = None
    expand_start = True

    while queue_start and queue_end:

        candidates = []

        if expand_start:

            # Expand one complete BFS level from start
            level_size = len(queue_start)

            for _ in range(level_size):

                current = queue_start.popleft()

                if current not in visited_order_set:
                    visited_order.append(current)
                    visited_order_set.add(current)

                for neighbor in get_neighbors(
                    maze,
                    current[0],
                    current[1]
                ):

                    if neighbor not in visited_start:

                        visited_start.add(neighbor)
                        parent_start[neighbor] = current

                        distance_start[neighbor] = (
                            distance_start[current] + 1
                        )

                        queue_start.append(neighbor)

                        if neighbor in visited_end:
                            candidates.append(neighbor)

        else:

            # Expand one complete BFS level from destination
            level_size = len(queue_end)

            for _ in range(level_size):

                current = queue_end.popleft()

                if current not in visited_order_set:
                    visited_order.append(current)
                    visited_order_set.add(current)

                for neighbor in get_neighbors(
                    maze,
                    current[0],
                    current[1]
                ):

                    if neighbor not in visited_end:

                        visited_end.add(neighbor)
                        parent_end[neighbor] = current

                        distance_end[neighbor] = (
                            distance_end[current] + 1
                        )

                        queue_end.append(neighbor)

                        if neighbor in visited_start:
                            candidates.append(neighbor)

        # Check all meeting points found in this level
        if candidates:

            meeting_point = min(
                candidates,
                key=lambda node: (
                    distance_start[node]
                    + distance_end[node]
                )
            )

            break

        # Alternate search direction
        expand_start = not expand_start

    # Reconstruct the shortest path
    if meeting_point is None:

        execution_time = (
            time.perf_counter() - start_time
        )

        return [], visited_order, execution_time

    path_from_start = reconstruct_path(
        parent_start,
        start,
        meeting_point
    )

    path_from_end = []

    current = parent_end[meeting_point]

    while current is not None:

        path_from_end.append(current)
        current = parent_end[current]

    path = path_from_start + path_from_end

    execution_time = (
        time.perf_counter() - start_time
    )

    return path, visited_order, execution_time


# ============================================================
# 5. DIJKSTRA'S ALGORITHM
# ============================================================

def dijkstra(maze, start, end):
    """
    Dijkstra's shortest-path algorithm.

    Every movement in the current maze has cost 1.

    Therefore Dijkstra will find the shortest path.
    """

    start_time = time.perf_counter()

    priority_queue = [
        (0, start)
    ]

    distance = {
        start: 0
    }

    parent = {
        start: None
    }

    visited_set = set()
    visited_order = []

    while priority_queue:

        current_distance, current = heapq.heappop(
            priority_queue
        )

        if current in visited_set:
            continue

        visited_set.add(current)
        visited_order.append(current)

        if current == end:
            break

        for neighbor in get_neighbors(
            maze,
            current[0],
            current[1]
        ):

            new_distance = current_distance + 1

            if (
                neighbor not in distance
                or new_distance < distance[neighbor]
            ):

                distance[neighbor] = new_distance

                parent[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (
                        new_distance,
                        neighbor
                    )
                )

    path = reconstruct_path(
        parent,
        start,
        end
    )

    execution_time = (
        time.perf_counter() - start_time
    )

    return path, visited_order, execution_time


# ============================================================
# 6. BELLMAN-FORD
# ============================================================

def bellman_ford(maze, start, end):
    """
    Bellman-Ford shortest-path algorithm.

    The maze is treated as a graph where each valid
    movement between adjacent cells has weight 1.

    Measurements:
        - visited_order: unique vertices processed
        - relaxation_count: number of edge relaxation attempts
        - execution_time: execution time

    Returns:
        path
        visited_order
        execution_time
    """

    start_time = time.perf_counter()

    rows = len(maze)
    cols = len(maze[0])

    # --------------------------------------------------------
    # Create list of walkable vertices
    # --------------------------------------------------------

    vertices = []

    for row in range(rows):

        for col in range(cols):

            if maze[row][col] != "#":

                vertices.append(
                    (row, col)
                )

    distance = {
        vertex: float("inf")
        for vertex in vertices
    }

    parent = {}

    distance[start] = 0
    parent[start] = None

    # --------------------------------------------------------
    # Track unique vertices
    # --------------------------------------------------------

    visited_set = set()

    # Track how many relaxation attempts are performed
    relaxation_count = 0

    # --------------------------------------------------------
    # Relax edges V-1 times
    # --------------------------------------------------------

    for _ in range(len(vertices) - 1):

        changed = False

        for vertex in vertices:

            # Ignore unreachable vertices
            if distance[vertex] == float("inf"):
                continue

            # Record vertex only once
            visited_set.add(vertex)

            for neighbor in get_neighbors(
                maze,
                vertex[0],
                vertex[1]
            ):

                relaxation_count += 1

                new_distance = (
                    distance[vertex] + 1
                )

                if new_distance < distance[neighbor]:

                    distance[neighbor] = new_distance
                    parent[neighbor] = vertex

                    changed = True

        # ----------------------------------------------------
        # Early stopping
        # ----------------------------------------------------

        if not changed:
            break

    # Convert set to list for consistency with other
    # algorithms.
    visited_order = list(visited_set)

    # --------------------------------------------------------
    # Reconstruct shortest path
    # --------------------------------------------------------

    path = reconstruct_path(
        parent,
        start,
        end
    )

    execution_time = (
        time.perf_counter() - start_time
    )

    return path, visited_order, execution_time