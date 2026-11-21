"""Reference checker for the Stage 5 test-data probe (instructor only).

Applies the ShopFront registration rules (templates/materials/user-stories.md)
and reports every row where the AI's expected_valid label is wrong.
Usage:  python check_registration_data.py sample_ai_registration_data.csv
Exit code 1 when any row is mislabelled or the header is wrong.
"""
import csv
import re
import sys

HEADER = ["username", "email", "age", "country", "marketing_opt_in", "expected_valid"]
USERNAME = re.compile(r"^[a-z][a-z0-9-]{3,15}$")          # 4-16 chars, starts with a letter
EMAIL = re.compile(r"^[^@\s]+@example\.(com|org)$")       # one @, reserved domains only


def broken_rules(row):
    problems = []
    if not USERNAME.match(row["username"]):
        problems.append("username")
    if not EMAIL.match(row["email"]):
        problems.append("email")
    age = row["age"].strip()
    if not (age.isdigit() and 16 <= int(age) <= 99):
        problems.append("age")
    if row["country"] not in ("US", "CA"):
        problems.append("country")
    if row["marketing_opt_in"] not in ("yes", "no"):
        problems.append("marketing_opt_in")
    return problems


def main(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != HEADER:
            print(f"BAD header: {reader.fieldnames} (format drift; expected {HEADER})")
            return 1
        rows = list(reader)
    bad = 0
    for n, row in enumerate(rows, start=1):
        problems = broken_rules(row)
        ai_valid = row["expected_valid"].strip().lower() == "true"
        if ai_valid == (not problems):
            continue
        bad += 1
        print(f"BAD row {n:2d}  AI label={ai_valid!s:5}  actual: "
              f"{'valid' if not problems else 'breaks ' + ', '.join(problems)}  ({row['username']})")
    print(f"{len(rows)} rows checked, {bad} mislabelled by the AI.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "sample_ai_registration_data.csv"))
