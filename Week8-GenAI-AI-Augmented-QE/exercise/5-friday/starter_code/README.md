# Starter: RequirementReviewer, built (Week 8, Friday)

This is Thursday's RequirementReviewer design (the instructor solution) carried forward as the
baseline, plus the runtime around it. Today you implement the parts marked TODO, run the agent
against a backlog, and refine it with numbers.

```
pip install -r requirements.txt          # jsonschema 4.18+ and pytest
python rr_lab.py check                    # environment, start-up, and which test files still fail
```

| Path | What it is | Edit? |
|---|---|---|
| `agent.json` | Pins every moving part (instructions, template, contract, settings) | Copy for v1.1.0 (Stage 6) |
| `agent/` | Thursday's design: CONTRACT.md, schemas, template, rules.md, samples P01-P06, manifest | Add regression pairs (Stage 6) |
| `instructions/rr_instructions_v1.0.0.md` | Thursday's instructions, versioned | Never edit; v1.1.0 is a new file |
| `instructions/rule_map_v1.0.0.json` | Rule-to-check map (5 of 15 entries) | Yes: Stage 1 |
| `instructions/CHANGELOG.md` | Version history with evidence | Yes: Stage 6 |
| `rr/instructions.py`, `rr/templates.py`, `rr/model.py`, `rr/agent.py` | Loader, renderer, model clients, the wired agent | No (read them) |
| `rr/contract.py` | The four enforcement points | Yes: Stage 2 |
| `rr/validation.py` | R1-R7, Q1-Q2; `validate_reply` is provided | Yes: Stage 3 |
| `validate_output.py` | The validation script (exit codes 0, 1, 2) | Yes: Stage 4 |
| `tests/test_contract.py` | Contract tests | No: make them pass |
| `tests/test_validation.py`, `tests/test_cli.py` | Tests for the validator | Yes: Stages 3 and 4 |
| `run_requirements.py`, `trace_matrix.py`, `rr_lab.py` | Run a backlog, trace, print a prompt for Claude | No |
| `requirements/backlog.csv`, `replies/` | The backlog and the scripted (illustrative) replies | No |
| `evaluate.py` | Seeded evaluation; `PAIR_CHECKS` for P01 only | Yes: Stage 6 |
| `show_failures.py`, `check_pairs_rules.py`, `check_rule_map.py`, `check_versions.py` | Refinement and consistency tools | No |
| `rr/simulated.py`, `sim_answers.json` | Simulated model for evaluation (illustrative rates) | No; do not read `MISTAKES` before your error analysis |
| `REPORT.md` | Your report | Yes |

Run every command from this folder.
