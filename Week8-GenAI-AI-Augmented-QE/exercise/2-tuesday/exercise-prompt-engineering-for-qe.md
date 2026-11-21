# Exercise: Build a Prompt Library for Test Design and Debugging

**Week 8, Tuesday** | Time box: 2-3 hours | Individual work | Tools: Claude, Python 3.10+, pytest, Git | Mode: Implementation (code lab)

## Objectives
By the end you can:
1. Write acceptance criteria for an AI reply **before** prompting, and turn them into a small scoring script.
2. Refine a prompt from vague to specific **one change at a time**, measuring every version and running the final one more than once.
3. Lock a prompt's output to a JSON contract, validate it defensively, re-ask once on drift, and run the result as parametrized pytest tests.
4. Use few-shot examples to get Gherkin in the team's house style, and detect example leakage.
5. Write a structured debugging request that asks for ranked hypotheses, confirm the cause yourself, and refuse a fix that weakens a test.
6. Store prompts as versioned, reviewed artifacts in Git, with evidence for every version.

## Prerequisites and setup
- Read today's seven lessons in `written/2-tuesday/`. Keep `prompt-engineering-principles.md` sections 3, 7 and 8 and `common-prompt-failure-modes.md` section 6 open while you work.
- Have the Tuesday demo assets to hand: `demos/2-tuesday/code/demo_prompt_engineering_for_qe.md` (the board criteria, the ladder, cards 3.1 to 5.3) and `prompts/coupon-test-ideas.v5.md` (the shape of a library entry).
- Claude open in your browser. Use a plain chat, **not** inside a Claude Project and with any custom instructions or memory switched off, so hidden context does not change your results.
- Python 3.10+ and Git.

1. Copy `starter_code/` to a working folder named `week8-tuesday-<yourname>/`.
2. In that folder: `pip install -r requirements.txt`, then `python -m pytest -q`. Expect **1 failed, 4 passed, 1 skipped**. The failure is intended (Stage 5).
3. `git init`, then commit the starter: `git add . && git commit -m "chore: import ShopFront prompt-library starter"`.
4. Read `README.md` in the starter, then `shopfront/shipping.py` (the same rule you met on Monday).

## Scenario
On Monday you proposed GenAI use cases for the ShopFront QE team. The team lead picked two to trial: **test design** and **debugging**. Before anyone uses Claude for real work, she wants a shared **prompt library**: prompts that are versioned like code, tested like code and come with a way to check their output. "If a prompt does not say how its reply is checked, it does not go in the library."

You will build five library entries:

| ID | Area | What it does | Technique you must use |
|---|---|---|---|
| TD-1 | test design | Test ideas for `shipping_cost` | Specificity ladder, scored by your acceptance criteria |
| TD-2 | test design | Test cases for `shipping_cost` as JSON, run by pytest | Format locking |
| TD-3 | test design | Gherkin for the registration form in the house style | Few-shot |
| DB-1 | debugging | Find the defect behind a failing test | Structured debugging request |
| DB-2 | debugging | Triage a nightly CI run | Format locking plus evidence quoting |

## Rules for using Claude today
1. **Fresh chat for every prompt run**, except a re-ask (Stage 3), which goes into the same chat.
2. **Synthetic material only**: files in `shopfront/`, `tests/` and `materials/`. Nothing from a real system.
3. **Save every reply** in `evidence/`, exactly as it came, named `<prompt file name>.run<k>.txt`.
4. **Measure before you trust.** Every reply is checked with the "Check with" command in its prompt header, then reviewed by you. A check passing is a first filter, not approval.
5. **One change per version.** Never edit a prompt version that already has evidence; copy it to a new version.
6. **Commit as you go**: `prompts: <what changed> (<ID> v<N>)`.
7. Prompt templates with placeholders, JSON Schema and agent instructions are Thursday. If you want them, write the idea in `REFINEMENT-LOG.md` and move on.

## Stage 1: Acceptance criteria first (about 25 min)
1. Read the six numbered sentences in `shopfront/shipping.py`. Write **at least 8** acceptance criteria for a good TD-1 reply in `tools/score_reply.py` (`criteria()` and `INVENTED_RULES`). The docstring lists what they must cover. Copy them into the top of `REFINEMENT-LOG.md` too.
2. **Calibrate your scorer** before using it:
   - `python tools/score_reply.py evidence/calibration/reply_good.txt` must give **full marks**.
   - `python tools/score_reply.py evidence/calibration/reply_bad.txt` must give **2 or less** and report invented rules.
   If either fails, fix the **check**, not the reply. A test that cannot fail, or cannot pass, is useless.
3. Create `prompts/test-design/shipping-test-ideas.v1.md` from `prompts/_TEMPLATE.md`. Its prompt is deliberately vague:

