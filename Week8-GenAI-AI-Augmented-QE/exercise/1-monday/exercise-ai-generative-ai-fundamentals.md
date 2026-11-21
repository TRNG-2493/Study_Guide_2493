# Exercise: Research and Present Three GenAI Use Cases for a Test Automation Framework

**Week 8, Monday** | Time box: 2-3 hours | Individual work (Stage 7 in small groups) | Tools: Claude, Python 3.10+, a text editor | Mode: Design and analysis (with one small code check)

## Objectives
By the end you can:
1. Map candidate AI tasks onto the STLC activities of a real-looking test automation framework.
2. Decide, with a stated reason, whether a task needs no AI, classic ML/NLP or Generative AI.
3. Score and rank GenAI use cases on value, frequency, verifiability, risk and data sensitivity, and explain how the ranking changes when verifiability is ignored.
4. Trace each use case's risks back to how an LLM works (sampling, next-token prediction, context window, knowledge cut-off).
5. Gather evidence with Claude for each use case, review every reply with the five review questions, and prove at least one reply right or wrong with deterministic code.
6. Present three ranked use cases, each with a named human verifier and a concrete verification method.

## Prerequisites and setup
- Read today's six lessons in `written/1-monday/`, especially `generative-ai-applications-within-qe.md` (sections 2, 5, 6 and 7).
- Have the Monday demo assets to hand: `demos/1-monday/code/demo_ai_generative_ai_fundamentals.md` (the five review questions, cards 2.2 to 2.8) and `llm_mechanics_lab.py rank`.
- Claude open in your browser, signed in. You will start a **fresh chat for every prompt**.
- Python 3.10+. `pytest` only if you choose a test-drafting probe in Stage 5 (`pip install pytest`).

1. Create a folder `week8-monday-<yourname>/` and copy the whole `templates/` folder into it.
2. Read `templates/system-brief.md` end to end (5 minutes). This synthetic system is the only target for today.
3. Run `python rank_use_cases.py` inside your copy. It should print one example row and a `CHECK` line saying you need at least 6 candidates. That is expected.

## Scenario
You have just joined the QE team that maintains the test automation framework for **ShopFront**, a small web shop (the same kind of shop and framework you worked on in Weeks 4 to 7). The team lead has been asked by management "where can we use GenAI?" and has handed the question to you. She wants **three** use cases she can trial next sprint, ranked, each with a named reviewer, a way to check the output and an honest list of what could go wrong. She has also warned you: "If you cannot tell me who checks it and how, it is not a use case yet."

Everything you need is in `templates/system-brief.md` and `templates/materials/`. All of it is synthetic, so you may paste it into Claude. Nothing else may go into a prompt.

## Rules for using Claude today
1. **Fresh chat per prompt.** The model has no memory between requests; an old conversation silently changes the context (`generative-ai-concepts.md`, section 6).
2. **Synthetic material only.** The system brief and `materials/`. No real logs, names, credentials, tokens or internal URLs.
3. **Plain prompts.** Use the prompts below as written, or write your own in the same plain style. Do not add roles, examples or output formats to "improve" them; that is Tuesday. Write any improvement idea in the "Tuesday list" of your evidence log.
4. **Log everything.** Every prompt and full reply goes into `claude-evidence-log.md` with a five-question review. A reply that is not reviewed does not count as evidence.
5. **Claude never decides.** Claude may suggest, draft and criticise. You choose, score, rank and sign off, and you say why.

## Stage 1: Build a long list (about 25 min)
1. Without AI, write at least **6** candidate tasks in Part A of `candidate-longlist.md`. Name the ShopFront part and the STLC activity for each. Use the pain points in the brief (section 3) and the STLC table in `generative-ai-applications-within-qe.md` section 2.
2. Open a fresh chat and send this prompt, pasting the full text of `system-brief.md` where shown:

```text
Here is a description of a web shop and its test automation framework.

<paste the full contents of system-brief.md here>

List 10 tasks in this team's testing work where generative AI could help.
For each task, name the testing activity it belongs to, in one line.
```

3. Copy only the **new** ideas into Part B. For each one, validate it against the brief: does it rely on a feature, tool or data source that the brief does not mention? Mark it "invented feature" if so. Do not keep ideas you cannot tie to the brief.
4. Make sure Parts A and B together cover at least **5** different STLC activities.
5. Write the Part C reflection.

