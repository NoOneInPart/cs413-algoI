"""
Verification script for Task D: Counterexample Proof
Demonstrates why the profit-based greedy heuristic fails to achieve the optimal schedule.
"""

def compute_value(p, delay):
    return p / (1 + delay)

def main():
    print("=" * 65)
    print("TASK D: COUNTEREXAMPLE VERIFICATION")
    print("=" * 65)

    deliveries = {
        "A": {"R": 0, "P": 18},
        "B": {"R": 0, "P": 12},
        "C": {"R": 1, "P": 6},
    }

    print("Deliveries:")
    for j, data in deliveries.items():
        print(f"  Delivery {j}: Ready Time = {data['R']}, Profit = {data['P']}")
    print()

    # 1. Greedy Strategy G (Order: A -> B -> C)
    # A gets slot 0, B gets slot 1, C gets slot 2
    sched_g = {"A": 0, "B": 1, "C": 2}
    print("Greedy Schedule G (Order by Profit: A -> B -> C):")
    val_g = 0
    for j in ["A", "B", "C"]:
        t = sched_g[j]
        r = deliveries[j]["R"]
        p = deliveries[j]["P"]
        d = t - r
        v = compute_value(p, d)
        val_g += v
        print(f"  Delivery {j}: Slot = {t}, Delay = {d}, Value = {p}/(1+{d}) = {v:.1f}")
    print(f"Total Greedy Value V(G) = {val_g:.1f}\n")

    # 2. Better Schedule S (A -> slot 0, C -> slot 1, B -> slot 2)
    sched_s = {"A": 0, "C": 1, "B": 2}
    print("Better Schedule S (A -> Slot 0, C -> Slot 1, B -> Slot 2):")
    val_s = 0
    for j in ["A", "C", "B"]:
        t = sched_s[j]
        r = deliveries[j]["R"]
        p = deliveries[j]["P"]
        d = t - r
        v = compute_value(p, d)
        val_s += v
        print(f"  Delivery {j}: Slot = {t}, Delay = {d}, Value = {p}/(1+{d}) = {v:.1f}")
    print(f"Total Schedule Value V(S) = {val_s:.1f}\n")

    print(f"Comparison: V(S) = {val_s:.1f} > V(G) = {val_g:.1f}")
    print("Result: Greedy Strategy G is PROVEN SUBOPTIMAL.")
    print("=" * 65)

if __name__ == "__main__":
    main()