```text
Write some tests for the shipping feature.
```

4. Lint it (`python tools/lint_prompt.py prompts/test-design/shipping-test-ideas.v1.md`), paste it into a fresh Claude chat, save the reply as `evidence/shipping-test-ideas.v1.run1.txt` and score it. Record lint and score in the log. Commit.

Checkpoint: the scorer has 8+ criteria, passes the good reply, fails the bad one, and v1 is scored.

## Stage 2: The TD-1 ladder (about 40 min)
1. Create v2, v3, v4 (and more if needed). Each version copies the previous one and makes **one** change, chosen from the building blocks and dimensions in `prompt-engineering-principles.md` section 3 and `specificity-and-context.md` section 2 (context, technique, quantity, audience, constraints, format, done-criteria, assumptions).
2. Before sending each version, write in the log which criterion you expect the change to fix. Then: lint, fresh chat, save, score, record. Did the criterion flip? Commit each version.
3. When a version reaches full marks, **run it twice more** in fresh chats and score both runs. If any run fails a criterion, the prompt is not done: diagnose with the prompt-debugging checklist (`common-prompt-failure-modes.md` section 6) and make another version.
4. If a criterion keeps failing after two focused changes, decide whether it is an **input problem** or a **model limitation** and write down the check **outside** the model that catches it (for example: recompute the expected values by calling `shipping_cost`).
5. **Human review** of the final version's replies: read every row against the six requirement sentences. Your scorer cannot see a wrong expected value that happens to contain the right number elsewhere. Write what you found in the prompt file's "Review notes".

Checkpoint: at least 4 versions with evidence, a final version scored on 3 runs, and review notes that go beyond the scorer.

## Stage 3: TD-2, format-locked cases run by pytest (about 30 min)
1. Create `prompts/test-design/shipping-cases-json.v1.md`. Lock the output to the contract in `tools/load_shipping_cases.py` (`REQUIRED_KEYS`, `TECHNIQUES`, `ID_PATTERN`), using the techniques in `format-locking.md` section 4.10: explicit format, "ONLY", every key with type and allowed values, delimiters around the requirement, one placeholder shape. If you change the contract, change the constants to match and say so in the header.
2. Implement `validate_cases()` in `tools/load_shipping_cases.py`. Its docstring lists the drift it must catch. Prove it catches drift before you trust it: make a copy of a reply, break it on purpose (a number as a string, `"true"` as a string, a missing key, a wrong technique) and run `python tools/load_shipping_cases.py <copy>`. Keep the broken copy in `evidence/` with `drift-test` in its name.
3. Run the prompt in a fresh chat, save the reply as it came, and load it. If it fails syntax or structure, run with `--reask` and paste the printed message into the **same** chat **once**. If the second reply fails too, stop: record it and change the prompt instead.
4. Run the cases: `python -m pytest -v tests/test_shipping_generated.py --cases evidence/<reply>.txt`.
5. Review **every** case, passing or failing, against the requirement. For each failure decide: is the code wrong, is Claude's case wrong, or is it a question for the product owner? Fill the content-review table in the log. Remember: format OK is not content OK.

Checkpoint: `validate_cases()` rejects your drift-test file with specific messages; a real reply loads and runs in pytest; every case has a verdict.

## Stage 4: TD-3, few-shot Gherkin in the house style (about 20 min)
1. Read `materials/house-style.md` and the two feature files in `materials/features/`.
2. Create `prompts/test-design/registration-gherkin-fewshot.v1.md`: an instruction, **two** delimited examples taken from `materials/features/` (other features, on purpose), then the criteria from `materials/registration-criteria.md`, ending on the same cue the examples use (`few-shot-prompting.md` section 4).
3. Fill `REQUIRED_VALUES` and `LEAK_MARKERS` in `tools/check_gherkin.py` **before** you run the prompt.
4. Run it, save it, check it: `python tools/check_gherkin.py evidence/<reply>.txt`.
5. Read the feature yourself: are the boundary values right (3, 4, 16, 17 characters; ages 15, 16, 99, 100)? Did the search example's "ignores letter case" turn into a registration rule? Make one more version if needed, changing one thing (for example, the example order or a rule line).

Checkpoint: a reply with no leakage and every required value, plus your reading notes in the log.

## Stage 5: Debugging prompts (about 35 min)

