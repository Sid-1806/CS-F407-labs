AI Laboratory: Agents
Constructing a Goal-Based Agent using a Large Language Model
Answers to Questions 1-9


Question 1: What is the environment?

The warehouse, represented as a 7 x 21 grid. Each square is either free space '.', a shelving unit '#', the loading bay S or the dispatch area G. It is fully observable (the whole map is known), deterministic (a move always has the same result), static (the shelves do not move) and discrete (the vehicle moves one square at a time).


Question 2: What is the goal of the agent?

To get the vehicle from the loading bay S at (1, 1) to the dispatch area G at (1, 19) along a collision-free path, i.e. without ever entering a '#' square or leaving the grid.


Question 3: What actions are available to the agent?

Up, Down, Left and Right, each moving the vehicle one grid square. A move is only allowed if the new square is inside the grid and not a shelf.


Question 4: What information must the agent maintain in order to choose its next action?

Its current position, its model of the map (which squares are free), the goal position, and the plan: the sequence of moves still to carry out. While planning, it also keeps the queue of squares still to explore and, for every square already reached, the square and move it was reached from, so the plan can be rebuilt once G is found.


Question 5: Why is this an example of a goal-based agent rather than a simple reflex agent?

A simple reflex agent chooses each move only from what it currently sees, with rules like "if the square ahead is free, move forward". It has no idea where G is compared with the walls, so it can walk into dead ends or go round in circles. On this map the direct route along the top row is blocked by the shelf at (1, 6), so the vehicle has to go down and around it. A goal-based agent uses its model of the warehouse and its explicit goal to look ahead: it searches for a whole sequence of moves that reaches G, and only then starts moving.


Question 6: Did the LLM generate a working program on the first attempt?

Yes. The program ran without errors on the first attempt. It found a 20-move collision-free path, printed the moves and the squares visited, confirmed that the vehicle finished on G, and drew the path on the map. When I gave it a map where G is walled off, make_plan returned None, which makes the program print that no collision-free path exists.


Question 7: If not, how can you improve your prompt?

It was not needed here. If the program had failed, I would make the prompt more precise: say that a state is a (row, col) tuple, exactly which squares count as free, what a valid move is, and exactly what the program should print. I would also ask for a test case with no possible path, so the "no path" branch gets checked as well.


Question 8: What search algorithm did the LLM choose?

Breadth-first search (BFS). It uses a deque as a first-in first-out queue, and a came_from dictionary that works both as the visited set and for rebuilding the sequence of moves.


Question 9: Why do you think the LLM selected this algorithm?

Every move costs the same, so the grid is an unweighted graph. On an unweighted graph BFS is complete and optimal: the first time it reaches G, it has used the fewest possible moves. It is also the simplest correct choice, with no heuristic or priority queue to get wrong, and it is easy to check, which matters for a vehicle that must not collide. The program's docstring notes that A* with Manhattan distance would also be optimal and would explore fewer squares in a much larger warehouse, but for a map this size BFS is enough.
