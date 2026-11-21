import time

from collections import deque

def bfs(problem):

    startTime = time.perf_counter()

    startState = problem.initialState()

    # Each frontier entry such as state, list of tests so far, cost so far
    opened = deque([(startState, [], 0)])

    seen = {startState}

    closed = []

    generated = 1

    maxOpened = 1

    solutionPath = None

    solutionCost = None

    while opened:

        state, path, cost = opened.popleft()

        if problem.goalTest(state):

            solutionPath = path
            solutionCost = cost

            break

        closed.append(state)

        for test in problem.actions(state):

            newState = problem.result(state, test)
            generated += 1

            if newState not in seen:

                seen.add(newState)
                opened.append((newState, path + [test], cost + problem.stepCost(state, test)))

                maxOpened = max(maxOpened, len(opened))

    return {
        "path": solutionPath,
        "total_cost": solutionCost,
        "nodes_generated": generated,
        "nodes_expanded": len(closed),
        "max_frontier": maxOpened,
        "time": time.perf_counter() - startTime,
        "explored": closed,
    }
