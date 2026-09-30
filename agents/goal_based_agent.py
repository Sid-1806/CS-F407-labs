"""
Goal-based agent for the warehouse navigation problem.

The vehicle must travel from the loading bay S to the dispatch area G without
entering a shelving unit '#'. It may move Up, Down, Left or Right, one square
per move.

Architecture (goal-based agent)
-------------------------------
    Environment  -- the warehouse grid; it reports the vehicle's position and
                    carries out moves.
    State        -- the vehicle's current (row, col).
    Model        -- the agent's copy of the map, used to predict which moves
                    are possible from any square.
    Goal         -- the square G.
    Decision     -- plan(): search the model for a sequence of moves that
                    reaches G, then act() executes that plan one move at a time.

A simple reflex agent would pick each move from what it sees right now and can
get trapped in dead ends; this agent looks ahead to the goal before moving.

Search algorithm: breadth-first search (BFS)
--------------------------------------------
Every move costs the same (one square), so the grid is an unweighted graph.
BFS explores squares in order of how many moves they are from the start, so
the first time it reaches G it has found a path with the fewest possible moves
(optimal), and it always finds a path if one exists (complete). It is also
simple and easy to check, which matters for a vehicle that must not collide.
A* with Manhattan distance would also be optimal and would explore fewer
squares on a very large warehouse, but for a map this size BFS is enough.
"""

from collections import deque

WAREHOUSE = """
#####################
#S....#............G#
#.##....##########..#
#....##.............#
#.######.###.#.###..#
#........#..........#
#####################
"""

MOVES = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}


class Environment:
    """The warehouse itself. It knows where the vehicle really is."""

    def __init__(self, ascii_map):
        self.grid = [list(line) for line in ascii_map.strip().splitlines()]
        self.position = self.find("S")

    def find(self, symbol):
        for r, row in enumerate(self.grid):
            for c, ch in enumerate(row):
                if ch == symbol:
                    return (r, c)
        return None

    def percept(self):
        return self.position

    def execute(self, move):
        dr, dc = MOVES[move]
        r, c = self.position
        target = (r + dr, c + dc)
        if self.grid[target[0]][target[1]] == "#":
            raise RuntimeError(f"collision at {target}")
        self.position = target


class GoalBasedAgent:
    def __init__(self, ascii_map):
        self.map = [line for line in ascii_map.strip().splitlines()]   # the agent's model
        self.goal = self._find("G")
        self.plan = []

    def _find(self, symbol):
        for r, line in enumerate(self.map):
            if symbol in line:
                return (r, line.index(symbol))
        return None

    def _free(self, cell):
        r, c = cell
        return 0 <= r < len(self.map) and 0 <= c < len(self.map[0]) and self.map[r][c] != "#"

    def make_plan(self, start):
        """BFS from `start` to the goal. Returns a list of moves, or None."""
        came_from = {start: None}          # cell -> (previous cell, move used)
        queue = deque([start])
        while queue:
            cell = queue.popleft()
            if cell == self.goal:
                moves = []
                while came_from[cell] is not None:
                    cell, move = came_from[cell][0], came_from[cell][1]
                    moves.append(move)
                return moves[::-1]
            for move, (dr, dc) in MOVES.items():
                nxt = (cell[0] + dr, cell[1] + dc)
                if self._free(nxt) and nxt not in came_from:
                    came_from[nxt] = (cell, move)
                    queue.append(nxt)
        return None

    def act(self, env):
        """Perceive, plan once, then carry out the plan move by move."""
        start = env.percept()
        self.plan = self.make_plan(start)
        if self.plan is None:
            return None
        route = [start]
        for move in self.plan:
            env.execute(move)
            route.append(env.percept())
        return route


def show(ascii_map, route):
    on_route = set(route[1:-1])
    for r, line in enumerate(ascii_map.strip().splitlines()):
        print("  " + "".join("*" if (r, c) in on_route else ch for c, ch in enumerate(line)))


if __name__ == "__main__":
    env = Environment(WAREHOUSE)
    agent = GoalBasedAgent(WAREHOUSE)

    print(f"Warehouse: {len(env.grid)} rows x {len(env.grid[0])} columns, "
          f"start S = {env.position}, goal G = {agent.goal}")
    route = agent.act(env)

    if route is None:
        print("No collision-free path exists from S to G.")
    else:
        print(f"Collision-free path found: {len(agent.plan)} moves")
        print(f"Moves: {' '.join(agent.plan)}")
        print(f"Squares visited: {route}")
        print(f"Vehicle finished at {env.position}, goal reached: {env.position == agent.goal}")
        show(WAREHOUSE, route)
