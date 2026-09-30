# Task 0: Understand the Search Problem

Warehouse map (rows numbered from 0 at the top, columns from 0 at the left):

```
#################
#S....#.........#
#.###.#.#######.#
#...#.#.......#.#
###.#.#######.#.#
#...#.........#.#
#.###########.#.#
#.............#G#
#################
```

## Search problem P = (S, A, T, s0, G, c)

| Component | My specification |
|---|---|
| State S | The robot's cell (row, col), for every cell that is not `#` (64 states) |
| Actions A | { Up, Down, Left, Right } |
| Transition T | T((r,c), Up) = (r-1,c), T((r,c), Down) = (r+1,c), T((r,c), Left) = (r,c-1), T((r,c), Right) = (r,c+1) — only if the new cell is inside the map and not `#`; otherwise the action is not applicable |
| Initial state s0 | (1, 1), the cell marked `S` |
| Goal G | (7, 15), the cell marked `G` |
| Cost c | 1 for every move |

## Questions (a)-(d)

See [answers.md](answers.md), Questions 1-4.
