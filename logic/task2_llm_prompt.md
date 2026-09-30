# Task 2: Ask an LLM to Implement the Planner

## Prompt used

I want to implement a simple planning agent in Python.
Represent a state as a set of logical propositions.
Each action should contain:
- a name;
- positive preconditions;
- negative preconditions;
- positive effects;
- negative effects.

An action is applicable if all of its preconditions are satisfied by the current state.
When an action is applied:
1. remove its negative effects from the state;
2. add its positive effects to the state.

Use breadth-first search to find a sequence of actions that achieves a specified goal.
The program should also:
- detect when no plan exists;
- print the resulting sequence of actions;
- print the states reached after each action.

Explain the implementation and identify any assumptions you make.

## Generated program

See [planner.py](planner.py) — the generic `Action` class + BFS planner (`bfs_plan`, `solve`)
generated from this prompt. The warehouse problem itself is encoded separately in
[robot_delivery.py](robot_delivery.py).

## Mapping the specification onto the code

| Specification idea | Where it appears in planner.py |
|---|---|
| Preconditions → when is an action applicable? | `Action.applicable(state)`: `pos_pre <= state and neg_pre.isdisjoint(state)` |
| Effects → how does the state change? | `Action.apply(state)`: `(state - neg_eff) \| pos_eff` (delete effects first, then add) |
| Goal → when does planning terminate? | `goal_satisfied(state, pos_goal, neg_goal)`, checked on the initial state and on every newly generated state in `bfs_plan` |
| BFS → how are alternative plans explored? | `frontier` (a FIFO `deque`), `visited` (seen states), `parent` (backpointers) in `bfs_plan` |

Run on the warehouse problem: see [task3_tests.md](task3_tests.md) for the executed output.
