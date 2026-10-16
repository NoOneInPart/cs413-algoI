# Pioneer Delivery Company's Algorithm Portfolio
## Part I: Greedy Algorithms
**Course:** CS 413 — Analysis of Algorithms  
**Programming Language:** Python 3 (Python 3.10+)

---

## 1. Overview
Pioneer Delivery is a local delivery company that receives delivery requests requiring driver availability during specific time intervals $[s_i, f_i)$. A driver can only perform one delivery at a time, but if a delivery finishes at time $t$ and another starts at time $t$, the same driver may perform both.

This repository implements the scheduling algorithms for Pioneer Delivery:
- **Task A:** Maximum Deliveries for One Driver ($O(n \log n)$ Interval Scheduling)
- **Task B:** Minimum Number of Drivers ($O(n \log n)$ Interval Partitioning with Min-Heap)
- **Task C:** Interview-Style Variant / Minimum Rejections ($O(n \log n)$)
- **Task D:** Theoretical Counterexample Analysis for Profit Scheduling

---

## 2. Program Organization

```text
cs413_alg/
├── delivery_scheduler.py   # Core data structures, file loader, Tasks A, B, and C schedulers
├── run_task_a_tests.py     # Automated test runner validating Task A required test cases
├── run_task_b_tests.py     # Automated test runner validating Task B required test cases
├── run_task_c_tests.py     # Automated test runner validating Task C required test cases
├── verify_task_d.py        # Verification script for Task D counterexample
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
- **`schedule_multiple_drivers(deliveries)`**: Implements interval partitioning with a min-heap for Task B.
- **`find_min_rejections(deliveries)`**: Computes the minimum deliveries to reject ($n - k$) for Task C.

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

### Run Task Suites
To automatically execute and verify all required test cases and analyses:
```bash
python run_task_a_tests.py   # Runs Task A tests 1-6
python run_task_b_tests.py   # Runs Task B tests 1-6
python run_task_c_tests.py   # Runs Task C tests 1-6
python verify_task_d.py      # Verifies Task D counterexample values
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

---

## 6. Task B: Minimum Number of Drivers

### 1. What information is stored in the priority queue?
The priority queue (min-heap) stores tuples of the form `(driver_finish_time, driver_id)`. 
- `driver_finish_time` is the completion time of the last delivery assigned to that driver.
- The min-heap property ensures that the driver who becomes available earliest is always at the top (`heap[0]`).

### 2. How is a driver selected for each new delivery?
Deliveries are processed in ascending order of their start times:
1. For each delivery, we inspect the driver at the top of the min-heap.
2. **If that driver finishes at or before the current delivery's start time** (`finish_time <= delivery.start`), that driver is free. We pop them from the heap, assign the current delivery to them, and push them back with their updated finish time.
3. **If that driver is still busy** (`finish_time > delivery.start`), then *all* active drivers are currently occupied. We hire a new driver, assign the delivery, and push the new driver into the heap.

### 3. Why does this algorithm use the minimum possible number of drivers?
Let $d$ be the maximum number of mutually overlapping deliveries at any single point in time (known as the **depth** of the interval set). Clearly, no valid schedule can ever use fewer than $d$ drivers because all $d$ deliveries must be handled concurrently.

The greedy algorithm only allocates a new driver (say, driver $k$) when all existing $k-1$ drivers are busy with deliveries that overlap the start time of the current delivery. This means at that exact moment, there are $k$ mutually overlapping deliveries. Therefore, the algorithm never allocates more drivers than the depth $d$. Since $\text{drivers used} = d \le \text{optimal drivers}$, the number of drivers used is guaranteed to be minimal.

### 4. What is the running time?
- **Sorting:** Sorting $n$ deliveries by start time takes **$O(n \log n)$** time.
- **Heap Operations:** For each of the $n$ deliveries, we perform at most one `heappop` and one `heappush` on a min-heap containing at most $d \le n$ drivers. Each heap operation takes $O(\log d) \le O(\log n)$ time. Total heap time across all deliveries is $O(n \log d) \le O(n \log n)$.
- **Total Running Time:** **$O(n \log n)$**, satisfying the project requirements.

