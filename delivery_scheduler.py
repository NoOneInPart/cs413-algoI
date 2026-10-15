"""
Pioneer Delivery Company - Scheduling System
CS 413: Analysis of Algorithms - Portfolio Part I
"""

from dataclasses import dataclass
import heapq
import sys


@dataclass
class Delivery:
    id: str
    start: int
    finish: int

    def __str__(self):
        return f"{self.id} ({self.start}, {self.finish})"


def load_deliveries(filepath: str) -> list[Delivery]:
    """
    Reads delivery requests from a file.
    Supports both comma-separated (.csv) and whitespace-separated text files.
    Skips headers and blank lines.
    """
    deliveries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines or comments
            if not line or line.startswith("#"):
                continue

            # Determine delimiter: comma if present, else whitespace
            parts = line.split(",") if "," in line else line.split()

            # Skip header row if present (e.g. "id,start_time,finish_time")
            if parts[0].lower() in ("id", "delivery_id") or not parts[1].lstrip("-").isdigit():
                continue

            delivery_id = parts[0].strip()
            start_time = int(parts[1].strip())
            finish_time = int(parts[2].strip())
            deliveries.append(Delivery(delivery_id, start_time, finish_time))

    return deliveries


def schedule_single_driver(deliveries: list[Delivery]) -> list[Delivery]:
    """
    Task A: Maximum Deliveries for One Driver (Interval Scheduling).
    
    Greedy Choice:
        Always select the compatible delivery that finishes earliest.
        This leaves the maximum remaining time available for subsequent deliveries.

    Time Complexity:
        O(n log n) dominated by the initial sort by finish time.
        The linear scan takes O(n).
    """
    # 1. Sort deliveries in ascending order of their finish times
    sorted_deliveries = sorted(deliveries, key=lambda d: d.finish)

    selected = []
    last_finish_time = -float("inf")

    # 2. Greedily select each delivery that starts at or after the previous finish time
    for delivery in sorted_deliveries:
        if delivery.start >= last_finish_time:
            selected.append(delivery)
            last_finish_time = delivery.finish

    return selected


def schedule_multiple_drivers(deliveries: list[Delivery]) -> dict[int, list[Delivery]]:
    """
    Task B: Minimum Number of Drivers (Interval Partitioning).

    Greedy Choice:
        Sort deliveries by start time. For each delivery, assign it to an
        available driver who finished earliest. If no driver is currently free,
        hire a new driver.

    Implementation:
        Uses a min-heap storing (earliest_finish_time, driver_id) to find
        the next available driver in O(log k) time.

    Time Complexity:
        O(n log n) where n is the number of delivery requests.
    """
    if not deliveries:
        return {}

    # 1. Sort deliveries in ascending order of start time
    sorted_deliveries = sorted(deliveries, key=lambda d: d.start)

    # Min-heap stores: (driver_finish_time, driver_id)
    driver_heap: list[tuple[int, int]] = []
    driver_schedules: dict[int, list[Delivery]] = {}
    driver_counter = 0

    # 2. Assign each delivery to an existing free driver or a new driver
    for delivery in sorted_deliveries:
        # Check if the earliest finishing driver is available
        if driver_heap and driver_heap[0][0] <= delivery.start:
            # Reuse this driver
            _, driver_id = heapq.heappop(driver_heap)
        else:
            # All active drivers are busy; allocate a new driver
            driver_counter += 1
            driver_id = driver_counter
            driver_schedules[driver_id] = []

        # Assign delivery to driver and update driver's finish time in min-heap
        driver_schedules[driver_id].append(delivery)
        heapq.heappush(driver_heap, (delivery.finish, driver_id))

    return driver_schedules


def find_min_rejections(deliveries: list[Delivery]) -> tuple[int, list[Delivery]]:
    """
    Task C: Interview-Style Variant / Minimum Rejections (LeetCode 435).

    Greedy Choice / Relation to Task A:
        To minimize the number of rejected deliveries, we must maximize the
        number of mutually compatible deliveries accepted by the single driver.
        If the maximum number of compatible deliveries is k, then the minimum
        number of deliveries that must be rejected is exactly n - k.

    Time Complexity:
        O(n log n) dominated by sorting in schedule_single_driver.
    """
    if not deliveries:
        return 0, []

    # Maximum compatible deliveries selected by greedy earliest-finish-time (Task A)
    accepted = schedule_single_driver(deliveries)
    accepted_ids = {d.id for d in accepted}

    # The rejected deliveries are all remaining deliveries not accepted
    rejected = [d for d in deliveries if d.id not in accepted_ids]
    min_rejected_count = len(deliveries) - len(accepted)

    return min_rejected_count, rejected


def print_task_a_results(selected: list[Delivery]) -> None:
    """Displays the output in the format specified by Task A."""
    print("--- Task A: Single Driver Schedule ---")
    if not selected:
        print("Selected delivery IDs: None")
        print("Total deliveries completed: 0")
        return

    print("Selected Deliveries (ID: start -> finish):")
    for d in selected:
        print(f"  {d.id}: ({d.start}, {d.finish})")
    
    selected_ids = ", ".join(d.id for d in selected)
    print(f"Delivery IDs: [{selected_ids}]")
    print(f"Total deliveries completed: {len(selected)}")


def print_task_b_results(schedules: dict[int, list[Delivery]]) -> None:
    """Displays the driver assignments in the format specified by Task B."""
    print("--- Task B: Multi-Driver Schedule ---")
    if not schedules:
        print("No deliveries to schedule.")
        print("Minimum drivers required: 0")
        return

    for driver_id in sorted(schedules.keys()):
        deliveries = schedules[driver_id]
        ids = " ".join(d.id for d in deliveries)
        print(f"Driver {driver_id}: {ids}")
    
    print(f"\nMinimum drivers required: {len(schedules)}")


def print_task_c_results(count: int, rejected: list[Delivery]) -> None:
    """Displays the output in the format specified by Task C."""
    print("--- Task C: Rejected Deliveries (One Driver) ---")
    print(f"Minimum deliveries to reject: {count}")
    if rejected:
        rejected_details = ", ".join(f"{d.id}: ({d.start}, {d.finish})" for d in rejected)
        print(f"Rejected deliveries: {rejected_details}")
    else:
        print("Rejected deliveries: None (all deliveries are compatible)")


if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "data/sample.csv"
    print(f"Loading data from: {file_path}")
    requests = load_deliveries(file_path)
    print(f"Loaded {len(requests)} delivery requests.\n")
    
    # Task A
    chosen = schedule_single_driver(requests)
    print_task_a_results(chosen)
    print()

    # Task B
    driver_plan = schedule_multiple_drivers(requests)
    print_task_b_results(driver_plan)
    print()

    # Task C
    rejected_count, rejected_list = find_min_rejections(requests)
    print_task_c_results(rejected_count, rejected_list)

