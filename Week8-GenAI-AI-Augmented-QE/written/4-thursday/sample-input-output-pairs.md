# Sample Input/Output Pairs

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a **sample input/output pair** is and why every agent contract should come with a set of them.
- Describe the **four jobs** pairs do: specification by example, few-shot examples, regression (golden) data and contract test data.
- Explain why **exact-match** expected outputs usually do not work for an LLM agent, and write **property-based expectations** using **MUST / MUST NOT / MAY**.
- Describe the **anatomy of a pair file**: id, category, purpose, input, expected output and expectations.
- Design pairs in five **categories**: happy path, edge, clarification, invalid input and out of scope.
- Build a **coverage matrix** against the contract rules (R1-R6) and statuses, and spot gaps and thin areas.
- Keep pairs **honest** (written by humans from the requirement, reviewed, versioned with the contract) and store them in a sensible **folder layout**.
- Use Python and `jsonschema` to check that every pair **obeys the contract itself**, and print a coverage matrix.

---

## Why This Matters

Today you have taken a QA agent apart piece by piece: its **architecture**, its **instructions**, its **prompt templates**, its **input/output contract**, that contract written in **JSON Schema**, and the **required fields and validation rules** (R1-R6) that the schema alone cannot express.

All of those pieces are *descriptions*. A schema says "`type` must be one of positive, negative or boundary". A rule says "every acceptance criterion must be covered". But people still ask: *"OK, but what does a good answer actually look like?"*

Sample input/output pairs answer that question with **concrete examples**. In testing terms they are the agent's **test data and expected results**: without them you cannot say whether an answer is right, whether a prompt change made things better or worse, or whether a teammate understood the contract the way you did.

This is the "IO contracts" part of the **Weekly Epic** made concrete. It also feeds **Project 2 (Test Automation Framework)**: in today's pair-programming exercise you design instructions, a schema and **sample pairs** for a requirements agent, and on Friday you build a first QA agent and run it against pairs like these.

> **Scope note.** Today is about **designing** pairs: what they contain, which ones to write, how to keep them honest and how to check that they obey the contract. **Running the agent against the pairs and scoring its answers** (executing agents against QA requirements, agent output validation, building validation scripts, testing and refinement) is covered on **Friday**. Using one model to grade another (**LLM-as-judge**) is covered in **Week 10**. Here we only name them.

---

## The Concept

### 1. What Is a Sample Input/Output Pair?

A **sample input/output pair** (also called a "sample" or a "golden example") is:

1. one **input** that a caller could send to the agent,
2. the **output** we expect the agent to return for it, and
3. a short description of **what makes an answer acceptable**.

Think of a maths textbook. Each chapter explains a rule and then shows a **worked example**: the problem, the correct answer, and why. Students learn more from the worked example than from the rule alone, because it removes doubt. The **answer key** at the back does a second job: it lets students check their own work. A sample pair is a worked example and an answer key at the same time, for an agent.

Here is a pair for our running example, the **TestCaseDesigner** agent (v1.0.0). You have seen both halves earlier today.

**Input** (a user story with acceptance criteria):

```json
{
  "story_id": "US-205",
  "title": "Apply coupon at checkout",
  "acceptance_criteria": [
    {"id": "AC1", "text": "SAVE10 gives 10% off a subtotal of $50.00 or more."},
    {"id": "AC2", "text": "Subtotals under $50.00 are unchanged and show \"Spend $50.00 to use SAVE10\"."},
    {"id": "AC3", "text": "Unknown codes show \"Coupon code not recognised\"."},
    {"id": "AC4", "text": "Only one coupon per order."}
  ],
  "techniques": ["EP", "BVA"],
  "max_cases": 6
}
```

**Expected output** (test cases as JSON):

```json
{
  "contract_version": "1.0.0",
  "story_id": "US-205",
  "status": "ok",
  "test_cases": [
    {"id": "TC-205-01", "title": "SAVE10 applied at exactly $50.00", "ac_ids": ["AC1"], "type": "boundary", "priority": "high",
     "preconditions": ["Cart subtotal is $50.00"], "steps": ["Enter coupon SAVE10", "Click Apply"], "expected_result": "Total is $45.00"},
    {"id": "TC-205-02", "title": "SAVE10 rejected at $49.99", "ac_ids": ["AC2"], "type": "boundary", "priority": "high",
     "preconditions": ["Cart subtotal is $49.99"], "steps": ["Enter coupon SAVE10", "Click Apply"], "expected_result": "Total stays $49.99 and message \"Spend $50.00 to use SAVE10\" is shown"},
    {"id": "TC-205-03", "title": "Unknown coupon code is rejected", "ac_ids": ["AC3"], "type": "negative", "priority": "medium",
     "preconditions": ["Cart subtotal is $80.00"], "steps": ["Enter coupon BOGUS", "Click Apply"], "expected_result": "Message \"Coupon code not recognised\" is shown and total stays $80.00"}
  ],
  "open_questions": ["AC4: should a second coupon replace the first or be rejected?"]
}
```

Read the two halves side by side and notice how much the pair shows that the schema did not:

- The agent **echoes** the story ID (`US-205`) and builds test case IDs from it (`TC-205-01`).
- A good answer **tests the boundary on both sides**: $50.00 (discount) and $49.99 (no discount).
- Messages from the acceptance criteria are **copied exactly**.
- When an AC is unclear (AC4 does not say what happens to a second coupon), the agent **asks** rather than guessing.

None of these is a new rule; the pair simply makes them **visible**.

> **Key idea.** A contract tells you the *shape* of a good answer. A sample pair *shows* you one.

---

### 2. The Four Jobs a Pair Does

The same pair file is useful in four different ways.

**Job 1: Specification by example (for humans).** Instead of describing behaviour only in abstract words, you agree on **concrete examples** of inputs and outcomes. You already did this with Given/When/Then scenarios. Pairs turn the agent's contract into examples that a product owner, a developer and a tester can all read and agree on. When people disagree about a rule ("Should the agent return test cases when it also has open questions?"), writing the pair forces the decision, because whoever writes the expected output has to choose.

