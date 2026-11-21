import time

def depth_limited_search(problem, limit, stats, exploredList):
    start = problem.initialState()
    stack = [(start, [], 0, 0)]
    reached = {start: 0}
    stats["generated"] += 1
    stats["max_frontier"] = max(stats["max_frontier"], len(stack))

    while stack:
        state, tests, cost, depth = stack.pop()

        if problem.goalTest(state):
            return tests, cost

        if depth == limit:
            continue

        stats["expanded"] += 1
        exploredList.append(state)

        for test in reversed(problem.actions(state)):
            child = problem.result(state, test)
            stats["generated"] += 1
            childDepth = depth + 1
            if child in reached and reached[child] <= childDepth:
                continue
            reached[child] = childDepth
            stack.append((child, tests + [test], cost + problem.stepCost(state, test), childDepth))

        stats["max_frontier"] = max(stats["max_frontier"], len(stack))

    return None

def ids (problem):
    startTime = time.perf_counter()
    stats = {"generated": 0, "expanded": 0, "max_frontier": 0}
    exploredList = []
    path, totalCost = None, None

    for limit in range(13):
        found = depth_limited_search(problem, limit, stats, exploredList)
        if found is not None:
            path, totalCost = found
            break

    return {
        "path": path,
        "total_cost": totalCost,
        "nodes_generated": stats["generated"],
        "nodes_expanded": stats["expanded"],
        "max_frontier": stats["max_frontier"],
        "time": time.perf_counter() - startTime,
        "explored": exploredList,
    }