from pathlib import Path

import matplotlib
matplotlib.use("Agg")         
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

figuresDir = Path(__file__).parent / "figures"

algorithmColors = {"BFS": "#4C72B0", "DFS": "#DD8452", "UCS": "#55A868", "IDS": "#C44E52"}


def path_states(problem, path):

    state = problem.initialState()
    states = [state]
    for test in path:
        state = problem.result(state, test)
        states.append(state)
    return states


def layout_by_depth(states):

    rows = {}
    for state in states:
        testsDone, _ = state
        rows.setdefault(len(testsDone), []).append(state)

    positions = {}
    for depth, rowStates in rows.items():
        rowStates.sort(key=lambda s: sorted(s[0]))
        count = len(rowStates)
        for i, state in enumerate(rowStates):
            x = 0.5 if count == 1 else i / (count - 1)
            positions[state] = (x, -depth)
    return positions


# Figure 1: explored states of one algorithm

def draw_explored_states(result, problem, algorithmName, ax):

    expandedOrder = list(dict.fromkeys(result["explored"]))

    solution = path_states(problem, result["path"]) if result["path"] else []

    allStates = list(dict.fromkeys(expandedOrder + solution))
    positions = layout_by_depth(allStates)

    xs = [positions[s][0] for s in expandedOrder]
    ys = [positions[s][1] for s in expandedOrder]
    dots = ax.scatter(xs, ys, c=range(len(expandedOrder)), cmap="viridis",
                      s=25, zorder=2)

    if solution:
        px = [positions[s][0] for s in solution]
        py = [positions[s][1] for s in solution]
        ax.plot(px, py, color="red", linewidth=2, zorder=3)
        ax.scatter(px, py, color="red", s=60, zorder=4)
        for test, (x, y) in zip(result["path"], zip(px[1:], py[1:])):
            ax.annotate(test, (x, y), textcoords="offset points", xytext=(6, 4),
                        fontsize=8, color="red")

        goalX, goalY = px[-1], py[-1]
        disease = next(iter(solution[-1][1]))
        ax.scatter([goalX], [goalY], marker="*", s=250, color="gold",
                   edgecolors="black", zorder=5)
        ax.annotate(disease, (goalX, goalY), textcoords="offset points",
                    xytext=(8, -12), fontsize=8, fontweight="bold")

    maxDepth = max(len(s[0]) for s in allStates)
    ax.set_yticks([-d for d in range(maxDepth + 1)])
    ax.set_yticklabels([str(d) for d in range(maxDepth + 1)])
    ax.set_ylabel("tests performed")
    ax.set_xticks([])
    ax.set_xlim(-0.08, 1.08)
    expandedText = f"{result['nodes_expanded']} expanded"
    if len(expandedOrder) != result["nodes_expanded"]:
        expandedText += f" ({len(expandedOrder)} unique shown)"
    ax.set_title(f"{algorithmName}: {expandedText}, cost {result['total_cost']}",
                 fontsize=10)
    return dots


def plot_explored_states(plotResults, problem, filename="explored_states.png"):

    figuresDir.mkdir(exist_ok=True)
    names = list(plotResults)
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))

    for ax, name in zip(axes.flat, names):
        dots = draw_explored_states(plotResults[name], problem, name, ax)
        bar = fig.colorbar(dots, ax=ax, fraction=0.04)
        bar.set_label("expansion order", fontsize=8)
        bar.locator = MaxNLocator(integer=True)   # whole numbers only
        bar.update_ticks()
    for ax in list(axes.flat)[len(names):]:
        ax.axis("off")

    fig.suptitle(f"Explored states, patient with {problem.trueDisease} "
                 f"(red = solution path)", fontsize=13)
    fig.tight_layout()
    outPath = figuresDir / filename
    fig.savefig(outPath, dpi=150)
    plt.close(fig)
    return outPath


# Figure 2: bar charts comparing the algorithms

def plot_comparison(table, filename="comparison.png"):

    figuresDir.mkdir(exist_ok=True)
    metrics = [
        ("total_cost", "Total cost of tests"),
        ("expanded", "Nodes expanded"),
        ("generated", "Nodes generated"),
        ("max_frontier", "Max frontier size"),
        ("time_ms", "Time (ms)"),
    ]
    cases = list(dict.fromkeys(table["case"]))
    algorithms = list(dict.fromkeys(table["algorithm"]))
    barWidth = 0.8 / len(algorithms)

    fig, axes = plt.subplots(len(metrics), 1, figsize=(11, 3.2 * len(metrics)))

    for ax, (column, title) in zip(axes, metrics):
        values = table.pivot(index="case", columns="algorithm", values=column)
        for i, alg in enumerate(algorithms):
            xs = [c + i * barWidth for c in range(len(cases))]
            ax.bar(xs, values.loc[cases, alg], width=barWidth, label=alg,
                   color=algorithmColors.get(alg))
        ax.set_xticks([c + barWidth * (len(algorithms) - 1) / 2
                       for c in range(len(cases))])
        ax.set_xticklabels(cases)
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.3)

    axes[0].legend(ncol=len(algorithms), loc="upper right")
    fig.tight_layout()
    outPath = figuresDir / filename
    fig.savefig(outPath, dpi=150)
    plt.close(fig)
    return outPath