**Job 2: Few-shot examples (for the model).** On **Tuesday** you learned **few-shot prompting**: putting worked examples inside the prompt so the model can imitate them. A pair is exactly a worked example: the input becomes a `user` turn and the expected output an `assistant` turn. Usually only one or two representative pairs go into the prompt (they cost prompt space and can bias the model, as you saw on Tuesday); the rest are kept for testing. You will see this in code in Section 11.

**Job 3: Regression (golden) data (for later).** A **golden example** is a pair whose expected output has been reviewed and approved. With golden pairs you can ask: "After I changed the instructions, does the agent still meet the expectations of every pair?" That is **regression testing** for an agent, like re-running pytest after a code change. Running and scoring is Friday's work; today we make sure the pairs exist and are trustworthy.

**Job 4: Contract test data (for the schema and rules).** If a pair's expected output fails the output schema, either the pair is wrong or the schema is stricter or looser than intended. Either way you found a defect **before** any model was called. This job needs both **valid samples** (must pass) and **deliberately invalid samples** (must fail), just as you test a login page with a correct **and** a wrong password.

---

### 3. Why Exact Match Usually Fails: Exact vs Property-Based Expectations

In a normal unit test you compare actual and expected results **exactly**:

```python
assert apply_coupon(50.00, "SAVE10") == 45.00
```

That works because `apply_coupon` is **deterministic**. An LLM agent is not: on Monday you saw that a model samples each next token, and on Tuesday that the same prompt can produce different wording. Consider two answers for US-205:

- **Answer A** (Section 1) has a test case titled `"SAVE10 applied at exactly $50.00"`.
- **Answer B** titles the same case `"Boundary: subtotal of $50.00 receives 10% discount"`, with steps `["Add items totalling $50.00 to the cart", "Type SAVE10 in the coupon box", "Press Apply"]`.

Both are **correct**: same boundary, traced to AC1, expecting $45.00. A character-by-character comparison would still "fail" Answer B. That is a **false failure**, and you know from Wednesday how false failures teach a team to ignore results.

So for an agent we describe the expected output in two layers:

1. **A reference answer** (`expected_output`): one example of a correct answer. Useful for humans and as a few-shot example, but the agent does **not** have to reproduce it word for word.
2. **Expectations**: the **properties** every acceptable answer must have. Checking properties rather than exact text is called a **property-based** expectation.

We write expectations in three groups:

- **MUST**: properties every acceptable answer has. Missing one means the answer is wrong.
- **MUST NOT**: things an acceptable answer never contains.
- **MAY**: freedoms the agent is allowed. Writing them down stops reviewers failing an answer for a harmless difference.

Here are the expectations for US-205, worked out **by hand** from the acceptance criteria (not from any AI output):

| Group | Expectation | Where it comes from |
|---|---|---|
| MUST | `status` is `"ok"` | All four ACs are understandable |
| MUST | A boundary case at subtotal **$50.00** where the discount is applied | AC1 "$50.00 or more"; BVA (Tuesday) |
| MUST | A boundary case at **$49.99** with no discount and the AC2 message | AC2 "under $50.00" |
| MUST | The AC3 message copied **exactly**: "Coupon code not recognised" | AC3 quotes the message |
| MUST NOT | Invent rules not in the story, e.g. a coupon **expiry date** | No AC mentions one (Wednesday: invented requirements) |
| MUST NOT | Return more than 6 test cases | `max_cases` is 6 (rule R5) |
| MAY | Word titles and steps differently | Wording is not part of the contract |
| MAY | Raise AC4 as an open question instead of testing it | AC4 is unclear in practice |

Notice that the **MUSTs are checkable** ("a case at $49.99" can be checked by a human now and a script later; "good test cases" could not), the **MUST NOTs target known AI mistakes** such as Wednesday's invented requirements, and the **MAYs protect good answers** like Answer B.

**When is exact match right?** For some fields, even in agent output: `contract_version` must be exactly `"1.0.0"`; `story_id` must equal the input's (rule R1); quoted AC messages must be exact; and in a deliberately small pair a **count** can be exact. Rule of thumb: **exact match for identifiers, codes, versions, counts and quoted text; properties for wording, ordering and anything a person could legitimately phrase another way.**

---

### 4. Anatomy of a Pair File

A pair needs more than an input and an output. It needs enough information that a teammate opening it in six months understands **why it exists**. Here is the pair file for US-205 (shortened with `"..."`; the complete file is created in Section 10):

~~~json
{
  "contract_version": "1.0.0",
  "pair_id": "P01",
  "category": "happy_path",
  "purpose": "Typical story with clear, numeric acceptance criteria.",
  "input": { "story_id": "US-205", "...": "the full input from Section 1" },
  "input_should_be_valid": true,
  "expected_output": { "story_id": "US-205", "...": "the full expected output from Section 1" },
  "expectations": {
    "must": [
      "status is ok",
      "a boundary case at subtotal $50.00 (discount applied)",
      "a boundary case at subtotal $49.99 (no discount, AC2 message)",
      "AC3 message text copied exactly"
    ],
    "must_not": [
      "invent rules not in the story (e.g. coupon expiry dates)",
      "more than 6 test cases"
    ],
    "may": [
      "word titles and steps differently",
      "raise AC4 as an open question instead of testing it"
    ]
  }
}
~~~

| Field | What it is | Why it matters |
|---|---|---|
| `contract_version` | Contract version the pair was written for | When the contract changes, you know which pairs to review (Section 9) |
| `pair_id` | Short, stable ID such as `P01` | Lets you refer to the pair in reviews, bug reports and coverage tables |
| `category` | happy_path, edge, clarification, invalid_input, out_of_scope | Says what kind of situation the pair represents (Section 5) |
| `purpose` | One sentence: why this pair exists | Stops people deleting a pair that looks "redundant" but guards a specific risk |
| `input` | Exactly what a caller would send | Must follow the **input** contract (unless deliberately invalid) |
| `input_should_be_valid` | `true` or `false` | Says whether the input is **meant** to pass, so a checker can tell a typo from a deliberate negative sample |
| `expected_output` | One reference answer, or `null` | `null` means "no agent output", e.g. for invalid input |
| `expectations` | MUST / MUST NOT / MAY lists | Decide whether an answer is acceptable |

