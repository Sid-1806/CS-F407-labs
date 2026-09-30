# Task 0: Understand the Planning Problem

## (a) Initial state I
I = { At(Robot,A), At(Package,A) }

## (b) Goal G
G = { At(Package,C) }

## (c) Actions available to the robot
- Move(A,B), Move(B,A), Move(B,C), Move(C,B)
- PickUp(Package,A), PickUp(Package,B), PickUp(Package,C)
- Drop(Package,A), Drop(Package,B), Drop(Package,C)

## (d) Preconditions and effects of each action

### Move(X,Y) — for each connected pair (A-B, B-A, B-C, C-B)
- Preconditions: At(Robot,X)
- Effects: ¬At(Robot,X), At(Robot,Y)

### PickUp(Package,L)
- Preconditions: At(Robot,L), At(Package,L)
- Effects: ¬At(Package,L), Holding(Package)

### Drop(Package,L)
- Preconditions: At(Robot,L), Holding(Package)
- Effects: ¬Holding(Package), At(Package,L)

## Which actions are applicable in the initial state?

I = { At(Robot,A), At(Package,A) }

- **PickUp(Package,A)** — preconditions are At(Robot,A) and At(Package,A). Both hold in I,
  so PickUp(Package,A) is **applicable**.
- **Drop(Package,C)** — preconditions are At(Robot,C) and Holding(Package). Neither holds
  in I (robot is at A, not C; nothing is being held), so Drop(Package,C) is **not applicable**.
- **Move(A,B)** — precondition At(Robot,A) holds in I, so it is **applicable**.
- All other Move/PickUp/Drop actions require facts (At(Robot,B), At(Robot,C), At(Package,B),
  At(Package,C), Holding(Package)) that are not in I, so they are **not applicable** initially.

An action being merely present in the action list does not make it usable — applicability is
decided purely by checking S ⊨ Preconditions(a) against the current state.
