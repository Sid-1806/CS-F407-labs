# Task 6: Prolog as a Plan Verifier — Results

Program: [task6_planner.pl](task6_planner.pl)

**Not executed in this session** — SWI-Prolog (`swipl`) is not installed on this
machine and this environment cannot install software silently. To reproduce:
install SWI-Prolog from https://www.swi-prolog.org/download/stable (or paste the
file into https://swish.swi-prolog.org, no install needed) then run:

```
swipl task6_planner.pl
?- can_move(a,b).
?- can_move(a,c).
```

## Expected / predicted results (derived from the rule definitions)

```
?- can_move(a,b).
true.

?- can_move(a,c).
false.
```

## Questions

**(a) Why does Prolog return `true` for `can_move(a,b)`?**
Because `connected(a,b).` is asserted as a fact, and the rule
`can_move(X,Y) :- connected(X,Y).` says: to prove `can_move(X,Y)`, it suffices to
prove `connected(X,Y)`. Unifying X=a, Y=b, Prolog looks up `connected(a,b)` in the
database, finds it as a fact, and succeeds.

**(b) Why does it not establish `can_move(a,c)`?**
There is no fact `connected(a,c)` in the database, and `can_move/2` has only one
clause, which requires `connected(X,Y)` to hold directly. Prolog's closed-world
assumption means anything it cannot prove from the given facts and rules is treated
as false, so the query fails (`false.`) rather than raising an error. Since a and c
are only connected via b (not directly), and `can_move` does not chain through
intermediate locations, it cannot be derived.

**(c) Relationship between `can_move(X,Y)` and Connected(X,Y) → CanMove(X,Y)?**
The Prolog clause is a direct encoding of the material implication
Connected(X,Y) → CanMove(X,Y): whenever the antecedent Connected(X,Y) is true (i.e.
a matching `connected/2` fact exists), Prolog's SLD-resolution inference derives the
consequent CanMove(X,Y) as true. Prolog's rule-application mechanism is essentially
modus ponens applied backward from the query to the facts.
