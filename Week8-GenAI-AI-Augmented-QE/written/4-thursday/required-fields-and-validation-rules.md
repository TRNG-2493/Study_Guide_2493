# Required Fields and Validation Rules

## Learning Objectives

By the end of this lesson you will be able to:

- **Distinguish** required and optional fields, and a **missing** field from an **empty** one.
- **Explain** the agent's validation rules R1 to R4 and Q1, and why each one exists.
- **Explain** why these rules cannot be written in a JSON Schema.
- **Check** two agent replies against the rules by hand, and record every rule each one breaks.
- **Separate** the checks into three layers: the schema, the rules and the human checklist.

---

## Why This Matters

In *JSON Schema* you saw a validator pass three replies that were plainly wrong: a test case for **AC9** in a story with four ACs, an expected result of **$99.00**, and an extra field nobody asked for. The schema was not broken. It was doing its job, which is checking **shape**. Those three defects need something it does not have: the **story**.

This lesson writes down the rules that compare a reply with its story. They are short, numbered and checkable: **R1** to **R4** for structure against the story, and **Q1** for the quality of expected results. Today you check them by hand, with pen and paper. Tomorrow, `check_reply.py` checks them automatically, **in exactly this order**, so the rules you write today are the specification for tomorrow's code.

The lesson also settles a question that trips up testers and programs alike: what is the difference between a field that is **missing** and a field that is **empty**? The answer decides whether a reply like US-311's honest refusal is valid or broken.

> **Using this with the handout:** this lesson goes deeper into **Handout 08, Topic 3**. It uses the same rules R1 to R4 and Q1, the same human checklist, the same Reply A (US-312) and Reply B (US-311), and the same answer keys.

---

## The Concept

### 1. Required and Optional

A **required field** must always be present. An **optional** field may be left out.

In TestCaseDesigner's contract, **every** field is required: the four top-level fields and the six fields of every test case. That is a deliberate design choice. With optional fields, a checker would have to guess what an absence means: did the AI decide there were no questions, or did it forget the field? With everything required, an absence has only one meaning: **the reply is broken**.

Optional fields are useful elsewhere: a bug report might have an optional "screenshot" field, because not every bug has one. The rule of thumb is: make a field optional only when "not there" has a clear, harmless meaning. For an agent whose replies will be checked by code, that is rarely true.

### 2. Missing Is Not the Same as Empty

The handout's first key idea:

| | Example | Meaning for `open_questions` |
|---|---|---|
| **Missing** | `{"story_id": "US-205", ...}` with no `open_questions` | ❌ Broken reply: the contract says it is required |
| **Empty** | `"open_questions": []` | ✅ Fine: the agent has no questions |

An everyday comparison helps. An **empty** inbox means you have no messages. A **missing** inbox means your email is not working. Both show you zero messages, but one is good news and the other is a fault.

The difference is real to a program, too. This short demonstration, `missing_vs_empty.py`, loads two replies: one with an empty `open_questions`, one without it:

```python
import json

empty = json.loads('{"story_id": "US-205", "status": "ok", "test_cases": [], "open_questions": []}')
missing = json.loads('{"story_id": "US-205", "status": "ok", "test_cases": []}')

for name, reply in [("empty", empty), ("missing", missing)]:
    print(f"{name}: present? {'open_questions' in reply}, "
          f"value: {reply.get('open_questions', 'NOT THERE')}")

print(len(empty["open_questions"]))       # 0: there, with nothing in it
print(len(missing["open_questions"]))     # crashes: there is nothing to measure
```

It prints:

```text
empty: present? True, value: []
missing: present? False, value: NOT THERE
0
```

and then stops with an error on the last line:

```text
KeyError: 'open_questions'
```

The empty list can be measured: its length is 0. The missing field cannot be measured at all, and the program crashes trying. Any code that uses the reply, such as tomorrow's checker or a report, would crash the same way. That is why "missing" is a broken reply, not just a reply with no questions.

