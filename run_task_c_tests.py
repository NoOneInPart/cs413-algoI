"""
Test runner for Task C: Minimum Number of Rejected Deliveries
Validates all required test cases from the CS 413 project specification.
"""

from pathlib import Path
from delivery_scheduler import load_deliveries, find_min_rejections

# Expected minimum rejected for each test case as specified in the PDF table (Page 4)
TASK_C_EXPECTED = {
    1: 0,  # No deliveries
    2: 0,  # (1, 3)
    3: 0,  # (1, 3), (3, 5), (5, 7)
    4: 2,  # (1, 5), (2, 6), (3, 7)
    5: 1,  # (5, 7), (1, 3), (3, 5), (2, 4)
    6: 1,  # (1, 2), (2, 3), (3, 4), (1, 3)
}


def run_tests():
    data_dir = Path("data/task_c")
    print("=" * 65)
    print("RUNNING REQUIRED TEST CASES FOR TASK C")
    print("=" * 65)

    all_passed = True
    for test_num in sorted(TASK_C_EXPECTED.keys()):
        filepath = data_dir / f"test{test_num}.csv"
        deliveries = load_deliveries(str(filepath))
        actual_count, rejected_deliveries = find_min_rejections(deliveries)

        expected = TASK_C_EXPECTED[test_num]
        passed = (actual_count == expected)
        all_passed = all_passed and passed

        intervals_str = ", ".join(f"({d.start}, {d.finish})" for d in deliveries) if deliveries else "No deliveries"
        rejected_str = ", ".join(f"{d.id}({d.start},{d.finish})" for d in rejected_deliveries) if rejected_deliveries else "None"
        status = "[PASS]" if passed else "[FAIL]"

        print(f"Test {test_num}: {status}")
        print(f"  Input intervals : {intervals_str}")
        print(f"  Total requests  : {len(deliveries)}")
        print(f"  Min rejected    : {actual_count} (Expected: {expected})")
        print(f"  Rejected items  : {rejected_str}\n")

    print("=" * 65)
    if all_passed:
        print("ALL TASK C REQUIRED TEST CASES PASSED SUCCESSFULLY!")
    else:
        print("SOME TESTS FAILED.")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()