Two design choices deserve a word. `input_should_be_valid` makes the **intention explicit**, like naming a pytest test `test_rejects_short_zip`: the reader knows the failure is the point. And `expected_output` is `null` for invalid input because the correct behaviour of the **system** is to reject the request at the validation gate (agent architecture lesson) **before** the model is called, so there is no agent output to expect.

---

### 5. Five Categories of Pairs

If every pair were an easy story like US-205, you would only learn how the agent behaves when everything is easy. Testers know the interesting behaviour lives at the edges, so we use five categories. (The complete reference outputs for every pair are in `make_pairs.py` in Section 10.)

#### 5.1 Happy path (P01, US-205)

A normal, well-written story with clear, testable acceptance criteria: what the agent sees most of the time. It shows the "standard" answer and is usually the best pair to use as a few-shot example. You have seen it in full in Sections 1, 3 and 4.

#### 5.2 Edge (P02, US-101 with one AC and `max_cases` 1)

A request that is legal but sits at the **limits** of the input contract: one acceptance criterion, and `max_cases` at its minimum.

```json
{
  "story_id": "US-101",
  "title": "Log in to my account",
  "acceptance_criteria": [
    {"id": "AC3", "text": "The account is locked for 15 minutes after 5 failed login attempts."}
  ],
  "max_cases": 1
}
```

**Expected:** `status` `"ok"` and **exactly one** test case tracing to AC3 (the reference answer, `TC-101-01`, tests that the 5th failed attempt locks the account).

- MUST: exactly 1 test case; it traces to AC3.
- MUST NOT: return 2 or more test cases (rule R5).
- MAY: choose the 5th-failure boundary **or** the 15-minute unlock boundary.

**Why:** models like to be "helpful" and add extra cases. BVA would normally test both the 4th and 5th attempts, but the caller asked for one; the MAY records that either boundary is a fair choice. Note also that the only AC is `AC3`: the agent must **not** renumber it to `AC1`, because `ac_ids` must refer to IDs in the input (rule R2).

#### 5.3 Clarification (P03, US-310 with a vague AC)

A story where at least one acceptance criterion **cannot be turned into a checkable expected result**:

```json
{
  "story_id": "US-310",
  "title": "Enter a shipping address",
  "acceptance_criteria": [
    {"id": "AC1", "text": "Name, street, city, ZIP and phone are required."},
    {"id": "AC2", "text": "ZIP must be exactly 5 digits."},
    {"id": "AC3", "text": "Phone must be exactly 10 digits."},
    {"id": "AC4", "text": "The address form must be fast and user-friendly."}
  ]
}
```

You met US-310 on Wednesday: AC4 contains **weak words** ("fast", "user-friendly") with no measurable target.

**Expected:** `status` `"needs_clarification"` with open questions naming AC4, for example *"AC4: what measurable target defines 'fast' (e.g. save in under 2 seconds)?"*. The agent may still include cases for the clear ACs (the reference answer has one: a 4-digit ZIP is rejected).

- MUST: `status` is `needs_clarification`; at least one open question names AC4.
- MUST NOT: invent a number for "fast" and test it **as if it were a requirement**.
- MAY: include test cases for AC1-AC3.

**Why:** it checks the agent's most important safety habit, **asking instead of guessing**, and exercises rule R6 (`needs_clarification` requires non-empty `open_questions`). Look closely at the MUST NOT: *suggesting* "under 2 seconds" inside a question is fine; a test case asserting it is not, because nobody agreed that number. Subtle differences like this are exactly what pairs should pin down.

> **Why is US-205 "ok" but US-310 "needs_clarification"?** Both have an open question. In US-205, AC4 is clear enough to state as a rule and the question is about a detail. In US-310, AC4 has **no** testable meaning at all. Writing these two pairs is how a team decides where that line is: Job 1 in action.

#### 5.4 Invalid input (P04)

A request that **breaks the input contract**:

```json
{"story_id": "205", "title": "Coupons", "acceptance_criteria": []}
```

`"205"` does not match `^US-[0-9]{3}$`, and `acceptance_criteria` is empty although the schema says `minItems: 1`.

**Expected:** rejected **before the model is called**; `input_should_be_valid` is `false` and `expected_output` is `null`.

- MUST: input is rejected by the input contract; the model is never called.
- MUST NOT: produce any test cases.

**Why:** it proves the validation gate works. Sending garbage to a model wastes time and money, and the model will often produce a confident answer anyway. This pair is pure contract test data (Job 4): its purpose is to fail.

#### 5.5 Out of scope (P05)

A request with a **valid shape** but the **wrong kind of content**: someone pasted release notes:

```json
{
  "story_id": "US-999",
  "title": "Release notes for version 4.2",
  "acceptance_criteria": [
    {"id": "AC1", "text": "Version 4.2 ships on Friday with a new checkout banner."}
  ]
}
```

This **passes** the input schema (pattern matches, texts are long enough): a schema checks **shape**, not **meaning**.

**Expected:** `status` `"needs_clarification"`, an **empty** `test_cases` list, and an open question explaining that this is not a user story.

- MUST: `status` is `needs_clarification`; `test_cases` is empty.
- MUST NOT: invent test cases for a "new checkout banner".
- MAY: suggest what information is missing.

**Why:** it tests the agent's **scope**, written in its instructions ("You only design test cases from user stories"), and shows that shape-valid input can still be nonsense that only the instructions (and a human reviewer) can catch.

