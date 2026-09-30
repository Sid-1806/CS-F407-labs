"""
Warehouse Navigation - Goal-Based Agent
========================================

Problem
-------
An autonomous warehouse vehicle must travel from a loading bay (S) to a
dispatch area (G) inside a warehouse that contains shelving units (obstacles)
which cannot be crossed. The vehicle must find a collision-free path.

Agent type: GOAL-BASED AGENT
-----------------------------
This is modeled as a goal-based agent (as opposed to a simple reflex agent)
because:
  - It maintains an internal model of the environment (the grid map).
  - It has an explicit goal (reach cell G).
  - It reasons about the CONSEQUENCES of possible action sequences (moves)
    before acting, by searching the state space for a sequence of moves
    that achieves the goal.
  - It does not just react to the current percept; it plans ahead.

Search Algorithm Chosen: Breadth-First Search (BFS)
-----------------------------------------------------
Why BFS is appropriate here:
  1. The warehouse grid is an UNWEIGHTED graph - every move (up/down/left/
     right) between adjacent free cells has the same cost (1 step).
  2. BFS explores the search space level by level (shortest number of moves
     first), which guarantees that the FIRST time it reaches the goal, it
     has found a path with the MINIMUM number of steps - i.e. it is
     optimal for unweighted graphs.
  3. BFS is complete: if a path exists, BFS is guaranteed to find it.
  4. BFS is simple, memory-efficient enough for typical warehouse grid
     sizes, and easy to verify/debug - all desirable properties for a
     safety-relevant task like vehicle path planning.
  (An alternative such as A* would also work and could be faster on very
  large grids by using a heuristic like Manhattan distance, but BFS already
  gives the optimal answer here since all step costs are equal, and is
  simpler to implement and reason about.)

Program Structure
------------------
  - Warehouse: represents the grid, obstacles, start and goal.
  - WarehouseAgent: the goal-based agent that perceives the warehouse model
    and searches for a plan (path) to the goal using BFS.
  - main(): builds a sample warehouse map, runs the agent, and prints the
    result.
"""

from collections import deque


class Warehouse:
    """Represents the warehouse as a 2D grid.

    Grid symbols:
        '.'  -> free, traversable cell
        '#'  -> shelving unit / obstacle (cannot be crossed)
        'S'  -> start position (loading bay)
        'G'  -> goal position (dispatch area)
    """

    def __init__(self, grid_layout):
        self.grid = [list(row) for row in grid_layout]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0
        self.start = self._find_symbol('S')
        self.goal = self._find_symbol('G')

        if self.start is None:
            raise ValueError("No start position 'S' found in the warehouse map.")
        if self.goal is None:
            raise ValueError("No goal position 'G' found in the warehouse map.")

    def _find_symbol(self, symbol):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == symbol:
                    return (r, c)
        return None

    def is_within_bounds(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_obstacle(self, pos):
        r, c = pos
        return self.grid[r][c] == '#'

    def is_free(self, pos):
        """A cell is traversable if it is within bounds and not a shelf."""
        return self.is_within_bounds(pos) and not self.is_obstacle(pos)

    def display(self, path=None):
        """Print the grid, optionally overlaying a found path with '*'."""
        path_cells = set(path) - {self.start, self.goal} if path else set()
        for r in range(self.rows):
            row_str = ""
            for c in range(self.cols):
                if (r, c) in path_cells:
                    row_str += "*"
                else:
                    row_str += self.grid[r][c]
            print(row_str)


class WarehouseAgent:
    """A goal-based agent that plans a collision-free path from S to G.

    The agent's internal model of the world is the Warehouse grid. Given
    the current state (its position) and the goal, it searches over
    possible action sequences (moves) using BFS and returns the resulting
    plan (path) if one exists.
    """

    # Possible moves: up, down, left, right (4-connectivity - a vehicle
    # cannot cut diagonally through the corner of a shelving unit).
    MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, warehouse: Warehouse):
        self.warehouse = warehouse

    def find_path(self):
        """Search for a collision-free path from start to goal using BFS.

        Returns:
            A list of (row, col) tuples representing the path from start
            to goal (inclusive), or None if no path exists.
        """
        start = self.warehouse.start
        goal = self.warehouse.goal

        frontier = deque([start])
        came_from = {start: None}  # tracks how each cell was reached

        while frontier:
            current = frontier.popleft()

            if current == goal:
                return self._reconstruct_path(came_from, goal)

            for dr, dc in self.MOVES:
                neighbor = (current[0] + dr, current[1] + dc)

                if not self.warehouse.is_free(neighbor):
                    continue  # obstacle or out of bounds: cannot go there
                if neighbor in came_from:
                    continue  # already visited/queued

                came_from[neighbor] = current
                frontier.append(neighbor)

        return None  # frontier exhausted without reaching goal: no path

    @staticmethod
    def _reconstruct_path(came_from, goal):
        """Backtrack from the goal to the start using the came_from map."""
        path = []
        node = goal
        while node is not None:
            path.append(node)
            node = came_from[node]
        path.reverse()
        return path


def main():
    # Sample warehouse map.
    #   S = loading bay (start), G = dispatch area (goal)
    #   # = shelving unit (obstacle), . = free aisle space
    warehouse_map = [
 "#####################"
"#S....#............G#"
"#.##....##########..#"
"#....##.............#"
"#.######.###.#.###..#"
"#........#..........#"
"#####################"
    ]

    warehouse = Warehouse(warehouse_map)
    agent = WarehouseAgent(warehouse)

    print("Warehouse layout ('S'=start, 'G'=goal, '#'=shelving unit obstacle):")
    warehouse.display()
    print()

    path = agent.find_path()

    if path:
        print(f"Collision-free path found! Length: {len(path)} cells "
              f"({len(path) - 1} moves).")
        print("Path (row, col):")
        print(path)
        print()
        print("Warehouse with path marked ('*'):")
        warehouse.display(path)
    else:
        print("No collision-free path exists between the loading bay (S) "
              "and the dispatch area (G). The shelving units completely "
              "block all routes.")


if __name__ == "__main__":
    main()