### DB-1 structured debugging request
1. Reproduce: `python -m pytest -q tests/test_shipping_buggy.py`. Read the failure yourself and write your own hypothesis in the log **before** asking Claude.
2. Create `prompts/debugging/structured-failure-analysis.v1.md` following `ai-assisted-coding-and-debugging.md` section 5.4. In Claude's chat interface, put the standing rules (role, environment, "Do not rewrite or weaken the test assertions") in a first section headed `## Instructions`, then the request. It must contain the real code, the real test and the **full** pytest output copied from the files and terminal (never retyped), expected vs actual tied to the requirement sentence, what you already tried, and a request for **ranked hypotheses with a way to confirm each, before any fix**.
3. Run it in a fresh chat and save the reply. Confirm the top hypothesis **yourself** with a one-line `python -c "..."` call before touching code. Record the command and output.
4. The weakening trap, while the defect is still there: in a fresh chat send `Make this failing test pass.` followed by the test file and the pytest output. Save the reply. Does it change the test, its expected value, add `xfail`/`skip`, or loosen the comparison? Record your verdict and why you reject it (`ai-assisted-coding-and-debugging.md` section 7.4). This prompt does **not** go into the library; write in the library README why.
5. Now apply the smallest fix to `shopfront/shipping_buggy.py` yourself. Run the full suite. Prove the tests did not change: `git diff --stat` must list only `shipping_buggy.py`. Commit.

### DB-2 CI triage
6. Create `prompts/debugging/ci-failure-triage.v1.md`. Its output must follow the contract in the docstring of `tools/check_triage.py` exactly (copy the contract into your prompt). Paste `materials/ci-failure-sample.txt` inside delimiters.
7. Run, save, then `python tools/check_triage.py evidence/<reply>.txt materials/ci-failure-sample.txt`. The script checks that each quoted evidence line really exists in the log.
8. Review each category yourself in the DB-2 table. A valid triage is not a correct triage: is any failure labelled with confidence where the brief gives no requirement to decide it?

Checkpoint: DB-1 fixed with the test untouched and the weakening reply rejected in writing; DB-2 passes the contract check and every category has your verdict.

## Stage 6: Publish the library (about 15 min)
1. Complete `prompts/README.md`: the index (latest file, technique, output, how it is checked) and at least **three** team rules of your own (what never goes into a prompt, what is never accepted from a reply, when a prompt needs a new version).
2. Lint every final prompt: `python tools/lint_prompt.py prompts/test-design/*.md prompts/debugging/*.md`. Every file must report no `HEADER missing` line. A low lint count is acceptable when you can say why (a debugging prompt does not need an audience line); write the reason in the prompt's review notes.
3. Finish `REFINEMENT-LOG.md` with three bullets you would tell a teammate.
4. Final commit. `git log --oneline` should read like a history of the library.

## Stretch goals
- Add a sixth library entry using the **critique-and-extend** pattern (`ai-assisted-test-design.md` section 11): paste your Stage 3 cases and ask only for missing partitions and boundaries.
- Make TD-2's checks stronger: write a small script that calls `shipping_cost` for every case and reports cases whose `expected` disagrees with the code, so a human only reviews the disagreements.
- Run TD-3 with the two examples in the opposite order and compare (order bias, `few-shot-prompting.md` section 7).
- Mutation check (`ai-assisted-coding-and-debugging.md` section 7.5): change `>= 75` to `> 75` in a copy of `shipping.py` and show which of your TD-2 cases kill the mutant.

## Deliverables
Submit the Git repository `week8-tuesday-<yourname>/` (zip including the `.git` folder, or a pushed branch) containing:
1. `prompts/` with at least TD-1 (v1 and every later version), TD-2, TD-3, DB-1 and DB-2, each with a complete header, and `prompts/README.md`.
2. `evidence/` with every reply, the drift-test file and the weakening-trap reply.
3. `tools/score_reply.py`, `tools/load_shipping_cases.py` and `tools/check_gherkin.py` completed.
4. `shopfront/shipping_buggy.py` fixed, with `tests/` unchanged.
5. `REFINEMENT-LOG.md` completed.
6. A Git history with at least one commit per prompt version.

## Definition of Done
- [ ] `score_reply.py` has 8+ criteria and 4+ invented-rule patterns; good calibration reply scores full marks, bad one scores 2 or less
- [ ] TD-1 has at least 4 versions, each with exactly one stated change, lint and score recorded, and the final version scored on 3 runs
- [ ] Every remaining TD-1 failure is classified as input problem or model limitation, with a named check outside the model
- [ ] `validate_cases()` rejects the drift-test file with one specific message per problem, and a real reply loads and runs in pytest
- [ ] Any re-ask happened once, in the same chat, and its result is recorded
- [ ] Every TD-2 case has a verdict (code right, case wrong, or product-owner question) tied to a requirement sentence
- [ ] TD-3 uses two delimited examples from other features; `check_gherkin.py` reports no leakage and all required values; you checked the boundaries by reading
- [ ] DB-1 asks for ranked hypotheses before a fix; the cause was confirmed by a command you ran; the fix changed only `shipping_buggy.py` and the suite passes
- [ ] The "make it pass" reply was saved and rejected in writing with a reason
- [ ] DB-2 passes `check_triage.py` and every category has your own verdict
- [ ] Every prompt file has a complete header; `prompts/README.md` has the index and 3+ team rules
- [ ] One commit per prompt version with a meaningful message; `pytest -q` shows the suite passing (generated test skipped without `--cases`)
- [ ] No real data, credentials or internal URLs in any prompt; no emojis in any deliverable

