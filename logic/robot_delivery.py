"""
Robot package-delivery problem, encoded for the planner in planner.py.

Locations: A, B, C
Connections (directed): A-B, B-A, B-C, C-B
Initial: At(Robot,A), At(Package,A)
Goal:    At(Package,C)
"""

from planner import Action, solve

CONNECTIONS = [("A", "B"), ("B", "A"), ("B", "C"), ("C", "B")]

actions = []

# Move(Robot, from, to) for each connected pair
for src, dst in CONNECTIONS:
    actions.append(Action(
        "Move(Robot,%s,%s)" % (src, dst),
        pos_pre=["At(Robot,%s)" % src],
        neg_pre=[],
        pos_eff=["At(Robot,%s)" % dst],
        neg_eff=["At(Robot,%s)" % src],
    ))

# PickUp(Package, L): robot and package co-located, robot not already holding it
for loc in ("A", "B", "C"):
    actions.append(Action(
        "PickUp(Package,%s)" % loc,
        pos_pre=["At(Robot,%s)" % loc, "At(Package,%s)" % loc],
        neg_pre=["Holding(Package)"],
        pos_eff=["Holding(Package)"],
        neg_eff=["At(Package,%s)" % loc],
    ))

# Drop(Package, L): robot at L and holding the package
for loc in ("A", "B", "C"):
    actions.append(Action(
        "Drop(Package,%s)" % loc,
        pos_pre=["At(Robot,%s)" % loc, "Holding(Package)"],
        neg_pre=[],
        pos_eff=["At(Package,%s)" % loc],
        neg_eff=["Holding(Package)"],
    ))

if __name__ == "__main__":
    solve(
        "Robot delivery: move Package from A to C",
        initial_state=["At(Robot,A)", "At(Package,A)"],
        actions=actions,
        pos_goal=["At(Package,C)"],
    )
