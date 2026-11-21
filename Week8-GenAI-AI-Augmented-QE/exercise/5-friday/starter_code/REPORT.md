# RequirementReviewer: Friday Report

Author: | Date: | AI tool: Claude (model name as shown in the interface):

## 1. Start-up and pinning
- What `agent.json` pins:
- Three ways I proved the agent refuses to start (what I broke, the error, restored):
- `check_rule_map.py` result (entries, problems):
- `check_versions.py` result:

## 2. Contract and validation
- `python -m pytest -q` result:
- One planted-defect test that first fired more than one rule, and what I changed:

## 3. Execution against the backlog (run id: )
| Story | Outcome | Action | Owner |
|---|---|---|---|
| | | | |
- `validate_output.py --run runs/<id>` result and exit code (does it agree with run.jsonl?):
- One output I wanted to "fix by hand", and why I did not:
- `trace_matrix.py` takeaway:

## 4. Live Claude runs (two stories)
| Story | Fingerprint (same as scripted run?) | Verdict | Human review (Q3): correct / wrong / missing |
|---|---|---|---|
| | | | |

## 5. Refinement
- Step 0, test the test data (`check_pairs_rules.py`):
- Baseline (paste `evaluate.py` output):
- Error analysis (groups of failures with counts, from `show_failures.py`):
- Hypotheses, written BEFORE editing (H1..Hn, each with the rule or check it should move and the expected direction):
- The change (diff summary; what is identical between `agent.json` and `agent_v1.1.0.json`):
- Re-evaluation with the same seeds (paste output) and before/after table:

| Measure | v1.0.0 | v1.1.0 | Hypothesis confirmed? |
|---|---|---|---|
| | | | |

- New regression pair(s) added from a real failure:

## 6. Ship decision
| Criterion (written BEFORE measuring) | Target | Result | Met |
|---|---|---|---|
| | | | |
Decision and reason:
