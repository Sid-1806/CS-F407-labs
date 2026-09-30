# Task 1: Plan the Agent

## 1. State representation
A tuple `(row, col)`. Tuples can be used as dictionary keys and set members.

## 2. Warehouse representation
The ASCII map is kept as a list of strings, one per row. `S` and `G` are found by scanning the rows.
The map never changes during the search.

## 3. Valid actions
For each move `Up (-1,0)`, `Down (1,0)`, `Left (0,-1)` and `Right (0,1)`, work out the new cell and
keep it only if it is inside the map and not `#`.

## 4. Goal recognition
`cell == goal`, checked when a cell is taken off the frontier, not when it is first generated. That
way A* only stops once the cheapest path to G is known.

## 5. Frontier contents
- A*: a priority queue (`heapq`) of `(f, cell)` entries, ordered by f = g + h.
- BFS: a FIFO queue (`deque`) of cells.

Kept alongside the frontier:
- `g[cell]` — the cheapest known cost from the start;
- `parent[cell]` — the cell it was reached from;
- `closed` — the cells already expanded, so no cell is expanded twice.

## 6. Path reconstruction
Follow `parent` back from G until reaching the start (whose parent is `None`), then reverse the list.

## Reported on termination
- whether a solution was found;
- the path (list of cells);
- the path length (number of moves);
- the number of states expanded.
