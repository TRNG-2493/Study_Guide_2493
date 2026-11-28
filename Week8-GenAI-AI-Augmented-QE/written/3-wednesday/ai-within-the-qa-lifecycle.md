# AI within the QA Lifecycle

## Learning Objectives

By the end of this lesson you will be able to:

- **Describe** the phases of the Software Testing Life Cycle (STLC) and what each phase hands to the next.
- **Explain** three levels of AI involvement (assist, draft and automate) and why higher levels need stronger checks.
- **Trace** one AI mistake through every phase, and show how it turns into wrong tests, wrong data and a false bug report.
- **Place** a human check at every hand-over, and explain why the earliest check is the cheapest.
- **Choose** a sensible level of AI involvement for a task, based on risk and on how easily you can check the result.

---

## Why This Matters

On Monday and Tuesday you used AI for one task at a time: explain a concept, write a prompt, draft some tests. Real testing work is a chain of tasks. A requirement becomes test cases, test cases need data, data feeds automated tests, and the results become bug reports and a release decision. AI can help at every link of that chain, which is exactly why it needs care.

A mistake made in one task stays in that task. A mistake made **early in a chain** is copied into every later step, often by people (or AIs) who have no reason to doubt it. By the time it shows up as a failing test or a bug report, it has already cost several people time.

