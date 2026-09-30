# Task 3: Prompt Engineering

LLM used: Claude.

## Prompt used

Write a well-documented Python program implementing a goal-based agent for the warehouse
navigation problem shown below.

```
#####################
#S....#............G#
#.##....##########..#
#....##.............#
#.######.###.#.###..#
#........#..........#
#####################
```

S is the starting position, G is the goal, # is an obstacle and . is free space. The vehicle may
move Up, Down, Left or Right, and one move changes its position by one grid square.

The program should:
- represent the warehouse as a two-dimensional grid;
- determine a collision-free path from S to G;
- avoid all obstacles;
- print either the path found or a suitable message if no path exists;
- explain the search algorithm that has been chosen and why it is appropriate.

Structure it as a goal-based agent: keep the environment separate from the agent, and let the
agent plan a path to the goal before it starts moving.

## Generated program

[goal_based_agent.py](goal_based_agent.py):
- `Environment` — the real warehouse; `percept()` gives the vehicle's position, and `execute(move)`
  moves it (and raises an error on a collision);
- `GoalBasedAgent` — keeps its own copy of the map and the goal; `make_plan` runs breadth-first
  search, and `act` plans once and then carries out the moves;
- the module docstring explains why BFS was chosen.

Run with `python goal_based_agent.py`.

## Output

```
Warehouse: 7 rows x 21 columns, start S = (1, 1), goal G = (1, 19)
Collision-free path found: 20 moves
Moves: Right Right Right Down Right Right Right Up Right Right Right Right Right Right Right Right Right Right Right Right
Squares visited: [(1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (2, 5), (2, 6), (2, 7), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19)]
Vehicle finished at (1, 19), goal reached: True
  #####################
  #S***.#************G#
  #.##****##########..#
  #....##.............#
  #.######.###.#.###..#
  #........#..........#
  #####################
```

The path goes down to row 2 to get round the shelf at (1, 6), then back up and straight along the
top row to G. 20 moves is the minimum: G is 18 columns from S, and getting round the shelf adds one
move down and one move back up.

No-path check: on a map where G is walled off (`#S#G#`), `make_plan` returns `None`, so the program
prints "No collision-free path exists from S to G."

## Questions 1-4

See [answers.md](answers.md), Questions 6-9.