Checkpoint: at least 9 candidates in total, at least 5 STLC activities, every Claude idea has a validation mark.

## Stage 2: Choose the right tool (about 20 min)
1. In `tool-choice-worksheet.md`, decide for **every** candidate: No AI, Classic ML (say supervised or unsupervised, and which task: classification, regression, clustering, anomaly detection), Classic NLP, or GenAI.
2. Give one sentence of reasoning per row that names the deciding property: is it a deterministic rule? are there labels? how much data and how often? does it need language or code? can a human check it?
3. Fill the "Rejected for GenAI" table with at least two candidates: at least one that should be **No AI** and at least one that should be **Classic ML/NLP**. Pain points 8, 9 and 10 in the brief are good places to look.
4. No Claude in this stage. This is your judgement, using the decision flow in `supervised-vs-unsupervised-learning.md` section 6 and `nlp-fundamentals.md` section 10.

Checkpoint: at least 6 candidates remain marked GenAI.

## Stage 3: Score and rank (about 20 min)
1. Add at least **6** GenAI candidates to `CANDIDATES` in `rank_use_cases.py`. Score each criterion 1 to 5 and write a short reason for **every** score in `why`.
2. Run `python rank_use_cases.py` until it prints no `CHECK` lines and exits cleanly.
3. Run the sensitivity experiment: `python rank_use_cases.py --weight verifiability=0`. Record both top-3 lists and what moved in the `SENSITIVITY NOTES` block at the bottom of the script.
4. Pick your **three** use cases. You may override the ranking, but you must write why in `use-case-card.md` ("Ranking decision").

Checkpoint: the script runs clean; the sensitivity notes explain in your own words why verifiability matters so much in QE.

## Stage 4: Research (about 25 min)
1. For each of your three use cases, find at least one credible external source that supports a claim you will make (what the technique is, how teams use it, a known risk). Course lessons may be added as extra sources.
2. You may ask Claude for sources. If you do, use a fresh chat and this prompt:

```text
I am evaluating this use of generative AI in software testing: <one-line use case>.
Suggest three published sources (official documentation, standards bodies or well-known
engineering publications) that discuss it. Give the title, publisher and URL for each.
```

3. **Open every source yourself**, whichever way you found it. Record in `research-log.md` whether it exists and says what you claim. A Claude-suggested source that does not exist, or that does not say what Claude claimed, is a hallucination: log it as one in the evidence log. It is good evidence for your presentation.
4. Complete the "Hype check" in `research-log.md`.

Checkpoint: three verified sources (one per use case) and one classified hype claim.

## Stage 5: Gather evidence with Claude (about 40 min)
For **each** of your three use cases, run one plain prompt that tries the use case on the synthetic material, **twice in two fresh chats**. Review every reply with the five questions in `claude-evidence-log.md`, then fill in the run-to-run comparison.

Use one of these probes where it fits your use case, or write your own plain prompt in the same style.

| If your use case is about... | Material to paste | Plain prompt |
|---|---|---|
| Requirements review | one story from `materials/user-stories.md` | "List the ambiguities and missing details in this user story. For each one, write the question a tester should ask the product owner." |
| Test design / test code | `materials/shipping.py` | "Write pytest unit tests for this function. Put them in one file named test_shipping_ai.py." |
| Test data | the "Registration rules" table from `materials/user-stories.md` | "Generate 12 synthetic registration records as CSV with the header username,email,age,country,marketing_opt_in,expected_valid. Follow these rules for valid records and include some invalid ones and boundary values. Output only the CSV." |
| Debugging / CI triage | `materials/ci-failure-sample.txt` | "Explain the most likely cause of each failure in this test run and say whether it looks like a product bug or a test bug." |
| Defect reporting | `materials/bug-notes.txt` | "Turn these exploratory testing notes into a bug report with title, steps to reproduce, expected result, actual result and severity." |
| Reporting | `materials/ci-failure-sample.txt` | "Write a five-line quality summary of this test run for a non-technical product owner." |

