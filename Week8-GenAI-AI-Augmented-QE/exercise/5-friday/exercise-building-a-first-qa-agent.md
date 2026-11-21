# Exercise: Build, Validate, Run and Refine Your First QA Agent

**Week 8, Friday** | Time box: 2-3 hours | Individual work | Tools: Claude, Python 3.10+, jsonschema 4.18+, pytest, Git | Mode: Implementation (code lab)

## Objectives
By the end you can:
1. Run an agent whose every moving part is pinned in `agent.json`, and show that it refuses to start with a broken instruction file, template pin or contract version.
2. Keep instructions and checks honest with a rule-to-check map and a version check.
3. Implement an IO contract at four enforcement points: input gate with defaults, strict parse, output schema gate, typed objects.
4. Implement every rule in the catalogue as code, and prove each one with a planted-defect test that fires exactly that rule.
5. Wrap validation in a command-line script with exit codes 0, 1 and 2, findings on stdout, problems on stderr and a JSON report.
6. Execute the agent against a backlog, re-check the evidence independently, triage every outcome with an owner, and review live Claude replies yourself.
7. Refine the agent with numbers: test the test data, baseline over seeded runs, analyse failures, write hypotheses first, change one versioned file, re-evaluate with the same seeds, and decide whether to ship against criteria set in advance.

## Prerequisites and setup
- Read today's seven lessons in `written/5-friday/`. Keep `agent-output-validation.md`, `building-validation-scripts.md` and `agent-testing-and-refinement.md` open.
- Have the Friday demo to hand: `demos/5-friday/demo-script.md` and its `code/` folder (`tcd/contract.py`, `tcd/validation.py`, `validate_output.py`, `evaluate.py`). Today's starter has the same structure for a different agent, so the demo is your model, not your answer.
- Claude in a plain chat (no Project, custom instructions or memory), a fresh chat for every live run.

1. Copy `starter_code/` to `week8-friday-<yourname>/`, `pip install -r requirements.txt`, `git init`, commit the starter.
2. `python rr_lab.py check`. Expected: environment OK, `agent.json assembles` OK, and all three test files MISSING. That is today's work.
3. Read `README.md`, then `agent.json`, `rr/agent.py` and `agent/rules.md` before writing any code.

## Scenario
On Thursday your pair designed **RequirementReviewer**: one user story in, grounded requirement findings with clarifying questions out. The team lead accepted the design (the starter carries the reference design forward so that everyone starts from the same baseline). Today it has to work: every reply checked by a script a CI job can trust, a run against the ShopFront backlog, and a measured improvement she can show the team. Her rule for the day: **"If we cannot measure it, we did not improve it. If no human looked at it, we did not ship it."**

## Rules for today
1. **Never repair a reply.** `run()` never strips fences, retries or edits. A failure is rejected and counted. Retries are Week 9.
2. **Never edit a released file.** v1.0.0 instructions stay as they are; refinement goes into a new file and a new `agent_v1.1.0.json`.
3. **Expected results first.** Pair checks, hypotheses and ship criteria are written before you run the numbers they judge. Your commit order is the evidence.
4. **Live Claude runs** (Stage 5): print the prompt with `rr_lab.py`, paste it as one message into a fresh chat, save the reply exactly as it came, then let the agent validate it. Review every live reply yourself against the story.
5. **Using Claude as a coding assistant is allowed** for Stages 2 to 4, on these conditions: paste only the file you are working on and `agent/rules.md`; never paste anything outside the repository; read and run every line before committing; your planted-defect tests are the gate; mark such files with a disclosure line, for example `# AI-assisted: Claude drafted check_r4; reviewed and tested by <you> <date>`.
6. Commit at least once per stage with a message that names the organ: `validation: implement R3 grounding with normalised quotes`.

## Stage 1: Start-up checks and the rule map (about 15 min)
1. Prove the agent fails fast. Make each change in a copy of `agent.json` (for example `tmp_agent.json`), try to construct `RequirementReviewer(ScriptedModel(), "tmp_agent.json")`, record the error, then delete the copy:
   - instructions pointing at a copy of the instruction file with one heading renamed;
   - a template pin that does not exist;
   - `contract_version` "1.1.0".
