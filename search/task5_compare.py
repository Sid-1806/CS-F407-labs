"""
Task 5: A* versus blind search (BFS) on the same, unchanged warehouse.
"""

from warehouse import Warehouse, astar, bfs, LAB_MAP

w = Warehouse(LAB_MAP)
results = {"BFS": bfs(w), "A*": astar(w)}

print(f"Lab warehouse ({w.free_cells()} free cells)")
print(f"  {'Measure':<17}{'BFS':>6}{'A*':>6}")
print(f"  {'Solution found':<17}" + "".join(f"{'yes' if p else 'no':>6}" for p, _ in results.values()))
print(f"  {'Path length':<17}" + "".join(f"{len(p) - 1 if p else '-':>6}" for p, _ in results.values()))
print(f"  {'States expanded':<17}" + "".join(f"{e:>6}" for _, e in results.values()))
