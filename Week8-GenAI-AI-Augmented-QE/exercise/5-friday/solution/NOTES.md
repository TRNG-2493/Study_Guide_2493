# Friday solution notes (instructors only)

## Exercise mode and scope
Mode A (code lab), individual. Time box 2-3 hours: setup 10, stages 15 / 25 / 35 / 20 / 25 / 40 / 10 minutes. Solvable from Monday to Friday material: the structure mirrors the demo's `tcd_agent` (`tcd/contract.py`, `tcd/validation.py`, `validate_output.py`, `run_requirements.py`, `evaluate.py`, `show_failures.py`, `check_pairs_rules.py`, `check_rule_map.py`, `check_versions.py`), applied to a different agent so the demo is a model, not an answer. Out of scope as in the demo: retries, chains, tools, LLM-as-grader (Week 9); prompt injection in depth (Week 10).

## Intentional deviations from the CMA log (do not flag in QA)
- **No Project 2 milestone.** The CMA log and the demo bridge say "run against real requirements; Project 2 milestone". By instructor decision, Project 2 is ignored this week. The agent runs against the synthetic ShopFront backlog (`requirements/backlog.csv`), the same system used Monday to Thursday. Every element of the demo bridge is kept: pinned `agent.json` with start-up refusals, rule-to-check map at 0 problems, contract at four points with version agreement, validation script with exit codes 0/1/2 and a JSON report plus planted-defect tests, a run with `run.jsonl`, evidence, triage with owners and a traceability matrix, one measured refinement with hypotheses, a new instruction version, same-seed re-evaluation, a CHANGELOG with evidence and a regression pair, meaningful commits and AI disclosure.
- **Thursday carried forward.** `starter_code/agent/` is exactly Thursday's instructor solution (`exercise/4-thursday/solution/agent/`): schemas, template, rules, samples P01-P06, CONTRACT.md, manifest. Thursday's `instructions.md` moved to `instructions/rr_instructions_v1.0.0.md` unchanged (versioned file, as Friday's lesson requires); Thursday's CHANGELOG moved to `instructions/CHANGELOG.md`. Trainees whose own Thursday design passed the design gate may port it, but grading anchors below assume the baseline.
- **Claude as the AI tool.** Stage 5 has two live Claude runs (prompt printed by `rr_lab.py prompt`, reply saved unedited, validated by the agent, then reviewed by the trainee finding by finding). Using Claude as a coding assistant in Stages 2 to 4 is allowed with disclosure; the planted-defect tests are the gate.
- **Full time box on Friday**, as instructed: no shortened scope.

## What the starter leaves to the trainee
`rr/contract.py` (defaults from schema, `check_input`, `parse_reply`, `check_output_schema`), `rr/validation.py` (R1-R7, Q1, Q2; `validate_reply` and the verdict logic are provided), `validate_output.py` `main()`, the planted-defect tests for R3-Q2, three CLI tests, `PAIR_CHECKS` for P02/P03/P05/P06, 10 of 15 rule-map entries, and everything in Stage 6. Provided complete: loader, renderer, model clients, the wired agent, runner, trace matrix, simulator, evaluation engine, failure listing and the consistency checkers.

## Verified results (Python 3.10, jsonschema 4.26, pytest 9.1)
| Command | Starter | Solution |
|---|---|---|
| `python rr_lab.py check` | env OK, agent assembles OK, 3 test files MISSING | all OK |
| `python -m pytest -q` | collection error (NotImplementedError from `check_input`), as intended | 41 passed |
| Starter with the solution's implementations dropped in | 39 passed (18 + 15 + 6) | n/a |
| `python check_rule_map.py instructions/rr_instructions_v1.0.0.md instructions/rule_map_v1.0.0.json` | 5 entries, 10 problems | 15 entries, 0 problems |
| same for v1.1.0 with `rule_map_v1.1.0.json` | n/a | 17 entries, 0 problems (v1.0.0 map on v1.1.0: 1 UNMAPPED) |
| `python check_versions.py` | AGREE | AGREE (also with `--config agent_v1.1.0.json`) |
| `python run_requirements.py requirements/backlog.csv --run-id demo` | runs once contract and validation exist | 7 stories, 6 model calls: US-420 PASS, US-430 FAIL R3, US-440 PASS, US-450 PASS, US-460 PASS, US-470 FAIL S1, US-48 rejected_input |
| `python validate_output.py --run runs/demo` | NotImplementedError until Stage 4 | 6 checked, 4 passed, 2 failed, exit 1 |
| `python check_pairs_rules.py` | needs Stage 3 | all PASS, P04 SKIP |
| `python evaluate.py` (v1.0.0, 20 seeds) | needs Stages 2, 3 and PAIR_CHECKS | 71/121 = 59%; errors R3 16, R4 13, R5 7, S1 13; warnings Q1 5, Q2 11 |
| `python evaluate.py --config agent_v1.1.0.json` | n/a | 92/121 = 76%; R3 3, R4 2, R5 5, S1 13; Q1 5, Q2 4 |
| Live run US-470 (`--model saved`, backup reply) | n/a | PASS, exit 0; fingerprint f0612d1fb29e identical to the scripted run |

Note: without P07, the solution scores are 60/101 = 59% and 76/101 = 75%; trainee numbers depend on which pair checks they write. Grade the method and the honesty of the comparison, not the percentage.

`replies/` and `backups/live_US-470.reply.txt` are **written for the course**, not real model output. The simulator's mistake rates are invented for teaching; say so whenever a number appears.

## The simulator (read before grading Stage 6)
`rr/simulated.py` starts from the reviewed answers (`sim_answers.json`) and injects: fences 8% (no instruction fixes it), quote cited on the wrong AC 30% (drops to 4% when the instructions contain a self-check that quotes appear in the named criterion), numbering gaps 20% (to 3% with "without gaps", "consecutive", "do not skip numbers"...), duplicates 20% (to 4% with "only once", "no duplicates", "same problem twice"...), proposed answers 10% (no instruction fixes it), over the limit 15% (no instruction fixes it), out-of-scope request obeyed 35% (to 5% with a rule that test cases/scripts/code are out of scope even when written as a criterion, or that a criterion asking for tests is not a requirement). Rule recognition is by regex on ordinary wording, verified with several phrasings; a trainee who writes a sensible rule should see the effect. If a reasonable rule does not register, accept the hypothesis as "not confirmed by the simulator" and check the regex in `MISTAKES` together; do not penalise.

## Grading anchors
- **Start-up refusals:** three different errors with the restore step. Editing `agent.json` itself and forgetting to restore it fails `check_versions.py`.
- **Contract:** `INPUT_DEFAULTS` read from the schema (a retyped dict loses marks even if tests pass); `{**INPUT_DEFAULTS, **story}` order; `iter_errors`, not `validate`; fences rejected, never stripped.
- **Rules:** R3 normalisation (case, whitespace, curly quotes) and per-AC comparison; R4 one message per finding; R6 both branches; R7 uses the gated `focus`; Q1 ignores numbers present in the story; Q2 on (ac_id, normalised quote).
- **Planted tests:** exact-set assertions. The classic trap is an R5 mutation made by copying a finding, which also fires Q2.
- **Script:** exit 2 for empty folders and invalid stories, messages on stderr; `--strict`; JSON report with `stopped_at`.
- **Triage:** US-460 is the rule-invisible PASS (it plans test scripts: out of scope). US-430 is rejected and logged, never hand-patched. US-470 is rejected for fences; the hidden content also proposes "within 5 days" (a reviewer who notices this deserves credit). US-48 goes to the backlog owner.
- **Live runs:** fingerprint compared with the scripted run; every finding judged against the story; "one run is one sample" stated.
- **Refinement:** criteria and hypotheses committed before the evaluation output; the v1.1.0 config differs only in `version` and `instructions`; unmoved numbers (S1, R5, Q1) predicted or explained; CHANGELOG evidence per change; a regression pair whose expectations come from the story. "Ship" while the human spot-check is not done should be marked not met.

## Known gotchas
- jsonschema 3.2 on some laptops: `pip install "jsonschema>=4.18"`.
- Run every command from the project folder; `conftest.py` puts it on the path.
- `tests/test_validation.py` fails at collection until `check_input` exists (it gates P01 at import). That is intended: Stage 2 before Stage 3.
- A new regression pair whose story is not in `sim_answers.json` must not be added to `PAIR_CHECKS` unless its reviewed answer is added to `sim_answers.json` too (the solution does this for P07/US-470); otherwise `evaluate.py` raises KeyError.
- `runs/` and `live/*.reply.txt` are git-ignored on purpose; trainees copy what they want to keep into `evidence/`.
- Windows: `echo $LASTEXITCODE` instead of `echo $?`; save replies as UTF-8.
