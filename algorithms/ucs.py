import time
import heapq


def ucs(problem):
  
    startTime = time.perf_counter()

    startState = problem.initialState()

    counter = 0
    frontier = [(0, counter, startState, [])]

    bestCost = {startState: 0}

    exploredSet = set()   
    exploredList = []     

    generated = 1         
    maxFrontier = 1
    solutionPath = None
    solutionCost = None

    while frontier:
        cost, _, state, path = heapq.heappop(frontier)

        if state in exploredSet:
            continue

        if problem.goalTest(state):
            solutionPath = path
            solutionCost = cost
            break

        exploredSet.add(state)
        exploredList.append(state)

        for test in problem.actions(state):
            child = problem.result(state, test)
            generated += 1
            newCost = cost + problem.stepCost(state, test)

            if child in exploredSet:
                continue
            if child not in bestCost or newCost < bestCost[child]:
                bestCost[child] = newCost
                counter += 1
                heapq.heappush(frontier, (newCost, counter, child, path + [test]))

        maxFrontier = max(maxFrontier, len(frontier))

    return {
        "path": solutionPath,
        "total_cost": solutionCost,
        "nodes_generated": generated,
        "nodes_expanded": len(exploredList),
        "max_frontier": maxFrontier,
        "time": time.perf_counter() - startTime,
        "explored": exploredList,
    }
