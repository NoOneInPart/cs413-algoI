"""
Test runner for Task A: Maximum Deliveries for One Driver
Validates all required test cases from the CS 413 project specification.
"""

from pathlib import Path
from delivery_scheduler import load_deliveries, schedule_single_driver

# Expected maximum selected for each test case as specified in the PDF table (Page 2)
TASK_A_EXPECTED = {
    1: 0,  # No deliveries
    2: 1,  # (1, 3)
    3: 3,  # (1, 3), (3, 5), (5, 7)
    4: 1,  # (1, 5), (2, 6), (3, 7)
    5: 3,  # (5, 7), (1, 3), (3, 5), (2, 4)
    6: 2,  # (1, 4), (2, 4), (4, 6)
}


def run_tests():
    data_dir = Path("data/task_a")
    print("=" * 65)
    print("RUNNING REQUIRED TEST CASES FOR TASK A")
    print("=" * 65)

    all_passed = True
    for test_num in sorted(TASK_A_EXPECTED.keys()):
        filepath = data_dir / f"test{test_num}.csv"
        deliveries = load_deliveries(str(filepath))
        selected = schedule_single_driver(deliveries)
        
        expected = TASK_A_EXPECTED[test_num]
        actual = len(selected)
        passed = (actual == expected)
        all_passed = all_passed and passed

        intervals_str = ", ".join(f"({d.start}, {d.finish})" for d in deliveries) if deliveries else "No deliveries"
        selected_str = ", ".join(f"{d.id}({d.start},{d.finish})" for d in selected) if selected else "None"
        status = "[PASS]" if passed else "[FAIL]"

        print(f"Test {test_num}: {status}")
        print(f"  Input intervals : {intervals_str}")
        print(f"  Selected        : {selected_str}")
        print(f"  Max count       : {actual} (Expected: {expected})\n")

    print("=" * 65)
    if all_passed:
        print("ALL TASK A REQUIRED TEST CASES PASSED SUCCESSFULLY!")
    else:
        print("SOME TESTS FAILED.")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
