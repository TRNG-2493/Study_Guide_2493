# Human Validation of AI Output

## Learning Objectives

By the end of this lesson you will be able to:

- **Define** human validation and human-in-the-loop, and explain who is accountable for AI-assisted work.
- **Recognise** three traps that make people trust AI too much: fluency, volume and automation bias.
- **Review** AI-generated test cases with a four-question checklist and decide to accept, edit or reject each one.
- **Record** every decision with a reason category in a correction log, and use the log to improve your prompts.
- **Match** the depth of a review to the risk of the area being tested.

---

## Why This Matters

All week, the same message has come up in different forms: AI drafts, people check. This lesson turns "people check" into a **method**, with a checklist, three allowed decisions and a written record.

Why does checking need a method? Because people are not naturally good at checking AI. Microsoft researchers reviewed around 60 studies on what they call **overreliance on AI**: users accepting incorrect AI outputs.

Their 2022 report notes that policymakers and practitioners increasingly make users "the last line of defense against AI failures", and explains how overreliance makes it hard for people to oversee AI's weaknesses ([Microsoft Research](https://www.microsoft.com/en-us/research/publication/overreliance-on-ai-literature-review/)). In other words: telling someone to "check the AI" is not enough. They need a way to do it that works even when they are busy or tired.

There is also the question of **who is responsible**. In February 2024, a Canadian tribunal decided *Moffatt v. Air Canada*. The airline's website chatbot had given a customer wrong information about bereavement fares. Air Canada argued, in effect, that the chatbot was responsible for its own words; the tribunal called this "a remarkable submission" and found the airline liable ([Civil Resolution Tribunal decision](https://decisions.civilresolutionbc.ca/crt/crtd/en/525448/1/document.do)). The lesson for testers is direct: when AI output goes into your work, **you** are accountable for it, not the tool.

> **Using this with the handout:** this lesson goes deeper into **Handout 06, Topic 2**. It uses the same four-question checklist, the same AI draft (TC-01 to TC-04), the same correction log and answer key, the same second-review prompt and the same review-depth table.

---

## The Concept

### 1. What Is Human Validation?

**Human validation** is the structured review a person does **before** AI output is trusted and used. It has four parts:

1. Check each item against the requirement, using a **checklist**.
2. Decide: **accept**, **edit** or **reject**.
3. **Record** the decision and the reason in a **correction log**.
4. Use the log to improve how the team uses AI.

This approach is called **human-in-the-loop**: the AI drafts, and a **named** person reviews, approves and stays **accountable** for the result. "Named" matters. "The team reviewed it" can quietly mean nobody did. "Reviewed by J. Singh, 27 November" means one person looked and is willing to say so.

The log is not paperwork for its own sake. Over time it shows **what kinds of mistakes** the AI makes, which tells the team which prompts to improve and where to look harder.

### 2. Three Traps That Make People Trust AI Too Much

The handout names three traps. Each one has a QE version you will meet in real projects:

| Trap | What happens | QE example |
|---|---|---|
| **Fluency trap** | Well-written text *feels* correct | A neatly formatted test case with a wrong expected value is accepted because it "reads right" |
| **Volume trap** | Many items look thorough, so nobody checks each one | 50 AI test cases are approved in bulk; one invents a rule |
| **Automation bias** | "The tool said so" replaces thinking | A tester ignores their own doubt about a boundary because the AI was confident |

You have seen all three this week. The fluency trap is why the AI's `test_login_works` in *AI-Assisted Automation Development* looked fine: its name and layout were good; only the assert was weak. The volume trap is why *AI-Generated Test Cases* used code to check structure before reading. Automation bias is the reason every lesson has said "check the story, not the AI".

The traps are not signs of a bad tester. They are normal human reactions, which is exactly why a method that does not depend on willpower helps.

### 3. The Review Checklist

For AI-generated test cases, the handout's checklist has four questions. Each one catches a different kind of mistake:

