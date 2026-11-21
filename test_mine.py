from problem import DiagnosticProblem
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ids import ids

# Test 1: problem.py on its own
problem = DiagnosticProblem("Bronchitis")
print("Number of states:", problem.count_states())          # should be 2304
print()

# Test 2: every algorithm on every disease
for disease in problem.diseases:
    patient = DiagnosticProblem(disease)
    for name, algorithm in [("BFS", bfs), ("DFS", dfs), ("IDS", ids)]:
        result = algorithm(patient)
        print(f"{disease:13} {name}  path = {result['path']}  cost = {result['total_cost']}"
              f"  expanded = {result['nodes_expanded']}")
    print()