2. Complete `instructions/rule_map_v1.0.0.json` so that every bullet in Rules, Output, Uncertainty and Escalation and Boundaries is mapped to the checks that verify it (`S1`, `R1`-`R7`, `Q1`, `Q2` or `HUMAN`). `python check_rule_map.py instructions/rr_instructions_v1.0.0.md instructions/rule_map_v1.0.0.json` must report 0 problems. A rule mapped only to `HUMAN` is a conscious decision: be ready to say why.
3. `python check_versions.py` must say AGREE. Record the three refusals in `REPORT.md` section 1. Commit.

## Stage 2: The contract, four enforcement points (about 25 min)
1. In `rr/contract.py`, read `INPUT_DEFAULTS` from the input schema (one fact, one place), then implement `check_input`, `parse_reply` and `check_output_schema` as their docstrings and TODOs describe. Collect every problem, not just the first.
2. `python -m pytest -q tests/test_contract.py` must pass (18 tests). If a test fails, read its name and assertion before changing code.
3. Commit.

## Stage 3: Validation, one rule at a time (about 35 min)
1. Implement `check_r1` to `check_r7`, `check_q1` and `check_q2` in `rr/validation.py`, exactly as `agent/rules.md` describes them. Read `validate_reply` first: it decides that rules only run after the shape passed, and that warnings never fail a reply.
2. Write the planted-defect tests in `tests/test_validation.py`: one minimal mutation of the P01 reference answer per rule. Each must fire **exactly** its own rule. If a mutation fires two rules, change the test data, not the rule.
3. Pay special attention to R3 (grounding): it is the heart of this agent. The catalogue says case-insensitive, whitespace collapsed, curly quotes normalised. Test that a quote with different case and spacing still passes.
4. `python -m pytest -q tests/test_validation.py` must pass. Commit.

## Stage 4: The validation script (about 20 min)
1. Implement `main()` in `validate_output.py`. The TODO block is the script's contract: exit 0 all valid, 1 at least one reply failed, 2 the check could not run (bad arguments, unreadable files, an invalid input story, nothing to check). Problems that stop the check go to stderr; findings go to stdout. `--strict` turns warnings into failures; `--json FILE` writes a report.
2. Add the three tests listed in the TODO in `tests/test_cli.py`.
3. `python -m pytest -q` must now pass everything; `python rr_lab.py check` must show three OK lines. Commit.

## Stage 5: Execute against the backlog (about 25 min)
1. `python run_requirements.py requirements/backlog.csv --run-id day1`. Read the table: how many stories, how many model calls, and why are they different?
2. Re-check the evidence independently: `python validate_output.py --run runs/day1`, then check the exit code (`echo $?`, or `echo $LASTEXITCODE` in PowerShell). Does it agree with `runs/day1/run.jsonl`?
3. Open every reply in `runs/day1/` and fill the triage table in `REPORT.md` section 3: outcome, action, owner (agent owner, backlog owner, story tester or product owner). At least one PASS reply is wrong in a way no rule can see: find it.
4. `python trace_matrix.py runs/day1` and write one takeaway.
5. **Live Claude runs, two stories.** For US-470 and one other valid story of your choice:
   - `python rr_lab.py prompt US-470`. Note the fingerprint: it must match the `day1` line for that story.
   - Paste everything between the lines as one message into a fresh Claude chat. Save the reply exactly as it came as `live/US-470.reply.txt` (UTF-8).
   - `python run_requirements.py requirements/backlog.csv --run-id live1 --model saved --only US-470,<other>` and `python validate_output.py --run runs/live1`.
   - Review each live reply yourself against the story (Q3): which findings are correct, which are wrong or invented, what is missing? Fill `REPORT.md` section 4. One run is one sample: say so.
6. Commit (the `runs/` folder is ignored; copy `runs/day1/run.jsonl` and your live replies into an `evidence/` folder and commit those).