## Grading rubric (100 points)
| Criterion | Weight | Full marks when |
|---|---|---|
| Acceptance criteria and scorer | 15 | criteria written before v1, cover the requirement sentences and invented rules, calibrated against both replies |
| TD-1 refinement ladder | 20 | one change per version, prediction before each run, criteria flips recorded, final version stable over 3 runs, input-vs-model diagnosis, review notes beyond the scorer |
| TD-2 format locking | 20 | contract stated completely in the prompt; `validate_cases()` catches every listed drift; re-ask used correctly; every case reviewed and judged against the requirement |
| TD-3 few-shot | 10 | examples from other features, delimited, same cue; leakage and required values checked; boundaries verified by reading |
| DB-1 and DB-2 debugging | 20 | structured request with real artefacts; hypothesis confirmed by the trainee's own command; test untouched; weakening reply rejected with reason; triage contract passed and categories judged |
| Library quality and Git | 15 | complete headers, useful README index and rules, one meaningful commit per version, evidence files match the headers |

## Common pitfalls and hints
- Writing criteria after seeing the reply is not testing. If you change a criterion after Stage 1, say so in the log and why.
- A scorer that only checks `"75" in reply` will pass a reply that mentions 75 once in a sentence. Look at `numbers_in()` and `table_rows()` in the starter, and at how the demo's `prompt_lab.py` scores.
- If two things changed between versions, you cannot say which one helped. Split them into two versions.
- One perfect run is not evidence. A criterion that fails on one run in three is a flaky prompt.
- Money: the boundary below 75.00 is 74.99, not 74. State the precision in the prompt if Claude keeps using whole numbers.
- In Python, `isinstance(True, int)` is `True`. Check booleans before numbers in `validate_cases()`.
- The string `"true"` and the JSON value `true` look alike in a chat window. `json.loads` tells them apart; so must your validator.
- Never "repair" a reply with search-and-replace. Re-ask once with the exact errors, or change the prompt.
- If Claude's few-shot answer contains a value from your example, the example leaked. Change the example or the instruction, not the checker.
- For DB-1, read the code path for an express order of $80.00 in the US, line by line, before asking anything.
- If `check_triage.py` says an evidence line is not in the log, compare it character by character with the log. Paraphrased "quotes" are a form of hallucination.
- Ask for help after 15 minutes stuck, with your last reply and its check output open.

## Reference: where to look (no solutions)
| Need | Look at |
|---|---|
| Building blocks of a prompt; prompt checklist | `prompt-engineering-principles.md` sections 3 and 9 |
| Acceptance criteria and the refinement loop | `prompt-engineering-principles.md` section 7; demo cards 1.1 and 1.2 |
| Versioning prompts, header fields, commit messages | `prompt-engineering-principles.md` section 8; demo `prompts/coupon-test-ideas.v5.md` |
| Dimensions of specificity; the five-iteration ladder | `specificity-and-context.md` sections 2 and 3; demo cards 2.1 to 2.6 |
| Assumptions and clarifying questions | `specificity-and-context.md` section 7 |
| Format-locking techniques, drift, defensive parsing, re-ask | `format-locking.md` sections 4 to 8; demo `load_cases.py`, cards 3.1 to 3.3 |
| Anatomy of a few-shot prompt; leakage and order bias | `few-shot-prompting.md` sections 4, 7, 8 and 12.3; demo cards 4.1 to 4.3 |
| Diagnosing a bad reply | `common-prompt-failure-modes.md` sections 6 and 7; demo card 5.1 |
| Technique-driven test design prompts | `ai-assisted-test-design.md` sections 3, 5 and 11 |
| Structured debugging request; never weaken a test | `ai-assisted-coding-and-debugging.md` sections 5.4 to 5.6 and 7.4; demo cards 5.2 and 5.3 |

## Suggested working order and checkpoints
1. After Stage 1, your scorer must disagree with you on nothing in the two calibration replies.
2. After Stage 2, you can point to the version where each criterion first passed and say which change caused it.
3. After Stage 3, break a reply on purpose; your loader must name the case and the problem.
4. After Stage 5, `git diff` between the starter commit and now shows no change under `tests/`.
5. Before submitting, open `prompts/README.md` as if you were a new teammate: could you use every prompt from it alone?
