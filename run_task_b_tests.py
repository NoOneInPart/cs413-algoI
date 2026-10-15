"""
Test runner for Task B: Minimum Number of Drivers
Validates all required test cases from the CS 413 project specification.
"""

from pathlib import Path
from delivery_scheduler import load_deliveries, schedule_multiple_drivers

# Expected minimum drivers for each test case as specified in the PDF table (Page 3)
TASK_B_EXPECTED = {
    1: 0,  # No deliveries
    2: 1,  # (1, 3)
    3: 1,  # (1, 3), (3, 5), (5, 7)
    4: 3,  # (1, 5), (2, 6), (3, 7)
    5: 2,  # (1, 4), (2, 5), (4, 7), (5, 8)
    6: 2,  # (5, 8), (1, 4), (2, 5), (4, 6), (6, 9)
}


def verify_no_overlaps(driver_schedules) -> bool:
    """Verifies that no driver is assigned overlapping deliveries."""
    for driver_id, deliveries in driver_schedules.items():
        # Sort assigned deliveries by start time to verify compatibility
        sorted_d = sorted(deliveries, key=lambda d: d.start)
        for i in range(len(sorted_d) - 1):
            if sorted_d[i].finish > sorted_d[i + 1].start:
                return False
    return True


def run_tests():
    data_dir = Path("data/task_b")
    print("=" * 65)
    print("RUNNING REQUIRED TEST CASES FOR TASK B")
    print("=" * 65)

    all_passed = True
    for test_num in sorted(TASK_B_EXPECTED.keys()):
        filepath = data_dir / f"test{test_num}.csv"
        deliveries = load_deliveries(str(filepath))
        schedules = schedule_multiple_drivers(deliveries)

        expected = TASK_B_EXPECTED[test_num]
        actual = len(schedules)
        valid_schedule = verify_no_overlaps(schedules)

        passed = (actual == expected) and valid_schedule
        all_passed = all_passed and passed

        intervals_str = ", ".join(f"({d.start}, {d.finish})" for d in deliveries) if deliveries else "No deliveries"
        status = "[PASS]" if passed else "[FAIL]"

        print(f"Test {test_num}: {status}")
        print(f"  Input intervals : {intervals_str}")
        print(f"  Drivers needed  : {actual} (Expected: {expected})")
        print(f"  Non-overlapping : {'Yes' if valid_schedule else 'No'}")
        for d_id in sorted(schedules.keys()):
            ids = " ".join(d.id for d in schedules[d_id])
            print(f"    Driver {d_id}: {ids}")
        print()

    print("=" * 65)
    if all_passed:
        print("ALL TASK B REQUIRED TEST CASES PASSED SUCCESSFULLY!")
    else:
        print("SOME TESTS FAILED.")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()

