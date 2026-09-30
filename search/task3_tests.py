"""
Task 3: Test the generated program.

Each A* result is compared with what we expect and with BFS, which always
returns a shortest path when every move costs 1.
"""

from warehouse import Warehouse, astar, bfs, show, LAB_MAP

TRIVIAL = """
#####
#SG##
#####
"""

NO_SOLUTION = """
#######
#S....#
###.###
#...#G#
#######
"""

# Two routes: along the top (8 moves) or around the bottom (12 moves)
TWO_ROUTES = """
###########
#S.......G#
#.#######.#
#.........#
###########
"""

TESTS = [
    ("Test 1: original warehouse", LAB_MAP, 40),
    ("Test 2: trivial case", TRIVIAL, 1),
    ("Test 3: no solution", NO_SOLUTION, None),
    ("Test 4: alternative paths", TWO_ROUTES, 8),
]

for label, ascii_map, expected in TESTS:
    w = Warehouse(ascii_map)
    path, expanded = astar(w)
    show(label, w, path, expanded)

    length = None if path is None else len(path) - 1
    bfs_path, _ = bfs(w)
    bfs_length = None if bfs_path is None else len(bfs_path) - 1
    verdict = "PASS" if length == expected == bfs_length else "FAIL"
    print(f"  expected {expected}, BFS gives {bfs_length} -> {verdict}\n")
