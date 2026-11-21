# Tuesday solution notes (instructors only)

## Exercise mode and scope
Mode A (code lab): `starter_code/` scaffold, `solution/` complete. Individual. Time box 2-3 hours: setup 10, stages 25 / 40 / 30 / 20 / 35 / 15 minutes. Solvable from Monday and Tuesday material only (lessons in `written/1-monday/`, `written/2-tuesday/`, demos for both days). It continues Monday's exercise: the same synthetic ShopFront system and `shipping.py`. Prompt templates with placeholders, JSON Schema and agent instructions are deliberately left for Thursday.

## Intentional deviations from the CMA log (do not flag in QA)
- **No Project 2 milestone.** The CMA log says "Build a prompt library for test design/debugging; milestone" and asks for a Project 2 link, and the demo's bridge mentions a `prompts/` folder in the Project 2 repository. By instructor decision, Project 2 is ignored this week: the library lives in the trainee's own exercise repository and targets the synthetic ShopFront code. The deliverable shape (a `prompts/` folder with README, versioned files, headers, evidence, Git history) matches the demo bridge exactly.
- **Claude as the AI tool.** All AI steps are written for Claude's chat interface. Because a chat has no separate system field, DB-1 puts the standing rules in an `## Instructions` section at the top of the message. Trainees use a plain chat (no Project, custom instructions or memory) so hidden context does not affect results.

## Verified results (Python 3.10, pytest 9.1)
| Command (run in `starter_code/` or `solution/`) | Starter | Solution |
|---|---|---|
| `python -m pytest -q` | 1 failed, 4 passed, 1 skipped | 5 passed, 1 skipped |
| `python tools/score_reply.py evidence/calibration/reply_good.txt` | 1/1 + CHECK line | 12/12 |
| `python tools/score_reply.py evidence/calibration/reply_bad.txt` | 0/1 + CHECK line | 0/12, 4 invented rules |
| `python tools/score_reply.py evidence/shipping-test-ideas.v*.txt` | n/a | v1 0, v2 5, v3 10, v4 11, v5 12/12 on runs 1-3 |
| `python tools/load_shipping_cases.py evidence/shipping-cases-json.v1.drift-test.txt --reask` | starter `validate_cases` returns nothing: "Structure: OK" (the point of the TODO) | 8 problems, re-ask message |
| `python -m pytest -q tests/test_shipping_generated.py --cases evidence/shipping-cases-json.v1.run1.txt` | n/a | 9 passed |
| same with `run2.txt` | n/a | 3 failed, 3 passed (format OK, content wrong) |
| same with `drift-test.txt` | n/a | collection error, 0 tests run |
| `python tools/check_gherkin.py evidence/registration-gherkin-fewshot.v1.run1.txt` | CHECK line (constants empty) | all OK, exit 0 |
| `python tools/check_gherkin.py evidence/registration-gherkin-fewshot.v1.leak.txt` | n/a | 8 content FAIL, 3 leak markers |
| `python tools/check_triage.py evidence/ci-failure-triage.v1.run1.txt materials/ci-failure-sample.txt` | same tool | Contract: OK |
| same with `run2.txt` | n/a | 3 problems (paraphrased evidence, missing and mistyped test id) |
| `python tools/lint_prompt.py prompts/test-design/*.md prompts/debugging/*.md` | n/a | TD-1 v1 1/9 to v5 9/9; no HEADER lines |

All files in `solution/evidence/` are **backup replies written for the course**, not live Claude output. Use them when Claude is unavailable, to show the class a drift or leak case, or to calibrate grading. Trainees' own evidence must be real replies.

## The DB-1 defect
`shipping_buggy.py` adds the express surcharge **before** the free-shipping rule, so `charge = 0.0` overwrites it on US orders of $75.00 or more. Only `test_us_express_on_free_order` fails. Fix: move the express block after the free-shipping rule (solution file shows it). The weakening trap is tempting here because Monday's backup Claude draft asserted exactly the wrong behaviour (express on a free order stays free); a "make it pass" reply usually changes the expected value to 0.0 or adds `xfail`.

## Grading hints
- **Criteria before prompting** is the core habit. Look at the Git history: `score_reply.py` should be committed before `shipping-test-ideas.v1.run1.txt`.
- One change per version: diff consecutive TD-1 versions. Several changes in one version lose ladder marks unless the log explains it.
- Scores will differ from the exemplar; live Claude often reaches full marks earlier (v3 or v4). That is fine if the log records it and the three-run check is done.
- Reward trainees who notice their scorer is wrong (false pass or false fail) and say so; the exemplar log shows two such cases. Penalise editing the calibration replies to make the scorer pass.
- `validate_cases()` must catch bool-as-number and `"false"`-as-boolean. Many first attempts miss `isinstance(True, int)`.
- TD-2 content review: the three run2 verdicts in `REFINEMENT-LOG.md` are the target reasoning. "Edit the code to match Claude" or "edit the case to match the code" without a requirement sentence loses marks; lower-case `us` must be a product-owner question.
- TD-3: examples must come from `materials/features/` (other features). Using a registration example defeats the exercise. A trainee who keeps the "ignores letter case" search scenario and then catches the leak deserves full marks.
- DB-1: the confirmation command must be the trainee's own run with pasted output; `git diff --stat` must show no change under `tests/`.
- DB-2: the search failure should end as `needs_clarification` after human review even if Claude says `product_bug`.
- Linter: it is tuned to test-design prompts. Debugging prompts legitimately score 3-5/9 (no audience, "triage" is not in the verb list). Accept a low lint with a one-line reason in the review notes.

## Known gotchas
- Run every command from the folder holding `pytest.ini`; `conftest.py` adds `shopfront/` and `tools/` to the path.
- Windows editors may save replies as UTF-16 or with smart quotes; save as UTF-8. Smart quotes break `json.loads` (syntax drift, a real lesson).
- Claude sometimes returns the JSON inside a code fence even when told not to; `extract_json` tolerates it by design.
- In DB-2 the evidence check is a substring match against stripped log lines; a reply that quotes a line with the leading "- " removed still passes. That is intended.
- If a trainee's v1 reply is already good (Claude with memory or a Project), have them start a plain chat; if it is still good, the ladder still has value because the three-run stability check is what matters.