| # | Question | Catches | Example from this week |
|---|---|---|---|
| 1 | Does it **trace** to an acceptance criterion? | Cases about nothing in the story | A case for "AC5" in a four-AC story |
| 2 | Does the **expected result** match the requirement **exactly**? | Wrong values, paraphrased messages | "Spend $50 to use SAVE10" |
| 3 | Is every rule in it **actually stated** in the story? | Invented rules | "Lowercase save10 gives 10% off" |
| 4 | Could this test ever **fail**? | Tests that prove nothing | `assert result` |

Questions 1 and 2 can be partly checked by code, as you did with `review_cases.py`. Questions 3 and 4 need a person: only a reader can see that a rule is invented, and only a "break it" check proves a test can fail.

### 4. Three Decisions, and Why Reasons Matter

Every reviewed item gets one of **three** decisions:

| Decision | Meaning | Needs a reason category? |
|---|---|---|
| **Accept** | Use as-is | No |
| **Edit** | Fix it, then use it | **Yes** |
| **Reject** | Remove it | **Yes** |

Only three decisions are allowed, on purpose. Options like "probably fine" or "check later" let items slip through without a real decision.

Every edit or rejection must have a **reason category**: a short, standard label for what was wrong. Using the same labels every time is what makes the log useful, because you can count them. A starting set of categories, built from this week's examples:

| Category | Example |
|---|---|
| Wrong expected result | $49.99 expected to give $44.99 |
| Wrong or paraphrased message | "Spend $50 to use SAVE10" |
| Invented rule | Lowercase codes accepted |
| Missing coverage | No case for AC4 |
| Weak check | `assert result` |
| Vague step | "Verify the discount" |
| Duplicate | Two cases checking $100.00 |

Your team can add categories, but keep the list short. If every review invents new labels, nothing can be counted.

### 5. Worked Example: Review an AI Draft and Keep a Correction Log

**The situation:** an AI drafted four test cases for US-205. You review each one with the checklist, decide, and record the decision. No code is needed for this part; a table on paper, in a spreadsheet or in a text file is enough. The **habit** is what matters.

```text
US-205 Apply coupon at checkout
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
```

#### Step 1: The checklist and the draft

| ID | AI's test case |
|---|---|
| TC-01 | SAVE10 on $100.00 gives $90.00 |
| TC-02 | SAVE10 on $49.99 gives $44.99 |
| TC-03 | Lowercase save10 gives 10% off |
| TC-04 | Unknown code shows "Coupon code not recognised" |

Before reading on, apply the four questions to each case yourself.

#### Step 2: Set up the log

The rules of a good log:

- Only **three** decisions are allowed: accept, edit or reject.
- Every edit or rejection **must** have a reason category.
- The **note** says **why**, quoting the requirement where possible.

| ID | Decision | Category | Note (why?) |
|---|---|---|---|
| | | | |

#### Step 3: Record your decisions

Work through the cases one by one. Two hints from the handout: for TC-02, check AC2's rule for subtotals **under** $50.00. For TC-03, ask: where in US-205 does it say lowercase works?

**Answer key:**

| ID | Decision | Category | Note (why?) |
|---|---|---|---|
| TC-01 | **Accept** | – | Matches AC1: 10% off $100.00 is $90.00 |
| TC-02 | **Edit** | Wrong expected result | AC2: under $50.00 is **unchanged**, so $49.99, plus the message "Spend $50.00 to use SAVE10" |
| TC-03 | **Reject** | Invented rule | Case-insensitivity is not in US-205. Ask the BA |
| TC-04 | **Accept** | – | Matches AC3 exactly |

Look at TC-02 closely, because it is a good example of the fluency trap. "$49.99 gives $44.99" **looks** like a reasonable discount: it is roughly 10% off. But AC2 says amounts under $50.00 get **no** discount. The AI applied AC1's rule to AC2's range. Only checking the expected result against the requirement word for word catches this.

