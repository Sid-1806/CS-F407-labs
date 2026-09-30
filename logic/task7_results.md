# Task 7: Using Prolog to Check a Proposed Plan — Results

Program: [task7_planner.pl](task7_planner.pl)

**Not executed in this session** — SWI-Prolog is not installed here (see
task6_results.md for install/online options).

## Expected results

```
?- valid_move(a,b).
true.

?- valid_move(b,c).
true.

?- valid_move(a,c).
false.
```

The first two queries succeed because `connected(a,b)` and `connected(b,c)` are
facts in the knowledge base, so the proposed plan Move(a,b), Move(b,c) is entirely
supported. The third fails because a and c have no direct connection — this matches
the note in the lab sheet ("the third should fail for the knowledge base given
above").

## Challenge: Move(a,c)

```
?- valid_move(a,c).
false.
```

Prolog reports that the action `Move(a,c)` is **not** supported by the warehouse
knowledge base. This means that if the Python planner (e.g. planner.py /
robot_delivery.py) were to ever propose `Move(a,c)` as part of a plan — for instance
due to a bug, or because someone incorrectly added a shortcut without updating the
action's precondition — Prolog, reasoning independently and only from the declared
`connected/2` facts, would catch it as an invalid move.

This demonstrates the architecture:

**Generate → Independent verification**

The Python program (possibly LLM-assisted) generates a candidate plan; Prolog,
using a separate logical description of the domain, checks whether each proposed
action is actually licensed by the facts — exactly the same principle used in
Task 5 to argue that an LLM's self-explanation is not a substitute for independent
verification.
