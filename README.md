# Pioneer Delivery Company's Algorithm Portfolio
## Part I: Greedy Algorithms
**Course:** CS 413 — Analysis of Algorithms  
**Programming Language:** Python 3 (Python 3.10+)

---

## 1. Overview
Pioneer Delivery is a local delivery company that receives delivery requests requiring driver availability during specific time intervals $[s_i, f_i)$. A driver can only perform one delivery at a time, but if a delivery finishes at time $t$ and another starts at time $t$, the same driver may perform both.

This repository implements the scheduling algorithms for Pioneer Delivery:
- **Task A:** Maximum Deliveries for One Driver ($O(n \log n)$ Interval Scheduling)
- **Task B:** Minimum Number of Drivers ($O(n \log n)$ Interval Partitioning with Min-Heap) *(In progress)*
- **Task C:** Interview-Style Variant / Minimum Rejections ($O(n \log n)$) *(In progress)*
- **Task D:** Theoretical Counterexample Analysis for Profit Scheduling *(In progress)*

---

## 2. Program Organization

```text
cs413_alg/
├── delivery_scheduler.py   # Core data structures (Delivery dataclass), file loader, and Task A scheduler
├── run_task_a_tests.py     # Automated test runner validating Task A required test cases
├── data/
│   ├── sample.csv          # Sample deliveries from project handout (Page 1)
│   ├── task_a/             # Required Test Cases 1–6 for Task A
│   │   ├── test1.csv ... test6.csv
│   │
│   ├── task_b/             # Required Test Cases 1–6 for Task B
│   │   ├── test1.csv ... test6.csv
│   │
│   └── task_c/             # Required Test Cases 1–6 for Task C
│       ├── test1.csv ... test6.csv
└── README.md               # Project documentation and algorithm analysis
```

- **`Delivery` Dataclass**: Models each delivery request with `id` (str), `start` (int), and `finish` (int).
- **`load_deliveries(filepath)`**: Robust parser supporting both CSV files (`id,start,finish`) and whitespace-separated text (`D01 10 13`), safely skipping header rows and comments.
- **`schedule_single_driver(deliveries)`**: Implements the greedy interval scheduling algorithm for Task A.

---

## 3. Input File Format
The program reads delivery requests from files in either CSV or space-delimited text format:

```csv
id,start_time,finish_time
D01,10,13
D02,2,5
D03,4,7
D04,1,8
D05,8,11
D06,11,14
D07,13,16
```

- Delivery IDs are strings (e.g., `D01`, `D1`).
- Start and finish times are integers with $start\_time < finish\_time$.
- Blank lines and lines starting with `#` are ignored.

---

## 4. Instructions for Running

No external dependencies are required (standard Python library only).

### Run Task A on a Specific Input File
```bash
python delivery_scheduler.py data/sample.csv
```
Or with any custom file:
```bash
python delivery_scheduler.py path/to/your_file.csv
```

### Run Task A Test Suite
To automatically execute and verify all required test cases for Task A:
```bash
python run_task_a_tests.py
```

---

## 5. Task A: Maximum Deliveries for One Driver

### 1. What is the greedy choice made by your algorithm?
At each step, among all remaining compatible delivery requests (deliveries whose start time is greater than or equal to the finish time of the last scheduled delivery), the algorithm selects the delivery with the **earliest finish time** ($f_i$).

### 2. Why does this greedy strategy produce an optimal solution?
By always picking the delivery that finishes earliest, we free up the driver as soon as possible, leaving the maximum amount of remaining time open for subsequent deliveries. 

Under the standard **"greedy stays ahead"** property, at every step $i$, the greedy choice finishes no later than the $i$-th delivery of any alternative schedule ($f(g_i) \le f(o_i)$). Because the driver is always freed up at least as early as in any other valid schedule, the greedy algorithm never falls behind and is guaranteed to complete at least as many deliveries as any hypothetical optimal schedule.

### 3. What is the running time of your algorithm?
- **Sorting:** Sorting $n$ deliveries by finish time takes **$O(n \log n)$** time using Python's Timsort.
- **Linear Scan:** Iterating once through the sorted deliveries and checking compatibility (`start >= last_finish_time`) takes **$O(n)$** time.
- **Total Running Time:** **$O(n \log n)$**, satisfying the project requirements.

### Required Test Case Results (Task A)

| Test | Input Delivery Intervals | Expected Max | Actual Output | Status |
| :---: | :--- | :---: | :--- | :---: |
| **1** | No deliveries | 0 | `0` (None) | **PASS** |
| **2** | `(1, 3)` | 1 | `1` [D1: (1, 3)] | **PASS** |
| **3** | `(1, 3), (3, 5), (5, 7)` | 3 | `3` [D1: (1, 3), D2: (3, 5), D3: (5, 7)] | **PASS** |
| **4** | `(1, 5), (2, 6), (3, 7)` | 1 | `1` [D1: (1, 5)] | **PASS** |
| **5** | `(5, 7), (1, 3), (3, 5), (2, 4)` | 3 | `3` [D2: (1, 3), D3: (3, 5), D1: (5, 7)] | **PASS** |
| **6** | `(1, 4), (2, 4), (4, 6)` | 2 | `2` [D1: (1, 4), D3: (4, 6)] | **PASS** |