## Stage 6: Refine with numbers (about 40 min)
1. **Test your test data.** `python check_pairs_rules.py`. Record the result. A reference answer that fails a rule is a bug in the oracle.
2. **Executable expectations.** In `evaluate.py`, write `PAIR_CHECKS` for P02, P03, P05 and P06 from their MUST and MUST NOT lists, in the style of P01.
3. **Ship criteria first.** Write your ship criteria in `REPORT.md` section 6 now (for example an overall target, "no pair worse", a target for the out-of-scope pair, the regression suite, a human spot-check). Commit before measuring.
4. **Baseline.** `python evaluate.py` (20 seeded runs per pair). Save the output. The model is a simulator with mistake rates chosen for teaching: the numbers are not facts about Claude; the method is the lesson.
5. **Read the failures.** `python show_failures.py agent.json P01`, then the pairs with the lowest scores. Group the failures by root cause and count them. Only now may you read `rr/simulated.py` to check your analysis.
6. **Hypotheses before edits.** Write H1, H2, ... in `REPORT.md`: which instruction change should move which rule or check, in which direction, and which numbers should NOT move (for example format drift, which no instruction fixes). Commit.
7. **One versioned change.** Copy the instructions to `instructions/rr_instructions_v1.1.0.md` (header Version 1.1.0, contract still 1.0.0) and add the rules your hypotheses need. Copy `agent.json` to `agent_v1.1.0.json` and change only `version` and `instructions`. Write `instructions/rule_map_v1.1.0.json` and get `check_rule_map.py` to 0 problems on the new file.
8. **Same suite, same seeds.** `python evaluate.py --config agent_v1.1.0.json`. Fill the before/after table: which hypotheses were confirmed, which numbers moved that you did not expect, is any pair worse?
9. **Record.** Add a 1.1.0 entry to `instructions/CHANGELOG.md` with the evidence for every change. Turn at least one real failure from Stage 5 into a new sample pair in `agent/samples/` (expectations from the story, never from the failing reply), and confirm `check_pairs_rules.py`, `check_versions.py` and `pytest` still pass.
10. **Decide.** Compare the results with your ship criteria. "Ship" with an unmet human spot-check is not "ship".

## Stage 7: Report and wrap-up (about 10 min)
Complete `REPORT.md`. `git log --oneline` should show criteria and hypotheses committed before the numbers they judge.

## Stretch goals
- Add a rule B1 that flags instructions hidden in a finding (for example "ignore your rules"), with an ID, a layer, a catalogue row and a planted-defect test.
- Run `evaluate.py --runs 50` for both versions. Do the conclusions hold? Which pair's score moves most between 20 and 50 runs, and why?
- Make a second refinement for one number that did not move. If no instruction can move it (format drift), write how a Week 9 retry could, without implementing it.
- Run the live Claude prompt for US-470 three times and compare the findings. Which ones appear every time?

## Deliverables
The Git repository `week8-friday-<yourname>/` containing:
1. `rr/contract.py`, `rr/validation.py`, `validate_output.py` implemented; `tests/` complete and passing.
2. `instructions/rule_map_v1.0.0.json` complete; `instructions/rr_instructions_v1.1.0.md`, `rule_map_v1.1.0.json`, `agent_v1.1.0.json`; `instructions/CHANGELOG.md` with a 1.1.0 entry.
3. `evaluate.py` with `PAIR_CHECKS` for every valid pair; at least one new regression pair in `agent/samples/`.
4. `evidence/` with the `day1` run record, your live Claude replies and the two evaluation outputs.
5. `REPORT.md`, all six sections complete.

## Definition of Done
- [ ] Three start-up refusals demonstrated and recorded
- [ ] `check_rule_map.py` reports 0 problems for v1.0.0 and v1.1.0 with their maps; `check_versions.py` says AGREE for both configs
- [ ] `python -m pytest -q` passes; `python rr_lab.py check` shows three OK lines
- [ ] Every catalogue rule (R1-R7, Q1, Q2) has a planted-defect test that fires exactly that rule
- [ ] `validate_output.py` returns 0, 1 and 2 in the right cases, writes problems to stderr and a JSON report on request
- [ ] Backlog run recorded; independent re-check agrees; every story triaged with an action and an owner; the PASS that no rule can catch is identified
- [ ] Two live Claude replies saved unedited, validated by the agent, and reviewed by you finding by finding
- [ ] Ship criteria and hypotheses committed before the numbers they judge
- [ ] Baseline and v1.1.0 evaluated with the same seeds; before/after table with confirmed and unconfirmed hypotheses; no unexplained pair got worse
- [ ] v1.0.0 files unchanged; v1.1.0 is a new instruction file and a new config differing only in version and instructions
- [ ] CHANGELOG entry with evidence; at least one regression pair from a real failure
- [ ] Ship decision against the criteria; AI-assisted code disclosed; no real data in any prompt; no emojis in any deliverable