| Category | Pair | Input valid? | Expected status | Main risk it guards |
|---|---|---|---|---|
| Happy path | P01 US-205 | yes | ok | Standard behaviour, format, boundaries |
| Edge | P02 US-101 (1 AC, max 1) | yes | ok | Limits ignored, AC renumbered |
| Clarification | P03 US-310 | yes | needs_clarification | Guessing instead of asking |
| Invalid input | P04 | **no** | (rejected, no output) | Garbage reaching the model |
| Out of scope | P05 US-999 | yes | needs_clarification | Inventing tests for non-stories |

---

### 6. Designing a Pair Set: The Coverage Matrix

How do you know you have enough pairs? Use the tool you already use for test cases: a **coverage matrix**. Rows are pairs; columns are what you want to cover. Today's contract gives natural columns, the six semantic rules and the possible outcomes:

- **R1** output `story_id` equals input `story_id`
- **R2** every `ac_ids` entry exists in the input acceptance criteria
- **R3** every input AC is covered by at least one test case (or appears in `open_questions`)
- **R4** test case IDs are unique and their middle part matches the story number (US-205 → TC-205-NN)
- **R5** number of test cases ≤ `max_cases` (default 10)
- **R6** `needs_clarification` requires non-empty `open_questions`; `ok` requires at least one test case (its two branches are the `ok` and `clarify` columns)
- Outcomes: status `ok`, status `needs_clarification`, input **rejected**

Fill it **by hand** first. A pair "exercises" a column when its expected output gives that rule or outcome something real to check. R1 needs an output (all pairs except P04). R2-R4 need at least one test case (P01, P02, P03). R5 is only really stressed when the count sits **exactly on** the limit: P02 (1 of 1) does, P01 (3 of 6) does not. That is BVA applied to a contract rule.

| Pair | R1 | R2 | R3 | R4 | R5 at max | ok | clarify | rejected |
|---|---|---|---|---|---|---|---|---|
| P01 happy_path | x | x | x | x | . | x | . | . |
| P02 edge | x | x | x | x | x | x | . | . |
| P03 clarification | x | x | x | x | . | . | x | . |
| P04 invalid_input | . | . | . | . | . | . | . | x |
| P05 out_of_scope | x | . | . | . | . | . | x | . |
| **pairs per column** | 4 | 3 | 3 | 3 | **1** | 2 | 2 | **1** |

- **Gaps** (columns with 0 pairs): none.
- **Thin columns** (only 1 pair): `R5 at max` and `rejected`. If P02 or P04 became wrong or were deleted, those areas would have no protection. Sensible additions: a story with 12 ACs and the default `max_cases` of 10 (the agent must choose, and raise the rest as questions), and a second invalid input (for example an unknown extra field, which `additionalProperties: false` must reject).

The matrix turns "I think we have enough pairs" into "we can **see** what is covered". You can add columns for techniques requested, story types, or known AI weaknesses from Wednesday (invented rules, wrong boundaries, paraphrased messages), but only when each column names a real risk. In Section 10, Python prints this matrix for you.

---

### 7. How Many Pairs?

There is no magic number. For a first agent like TestCaseDesigner:

- **Start with 5-10 pairs**: at least one per category, and no empty column in the matrix. Our 5 are a minimum.
- **Quality beats quantity.** Every pair must be reviewed by a person; a wrong golden answer actively teaches the wrong thing.
- **Grow the set from real mistakes.** Each new kind of agent error earns a pair that would have caught it, just as every bug fix earns a regression test.
- **Keep some pairs out of the prompt.** A pair used as a few-shot example has shown the agent the answer; judge the agent on pairs it has not seen.

Larger teams maintain dozens or hundreds of pairs, often called an **evaluation set**. Running and scoring one is Friday's topic; grading with another model is Week 10's.

---

### 8. Keeping Pairs Honest

A pair is only useful if its expected output is **actually correct**. A wrong golden answer makes a correct agent look broken and a broken agent look correct.

1. **Humans write expectations from the requirement, before seeing AI output.** On Wednesday you learned about **anchoring**: once you read an AI draft, your judgement drifts towards it. If you generate a "golden" answer with AI and lightly edit it, the pair inherits the AI's blind spots, and later checks reward the agent for repeating its own mistakes. That is a circular test: the answer key written by the student. AI may **suggest** ideas for new pairs; it must not **decide** the expected result.
2. **Review every pair** with Wednesday's checklist (correct, complete, grounded, relevant, consistent, executable, traceable, safe, non-duplicated), watching especially **boundaries** ($49.99, not $49.00), **exact text** ("recognised", as the AC spells it) and **traceability**. Pairs are small, so a second reviewer is cheap.
3. **Check pairs against the schema automatically.** Humans are good at meaning and bad at noticing that `TC-205-1` is missing a digit; code is the opposite (Section 10).
4. **Record why each pair exists** in `purpose`, so nobody deletes it as "boring".
5. **Never "fix" a pair to match the agent.** Change a pair only when the **requirement** shows it was wrong, and record the change and evidence, as in Wednesday's correction log.

---

### 9. Storing Pairs: Folder Layout and Versioning

Pairs are files, so they live in the repository next to the agent's instructions, templates and schemas. Two layouts are common:

- **Layout A, one folder per pair:** `samples/P01-happy_path/input.json`, `expected.json` and `notes.md` (purpose, category, MUST / MUST NOT / MAY). Good when files are long or non-technical reviewers read them; `input.json` and `expected.json` are pure contract documents that validate directly against the schemas.
- **Layout B, one JSON file per pair** (used in Section 10): everything about a pair in one place, easy to process with code.

```
agents/test-case-designer/
├── instructions.md
├── templates/
├── schemas/
│   ├── tcd_input.schema.json
│   └── tcd_output.schema.json
└── samples/
    ├── P01-happy_path.json
    ├── P02-edge.json
    ├── P03-clarification.json
    ├── P04-invalid_input.json
    └── P05-out_of_scope.json
```

Pick one layout per agent and use it consistently.

**Versioning with the contract.** In the input/output contracts lesson you learned semantic versioning (`1.0.0`). Every pair records `contract_version`. A **minor** change (for example an optional `notes` field in 1.1.0) usually leaves old pairs valid. A **major** change (for example renaming `ac_ids` to `traces_to` in 2.0.0) breaks them all, so schema, instructions, templates and pairs are updated together in one commit or pull request. Keeping pairs in Git (as you keep prompts, per Tuesday) gives every change to an expected answer an author, a date and a reason.

