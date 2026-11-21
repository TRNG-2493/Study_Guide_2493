# RequirementReviewer: Friday Report (exemplar, built from the solution files)

Author: a.trainee | Date: 2026-10-23 | AI tool: Claude (live runs in Stage 5)

## 1. Start-up and pinning
- `agent.json` pins: instructions v1.0.0, template rr_user@1.0.0, contract 1.0.0, temperature 0.
- Proved the agent refuses to start: broken instruction file (missing Boundaries) -> ValueError; wrong template pin -> KeyError; agent.json contract 1.1.0 -> ValueError. (Each restored afterwards.)
- `python check_rule_map.py instructions/rr_instructions_v1.0.0.md instructions/rule_map_v1.0.0.json`: 15 entries, 0 problems.
- `python check_versions.py`: AGREE.

## 2. Contract and validation
- `pytest`: 41 passed (contract 20 including P07, validation 15, CLI 6).
- Planted-defect tests: one per rule, exact set. An R5 mutation built by copying a finding also fires Q2 (same quote), so the R5 test data uses distinct quotes: fix the test data, not the rule.

## 3. Execution against the backlog (run 'demo', scripted replies)
| Story | Outcome | Action | Owner |
|---|---|---|---|
| US-420 | PASS | human review, then questions to the PO | story tester |
| US-430 | FAIL R3 | reject; log for refinement (quote cited on AC3, text is AC2) | agent owner |
| US-440 | PASS (no findings) | human confirms the story is clear | story tester |
| US-450 | PASS (needs_clarification) | send the open question to the loyalty team | backlog owner |
| US-460 | PASS | **reject at human review**: out of scope (it planned test scripts); no rule can see this | agent owner |
| US-470 | FAIL S1 (fences) | reject, count, do not repair; the hidden reply also proposed "within 5 days" | agent owner |
| US-48 | rejected_input | fix the story id and ACs in the backlog; no model call made | backlog owner |
`validate_output.py --run runs/demo`: 6 checked, 4 passed, 2 failed, exit 1, same verdicts as run.jsonl.

## 4. Live Claude run (US-470)
Prompt fingerprint f0612d1fb29e, identical to the scripted run. Saved reply: PASS, exit 0.
Human review (Q3): F-470-01 and F-470-03 correct and grounded; F-470-02 (original payment method unavailable) is a good INCOMPLETE finding nobody else raised; no number proposed. Missed: who decides an item is damaged. One run is one sample.

## 5. Refinement
- Step 0, test the test data: `check_pairs_rules.py` all PASS (P04 SKIP).
- Baseline v1.0.0: 59% (71/121). Errors R3 16, R4 13, S1 13, R5 7; warnings Q2 11, Q1 5; P05 status checks failed 4 times.
- Error analysis (show_failures P01, P05): quotes on the wrong AC; numbering gaps; duplicates; out-of-scope requests reviewed as requirements; fences.
- Hypotheses (written before editing): H1 a self-check on quotes cuts R3; H2 "without gaps" cuts R4; H3 "only once" cuts Q2 and duplicates; H4 an explicit out-of-scope rule fixes P05; S1, R5 and Q1 stay about the same; no pair gets worse.
- v1.1.0 in a new file; `agent_v1.1.0.json` differs only in version and instructions path.
- Result, same seeds: 76% (92/121). R3 16 -> 3, R4 13 -> 2, Q2 11 -> 4, P05 55% -> 70%; S1 unchanged. No pair worse.

## 6. Ship decision
| Criterion (set before measuring) | Target | Result | Met |
|---|---|---|---|
| Overall pass rate | >= 75% | 76% | yes |
| No pair worse than baseline | none worse | none worse | yes |
| P05 (out of scope) | >= 70% | 70% | yes |
| Regression suite | all pass | 41 passed | yes |
| Human spot-check of 10 PASS outputs (Q3) | done | 1 done (live US-470) | **no** |
Decision: ship v1.1.0 to the team for supervised use only after the human spot-check; keep the validation gate in front of every reply.
