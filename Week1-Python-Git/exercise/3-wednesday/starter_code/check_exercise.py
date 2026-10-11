"""Self-check for the Day 3 exercise. Run:  python3 check_exercise.py
Plain asserts, no pytest. Each check prints PASS or FAIL with a hint.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

try:
    import manager as m
except Exception as exc:                      # a crash in manager.py
    print(f"FAIL: manager.py crashed on import: {type(exc).__name__}: {exc}")
    print("Read the last lines of the traceback: run `python3 manager.py` to see it.")
    sys.exit(1)

results = []


def check(name, fn):
    try:
        fn()
        results.append((name, True, ""))
    except AssertionError as exc:
        results.append((name, False, str(exc)))
    except Exception as exc:
        results.append((name, False, f"{type(exc).__name__}: {exc}"))


def ids_of(cases):
    return [c["id"] for c in cases]


# ---- Part 1 ---------------------------------------------------------------
def part1():
    assert m.raw_ids, "raw_ids is empty/None: TODO 1a (loop and append each id)"
    assert len(m.raw_ids) == 14, f"raw_ids should have 14 IDs, has {len(m.raw_ids)}"
    assert m.first_three_ids == ["TC-101", "TC-102", "TC-103"], \
        f"first_three_ids wrong: {m.first_three_ids!r} (TODO 1b: raw_ids[:3])"
    assert m.last_two_ids == ["TC-110", "TC-111"], \
        f"last_two_ids wrong: {m.last_two_ids!r} (TODO 1c: raw_ids[-2:])"
    assert m.every_other_id == m.raw_ids[::2] and len(m.every_other_id) == 7, \
        f"every_other_id wrong: {m.every_other_id!r} (TODO 1d: raw_ids[::2])"


# ---- Part 2 ---------------------------------------------------------------
def part2():
    assert isinstance(m.unique_cases, list), \
        f"unique_cases should be a list, is {type(m.unique_cases).__name__} (TODO 2)"
    assert len(m.RAW_TEST_CASES) == 14, "RAW_TEST_CASES was changed: do not remove items from it"
    assert len(m.unique_cases) == 11, f"expected 11 unique cases, got {len(m.unique_cases)}"
    ids = ids_of(m.unique_cases)
    assert len(set(ids)) == len(ids), "unique_cases still contains duplicate IDs"
    assert ids == ["TC-101", "TC-102", "TC-103", "TC-104", "TC-105", "TC-106",
                   "TC-107", "TC-108", "TC-109", "TC-110", "TC-111"], \
        f"order must match the original data (first occurrence kept). Got {ids}"
    tc106 = [c for c in m.unique_cases if c["id"] == "TC-106"][0]
    assert tc106["status"] == "fail", "TC-106: keep the FIRST record (status 'fail'), not the re-run"
    assert isinstance(m.seen_ids, set) and len(m.seen_ids) == 11, \
        "seen_ids should be a set holding the 11 IDs you have kept"


# ---- Part 3 ---------------------------------------------------------------
def part3():
    assert m.ids_by_module is not None, "ids_by_module is None (TODO 3a/3b)"
    got = dict(m.ids_by_module)
    expected = {
        "login": ["TC-101", "TC-102", "TC-103"],
        "search": ["TC-104", "TC-105", "TC-111"],
        "checkout": ["TC-106", "TC-107", "TC-108"],
        "profile": ["TC-109", "TC-110"],
    }
    assert got == expected, f"grouping wrong.\n    expected {expected}\n    got      {got}"


# ---- Part 4 ---------------------------------------------------------------
def part4():
    assert isinstance(m.lookup, dict), f"lookup should be a dict, is {type(m.lookup).__name__} (TODO 4a)"
    assert len(m.lookup) == 11, f"lookup should have 11 entries, has {len(m.lookup)}"
    assert m.lookup["TC-106"]["status"] == "fail", "lookup['TC-106'] should be the whole case dict (status 'fail')"
    assert m.found_case == {"id": "TC-107", "module": "checkout", "priority": "High", "status": "pass"}, \
        f"found_case wrong: {m.found_case!r} (TODO 4b)"
    assert m.missing_case == "not found", \
        f"missing_case should be the text 'not found', got {m.missing_case!r} (TODO 4c: .get with a default)"
    assert "TC-999" not in m.lookup, "do not add TC-999 to lookup; use .get() with a default"


# ---- Part 5 ---------------------------------------------------------------
def part5():
    assert m.status_counts is not None, "status_counts is None (TODO 5a)"
    assert dict(m.status_counts) == {"pass": 5, "fail": 3, "skip": 2, "unknown": 1}, \
        f"status counts wrong: {dict(m.status_counts)}  (expected pass 5, fail 3, skip 2, unknown 1)"
    assert isinstance(m.executed_ids, set), \
        f"executed_ids should be a set, is {type(m.executed_ids).__name__} (TODO 5b)"
    assert len(m.executed_ids) == 10 and "TC-110" not in m.executed_ids, \
        "executed_ids: only cases that HAVE a status (10 of them; TC-110 has none)"
    assert m.not_run_ids == ["TC-110", "TC-112"], \
        f"not_run_ids should be the sorted list ['TC-110', 'TC-112'], got {m.not_run_ids!r} (TODO 5c)"


check("Part 1 - raw IDs and slicing", part1)
check("Part 2 - dedupe with a set", part2)
check("Part 3 - group by module (defaultdict)", part3)
check("Part 4 - lookup by ID (dict + .get)", part4)
check("Part 5 - Counter and set difference", part5)

print("\n=== Self-check results ===")
for name, ok, msg in results:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        print(f"       -> {msg}")
passed = sum(1 for _, ok, _ in results if ok)
print(f"\n{passed}/{len(results)} parts passing")
if passed == len(results):
    print("All checks pass. Now confirm your Git history (README, Definition of Done).")
    sys.exit(0)
print("Fix the first FAIL, re-run, repeat. (The self-check does not grade your Git work.)")
sys.exit(1)