The same applies to `test_cases`. For US-311's honest refusal, `"test_cases": []` is **correct**: the contract's "Saying I can't" section requires it. A reply with no `test_cases` field at all would be broken, even if it had the right status and question.

### 3. The Validation Rules

Some rules cannot be checked by looking at the reply alone. They **compare the reply with the story**. The handout calls them **validation rules** and gives each a short ID:

| ID | Rule | Why |
|---|---|---|
| **R1** | `story_id` in the reply = `story_id` in the story | The reply answers the right story |
| **R2** | Every AC id in the reply exists in the story | No invented requirements |
| **R3** | Number of test cases ≤ `max_cases` | The agent respects the limit |
| **R4** | Every AC in the story has a test case **or** an open question starting with its id | Nothing is forgotten |
| **Q1** | Expected results have no vague words ("works", "correctly", "properly", "as expected", "successfully") | Every test can clearly pass or fail |

Each rule guards against a mistake you have met this week:

| Rule | The mistake it catches | Where you saw it |
|---|---|---|
| R1 | A reply for the wrong story, or a typo in the ID | New: AI tools can mix up stories in a long chat |
| R2 | An invented AC, like AC9 for US-205 | *JSON Schema*: the validator passed it |
| R3 | Too many cases to review | *Agent Architecture*: 6 to 15 cases per run |
| R4 | A criterion silently skipped, like AC4 | *AI-Generated Test Cases* (Wednesday): no case for AC4 |
| Q1 | "Discount is applied correctly" | *AI-Generated Test Cases* (Wednesday): vague expected results |

R4 is worth reading twice. It does not demand a test case for every AC. It demands a test case **or** an open question. That is what lets the agent handle AC4 honestly: it cannot write a test case for "only one coupon per order" without knowing what message appears, so it asks instead. A question **counts** as covering the AC, because it shows the agent looked at it and did not forget it.

The `R` and `Q` prefixes mark two kinds of rule. **R** rules are about **structure against the story**: right story, real ACs, the limit, coverage. **Q** rules are about **quality**. Q1 is the only one for now; Friday may add more.

### 4. Why a Schema Cannot Check These Rules

The handout's third key idea: **rules need both the story and the reply.** A schema sees only the reply.

Take each rule in turn:

- **R1** needs the story's `story_id` to compare with. The schema can check that `"US-031"` **looks like** an ID (`US-` plus three digits); it cannot know it should be `US-311`.
- **R2** needs the story's list of AC ids. To the schema, `AC3` and `AC9` are both just strings.
- **R3** needs the story's `max_cases`, which is different for every story.
- **R4** needs the story's ACs **and** the reply's test cases **and** its questions, all at once.
- **Q1** could, in principle, be written as a schema pattern. But it is easier to read, explain and change as a plain rule with a word list, like the weak-word check you wrote on Wednesday.

So the checks have **layers**. The schema checks the reply on its own. The rules check the reply against the story. And some things need a person.

### 5. What Only a Person Can Check

The handout's fourth key idea: **some things only a person can check.** These go on a **human checklist**:

- **No invented rules or values.** "2 seconds" in a US-311 reply passes every R rule: the story ID matches, AC1 exists, one case is within the limit, AC1 is covered. Only a reader who compares the value with the story sees that it was invented.
- **Every boundary tested at the limit and just below it.** Whether $50.00 and $49.99, or 10 and 9 items, appear in the right test cases depends on understanding each story's numbers.
- **Messages copied exactly.** A program could compare quoted text, as `review_cases.py` did on Wednesday, but deciding whether a case **should** contain a message, and which one, needs a person.

Why not automate these too? Some could be partly automated, and Friday's checks go a little further. But each one depends on **meaning**: what counts as a boundary in this story, whether a number came from the story or from the AI. Those are judgements, and the human-in-the-loop habit from Wednesday applies: code points, people decide.

### 6. Worked Example: Check Two Replies by Hand

#### Step 1 (Editor): Add the rules to `contract.md`

Add this section at the end of `contract.md`:

