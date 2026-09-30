# Task 5: Compare A* with Blind Search

Code: [task5_compare.py](task5_compare.py). BFS is `bfs()` in [warehouse.py](warehouse.py): the same
`Warehouse` and moves, but a FIFO `deque` frontier instead of a priority queue. The warehouse was not
changed.

```
Lab warehouse (64 free cells)
  Measure             BFS    A*
  Solution found      yes   yes
  Path length          40    40
  States expanded      63    63
```

| Measure | BFS | A* |
|---|---|---|
| Solution found | yes | yes |
| Path length | 40 | 40 |
| States expanded | 63 | 63 |

Both algorithms expanded every free cell except G. The only route to G first leads away from it,
so the heuristic cannot save any work on this map.

## Questions (a)-(d)

See [answers.md](answers.md), Questions 10-13.