---

### 10. In Code: Do the Pairs Obey the Contract?

Now we turn Sections 4-6 into code. We will create the five pair files (Layout B), check each pair against the schemas **as intended**, and print the coverage matrix. **No model is called**: we are testing the **pairs themselves** (Job 4).

**Setup.** You need Python 3.9+ and `jsonschema` 4.18 or newer:

```bash
pip install "jsonschema>=4.18"
```

> Some machines still have `jsonschema` 3.2, which lacks `Draft202012Validator`. Check with `python -c "import importlib.metadata as m; print(m.version('jsonschema'))"` and upgrade if needed.

In a working folder, create `schemas/` and save the two TestCaseDesigner schema files from the JSON Schema lesson there, unchanged, as `schemas/tcd_input.schema.json` and `schemas/tcd_output.schema.json`.

#### Step 1: Create the pair files

`make_pairs.py` stores the five pairs as Python dictionaries and writes each to `samples/` as indented JSON. In a real project you would write the JSON by hand; generating it here keeps the lesson self-contained. Note that Python's `None` becomes JSON `null`, and `{"contract_version": "1.0.0", **pair}` builds a new dictionary that starts with the version and then copies every key of `pair` (`**` unpacks a dictionary).

```python
# make_pairs.py
# Writes five sample input/output pairs for TestCaseDesigner v1.0.0 into samples/.
import json
from pathlib import Path

SAMPLES = Path("samples")
SAMPLES.mkdir(exist_ok=True)

US205_INPUT = {
    "story_id": "US-205",
    "title": "Apply coupon at checkout",
    "acceptance_criteria": [
        {"id": "AC1", "text": "SAVE10 gives 10% off a subtotal of $50.00 or more."},
        {"id": "AC2", "text": "Subtotals under $50.00 are unchanged and show \"Spend $50.00 to use SAVE10\"."},
        {"id": "AC3", "text": "Unknown codes show \"Coupon code not recognised\"."},
        {"id": "AC4", "text": "Only one coupon per order."},
    ],
    "techniques": ["EP", "BVA"],
    "max_cases": 6,
}

US205_EXPECTED = {
    "contract_version": "1.0.0",
    "story_id": "US-205",
    "status": "ok",
    "test_cases": [
        {"id": "TC-205-01", "title": "SAVE10 applied at exactly $50.00", "ac_ids": ["AC1"],
         "type": "boundary", "priority": "high", "preconditions": ["Cart subtotal is $50.00"],
         "steps": ["Enter coupon SAVE10", "Click Apply"], "expected_result": "Total is $45.00"},
        {"id": "TC-205-02", "title": "SAVE10 rejected at $49.99", "ac_ids": ["AC2"],
         "type": "boundary", "priority": "high", "preconditions": ["Cart subtotal is $49.99"],
         "steps": ["Enter coupon SAVE10", "Click Apply"],
         "expected_result": "Total stays $49.99 and message \"Spend $50.00 to use SAVE10\" is shown"},
        {"id": "TC-205-03", "title": "Unknown coupon code is rejected", "ac_ids": ["AC3"],
         "type": "negative", "priority": "medium", "preconditions": ["Cart subtotal is $80.00"],
         "steps": ["Enter coupon BOGUS", "Click Apply"],
         "expected_result": "Message \"Coupon code not recognised\" is shown and total stays $80.00"},
    ],
    "open_questions": ["AC4: should a second coupon replace the first or be rejected?"],
}

pairs = [
    {
        "pair_id": "P01",
        "category": "happy_path",
        "purpose": "Typical story with clear, numeric acceptance criteria.",
        "input": US205_INPUT,
        "input_should_be_valid": True,
        "expected_output": US205_EXPECTED,
        "expectations": {
            "must": ["status is ok",
                     "a boundary case at subtotal $50.00 (discount applied)",
                     "a boundary case at subtotal $49.99 (no discount, AC2 message)",
                     "AC3 message text copied exactly"],
            "must_not": ["invent rules not in the story (e.g. coupon expiry dates)",
                         "more than 6 test cases"],
            "may": ["word titles and steps differently",
                    "raise AC4 as an open question instead of testing it"],
        },
    },
    {
        "pair_id": "P02",
        "category": "edge",
        "purpose": "Smallest legal request: one AC and max_cases 1.",
        "input": {
            "story_id": "US-101",
            "title": "Log in to my account",
            "acceptance_criteria": [
                {"id": "AC3", "text": "The account is locked for 15 minutes after 5 failed login attempts."}],
            "max_cases": 1,
        },
        "input_should_be_valid": True,
        "expected_output": {
            "contract_version": "1.0.0", "story_id": "US-101", "status": "ok",
            "test_cases": [
                {"id": "TC-101-01", "title": "Account locks on the 5th failed login", "ac_ids": ["AC3"],
                 "type": "boundary", "priority": "high", "preconditions": ["Account is active"],
                 "steps": ["Enter a wrong password 5 times", "Enter the correct password"],
                 "expected_result": "Login is refused and the account is locked for 15 minutes"}],
            "open_questions": [],
        },
        "expectations": {
            "must": ["exactly 1 test case", "the test case traces to AC3"],
            "must_not": ["return 2 or more test cases"],
            "may": ["choose the 5th-failure boundary or the 15-minute unlock boundary"],
        },
    },
    {
        "pair_id": "P03",
        "category": "clarification",
        "purpose": "Story with an untestable AC (vague wording).",
        "input": {
            "story_id": "US-310",
            "title": "Enter a shipping address",
            "acceptance_criteria": [
                {"id": "AC1", "text": "Name, street, city, ZIP and phone are required."},
                {"id": "AC2", "text": "ZIP must be exactly 5 digits."},
                {"id": "AC3", "text": "Phone must be exactly 10 digits."},
                {"id": "AC4", "text": "The address form must be fast and user-friendly."}],
        },
        "input_should_be_valid": True,
        "expected_output": {
            "contract_version": "1.0.0", "story_id": "US-310", "status": "needs_clarification",
            "test_cases": [
                {"id": "TC-310-01", "title": "ZIP with 4 digits is rejected", "ac_ids": ["AC2"],
                 "type": "boundary", "priority": "medium",
                 "steps": ["Fill all fields with valid data", "Enter ZIP 1234", "Click Save"],
                 "expected_result": "Address is not saved and the ZIP field shows an error"}],
            "open_questions": ["AC4: what measurable target defines 'fast' (e.g. save in under 2 seconds)?",
                               "AC4: what does 'user-friendly' mean in checkable terms?"],
        },
        "expectations": {
            "must": ["status is needs_clarification",
                     "at least one open question that names AC4"],
            "must_not": ["invent a number for 'fast' and test it as if it were a requirement"],
            "may": ["include test cases for the clear ACs (AC1-AC3)"],
        },
    },
    {
        "pair_id": "P04",
        "category": "invalid_input",
        "purpose": "Malformed request must be rejected BEFORE it reaches the model.",
        "input": {"story_id": "205", "title": "Coupons", "acceptance_criteria": []},
        "input_should_be_valid": False,
        "expected_output": None,
        "expectations": {
            "must": ["input is rejected by the input contract", "the model is never called"],
            "must_not": ["produce any test cases"],
            "may": [],
        },
    },
    {
        "pair_id": "P05",
        "category": "out_of_scope",
        "purpose": "Valid shape, but the content is release notes, not a user story.",
        "input": {
            "story_id": "US-999",
            "title": "Release notes for version 4.2",
            "acceptance_criteria": [
                {"id": "AC1", "text": "Version 4.2 ships on Friday with a new checkout banner."}],
        },
        "input_should_be_valid": True,
        "expected_output": {
            "contract_version": "1.0.0", "story_id": "US-999", "status": "needs_clarification",
            "test_cases": [],
            "open_questions": ["The input looks like release notes, not a user story. Which behaviour should be tested?"],
        },
        "expectations": {
            "must": ["status is needs_clarification", "test_cases is empty"],
            "must_not": ["invent test cases for a 'new checkout banner'"],
            "may": ["suggest what information is missing"],
        },
    },
]

for pair in pairs:
    path = SAMPLES / f"{pair['pair_id']}-{pair['category']}.json"
    path.write_text(json.dumps({"contract_version": "1.0.0", **pair}, indent=2))
    print("wrote", path)
```