### Required Test Case Results (Task B)

| Test | Input Delivery Intervals | Expected Drivers | Actual Drivers | Schedule Assignment | Status |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **1** | No deliveries | 0 | 0 | None | **PASS** |
| **2** | `(1, 3)` | 1 | 1 | Driver 1: `D1` | **PASS** |
| **3** | `(1, 3), (3, 5), (5, 7)` | 1 | 1 | Driver 1: `D1 D2 D3` | **PASS** |
| **4** | `(1, 5), (2, 6), (3, 7)` | 3 | 3 | Driver 1: `D1`<br>Driver 2: `D2`<br>Driver 3: `D3` | **PASS** |
| **5** | `(1, 4), (2, 5), (4, 7), (5, 8)` | 2 | 2 | Driver 1: `D1 D3`<br>Driver 2: `D2 D4` | **PASS** |
| **6** | `(5, 8), (1, 4), (2, 5), (4, 6), (6, 9)` | 2 | 2 | Driver 1: `D2 D4 D5`<br>Driver 2: `D3 D1` | **PASS** |

---

## 7. Task C: Interview-Style Variant (Min Rejections)

### 1. How is this problem related to Task A?
Task C is the mathematical complement of Task A:
- In **Task A**, the goal is to maximize the number of compatible deliveries ($k$) that a single driver can complete without overlap.
- In **Task C**, any delivery not chosen in that compatible set creates a conflict and must be rejected.
- Because every non-selected delivery must be rejected to ensure all remaining deliveries are mutually compatible, minimizing the number of rejected deliveries is strictly equivalent to maximizing the number of compatible deliveries kept.

### 2. If the maximum number of compatible deliveries is $k$, how many deliveries must be rejected?
Exactly **$n - k$** deliveries must be rejected (where $n$ is the total number of delivery requests).
- Keeping more than $k$ deliveries is impossible without introducing overlaps (by definition of $k$ as the maximum compatible set).
- Thus, rejecting the remaining $n - k$ deliveries leaves a valid, conflict-free schedule while discarding the absolute minimum number of requests.

### 3. What is the running time of your algorithm?
- **Sorting & Selection (Task A):** Sorting $n$ deliveries by finish time takes **$O(n \log n)$**, followed by an **$O(n)$** linear pass to pick the $k$ compatible deliveries.
- **Set Difference:** Identifying the $n - k$ rejected deliveries takes **$O(n)$** using a set of accepted IDs.
- **Total Running Time:** **$O(n \log n)$**, matching the $O(n \log n)$ optimal bound for LeetCode 435 (*Non-overlapping Intervals*).

### Required Test Case Results (Task C)

| Test | Input Delivery Intervals | Total ($n$) | Expected Rejected | Actual Rejected | Rejected Deliveries | Status |
| :---: | :--- | :---: | :---: | :---: | :--- | :---: |
| **1** | No deliveries | 0 | 0 | 0 | None | **PASS** |
| **2** | `(1, 3)` | 1 | 0 | 0 | None | **PASS** |
| **3** | `(1, 3), (3, 5), (5, 7)` | 3 | 0 | 0 | None | **PASS** |
| **4** | `(1, 5), (2, 6), (3, 7)` | 3 | 2 | 2 | `D2(2,6), D3(3,7)` | **PASS** |
| **5** | `(5, 7), (1, 3), (3, 5), (2, 4)` | 4 | 1 | 1 | `D4(2,4)` | **PASS** |
| **6** | `(1, 2), (2, 3), (3, 4), (1, 3)` | 4 | 1 | 1 | `D4(1,3)` | **PASS** |

---

## 8. Task D: When a Greedy Choice Fails (Counterexample)

In this variant, flexible same-day deliveries each require 1 unit of driver time. Each delivery $j$ has a ready time $R_j \ge 0$ and distinct profit $P_j > 0$. If delivery $j$ is scheduled in integer time slot $T_j(S) \ge R_j$, its delay is $D_j(S) = T_j(S) - R_j$, yielding value:

