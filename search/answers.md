AI Laboratory: Search and A*
Answers to Questions 1-29


Question 1: What information is necessary to specify a state?

Only the robot's position (row, col). The map never changes and the robot carries nothing, so the position alone tells us everything that matters for choosing the next move.


Question 2: What makes an action invalid?

An action is invalid if it would move the robot off the edge of the map or into a shelf '#'. Moving into a free cell, S or G is always allowed.


Question 3: Is this a deterministic search problem?

Yes. Each action from a given state always leads to exactly one next state, and the whole map is known in advance.


Question 4: What would constitute a solution?

A sequence of valid actions, for example Right, Right, Right, Right, Down, ..., that takes the robot from S to G. An optimal solution is one with the fewest moves, since every move costs 1.


Question 5: What data structure is used for the A* frontier?

A binary min-heap: a Python list used through heapq.heappush and heapq.heappop. Each entry is a tuple (f, cell).


Question 6: How does the program select the next state to expand?

heappop returns the entry with the smallest f = g + h. If two entries have the same f, Python compares the (row, col) tuples, so the cell with the smaller row (then smaller column) comes first. If the popped cell is already in the closed set, it is an older, more expensive entry and is skipped.


Question 7: Where is the heuristic calculated?

In the inner loop of astar, h(nxt, w.goal) is calculated for a neighbour when a cheaper path to it has just been found, right before it is pushed onto the frontier. It is also calculated once for the start cell when the frontier is created.


Question 8: Does the program explicitly calculate f(n) = g(n) + h(n)?

Yes. The value pushed onto the heap is cost + h(nxt, w.goal), where cost = g[cell] + 1 is g(n) for the neighbour and h gives h(n).


Question 9: How does the program prevent unnecessary repeated exploration?

In two ways. A neighbour is only pushed if the new path to it is cheaper than any found before (cost < g.get(nxt, infinity)). And the closed set records every cell that has been expanded, so each cell is expanded at most once; older copies of it that are still on the heap are skipped when popped.


Question 10: Did both algorithms find a solution?

Yes. On the lab warehouse both BFS and A* found a path from S to G.


Question 11: Did they find paths of the same length?

Yes, both found 40 moves. BFS is optimal because every step costs the same, and A* is optimal because Manhattan distance never overestimates.


Question 12: Which algorithm expanded fewer states?

Neither, both expanded 63 states. The map only has 64 free cells, so both expanded every cell except G. The warehouse is a maze of narrow corridors, and the only way to G winds back and forth: after heading down towards G's row, it has to turn back up and left, away from G, to reach the top row before it can come down the right side to G. So the heuristic keeps pointing the wrong way, and A* ends up trying every dead end, just like BFS.


Question 13: Why might A* expand fewer states?

BFS expands states in order of distance from the start, in every direction. A* expands in order of g + h, so states that are close to the start but far from the goal get a large f and are left on the frontier. When h is a good estimate, A* only expands states near the optimal path. When walls make h misleading, as in the lab warehouse, that advantage disappears.


Question 14: What happens if the heuristic is replaced by h(n) = 0?

A* turns into uniform-cost search, which with unit costs behaves like BFS. It still finds the shortest path (40 on the lab map, 13 on the shelves map I also tested), but it gets no guidance, so it expands the most states: 63 on the lab map and 44 on the shelves map, against 40 for Manhattan.


Question 15: What happens if the heuristic is replaced by Euclidean distance?

It is still admissible, because a straight line is never longer than a path along the grid, so the path is still the shortest (40 and 13). It is never larger than Manhattan distance, so in general it guides the search less well. In my runs it expanded exactly as many states as Manhattan: 63 on the lab map and 40 on the shelves map.


Question 16: What happens if the heuristic is multiplied by 2?

It overestimates the real cost, so it is no longer admissible. On the lab map nothing changed (40 moves, 63 expanded), because there is only one route to G anyway. On the shelves map it expanded far fewer states (22 against 40), but it returned a 17-move path when the shortest is 13. It rushed along the top row because that looked closest to G, and never came back to check the shorter route through the middle. So an overestimating heuristic can make A* faster but no longer guarantees the shortest path.