Also notice what the log says about what is **missing**. Nothing covers **AC4**, and nothing tests the **$50.00 boundary**. A good reviewer adds a note below the log: *"Missing: AC4 test (ask the BA for the message); boundary test at exactly $50.00."* A review is not only about the items in front of you.

#### Step 4: Learn from the log

When the log is complete, count:

- **Accepted as-is:** 2 of 4 = **50%**. This **accepted-as-is rate** is a simple measure of how good the AI's draft was.
- **Categories:** 1 × wrong expected result, 1 × invented rule.

Each category tells you what to add to your prompt next time:

| Category found | Line to add to the test-case prompt |
|---|---|
| Invented rule | "Use only rules stated in the story. List anything unclear as a question." |
| Wrong expected result | "For each case, quote the AC that gives the expected result." |
| Missing coverage | "Every AC has at least one test case." |

Those lines should look familiar: they are in the stronger prompt in *AI-Generated Test Cases*. That prompt was written from exactly this kind of log.

#### Step 5: Ask the AI to review itself, then compare

Paste the four test cases and US-205 into a **new chat**:

```text
Review these 4 test cases against the user story. For each, answer: accept, edit or reject,
with a one-line reason. Use only the story as the source of truth.

### User story
US-205 Apply coupon at checkout
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.

### Test cases
TC-01: SAVE10 on $100.00 gives $90.00
TC-02: SAVE10 on $49.99 gives $44.99
TC-03: Lowercase save10 gives 10% off
TC-04: Unknown code shows "Coupon code not recognised"
```

Mark the AI's review against your log:

- ✅ TC-02 flagged for editing.
- ✅ TC-03 rejected as not in the story.
- ✅ TC-01 and TC-04 accepted.
- ⭐ Bonus if it mentions the missing AC4 or boundary tests.

Where you disagree with the AI, ask: **who is right according to the story?** Not "who sounds more sure". The story decides.

An AI can be a useful **second reviewer**: it is fast, never bored, and may notice something you missed. But it is not the **accountable** one. If both of you missed something, the log still has **your** name on it. That is the Air Canada lesson again, at a smaller scale.

### 6. Summarising the Log with Code

For four cases, counting by hand is easy. For forty, a short script helps, and it also enforces the rule that edits and rejections need a category. Save this as `log_summary.py`:

```python
log = [                                   # one row per reviewed AI test case
    {"id": "TC-01", "decision": "accept", "category": ""},
    {"id": "TC-02", "decision": "edit",   "category": "wrong expected result"},
    {"id": "TC-03", "decision": "reject", "category": "invented rule"},
    {"id": "TC-04", "decision": "accept", "category": ""},
]

accepted = sum(1 for row in log if row["decision"] == "accept")
print(f"Accepted as-is: {accepted} of {len(log)} = {accepted / len(log):.0%}")

for row in log:
    if row["decision"] != "accept" and not row["category"]:
        print(f"{row['id']}: {row['decision']} has no category")

categories = {}
for row in log:
    if row["category"]:
        categories[row["category"]] = categories.get(row["category"], 0) + 1
print("Categories:", categories)
```

Running `python log_summary.py` prints:

```text
Accepted as-is: 2 of 4 = 50%
Categories: {'wrong expected result': 1, 'invented rule': 1}
```

**What this code does:**

- `sum(1 for row in log if ...)` counts the rows that match a condition.
- `:.0%` formats a fraction as a percentage with no decimal places, so 0.5 prints as `50%`.
- The middle loop is a **rule check**: it prints a warning for any edit or rejection with an empty category. Here there are none, so it prints nothing.
- `categories.get(name, 0) + 1` is a common way to count: start at 0 the first time a name appears, then add 1 each time.

As with every script this week, the code **counts and points**; the decisions in the log are still yours.

### 7. The Checklist for Other Kinds of AI Output

The four questions were written for test cases, but the same ideas fit every kind of AI output you have reviewed this week. Only the wording changes:

