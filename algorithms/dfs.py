import time

def dfs(problem):

    startTime = time.perf_counter()

    start = problem.initialState()
    stack = [(start, [], 0)]

    exploredSet = set()
    exploredList = []

    nodesGenerated = 1
    maxFront = 1
    path, totalCost = None, None

    while stack:
        state, tests, cost = stack.pop()

        if state in exploredSet:
            continue
        if problem.goalTest(state):
            path, totalCost = tests, cost
            break

        exploredSet.add(state)
        exploredList.append(state)

        for test in reversed(problem.actions(state)):
            child = problem.result(state, test)
            nodesGenerated += 1
            if child not in exploredSet:
                stack.append((child, tests + [test], cost + problem.stepCost(state, test)))

        maxFront = max(maxFront, len(stack))

    return {
        "path": path,
        "total_cost": totalCost,
        "nodes_generated": nodesGenerated,
        "nodes_expanded": len(exploredList),
        "max_frontier": maxFront,
        "time": time.perf_counter() - startTime,
        "explored": exploredList,
    }