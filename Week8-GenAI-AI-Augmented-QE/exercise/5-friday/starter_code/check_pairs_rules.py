# check_pairs_rules.py
"""Step 0 of refinement: test your test data. Run every reference answer through the validator.
A reference answer that fails a rule is a bug in the ORACLE, not in the agent.
Usage:  python check_pairs_rules.py      (exit 1 if any reference answer fails)
Provided complete. Lesson: written/5-friday/agent-testing-and-refinement.md, section 3.
"""
import json
import sys

from evaluate import load_pairs
from rr.contract import check_input
from rr.validation import validate_reply

bad = 0
for pid, pair in sorted(load_pairs().items()):
    if not pair["input_should_be_valid"]:
        print(f"{pid}  SKIP  (invalid input, no reference answer)")
        continue
    report = validate_reply(check_input(pair["input"]), json.dumps(pair["expected_output"]))
    print(f"{pid}  {report.verdict}")
    for f in report.findings:
        print(f"      {f.rule} {f.where}: {f.message}")
    bad += report.verdict == "FAIL"
sys.exit(1 if bad else 0)
