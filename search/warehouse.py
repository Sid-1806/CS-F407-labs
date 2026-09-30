"""
Warehouse robot navigation as a search problem  P = (S, A, T, s0, G, c).

    S  : free cells (row, col) of the map
    A  : Up, Down, Left, Right
    T  : move one cell; allowed only if the new cell is inside the map and not '#'
    s0 : the cell marked 'S'
    G  : the cell marked 'G'
    c  : 1 per move

A* orders the frontier by f(n) = g(n) + h(n). BFS is the blind baseline.
Standard library only.
"""

import heapq
from collections import deque

ACTIONS = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}


class Warehouse:
    def __init__(self, ascii_map):
        self.rows = ascii_map.strip().splitlines()
        self.height = len(self.rows)
        self.width = len(self.rows[0])
        self.start = self.locate("S")
        self.goal = self.locate("G")

    def locate(self, symbol):
        for r, line in enumerate(self.rows):
            if symbol in line:
                return (r, line.index(symbol))
        return None

    def free(self, cell):
        r, c = cell
        return 0 <= r < self.height and 0 <= c < self.width and self.rows[r][c] != "#"

    def moves(self, cell):
        """Transition function: every (action, next cell) allowed from `cell`."""
        r, c = cell
        for action, (dr, dc) in ACTIONS.items():
            nxt = (r + dr, c + dc)
            if self.free(nxt):
                yield action, nxt

    def free_cells(self):
        return sum(self.free((r, c)) for r in range(self.height) for c in range(self.width))

    def draw(self, path):
        marked = set(path) - {self.start, self.goal}
        for r, line in enumerate(self.rows):
            print("  " + "".join("*" if (r, c) in marked else ch for c, ch in enumerate(line)))


# ---- heuristics h(n) --------------------------------------------------------
def manhattan(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def euclidean(cell, goal):
    return ((cell[0] - goal[0]) ** 2 + (cell[1] - goal[1]) ** 2) ** 0.5


def zero(cell, goal):
    return 0


def twice_manhattan(cell, goal):
    return 2 * manhattan(cell, goal)


# ---- search -------------------------------------------------------------------
def build_path(parent, cell):
    path = []
    while cell is not None:
        path.append(cell)
        cell = parent[cell]
    return path[::-1]


def astar(w, h=manhattan):
    """Returns (path or None, number of states expanded)."""
    g = {w.start: 0}
    parent = {w.start: None}
    frontier = [(h(w.start, w.goal), w.start)]   # entries are (f, cell)
    closed = set()

    while frontier:
        _, cell = heapq.heappop(frontier)
        if cell in closed:            # an older, more expensive entry for this cell
            continue
        if cell == w.goal:            # goal test when the cell leaves the frontier
            return build_path(parent, cell), len(closed)
        closed.add(cell)

        for _, nxt in w.moves(cell):
            cost = g[cell] + 1
            if cost < g.get(nxt, float("inf")):
                g[nxt] = cost
                parent[nxt] = cell
                heapq.heappush(frontier, (cost + h(nxt, w.goal), nxt))

    return None, len(closed)


def bfs(w):
    """Returns (path or None, number of states expanded)."""
    parent = {w.start: None}
    frontier = deque([w.start])
    expanded = 0

    while frontier:
        cell = frontier.popleft()
        if cell == w.goal:
            return build_path(parent, cell), expanded
        expanded += 1
        for _, nxt in w.moves(cell):
            if nxt not in parent:
                parent[nxt] = cell
                frontier.append(nxt)

    return None, expanded


def show(label, w, path, expanded):
    print(label)
    if path is None:
        print("  solution found:  no")
    else:
        print("  solution found:  yes")
        print(f"  path length:     {len(path) - 1}")
        print(f"  path:            {path}")
    print(f"  states expanded: {expanded}")


LAB_MAP = """
#################
#S....#.........#
#.###.#.#######.#
#...#.#.......#.#
###.#.#######.#.#
#...#.........#.#
#.###########.#.#
#.............#G#
#################
"""


if __name__ == "__main__":
    w = Warehouse(LAB_MAP)
    path, expanded = astar(w)
    show("A* with Manhattan distance on the lab warehouse", w, path, expanded)
    w.draw(path)