```
$ python make_pairs.py
wrote samples/P01-happy_path.json
wrote samples/P02-edge.json
wrote samples/P03-clarification.json
wrote samples/P04-invalid_input.json
wrote samples/P05-out_of_scope.json
```

#### Step 2: Check the pairs and print the coverage matrix

```python
# check_pairs.py
# 1) Every sample pair must itself obey the TestCaseDesigner contract.
# 2) Print a coverage matrix: which situations do our pairs exercise?
import json
from pathlib import Path
from jsonschema import Draft202012Validator

input_v = Draft202012Validator(json.loads(Path("schemas/tcd_input.schema.json").read_text()))
output_v = Draft202012Validator(json.loads(Path("schemas/tcd_output.schema.json").read_text()))

pairs = [json.loads(p.read_text()) for p in sorted(Path("samples").glob("*.json"))]

print("== Step 1: do the pairs obey the contract? ==")
problems = 0
for pair in pairs:
    in_errors = list(input_v.iter_errors(pair["input"]))
    input_ok = (len(in_errors) == 0)
    if input_ok != pair["input_should_be_valid"]:
        problems += 1
        print(f"{pair['pair_id']}: PROBLEM - input valid={input_ok}, "
              f"but pair says {pair['input_should_be_valid']}")
    elif not input_ok:
        reasons = "; ".join(e.message for e in in_errors)
        print(f"{pair['pair_id']}: input rejected as intended ({reasons})")
    else:
        print(f"{pair['pair_id']}: input valid")

    expected = pair["expected_output"]
    if expected is not None:
        out_errors = list(output_v.iter_errors(expected))
        for e in out_errors:
            problems += 1
            print(f"{pair['pair_id']}: PROBLEM in expected output at "
                  f"{list(e.absolute_path)}: {e.message}")
        if not out_errors:
            print(f"{pair['pair_id']}: expected output valid")
print("problems found:", problems)

print()
print("== Step 2: coverage matrix ==")
COLUMNS = ["R1", "R2", "R3", "R4", "R5@max", "ok", "clarify", "rejected"]

def covers(pair):
    """Return the set of columns this pair exercises."""
    hits = set()
    expected = pair["expected_output"]
    if expected is None:
        return {"rejected"}
    hits.add("R1")                                   # story_id must be echoed
    cases = expected["test_cases"]
    if cases:
        hits.update({"R2", "R3", "R4"})              # tracing, AC coverage, ids
    if len(cases) == pair["input"].get("max_cases", 10):
        hits.add("R5@max")                           # sits exactly on the limit
    hits.add("ok" if expected["status"] == "ok" else "clarify")
    return hits

print(f"{'pair':<22}" + "".join(f"{c:>9}" for c in COLUMNS))
totals = {c: 0 for c in COLUMNS}
for pair in pairs:
    hits = covers(pair)
    label = f"{pair['pair_id']} {pair['category']}"
    print(f"{label:<22}" + "".join(f"{('x' if c in hits else '.'):>9}" for c in COLUMNS))
    for c in hits:
        totals[c] += 1
print(f"{'pairs per column':<22}" + "".join(f"{totals[c]:>9}" for c in COLUMNS))

gaps = [c for c in COLUMNS if totals[c] == 0]
thin = [c for c in COLUMNS if totals[c] == 1]
print("gaps (no pair):", gaps or "none")
print("thin (only one pair):", thin or "none")
```

How it works:

