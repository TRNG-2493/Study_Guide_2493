# Thursday solution notes (instructors only)

## Exercise mode and scope
Pair programming, design mode (Mode C, design first; implementation is Friday). One shared repository or branch per pair, driver and navigator, swap every 30 minutes (six blocks, 3 hours), commit before every swap, short retrospective. Solvable from Monday to Thursday material: the agent organs, instruction sections, template rules, contract tables, JSON Schema keywords, rule catalogue and sample pairs all come from `written/4-thursday/` and the demo's `anatomy_lab.py`, generalised as `design_lab.py`. No runtime, no validation script and no logs today: those are Friday, and Friday's starter carries this solution forward as the baseline.

## Intentional deviations from the CMA log (do not flag in QA)
- **No Project 2 milestone.** The CMA log and the demo bridge say "a requirements agent for Project 2". By instructor decision, Project 2 is ignored this week: pairs design the agent for the synthetic ShopFront stories used Monday to Wednesday (`materials/inputs/`). Every element of the demo bridge is kept: job sentence and autonomy, anatomy manifest and 12 design questions, nine-section instructions, plain-English contract then Draft 2020-12 schemas, rule catalogue with layers, at least five sample pairs with expectations written first, meaningful commits, AI disclosure.
- **Requirements agent, not the demo's test-case designer.** Pairs design **RequirementReviewer**: one story in, grounded findings with clarifying questions out. It reuses Wednesday's requirements-review vocabulary (five defect categories, quote, question, "ask, never answer"), so the design problem is new but the domain is familiar.
- **Claude as the AI tool.** Block 5 has two Claude steps: a dry run of the pair's own agent (paste `messages --full`, check the reply with `check-output`, apply the rule catalogue by hand) and a design critique. Both end in a written human decision in `evidence/CLAUDE-REVIEW.md`.

## Verified results (Python 3.10, jsonschema 4.26, pytest 9.1)
| Command | Starter | Solution |
|---|---|---|
| `python design_lab.py gate` | DESIGN GATE: FAIL (69 TODOs, all steps fail) | DESIGN GATE: PASS |
| `python -m pytest -q` | 6 failed, 2 passed, 2 skipped | 19 passed, 1 skipped (P04 render skipped by design) |
| `python design_lab.py pairs` | "no sample pairs yet" | 6 pairs, 0 problems, no coverage gaps |
| `python design_lab.py dissect` | 12 GAPs | 0 gaps, every part has an owner |
| `python design_lab.py render materials/inputs/us420.json` | renders (skeleton) | no leftover placeholders; defaults for focus and max_findings come from the input schema |
| `python design_lab.py check-output evidence/dryrun.us420.txt` | n/a | NOT pure JSON (fence), S1 PASS |

`solution/evidence/` holds **backup replies written for the course**, not live Claude output. Use them if Claude is unavailable or to calibrate grading.

## Grading anchors
- **Job sentence:** one job, no "and" (the test enforces it). "Reviews a story and suggests fixes" is two jobs and breaks "ask, never answer".
- **Autonomy:** workflow with a human reviewer. "Autonomous" without a strong reason loses marks.
- **Instructions:** nine sections; a rule with a **reason** for grounding and for not proposing answers; a tie-break for max_findings (highest severity first); an honest path for placeholder stories and out-of-scope requests; data-not-instructions boundary. Weak words inside quoted examples (for example "user-friendly" as an example of a vague word) are acceptable.
- **Contract:** plain English first (CONTRACT.md is graded); `contract_version` const; `status` with `needs_clarification`; `open_questions` required; `additionalProperties: false`; findings with `ac_id`, `quote`, `question` ending in "?". An empty findings list must be legal for a clear story (P02): pairs that make `minItems: 1` on findings lose marks unless they justify a separate status.
- **Rule catalogue:** the key semantic rule is **R3 grounding** (quote must be in the cited AC). Also expected: story id equality, AC existence, id pattern and uniqueness, max_findings, status consistency. Each rule in exactly one layer.
- **Sample pairs:** five categories covered; expectations are properties (MUST, MUST NOT, MAY), written from the story, not copied from a Claude reply. Git history should show pairs committed before `evidence/dryrun.*`.
- **Claude review:** the dry run must be checked with `check-output` and every Code rule applied by hand. Critiques must be accepted or rejected with a reason; accepting the "suggested_ac" idea without discussing "ask, never answer" is a red flag.
- **Pairing:** six rows in the log with commit hashes, both names in `git log`, a retrospective with a real disagreement and how it was settled.

## Rubric weighting rationale
Design quality (contract, instructions, rules, pairs) is 70 of 100 points; the Claude review 15; pairing practice and retrospective 15. Pairs that pass the gate but have weak reasoning (for example rules that are not codeable as written) should not get full marks: the gate checks structure, the grader checks meaning.

## Known gotchas
- jsonschema 3.2 on some laptops: `pip install "jsonschema>=4.18"`.
- Placeholders in the template need either an input value or an input-schema `default`; otherwise render fails loudly with KeyError (intended).
- `$` inside AC text (for example "$50.00") is not a placeholder; the leftover check ignores it.
- The design gate counts every "TODO" in `agent/`, including in the manifest's boundaries list.
- Windows: save JSON as UTF-8.
- If a pair renames schema or template files, `design_parts.py` still finds them as long as there is exactly one `*input*.schema.json`, one `*output*.schema.json` and one template `.txt`.
