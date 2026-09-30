"""
Task 3: Test the Generated Planner.

Three tests against planner.py's BFS planner:
  A. Solvable problem      - the original warehouse problem.
  B. Impossible problem    - PickUp action removed, so the package can never move.
  C. Irrelevant actions    - an extra Move that repositions the robot but not the
                              package, to check the planner doesn't confuse
                              "robot reaches C" with "package reaches C".
"""

from planner import Action, solve

CONNECTIONS = [("A", "B"), ("B", "A"), ("B", "C"), ("C", "B")]


def make_actions(include_pickup=True, extra_shortcut=False):
    actions = []
    conns = list(CONNECTIONS)
    if extra_shortcut:
        conns.append(("A", "C"))  # Test C: direct robot-only shortcut A->C

    for src, dst in conns:
        actions.append(Action(
            "Move(Robot,%s,%s)" % (src, dst),
            pos_pre=["At(Robot,%s)" % src],
            neg_pre=[],
            pos_eff=["At(Robot,%s)" % dst],
            neg_eff=["At(Robot,%s)" % src],
        ))

    if include_pickup:
        for loc in ("A", "B", "C"):
            actions.append(Action(
                "PickUp(Package,%s)" % loc,
                pos_pre=["At(Robot,%s)" % loc, "At(Package,%s)" % loc],
                neg_pre=["Holding(Package)"],
                pos_eff=["Holding(Package)"],
                neg_eff=["At(Package,%s)" % loc],
            ))

    for loc in ("A", "B", "C"):
        actions.append(Action(
            "Drop(Package,%s)" % loc,
            pos_pre=["At(Robot,%s)" % loc, "Holding(Package)"],
            neg_pre=[],
            pos_eff=["At(Package,%s)" % loc],
            neg_eff=["Holding(Package)"],
        ))

    return actions


if __name__ == "__main__":
    initial = ["At(Robot,A)", "At(Package,A)"]
    goal = ["At(Package,C)"]

    # Test A: Solvable problem
    solve("Test A: Solvable problem", initial, make_actions(), goal)

    # Test B: Impossible problem (PickUp removed)
    solve("Test B: Impossible problem (no PickUp action)",
          initial, make_actions(include_pickup=False), goal)

    # Test C: Irrelevant actions (robot-only shortcut A->C added)
    solve("Test C: Irrelevant actions (robot-only shortcut Move(A,C))",
          initial, make_actions(extra_shortcut=True), goal)