Then, for **at least one** of your use cases, prove a reply right or wrong with deterministic code or a tool, and record it under "Deterministic check":
- **Test code:** save the reply as `test_shipping_ai.py` next to a copy of `shipping.py` and run `python -m pytest -q test_shipping_ai.py`. Then review the tests against the six numbered requirement sentences in the docstring, one at a time. Passing is not the same as proving the requirement.
- **Test data:** write a small checker (15 to 30 lines) that applies the registration rules to the CSV and reports every row where `expected_valid` is wrong. The Monday demo's `check_test_data.py` shows the pattern; your rules are different, so do not copy its regular expressions.
- **Debugging:** for every cause Claude gives, quote the exact log line that supports or contradicts it. Run a command (for example `python -m pytest --help`) for any flag or option it mentions.
- Other use cases: agree a check with your instructor before you start.

Checkpoint: six logged and reviewed replies (two per use case), a run-to-run comparison for each use case, and one deterministic check with its output pasted.

## Stage 6: Write the use-case cards and challenge them (about 25 min)
1. Fill in one card per use case in `use-case-card.md`. Every field. "Who verifies" must be a role; "how" must be a concrete check with a rough time.
2. For each "what could go wrong", name the mechanism behind it (`generative-ai-concepts.md` sections 3, 6 and 8). For example, an invented business rule is a hallucination: plausible next tokens with no fact-check in the generation loop.
3. Ask Claude to challenge your work. Fresh chat, paste your three completed cards:

```text
Here are three proposed uses of generative AI in a software testing team.

<paste your three use-case cards here>

For each one, list the weaknesses in the proposal: risks that are missing,
verification methods that would not work, or reasons another approach would be better.
```

4. Log the reply and review it. In the "Claude challenge" table, **accept or reject each critique** with a reason. Update your cards for every critique you accept. Rejecting a critique is fine when you can say why.

Checkpoint: three complete cards, a ranking decision, and a decided critique table.

## Stage 7: Present (about 15 min, in groups of 3 or 4)
1. Prepare `presentation-outline.md` (5 minutes of talk). Slides are optional.
2. Present to your group. Each listener asks one question, ideally about verification.
3. Record the feedback you received at the bottom of the outline.

## Stretch goals
- Add an `effort_to_adopt` criterion to `rank_use_cases.py` with a justified negative weight. Does your top 3 change?
- Run your Stage 5 probe a third time and count how many items appear in all three replies. What does that overlap tell you?
- For one rejected candidate (for example pain point 8), write the outline of the classic NLP pipeline you would use instead, naming the steps from `nlp-fundamentals.md` (preprocessing, TF-IDF, similarity or clustering).
- Use the Monday demo's card 2.8 approach: ask Claude about one specific pytest or Playwright option your use case would rely on, then verify it against the tool's `--help` or official documentation.

## Deliverables
Submit the folder `week8-monday-<yourname>/` containing:
1. `candidate-longlist.md` and `tool-choice-worksheet.md`, completed.
2. `rank_use_cases.py` with your candidates and the sensitivity notes, running with no `CHECK` lines.
3. `research-log.md`, completed, with the hype check.
4. `claude-evidence-log.md` with every prompt, full reply and review, the run-to-run comparison and the deterministic check.
5. Any file your check used or produced (for example `test_shipping_ai.py`, your checker script, the CSV).
6. `use-case-card.md` with three cards, the ranking decision and the decided critique table.
7. `presentation-outline.md` with the feedback you received.

## Definition of Done
- [ ] At least 9 candidates covering at least 5 STLC activities; every Claude-suggested candidate has a validation mark
- [ ] Every candidate has a tool choice and a one-sentence reason; at least one rejected as No AI and one as Classic ML/NLP
- [ ] `rank_use_cases.py` holds at least 6 GenAI candidates with a reason for every score, runs with no `CHECK` lines, and the sensitivity notes are filled in
- [ ] Three use cases selected; any override of the ranking is justified
- [ ] At least one verified external source per use case; every Claude-suggested source was opened and its status recorded
- [ ] Every Claude prompt and full reply is logged and reviewed with all five questions
- [ ] Each use case was probed twice in fresh chats and the two runs are compared
- [ ] At least one Claude reply was proved right or wrong by code or a tool, with the output pasted
- [ ] Three complete use-case cards, each with a named verifier role, a concrete check, at least two failure modes with their mechanism, and a data-sensitivity rule
- [ ] Every Claude critique is accepted or rejected with a reason
- [ ] Presentation given within 5 minutes; feedback recorded
- [ ] No real data, credentials or internal URLs in any prompt; no emojis in any deliverable

