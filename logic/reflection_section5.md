# Section 5: Reflection Questions

**1. Why is it useful to specify action preconditions and effects before asking an
LLM to write the planner?**
It turns a vague request ("write a planner") into a precise, checkable
specification. With preconditions/effects nailed down first, you know exactly what
correct behavior looks like and can verify the generated code against that
spec, rather than trusting whatever the LLM decides "a planner" should do.

**2. Give an example of an error that could occur if the planner failed to check
an action's preconditions.**
If `Drop(Package,C)` were applied without checking `Holding(Package)`, the planner
could "drop" a package the robot was never carrying — e.g. adding `At(Package,C)`
to the state while the package is still validly at A, producing a state where the
package is impossibly in two places, or a plan that looks like it reached the goal
without ever actually transporting anything.

**3. Why is a plan that "looks reasonable" not necessarily a valid plan?**
A plan can be structurally plausible in natural language (move here, pick up,
move there, drop) while silently skipping a step whose precondition wasn't
actually satisfied at that point in the state sequence — e.g. dropping before
picking up, or moving to a location with no connecting edge. Only checking each
action's preconditions against the actual state immediately before it (not just
"does the story make sense") confirms validity.

**4. What did the LLM contribute to the implementation?**
The boilerplate translation of the specification into working code: the `Action`
class, the applicability/apply logic, the BFS loop with a visited set and parent
back-pointers for plan reconstruction, and the print formatting — i.e., the
mechanical engineering of turning a precise spec into runnable Python quickly.

**5. What did you have to verify independently?**
That `applicable`/`apply` actually implement the stated precondition/effect
semantics correctly (Task 3's tests A–C), that BFS finds the shortest plan and
correctly reports failure when none exists, and — per Task 5 — that the LLM's own
natural-language explanation of a plan matches what the code actually computes,
rather than trusting the explanation at face value.

**6. In this laboratory, where is logical reasoning being used?**
In deciding whether an action's preconditions are entailed by the current state
(S ⊨ Preconditions(a)), in computing the successor state via the effects, and in
testing whether a state entails the goal (S ⊨ G). Also, in Section 7, in Prolog's
fact/rule resolution (e.g. `connected(X,Y)` → `can_move(X,Y)`) used as an
independent check on the Python-generated plan.

**7. How is planning related to the search algorithms studied in the previous
module?**
Planning is search over a state graph where edges are the domain's actions:
generating successors corresponds to applying applicable actions, and BFS explores
this graph exactly as it would explore any other graph, guaranteeing a
shortest-length plan when uninformed search is used. The novelty here is that the
graph is not given explicitly — it is generated on the fly by logical evaluation
of preconditions/effects at each state, which is what "Logic + Search = Planning"
means.