```text
## Rules (checked by check_reply.py, Friday)
R1  story_id in the reply = story_id in the story
R2  every ac_id in the reply exists in the story (no invented ACs)
R3  number of test cases <= max_cases
R4  every AC in the story has a test case OR an open question starting with its id
Q1  expected results are exact: no "works", "correctly", "properly",
    "as expected" or "successfully"

## Checked by a person (Friday)
- No invented rules or values
- Every boundary tested at the limit and just below it
- Messages copied exactly
```

`contract.md` now holds everything that defines a good reply: the input, the output, the "I can't" rule, the machine-checkable rules and the human checklist. One file, one source of truth.

#### Step 2 (Paper): Check Reply A

This reply is for **US-312** (`max_cases` is 3; the ACs are AC1 and AC2):

```json
{"story_id": "US-312", "status": "ok", "test_cases": [
 {"id": "TC-312-01", "title": "Order with exactly 10 items", "ac_ids": ["AC1"], "type": "boundary",
  "steps": ["Add 10 items", "Go to checkout"], "expected_result": "Free gift wrap is offered"},
 {"id": "TC-312-02", "title": "Order with 9 items", "ac_ids": ["AC1"], "type": "boundary",
  "steps": ["Add 9 items", "Go to checkout"], "expected_result": "Gift wrap works correctly"},
 {"id": "TC-312-03", "title": "Gift wrap message is shown in red", "ac_ids": ["AC3"], "type": "positive",
  "steps": ["Add 10 items", "Go to checkout"], "expected_result": "The gift wrap message is red"},
 {"id": "TC-312-04", "title": "Order with 11 items", "ac_ids": ["AC1"], "type": "positive",
  "steps": ["Add 11 items", "Go to checkout"], "expected_result": "Free gift wrap is offered"}
], "open_questions": []}
```

Go through R1, R2, R3, R4 and Q1 **in order**, and write down every rule it breaks. A tip for R2 and R4: first list the story's AC ids (AC1, AC2), then list every id in the reply's `ac_ids` (AC1, AC1, AC3, AC1) and its questions (none). Compare the two lists.

**Answer key:**

| Rule | Broken? | Why |
|---|---|---|
| R1 | No | `US-312` matches |
| **R2** | **Yes** | TC-312-03 refers to **AC3**, which is not in the story (invented) |
| **R3** | **Yes** | **4** test cases; the maximum is 3 |
| **R4** | **Yes** | **AC2** (the message) has no test case and no question |
| **Q1** | **Yes** | TC-312-02: "works correctly" is vague |

Four of the five rules broken, by a reply that **looks** reasonable at first glance. Before reading the rules, run it through the schema in your head: every field is present, every ID matches its pattern, every `type` is allowed. **It passes the schema.** That is the layering in action.

Look at TC-312-03 once more. "Gift wrap message is shown in red" is not just an invented AC id; it is an invented **requirement**. US-312 says nothing about colour. R2 catches it because the AI had to give it an AC id, and there was no real one to give. That is a useful side effect of the `ac_ids` field: invented requirements often reveal themselves by pointing at criteria that do not exist.

#### Step 3 (Paper): Check Reply B

This reply is for **US-311** (one AC, `max_cases` is 3):

```json
{"story_id": "US-031", "status": "needs_clarification", "test_cases": [],
 "open_questions": ["AC1: What is the maximum time, in seconds, for search results to appear?"]}
```

Check it the same way. Careful: this one is **almost** perfect.

**Answer key:** only **R1** is broken: `"US-031"` should be `"US-311"`, a typo. Everything else is right: no invented ACs, zero cases is within the limit, AC1 is covered by a question that starts with `AC1:`, and there are no expected results for Q1 to check.

Two things are worth noticing. First, `"US-031"` **passes the schema**: it is `US-` followed by three digits. Only R1, comparing with the story, catches it. Second, apart from that typo, this is exactly the honest refusal the contract asks for. The content is right; one character is wrong. A good checker reports exactly that, so the fix is quick and the good content is not thrown away.

#### Step 4 (Paper): Missing or empty?

For Reply B, `test_cases` is `[]`. Is that a problem?

