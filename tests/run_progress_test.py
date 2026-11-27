"""Progress checks: mastery derives only from recorded sessions."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
from progress import mastery  # noqa: E402


def main():
    failures = 0

    def check(name, ok):
        nonlocal failures
        failures += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} {name}")

    check("no sessions = untouched", mastery([], "bt-01") == 0)
    check("one session = practiced", mastery(
        [{"technique": "bt-01", "date": "2026-11-27", "completed": False}], "bt-01") == 1)
    three = [{"technique": "bt-01", "date": "2026-11-27", "completed": True}] * 3
    check("three completions = steady", mastery(three, "bt-01") == 2)
    seven_one_day = [{"technique": "bt-01", "date": "2026-11-27", "completed": True}] * 7
    check("seven completions one day is not mastery", mastery(seven_one_day, "bt-01") == 2)
    seven = ([{"technique": "bt-01", "date": "2026-11-25", "completed": True}] * 3
             + [{"technique": "bt-01", "date": "2026-11-26", "completed": True}] * 2
             + [{"technique": "bt-01", "date": "2026-11-27", "completed": True}] * 2)
    check("seven completions across three days = mastered", mastery(seven, "bt-01") == 3)
    check("other techniques do not count", mastery(seven, "bt-02") == 0)
    print(f"{6 - failures}/6 progress checks pass")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
