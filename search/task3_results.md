# Task 3: Test the Generated Program

Test code: [task3_tests.py](task3_tests.py). Run with `python task3_tests.py`.
Each A* result is checked against the expected length and against BFS, which always gives the
shortest path when every move costs 1.

## Test 1: Original warehouse
- Solution found: yes
- Path: (1,1) → (1,2) → (1,3) → (1,4) → (1,5) → (2,5) → (3,5) → (4,5) → (5,5) → (5,6) → … → (5,13)
  → (4,13) → (3,13) → (3,12) → … → (3,7) → (2,7) → (1,7) → (1,8) → … → (1,15) → (2,15) → … → (7,15)
- Path length: 40
- States expanded: 63
- BFS also gives 40, so this is a shortest path.

## Test 2: Trivial case
```
#####
#SG##
#####
```
- Solution found: yes
- Path: (1,1) → (1,2)
- Path length: 1
- States expanded: 1

## Test 3: No solution
```
#######
#S....#
###.###
#...#G#
#######
```
- Solution found: no
- States expanded: 9 — exactly the cells reachable from S. The search stops when the frontier is
  empty instead of looping forever.

## Test 4: Alternative paths
```
###########
#S.......G#
#.#######.#
#.........#
###########
```
Two routes: along the top row (8 moves) or down and around the bottom (12 moves).
- Solution found: yes
- Path: (1,1) → (1,2) → … → (1,9), the top route
- Path length: 8, the shorter route
- States expanded: 8

## Summary

| Test | Solution found | Path length | States expanded | Expected | Result |
|---|---|---|---|---|---|
| 1. Original warehouse | yes | 40 | 63 | 40 | PASS |
| 2. Trivial case | yes | 1 | 1 | 1 | PASS |
| 3. No solution | no | – | 9 | no path | PASS |
| 4. Alternative paths | yes | 8 | 8 | 8 | PASS |
