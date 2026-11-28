# Agent Output Validation

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** the two layers of agent output validation, the checker script and the human checklist, and what each one can and cannot see.
- **Apply** the human checklist H1 to H4 to an agent reply, and link each question to the instruction rule it protects.
- **Decide** what happens to each reply: accept, fix the instructions, or send questions to the business analyst (BA).
- **Record** every problem with the rule it breaks, ready for improving the agent.
- **Explain** why a script PASS means "well-formed", not "correct".

---

## Why This Matters

Earlier today, in *Implementing IO Contracts*, the checker gave the US-311 sample reply a clean **PASS**. That reply invents a time limit, "within 2 seconds", for a story that never mentions one, and says `status: "ok"` when the honest answer was "I can't test this yet". If PASS meant "accept", an invented requirement would now be on its way to the test team, formatted perfectly and approved by code.

This is not a weakness of our particular checker. It is the nature of automatic checks. Code can confirm that a reply has the right **shape** and follows the rules that compare it with the story. It cannot understand what the reply **means**. On Wednesday, in *Human Validation of AI Output*, you learned a method for reviewing AI drafts: a checklist, three decisions, a written reason. This lesson applies the same method to the agent's replies, as the second layer on top of the checker.

The principle matters well beyond this course. Microsoft researchers, reviewing around 60 studies on overreliance on AI, noted that people are increasingly treated as **the last line of defense** against AI failures ([Microsoft Research](https://www.microsoft.com/en-us/research/publication/overreliance-on-ai-literature-review/)). An agent with a checker reduces how much the person has to look at. It does not remove the person.

> **Using this with the handout:** this lesson goes deeper into **Handout 10, Topic 1**. It uses the same two layers, the same human checklist H1 to H4, the same decision table, the same second-opinion prompt and the same answer key for the three v1 sample replies.

---

## The Concept

### 1. What Is Agent Output Validation?

**Agent output validation** means checking every answer **before anyone uses it**, in two layers:

- The **checker script** tests the contract: the JSON, the required fields, and rules R1 to R4 and Q1. It is fast and always gives the same result, but it cannot understand meaning.
- The **human review** checks what code cannot: invented rules or values, missing boundaries, messages not copied exactly, and whether the agent should have refused.

A reply is only **accepted** when it passes **both** layers. A script "PASS" means "well-formed", **not** "correct".

### 2. Two Layers, Different Jobs

| Layer | Checks | Strength | Blind spot |
|---|---|---|---|
| **Script** (`check_reply.py`) | JSON, fields, R1 to R4, Q1 | Fast, identical every time | Cannot see invented values or meaning |
| **Human checklist** | H1 to H4 (below) | Understands meaning | Slower; needs care |

The two layers are not competitors; they **cover each other's blind spots**. The script never tires, never skips a rule and never falls into the R4 trap. The person notices that "2 seconds" is not in the story, which no rule in the script could know.

There is also an order. The script goes **first**, because it is fast and it filters out the mechanically broken replies. The person then spends their attention on the replies that are well-formed, asking only the questions that need a person. That is the "code points, humans decide" idea from Wednesday, built into the agent.

### 3. The Human Checklist

The human checklist has four questions. Each one protects one of the instruction rules that the rule map in *Building Agent Instructions* marked as "human review":

| ID | Question | Linked instruction rule |
|---|---|---|
| **H1** | Is every rule or value in the test cases actually in the story? | G1 |
| **H2** | Is every numeric limit tested at the limit **and** just below it? | B1 |
| **H3** | Is every message copied **exactly**? | M1 |
| **H4** | Is the status right? (A story with no measurable value should be `needs_clarification`) | U1 |

Each question needs a slightly different way of reading the reply:

- **H1: read every title and expected result against the story.** Invented rules often show in a **title** ("Lowercase save10 is accepted"); invented values often show in an **expected result** ("within 2 seconds"). For each claim, ask: where in the story does it say that?
- **H2: list the story's limits first**, then look for both tests. US-205 has one limit ($50.00), so you need $50.00 and $49.99. US-312 has one limit (10 items), so you need 10 and 9. A test at $50.01 is a welcome extra; it does not replace $49.99.
- **H3: find every quoted message in the story**, then look for it, character for character, in the expected results. "Spend $50 to use SAVE10" is not "Spend $50.00 to use SAVE10".
- **H4: ask whether the story could be tested at all.** If a criterion has no measurable value, the honest status is `needs_clarification`, with a question. A status of `"ok"` with invented test cases is the wrong answer, however tidy it looks.

### 4. Every Reply Gets a Decision

| Script | Human | Decision |
|---|---|---|
| PASS | OK | **Accept**: the test cases go to the tester |
| FAIL | (any) | **Fix the instructions** or rerun |
| PASS | Problem found | **Fix the instructions**: the script missed it |
| PASS, `needs_clarification` | OK | **Send the questions to the BA** |

Three things about this table are worth noticing.

- **There is no "accept anyway".** A reply with a known problem is not used, even if the problem looks small. The test cases go to a tester who will rely on them.
- **"Fix the instructions" means the agent, not the reply.** You do not hand-edit the reply into shape. A hand-edited reply hides the agent's real behaviour, and the same mistake would come back on the next story. The fix goes into the next version of the instructions, later today.
- **`needs_clarification` can be a success.** When the agent honestly says it cannot test a story, and the human agrees, that is the right result. The questions go to the BA, as on Wednesday.

### 5. Record Why

The handout's fourth key idea: **record why.** For every problem, note which rule it breaks: `R...`, `Q...` or `H...`.

This is the correction log from Wednesday, with the agent's rule IDs as the reason categories. Later today, in *Agent Testing and Refinement*, those notes are counted, and the counts tell you exactly what to improve. A note that says only "bad reply" cannot be counted. A note that says "H1: TC-205-05 invents lowercase codes" can.

### 6. Worked Example: Review the Three v1 Replies

This worked example uses the **sample replies** from *Creating Reusable Prompt Templates*. If you used your own AI's replies, follow the same steps with yours.

#### Step 1 (Terminal): Get the script verdicts

Run the checker for each story. In `check_reply.py`'s bottom block, change the two file names to each story in turn, and run `python check_reply.py`. Write down PASS or FAIL and the problems for each story. (In *Building Validation Scripts*, a runner will do this for every story in one go.)

With the sample replies, the verdicts are the ones you saw in *Implementing IO Contracts*:

| Story | Script |
|---|---|
| US-205 | FAIL: R3 (6 test cases, max 5), R4 (AC4 forgotten) |
| US-311 | PASS |
| US-312 | FAIL: Q1 (TC-312-02 vague) |

#### Step 2 (Paper): Human review with the checklist

Open each reply in your editor and answer H1 to H4 for it. Fill in a table like this one before reading the answer key:

| Story | H1 nothing invented? | H2 boundaries? | H3 exact messages? | H4 right status? |
|---|---|---|---|---|
| US-205 | | | | |
| US-311 | | | | |
| US-312 | | | | |

**Tips from the handout:** for US-205, look closely at **TC-205-05**. For US-311, ask: is "2 seconds" anywhere in the story? For US-312, compare TC-312-02's expected result with AC2's message.

#### Step 3 (AI tool): Get a second opinion (optional)

AI can help with the human checklist, but it does not replace you. Open a **new chat** and paste:

```text
Review this AI-generated reply against the user story. Answer each question with Yes or No and one line of explanation.
H1: Is every rule or value in the test cases stated in the story?
H2: Is every numeric limit tested at the limit and just below it?
H3: Is every message copied exactly from the story?
H4: If the story has no measurable value, did the reply ask instead of inventing one?

### Story
<paste the story's acceptance criteria here>

### Reply
<paste the reply here>
```

Replace the two `<paste ... here>` lines. Compare its answers with yours. Where you disagree, **the story decides**: re-read the exact acceptance criterion, not your memory of it, and not the AI's confidence.

#### Step 4 (Paper): Decide

Using the decision table in section 4, write a decision for each reply: accept, fix the instructions, or send questions to the BA.

### 7. The Answer Key, Explained

| Story | Script | Human | Decision |
|---|---|---|---|
| US-205 | **FAIL**: R3 (6 test cases, max 5), R4 (AC4 forgotten) | **H1 ✗**: TC-205-05 invents "lowercase save10 is accepted". H2 ✓ ($50.00 and $49.99), H3 ✓, H4 ✓ | Fix the instructions |
| US-311 | **PASS** | **H1 ✗**: "2 seconds" is invented. **H4 ✗**: should be `needs_clarification` | Fix the instructions. **The script missed this one** |
| US-312 | **FAIL**: Q1 (TC-312-02 vague) | H2 ✓ (10 and 9 items). **H3 ✗**: AC2's message "Add 10 items for free gift wrap" is not copied | Fix the instructions |

Each row teaches something different.

**US-205: the script and the person find different problems.** The script found R3 and R4. The person found H1: TC-205-05, "Lowercase save10 is accepted", is the invented rule you have traced all week, now produced by the agent. The script could not see it, because the test case points at AC3, which exists. If only the script's findings were fixed, the invented rule would survive into v1.1. Notice also that H2 passes: TC-205-02 tests $50.00 and TC-205-03 tests $49.99, and TC-205-06 adds $50.01, a good extra.

**US-311: the script passes a wrong reply.** Every rule the checker knows is satisfied. The person sees two problems in one: H1, because "2 seconds" is not in the story, and H4, because a story with no measurable value should have been refused. This is the row that justifies the whole human layer.

**US-312: one problem, seen from two sides.** The script found Q1: "The message works as expected" is vague. The person found H3: AC2's exact message, "Add 10 items for free gift wrap", appears nowhere. These are the **same defect** from two angles: the vague phrase is **where** the exact message should have been. Recording both is still right, because they point to two different instruction rules (Q1 and M1), and either rule, strengthened, might fix it.

The handout calls the US-311 row **the big lesson**: it **passed the script** and was still **wrong**. Without the human layer, an invented requirement would have reached the test team.

### 8. Saving the Review: `review_v1.md`

Save your completed review in the `agent` folder as `review_v1.md`, so it can be counted later today. A simple layout that keeps everything together:

```text
# Review v1 (sample replies)
Reviewer: <your name>   Date: <date>

| Story  | Script                 | H1 | H2 | H3 | H4 | Decision | Notes |
|--------|------------------------|----|----|----|----|----------|-------|
| US-205 | FAIL R3, R4            | ✗  | ✓  | ✓  | ✓  | Fix      | H1: TC-205-05 invents lowercase codes |
| US-311 | PASS                   | ✗  | -  | -  | ✗  | Fix      | H1: "2 seconds" invented; H4: should be needs_clarification |
| US-312 | FAIL Q1                | ✓  | ✓  | ✗  | ✓  | Fix      | H3: AC2 message not copied (TC-312-02) |
```

Three features make it useful later:

- **Reviewer and date**, for accountability, as on Wednesday.
- **Every ✗ has a note** with the test case and the evidence, so anyone can check the finding.
- **"-" where a question does not apply.** US-311 has no numeric limit and no message, so H2 and H3 cannot fail. Writing "-" instead of "✓" keeps the review honest: nothing was checked, so nothing passed.

### 9. Edge Calls: Test Data or Invented Value?

H1 asks whether every rule or value is in the story. Applied too literally, it would fail almost every reply, because test cases are **full** of values the story does not mention. US-205's TC-205-01 uses a $100.00 subtotal; the story never says "$100.00". Is that invented?

No, and the difference matters. There are two kinds of value in a test case:

| Kind | Example | Where it comes from | H1 verdict |
|---|---|---|---|
| **Test data**: an input the tester chooses | $100.00 subtotal; order number 00000000 | Any value allowed by the story | ✓ Fine, if it follows the story's rules |
| **Expected behaviour**: a claim about what the system does | "within 2 seconds"; "lowercase save10 is accepted" | Must come from the story | ✗ Invented, if the story does not say it |

Test data is chosen; expected behaviour is **stated**. $100.00 is a sensible input for "a subtotal of $50.00 or more", and the expected result, $90.00, follows from AC1. "Within 2 seconds" is a claim about how the system must behave, and nothing in US-311 makes it.

Some calls are closer. Three, **illustrative**, from the sample replies:

- **US-313, "Enter order number 00000000".** Test data for "an unknown order number". It assumes that 00000000 is not a real order, which is a reasonable choice for a tester to make. The handout marks US-313 H1 ✓. A careful reviewer might add a note: "check 00000000 is unknown in the test environment".
- **US-312, "Free gift wrap is offered".** AC1 says orders of 10 or more items "get free gift wrap". "Is offered" is a slight paraphrase: does the shopper have to accept it? It is not a quoted message, so H3 does not apply, and it does not add a new rule. ✓, perhaps with a note to confirm the wording with the BA.
- **US-205, "Total is $54.00" in TC-205-05.** The arithmetic is right (10% off $60.00), but the whole case rests on an invented rule. The value is not the problem; the rule is. ✗ under H1.

The question that settles every edge call is the one from Wednesday: **can you point to the words in the story that make this true?** For test data, point to the rule it satisfies. For expected behaviour, point to the rule that states it. If you cannot point to anything, it is invented.

### 10. Reviewing Your Own AI's Replies

The answer key uses the sample replies, so everyone has a common reference. Your own AI's replies will differ, and that is fine. Some patterns to expect when you review them:

- **More or fewer test cases.** Count them against `max_cases`; the script will too.
- **Different but valid test data.** $75.00 instead of $100.00 is fine; H1 is about behaviour, not about matching the sample.
- **A different AC4 question.** Any question starting with `AC4:` that asks what happens on a second coupon satisfies U1 and R4.
- **A good reply.** Your AI may get US-311 right even with v1. If so, record it honestly: a PASS with H1 to H4 ✓ is an **accept**. The point of the review is the truth about **your** replies, not agreement with the sample.

When your review differs from a classmate's, compare the **evidence**, not the verdicts. "I marked H1 ✗ because TC-205-05 says lowercase works, and US-205 only mentions SAVE10" can be checked. "I just thought it looked wrong" cannot.

### 11. Could the Human Checks Become Code?

The handout's exercise 3 asks whether any of H1 to H4 could be turned into code. Some can, **partly**. H3 is the easiest. A short script can find every quoted message in a story and look for it in the reply's expected results. This one, `message_check.py`, is optional and uses the same defensive parsing as the checker:

```python
import json
import sys

story = json.load(open(f"stories/{sys.argv[1]}.json", encoding="utf-8"))
reply_text = open(f"replies/{sys.argv[2]}/{sys.argv[1]}.txt", encoding="utf-8").read()
reply = json.loads(reply_text[reply_text.find("{"):reply_text.rfind("}") + 1])

expected = " ".join(tc.get("expected_result", "") for tc in reply["test_cases"])
for ac in story["acceptance_criteria"]:
    if '"' in ac["text"]:
        message = ac["text"].split('"')[1]
        found = message in expected
        print(f"{ac['id']}: \"{message}\" {'copied' if found else 'NOT FOUND in any expected result'}")
```

Running `python message_check.py US-312 v1` on the sample reply prints:

```text
AC2: "Add 10 items for free gift wrap" NOT FOUND in any expected result
```

and for US-205:

```text
AC2: "Spend $50.00 to use SAVE10" copied
AC3: "Coupon code not recognised" copied
```

It finds exactly the H3 problem from the answer key. So why is H3 still on the **human** checklist? Because the script answers a narrower question than H3 does. It checks that each message appears **somewhere**, not that it appears in the **right** test case, or that the test case around it makes sense.

A reply could copy "Add 10 items for free gift wrap" into the expected result of the **10-item** case, where the message should **not** appear, and the script would say "copied". It is a **pointer**: a fast way to find likely H3 problems, which a person then confirms.

The other checks are harder:

| Check | Could code help? | What it would still miss |
|---|---|---|
| **H1** invented values | A little: flag numbers in the reply that are not in the story | Invented **rules** with no numbers, such as lowercase codes |
| **H2** boundaries | Partly: find the story's numbers, look for them and "just below" in the steps | Which number is the real limit, and what "just below" means (49.99 or 9) |
| **H3** exact messages | Mostly: as above | Whether the message is in the right test case |
| **H4** status | A little: flag vague words in the story, as Wednesday's `word_check.py` did | Whether the story is really untestable |

This is the same lesson as all week: code can **point**, a person **decides**. Each pointer you add makes the human review faster, and none of them makes it unnecessary.

### 12. A Fifth Human Check

The handout's exercise 2 asks for a fifth human check. A good candidate, **illustrative**, is about the test steps:

> **H5:** Could a tester who has never seen the feature follow the steps exactly, with the test data written down?

It protects against the vague steps you met on Wednesday in *AI-Generated Test Cases*, such as "Add items to the cart" when the whole point is a $50.00 subtotal. Look at the sample replies with H5 in mind. US-205's steps are good: "Add items totalling $50.00, Enter SAVE10, Click Apply". US-313's TC-313-01 says "Enter a valid order number", which a tester could follow only if they know where to find one: a reasonable H5 note, even though the case passes H1 to H4.

If you add H5, give it a linked instruction rule (for example, a new rule asking for specific test data in the steps), and add both to the rule map. A check with no rule behind it finds problems the agent was never told to avoid.

### 13. How Much Human Review?

With three stories, reviewing every reply in full is easy. With thirty, the review-depth table from Wednesday applies:

- **Money, security and personal data are high risk**: review every reply fully. US-205, a discount, is in this group.
- **A script FAIL does not need a full human review yet**: the reply will be fixed through the instructions and rerun. A quick look for the most important H problems is still worth it, so the fix covers everything at once.
- **Every script PASS needs a human review**, because that is where invented values hide. US-311 showed why.
- **If a review finds a problem, look harder at the rest.** One invented rule suggests a missing line in the instructions, which affects every story.

### 14. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| You marked US-311 as "accept" | The script said PASS | PASS means well-formed, not correct. Always do the human checklist |
| The AI second opinion disagrees with you | The AI can be wrong too | Re-read the story. The story is the only source of truth |
| You hand-edited a reply to fix it | It seemed quicker | Never edit replies; fix the instructions and rerun |
| A ✗ in the review has no note | It felt obvious at the time | Every ✗ needs the test case and the evidence, so it can be counted and checked |
| You marked a $100.00 test as invented | Test data and expected behaviour were confused | Chosen inputs are fine if they follow the story's rules; only claims about behaviour must be stated |
| You ticked H2 for a story with no limit | Nothing failed, so it seemed like a pass | Use "-" when a question does not apply |

---

## Practice Exercises

1. **Compare reviews (paper, 5 min).** Compare your review table with a neighbour's. Did you both catch TC-205-05? Did you both record US-312's problem under H3 as well as Q1?

2. **Review your own replies (AI tool, 20 min).** Follow this week's four steps:
   - **Prompt:** if you saved your own AI's v1 replies, use those.
   - **Review:** apply H1 to H4 to each, before running the script.
   - **Run:** run the checker on each, and compare its verdicts with your human review. Where do they disagree?
   - **Record:** save the result as `review_v1.md`, with a note for every ✗.

3. **A fifth check (paper, 10 min).** Write a fifth human check, H5, as a one-line question, using section 10 as a model. Which instruction rule would it protect? Apply it to the three sample replies.

4. **Code for a human check (paper or code, 15 min).** Pick one of H1, H2 or H4. Describe in one sentence how a script might check it, and what it would still miss. If you like, run `message_check.py` on all the sample replies and confirm it agrees with your H3 column.

5. **Edge calls (paper, 10 min).** For each value, say whether it is test data or expected behaviour, and whether it passes H1 for its story: (a) a US-205 test with a $75.00 subtotal; (b) a US-312 expected result "Gift wrap is free for members"; (c) a US-313 step "Enter order number 12345678"; (d) a US-311 expected result "Results appear instantly".

---

## Knowledge Check

1. What are the two layers of output validation, and what does each catch?

<details><summary>Answer</summary>

The checker script (JSON, fields, R1 to R4, Q1: well-formed and rule-following) and the human checklist (H1 to H4: invented values, boundaries, exact messages, right status).

</details>

2. US-311 passed the checker but was still wrong. Why?

<details><summary>Answer</summary>

The checker cannot tell that "2 seconds" was invented, or that the story should have been refused. Only a person comparing the reply with the story can.

</details>

3. Which instruction rule does each human check protect?

<details><summary>Answer</summary>

H1 protects G1, H2 protects B1, H3 protects M1, and H4 protects U1.

</details>

4. TC-205-05 points at AC3. Why does the script not catch it, and which human check does?

<details><summary>Answer</summary>

AC3 exists, so R2 is satisfied. H1 catches it: lowercase codes are not in the story.

</details>

5. US-312 fails Q1 and H3. Are these two separate defects?

<details><summary>Answer</summary>

They are the same defect seen from two sides: the vague phrase sits where the exact message should be. Both are recorded because they point to two rules (Q1 and M1).

</details>

6. What decision does a script PASS with `needs_clarification` get, if the human agrees?

<details><summary>Answer</summary>

Send the open questions to the BA.

</details>

7. Why do you never hand-edit an agent reply to fix it?

<details><summary>Answer</summary>

It hides the agent's real behaviour, and the same mistake would return on the next story. The fix goes into the next version of the instructions.

</details>

8. `message_check.py` reports a message as "copied". Why is H3 still a human check?

<details><summary>Answer</summary>

The script only checks that the message appears somewhere, not that it is in the right test case or that the case makes sense.

</details>

9. TC-205-01 uses a $100.00 subtotal, which the story never mentions. Does it fail H1? Why?

<details><summary>Answer</summary>

No. $100.00 is test data, an input the tester chooses within the story's rules. H1 is about expected behaviour; "Total is $90.00" follows from AC1.

</details>

---

## Glossary

- **Agent output validation:** checking every agent answer before it is used.
- **Two layers:** the checker script (contract) and the human checklist (meaning).
- **Human checklist:** questions H1 to H4 that check meaning, which code cannot.
- **Well-formed:** matching the contract's shape and rules, whether or not the content is correct.
- **Decision:** what happens to a reply: accept, fix the instructions, or send questions to the BA.
- **Second opinion:** an AI's review of a reply, used for comparison, never as the verdict.
- **`review_v1.md`:** the saved human review of the v1 replies, with a note for every problem.
- **Test data vs expected behaviour:** chosen inputs, which may be any allowed value, vs claims about what the system does, which must come from the story.
- **Edge call:** a review decision that is not obvious and needs evidence from the story.
- **Pointer (check):** a check that flags likely problems for a person to confirm.
- **Not applicable ("-"):** a review mark for a question that cannot fail for this story.

---

## Summary

- **Validate in two layers:** the script checks the contract; a person checks the meaning. **PASS means well-formed, not correct.**
- The **human checklist** H1 to H4 protects G1, B1, M1 and U1: nothing invented, both boundary tests, exact messages, the right status.
- **Every reply gets a decision**: accept, fix the instructions, or send questions to the BA. Never hand-edit a reply.
- **Record why**, with rule IDs and evidence, in `review_v1.md`. Those notes drive the improvements later today.
- **US-311 passed the script and was wrong.** Code can point; a person decides.

---

## Additional Resources

- Microsoft Research, *Overreliance on AI: Literature Review* (2022): https://www.microsoft.com/en-us/research/publication/overreliance-on-ai-literature-review/
- NIST, *AI Risk Management Framework*: https://www.nist.gov/itl/ai-risk-management-framework
- OpenAI, *A practical guide to building agents* (PDF; human intervention and guardrails): https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
