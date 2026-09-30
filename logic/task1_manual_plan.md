# Task 1: Construct a Plan by Hand

Sequence of actions:

a1 = PickUp(Package,A)
a2 = Move(A,B)
a3 = Move(B,C)
a4 = Drop(Package,C)

I --a1--> S1 --a2--> S2 --a3--> S3 --a4--> S4, and S4 ⊨ G.

## State table

| State | Facts |
|-------|-------|
| S0 | At(Robot,A), At(Package,A) |
| S1 | At(Robot,A), Holding(Package) |
| S2 | At(Robot,B), Holding(Package) |
| S3 | At(Robot,C), Holding(Package) |
| S4 | At(Robot,C), At(Package,C) |

S4 satisfies the goal G = { At(Package,C) }, so this 4-action sequence is a valid plan.
