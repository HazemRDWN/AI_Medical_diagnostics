from pathlib import Path
import pandas as pd

#______________Filling CSV with necessary data______________

DATA_DIR = Path(__file__).parent / "data"

TESTS = [
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

TEST_ORDER = [t[0] for t in TESTS]

RESULTS = {
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

    DATA_DIR.mkdir(exist_ok=True)

    # tests.csv
    tests_table = pd.DataFrame(
        TESTS,
        columns=["test_id", "name", "financial_cost", "risk_cost", "prerequisites"],
    )
    tests_table.to_csv(DATA_DIR / "tests.csv", index=False)

    results_table = pd.DataFrame.from_dict(RESULTS, orient="index", columns=TEST_ORDER)
    results_table.index.name = "disease"
    results_table.to_csv(DATA_DIR / "disease_results.csv")

if __name__ == "__main__":
    writeDataFiles()
    print("Data files written to", DATA_DIR)