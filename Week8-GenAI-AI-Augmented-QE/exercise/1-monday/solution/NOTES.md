# Monday solution notes (instructors only)

## Exercise mode and scope
Mode B (design and analysis) with one small deterministic check, so the folder uses `templates/` rather than `starter_code/`. Time box 2-3 hours: setup 10, stages 25 / 20 / 20 / 25 / 40 / 25 / 15 minutes. Solvable from Monday material only (six lessons in `written/1-monday/` and the demo in `demos/1-monday/`); no later-week technique is required. Prompt engineering is explicitly deferred to Tuesday.

## Intentional deviations from the CMA log (do not flag in QA)
- **No Project 2 milestone.** The CMA log asks for "three GenAI use cases for Project 2" and a Project 2 milestone section. By instructor decision, Project 2 is ignored for this week's exercises: there is no Project 2 milestone section. To keep the CMA intent (use cases tied to a real part of a test automation framework), trainees target the synthetic **ShopFront** framework described in `templates/system-brief.md`, which mirrors the Week 4-7 framework and the demo's "generic web app".
- **Claude as the AI tool.** All AI steps are written for Claude (fresh chat per prompt, prompts to paste, what to capture, how to validate). Every Claude output must be reviewed by the trainee with the five review questions from the demo; at least one must be proved by code or a tool.

## Files
| File | Purpose |
|---|---|
| `rank_use_cases.py` | Completed exemplar with eight candidates and verified sensitivity notes. Run: `python rank_use_cases.py` and `python rank_use_cases.py --weight verifiability=0`. |
| `sample-use-case-brief.md` | Expected tool choices for the brief's pain points, three exemplar cards, rejected candidates, and the Claude faults trainees should catch. |
| `checks/shipping.py` | Copy of `templates/materials/shipping.py` so the checks run in place. |
| `checks/test_shipping_reviewed.py` | Reference human-reviewed tests: **17 passed** (verified). The last comment block shows the open question on lower-case country codes. |
| `checks/test_shipping_ai_draft.py` | Backup "Claude draft" if the tool is unavailable: **3 failed, 3 passed** (verified). Failures: express on a free order, case-insensitive country (invented), unknown country returns 0. |
| `checks/check_registration_data.py` | Reference rules checker for the data probe. |
| `checks/sample_ai_registration_data.csv` | Backup "Claude CSV": the checker reports **3 mislabelled rows** (verified): `bob` (3 chars), `emma_w` (underscore), `gina@gmail.com` (domain), exit code 1. |

Verified on Python 3.10 with pytest 9.1. Run from `checks/`: `python -m pytest -q test_shipping_reviewed.py`, `python -m pytest -q test_shipping_ai_draft.py`, `python check_registration_data.py sample_ai_registration_data.csv`. The template `templates/rank_use_cases.py` deliberately prints a `CHECK` line and exits 1 until trainees add six candidates with reasons.

## Grading hints
- **Verification is the centre of the grade.** "Who verifies" must be a role and "how" a concrete check with a time. "The team reviews it" earns little.
- Tool choice: pain point 8 must not be GenAI-first (unlabelled volume: clustering / TF-IDF), 9 is supervised classification (labels exist), 10 is No AI. These are the "rejected" rows most trainees should find.
- Failure modes must be traced to the right mechanism: invented rule or flag = hallucination; different answers per run = sampling / non-determinism; outdated API = knowledge cut-off; ignores the team's conventions = only sees the context window; miscounted characters = tokens are not characters.
- Evidence log: replies must be pasted in full. A review that only says "looks good" for all five questions should lose most of the evidence marks, especially if the reply contains a fault listed in `sample-use-case-brief.md`.
- Deterministic check: it must have actually run (pasted output). If a trainee's Claude tests all pass, full marks still require them to note missing boundaries.
- Research: a Claude-suggested source logged as "hallucinated" is a positive finding, not a penalty. Penalise sources that were clearly never opened.
- Claude challenge: a mix of accepted and rejected critiques with reasons is the target. Accepting everything without updating the cards, or rejecting everything without reasons, loses marks.
- Scores may differ from the exemplar. Accept any score whose reason is plausible; challenge scores that contradict their own reason (for example verifiability 5 with "hard to check").

## Known gotchas
- Claude may answer the Stage 1 prompt with features that are not in the brief (mobile app, payment gateway logs, A/B testing). These must be marked "invented feature".
- Trainees sometimes paste their entire previous chat into the next prompt. Insist on a fresh chat per prompt.
- Data probe replies often include prose or code fences around the CSV, or rename a header column. The reference checker reports a bad header; trainees should treat this as format drift (a Tuesday topic) and fix the file by hand before checking.
- `shipping_cost` returns floats; comparing `== 5.99` is safe here because of `round(..., 2)`, but trainees who question float equality deserve credit.
- In `ci-failure-sample.txt` the search failure is deliberately ambiguous: the expected message text is not specified in the brief, so "product bug or test bug" is a question for the product owner. The pagination failure (21 vs 20) looks like an off-by-one product bug; the checkout failure is the disabled-button case from the demo (card 2.7).
- `bug-notes.txt` contains two separate issues (discount kept below minimum spend; email accepted without validation). A good review flags a Claude report that merges them or turns "I think $60" into a fact.
- Trainees may try to improve prompts. Allow a note on the Tuesday list; keep the graded prompts plain.
