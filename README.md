# AI-Based Medical Diagnostics (Phase I)

CSAI 301 – Artificial Intelligence, Zewail City

A patient has one of 8 possible diseases, and we don't know which. There are 12 medical tests; each test result rules out some diseases, some tests need another test first, and every test has a cost. We model this as a search problem and solve it with four uninformed search algorithms written from scratch: **BFS, DFS, UCS and IDS**. The goal is a sequence of tests that leaves exactly one disease, and the algorithms are compared on the solutions they find and the work they do.

No search libraries are used. Pandas, NumPy, Matplotlib and NetworkX are used only for data, tables and plots.

## Requirements

- Python 3.10 or newer
- pandas, numpy, matplotlib

Install the libraries once:

```
pip install pandas numpy matplotlib
```

## How to run

From the project folder:

```
python main.py
```

This will:

1. Write the two data files in `data/` (`tests.csv` and `disease_results.csv`).
2. Print the number of reachable states (2,304) and the list of tests with their costs.
3. Run all four algorithms on five patient cases (Common Cold, Bronchitis, Asthma, Allergies, COVID-19), with each run repeated 5 times to average the running time.
4. Print a results table (one row per algorithm and case) and a table of averages per algorithm.
5. Save the figures to the `figures/` folder.

Running times change slightly from run to run; all other numbers are always the same.

## Project structure

```
AI_Medical_diagnostics/
├── README.md
├── main.py
├── problem.py
├── visualization.py
├── data/
│   ├── tests.csv
│   └── disease_results.csv
├── algorithms/
│   ├── bfs.py
│   ├── dfs.py
│   ├── ucs.py
│   └── ids.py
└── figures/
```