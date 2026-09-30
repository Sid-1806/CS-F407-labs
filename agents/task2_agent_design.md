# Task 2: Designing the Agent

## Components

| Component | Design | In [goal_based_agent.py](goal_based_agent.py) |
|---|---|---|
| Environment | 7 x 21 warehouse grid: `.` free, `#` shelving unit, `S` loading bay, `G` dispatch area. Fully observable, deterministic, static, discrete. It reports where the vehicle is and carries out moves. | `Environment` — `percept()`, `execute(move)` |
| Current state | The vehicle's position (row, col), starting at S = (1, 1) | `Environment.position`, read through `percept()` |
| Goal | Reach G = (1, 19) without entering a `#` square or leaving the grid | `GoalBasedAgent.goal` |
| Available actions | Up, Down, Left, Right — one square each, only into free squares | `MOVES`, checked with `GoalBasedAgent._free` |
| Decision-making component | Plan first: breadth-first search over the agent's copy of the map for a sequence of moves from the current position to G. Then act: carry out the moves one at a time. | `make_plan` (BFS), `act` |

## Block diagram

```
   +--------------------------------+
   |  Environment (warehouse grid)  |
   +--------------------------------+
        | percept: current           ^
        | position                   |  execute(move): Up/Down/Left/Right
        v                            |
   +----------------------------+    |
   |  State: current (row,col)  |    |
   |  Model: agent's map copy   |    |
   +----------------------------+    |
        |                            |
        v                            |
   +----------------------------+    |
   |  Goal: reach G             |    |
   +----------------------------+    |
        |                            |
        v                            |
   +----------------------------+    |
   |  Decision making:          |    |
   |  BFS plan S -> ... -> G,   |----+
   |  then execute move by move |
   +----------------------------+
```

The agent perceives its position and uses its model of the map to work out which moves are
possible. It searches for a sequence of moves that reaches the goal, and then carries out that plan
in the environment. The environment refuses any move into a shelf, so a wrong plan would show up as
a collision error.