- **`Draft202012Validator(schema)`** builds a reusable validator for a Draft 2020-12 schema; we make one for inputs and one for outputs.
- **`sorted(Path("samples").glob("*.json"))`** finds every pair file in name order.
- **`iter_errors(instance)`** returns **every** error, not just the first (as `validate()` would). You met it in the JSON Schema lesson.
- **The intention check** `input_ok != pair["input_should_be_valid"]` is the heart of Step 1: reality and intention disagree, so either a valid pair was broken by a typo or a "deliberately invalid" pair accidentally became valid. When an input fails **as intended** (P04), we print the reasons so a reader can confirm it failed for the **right** reasons.
- **`e.absolute_path`** says where the error is (for example `['test_cases', 0, 'id']`), and **`e.message`** explains it.
- **`covers(pair)`** is Section 6's hand reasoning as code. `pair["input"].get("max_cases", 10)` applies the contract's default when the field is missing.
- **`:<22`** and **`:>9`** in the f-strings pad text to fixed widths so the columns line up.

Output (real run):

```
== Step 1: do the pairs obey the contract? ==
P01: input valid
P01: expected output valid
P02: input valid
P02: expected output valid
P03: input valid
P03: expected output valid
P04: input rejected as intended ('205' does not match '^US-[0-9]{3}$'; [] should be non-empty)
P05: input valid
P05: expected output valid
problems found: 0

== Step 2: coverage matrix ==
pair                         R1       R2       R3       R4   R5@max       ok  clarify rejected
P01 happy_path                x        x        x        x        .        x        .        .
P02 edge                      x        x        x        x        x        x        .        .
P03 clarification             x        x        x        x        .        .        x        .
P04 invalid_input             .        .        .        .        .        .        .        x
P05 out_of_scope              x        .        .        .        .        .        x        .
pairs per column              4        3        3        3        1        2        2        1
gaps (no pair): none
thin (only one pair): ['R5@max', 'rejected']
```

The matrix matches the one we built by hand, and P04 failed for exactly the two reasons predicted in Section 5.4: a good negative sample.

> **What this does not check.** Only **shape** (schema) and coverage. It does not check rules R1-R6 or the MUST / MUST NOT / MAY expectations; today a human reviewer does that with the Wednesday checklist. Turning rules and expectations into automated checks and running them against real agent output is **Friday's** work (building validation scripts).

#### What happens when a pair breaks the contract?

Simulate a teammate's mistake: copy P01, introduce two typical errors, and save it as P06.

```python
# broken_pair_demo.py - what happens when a pair breaks the contract?
import json
from pathlib import Path

pair = json.loads(Path("samples/P01-happy_path.json").read_text())
pair["pair_id"] = "P06"
case = pair["expected_output"]["test_cases"][0]
case["id"] = "TC-205-1"        # typo: only one digit at the end
case["priority"] = "urgent"    # not one of high / medium / low
Path("samples/P06-broken.json").write_text(json.dumps(pair, indent=2))
print("wrote samples/P06-broken.json")
```

Rerun `check_pairs.py`. The end of Step 1 now reads (real output):

```
P05: expected output valid
P06: input valid
P06: PROBLEM in expected output at ['test_cases', 0, 'id']: 'TC-205-1' does not match '^TC-[0-9]{3}-[0-9]{2}$'
P06: PROBLEM in expected output at ['test_cases', 0, 'priority']: 'urgent' is not one of ['high', 'medium', 'low']
problems found: 2
```

A human could easily read past `TC-205-1`; the schema cannot. (Delete `samples/P06-broken.json` afterwards.) Pairs and schemas protect each other: the schema catches mistakes in pairs, and a reasonable pair that gets rejected reveals a schema that is too strict.

---

### 11. Reusing a Pair as a Few-Shot Example

Job 2 says a pair can go inside the prompt. Here it is with Tuesday's role/content message list, using P01 as the worked example and P02's input as the real request:

```python
# pairs_as_few_shot.py - reuse a sample pair as a few-shot example (Tuesday)
import json
from pathlib import Path

example = json.loads(Path("samples/P01-happy_path.json").read_text())
new_story = json.loads(Path("samples/P02-edge.json").read_text())["input"]

messages = [
    {"role": "system", "content": "You are TestCaseDesigner. Reply with JSON only."},
    # the worked example: one user turn + the answer we want to imitate
    {"role": "user", "content": json.dumps(example["input"])},
    {"role": "assistant", "content": json.dumps(example["expected_output"])},
    # the real request
    {"role": "user", "content": json.dumps(new_story)},
]

for m in messages:
    print(f"{m['role']:<10} {len(m['content']):>5} chars  {m['content'][:45]}...")
```

Output (real run):

```
system        47 chars  You are TestCaseDesigner. Reply with JSON onl...
user         440 chars  {"story_id": "US-205", "title": "Apply coupon...
assistant   1045 chars  {"contract_version": "1.0.0", "story_id": "US...
user         190 chars  {"story_id": "US-101", "title": "Log in to my...
```

Three things to notice:

- The one-line system message is a placeholder; in a real agent it comes from the full **agent instructions**.
- The worked example's output (1,045 characters) is over five times the size of the real request. Few-shot examples are expensive, which is one reason to use only one or two.
- P01 is now **inside** the prompt, so it is no longer a fair test; judge the agent on the other pairs.

Turning this into a reusable template inside a working agent is covered on **Friday**.

---

### 12. Putting Thursday Together

Pairs are the last part of today's anatomy, and they connect all the others:

| Anatomy part | For TestCaseDesigner | How the pairs relate |
|---|---|---|
| Agent architecture | Model, instructions, templates, contract, validation gate | P04 tests the gate; the others test the model's behaviour |
| Agent instructions | Role, scope, process, rules, output rules | P03 tests "ask, don't guess"; P05 tests scope |
| Prompt templates | Fixed text + placeholders | Pairs supply real values and few-shot examples |
| Input/output contract | What goes in and out, version 1.0.0 | Every pair records and obeys `contract_version` |
| JSON Schema | Machine-readable contract | `check_pairs.py` validates every pair |
| Required fields and rules | Required fields plus R1-R6 | The coverage matrix shows which rules pairs exercise |
| **Sample I/O pairs** | P01-P05 | Concrete, reviewed examples of all of the above |

