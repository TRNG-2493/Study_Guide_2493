# JSON Schema

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** what JSON Schema is, and how it relates to the agent's contract.
- **Read** a simple schema using the keywords `type`, `required`, `properties`, `enum`, `pattern` and `items`.
- **Check** a reply against a schema by hand, and find wrong values, wrong patterns and missing fields.
- **Compare** your findings with an AI's check and with a real schema validator.
- **Explain** why a schema checks shape, not meaning, and what it cannot express.

---

## Why This Matters

In *Input/Output Contracts* you wrote TestCaseDesigner's contract as tables in plain English. Tables are perfect for people: anyone on the team can read them. But a program cannot read "May be empty; each starts with an AC id". To check thousands of replies automatically, the contract needs a form a **computer** can read.

**JSON Schema** is that form. It describes what valid JSON looks like, and it is written in JSON itself. The project's own site describes it as a vocabulary you can use to annotate and validate JSON documents ([JSON Schema](https://json-schema.org/learn/getting-started-step-by-step)). Tools called **validators** read a schema and check any JSON against it, reporting every place that does not match.

JSON Schema matters beyond this course. Many APIs describe their requests and responses with it. And AI providers use it too: on Tuesday, in *Format Locking*, you met OpenAI's **Structured Outputs**, a feature that makes a model's reply follow a JSON Schema the developer supplies ([OpenAI](https://developers.openai.com/api/docs/guides/structured-outputs)). Reading a schema is becoming a basic skill for anyone who tests AI systems.

This week you only need to **read** a schema, not write one from scratch. Tomorrow you will write a short checker in plain Python that does the most important checks. Today's job is to understand what a schema says, and, just as important, what it **cannot** say.

> **Using this with the handout:** this lesson goes deeper into **Handout 08, Topic 2**. It uses the same schema, the same reply with three problems, the same validation prompt and the same answer key.

---

## The Concept

### 1. What Is JSON Schema?

**JSON Schema** is a standard way to describe **what valid JSON looks like**, written in JSON itself. A schema lists:

- which fields are **required**,
- what **type** each value is,
- which values are **allowed** (`enum`),
- and what text must look like (`pattern`).

Validators can then check any JSON reply against the schema automatically. In other words, a schema is your contract's output table written so that a **computer** can read it.

**Same contract, two forms:** a plain-English table for people, a schema for machines. Both should say the same thing. If they disagree, you have two contracts, and the people and the programs will disagree too.

### 2. A JSON Refresher

A schema is built from the same pieces as the JSON it checks:

| JSON | Means | Example |
|---|---|---|
| `{ }` | An object: named fields | `{"status": "ok"}` |
| `[ ]` | A list (called an **array** in JSON) | `["AC1", "AC2"]` |
| `"text"` | A string (always double quotes) | `"US-205"` |
| `5`, `45.00` | A number | `5` |

Two words in schemas come from JSON rather than everyday English: a list is an **array**, and a named field in an object is a **property**. When a schema says `"type": "array"`, it means "a list".

### 3. The Schema Keywords You Will See

| Keyword | Meaning | Example |
|---|---|---|
| `type` | What kind of value | `"type": "array"` (a list) |
| `required` | Fields that must be present | `["story_id", "status"]` |
| `properties` | Rules for each named field | `"status": {...}` |
| `enum` | Only these values allowed | `["ok", "needs_clarification"]` |
| `pattern` | Text must match this pattern | `"^US-[0-9]{3}$"` |
| `items` | Rules for every item in a list | each test case |

Each one is easiest to understand with a valid and an invalid example:

| Keyword and rule | Valid | Invalid |
|---|---|---|
| `"type": "array"` | `[]`, `["a"]` | `"none"` (a string) |
| `"required": ["status"]` | `{"status": "ok"}` | `{}` (no `status` at all) |
| `"enum": ["ok", "needs_clarification"]` | `"ok"` | `"done"`, `"OK"` |
| `"pattern": "^US-[0-9]{3}$"` | `"US-205"` | `"US-31"`, `"us-205"`, `"US-2050"` |

Look at the invalid `enum` examples. `"OK"` in capitals is invalid, because enum values are compared **exactly**. And look at the `pattern` examples. The pattern you met on Monday as a **regular expression** reads: `^` start, `US-`, `[0-9]{3}` exactly three digits, `$` end. So `US-31` (two digits) and `US-2050` (four digits) both fail, and so does lower-case `us-205`.

### 4. Worked Example: Read the Schema

#### Step 1 (Paper): Read it slowly, top to bottom

This is the output side of our contract as a JSON Schema:

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
- `story_id` must be a string matching `^US-[0-9]{3}$`: `US-` and exactly three digits.
- `status` must be one of two values (`enum`).
- `test_cases` is a list (`array`), and **every** item in it (`items`) must be an object with six **required** fields. Its `id` must look like `TC-205-01`, and its `type` must be one of three values.
- `open_questions` must be a list.

Notice the nesting. The schema has the same shape as the JSON it describes: an outer object for the reply, and inside `test_cases`, an inner object for each test case. Reading a schema is mostly a matter of following that nesting, one level at a time.

There is one word that can confuse: `type`. Near the bottom, `"type": {"enum": [...]}` is **not** the schema keyword `type`. It is the rule for the test case field that happens to be **called** `type` (positive, negative or boundary). It sits inside `properties`, so it is a field name. Keywords and field names live in different places, which is how you tell them apart.

#### Compare with the contract

Line up the schema with the output table from `contract.md`:

| Contract (for people) | Schema (for machines) |
|---|---|
| All four fields required | `"required": ["story_id", "status", "test_cases", "open_questions"]` |
| `story_id`: "US-" + 3 digits | `"pattern": "^US-[0-9]{3}$"` |
| `status`: "ok" or "needs_clarification" | `"enum": ["ok", "needs_clarification"]` |
| `test_cases`: a list, may be empty | `"type": "array"` (an empty list is still an array) |
| Each test case has six fields | `"items": {"required": [six names]}` |
| `id` like TC-205-01 | `"pattern": "^TC-[0-9]{3}-[0-9]{2}$"` |
| `type`: positive, negative or boundary | `"enum": ["positive", "negative", "boundary"]` |
| `open_questions`: a list, may be empty | `"type": "array"` |

It is the same contract. Every line of the schema corresponds to a line of the table. Keeping the two in step is part of maintaining the agent: when *Input/Output Contracts* talked about adding a `priority` field, the schema would be one more file on the list of changes. A good habit is to put the contract version in both places, so that anyone can see at a glance whether the table and the schema describe the same agreement.

### 5. Worked Example: Check a Reply

#### Step 2 (Paper): Find the problems yourself first

Here is a reply with **three** problems. Find them using the schema, before asking the AI:

```json
{"story_id": "US-205", "status": "done", "test_cases": [
 {"id": "TC-1", "title": "SAVE10 on exactly $50.00", "ac_ids": ["AC1"], "type": "boundary",
  "steps": ["Add items totalling $50.00", "Enter SAVE10", "Click Apply"], "expected_result": "Total is $45.00"},
 {"id": "TC-205-02", "title": "SAVE10 on $49.99", "ac_ids": ["AC2"], "type": "boundary",
  "steps": ["Add items totalling $49.99", "Enter SAVE10", "Click Apply"]}
], "open_questions": ["AC4: What message is shown when a second coupon is entered?"]}
```

A good method is to walk through the schema from top to bottom, asking one question per line: are all four required fields present? Does `story_id` match its pattern? Is `status` one of the two values? Then, for **each** test case in turn: are all six fields present? Does `id` match? Is `type` allowed?

Written out as a table, the walk-through for this reply looks like this:

| Question | First test case | Second test case |
|---|---|---|
| All six required fields present? | ✅ | ❌ no `expected_result` |
| `id` matches `^TC-[0-9]{3}-[0-9]{2}$`? | ❌ `TC-1` | ✅ `TC-205-02` |
| `type` is positive, negative or boundary? | ✅ | ✅ |

Above the test cases, the four top-level fields are all present, `story_id` matches its pattern, `open_questions` is a list, and `status` is ❌ `"done"`. One table, three crosses: the same three problems as the answer key below. Filling in a table like this takes a couple of minutes, and it is the best way to make sure an absence does not slip past you.

#### Step 3 (AI tool): Ask the AI to validate it

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

Replace the two `<paste ... here>` lines with the schema and the reply. The prompt uses three techniques from Tuesday: a precise task ("list every place"), a constraint ("only report schema problems") and delimiters around the two pieces of data.

#### Step 4 (Paper): Compare

Here is the answer key. This is exactly what a real schema validator reports:

| Where | Problem |
|---|---|
| `status` | `"done"` is not one of `"ok"`, `"needs_clarification"` |
| First test case, `id` | `"TC-1"` does not match the pattern `TC-` + 3 digits + `-` + 2 digits |
| Second test case | `expected_result` is **missing** (it is required) |

Mark your AI's answer: ✅ all three found; ✅ nothing extra reported; ❌ if it missed the missing `expected_result`. That miss is common, because people and AIs notice **wrong values** more easily than **missing** ones. A wrong value is visible on the page; a missing field is an absence, and absences are easy to read past.

Also check whether the AI reported anything that **is not** a schema problem, for example *"the expected result should mention the discount"*. That would mean it ignored the instruction "only report schema problems". It is the scope problem from *Agent Instructions*, in a different task.

### 6. What a Real Validator Prints

The handout says the answer key is what a real validator reports. We checked. Python has a widely used validator library called `jsonschema`. With it installed (`pip install jsonschema`), this short script, `validate.py`, checks a reply file against `schema.json` and lists every problem. You do not need to run it this week:

```python
import json
import sys
from jsonschema import Draft7Validator

schema = json.load(open("schema.json"))
reply = json.load(open(sys.argv[1]))
errors = sorted(Draft7Validator(schema).iter_errors(reply), key=lambda e: list(e.path))
for error in errors:
    where = "/".join(str(part) for part in error.path) or "(top level)"
    print(f"{where}: {error.message}")
print(f"{len(errors)} problem(s)")
```

Run on the Step 2 reply, it prints:

```text
status: 'done' is not one of ['ok', 'needs_clarification']
test_cases/0/id: 'TC-1' does not match '^TC-[0-9]{3}-[0-9]{2}$'
test_cases/1: 'expected_result' is a required property
3 problem(s)
```

We got the same result with two different versions of the library and of Python. Exactly the three problems in the answer key, nothing more.

**How to read the output:** the part before the colon is the **path** to the problem. `test_cases/0/id` means "inside `test_cases`, item number 0, the field `id`". Python counts from 0, so item 0 is the **first** test case and item 1 is the second. The missing field is reported at `test_cases/1`, the object it is missing **from**, because a missing field has no location of its own.

Compare the validator with the AI from Step 3. The validator is **deterministic**: the same reply always gives the same three lines. It never reports a non-schema problem, never misses a missing field, and never has a bad day. That is why, when an AI's check and a validator disagree about the schema, the validator wins. The AI is useful for **explaining** a schema or a problem; the validator is what you trust for the verdict.

### 7. A Schema Checks Shape, Not Meaning

The handout's third key idea: **a schema checks shape, not meaning.** `"expected_result": "Total is $99.00"` matches the schema even though it is wrong.

We tested this, too, by making small changes to a **valid** US-205 reply and running the validator on each:

| Change to a valid reply | Validator result | Is the reply actually OK? |
|---|---|---|
| None | 0 problems | ✅ Yes |
| `expected_result` changed to "Total is $99.00" | **0 problems** | ❌ Wrong value |
| `ac_ids` changed to `["AC9"]` (US-205 has no AC9) | **0 problems** | ❌ Invented requirement |
| An extra field `"mood": "happy"` added to a test case | **0 problems** | ❌ Not in the contract |
| `open_questions` changed to `[]` | 0 problems | ✅ Yes: empty is allowed |
| `open_questions` removed | 1 problem: `'open_questions' is a required property` | ❌ Broken |
| `open_questions` changed to `"none"` | 1 problem: `'none' is not of type 'array'` | ❌ Broken |
| Second test case's `type` changed to `"edge"` | 1 problem: `'edge' is not one of [...]` | ❌ Broken |

Read the top half carefully. A wrong amount, an **invented AC** and an unknown extra field all pass with **zero problems**. Each is a real defect, and the schema cannot see any of them:

- **The wrong amount** is a meaning problem: the schema knows `expected_result` must be present, not what it should say.
- **The invented AC9** needs the **story** to detect: the schema only sees the reply, so it cannot know which AC ids exist.
- **The extra field** passes because this schema does not forbid extra fields (section 8).

The bottom half shows what the schema is good at: missing fields, wrong types and values outside a fixed list. Those are exactly the mechanical mistakes that are easy to miss by eye.

So a schema is a **first filter**, not a final verdict. It removes broken replies quickly and reliably, leaving the replies that are **well-formed** for the checks that need the story and the checks that need a person.

### 8. What Our Schema Does Not Say

Read the schema once more, looking for what is **not** there:

- **Four test case fields have no rules at all.** `title`, `ac_ids`, `steps` and `expected_result` are required, but nothing says what kind of value they hold. `"steps": 42` would pass. A fuller schema would add `{"type": "array"}` for `steps` and `ac_ids`, and `{"type": "string"}` for the others.
- **Extra fields are allowed.** By default, JSON Schema accepts fields the schema does not mention. That is why `"mood": "happy"` passed.
- **Nothing limits the number of test cases.** A schema can limit a list's length with `maxItems`, but our limit is `max_cases`, which is different for every story. The schema only sees the reply, so it cannot know the story's limit.

The second point has a well-known fix, `"additionalProperties": false`, which tells the validator to reject fields that are not listed. But it comes with a trap, and we hit it while testing. Adding it to our test case rules, as they are, made the validator reject **every** test case, including valid ones:

```text
Additional properties are not allowed ('ac_ids', 'expected_result', 'mood', 'steps', 'title' were unexpected)
```

Why? `additionalProperties: false` means "only the fields listed in `properties` are allowed". Our schema lists only `id` and `type` there. So `title`, `ac_ids`, `steps` and `expected_result` count as **extra**, even though `required` demands them. To use it safely, every allowed field must appear under `properties`. It is a good example of a rule that looks simple and has a surprising effect, which is exactly why schema changes should be tested on known good and bad replies, like any code.

The third point is the most important for tomorrow. Some rules **cannot** be written in a schema at all, because they compare the reply with the story: the number of test cases against `max_cases`, the `ac_ids` against the story's ACs, the `story_id` against the input. *Required Fields and Validation Rules*, next, writes those rules down in plain English.

### 9. A Second Schema: the Input Side

The handout's schema describes the **output**. The same keywords can describe the **input** side of the contract: the story files. Here is a schema for them, written for this lesson so you can see a few more keywords:

```json
{
  "type": "object",
  "required": ["story_id", "title", "acceptance_criteria", "max_cases"],
  "properties": {
    "story_id": {"type": "string", "pattern": "^US-[0-9]{3}$"},
    "title": {"type": "string"},
    "acceptance_criteria": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "text"],
        "properties": {
          "id": {"type": "string", "pattern": "^AC[0-9]+$"},
          "text": {"type": "string"}
        }
      }
    },
    "max_cases": {"type": "integer", "minimum": 1}
  }
}
```

Three new keywords appear, each matching a rule from the input table in `contract.md`:

| Keyword | Meaning here | Contract rule |
|---|---|---|
| `minItems: 1` | The list must have at least one item | "At least 1" acceptance criterion |
| `"type": "integer"` | A whole number, not text and not a decimal | `max_cases` is a number |
| `minimum: 1` | The number must be 1 or more | A story must allow at least one test case |

We ran it against the three story files from *Input/Output Contracts*: all three passed with **0 problems**. Then we tried a broken story, with an empty criteria list and `"max_cases": "3"` written as text. The validator reported both:

```text
acceptance_criteria : [] should be non-empty
max_cases : '3' is not of type 'integer'
```

On an older version of the library, the first message reads `[] is too short` instead. The wording changes; the finding does not. That is worth remembering whenever you compare tool output with a lesson: read for **what** is reported, not the exact words.

Notice the pattern for AC ids: `^AC[0-9]+$`. The `+` means "one or more digits", so `AC1` and `AC12` both match, but `AC` alone or `ac1` do not. This one pattern, applied to every story file, guarantees the ids that the agent's replies will refer to are written consistently.

### 10. Schemas and AI Providers

Structured Outputs, which you met on Tuesday, changes where the schema is used. Instead of checking a reply **after** it arrives, the developer gives the schema to the AI provider **with** the request, and the model's reply is made to follow it.

That removes most **shape** problems: no missing fields, no `"done"` status, no text around the JSON. It is a real improvement, and teams that build agents with code often use it.

But look again at the table in section 7. The wrong amount, the invented AC9 and, unless the schema forbids it, the extra field all **matched the schema**. A provider enforcing the schema would accept them too. Structured Outputs moves shape checking earlier; it does not touch meaning. The rules that compare the reply with the story, and the human review, are still needed. This week, with replies pasted by hand, the schema is used the classic way: as a check after the reply is saved.

### 11. A Checklist for Reading Any Schema

You will meet other schemas: in API documentation, in tools, in other agents. The same questions work for all of them:

1. **What is the top-level type?** Usually an object.
2. **What is required?** Read every `required` list, at every level.
3. **What are the allowed values?** Look for `enum` and `pattern`, and read each pattern piece by piece.
4. **What is inside each list?** Find `items` and repeat questions 1 to 3 for it.
5. **What is not said?** Fields with no rules, extra fields, missing limits.

The fifth question is the tester's question. A schema tells you what will be **rejected**. Everything it does not mention will be **accepted**, and that is where the surprises live.

### 12. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| The AI "fixes" the reply instead of listing problems | It drifted from the task | Re-ask: "Do not rewrite it. Only list the problems." |
| The AI reports a problem that is not one | AIs can be wrong when checking, too | Check each claim against the schema yourself, or with a validator |
| The AI misses the missing field | Absences are harder to notice than wrong values | Walk through every `required` list, field by field |
| You confuse the field `type` with the keyword `type` | Same word, two meanings | Inside `properties`, a name is a field; elsewhere, `type` is a keyword |
| A pattern rejects a value you think is fine | Patterns are exact: `^` and `$` mean the whole text must match | Read the pattern piece by piece and test it on the value |
| A schema change rejects valid replies | For example, `additionalProperties: false` without listing every field | Test every schema change on a known good reply first |

---

## Practice Exercises

1. **Which keyword? (paper, 5 min).** In the Step 2 reply, change `"type": "boundary"` in the second test case to `"type": "edge"`. Which schema keyword catches it? How many problems would a validator now report?

2. **A valid reply (AI tool, 10 min).** Follow this week's four steps:
   - **Prompt:** run the Step 3 prompt with the **valid** sample reply from *Agent Instructions*.
   - **Review:** does the AI correctly say there are **no** problems?
   - **Run:** if it reports a problem, check it against the schema line by line.
   - **Record:** in `prompts.txt`, note whether the AI invented a problem.

3. **Explain the schema (AI tool, 10 min).** Ask your AI: *"Explain this JSON Schema line by line for a beginner."* and paste the schema. Did it explain `required` and `enum` correctly? Did it notice that the second `type` is a field name?

4. **Predict, then improve (paper, 15 min).** Add `"steps": {"type": "array"}` and `"ac_ids": {"type": "array"}` under the test case `properties`. For each of these test case values, predict whether the reply now passes: (a) `"steps": "Click Apply"`; (b) `"ac_ids": []`; (c) `"ac_ids": ["AC9"]`. Which ones still pass, and is each of those actually correct?

5. **Validate a story (paper, 10 min).** Using the input schema in section 9, check `stories/US-313.json` from *Input/Output Contracts* (exercise 2) by hand. Then write a broken version that the schema rejects for **two** different reasons, and say which keyword catches each.

---

## Knowledge Check

1. What is JSON Schema, and how does it relate to the contract?

<details><summary>Answer</summary>

A standard, machine-readable way to describe valid JSON. It is the contract's output table written so a computer can check replies against it.

</details>

2. What does the keyword `enum` do?

<details><summary>Answer</summary>

It lists the only values allowed, for example `"ok"` or `"needs_clarification"`. Values are compared exactly, so `"OK"` is not allowed.

</details>

3. Does `"US-2050"` match `^US-[0-9]{3}$`? Why?

<details><summary>Answer</summary>

No. The pattern needs exactly three digits between `US-` and the end of the text; `US-2050` has four.

</details>

4. What are the three schema problems in the Step 2 reply, and which is most often missed?

<details><summary>Answer</summary>

`status` is "done"; the first test case's `id` is "TC-1"; the second test case is missing `expected_result`. The missing field is most often missed.

</details>

5. A validator reports `test_cases/1: 'expected_result' is a required property`. Which test case is it about?

<details><summary>Answer</summary>

The second one. Paths count from 0, so item 1 is the second test case.

</details>

6. A reply has `"ac_ids": ["AC9"]` for US-205. Why does the schema not catch it?

<details><summary>Answer</summary>

The schema only sees the reply. Knowing which AC ids exist needs the story, so this needs a validation rule that compares the reply with the story.

</details>

7. Why did adding `"additionalProperties": false` make valid test cases fail?

<details><summary>Answer</summary>

It allows only the fields listed under `properties`, and our schema lists only `id` and `type` there. Every other required field counted as extra.

</details>

8. When an AI's schema check and a validator disagree, which do you trust, and why?

<details><summary>Answer</summary>

The validator. It is deterministic and applies the schema exactly. The AI is useful for explaining, but can miss or invent problems.

</details>

9. If an AI provider enforces your schema with Structured Outputs, do you still need validation rules and human review? Why?

<details><summary>Answer</summary>

Yes. Enforcing the schema removes shape problems, but replies with wrong amounts or invented AC ids still match the schema. Those need rules that compare the reply with the story, and a person.

</details>

---

## Glossary

- **JSON Schema:** a standard, machine-readable description of valid JSON, written in JSON.
- **Validator:** a tool that checks JSON against a schema and reports every mismatch.
- **Property:** a named field in a JSON object.
- **Array:** JSON's name for a list.
- **`type`:** the keyword for what kind of value is allowed.
- **`required`:** the keyword listing fields that must be present.
- **`properties`:** the keyword holding the rules for each named field.
- **`enum`:** the keyword listing the only allowed values.
- **`pattern`:** the keyword giving a regular expression that text must match.
- **`items`:** the keyword giving the rules for every item in a list.
- **`additionalProperties`:** the keyword controlling whether fields not listed in `properties` are allowed.
- **`minItems`:** the keyword setting the smallest allowed length of a list.
- **`minimum`:** the keyword setting the smallest allowed number.
- **`integer`:** a whole number, such as 3; a type that rejects text such as "3".
- **Path (in validator output):** the location of a problem, such as `test_cases/0/id`.
- **Well-formed:** matching the required shape, whether or not the content is correct.

---

## Summary

- **JSON Schema** is the contract in machine-readable form, and **validators** check replies against it automatically.
- Read a schema by following its **nesting**: the reply object, then each test case inside `items`.
- Walk the `required` lists field by field. **Missing fields** are the problem people and AIs most often miss.
- A real validator reported exactly the three handout problems. It is **deterministic**, so its verdict beats an AI's.
- **A schema checks shape, not meaning.** A wrong amount, an invented AC and an extra field all passed. Rules that need the **story** come next.

---

## Additional Resources

- JSON Schema, *Creating your first schema*: https://json-schema.org/learn/getting-started-step-by-step
- JSON Schema, *Understanding JSON Schema: the basics*: https://json-schema.org/understanding-json-schema/basics
- OpenAI, *Structured Outputs*: https://developers.openai.com/api/docs/guides/structured-outputs