| AI output | Traces to...? | Exact against the source? | Anything invented? | Could it fail / be wrong? |
|---|---|---|---|---|
| **Requirements review** | Each finding names a requirement ID | Quotes match the story | Questions, not invented answers | Is a "testable" verdict really testable? |
| **Test data** | Each row has a purpose and an AC | Values follow the stated rules | No codes or ranges the rules do not allow | Does each negative row break the rule it claims? |
| **Automation code** | Each test names a reviewed test case | Asserts use the exact expected value | No extra tests or rules | Does the break-it check turn it red? |
| **Bug report** | Quotes the requirement it breaks | Expected and actual match the evidence | No guessed cause stated as fact | Is the severity justified by the evidence? |

The pattern underneath is always the same: **where did it come from, is it exact, is anything made up, and does it really prove what it claims?** If you remember those four ideas, you can build a checklist for any AI output in a minute.

Here is the same log format applied to automation code: the AI's two login tests from *AI-Assisted Automation Development*.

| ID | Decision | Category | Note (why?) |
|---|---|---|---|
| `test_login_works` | **Edit** | Weak check | `assert result` passes for the error message too. Compare with "Welcome back!" using `==` |
| `test_wrong_password_is_handled` | **Edit** | Weak check | `is not None` passes for any value. Compare with "Invalid email or password" |

*Missing: tests for an unknown email and an empty password.*

Accepted as-is: **0 of 2 = 0%**, with one category twice. That single category points straight at the prompt line that fixes it: *"every assert compares the EXACT expected message with =="*, which is in the handout's automation template. The log format did not change at all; only the checklist wording did.

### 8. Habits That Make Reviews Work

A checklist tells you **what** to check. A few habits help you check it **well**:

- **Work out the answer before you read the AI's.** For a boundary case, calculate the expected value yourself first, then compare. If you read the AI's value first, it anchors your thinking, and "$44.99" starts to look plausible. This is a simple defence against the fluency trap.
- **Read the requirement, not your memory of it.** Have the story open beside the draft. Most review mistakes come from remembering "over $50" when the story says "$50.00 or more".
- **Review in two passes.** First pass: titles and traceability only, quickly, to find invented rules and missing coverage. Second pass: expected results and steps, slowly.
- **Take a break on large reviews.** Accuracy drops as attention fades, which is the volume trap from the inside. Twenty careful reviews beat fifty tired ones.
- **Say "I don't know" in the log.** If you cannot tell whether a case is right, the honest decision is "edit" with the note "ask the BA", not "accept" because it is probably fine.

None of these habits needs a tool. They are the human part of human validation.

### 9. When AI Stops Saving Time

The correction log can also answer a practical question: **is AI actually helping with this task?** Here is a rough calculation, **illustrative**, for 20 AI-drafted test cases:

| Activity | Time |
|---|---|
| Reviewing each case (20 × 2 minutes) | 40 minutes |
| Fixing the edited cases (8 × 4 minutes) | 32 minutes |
| Writing replacements for rejected cases (6 × 5 minutes) | 30 minutes |
| **Total** | **102 minutes** |

That draft had an accepted-as-is rate of 30% (6 of 20 accepted). If writing 20 good cases by hand takes about 100 minutes, the AI saved nothing, and the team carried the extra risk of a mistake slipping through.

The answer is usually not to give up on AI, but to **use the log**: the categories show what the prompt is missing, and a better prompt raises the accepted-as-is rate. If the rate stays low even after several prompt improvements, that is useful evidence too. Some tasks are better done by hand, or with AI at the **assist** level from *AI within the QA Lifecycle* rather than the **draft** level.

### 10. How Much Review Is Enough?

You cannot always review 200 AI-generated test cases one by one with the same care. The handout's answer is to match the **depth** of the review to the **risk**:

