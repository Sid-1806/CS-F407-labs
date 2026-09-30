# Task 2: Ask an LLM to Generate A*

LLM used: Claude.

## Prompt used

I am implementing a simple goal-based search agent in Python.
The environment is a grid represented by an ASCII map. The agent starts at S and must reach G.
`#` is an obstacle and `.` is a free cell. The agent can move up, down, left or right, and every
move costs 1. Implement A* search with Manhattan distance h(n) = |r - rG| + |c - cG|.

The program should:
- represent states as (row, col) tuples;
- keep a heapq priority queue as the frontier;
- calculate g(n), h(n) and f(n);
- never expand the same state twice;
- do the goal test when a state is taken off the frontier;
- reconstruct the path when the goal is reached;
- report whether a solution was found, the path, its length and the number of states expanded.

Also write a BFS version for comparison, and make the heuristic a parameter so that I can try
h = 0, Euclidean distance and 2 x Manhattan. Use only the standard library and keep it simple.

## Generated program

[warehouse.py](warehouse.py):
- `Warehouse` — reads the map; `free`, `moves` (transition function), `free_cells`, `draw`;
- heuristics — `manhattan`, `euclidean`, `zero`, `twice_manhattan`;
- `astar(w, h)` and `bfs(w)` — each returns `(path, states expanded)`;
- `build_path` — path reconstruction.

Experiment scripts: [task3_tests.py](task3_tests.py), [task5_compare.py](task5_compare.py),
[task6_heuristics.py](task6_heuristics.py).

## Changes made to the generated code

None. The code passed every test in Task 3, and its path lengths matched BFS.

## Output on the lab warehouse (`python warehouse.py`)

```
A* with Manhattan distance on the lab warehouse
  solution found:  yes
  path length:     40
  path:            [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (4, 13), (3, 13), (3, 12), (3, 11), (3, 10), (3, 9), (3, 8), (3, 7), (2, 7), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (2, 15), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15)]
  states expanded: 63
  #################
  #S****#*********#
  #.###*#*#######*#
  #...#*#*******#*#
  ###.#*#######*#*#
  #...#*********#*#
  #.###########.#*#
  #.............#G#
  #################
```
