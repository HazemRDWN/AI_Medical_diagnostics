import importlib
from pathlib import Path

import numpy as np
import pandas as pd

from problem import DiagnosticProblem

dataDir = Path(__file__).parent / "data"

#______________Filling CSV with the necessary data______________

tests = [
    ("T1",  "Temperature check",             5,   1, ""),
    ("T2",  "Throat swab (strep test)",      25,  1, ""),
    ("T3",  "Rapid COVID test",              30,  1, ""),
    ("T4",  "Rapid flu test",                35,  1, ""),
    ("T5",  "Chest X-ray",                   80,  3, ""),
    ("T6",  "Blood test",                    50,  2, ""),
    ("T7",  "Breathing test",                70,  2, "T9"),
    ("T8",  "Allergy skin test",             60,  2, ""),
    ("T9",  "Oxygen level check",            12,  1, ""),
    ("T10", "Mucus sample test",             40,  2, ""),
    ("T11", "Runny nose and sneezing check", 8,   1, ""),
    ("T12", "CT scan",                       200, 5, "T5"),
]

testOrder = [t[0] for t in tests]

results = {
    "Common Cold":  ["no fever", "negative", "negative", "negative", "normal",   "normal", "normal",  "negative", "normal", "clear",     "yes", "normal"],
    "Flu":          ["fever",    "negative", "negative", "positive", "normal",   "normal", "normal",  "negative", "normal", "clear",     "no",  "normal"],
    "COVID-19":     ["fever",    "negative", "positive", "negative", "normal",   "normal", "normal",  "negative", "normal", "clear",     "no",  "abnormal"],
    "Strep Throat": ["fever",    "positive", "negative", "negative", "normal",   "high",   "normal",  "negative", "normal", "clear",     "no",  "normal"],
    "Bronchitis":   ["no fever", "negative", "negative", "negative", "normal",   "normal", "reduced", "negative", "normal", "infection", "no",  "normal"],
    "Pneumonia":    ["fever",    "negative", "negative", "negative", "abnormal", "high",   "normal",  "negative", "low",    "infection", "no",  "abnormal"],
    "Asthma":       ["no fever", "negative", "negative", "negative", "normal",   "normal", "reduced", "positive", "low",    "clear",     "no",  "normal"],
    "Allergies":    ["no fever", "negative", "negative", "negative", "normal",   "normal", "normal",  "positive", "normal", "clear",     "yes", "normal"],
}

def writeDataFiles():

    dataDir.mkdir(exist_ok=True)

    #tests.csv
    testsTable = pd.DataFrame(
        tests,
        columns=["test_id", "name", "financial_cost", "risk_cost", "prerequisites"],
    )
    testsTable.to_csv(dataDir / "tests.csv", index=False)

    resultsTable = pd.DataFrame.from_dict(results, orient="index", columns=testOrder)
    resultsTable.index.name = "disease"
    resultsTable.to_csv(dataDir / "disease_results.csv")

#_______________Running the algorithms_______________

patientCases = ["Common Cold", "Bronchitis", "Asthma", "Allergies", "COVID-19"]

algorithmFiles = ["bfs", "dfs", "ucs", "ids"]

iterations = 5

plotCase = "Bronchitis"

def loadAlgorithm():

    algorithms = {}

    for name in algorithmFiles:

        moduleName = f"algorithms.{name}"
        module = importlib.import_module(moduleName)
        algorithms[name.upper()] = getattr(module, name)

    return algorithms

def run_algorithm(algorithm, problem):

    times = []
    for iterationIndex in range(iterations):
        result = algorithm(problem)
        times.append(result["time"])
    result["time"] = float(np.mean(times))
    return result


def run_experiments():
    algorithms = loadAlgorithm()
    if not algorithms:
        print("Algorithms not loaded yet")
        return

    #Problem size
    firstProblem = DiagnosticProblem(patientCases[0])
    print(f"\nNumber of reachable states: {firstProblem.count_states()}")
    print("\nTests:")
    for testId, name in firstProblem.test_names.items():
        print(f"  {testId} = {name} (cost {firstProblem.step_costs[testId]})")

    #Run every algorithm on every patient case
    rows = []
    plotResults = {}
    for case in patientCases:
        problem = DiagnosticProblem(case)
        for name, algorithm in algorithms.items():
            result = run_algorithm(algorithm, problem)
            path = result["path"]
            rows.append({
                "case": case,
                "algorithm": name,
                "path": " > ".join(path),
                "tests": len(path),
                "total_cost": result["total_cost"],
                "generated": result["nodes_generated"],
                "expanded": result["nodes_expanded"],
                "max_frontier": result["max_frontier"],
                "time_ms": result["time"] * 1000,
            })
            if case == plotCase:
                plotResults[name] = result

    table = pd.DataFrame(rows)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)

    print("\nResults for every case:\n")
    print(table.round({"time_ms": 3}).to_string(index=False))

    print("\nAverage over all cases:\n")
    summary = table.groupby("algorithm")[
        ["tests", "total_cost", "generated", "expanded", "max_frontier", "time_ms"]
    ].mean()
    print(summary.round(2).to_string())