## Grading rubric (100 points)
| Criterion | Weight | Full marks when |
|---|---|---|
| Start-up and instruction checks | 10 | three refusals shown; rule map complete with conscious HUMAN entries; versions agree |
| Contract implementation | 15 | defaults read from the schema; all problems collected; strict parse; contract tests pass without being edited |
| Validation rules and their tests | 20 | every rule matches the catalogue (R3 normalisation included); one minimal planted defect per rule firing exactly that rule |
| Validation script | 10 | exit-code contract honoured including "nothing to check"; stdout/stderr split; strict and JSON report tested |
| Execution and human review | 15 | run recorded and re-checked; triage with owners; the rule-invisible PASS found; two live Claude replies reviewed finding by finding, fingerprints compared |
| Refinement with evidence | 25 | test data tested; executable pair checks; criteria and hypotheses before numbers; one versioned change; same-seed comparison read honestly (including what did not move); CHANGELOG and regression pair |
| Report and professional habits | 5 | concise, evidence-based report; meaningful commits; disclosure |

## Common pitfalls and hints
- `{**INPUT_DEFAULTS, **story}` and `{**story, **INPUT_DEFAULTS}` are not the same. Which one lets the caller's `max_findings` win?
- `iter_errors` returns every schema problem; `validate` raises on the first. The tests expect all of them.
- A reply that starts with a code fence is a contract break, even if the JSON inside is perfect. Count it; do not strip it.
- R3 compares the quote with the text of the AC named in `ac_id`, not with the whole story. Normalise both sides the same way.
- R4 has three ways to fail: duplicate id, wrong story number, a gap in the sequence. One finding should produce one message.
- R6 depends on `status`: write down both branches before coding.
- R7 needs the gated story: `focus` exists only after defaults are applied.
- Q1 must not warn about numbers the story already contains ("16 characters", "30 days").
- A planted mutation that fires two rules usually means the mutation changed two things. Copying a finding changes its quote too.
- `return 2` for "nothing to check" matters: a validator that checks nothing and exits 0 is a silent pass in CI.
- If v1.1.0 makes a pair worse, do not hide it. Explain it, or change one thing and measure again.
- The simulator recognises rules by their meaning, written in ordinary words. Write rules a human reviewer would understand; do not tune wording to the simulator.
- Ask for help after 15 minutes stuck, with the failing test and its output.

## Reference: where to look (no solutions)
| Need | Look at |
|---|---|
| Job card, rule-to-check map, desk-check, loading safely | `building-agent-instructions.md` sections 4, 12 and 13; demo cards 1.1 to 1.4 |
| Template library, pinning, strict rendering | `creating-reusable-prompt-templates.md`; demo cards 2.1 to 2.5 |
| Four enforcement points, defaults, strict parse, version agreement | `implementing-io-contracts.md` sections 3 to 9; demo `tcd/contract.py`, cards 3.1 to 3.5 |
| Fail fast then collect all; three verdicts; limits of validation | `agent-output-validation.md` section 5 and 6; demo `tcd/validation.py`, cards 4.1 and 4.2 |
| Exit codes, stdout/stderr, JSON report, testing the validator | `building-validation-scripts.md` sections 4 to 7; demo `validate_output.py`, `tests/test_validation.py`, cards 4.3 and 4.4 |
| Backlog to input contract, run records, fingerprints, triage, traceability | `executing-agents-against-qa-requirements.md` sections 3 to 9; demo cards 5.1 to 5.4 |
| Test the pairs, baseline, error analysis, hypotheses, versioned change, ship decision | `agent-testing-and-refinement.md` sections 3 to 8; demo cards 6.1 to 6.6 |
| The agent's rules and contract | `agent/rules.md`, `agent/CONTRACT.md` (Thursday) |

## Suggested working order and checkpoints
1. After Stage 2: `tests/test_contract.py` green before any rule is written.
2. After Stage 3: break each rule on purpose in the code; exactly one planted test should go red.
3. After Stage 4: `python validate_output.py --run empty_folder` prints to stderr and exits 2.
4. After Stage 6: you can point at the line in v1.1.0 that moved each number, and at the number that did not move and why.
