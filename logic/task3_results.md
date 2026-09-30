# Task 3: Test Results

Test code: [task3_tests.py](task3_tests.py). Run with `python task3_tests.py`.

## Test A: Solvable problem
- Initial state: { At(Robot,A), At(Package,A) }
- Goal: { At(Package,C) }
- Plan found: yes
- Plan:
  1. PickUp(Package,A) → { At(Robot,A), Holding(Package) }
  2. Move(Robot,A,B) → { At(Robot,B), Holding(Package) }
  3. Move(Robot,B,C) → { At(Robot,C), Holding(Package) }
  4. Drop(Package,C) → { At(Package,C), At(Robot,C) }
- Valid? Yes — every action's preconditions hold in the state immediately before it
  (checked by hand against the state table, matching Task 1's manual plan).

## Test B: Impossible problem (PickUp action removed)
- Initial state: { At(Robot,A), At(Package,A) }
- Goal: { At(Package,C) }
- Plan found: no — planner prints "No plan exists."
- Reasoning: without PickUp, `Holding(Package)` can never become true, so `At(Package,C)`
  can never be added by Drop either (Drop requires Holding(Package)). The package is
  permanently stuck at A. BFS correctly exhausts the (finite) reachable state space
  — {At(Robot,A)|At(Robot,B)|At(Robot,C)} x {At(Package,A)} — without ever finding a
  goal state, and reports failure instead of inventing an action.

## Test C: Irrelevant actions (extra Move(A,C) robot-only shortcut)
- Initial state: { At(Robot,A), At(Package,A) }
- Goal: { At(Package,C) }
- Plan found: yes
- Plan:
  1. PickUp(Package,A) → { At(Robot,A), Holding(Package) }
  2. Move(Robot,A,C) → { At(Robot,C), Holding(Package) }
  3. Drop(Package,C) → { At(Package,C), At(Robot,C) }
- Valid? Yes. Because BFS explores shortest plans first, adding a robot-only shortcut A→C
  actually shortens the true plan from 4 to 3 actions (robot carries the package, so
  reaching C directly with the package still held is legitimate progress). Crucially,
  the planner never treats the robot merely arriving at C as satisfying the goal — the
  goal At(Package,C) only becomes true after Drop(Package,C) explicitly adds it. This
  confirms the planner distinguishes "robot's location" from "package's location" and
  does not shortcut the goal test incorrectly.