Question 17: What parts of the generated code were correct immediately?

All of it worked on the first run: reading the map, the moves function with its bounds and wall checks, the four heuristics, the heapq frontier with the closed set, path reconstruction and the BFS version. All four tests in Task 3 passed straight away.


Question 18: Did you find any bugs or design problems?

No bugs showed up in testing: every path was valid, and every length matched the BFS shortest path. One design detail to be aware of is that ties in f are broken by comparing the (row, col) tuples, which is arbitrary. It does not affect correctness, but it can change which of several equally short paths is returned, and how many states are expanded.


Question 19: How did you discover those problems?

By running tests whose answers I knew in advance (the one-step map, the walled-off goal, and the map with an 8-move and a 12-move route), and by checking every A* result against BFS, which always gives the shortest length. I also checked that the number of states expanded was never more than the number of free cells.


Question 20: Did the LLM use terminology or data structures that you did not understand?

No. heapq, deque, dictionaries for g and parent, and a set for the closed list are standard. The one point I had to think through was why the goal test happens when a cell is popped rather than when it is first generated: testing at generation time can return a path before a cheaper one has been found.


Question 21: Did you modify the LLM-generated code?

No. The code was used as generated, because it passed every test and its results matched BFS.


Question 22: Which tests were most useful?

The no-solution test, because it shows the search stops and reports failure instead of looping forever. The alternative-paths test, because a wrong algorithm could still return a valid but longer path. Comparing every result with the BFS shortest path was the most useful check overall.


Question 23: Could you have trusted the program without testing it?

No. A path that looks reasonable is not necessarily correct. The program could return a valid but longer path, or loop forever when there is no solution, and just looking at the output on the lab map would not show either problem. Only the tests with known answers showed that it finds shortest paths and stops when the goal is unreachable.


Question 24: What did you understand about A* that you did not understand before implementing it?

That A* is only as good as its heuristic compared with the actual map. On the lab warehouse it did no better than BFS, because the walls make the straight-line direction misleading. And that admissibility is what makes it optimal: doubling h made it much faster on the shelves map but gave a longer path.


Question 25: Why is it important to formulate the search problem before writing the search algorithm?

The algorithm only works with states, successors, a goal test and costs, so these have to be defined correctly first. If the state or the valid actions are wrong, even a perfect A* will search the wrong problem. Having the formulation first also tells me what to test, for example that walls and edges are never crossed, that every step costs 1, and what the shortest length for a map should be.


Question 26: In what sense is A* an "informed" search algorithm?

It uses extra knowledge about the problem, the heuristic h(n), to estimate how far each state is from the goal. BFS only knows how far a state is from the start. A* orders the frontier by g(n) + h(n), so it can prefer states that seem to lead towards the goal instead of spreading out equally in all directions.


Question 27: Why does the choice of heuristic matter?

It decides both how much work A* does and whether its answer is optimal. With no information (h = 0), A* behaves like BFS and expands the most states. An admissible heuristic close to the true cost, like Manhattan, keeps the path optimal and expands fewer states. One that overestimates (2 x Manhattan) can expand far fewer states but return a longer path, as it did on the shelves map (17 moves instead of 13).


Question 28: What did the LLM contribute to the engineering process?

It turned the problem specification into working Python quickly: reading the map, the moves function, the heapq frontier with g, parent and the closed set, path reconstruction, the BFS version, and the test and experiment scripts. My part was the specification, checking the code against it, running the tests and interpreting the results.


Question 29: What could go wrong if an engineer simply accepted LLM-generated code without testing it?

The code can run and return sensible-looking paths while still being wrong. For example, it could do the goal test too early, forget to update the parent when a cheaper path is found, or use a heuristic that overestimates. All of these return paths that are not the shortest, with no error message. In a real warehouse that means inefficient routes, or collisions if the obstacle check is wrong. Tests with known answers are what catch this.
