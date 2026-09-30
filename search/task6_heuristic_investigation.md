# Task 6: Investigate the Heuristic

Code: [task6_heuristics.py](task6_heuristics.py). Run with `python task6_heuristics.py`.

## Why Manhattan distance is appropriate (LLM explanation)

The robot moves one cell at a time and only horizontally or vertically, so reaching G needs at
least |r - rG| vertical moves and |c - cG| horizontal moves. Manhattan distance is exactly that
number. It equals the true cost when nothing is in the way, and walls can only make the real path
longer, so it never overestimates (it is admissible). Of the estimates that ignore walls, it is the
most accurate one.

## Heuristics tested

| Heuristic | Formula | Admissible? |
|---|---|---|
| Manhattan | \|dr\| + \|dc\| | yes |
| h(n) = 0 | 0 | yes (A* becomes uniform-cost search) |
| Euclidean | sqrt(dr² + dc²) | yes, but never larger than Manhattan |
| 2 x Manhattan | 2(\|dr\| + \|dc\|) | no — overestimates |

## Results: lab warehouse (shortest path 40)

| Heuristic | Solution found | Path length | States expanded |
|---|---|---|---|
| Manhattan | yes | 40 | 63 |
| h(n) = 0 | yes | 40 | 63 |
| Euclidean | yes | 40 | 63 |
| 2 x Manhattan | yes | 40 | 63 |

All four are the same: the maze has one route to G, and every search expands all 63 cells other
than G. So I also used a second map with open floor, where the heuristics can differ.

## Results: shelves map (shortest path 13)

```
###########
#S........#
#..#......#
##...#.##.#
#.....#...#
##......###
#........G#
###########
```

| Heuristic | Solution found | Path length | States expanded |
|---|---|---|---|
| Manhattan | yes | 13 | 40 |
| h(n) = 0 | yes | 13 | 44 |
| Euclidean | yes | 13 | 40 |
| 2 x Manhattan | yes | **17** | **22** |

Path with Manhattan (13 moves):
```
###########
#S***.....#
#..#*.....#
##..*#.##.#
#...**#...#
##...***###
#......**G#
###########
```

Path with 2 x Manhattan (17 moves):
```
###########
#S********#
#..#.....*#
##...#.##*#
#.....#***#
##.....*###
#......**G#
###########
```

## Observations

- **h = 0** (too optimistic): still finds the shortest path, but expands the most states (44), since
  it has no guidance.
- **Euclidean**: still finds the shortest path. It is never larger than Manhattan, but on these maps
  it expanded the same number of states.
- **Manhattan**: finds the shortest path and expands fewer states than h = 0.
- **2 x Manhattan** (too aggressive): expands the fewest states (22), but returns a path 4 moves
  longer than the shortest. It rushes along the top row because that looks closest to G, and never
  comes back to check the shorter route through the middle.

A* is only guaranteed to return a shortest path when h(n) ≤ h*(n).

## Questions 1-3

See [answers.md](answers.md), Questions 14-16.