On **Friday** you will **build** an agent: full instructions, reusable templates, an implemented contract, runs against requirements, validation scripts and refinement, using pairs like these.

**Connecting to Project 2.** In today's pair-programming exercise you design a **requirements agent** for the e-commerce app. Use this lesson as a checklist: at least one pair per category; MUST / MUST NOT / MAY written **from the requirement** before any AI output; every pair validating against your schema (or failing on purpose with `input_should_be_valid: false`); a coverage matrix with no gaps; and every pair stored with `contract_version` in one consistent layout.

---

## Practice Exercises

1. **Write expectations by hand.** For US-101 AC2 ("A wrong email or password shows \"Invalid email or password\""), write a pair input with only that AC and `max_cases` 3, then at least two MUST, one MUST NOT and one MAY expectation, without looking at any AI output.
2. **Fill a thin column.** Add a pair `P06-edge`: a story with **12** acceptance criteria and **no** `max_cases` (default 10). Decide the expected output (which ACs get cases, which go to `open_questions`, which status), add it to `make_pairs.py`, and confirm with `check_pairs.py` that `R5@max` is no longer thin. (Hint: the reference answer needs exactly 10 test cases.)
3. **A second negative sample.** Add `P07-invalid_input` with a valid story but an unknown extra top-level field `"priority": "high"`. Predict the error message, then run `check_pairs.py` and compare. Which schema keyword causes the rejection?
4. **Catch a lying pair.** Change P04's `input_should_be_valid` to `true` and rerun `check_pairs.py`. What does it print, and why is this useful rather than noise?

---

## Knowledge Check

1. What three things does a complete sample pair contain, and which one do we usually **not** require the agent to reproduce word for word?

<details><summary>Answer</summary>

An input, a reference expected output, and expectations (MUST / MUST NOT / MAY). The reference output is usually not compared exactly, because an LLM can phrase a correct answer differently; the expectations decide acceptability.
</details>

2. Name the four jobs a sample pair can do.

<details><summary>Answer</summary>

Specification by example (humans), few-shot example (model), regression / golden data (later checks), and contract test data (schema and rules, with valid and deliberately invalid samples).
</details>

3. Why is P05 (release notes) not caught by the input schema, and what catches it?

<details><summary>Answer</summary>

Its **shape** is valid; a schema checks shape, not meaning. The agent's instructions (scope) should make it return `needs_clarification` with no test cases, and a human reviewer confirms it.
</details>

4. Why does P04 have `expected_output: null`?

<details><summary>Answer</summary>

Its input breaks the input contract, so it must be rejected before the model is called. There is no agent output to expect.
</details>

5. In a coverage matrix, what is the difference between a **gap** and a **thin** column?

<details><summary>Answer</summary>

A gap has no pair exercising it: add one. A thin column has only one pair: it works, but one mistake or deletion leaves it unprotected, so add a second when you can.
</details>

6. A teammate generates a "golden" output with AI and edits two words. Why is this risky?

<details><summary>Answer</summary>

Anchoring: the pair inherits the AI's mistakes, so later checks reward the agent for repeating them (a circular test). Expected results should be written by humans from the requirement, then reviewed.
</details>

7. The contract moves from 1.0.0 to 2.0.0 because `ac_ids` is renamed. What happens to the pairs?

<details><summary>Answer</summary>

It is a breaking (major) change, so every expected output becomes invalid. All pairs are reviewed and migrated, with `contract_version` updated, in the same change as the schema, instructions and templates.
</details>

---

## Glossary

- **Sample input/output pair:** An input, a reference expected output, and the expectations that define an acceptable answer.
- **Golden example:** A reviewed, approved pair used as a reference for later checks.
- **Specification by example:** Clarifying requirements by agreeing on concrete examples of inputs and outcomes.
- **Property-based expectation:** A check on a property of the answer (e.g. "contains a case at $49.99") rather than its exact text.
- **MUST / MUST NOT / MAY:** Required properties, forbidden properties, and allowed freedoms of an acceptable answer.
- **Negative sample:** A deliberately invalid input or output that the contract must reject.
- **Coverage matrix:** A table of pairs against rules and outcomes, used to find gaps (no pair) and thin columns (one pair).
- **Evaluation set:** A larger, maintained collection of pairs used to measure an agent over time.

---

## Summary

- A **sample input/output pair** is a worked example and answer key for an agent: an input, a reference output and the expectations for an acceptable answer.
- Pairs do **four jobs**: specification by example, few-shot examples, regression (golden) data and contract test data.
- LLM output varies, so **exact match** is reserved for IDs, versions, counts and quoted text; everything else uses **MUST / MUST NOT / MAY** properties.
- A pair file records `contract_version`, `pair_id`, `category`, `purpose`, `input`, `input_should_be_valid`, `expected_output` (or `null`) and `expectations`.
- Cover five **categories**: happy path, edge, clarification, invalid input (rejected before the model) and out of scope (shape-valid nonsense).
- A **coverage matrix** against R1-R6 and the statuses reveals gaps and thin columns.
- Keep pairs **honest**: human-written from the requirement, reviewed, schema-checked, explained, never edited to match the agent, and **versioned with the contract**.
- Running the agent against pairs and building validation scripts follow on **Friday**; LLM-as-judge follows in **Week 10**.

---

## Additional Resources

- Anthropic, *Define success criteria and build evaluations* (designing test cases for LLM tasks, including edge cases such as irrelevant or ambiguous input): https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- Martin Fowler, *Specification By Example* (short classic essay on using concrete examples as specifications, and their limits): https://martinfowler.com/bliki/SpecificationByExample.html
- python-jsonschema documentation, *Handling Validation Errors* (what `iter_errors`, `message` and `absolute_path` give you): https://python-jsonschema.readthedocs.io/en/stable/errors/