$$V_j(S) = \frac{P_j}{1 + D_j(S)}$$

A proposed greedy strategy $G$ processes deliveries in **decreasing order of profit** and assigns each to the **earliest available slot at or after its ready time**.

Below is a simple 3-delivery counterexample proving that this greedy strategy is not always optimal.

---

### 1. Delivery Ready Times and Profits

| Delivery | Ready Time ($R_j$) | Profit ($P_j$) |
| :---: | :---: | :---: |
| **A** | 0 | 18 |
| **B** | 0 | 12 |
| **C** | 1 | 6 |

*(Note: All profits are distinct: $18 \ne 12 \ne 6 > 0$, and all ready times are nonnegative integers).*

---

### 2. Schedule Produced by Greedy Strategy $G$ and $V(G)$

Greedy processes deliveries in order of decreasing profit: **A ($P=18$) $\rightarrow$ B ($P=12$) $\rightarrow$ C ($P=6$)**:

1. **Delivery A:** Earliest available slot at or after $R_A = 0$ is **Slot 0**.
   - Slot: $T_A(G) = 0$
   - Delay: $D_A = 0 - 0 = 0$
   - Value: $V_A = \frac{18}{1 + 0} = 18$
2. **Delivery B:** Earliest available slot at or after $R_B = 0$ is **Slot 1** (slot 0 is occupied).
   - Slot: $T_B(G) = 1$
   - Delay: $D_B = 1 - 0 = 1$
   - Value: $V_B = \frac{12}{1 + 1} = 6$
3. **Delivery C:** Earliest available slot at or after $R_C = 1$ is **Slot 2** (slot 1 is occupied).
   - Slot: $T_C(G) = 2$
   - Delay: $D_C = 2 - 1 = 1$
   - Value: $V_C = \frac{6}{1 + 1} = 3$

$$\mathbf{V(G)} = 18 + 6 + 3 = \mathbf{27}$$

---

### 3. A Better Schedule $S$ and $V(S)$

Consider an alternative schedule $S$ that assigns the slots as follows:

1. **Delivery A** $\rightarrow$ **Slot 0**:
   - Delay: $D_A = 0 - 0 = 0$
   - Value: $V_A = \frac{18}{1 + 0} = 18$
2. **Delivery C** $\rightarrow$ **Slot 1**:
   - Delay: $D_C = 1 - 1 = 0$
   - Value: $V_C = \frac{6}{1 + 0} = 6$
3. **Delivery B** $\rightarrow$ **Slot 2**:
   - Delay: $D_B = 2 - 0 = 2$
   - Value: $V_B = \frac{12}{1 + 2} = 4$

All constraints are satisfied ($T_j \ge R_j$ and no two deliveries share a slot).

$$\mathbf{V(S)} = 18 + 6 + 4 = \mathbf{28}$$

---

### 4. Why This Proves $G$ Is Not Always Optimal

Since $\mathbf{V(S) = 28 > 27 = V(G)}$, schedule $S$ produces strictly greater total value than greedy strategy $G$.

**Intuitive Explanation:**
- Greedy chooses delivery $B$ before $C$ solely because $P_B (12) > P_C (6)$. By greedily taking slot 1 for $B$, it delays $B$ by 1 time unit (reducing its value from 12 to 6) **and** crowds out $C$, forcing $C$ into slot 2 with a delay of 1 (reducing its value from 6 to 3).
- In contrast, schedule $S$ gives slot 1 to $C$ right when it is ready ($D_C = 0$), capturing $C$'s full value of $6$ (a $+3$ gain over greedy). Delaying $B$ to slot 2 only drops $B$'s value from $6$ to $4$ (a $-2$ loss).
- The net benefit of letting $C$ take slot 1 is $+3 - 2 = +1$.
- Because greedy looks only at raw profit rather than how delays impact the marginal rate of return across competing requests, it makes a locally attractive choice that damages the global objective. Hence, $G$ is not always optimal.