The testing profession has noticed. In 2025 the ISTQB, the body behind the Foundation Level certificate many testers hold, released a specialist syllabus called **Testing with Generative AI (CT-GenAI)**, and updated it to version 1.1 in April 2026. Its scope is applying large language models **across the entire testing lifecycle**, from requirements analysis and test design to automation and reporting ([ISTQB](https://istqb.org/certifications/gen-ai/)). That is the view this lesson takes: not "what can AI do?", but "where in the lifecycle does it help, what can go wrong there, and who checks?"

> **Using this with the handout:** this lesson goes deeper into **Handout 05, Topic 1**. It uses the same running example (US-205), the same invented rule ("codes are case-insensitive"), the same four-step table and the same lifecycle checklist.

---

## The Concept

### 1. A Quick Refresher: The STLC

The **Software Testing Life Cycle (STLC)** is the sequence of activities a team works through to test a product. Different books draw it slightly differently, but the shape is always similar:

| Phase | What happens | What it hands to the next phase |
|---|---|---|
| **Requirements analysis** | Read the stories; find gaps and questions | Clear, testable requirements; questions for the BA |
| **Test planning** | Decide scope, approach, risks, effort | A test plan |
| **Test design** | Turn requirements into test cases | Test cases, each linked to a requirement |
| **Test data and environment** | Prepare inputs, users and systems | Data sets and a ready environment |
| **Test execution** | Run the tests, manual and automated | Results: passes, failures, logs |
| **Defect reporting** | Investigate failures; write bug reports | Bug reports linked to requirements |
| **Test closure** | Summarise; decide if the release can ship | A test summary report |

The last column is the important one for this lesson. Every phase **consumes** the output of an earlier phase. Nobody in test design re-reads the original customer conversation; they work from the requirements as analysed. Nobody running tests re-derives each expected result; they trust the test cases. That trust is what makes teamwork efficient. It is also what makes early mistakes dangerous.

The handout compares this to a **relay race**: each phase passes the baton to the next. If the baton is dropped early and nobody notices, every later runner carries the mistake forward, very efficiently.

### 2. Three Levels of AI Involvement

AI can play different roles in a phase. The handout names three levels:

| Level | What the AI does | What the human does | Example |
|---|---|---|---|
| **Assist** | Suggests ideas | Writes the real output | "Here are 10 test ideas for AC1" |
| **Draft** | Writes a first version | Reviews and edits every item | A full set of test cases for US-205 |
| **Automate** | Runs on its own, repeatedly | Checks samples or results | A nightly job that summarises failures |

The rule that goes with the table: **the higher the level, the stronger your checks must be.**

- At **assist**, a bad idea costs little. You read it, see it is wrong and ignore it. Your own judgement is still writing the output.
- At **draft**, the AI's words become the output unless you change them. A wrong expected result survives if you skim.
- At **automate**, nobody reads each output at all. If the job summarises 200 failures every night, a systematic mistake repeats 200 times before anyone looks.

Notice that the level is a **choice**, not a property of the tool. The same chat assistant can assist (you ask for ideas), draft (you ask for finished test cases) or, wired into a script, automate. Choosing the level is part of using AI responsibly, and section 8 gives a way to choose.

### 3. Error Propagation

**Error propagation** means an early mistake being carried forward into later phases, where it causes new mistakes. Two features make it especially costly with AI:

- **Fluency.** AI output reads well. A confident, well-formatted sentence is less likely to be questioned than a scribbled note, even when it is wrong.
- **Speed.** AI can produce the next phase's output in seconds. A human might pause between phases and notice something odd; a fast pipeline does not pause.

The worked example shows this with a single sentence.

### 4. Worked Example: Trace One AI Mistake Through the Lifecycle

**The situation:** our running story is US-205.

```text
US-205 Apply coupon at checkout
As a shopper I want to apply a coupon code so that I pay less.
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
```

While reviewing it, an AI assistant confidently added: *"Coupon codes are case-insensitive, so save10 also works."* That is **not** in the story. You have met this invented rule all week; now we follow it through the lifecycle as if nobody checks. Build the table with the handout, one column at a time.

#### Step 1: List the phases

| Phase |
|---|
| 1. Requirements analysis |
| 2. Test design |
| 3. Test data |
| 4. Test automation |
| 5. Execution and defect reporting |

We use five phases here, combining a few from section 1, to keep the table readable.

#### Step 2: Add how AI helps in each phase

| Phase | How AI helps |
|---|---|
| 1. Requirements analysis | Reviews the story, finds gaps and questions |
| 2. Test design | Drafts test cases from the acceptance criteria |
| 3. Test data | Generates input values and users |
| 4. Test automation | Writes the pytest or Playwright code |
| 5. Execution and defect reporting | Summarises failures and drafts bug reports |

Every phase has a genuine use for AI. That is the point: the invented rule will have a "helper" waiting at every step.

#### Step 3: Follow the invented rule through every phase

| Phase | What the invented rule causes |
|---|---|
| 1. Requirements analysis | "Codes are case-insensitive" is written into the review notes as if it were fact |
| 2. Test design | A test case appears: "lowercase save10 gives 10% off" |
| 3. Test data | `save10`, `Save10` and `sAvE10` are listed as **valid** codes |
| 4. Test automation | `assert apply_coupon(100, "save10") == 90` is written |
| 5. Execution and defect reporting | The test fails, and a **false bug** is filed: "lowercase coupon rejected" |

Read the last row carefully. The code is **correct**: it does exactly what US-205 says, which is to recognise `SAVE10`. The test fails because the **test** is wrong. But the bug report says the **code** is wrong, and now a developer spends time investigating a "bug" that does not exist. Worse, they might "fix" it, changing the product to match a rule nobody asked for.

One invented sentence produced a wrong test case, three wrong data rows, a failing test, a false bug report and a wasted investigation.

#### Step 4: Add the human check at each hand-over

| Phase | Human check that stops it |
|---|---|
| 1. Requirements analysis | **Is every statement in the story? If not, ask the BA.** |
| 2. Test design | **Does every test case trace to an AC?** |
| 3. Test data | **Does every value follow a stated rule?** |
| 4. Test automation | **Does each assert match a reviewed test case?** |
| 5. Execution and defect reporting | **Does the bug report quote the requirement it breaks?** |

Each question is short, and each one would have stopped the invented rule at that phase. Try the last one on the false bug: *"Which requirement does 'lowercase coupon rejected' break?"* There is no such requirement, so the bug report cannot quote one. The question exposes the mistake even at the very end.

This table is your **lifecycle checklist**. Keep it in your notes; the rest of today's lessons turn the first three checks into code.

### 5. Why the Earliest Check Is the Cheapest

Count what has to be undone if the invented rule is caught at each phase. Work it out yourself from the Step 3 table before reading the answer.

| Caught at | Things already built on the mistake that must be fixed |
|---|---|
| 1. Requirements analysis | Nothing. One question to the BA |
| 2. Test design | 1 test case |
| 3. Test data | 1 test case + 3 data rows |
| 4. Test automation | 1 test case + 3 data rows + 1 automated test |
| 5. Defect reporting | All of the above + 1 bug report + a developer's investigation |

The list grows at every phase, and the later items are more expensive: an automated test takes longer to fix than a line in a review note, and a developer's investigation involves a second person. This is a small version of a widely taught idea in testing: **defects are cheaper to fix the earlier they are found.** Here, the cheapest fix of all is a single question at phase 1: *"Is this statement actually in the story?"*

There is a second, quieter cost. Each phase that accepts the mistake makes it look **more** trustworthy. By phase 4 it is not "something the AI said" but "what our test suite checks". People defend their test suite. The longer a mistake survives, the harder it is to remove.

### 6. A Second Trace: a Mistake That Starts Late

Not every AI mistake starts at phase 1. Here is one that starts at the end, so you can see that the checklist protects late phases too.

**The situation:** the nightly run has one failing test, `test_save10_on_exactly_50`. You ask an AI to draft the bug report. Its draft, **illustrative**:

```text
Title: SAVE10 coupon is broken for all customers
Severity: Critical
Description: The SAVE10 coupon does not work. Customers cannot get their discount.
```

Apply the phase 5 check: **does the bug report quote the requirement it breaks?** It does not. Now read the evidence: one test fails, at exactly $50.00. The test at $100.00 passes. So the coupon works for most orders; it fails **at the boundary**. The accurate report is much narrower:

```text
Title: SAVE10 not applied at exactly $50.00
Severity: Major (discount missing at boundary; other amounts work)
Requirement: US-205 AC1 "SAVE10 gives 10% off a subtotal of $50.00 or more."
Steps: Cart subtotal $50.00, enter SAVE10, click Apply.
Expected: Total $45.00. Actual: Total $50.00.
```

The AI's draft is a different failure from the invented rule: an **over-generalisation**, turning one failing case into "broken for all customers". The damage is different too. A "Critical, broken for everyone" report can stop a release or wake people up at night for a bug that affects only orders of exactly $50.00. The same five-question checklist catches it, because quoting the requirement forces you to look at what actually failed.

### 7. Automating the First Check (a Small Demo)

The phase 1 question, "is every statement in the story?", can be partly automated. This small script, `in_story.py`, checks whether each statement from an AI review appears **word for word** in the story. It uses standard Python only:

```python
STORY = """US-205 Apply coupon at checkout
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order."""

ai_claims = [                       # statements from an AI review of US-205
    "10% off a subtotal of $50.00 or more",
    "Coupon code not recognised",
    "codes are case-insensitive",
    "one coupon per order",
    "orders over $50 get 10% off",
]

for claim in ai_claims:
    found = claim.lower() in STORY.lower()
    print(f"{'IN STORY ' if found else 'NOT FOUND'} | {claim}")
```

Running `python in_story.py` prints:

```text
IN STORY  | 10% off a subtotal of $50.00 or more
IN STORY  | Coupon code not recognised
NOT FOUND | codes are case-insensitive
IN STORY  | one coupon per order
NOT FOUND | orders over $50 get 10% off
```

The invented rule is flagged. But look at the last line. "Orders over $50 get 10% off" is also flagged, and it is a **different kind** of finding: a **paraphrase**, not an invention. A word-for-word check cannot tell the difference between "the AI made this up" and "the AI said it in its own words".

A human reading that line notices something more. "Over $50" is not the same as "$50.00 or more": the paraphrase has quietly moved the boundary, which is exactly the `>` vs `>=` bug from Monday and Tuesday. So the script found a genuine problem, but for the wrong reason, and only a person can see the real one.

This is a pattern you will see in every lesson today: **code points, humans decide.** A script is fast, predictable and never tired, so it is good at pointing at suspicious lines. Deciding what those lines mean is still your job.

### 8. Choosing a Level of AI Involvement

How do you decide whether AI should assist, draft or automate a task? Three questions help:

1. **How bad is a mistake?** A wrong idea in a brainstorm costs nothing; a wrong "ship it" decision can cost customers money.
2. **Can I check the result quickly and reliably?** You can check ten test ideas in a minute. Checking whether a release is safe is the whole job of testing.
3. **Can the mistake be undone?** A draft bug report can be edited before anyone sees it. A message sent to a customer cannot be unsent.

Apply them to some typical tasks, as a fresher:

| Task | Sensible level | Why |
|---|---|---|
| Brainstorming edge cases for US-205 | **Assist** or **draft** | Low cost of a bad idea; easy to check; nothing to undo |
| Writing a bug report | **Draft** | Useful wording help, but you must check every claim against the evidence (section 6) |
| Generating 50 test data rows | **Draft**, with a script to check them | Easy to check with code (Topic 4 today) |
| Summarising last night's failures | **Automate**, once you trust it, with spot checks | Repeats daily; read samples and the full report when something looks odd |
| Deciding whether a release can ship | **Assist** at most | High cost; hard to check; a person must own the decision |

That last row matters. AI can help you **gather** information for a release decision, for example "list the open Critical bugs and their status", but the decision itself stays with an accountable person. You will see accountability again in *Human Validation of AI Output* and *Responsible Use of AI in QE* today.

### 9. Make Every Hand-Over Traceable

The checklist questions in Step 4 all ask the same thing in different words: **where did this come from?** You can make that question easy to answer by giving every artefact a **source** as it is created. Here is US-205's AC2 carried through the lifecycle, with the source written into each item:

| Artefact | Example | Its source |
|---|---|---|
| Requirement | AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10". | The story |
| Test case | TC-03: SAVE10 on $49.99; expected total $49.99 and the AC2 message | `ac: AC2` |
| Test data row | `{"subtotal": 49.99, "purpose": "just under the AC2 boundary"}` | The purpose names AC2 |
| Automated test | `test_save10_under_50_unchanged`, with a comment `# TC-03, AC2` | The test case ID |
| Bug report | "AC2 message missing" quoting the AC2 text | The requirement, quoted |

When every item points back to its source, the review questions become quick look-ups instead of detective work. An item that **cannot** name a source, like the lowercase test case or the "broken for all customers" report, stands out immediately.

This is **traceability**, a term you will meet again in *AI-Generated Test Cases*, where a short script checks that every AC has at least one test case. It is also why the prompts you saved this week ask the AI to include an AC column: you are asking it to keep the trail, so you can check it.

### 10. AI in Test Planning: a Short Example

Test planning gets less attention than test design, but AI is often asked to help with it. Suppose you ask an AI to *"list the main risks for testing the checkout coupon feature"*. A typical reply, **illustrative**:

```text
1. Performance issues under load
2. Security vulnerabilities
3. Browser compatibility problems
4. Incorrect discount calculation at the $50.00 boundary
5. Coupon accepted twice on the same order
```

Apply the planning check from the table in the next section: **does each risk name a real feature or story?** Risks 1 to 3 could be pasted into any project's plan; they are true of almost every web feature, so they tell the team nothing new.

Risks 4 and 5 are specific: they name US-205's boundary (AC1) and its one-coupon rule (AC4), and each suggests a test. A good plan keeps the specific risks and either sharpens the generic ones ("checkout must respond within the time agreed for US-310") or drops them.

This is a mild version of the same failure you met in *Specificity and Context* on Tuesday: a vague prompt gets a generic answer. Giving the AI the story itself, rather than "the coupon feature", makes specific risks much more likely.

### 11. Phase-by-Phase: Where AI Helps and What to Watch

Here is the full lifecycle with AI's typical strengths and risks in each phase. Use it as a reference rather than reading it in one go:

| Phase | AI is good at | Typical AI risk | Human check |
|---|---|---|---|
| Requirements analysis | Spotting vague words, listing questions | Inventing answers to its own questions | Is every statement in the story? |
| Test planning | Drafting a plan outline, listing risks | Generic plans that ignore your project | Does each risk name a real feature or story? |
| Test design | Drafting many cases quickly | Wrong boundaries, paraphrased messages, invented rules | Does every case trace to an AC? |
| Test data | Realistic-looking values | Hidden rule breaks (formats, ranges, codes) | Does every value follow a stated rule? |
| Test automation | Writing test code and locators | Tests that pass but prove nothing | Does each assert match a reviewed case, and can it fail? |
| Test execution | Summarising long logs | Missing the one important line | Does the summary match the raw results? |
| Defect reporting | Clear, well-structured reports | Over-generalising; inventing causes | Does the report quote the requirement and the evidence? |
| Test closure | Drafting the summary report | Smoothing over open risks | Are open bugs and gaps stated plainly? |

Today's lessons zoom in on the early phases: requirements (*AI-Assisted Requirements Analysis*), test design (*AI-Generated Test Cases*) and test data (*AI-Generated Test Data*). This afternoon covers automation and human validation, and the rules for using AI responsibly.

### 12. Common Mistakes

| Mistake | What goes wrong | Better habit |
|---|---|---|
| Checking only the final output | The mistake has already spread | Check at every hand-over |
| Treating each phase's input as true | Early mistakes look like facts by phase 4 | Ask "where did this come from?" |
| Fixing the code to match a failing test | A false bug becomes a real one | Quote the requirement first |
| Using "automate" for tasks you cannot check | Systematic mistakes repeat unseen | Start at "draft" until you trust the output |
| Letting AI make the ship decision | No one is accountable | AI gathers; a person decides |

---

## Practice Exercises

1. **Trace a different mistake (paper, 10 min).** During test design, the AI wrote the AC2 message as `"Spend $50 to use SAVE10"`, missing the `.00`. Using the Step 3 table as a model, write what this mistake causes in each later phase. Which human check from Step 4 stops it first?

2. **Choose the level (paper, 10 min).** For each task, choose assist, draft or automate, and give one reason using the three questions from section 8:
   - (a) writing a bug report;
   - (b) deciding whether a release can ship;
   - (c) brainstorming edge cases;
   - (d) checking 300 rows of test data against the rules.

3. **Compare the AI's lifecycle (AI tool, 15 min).** Follow this week's four steps:
   - **Prompt:** ask *"List the phases of the Software Testing Life Cycle and one way AI can help in each."*
   - **Review:** compare its list with the table in section 1. Did it add, skip or merge any phases?
   - **Run:** pick its suggestion for one phase and try it on US-205.
   - **Record:** note in `prompts.txt` one thing its list did well and one thing you would add.

4. **Extend the in-story check (code, 15 min).** Add two claims of your own to `ai_claims` in `in_story.py`: one that is a word-for-word quote from US-205, and one paraphrase that changes the meaning. Run it. Then write one sentence explaining why the script cannot tell a harmless paraphrase from a harmful one.

---

## Knowledge Check

1. What does each STLC phase hand to the next, and why does that matter for AI mistakes?

<details><summary>Answer</summary>

Each phase hands its output (requirements, test cases, data, results, bug reports) to the next phase, which treats it as correct. An AI mistake early on is therefore copied into every later phase.

</details>

2. Name the three levels of AI involvement and the rule that goes with them.

<details><summary>Answer</summary>

Assist, draft and automate. The higher the level, the stronger your checks must be.

</details>

3. The invented rule "codes are case-insensitive" ends up as a false bug report. Why is the bug false?

<details><summary>Answer</summary>

The code correctly follows US-205, which only mentions SAVE10. The test is wrong because it was built on an invented rule, so the failure says nothing about the code.

</details>

4. Where is the cheapest place to catch an invented rule, and what single question catches it?

<details><summary>Answer</summary>

In requirements analysis, by asking "Is this statement actually in the story?" Nothing has been built on the mistake yet.

</details>

5. An AI drafts a bug report saying "SAVE10 is broken for all customers", but only the $50.00 test fails. What kind of mistake is this, and which check catches it?

<details><summary>Answer</summary>

An over-generalisation. The check "Does the bug report quote the requirement it breaks?" forces you to look at the evidence, which shows the failure is only at the boundary.

</details>

6. `in_story.py` flagged "orders over $50 get 10% off" as NOT FOUND. What did a human notice that the script could not?

<details><summary>Answer</summary>

The paraphrase changed the meaning: "over $50" excludes exactly $50.00, while the story says "$50.00 or more". The script only knew the words did not match.

</details>

7. An AI lists "security vulnerabilities" as a risk in the test plan for US-205. Why is that weak, and how would you improve it?

<details><summary>Answer</summary>

It is generic: it could apply to any project and names no feature or story. Keep risks that name something specific, such as the $50.00 boundary (AC1) or a second coupon (AC4), and give the AI the story itself so its risks are specific.

</details>

---

## Glossary

- **STLC (Software Testing Life Cycle):** the sequence of testing activities, from requirements analysis to test closure.
- **Hand-over:** the point where one phase's output becomes the next phase's input.
- **Assist / draft / automate:** three levels of AI involvement, from suggesting ideas to running on its own.
- **Error propagation:** an early mistake carried forward into later phases.
- **Invented rule:** a rule that appears in AI output but is not stated in the requirement.
- **False bug:** a bug report about behaviour that is actually correct.
- **Over-generalisation:** turning a narrow result, such as one failing case, into a broad claim.
- **Lifecycle checklist:** one human-check question for each hand-over.
- **Traceability:** the link from each test case or bug back to the requirement it concerns.
- **Paraphrase:** saying the same thing in different words, which can quietly change the meaning.
- **Accountable:** being the named person responsible for a result or decision.
- **Generic risk:** a risk so broad it could apply to any project, such as "security vulnerabilities", and so gives the team nothing specific to test.
- **Test summary report:** the closure document stating what was tested, what failed and what risks remain open.

---

## Summary

- **AI can help in every STLC phase**, from requirements analysis to test closure.
- **Each phase trusts the one before it**, so an early AI mistake spreads: one invented sentence became a wrong test case, wrong data, a failing test and a false bug.
- **Put a human check at every hand-over.** The cheapest check is the first: *"Is this statement actually in the story?"*
- **Choose the AI level deliberately:** assist, draft or automate, based on the cost of a mistake, how easily you can check it, and whether it can be undone.
- **Code points, humans decide.** Simple scripts can flag suspicious statements, but only a person can judge what they mean.

---

## Additional Resources

- ISTQB, *Certified Tester – Testing with Generative AI (CT-GenAI)*: https://istqb.org/certifications/gen-ai/
- ISTQB, *Certified Tester Foundation Level Syllabus v4.0.1* (the test process, chapter 1): https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
- NIST, *AI Risk Management Framework*: https://www.nist.gov/itl/ai-risk-management-framework
