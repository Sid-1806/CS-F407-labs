# Task 4: Logic and Search

## Completed diagram

```
Current state
   |
Check action preconditions   <- LOGICAL REASONING
   |
Apply effects                <- LOGICAL REASONING  (the missing "?")
   |
Generate successor state
   |
Search over alternatives     <- SEARCH
   |
Goal?                        <- LOGICAL REASONING (entailment test)
```

The blank between "Check action preconditions" and "Generate successor state" is
**Apply effects**: compute S' = Apply(S, a) by removing negative effects and adding
positive effects.

## Explanation

**Where logical reasoning is used:**
- Testing whether an action is applicable: S ⊨ Preconditions(a) — positive
  preconditions are a subset of the current state and negative preconditions are
  disjoint from it (`Action.applicable` in planner.py).
- Computing the successor state: S' = Apply(S, a) — delete-then-add update
  (`Action.apply`).
- Testing whether a state satisfies the goal: S ⊨ G (`goal_satisfied`).

This is a fixed, deterministic evaluation of one action against one state — it does
not involve trying multiple possibilities. This is the "logic" half: it determines
*what is possible* from a given state.

**Where search is used:**
- Deciding which applicable action to try next, and in what order, when a state has
  several options — the BFS frontier/queue (`frontier`, `visited`, `parent` in
  `bfs_plan`).
- Exploring the space of reachable states level by level until one satisfies the
  goal, never revisiting a state already seen.

## Summary

Logic answers "is this action legal here, and what does it produce?" for a single
action/state pair. Search answers "given many legal branches, which sequence
actually reaches the goal?" The two combine at every node of the search: logic
generates/prunes each edge, search decides how to traverse the resulting graph.

**Logic determines what is possible; search determines what to try.**
