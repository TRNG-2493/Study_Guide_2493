# Week 08 · Lecture 08: Agreeing on Inputs and Outputs

**Topics:**

1. [Input/Output Contracts](#topic-1)
2. [JSON Schema](#topic-2)
3. [Required Fields and Validation Rules](#topic-3)
4. [Sample Input/Output Pairs](#topic-4)

---

## Before Class

> **Setup checklist (do this before the lecture starts)**
>
> 1. Open your `week08/agent` folder from Lecture 07. It should contain `README.txt`, `instructions_draft.md` and `input_template.txt`.
> 2. Inside `agent`, create an empty folder called **`stories`**.
> 3. Open your AI assistant: **ChatGPT, Copilot Chat or Claude**.
> 4. Nothing to install. There's **no code** today: you'll write the agent's **contract**, its **rules** and its **examples**, and test them in your AI tool. Next lecture, code will use everything you write today.

---

## How to Use This Handout

Same labels as Lecture 07. **Every step tells you where to do it:**

| Label | Where | What you do |
|---|---|---|
| 🤖 **AI tool** | ChatGPT, Copilot Chat or Claude | Open a **new chat**, paste exactly what the step shows, and read the reply |
| 📝 **Editor** | VS Code (or any editor) | Create or edit a file in your `agent` folder |
| ✍️ **Paper** | Pen and paper, or a text file | Work something out yourself |

In Lecture 07 the agent's output format was a few lines in the instructions. Today you write down **exactly** what goes into the agent and what must come out (the **contract**), the **rules** for checking an answer, and **examples** of good answers.

> **About AI answers:** answers vary between tools and runs. Mark them with the checklist; use the **sample AI answer** if your tool isn't working.

---

## Learning Objectives

By the end of this lecture you will be able to:

- Write an agent's **input/output contract** in plain English, including how the agent says **"I can't"**.
- **Read** a simple **JSON Schema** and explain how it describes valid JSON.
- Explain **required fields**, **missing vs. empty**, and **rules** that compare the answer with the story, and use them to check answers by hand.
- Write **sample input/output pairs** and use them as examples that make the agent more reliable.

---

<a id="topic-1"></a>

# Topic 1: Input/Output Contracts

## Definition

An **input/output contract** is a written agreement about **what an agent receives** (the input) and **what it must return** (the output): which fields, what kind of values, what is required, and what is allowed. Everyone who builds or uses the agent relies on it: you when writing the instructions, the checker script in Lecture 09, and the tester who reviews the results. AI answers vary from run to run, so a clear contract is the **definition of "a valid answer"** that every check is built from. Our contract also includes an honest way for the agent to say **"I can't test this story"**.

## Key Ideas

1. **Two sides of the contract:**

   | Side | Describes | Our version |
   |---|---|---|
   | **Input** | What a story looks like when it goes in | A JSON file in `stories/` |
   | **Output** | What every reply must look like | One JSON object with four fields |

2. **A contract states, for every field:** its name, what kind of value it holds (text, number, list), whether it's **required**, and any **rule** for valid values.
3. **The agent must be able to say "I can't".** `status: "needs_clarification"` plus questions in `open_questions` lets the agent refuse honestly instead of inventing tests for a vague story.
4. **The story becomes a data file.** Code can't read "US-205 Apply coupon…" from a handout, but it can read a **JSON file** that follows the input contract.

## Worked Example: Write `contract.md` and the Story Files

### Step 1 (📝 Editor): The input side

Create `contract.md` in your `agent` folder:

```text
# TestCaseDesigner contract - v1

## Input: one story (one JSON file in stories/)
| Field               | Kind   | Required? | Rule                                      |
|---------------------|--------|-----------|-------------------------------------------|
| story_id            | text   | yes       | "US-" + 3 digits, e.g. US-205             |
| title               | text   | yes       | A short name for the story                |
| acceptance_criteria | list   | yes       | At least 1; each has an id (AC1...) and text |
| max_cases           | number | yes       | The most test cases the agent may return  |
```

**Why:** each row answers "what is it called?", "what kind of value?", "must it be there?" and "what does valid look like?".

### Step 2 (📝 Editor): The output side

Add:

```text
## Output: one JSON object, and nothing else
| Field          | Kind | Required? | Rule                                          |
|----------------|------|-----------|-----------------------------------------------|
| story_id       | text | yes       | The same as the input story_id                |
| status         | text | yes       | "ok" or "needs_clarification"                 |
| test_cases     | list | yes       | May be empty                                  |
| open_questions | list | yes       | May be empty; each starts with an AC id       |

Each test case has: id (e.g. TC-205-01), title, ac_ids (a list, e.g. ["AC1"]),
type (positive, negative or boundary), steps (a list), expected_result.
```

**Why:** notice "**may be empty**". When the agent can't produce tests, `test_cases` is `[]`, which is very different from the field being **missing**. Topic 3 explains why.

### Step 3 (📝 Editor): How the agent says "I can't"

Add:

```text
## Saying "I can't"
If no criterion can be tested: status = "needs_clarification", test_cases = [],
and one open question per problem, starting with the AC id (e.g. "AC1: ...").
```

### Step 4 (📝 Editor): Write the stories as data files

Create three files in the `stories` folder. Type them exactly as shown; the next lecture's code will read them.

**`stories/US-205.json`**

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
  "max_cases": 5
}
```

**`stories/US-311.json`**

```json
{
  "story_id": "US-311",
  "title": "Fast search",
  "acceptance_criteria": [
    {"id": "AC1", "text": "Search results should appear fast."}
  ],
  "max_cases": 3
}
```

**`stories/US-312.json`**

```json
{
  "story_id": "US-312",
  "title": "Free gift wrap",
  "acceptance_criteria": [
    {"id": "AC1", "text": "Orders of 10 or more items get free gift wrap."},
    {"id": "AC2", "text": "Orders under 10 items show \"Add 10 items for free gift wrap\"."}
  ],
  "max_cases": 3
}
```

**Why these three?** Each one tests the agent differently: **US-205** has a boundary and an incomplete AC (AC4), **US-311** is too vague to test, and **US-312** has a boundary with whole numbers (10 vs. 9). Inside a JSON string, a double quote is written as `\"`.

### Consolidated Result

`contract.md` (Steps 1–3) and the three story files. You'll add a **Rules** section to `contract.md` in Topic 3.

## Checkpoint

Answer from your contract alone:

| Question | Answer |
|---|---|
| Can `test_cases` be an empty list? | **Yes**, for example when status is `needs_clarification` |
| Can `open_questions` be left out of a reply? | **No**: it's required (but may be empty) |
| A reply says `"status": "done"`. Valid? | **No**: only `"ok"` or `"needs_clarification"` |
| How does the agent say "this story is too vague"? | `status: "needs_clarification"`, empty `test_cases`, a question starting `AC1:` |

**Check your story files:** each one opens with `{` and closes with `}`, every field name is in **double quotes**, and there's **no comma after the last item** in a list or object.

## Your Turn

1. **(In class, 3 min)** A reply contains 7 test cases for US-205. Which line of the contract does that break? (Hint: look at the input side.)
2. **(After class)** Write `stories/US-313.json` for: *US-313 Track an order. AC1: Guests can track an order by entering its order number. AC2: An unknown order number shows "Order not found".* Use `"max_cases": 3`.
3. **(After class)** 🤖 Paste your `contract.md` into your AI tool and ask: *"Write one valid example reply for story US-312 that follows this contract."* Check its reply against every row of your output table.

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| Story file breaks later with "Expecting ',' delimiter" | A missing comma between fields, or an extra one at the end | Compare with the handout character by character |
| Quotes inside the AC text break the file | A plain `"` inside a JSON string ends the string | Write it as `\"`, as in US-205's AC2 |

---

<a id="topic-2"></a>

# Topic 2: JSON Schema

## Definition

**JSON Schema** is a standard way to describe **what valid JSON looks like**, written in JSON itself. A schema lists which fields are **required**, what **type** each value is, which values are **allowed** (`enum`), and what text must look like (`pattern`). Tools called **validators** can then check any JSON reply against the schema automatically. In other words, a schema is your contract's output table written so that a **computer** can read it. This week you only need to **read** a schema; in Lecture 09 you'll write a short checker that does the most important checks in plain Python.

## Key Ideas

1. **JSON refresher:**

   | JSON | Means | Example |
   |---|---|---|
   | `{ }` | An object: named fields | `{"status": "ok"}` |
   | `[ ]` | A list | `["AC1", "AC2"]` |
   | `"text"` | A string (always double quotes) | `"US-205"` |
   | `5`, `45.00` | A number | `5` |

2. **The schema keywords you'll see:**

   | Keyword | Meaning | Example |
   |---|---|---|
   | `type` | What kind of value | `"type": "array"` (a list) |
   | `required` | Fields that must be present | `["story_id", "status"]` |
   | `enum` | Only these values allowed | `["ok", "needs_clarification"]` |
   | `pattern` | Text must match this pattern | `"^US-[0-9]{3}$"` |
   | `items` | Rules for every item in a list | each test case |

3. **A schema checks shape, not meaning.** `"expected_result": "Total is $99.00"` matches the schema even though it's wrong.
4. **Same contract, two forms:** a plain-English table for people, a schema for machines.

## Worked Example: Read a Schema and Use It to Check a Reply

### Step 1 (✍️ Paper): Read the schema

This is the output side of our contract as a JSON Schema. Read it slowly, top to bottom:

```json
{
  "type": "object",
  "required": ["story_id", "status", "test_cases", "open_questions"],
  "properties": {
    "story_id": {"type": "string", "pattern": "^US-[0-9]{3}$"},
    "status": {"enum": ["ok", "needs_clarification"]},
    "test_cases": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "ac_ids", "type", "steps", "expected_result"],
        "properties": {
          "id": {"type": "string", "pattern": "^TC-[0-9]{3}-[0-9]{2}$"},
          "type": {"enum": ["positive", "negative", "boundary"]}
        }
      }
    },
    "open_questions": {"type": "array"}
  }
}
```

**How to read it:**

- The reply must be an **object** with four **required** fields.
- `story_id` must match the pattern `^US-[0-9]{3}$`: `^` = start, `US-`, exactly three digits, `$` = end.
- `status` must be one of two values (`enum`).
- `test_cases` is a list (`array`), and **every** item must have six required fields. Its `id` must look like `TC-205-01`, and its `type` must be one of three values.

Compare it line by line with your output table in `contract.md`. It's the same contract.

### Step 2 (✍️ Paper): Find the problems yourself first

Here's a reply with **three** problems. Find them using the schema, before asking the AI:

```json
{"story_id": "US-205", "status": "done", "test_cases": [
 {"id": "TC-1", "title": "SAVE10 on exactly $50.00", "ac_ids": ["AC1"], "type": "boundary",
  "steps": ["Add items totalling $50.00", "Enter SAVE10", "Click Apply"], "expected_result": "Total is $45.00"},
 {"id": "TC-205-02", "title": "SAVE10 on $49.99", "ac_ids": ["AC2"], "type": "boundary",
  "steps": ["Add items totalling $49.99", "Enter SAVE10", "Click Apply"]}
], "open_questions": ["AC4: What message is shown when a second coupon is entered?"]}
```

### Step 3 (🤖 AI tool): Ask the AI to validate it

Open a **new chat** and paste:

```text
Check this JSON reply against this JSON Schema.
List every place where the reply does NOT match the schema: which field, and why.
Only report schema problems. Do not comment on anything else.

### Schema
<paste the schema from Step 1 here>

### Reply
<paste the reply from Step 2 here>
```

Replace the two `<paste … here>` lines with the schema and the reply.

### Step 4 (✍️ Paper): Compare

Did the AI find the same three problems you did? Did it report anything that **isn't** a schema problem (for example "the expected result should mention the discount")? That would mean it ignored the instruction "only report schema problems".

### Consolidated Prompt

Save the Step 3 prompt in `prompts.txt` (in your `week08` folder) with the schema and reply filled in:

```text
=== Check JSON against a schema - v1 ===
Use: check an AI reply against a JSON Schema and list the mismatches.
Source: Handout 08, Topic 2

--- Prompt (new chat) ---
Check this JSON reply against this JSON Schema.
List every place where the reply does NOT match the schema: which field, and why.
Only report schema problems. Do not comment on anything else.

### Schema
{
  "type": "object",
  "required": ["story_id", "status", "test_cases", "open_questions"],
  "properties": {
    "story_id": {"type": "string", "pattern": "^US-[0-9]{3}$"},
    "status": {"enum": ["ok", "needs_clarification"]},
    "test_cases": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "ac_ids", "type", "steps", "expected_result"],
        "properties": {
          "id": {"type": "string", "pattern": "^TC-[0-9]{3}-[0-9]{2}$"},
          "type": {"enum": ["positive", "negative", "boundary"]}
        }
      }
    },
    "open_questions": {"type": "array"}
  }
}

### Reply
{"story_id": "US-205", "status": "done", "test_cases": [
 {"id": "TC-1", "title": "SAVE10 on exactly $50.00", "ac_ids": ["AC1"], "type": "boundary",
  "steps": ["Add items totalling $50.00", "Enter SAVE10", "Click Apply"], "expected_result": "Total is $45.00"},
 {"id": "TC-205-02", "title": "SAVE10 on $49.99", "ac_ids": ["AC2"], "type": "boundary",
  "steps": ["Add items totalling $49.99", "Enter SAVE10", "Click Apply"]}
], "open_questions": ["AC4: What message is shown when a second coupon is entered?"]}
```

## Checkpoint

**Answer key: the three schema problems** (this is exactly what a real schema validator reports):

| Where | Problem |
|---|---|
| `status` | `"done"` is not one of `"ok"`, `"needs_clarification"` |
| First test case, `id` | `"TC-1"` doesn't match the pattern `TC-` + 3 digits + `-` + 2 digits |
| Second test case | `expected_result` is **missing** (it's required) |

**Mark your AI's answer:** ✅ all three found · ✅ nothing extra reported · ❌ if it missed the missing `expected_result` (a common miss, because people and AIs notice wrong values more easily than missing ones).

**Sample AI answer:** *1. "status" is "done", but the schema only allows "ok" or "needs_clarification". 2. test_cases[0].id "TC-1" does not match the pattern ^TC-[0-9]{3}-[0-9]{2}$. 3. test_cases[1] is missing the required property "expected_result".*

## Your Turn

1. **(In class, 3 min)** In the Step 2 reply, change `"type": "boundary"` in the second test case to `"type": "edge"`. Which schema keyword catches it?
2. **(After class)** Run the Step 3 prompt with the **sample reply** from Lecture 07, Topic 2 (the valid one). Does the AI correctly say there are **no** problems?
3. **(After class)** Ask your AI: *"Explain this JSON Schema line by line for a beginner."* and paste the schema. Did it explain `required` and `enum` correctly?

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| The AI "fixes" the reply instead of listing problems | It drifted from the task | Re-ask: "Do not rewrite it. Only list the problems." |
| The AI reports a problem that isn't one | AIs can be wrong when checking, too | Check each claim against the schema yourself. In Lecture 09, code does this exactly |

---

<a id="topic-3"></a>

# Topic 3: Required Fields and Validation Rules

## Definition

A **required field** must always be present; an **optional** one may be left out. It's important to tell apart a field that is **missing** (not there at all) from one that is **empty** (there, but `[]` or `""`), because they mean different things: an empty `open_questions` list means "no questions", while a missing one means the reply is broken. Some rules can't be written in a schema at all, because they **compare the reply with the story**, for example "every AC must be covered". We write these **validation rules** in plain English with short IDs (R1, R2…), check them by hand today, and turn them into code in Lecture 09.

## Key Ideas

1. **Missing ≠ empty:**

   | | Example | Meaning for `open_questions` |
   |---|---|---|
   | **Missing** | `{"story_id": "US-205", ...}` with no `open_questions` | ❌ Broken reply: the contract says it's required |
   | **Empty** | `"open_questions": []` | ✅ Fine: the agent has no questions |

2. **Our validation rules:**

   | ID | Rule | Why |
   |---|---|---|
   | **R1** | `story_id` in the reply = `story_id` in the story | The reply answers the right story |
   | **R2** | Every AC id in the reply exists in the story | No invented requirements |
   | **R3** | Number of test cases ≤ `max_cases` | The agent respects the limit |
   | **R4** | Every AC in the story has a test case **or** an open question starting with its id | Nothing is forgotten |
   | **Q1** | Expected results have no vague words ("works", "correctly", "properly", "as expected", "successfully") | Every test can clearly pass or fail |

3. **Rules need both the story and the reply.** That's why a schema (which sees only the reply) can't check them.
4. **Some things only a person can check:** invented values (like "2 seconds"), whether boundaries are tested, and whether messages are copied exactly. These go on a **human checklist** (Lecture 10).

## Worked Example: Check Two Replies by Hand

### Step 1 (📝 Editor): Add the rules to `contract.md`

Add this section at the end of `contract.md`:

```text
## Rules (checked by check_reply.py, Lecture 09)
R1  story_id in the reply = story_id in the story
R2  every ac_id in the reply exists in the story (no invented ACs)
R3  number of test cases <= max_cases
R4  every AC in the story has a test case OR an open question starting with its id
Q1  expected results are exact: no "works", "correctly", "properly",
    "as expected" or "successfully"

## Checked by a person (Lecture 10)
- No invented rules or values
- Every boundary tested at the limit and just below it
- Messages copied exactly
```

### Step 2 (✍️ Paper): Check Reply A

This reply is for **US-312** (`max_cases` is 3, ACs are AC1 and AC2):

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

Go through R1, R2, R3, R4 and Q1 in order, and write down every rule it breaks.

### Step 3 (✍️ Paper): Check Reply B

This reply is for **US-311** (one AC, `max_cases` is 3):

```json
{"story_id": "US-031", "status": "needs_clarification", "test_cases": [],
 "open_questions": ["AC1: What is the maximum time, in seconds, for search results to appear?"]}
```

Check it the same way. Careful: this one is **almost** perfect.

### Step 4 (✍️ Paper): Missing or empty?

For Reply B, `test_cases` is `[]`. Is that a problem? Look at the contract's output table and its "I can't" section.

### Consolidated Result

`contract.md` now has the input side, the output side, the "I can't" rule and the **Rules** section. In Lecture 09, `check_reply.py` will check R1–R4 and Q1 automatically, in exactly this order.

## Checkpoint

**Answer key, Reply A (US-312):**

| Rule | Broken? | Why |
|---|---|---|
| R1 | No | `US-312` matches |
| **R2** | **Yes** | TC-312-03 refers to **AC3**, which isn't in the story (invented) |
| **R3** | **Yes** | **4** test cases; the maximum is 3 |
| **R4** | **Yes** | **AC2** (the message) has no test case and no question |
| **Q1** | **Yes** | TC-312-02: "works correctly" is vague |

**Answer key, Reply B (US-311):** only **R1** is broken: `"US-031"` should be `"US-311"` (a typo). Everything else is right. **Step 4:** `test_cases: []` is **correct** here, because the contract allows an empty list for `needs_clarification`.

## Your Turn

1. **(In class, 3 min)** Fix Reply A on paper so it breaks **no** rules. What's the smallest set of changes?
2. **(After class)** Write a reply for US-205 that breaks **only R4**. Swap with a classmate and check each other's.
3. **(After class)** 🤖 Paste `contract.md` and Reply A into your AI tool and ask: *"Which of the rules R1, R2, R3, R4 and Q1 does this reply break? Answer as a table."* Compare it with the answer key. Did the AI find all four?

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| You marked R4 as passed for Reply A | TC-312-02 is about 9 items, but its `ac_ids` says **AC1**, not AC2 | R4 looks at `ac_ids`, not at what the title seems to cover |
| You thought `test_cases: []` breaks the contract | Confusing **empty** with **missing** | Empty is allowed; missing is not |

---

<a id="topic-4"></a>

# Topic 4: Sample Input/Output Pairs

## Definition

A **sample input/output pair** is an example **story** together with a **correct reply** for it. Pairs do two jobs for our agent: they **document** what a good answer looks like, and, when added to the prompt, they work as **few-shot examples** (Lecture 03): the AI copies their pattern, including the exact JSON shape and how to say "I can't". Choosing pairs that show **different situations**, such as a clear story and a vague one, is what makes them useful. Every example must itself obey the contract, because the AI copies mistakes too.

## Key Ideas

1. **Show, don't tell.** One good example reply teaches the JSON shape better than a paragraph of rules.
2. **Cover different situations.** Our two pairs: a **clear** story (normal test cases, boundaries) and a **vague** story (`needs_clarification` with a question).
3. **Use different stories from the real ones.** Examples about free delivery (US-150) and login (US-160) teach the pattern without giving away answers for US-205, US-311 or US-312.
4. **Examples must pass every rule.** A broken example teaches broken habits.

## Worked Example: Write `examples.txt` and See the Difference

### Step 1 (📝 Editor): Example 1, a clear story

Create `examples.txt` in your `agent` folder:

```text
### Example 1: a clear story
Story: US-150 Free delivery. Maximum test cases: 2
AC1: Orders of $30.00 or more get free delivery.
Reply:
{"story_id": "US-150", "status": "ok", "test_cases": [
 {"id": "TC-150-01", "title": "Order of exactly $30.00 gets free delivery", "ac_ids": ["AC1"],
  "type": "boundary", "steps": ["Add items totalling $30.00", "Go to checkout"],
  "expected_result": "Delivery cost shows $0.00"},
 {"id": "TC-150-02", "title": "Order of $29.99 pays delivery", "ac_ids": ["AC1"],
  "type": "boundary", "steps": ["Add items totalling $29.99", "Go to checkout"],
  "expected_result": "Delivery cost is not $0.00"}],
 "open_questions": []}
```

**What it teaches:** the exact JSON shape, the ID format, testing **at** the limit ($30.00) and **just below** it ($29.99), and exact expected results. Notice the second expected result doesn't invent a delivery price, because the story doesn't give one.

### Step 2 (📝 Editor): Example 2, a vague story

Add underneath:

```text
### Example 2: a story that is too vague to test
Story: US-160 Quick login. Maximum test cases: 2
AC1: Login should be quick.
Reply:
{"story_id": "US-160", "status": "needs_clarification", "test_cases": [],
 "open_questions": ["AC1: What is the maximum login time, in seconds?"]}
```

**What it teaches:** how to say "I can't": `needs_clarification`, an empty list, and a question that starts with the AC id. "Quick" is like "fast" in US-311, so this example should help with exactly the mistake from Lecture 07.

### Step 3 (✍️ Paper): Check your examples against the rules

Run R1–R4 and Q1 over both example replies (using their own stories). Both should break **no** rules.

### Step 4 (🤖 AI tool): Run US-311 again, now with examples

Open a **new chat** and paste, **in this order**, as **one message**:

1. the whole of `instructions_draft.md`
2. the whole of `examples.txt`
3. the whole of `filled_US-311.txt` from Lecture 07 (shown here in case you don't have it):

```text
### Story
ID: US-311
Title: Fast search
Maximum test cases: 3
Acceptance criteria:
AC1: Search results should appear fast.
### End of story

Now write the JSON reply for this story.
```

Compare the reply with what you got in Lecture 07 **without** examples.

### Consolidated File: `examples.txt`

```text
### Example 1: a clear story
Story: US-150 Free delivery. Maximum test cases: 2
AC1: Orders of $30.00 or more get free delivery.
Reply:
{"story_id": "US-150", "status": "ok", "test_cases": [
 {"id": "TC-150-01", "title": "Order of exactly $30.00 gets free delivery", "ac_ids": ["AC1"],
  "type": "boundary", "steps": ["Add items totalling $30.00", "Go to checkout"],
  "expected_result": "Delivery cost shows $0.00"},
 {"id": "TC-150-02", "title": "Order of $29.99 pays delivery", "ac_ids": ["AC1"],
  "type": "boundary", "steps": ["Add items totalling $29.99", "Go to checkout"],
  "expected_result": "Delivery cost is not $0.00"}],
 "open_questions": []}

### Example 2: a story that is too vague to test
Story: US-160 Quick login. Maximum test cases: 2
AC1: Login should be quick.
Reply:
{"story_id": "US-160", "status": "needs_clarification", "test_cases": [],
 "open_questions": ["AC1: What is the maximum login time, in seconds?"]}
```

**Your `agent` folder now has every text part of the agent:**

```text
agent/
├── README.txt
├── instructions_draft.md
├── input_template.txt
├── contract.md
├── examples.txt
└── stories/
    ├── US-205.json
    ├── US-311.json
    └── US-312.json
```

## Checkpoint

**Step 3:** both examples pass every rule (R1–R4, Q1).

**Mark your AI's reply (Step 4):**

- ✅ `status` is `"needs_clarification"` and `test_cases` is `[]`
- ✅ One open question starting with `AC1:` asking for a time in seconds
- ✅ **No invented time limit**
- ✅ The JSON shape matches the examples exactly

**Sample AI reply:**

```json
{"story_id": "US-311", "status": "needs_clarification", "test_cases": [],
 "open_questions": ["AC1: What is the maximum time, in seconds, for search results to appear?"]}
```

With an example of a vague story, most AIs now copy the honest refusal pattern. If yours still invented a number, don't worry: Lecture 10 adds a rule that targets exactly this.

## Your Turn

1. **(In class, 3 min)** With a neighbour, compare your Step 4 replies with your Lecture 07 replies for US-311. Did the examples change the answer?
2. **(After class)** Run US-312 (`filled_US-312.txt` from Lecture 07, exercise 2) with the instructions **and** the examples. Did it test 10 and 9 items, and copy the AC2 message exactly?
3. **(After class)** **Bad examples teach bad habits:** in a copy of `examples.txt`, change Example 1's second expected result to `"Delivery works correctly"`. Run US-312 with it. Did any vague wording appear in the reply?

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| The AI also "answers" the examples | The story at the end isn't clearly separated | Keep the `### Story` … `### End of story` fences and the final instruction line |
| The AI copies an example's story ID | It confused the example with the real story | Use clearly different IDs (US-150, US-160) and keep the real story **last** |

---

## Lecture Wrap-Up: Quick Check

1. What are the two sides of an agent's contract?
2. How does our agent say "I can't test this story"?
3. What does the schema keyword `enum` do?
4. Why can't a JSON Schema check rule R4?
5. What's the difference between a **missing** field and an **empty** one?
6. Why do our examples include a vague story?

<details>
<summary>Answers</summary>

1. The **input** (what a story looks like) and the **output** (what every reply must look like).
2. `status: "needs_clarification"`, an empty `test_cases` list, and open questions starting with the AC id.
3. It lists the only values allowed, for example `"ok"` or `"needs_clarification"`.
4. R4 compares the reply **with the story** (are all ACs covered?). A schema only sees the reply.
5. Missing = the field isn't there (broken). Empty = it's there with no items (`[]`), which can be fine.
6. So the AI sees how to refuse honestly instead of inventing a value, the mistake from US-311.

</details>

---

## Glossary

| Term | Meaning |
|---|---|
| **Contract** | A written agreement on what goes into the agent and what must come out |
| **JSON Schema** | A machine-readable description of valid JSON |
| **Validator** | A tool that checks JSON against a schema |
| **`required` / `enum` / `pattern`** | Must be present / only these values / must match this text pattern |
| **Missing vs. empty** | Not there at all vs. there with nothing in it |
| **Validation rule** | A rule that compares the reply with the story (R1–R4, Q1) |
| **Sample input/output pair** | An example story with a correct reply |
| **Few-shot examples** | Example pairs in the prompt that the AI copies the pattern from |

## Summary

- The **contract** defines a valid input (story file) and a valid output (reply), including an honest way to say **"I can't"**.
- A **JSON Schema** is the same contract in machine-readable form. It checks **shape**, not meaning.
- **Rules R1–R4 and Q1** compare the reply with the story. You checked them by hand today; next lecture, code checks them.
- **Example pairs** teach the AI the exact pattern, including refusing vague stories, so choose them carefully and make sure they obey every rule.
