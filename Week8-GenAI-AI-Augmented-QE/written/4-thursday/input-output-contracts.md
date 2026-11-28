# Input/Output Contracts

## Learning Objectives

By the end of this lesson you will be able to:

- **Define** an input/output contract and explain who relies on it.
- **Write** both sides of TestCaseDesigner's contract: what a story looks like going in, and what every reply must look like coming out.
- **Describe** each field by name, kind, whether it is required, and its rule.
- **Explain** how the agent says "I can't test this story", and why that is part of the contract.
- **Write** stories as JSON data files, and fix the most common JSON errors.

---

## Why This Matters

In *Agent Instructions* the output format was a few lines of text: "Reply with ONE JSON object... Keys: story_id, status, test_cases, open_questions". That was enough to test the idea. It is not enough to build on.

Tomorrow, three different things will depend on the agent's format: a program that builds the prompts, a program that checks every reply, and a person who reviews the results. If each of them has a slightly different idea of what a "valid reply" is, they will disagree, and nobody will know who is right. Can `test_cases` be empty? Is `open_questions` optional? What exactly are the allowed `status` values? A few lines of text leave these open.

An **input/output contract** answers them, in writing, once. It is the **definition of "a valid answer"** that every check is built from.

Contracts are an old and proven idea in software. The computer scientist Bertrand Meyer coined the term **design by contract** in connection with his design of the Eiffel programming language, first described in articles from 1986: software components should have precise, verifiable specifications of what they expect and what they guarantee ([Wikipedia](https://en.wikipedia.org/wiki/Design_by_contract)).

Testers meet the idea today in **contract testing**: tools such as Pact use contract tests to check that messages between applications conform to a shared understanding documented in a contract ([Pact docs](https://docs.pact.io/)). TestCaseDesigner's contract is a simple version of the same thing: a shared, written agreement about what goes in and what must come out.

> **Using this with the handout:** this lesson goes deeper into **Handout 08, Topic 1**. It uses the same `contract.md`, the same input and output tables, the same "I can't" rule, the same three story files and the same checkpoint questions.

---

## The Concept

### 1. What Is an Input/Output Contract?

An **input/output contract** is a written agreement about **what an agent receives** (the input) and **what it must return** (the output): which fields, what kind of values, what is required and what is allowed.

Everyone who builds or uses the agent relies on it:

| Who | How they use the contract |
|---|---|
| **You, writing the instructions** | The Output section must describe exactly what the contract says |
| **The prompt builder** (tomorrow) | Reads story files that follow the input side |
| **The reply checker** (tomorrow) | Decides "valid" or "not valid" from the output side |
| **The tester reviewing results** | Knows what every field means and what to expect |
| **Anyone using the results later** | Can rely on the shape without reading the agent's code |

AI answers vary from run to run, which makes the contract more important for an agent than for ordinary code. A normal function returns the same shape every time because its code says so. An AI returns whatever it generates. The contract is how you say, precisely, which of those replies are acceptable.

### 2. Two Sides of the Contract

| Side | Describes | Our version |
|---|---|---|
| **Input** | What a story looks like when it goes in | A JSON file in `stories/` |
| **Output** | What every reply must look like | One JSON object with four fields |

The two sides are linked. Several output rules refer to the input: `story_id` must be **the same** as the input's, and the number of test cases must not exceed the input's `max_cases`. That is why both sides live in one document.

If you have tested an API, this will feel familiar. An API's documentation describes the request (input) and the response (output) for each endpoint, and API tests check that real responses match. Our contract is the same idea, for an AI agent.

### 3. Describing a Field

For **every** field, a contract states four things:

| Property | Question it answers | Example for `max_cases` |
|---|---|---|
| **Name** | What is it called, exactly? | `max_cases` |
| **Kind** | What type of value? | number |
| **Required?** | Must it always be there? | yes |
| **Rule** | What does a valid value look like? | The most test cases the agent may return |

The kinds we use are the basic JSON types you met on Tuesday in *Format Locking*:

| Kind | JSON form | Example |
|---|---|---|
| **text** (string) | In double quotes | `"US-205"` |
| **number** | No quotes | `5` |
| **list** (array) | Square brackets | `["AC1", "AC2"]` |
| **object** | Curly braces, named fields | `{"id": "AC1", "text": "..."}` |

Exact names matter. To a program, `story_id`, `storyId` and `story-id` are three different fields. A contract that says `story_id` means **only** `story_id`. Kinds matter just as much: `"max_cases": "5"` (text) is not the same as `"max_cases": 5` (a number). A program that compares the number of test cases with `max_cases` will fail, or quietly give the wrong answer, if the kind is wrong. You saw the same problem with ages written as text in *AI-Generated Test Data* on Wednesday.

### 4. The Agent Must Be Able to Say "I Can't"

The third key idea in the handout is the most unusual: **the contract includes a way to refuse.**

When a story is too vague to test, like US-311 ("search results should appear fast"), the honest answer is "I can't write test cases for this yet". If the contract has no way to say that, the agent has two options: break the contract (reply with free text) or obey it with invented content ("within 2 seconds"). You saw the second happen in *Prompt Templates*.

So the contract defines the refusal precisely:

- `status` is `"needs_clarification"`,
- `test_cases` is an **empty list** `[]`,
- and `open_questions` holds one question per problem, each starting with its AC id.

This makes "I can't" a **valid, checkable answer**, not a failure. A program can recognise it, count it and report it: *"US-311: needs clarification, 1 question"*. That is far more useful than an invented test case nobody can trust. It is also the agent version of what you did by hand on Wednesday: when a requirement is untestable, ask the BA a question instead of guessing.

### 5. The Story Becomes a Data File

The last key idea is practical. Code cannot read "US-205 Apply coupon..." from a handout. It **can** read a **JSON file** that follows the input contract. So each story is written as a file in the `stories` folder, one file per story.

Writing stories as data has benefits beyond code:

- Every story has **exactly** the fields the contract requires, so nothing is forgotten.
- The ACs are a **list**, each with an `id` and `text`, so they can be counted and matched.
- Adding a story means adding a file, without touching the instructions or the template.

### 6. Worked Example: Write `contract.md` and the Story Files

#### Step 1 (Editor): The input side

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

Each row answers the four questions from section 3. Notice the rule for `acceptance_criteria`: **at least 1**. A story with no criteria cannot be tested, so it is not a valid input at all. That rule protects the agent from being asked to do the impossible.

The title says **v1**. Contracts change, and a version number tells everyone which agreement a file follows.

#### Step 2 (Editor): The output side

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

Notice "**may be empty**" twice. When the agent cannot produce tests, `test_cases` is `[]`, which is very different from the field being **missing**. An empty list says "I looked, and there are none". A missing field says "this reply is broken". *Required Fields and Validation Rules*, later today, explains this difference in detail.

Notice also that every output field is **required**. That is a deliberate choice: a checker never has to wonder whether a missing `open_questions` means "no questions" or "the AI forgot". It always means "broken".

#### Step 3 (Editor): How the agent says "I can't"

Add:

```text
## Saying "I can't"
If no criterion can be tested: status = "needs_clarification", test_cases = [],
and one open question per problem, starting with the AC id (e.g. "AC1: ...").
```

Three lines, and every part of them is checkable: the status value, the empty list, and the question prefix.

#### Step 4 (Editor): Write the stories as data files

Create three files in the `stories` folder. Type them exactly as shown; tomorrow's code will read them.

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

**Why these three?** Each one tests the agent differently. **US-205** has a boundary and an incomplete AC (AC4). **US-311** is too vague to test. **US-312** has a boundary with whole numbers (10 vs 9). Together they cover the three situations the agent must handle: a normal story, an impossible one, and a different kind of boundary.

Look at AC2 in US-205. Inside a JSON string, a double quote is written as `\"`. Without the backslash, the quote would **end** the string early, and the file would break. This is called **escaping**: the backslash tells JSON "this quote is part of the text".

### 7. Checking the Story Files

Before tomorrow's code reads your story files, it helps to check that they are valid JSON. Python's built-in `json` module can do it. This short script, `check_story_files.py`, loads every file in `stories/` and prints a one-line summary of each. You do not need to run it today, but it shows what tomorrow's code will see:

```python
import json
from pathlib import Path

for path in sorted(Path("stories").glob("*.json")):
    try:
        story = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        print(f"{path.name}: NOT valid JSON - {error}")
        continue
    ac_ids = [ac["id"] for ac in story["acceptance_criteria"]]
    print(f"{path.name}: {story['story_id']}, {len(ac_ids)} AC(s) {ac_ids}, max {story['max_cases']}")
```

With the three files typed correctly, it prints:

```text
US-205.json: US-205, 4 AC(s) ['AC1', 'AC2', 'AC3', 'AC4'], max 5
US-311.json: US-311, 1 AC(s) ['AC1'], max 3
US-312.json: US-312, 2 AC(s) ['AC1', 'AC2'], max 3
```

**What this code does:**

- `Path("stories").glob("*.json")` finds every `.json` file in the folder; `sorted` keeps the order predictable.
- `json.loads(...)` turns the file's text into Python data. If the text is not valid JSON, it raises a `JSONDecodeError`, which the `except` catches and reports instead of crashing.
- `[ac["id"] for ac in ...]` collects the AC ids from the list, so you can see at a glance that every AC was typed.

The useful part is the error messages. Here is what Python prints for the four mistakes students make most often, tested on Python 3.13:

| Mistake | Example | Message |
|---|---|---|
| Missing comma between fields | `"title": "Fast search"` with no comma | `Expecting ',' delimiter: line 4 column 3` |
| Extra comma after the last item | `"max_cases": 3,` then `}` | `Illegal trailing comma before end of object: line 7 column 17` |
| A plain quote inside a string | `show "Coupon code not recognised".` without `\` | `Expecting ',' delimiter: line 7 column 48` |
| Single quotes | `'title': ...` | `Expecting property name enclosed in double quotes: line 3 column 3` |

Two things to know about these messages. First, the **line and column** tell you where Python got confused, which is usually at or just **after** the real mistake. For the missing comma, Python reports line 4, the line **after** the title, because that is where it expected a comma and found something else.

Second, messages vary a little between Python versions. On Python 3.10, the trailing comma gives `Expecting property name enclosed in double quotes` instead. If a message seems strange, look at the reported line and the line before it.

The plain-quote row shows why the handout's escaping tip matters. A missing backslash does not produce a message about quotes; it produces a message about a **missing comma**, because JSON thinks the string ended and expects the next field. Error messages describe what the reader expected, not what you did wrong.

### 8. The Test Case Fields, in Detail

The output table describes the four top-level fields. The line underneath it, "Each test case has...", describes the six fields inside every test case. Written out with the same four properties, they look like this:

| Field | Kind | Required? | Rule |
|---|---|---|---|
| `id` | text | yes | `TC-` + the story's 3-digit number + `-` + 2 digits, e.g. `TC-205-01` |
| `title` | text | yes | A short description of what the case checks |
| `ac_ids` | list of text | yes | Each item is an AC id **from this story**, e.g. `["AC1"]` |
| `type` | text | yes | `positive`, `negative` or `boundary` |
| `steps` | list of text | yes | The actions a tester takes, in order |
| `expected_result` | text | yes | The exact outcome that decides pass or fail |

Two rules here reach back to the input. The `id` uses the **story's** number, so `TC-205-01` belongs to US-205 and a reply for US-205 containing `TC-312-01` is suspicious. And `ac_ids` must use ids **from this story**, so a test case for "AC3" in a reply for US-312, which only has AC1 and AC2, is an invented requirement. Rules like these, which compare the reply with the story, are the subject of *Required Fields and Validation Rules* later today.

Notice also that `ac_ids` is a **list**, not a single value. One test case can cover two criteria, for example a single checkout that checks an amount rule from one AC and a message rule from another. Making it a list from the start means the contract does not need to change when that happens.

### 9. Checking a Reply Against the Contract

Take the typical US-311 mistake from *Prompt Templates*:

```json
{"story_id": "US-311", "status": "ok", "test_cases": [
 {"id": "TC-311-01", "title": "Search results appear within 2 seconds", "ac_ids": ["AC1"],
  "type": "positive", "steps": ["Open the search page", "Search for \"shoes\""],
  "expected_result": "Results are displayed within 2 seconds"}
], "open_questions": []}
```

Check it against the output side, row by row:

| Contract line | Result |
|---|---|
| `story_id` is the same as the input | ✅ `US-311` |
| `status` is "ok" or "needs_clarification" | ✅ `ok` is allowed |
| `test_cases` is a list | ✅ |
| `open_questions` is a list | ✅ (empty, which is allowed) |
| Every test case has all six fields | ✅ |
| `id` follows `TC-311-xx` | ✅ |
| `ac_ids` uses ids from the story | ✅ `AC1` |
| `type` is one of three values | ✅ `positive` |

**It passes every line.** And it is still wrong: "2 seconds" is invented, and the agent should have refused.

This is not a flaw in the contract. It shows what a contract **is**: a definition of acceptable **shape and values**, not a judge of meaning. The contract says what a valid refusal looks like, but it cannot force the AI to refuse when it should. Catching the invented value needs something else: a rule that reads the reply **together with** the story, or a person. You will meet both later today and tomorrow.

### 10. What a Contract Does Not Do

Three limits are worth stating plainly, so nobody expects too much:

- **It does not make the AI obey.** The contract is a description. The instructions and examples are what persuade the AI to follow it, and the checker is what finds out whether it did.
- **It does not define good tests.** A reply with six fields in every test case can still have weak expected results or missing boundaries. Quality rules live in the instructions and the human checklist.
- **It does not check meaning.** As section 9 shows, a reply can match every line and still contain an invented value.

What the contract **does** do is make every other check possible. A checker needs to know what "valid" means before it can say "not valid". A reviewer needs to know what each field means before judging its content. The contract is the foundation the other checks stand on.

### 11. Answering Questions from the Contract

A contract is useful only if it answers questions without anyone needing to ask the author. The handout's checkpoint tests exactly that:

| Question | Answer from the contract | Where it says so |
|---|---|---|
| Can `test_cases` be an empty list? | **Yes**, for example when status is `needs_clarification` | Output table: "May be empty" |
| Can `open_questions` be left out of a reply? | **No**: it is required, but may be empty | Output table: "yes", "May be empty" |
| A reply says `"status": "done"`. Valid? | **No**: only `"ok"` or `"needs_clarification"` | Output table, status rule |
| How does the agent say "this story is too vague"? | `status: "needs_clarification"`, empty `test_cases`, a question starting `AC1:` | "Saying I can't" section |

Every answer points to a specific line. That is the test of a good contract: **every question about validity has one answer, and you can point to where it is written.** If you find yourself saying "I think..." about a field, the contract needs another line.

### 12. Contract First

Notice the order of work this week: the contract is written **before** the checker and before the final instructions. That order is deliberate, and it is common in software teams, sometimes called **contract-first** design. Write down what must be true, then build the pieces that produce and check it.

The contract also shows what a change will affect. Suppose the team decides each test case needs a `priority` field:

| File | Change needed |
|---|---|
| `contract.md` | Add `priority` to the test case fields, with its allowed values |
| Instructions | Add `priority` to the Output section |
| Examples | Add `priority` to every example reply |
| Checker (tomorrow) | Check that `priority` is present and allowed |

One line in the contract leads to four changes. Without the contract, someone would update the instructions and forget the examples, and the AI would receive mixed signals: the instructions asking for `priority`, the examples showing replies without it. With the contract as the single source of truth, the list of files to update is clear. This is also when the version number changes: the new agreement becomes **v2**.

### 13. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| Story file breaks later with "Expecting ',' delimiter" | A missing comma between fields, or a plain quote inside a string | Look at the reported line and the line before it; compare with the handout character by character |
| Quotes inside the AC text break the file | A plain `"` inside a JSON string ends the string | Write it as `\"`, as in US-205's AC2 |
| A reply passes the contract but is still wrong | The contract checks shape and values, not meaning | Use the validation rules and the human checklist as well |
| `test_cases` uses another story's number, such as `TC-312-01` in a US-205 reply | The AI copied an ID pattern from somewhere else | The `id` rule ties every ID to this story's number |
| A field name does not match the contract | `storyId` or `story-id` instead of `story_id` | Copy names from the contract, never retype them from memory |
| The instructions and the contract disagree | One was changed without the other | Treat the contract as the source of truth, and update everything it lists |

---

## Practice Exercises

1. **Which line? (paper, 5 min).** A reply contains 7 test cases for US-205. Which line of the contract does that break? Hint: look at the input side as well as the output side.

2. **Write US-313 (editor, 10 min).** Write `stories/US-313.json` for: *US-313 Track an order. AC1: Guests can track an order by entering its order number. AC2: An unknown order number shows "Order not found".* Use `"max_cases": 3`. Remember the escaped quotes in AC2.

3. **Ask for an example reply (AI tool, 15 min).** Follow this week's four steps:
   - **Prompt:** paste your `contract.md` into your AI tool and ask: *"Write one valid example reply for story US-312 that follows this contract."*
   - **Review:** check its reply against **every** row of your output table, and the test case fields.
   - **Run:** if you have Python set up, save the reply as a `.json` file and check it loads with `json.loads`.
   - **Record:** in `prompts.txt`, note any field the AI got wrong or added.

4. **Break a story file (code, 10 min).** Make a copy of `US-311.json`, remove the comma after the title, and load it with `check_story_files.py` (or `json.loads` in Python). Read the message. Which line does it report, and why is it not the line you changed?

---

## Knowledge Check

1. What are the two sides of an agent's contract?

<details><summary>Answer</summary>

The input (what a story looks like going in) and the output (what every reply must look like).

</details>

2. What four things does the contract state for every field?

<details><summary>Answer</summary>

Its name, its kind (text, number, list or object), whether it is required, and its rule for valid values.

</details>

3. How does our agent say "I can't test this story"?

<details><summary>Answer</summary>

`status: "needs_clarification"`, an empty `test_cases` list, and open questions starting with the AC id.

</details>

4. Why is it useful to make "I can't" a valid answer in the contract?

<details><summary>Answer</summary>

Without it, the agent's only options are to break the format or invent content. A defined refusal is honest, checkable and can be counted and reported.

</details>

5. Can `open_questions` be left out of a reply? Can it be empty?

<details><summary>Answer</summary>

It cannot be left out: it is required. It can be empty, which means the agent has no questions.

</details>

6. Why is the quote in US-205's AC2 written as `\"`?

<details><summary>Answer</summary>

A plain `"` would end the JSON string early and break the file. The backslash escapes the quote, making it part of the text.

</details>

7. The team adds a `priority` field to test cases. Which files must change?

<details><summary>Answer</summary>

The contract, the instructions' Output section, every example reply, and the checker. The contract's version should change too.

</details>

8. The US-311 reply with "within 2 seconds" passes every line of the output contract. What does that tell you about contracts?

<details><summary>Answer</summary>

A contract defines acceptable shape and values, not meaning. Catching an invented value needs a rule that compares the reply with the story, or a person.

</details>

---

## Glossary

- **Input/output contract:** a written agreement on what goes into the agent and what must come out.
- **Input side / output side:** the parts of the contract describing stories and replies.
- **Field:** a named value in a JSON object, such as `story_id`.
- **Kind (type):** what sort of value a field holds: text, number, list or object.
- **Required field:** a field that must always be present.
- **Rule (in a contract):** what a valid value looks like.
- **`needs_clarification`:** the status the agent uses to say "I can't test this story yet".
- **Escaping:** writing a special character, such as `"` inside a string, as `\"` so it is treated as text.
- **Design by contract:** Bertrand Meyer's approach of giving software components precise, verifiable specifications.
- **Contract testing:** testing that messages between systems match a shared, documented contract.
- **Contract-first:** writing the contract before building the parts that produce and check the data.
- **Top-level field:** a field directly in the reply object, such as `status`, rather than inside a test case.
- **Contract version:** a number, such as v1, that changes whenever the agreement changes.
- **Source of truth:** the one document everyone treats as correct when others disagree.

---

## Summary

- The **contract** defines a valid input (a story file) and a valid output (a reply). It is the definition of "a valid answer" that every check is built from.
- For every field, state its **name, kind, whether it is required, and its rule**.
- The contract includes an honest way to say **"I can't"**: `needs_clarification`, an empty list and AC-prefixed questions.
- Stories become **JSON data files**, so code can read them. Escape quotes inside strings as `\"`.
- Write the **contract first**, and treat it as the **source of truth** when files disagree.

---

## Additional Resources

- Pact documentation, *Introduction to contract testing*: https://docs.pact.io/
- Python documentation, *json — JSON encoder and decoder*: https://docs.python.org/3/library/json.html
- OpenAI, *Structured Outputs* (how AI providers use a contract-like schema for replies): https://developers.openai.com/api/docs/guides/structured-outputs
