"""Test-Data Manager (starter) - Day 3 exercise.

Work through the parts in README.md, top to bottom.
Replace every `None` / empty placeholder marked TODO with your own code.
No functions are needed: write plain statements (variables, loops, if).
Run it:            python3 manager.py
Check your work:   python3 check_exercise.py
"""
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# SAMPLE DATA - an export from a test-management tool. Do NOT edit this list.
# It contains duplicate IDs (TC-102, TC-104, TC-106) and one record
# with no "status" key (TC-110).
# ---------------------------------------------------------------------------
RAW_TEST_CASES = [
    {"id": "TC-101", "module": "login",    "priority": "High",   "status": "pass"},
    {"id": "TC-102", "module": "login",    "priority": "High",   "status": "fail"},
    {"id": "TC-103", "module": "login",    "priority": "Medium", "status": "pass"},
    {"id": "TC-104", "module": "search",   "priority": "Medium", "status": "pass"},
    {"id": "TC-102", "module": "login",    "priority": "High",   "status": "fail"},  # exact duplicate
    {"id": "TC-105", "module": "search",   "priority": "Low",    "status": "skip"},
    {"id": "TC-106", "module": "checkout", "priority": "High",   "status": "fail"},
    {"id": "TC-107", "module": "checkout", "priority": "High",   "status": "pass"},
    {"id": "TC-104", "module": "search",   "priority": "Medium", "status": "pass"},  # exact duplicate
    {"id": "TC-108", "module": "checkout", "priority": "Medium", "status": "skip"},
    {"id": "TC-109", "module": "profile",  "priority": "Low",    "status": "pass"},
    {"id": "TC-106", "module": "checkout", "priority": "High",   "status": "pass"},  # re-run, DIFFERENT status
    {"id": "TC-110", "module": "profile",  "priority": "Low"},                       # no status yet
    {"id": "TC-111", "module": "search",   "priority": "High",   "status": "fail"},
]

# Test cases the team PLANNED to run this sprint (a set of IDs).
PLANNED_IDS = {"TC-101", "TC-102", "TC-103", "TC-104", "TC-105", "TC-106",
               "TC-107", "TC-108", "TC-109", "TC-110", "TC-111", "TC-112"}

# ===========================================================================
# PART 1 - Look at the raw data (slicing)
# ===========================================================================
raw_ids = []                 # TODO 1a: loop over RAW_TEST_CASES, append each case's "id"
first_three_ids = None       # TODO 1b: slice of raw_ids: the first 3 IDs
last_two_ids = None          # TODO 1c: slice of raw_ids: the last 2 IDs (negative index)
every_other_id = None        # TODO 1d: slice of raw_ids: every 2nd ID (step)

print("Raw records :", len(RAW_TEST_CASES))
print("First three :", first_three_ids)
print("Last two    :", last_two_ids)

# ===========================================================================
# PART 2 - Remove duplicates (list + set)
# Rule: keep the FIRST record for each ID, keep the original order.
# ===========================================================================
seen_ids = set()
unique_cases = []
# TODO 2: for each case in RAW_TEST_CASES, if its id is not in seen_ids,
#         add the id to seen_ids and append the case to unique_cases.
unique_cases = None          # TODO 2 (delete this line once your loop works)

print("Unique cases:", unique_cases)

# ===========================================================================
# PART 3 - Group by module (defaultdict)
# Result shape: {"login": ["TC-101", "TC-102", ...], "search": [...], ...}
# ===========================================================================
ids_by_module = None         # TODO 3a: create a defaultdict(list)
# TODO 3b: loop over unique_cases and append each case's id under its module

print("By module   :", ids_by_module)

# ===========================================================================
# PART 4 - Lookup by ID (dict)
# ===========================================================================
lookup = None                # TODO 4a: dict mapping id -> the whole case dict (use unique_cases)
found_case = None            # TODO 4b: the case for "TC-107", using lookup.get(...)
missing_case = None          # TODO 4c: lookup for "TC-999" that returns the text "not found" instead of crashing

print("TC-107      :", found_case)
print("TC-999      :", missing_case)

# ===========================================================================
# PART 5 - Counts by status (Counter) and planned-vs-executed (sets)
# ===========================================================================
status_counts = None         # TODO 5a: Counter of statuses over unique_cases;
                             #          a case with no "status" counts as "unknown" (hint: .get)
executed_ids = None          # TODO 5b: SET of ids of unique cases that HAVE a "status"
not_run_ids = None           # TODO 5c: SORTED LIST of IDs in PLANNED_IDS that are not in executed_ids

print("By status   :", status_counts)
print("Not run     :", not_run_ids)