No. Look at the contract's output table, which says `test_cases` "May be empty", and its "Saying I can't" section, which requires `test_cases = []` for a `needs_clarification` reply. The empty list is **correct** here. If the field were **missing**, that would be a broken reply, as section 2 showed.

### 7. The R4 Trap

The handout warns about one common marking mistake, and it is worth understanding properly. Many students mark **R4 as passed** for Reply A, reasoning: *"TC-312-02 tests 9 items, and AC2 is about orders under 10 items, so AC2 is covered."*

But TC-312-02's `ac_ids` says **AC1**, not AC2. R4 looks at the `ac_ids` field, **not** at what the title seems to cover.

Why be so strict? Because tomorrow's checker will be strict. A program cannot read the title "Order with 9 items" and decide it is about AC2; it can only read `ac_ids`. If your hand check is more generous than the program, the two will disagree, and you will not trust either.

More importantly, the strictness is **right**. Look at TC-312-02's expected result: "Gift wrap works correctly". It does not check AC2's message, "Add 10 items for free gift wrap", at all. The case is not really testing AC2. The `ac_ids` field told the truth, and the title misled.

The lesson generalises: **check what the data says, not what it seems to mean.** It is the same habit as reading an assert rather than a test name, from *AI-Assisted Automation Development* on Wednesday.

### 8. Why the Rules Are Checked in Order

The handout says to check R1, R2, R3, R4 and Q1 **in order**, and tomorrow's checker does the same. The order is not arbitrary:

1. **R1 first**, because if the reply is for the wrong story, every other check compares it with the wrong ACs and the wrong limit. Its results would be meaningless.
2. **R2 next**, because it finds invented ACs before R4 counts coverage. An invented AC3 test case should not be mistaken for useful coverage.
3. **R3**, a simple count.
4. **R4**, coverage, which needs the story's full AC list.
5. **Q1 last**, because it looks at the content of individual expected results, the most detailed check.

The general idea, **check the broadest things first**, is common in testing. There is little point checking the spelling on a page that failed to load.

Note that checking in order does **not** mean stopping at the first failure. Reply A broke four rules, and a useful report lists all four, so they can all be fixed at once.

### 9. Three Layers of Checking

Put the day's checks together and you get three layers, each catching what the others cannot:

| Problem | Schema | Rules (R1–R4, Q1) | Person |
|---|---|---|---|
| `status` is "done" | ✅ catches it | | |
| `expected_result` missing | ✅ catches it | | |
| `story_id` is "US-031" for US-311 | ❌ passes | ✅ R1 | |
| A test case for AC3 in US-312 | ❌ passes | ✅ R2 | |
| 4 test cases when the maximum is 3 | ❌ passes | ✅ R3 | |
| AC2 has no case and no question | ❌ passes | ✅ R4 | |
| "Gift wrap works correctly" | ❌ passes | ✅ Q1 | |
| "Within 2 seconds" invented for US-311 | ❌ passes | ❌ passes | ✅ catches it |
| No test at $49.99 | ❌ passes | ❌ passes | ✅ catches it |

Read the table from the bottom up. The last two rows pass **every** automatic check. They are the most important mistakes an AI makes, invented values and missing boundaries, and they need a person. That is not a failure of the checks. It is the reason the human checklist exists, and the reason Wednesday's *Human Validation of AI Output* still applies to everything the agent produces.

The automatic layers have a different value: they make the human layer **smaller**. If code has already rejected the broken replies, and flagged the invented ACs, the uncovered criteria and the vague results, the reviewer can spend their attention on the questions only a person can answer.

### 10. The Limits of Q1

Q1 is a word list, like Wednesday's weak-word check, and it shares the same limits.

It can **miss** vague results that use other words. "Gift wrap is fine" and "Everything looks good" contain none of the five words, and both are just as vague.

It can also **flag** results that are fine. The rule as written looks for the words; an expected result such as *"The message 'Payment completed successfully' is shown"* contains "successfully" inside an **exact message** copied from a story. That is precise, not vague. A person reading the flag would see that at once.