| Risk of the area | Examples | Review depth |
|---|---|---|
| **High** | Payments, discounts, login and security, personal data | Review **every** item against the full checklist |
| **Medium** | Search, filters, error messages | Review every item quickly; apply the full checklist to a sample |
| **Low** | Cosmetic text, help pages | Review a **sample** (for example 1 in 5). If the sample has problems, review them all |

Two rules always apply, whatever the risk:

1. **Anything involving money or security is high risk.** US-205 is about discounts, so every case gets a full review. The login tests in *AI-Assisted Automation Development* are about security, so the same applies.
2. **If a sample finds problems, widen the review.** Finding one invented rule means there are probably more. Mistakes in AI output tend to come from the same cause, such as a missing line in the prompt, so they come in groups.

Here is the second rule in action, **illustrative**. A tester samples 1 in 5 of 40 AI-generated test cases for a help page, so 8 cases. One has an invented rule. Under the rule, they now review all 40, and find two more with the same problem. Without the rule, the sample would have suggested "1 bad case, fixed", and two would have stayed in the suite.

### 11. Making the Log Useful Over Time

A single log tells you about one draft. A log kept over weeks tells you about **your AI and your prompts**. Two extra columns make that possible:

| Column | Why it matters |
|---|---|
| **Reviewer** | Accountability: someone can ask the reviewer about a decision |
| **Date** | Trends: is the accepted-as-is rate improving since the prompt changed? |

Suppose, **illustrative**, your team's accepted-as-is rate for test cases was 50% in week 1, and the most common category was "invented rule". You add *"Use only rules stated in the story"* to the prompt. In week 2 the rate is 70%, and "invented rule" has dropped to almost zero, but "missing coverage" has become the most common category. That tells you exactly what to work on next.

This is the correction log doing its real job: turning individual reviews into **evidence** for improving the process. You will look at keeping formal records of AI use, such as audit trails, in more depth in Week 11.

### 12. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| A decision of "edit" with no category | Easy to skip when you are in a hurry | Every edit or rejection needs a category. That is what makes the log useful |
| You and the AI disagree | One of you missed something | The **story** decides. Re-read the exact AC |
| The log says "accept" for everything | Review fatigue (the **volume trap**) | Slow down on money and security cases. Use the review-depth table |
| Categories differ every week | Reviewers invent new labels | Agree a short category list as a team |
| You accept a case you are unsure about | It is probably fine, and asking feels slow | Log it as "edit" with "ask the BA"; never accept on a guess |
| Missing cases are never logged | The log only lists the AI's items | Add a "Missing" note below every log |

---

## Practice Exercises

1. **Add a fifth case (paper, 5 min).** Add **TC-05: SAVE10 on exactly $50.00 gives $45.00** to your log. Apply the checklist and record your decision. What is the accepted-as-is rate now? Does it change the "Missing" note?

2. **Review your own AI's cases (AI tool, 20 min).** Follow this week's four steps:
   - **Prompt:** use your AI's test cases from *AI-Generated Test Cases* (exercise 4), or ask for new ones.
   - **Review:** apply the checklist to 5 of them and log each decision with a category.
   - **Run:** put your log into `log_summary.py` and run it.
   - **Record:** in `prompts.txt`, note the accepted-as-is rate and the most common category.

3. **Improve the prompt (paper, 10 min).** Look at your categories from exercise 2. Write **one new line** for your test-case prompt that would prevent the most common problem. Explain in one sentence why it targets that category.

4. **Spreadsheet log (spreadsheet, 15 min).** Turn your log into a spreadsheet with the four columns, plus **Reviewer** and **Date**. Write two sentences on why those two columns matter, using the ideas in section 11.

5. **Log a different output (paper, 10 min).** Take the AI's "negative" test users from *AI-Generated Test Data* (section 6). Build a correction log for the four rows, using the test-data wording of the checklist from section 7. Which row gets edited, and what category would you give it? Is "wrong boundary" a category your team should add?

---

## Knowledge Check

1. What does "human-in-the-loop" mean?

<details><summary>Answer</summary>

