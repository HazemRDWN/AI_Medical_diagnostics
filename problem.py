import pandas as pd
from pathlib import Path

dataDir = Path(__file__).parent / "data"

class DiagnosticProblem:
    def __init__(self, trueDisease):
        self.trueDisease = trueDisease

        testsTable = pd.read_csv(dataDir / "tests.csv").fillna("")
        self.resultsTable = pd.read_csv(dataDir / "disease_results.csv", index_col="disease")

        self.testIds = list(testsTable["test_id"])
        self.diseases = list(self.resultsTable.index)
        self.test_names = {}
        self.step_costs = {}
        self.prerequisites = {}

        for _, row in testsTable.iterrows():
            testId = row["test_id"]
            self.test_names[testId] = row["name"]
            self.step_costs[testId] = row["financial_cost"] + 10 * row["risk_cost"]
            if row["prerequisites"] == "":
                self.prerequisites[testId] = []
            else:
                self.prerequisites[testId] = row["prerequisites"].split(";")

    def initialState(self):
        return (frozenset(), frozenset(self.diseases))

    def goalTest(self, state):
        testsDone, possibleDiseases = state
        return len(possibleDiseases) == 1

    def actions(self, state):
        testsDone, possibleDiseases = state
        allowed = []

        for test in self.testIds:
            if test in testsDone:
                continue

            prerequisitesDone = all(p in testsDone for p in self.prerequisites[test])
            if prerequisitesDone:
                allowed.append(test)

        return allowed

    def result(self, state, test):
        testsDone, possibleDiseases = state
        patientAnswer = self.resultsTable.at[self.trueDisease, test]

        remaining = set()
        for disease in possibleDiseases:
            if self.resultsTable.at[disease, test] == patientAnswer:
                remaining.add(disease)
        return (testsDone | {test}, frozenset(remaining))

    def stepCost(self, state, test):
        return self.step_costs[test]

    def count_states(self):
        start = frozenset()
        seen = {start}
        stack = [start]

        while stack:
            testsDone = stack.pop()
            for test in self.testIds:
                if test in testsDone:
                    continue
                if all(p in testsDone for p in self.prerequisites[test]):
                    newSet = testsDone | {test}
                    if newSet not in seen:
                        seen.add(newSet)
                        stack.append(newSet)
        return len(seen)