So treat Q1 the way you treated `word_check.py`: as a **pointer** to results worth reading, not a judge. A Q1 flag means "look at this one"; no flag does not mean "this one is fine".

### 11. What Makes a Good Rule

R1 to R4 and Q1 share four features. They are worth copying whenever you write a rule of your own, for this agent or another:

| Feature | In R3 | Why it matters |
|---|---|---|
| **A short ID** | `R3` | Easy to refer to in a review, a results table or a bug report |
| **An exact comparison** | number of test cases ≤ `max_cases` | Two people checking the same reply get the same answer |
| **A clear pass or fail** | Either 4 ≤ 3 or it is not | No "partly passed" |
| **A stated reason** | "The agent respects the limit" | People know why it exists, so nobody deletes it by mistake |

Compare a weak version: *"Test cases should match the story."* It has no ID, no exact comparison and no clear pass/fail. Two reviewers would disagree about Reply A, and no program could check it. Split into exact pieces, the same idea becomes R1 (right story), R2 (real ACs) and R4 (nothing forgotten).

That splitting is the skill. Almost every vague rule contains several exact ones, the same lesson as *Agent Instructions*, where "write good test cases" became two checkable rules. Rules in the instructions tell the AI what to do; rules in the contract tell the checker what to verify. The best agents have the **same** rules in both places: the instructions say "never return more than the maximum", and R3 checks it.

### 12. Recording a Check

A check is only useful if its result is written down clearly. For Reply A, a good one-line record names the story, the overall result and every broken rule with its evidence:

```text
US-312: FAIL  R2 (TC-312-03 uses AC3)  R3 (4 cases, max 3)  R4 (AC2 not covered)  Q1 (TC-312-02 "works correctly")
```

And for Reply B:

```text
US-311: FAIL  R1 (story_id "US-031", expected "US-311")
```

Notice that each broken rule carries its **evidence**: which test case, which value, what was expected. A record that says only "FAIL R2" sends the reader back to the reply to find out why. A record with evidence can be acted on immediately, the same principle as a good bug report quoting the requirement it breaks, from *AI within the QA Lifecycle* on Wednesday.

Tomorrow, the checker writes records like these for every story, and collects them into a results table. Today's hand-written versions are the specification for that output: if your hand records and the program's records disagree, one of them is wrong, and the rules in `contract.md` decide which.

### 13. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| You marked R4 as passed for Reply A | TC-312-02 is about 9 items, but its `ac_ids` says **AC1**, not AC2 | R4 looks at `ac_ids`, not at what the title seems to cover |
| You thought `test_cases: []` breaks the contract | Confusing **empty** with **missing** | Empty is allowed; missing is not |
| You stopped after the first broken rule | It feels like enough to reject the reply | Check every rule, so all the fixes can be made at once |
| You missed the R1 typo in Reply B | "US-031" looks like a valid ID | Compare the reply's ID with the story's, character by character |
| Your hand record says only "FAIL" | Writing evidence feels slow | Name the test case and the value for every broken rule |
| A Q1 flag on an exact message | The vague word is part of a quoted message | Read every Q1 flag; it is a pointer, not a verdict |

---

## Practice Exercises

1. **Fix Reply A (paper, 10 min).** Fix Reply A on paper so it breaks **no** rules. What is the smallest set of changes? Check your fixed reply against R1 to R4 and Q1, and against the human checklist.

2. **Break only R4 (paper, 15 min).** Write a reply for US-205 that breaks **only R4**. Swap with a classmate and check each other's. Did your classmate's reply accidentally break anything else?

3. **Ask the AI to check (AI tool, 15 min).** Follow this week's four steps:
   - **Prompt:** paste `contract.md` and Reply A into your AI tool and ask: *"Which of the rules R1, R2, R3, R4 and Q1 does this reply break? Answer as a table."*
   - **Review:** compare its table with the answer key. Did it find all four? Did it fall into the R4 trap?
   - **Run:** ask the same about Reply B. Does it find the R1 typo?
   - **Record:** in `prompts.txt`, note which rules it got right and wrong.