The AI drafts, and a named person reviews, approves and stays accountable for the result before it is used.

</details>

2. Name the three traps that make people trust AI too much.

<details><summary>Answer</summary>

The fluency trap (well-written text feels correct), the volume trap (many items look thorough) and automation bias ("the tool said so").

</details>

3. What are the four questions on the review checklist?

<details><summary>Answer</summary>

Does it trace to an AC? Does the expected result match the requirement exactly? Is every rule actually stated in the story? Could this test ever fail?

</details>

4. Why must every edit or rejection have a reason category?

<details><summary>Answer</summary>

So the log can be counted. The categories show what kinds of mistakes the AI makes and which prompt lines to add.

</details>

5. TC-02 says "SAVE10 on $49.99 gives $44.99". Why is it edited, not accepted?

<details><summary>Answer</summary>

AC2 says subtotals under $50.00 are unchanged, so the expected result is $49.99 with the message "Spend $50.00 to use SAVE10". The AI applied AC1's discount to AC2's range.

</details>

6. You and an AI second reviewer disagree about a case. How do you decide?

<details><summary>Answer</summary>

The story decides. Re-read the exact acceptance criterion. And whatever the AI says, you are the accountable reviewer.

</details>

7. A 1-in-5 sample of low-risk AI test cases finds one invented rule. What should you do?

<details><summary>Answer</summary>

Widen the review to all the items. Mistakes in AI output often share a cause, so one problem suggests there are more.

</details>

8. Why should you calculate a boundary case's expected value before reading the AI's value?

<details><summary>Answer</summary>

Reading the AI's value first anchors your thinking and makes a wrong value look plausible (the fluency trap). Working it out first gives you an independent answer to compare.

</details>

---

## Glossary

- **Human validation:** a structured review by a person before AI output is trusted and used.
- **Human-in-the-loop:** a way of working in which AI drafts and a named person approves and stays accountable.
- **Accountability:** being responsible for a result, even when AI helped produce it.
- **Overreliance:** accepting AI outputs that are incorrect.
- **Fluency trap:** trusting text because it is well written.
- **Volume trap:** trusting a large amount of output because it looks thorough.
- **Automation bias:** trusting a tool's output more than you should.
- **Correction log:** a record of each review decision, its reason category and a note.
- **Reason category:** a short standard label for why an item was edited or rejected.
- **Accepted-as-is rate:** the share of AI output used without changes.
- **Second reviewer:** an extra reviewer, human or AI, who checks the same items; not the accountable one if it is an AI.
- **Anchoring:** being pulled towards the first value you see, such as an AI's answer, when making your own judgement.
- **Two-pass review:** a quick first pass for traceability and invented rules, then a slow second pass for expected results and steps.
- **Review depth:** how thoroughly items are checked, matched to the risk of the area.

---

## Summary

- **Human validation** is checklist → accept, edit or reject → **record why**. A named person stays **accountable**.
- Watch for the **fluency trap, the volume trap and automation bias**. A method protects you when attention fails.
- The **four checklist questions**: trace to an AC, exact expected result, nothing invented, could it fail?
- The **correction log** turns reviews into evidence: in the worked example, 50% accepted as-is, with one wrong expected result and one invented rule, each pointing to a prompt fix.
- An AI can be a **second reviewer**, but the story decides disagreements, and you are the one accountable.
- Match **review depth to risk**: money and security get a full review, and a sample that finds problems means review everything.

---

## Additional Resources

- Microsoft Research, *Overreliance on AI: Literature Review* (2022): https://www.microsoft.com/en-us/research/publication/overreliance-on-ai-literature-review/
- Civil Resolution Tribunal of British Columbia, *Moffatt v. Air Canada, 2024 BCCRT 149*: https://decisions.civilresolutionbc.ca/crt/crtd/en/525448/1/document.do
- NIST, *AI Risk Management Framework*: https://www.nist.gov/itl/ai-risk-management-framework
