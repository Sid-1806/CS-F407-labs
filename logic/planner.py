"""
Simple STRIPS-style planning agent.

A state is a set of logical propositions (strings). An action has positive and
negative preconditions and positive and negative effects. Breadth-first search
finds a shortest (fewest-actions) plan from the initial state to a state that
satisfies the goal.
"""

from collections import deque


class Action:
    def __init__(self, name, pos_pre=None, neg_pre=None, pos_eff=None, neg_eff=None):
        self.name = name
        self.pos_pre = frozenset(pos_pre or [])   # must be present in the state
        self.neg_pre = frozenset(neg_pre or [])   # must be absent from the state
        self.pos_eff = frozenset(pos_eff or [])   # added on application
        self.neg_eff = frozenset(neg_eff or [])   # removed on application

    def applicable(self, state):
        """True if every precondition holds in `state`."""
        return self.pos_pre <= state and self.neg_pre.isdisjoint(state)

    def apply(self, state):
        """Return the new state after applying this action.

        Delete effects first, then add effects (so an atom in both is kept).
        """
        return (state - self.neg_eff) | self.pos_eff

    def __repr__(self):
        return self.name


def goal_satisfied(state, pos_goal, neg_goal):
    pos_goal = frozenset(pos_goal or [])
    neg_goal = frozenset(neg_goal or [])
    return pos_goal <= state and neg_goal.isdisjoint(state)


def bfs_plan(initial_state, actions, pos_goal, neg_goal=None):
    """Breadth-first search over states.

    Returns (plan, states) where `plan` is the list of actions and `states` is
    the list of states reached after each action. Returns (None, None) if no
    plan exists.
    """
    start = frozenset(initial_state)

    if goal_satisfied(start, pos_goal, neg_goal):
        return [], []                     # goal already true: empty plan

    frontier = deque([start])
    # visited guards against revisiting a state and against infinite loops
    visited = {start}
    # parent[state] = (previous_state, action_that_led_here)
    parent = {start: None}

    while frontier:
        state = frontier.popleft()
        for action in actions:
            if not action.applicable(state):
                continue
            nxt = action.apply(state)
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = (state, action)

            if goal_satisfied(nxt, pos_goal, neg_goal):
                return reconstruct(nxt, parent)
            frontier.append(nxt)

    return None, None                     # frontier exhausted: no plan


def reconstruct(end_state, parent):
    """Walk parent pointers back to the start to build the plan."""
    plan, states = [], []
    node = end_state
    while parent[node] is not None:
        prev, action = parent[node]
        plan.append(action)
        states.append(node)
        node = prev
    plan.reverse()
    states.reverse()
    return plan, states


def solve(name, initial_state, actions, pos_goal, neg_goal=None):
    print("=" * 60)
    print(name)
    print("=" * 60)
    print("Initial state:", set(initial_state))
    print("Goal (positive):", set(pos_goal))
    if neg_goal:
        print("Goal (negative):", set(neg_goal))

    plan, states = bfs_plan(initial_state, actions, pos_goal, neg_goal)

    if plan is None:
        print("\nNo plan exists.")
        return

    if not plan:
        print("\nGoal already satisfied; empty plan.")
        return

    print("\nPlan (%d actions):" % len(plan))
    for i, (action, state) in enumerate(zip(plan, states), start=1):
        print("  %d. %s" % (i, action.name))
        print("       -> state: %s" % sorted(state))
    print()


if __name__ == "__main__":
    # ---- Example: a tiny blocks-world-ish domain --------------------------
    # Propositions: at-A, at-B, at-C, key, door-open

    actions = [
        Action("walk-A-to-B",
               pos_pre=["at-A"],
               neg_pre=[],
               pos_eff=["at-B"],
               neg_eff=["at-A"]),
        Action("pick-up-key",
               pos_pre=["at-B"],
               neg_pre=["key"],
               pos_eff=["key"],
               neg_eff=[]),
        Action("open-door",
               pos_pre=["at-B", "key"],
               neg_pre=["door-open"],
               pos_eff=["door-open"],
               neg_eff=[]),
        Action("walk-B-to-C",
               pos_pre=["at-B", "door-open"],
               neg_pre=[],
               pos_eff=["at-C"],
               neg_eff=["at-B"]),
    ]

    solve("Solvable problem",
          initial_state=["at-A"],
          actions=actions,
          pos_goal=["at-C"])

    # ---- Example with no solution: no way to obtain the key -------------
    actions_no_key = [a for a in actions if a.name != "pick-up-key"]
    solve("Unsolvable problem (key unreachable)",
          initial_state=["at-A"],
          actions=actions_no_key,
          pos_goal=["at-C"])
