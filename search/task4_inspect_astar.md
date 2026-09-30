# Task 4: Inspect the A* Algorithm

Code: [warehouse.py](warehouse.py)

| Concept | Where it appears in the code |
|---|---|
| State | `(row, col)` tuples — `w.start`, `cell`, `nxt` |
| Action | the `ACTIONS` dictionary: `{"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}` |
| Transition | `Warehouse.moves(cell)` — applies each action and yields the new cell only if `free(nxt)` |
| Goal test | `if cell == w.goal:` in `astar`, right after a cell is popped and checked against `closed` |
| g(n) | the `g` dictionary; `cost = g[cell] + 1` |
| h(n) | `h(nxt, w.goal)` — `h` is `manhattan` by default |
| f(n) | `cost + h(nxt, w.goal)`, the first element of the heap entry |
| Frontier | the `frontier` list, used with `heapq.heappush` / `heapq.heappop` |
| Visited states | the `closed` set (cells already expanded), plus `g`, which records every cell reached |
| Path reconstruction | `build_path(parent, cell)` — follows `parent` back to the start and reverses the list |

## Questions (a)-(e)

See [answers.md](answers.md), Questions 5-9.