4. **Q1 by hand (paper, 10 min).** For each expected result, say whether Q1 flags it, and whether it is really vague: (a) "Total is $45.00"; (b) "Coupon works as expected"; (c) "Discount looks right"; (d) "The message 'Order placed successfully' is shown".

5. **Write the records (paper, 5 min).** Using section 12 as a model, write the one-line record for your fixed Reply A from exercise 1, and for the reply you wrote in exercise 2.

---

## Knowledge Check

1. What is the difference between a missing field and an empty one?

<details><summary>Answer</summary>

Missing means the field is not there at all, which makes the reply broken. Empty means it is there with nothing in it, such as `[]`, which can be fine.

</details>

2. Why are all the fields in our contract required?

<details><summary>Answer</summary>

So an absence always means one thing: the reply is broken. With optional fields, a checker would have to guess whether "not there" meant "none" or "forgot".

</details>

3. What does R4 check, and why does an open question count?

<details><summary>Answer</summary>

That every AC in the story has a test case or an open question starting with its id. A question shows the agent considered the AC instead of forgetting it, which is the honest answer for an incomplete AC like AC4.

</details>

4. Why can a JSON Schema not check R2?

<details><summary>Answer</summary>

R2 compares the reply's AC ids with the story's. A schema only sees the reply, so it cannot know which AC ids exist.

</details>

5. Which rules does Reply A break?

<details><summary>Answer</summary>

R2 (AC3 is invented), R3 (4 test cases, maximum 3), R4 (AC2 has no case and no question) and Q1 ("works correctly").

</details>

6. Reply B's `story_id` is "US-031". Why does the schema pass it, and which rule catches it?

<details><summary>Answer</summary>

It matches the pattern: `US-` plus three digits. R1 catches it by comparing it with the story's ID, US-311.

</details>

7. Why is R1 checked first?

<details><summary>Answer</summary>

If the reply is for the wrong story, every other rule compares it with the wrong ACs and limit, so their results would be meaningless.

</details>

8. Name two mistakes that pass the schema and all five rules.

<details><summary>Answer</summary>

An invented value, such as "within 2 seconds" for US-311, and a missing boundary test, such as no case at $49.99. Only a person catches these.

</details>

---

## Glossary

- **Required field:** a field that must always be present.
- **Optional field:** a field that may be left out.
- **Missing vs empty:** not there at all vs there with nothing in it.
- **`KeyError`:** Python's error when code asks for a dictionary key that is not there.
- **Validation rule:** a rule that compares the reply with the story, such as R1 to R4.
- **Quality rule:** a rule about the content of the reply, such as Q1.
- **Coverage (R4):** every AC has a test case or an open question.
- **Human checklist:** the checks only a person can do: invented values, boundaries, exact messages.
- **Layers of checking:** schema (shape), rules (reply against story), person (meaning).
- **Evidence (in a check record):** the specific value or test case that shows why a rule failed.
- **Pointer (check):** a check that flags things worth reading, rather than giving a final verdict.

---

## Summary

- **Missing is not empty.** An empty list means "none"; a missing field means a broken reply. Our contract makes every field required, so an absence always means broken.
- **R1 to R4 and Q1** compare the reply with the story: right story, no invented ACs, within the limit, nothing forgotten, no vague expected results.
- A **schema cannot check them**, because it sees only the reply.
- **Reply A** broke R2, R3, R4 and Q1 while passing the schema. **Reply B** broke only R1, with a typo the schema also passed.
- Checks come in **three layers**. Invented values and missing boundaries pass both automatic layers, so the **human checklist** stays essential.

---

## Additional Resources

- JSON Schema, *Understanding JSON Schema: the basics*: https://json-schema.org/understanding-json-schema/basics
- Python documentation, *Data Structures: dictionaries* (keys, `in` and `get`): https://docs.python.org/3/tutorial/datastructures.html#dictionaries
- ISTQB, *Certified Tester Foundation Level Syllabus v4.0.1* (test oracles and expected results): https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