## Grading rubric (100 points)
| Criterion | Weight | Full marks when |
|---|---|---|
| Long list and STLC mapping | 10 | 9+ candidates, 5+ STLC activities, tied to the brief; Claude ideas validated against the brief, invented features caught |
| Tool choice reasoning | 15 | every row names its deciding property; rejections are correct (deterministic rule as No AI, labelled history as supervised ML, unlabelled volume as clustering or NLP) |
| Scoring, ranking and sensitivity | 15 | every score has a reason; script runs clean; sensitivity notes explain the effect of verifiability in the trainee's own words; overrides justified |
| Use-case cards | 20 | value, verifier role, concrete check, two or more failure modes traced to the right LLM mechanism, data-sensitivity rule, success measure |
| Claude evidence and human validation | 20 | all replies logged in full and reviewed with the five questions; two-run comparison drawn; one deterministic check that actually ran; corrections stated; critiques decided with reasons |
| Research quality | 10 | sources are credible, opened and accurately represented; any hallucinated source caught and logged; hype claim classified with reasoning |
| Presentation | 10 | within time; ranked; each use case answers "who checks it and how"; one AI mistake and one rejected candidate shown |

## Common pitfalls and hints
- "Who verifies: the team" is not an answer. Name a role (test lead, the story's tester, the product owner) and a check they can finish in minutes.
- If checking the output takes as long as doing the task by hand, verifiability is low. Score it honestly; the ranking will show you the consequence.
- A use case that only works when the reply is perfect is not ready. Look at your two runs: would the team still get value from the weaker one?
- Pain point 10 is a deterministic rule. Ask yourself what a parametrised pytest test would do that an LLM cannot.
- Pain points 8 and 9 differ in one important way. Re-read section 1 of `supervised-vs-unsupervised-learning.md` and ask "do we have labels?"
- When Claude's tests for `shipping.py` all pass, look for what is not there: the value just below a boundary, express on a free order, the error cases. When some fail, read the docstring before deciding whether the code or the test is wrong.
- When a probe reply is very good, the lesson still applies: how do you know it is right? Your check, not Claude's tone, decides.
- Copy Claude's reply in full before you review it. Reviewing from memory hides the exact sentence that was invented.
- Keep prompts plain today. If you catch yourself writing "You are an expert...", put that idea on your Tuesday list instead.
- Ask for help after 15 minutes stuck, with your evidence log open.

## Reference: where to look (no solutions)
| Need | Look at |
|---|---|
| STLC activities and GenAI applications | `generative-ai-applications-within-qe.md`, sections 2 and 3 |
| No AI vs classic ML/NLP vs GenAI | `generative-ai-applications-within-qe.md` section 5; `nlp-fundamentals.md` section 10; demo card 3.1 |
| Supervised vs unsupervised decision flow | `supervised-vs-unsupervised-learning.md`, sections 1 and 6 |
| Scoring criteria and the ranking helper | `generative-ai-applications-within-qe.md` section 6; `llm_mechanics_lab.py rank` |
| Why replies vary between runs | `generative-ai-concepts.md` sections 3.3 and 7; demo cards 1.2 and 2.5 |
| Hallucination, cut-off, context window and other limits | `generative-ai-concepts.md` sections 5, 6 and 8 |
| Confidence is not correctness | `neural-network-fundamentals.md` section 9 |
| The five review questions | demo asset `demo_ai_generative_ai_fundamentals.md`, section 2 |
| Checking AI tests and AI data with code | `generative-ai-applications-within-qe.md` section 7; demo cards 2.3 and 2.6 |
| Realistic vs unrealistic claims | `generative-ai-applications-within-qe.md` section 8 |

## Suggested working order and checkpoints
1. After Stage 2, you should be able to say in one sentence why each rejected candidate is better off without GenAI.
2. After Stage 3, your ranking should still make sense to you when you read it aloud. If it does not, a score is wrong; fix the score, not the weights.
3. After Stage 5, every use case has evidence: two reviewed replies and at least one fact you checked yourself.
4. Before Stage 7, time your talk once. Cut detail, not the verification story.
