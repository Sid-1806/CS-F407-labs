# Task 8: Connect Prolog to Logical Reasoning

## Program

```prolog
wet_road.

slippery :-
    wet_road.

reduce_speed :-
    slippery.
```

Query: `?- reduce_speed.`

## Why the query succeeds

`wet_road` is a fact, so it is true. The rule `slippery :- wet_road.` means slippery
can be derived once wet_road is true, so slippery becomes true. The rule
`reduce_speed :- slippery.` means reduce_speed can be derived once slippery is true,
so reduce_speed is also true. Prolog resolves the query by chaining these rules
backward from `reduce_speed` to `slippery` to `wet_road`, finds `wet_road` as an
established fact, and returns `true.`

## Logical reasoning as a chain of implications

Fact: WetRoad
Rule 1: WetRoad → Slippery
Rule 2: Slippery → ReduceSpeed

WetRoad ⇒ Slippery ⇒ ReduceSpeed

Since WetRoad holds, Slippery holds (Rule 1, modus ponens), and since Slippery
holds, ReduceSpeed holds (Rule 2, modus ponens). Conclusion: ReduceSpeed.
