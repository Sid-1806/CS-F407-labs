"""
Task 6: Investigate the heuristic.

    Manhattan       |dr| + |dc|            admissible
    h(n) = 0        0                      admissible (A* = uniform-cost search)
    Euclidean       sqrt(dr^2 + dc^2)      admissible, but weaker than Manhattan
    2 x Manhattan   2(|dr| + |dc|)         overestimates -> not admissible

The lab warehouse is one long winding corridor, so a second map with open
floor and a few shelves is also used, where the heuristics can disagree.
"""

from warehouse import Warehouse, astar, bfs, manhattan, zero, euclidean, twice_manhattan, LAB_MAP

SHELVES = """
###########
#S........#
#..#......#
##...#.##.#
#.....#...#
##......###
#........G#
###########
"""

HEURISTICS = [("Manhattan", manhattan), ("h(n) = 0", zero),
              ("Euclidean", euclidean), ("2 x Manhattan", twice_manhattan)]

for name, ascii_map in [("Lab warehouse", LAB_MAP), ("Shelves map", SHELVES)]:
    w = Warehouse(ascii_map)
    optimal = len(bfs(w)[0]) - 1
    print(f"{name} (shortest possible path: {optimal})")
    print(f"  {'Heuristic':<15}{'Found':>7}{'Length':>8}{'Expanded':>10}")
    for label, h in HEURISTICS:
        path, expanded = astar(w, h)
        print(f"  {label:<15}{'yes' if path else 'no':>7}{len(path) - 1 if path else '-':>8}{expanded:>10}")
    print()

w = Warehouse(SHELVES)
for label, h in [("Manhattan", manhattan), ("2 x Manhattan", twice_manhattan)]:
    path, _ = astar(w, h)
    print(f"Shelves map, path with {label} ({len(path) - 1} moves):")
    w.draw(path)
