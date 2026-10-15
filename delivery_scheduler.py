"""
Pioneer Delivery Company - Scheduling System
CS 413: Analysis of Algorithms - Portfolio Part I
"""

from dataclasses import dataclass
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


if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "data/sample.csv"
    print(f"Loading data from: {file_path}")
    requests = load_deliveries(file_path)
    print(f"Loaded {len(requests)} delivery requests.\n")
    
    chosen = schedule_single_driver(requests)
    print_task_a_results(chosen)

