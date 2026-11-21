# Required Fields and Validation Rules

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the difference between a **required**, **optional**, **nullable** and **defaulted** field, and why "missing", "empty" and "null" are three different things.
- Decide, field by field, whether a field in an agent contract should be required, using three questions: **who consumes it, can they work without it, and is there a safe default?**
- Classify validation rules into five categories: **structural**, **field-level**, **cross-field (conditional)**, **cross-document (semantic)** and **business/quality** rules.
- Express a conditional rule in JSON Schema with **`if` / `then`** and **`dependentRequired`**, and test it with Python's `jsonschema` library.
- Recognise rules that a schema **cannot** express, and write a tiny Python check for one of them.
- Build a **rule catalogue** that records each rule's ID, layer (schema, code or human), severity (error or warning), an example violation and its error message.
- Write **good validation error messages** that say what failed, where, what was expected, what was found, and how to fix it.
- Choose between **strict and lenient** validation, and between **fail fast** and **collect all errors**.

---

## Why This Matters

Earlier today you met the **TestCaseDesigner** agent, its **input/output contract**, and the **JSON Schema** language that writes that contract down in a form a computer can check. A schema is only as useful as the decisions inside it. Two of the most important decisions are:

1. **Which fields must always be there?** (required fields)
2. **What makes a value acceptable?** (validation rules)

Get these wrong and the agent hurts you quietly. Too few required fields and the code reading the output crashes on a missing key in CI. Too many and the agent is forced to invent values to fill them, the "confident filler" you learned to distrust on Wednesday. Vague rules let "Expected result: it works" slip into the suite.

This lesson is the bridge between *describing* a contract (this morning) and *enforcing* it (Friday). It connects directly to the **Weekly Epic**: you are designing the IO contract and validation rules for your first QA agent. It also feeds **Project 2 (Test Automation Framework)**: any agent that generates test cases for the e-commerce app will need a clear list of what "valid output" means before its output is allowed anywhere near your pytest suite.

Think of a passport office: some boxes are required, some optional, and each has rules. A machine checks some rules, a clerk compares the form with your birth certificate, and an officer judges the photo. Agent validation works the same way, and today you learn which check belongs where.

> **Scope note.** Today is about **designing** required fields and validation rules: deciding them, writing them down and seeing a few of them run. You will run small `jsonschema` checks and two tiny rule functions. The **full validation script** that loads an agent's output, applies the schema plus all the extra rules and prints a report, and the **agent output validation** workflow around it, are built on **Friday** (*Agent output validation* and *Building validation scripts*). Retrying a model when its output is invalid is covered in **Week 9**.

---

## The Concept

### 1. A Quick Recap: The TestCaseDesigner Contract

In the JSON Schema lesson you learned the core keywords (`type`, `properties`, `required`, `additionalProperties`, `enum`, `const`, `pattern`, `minLength`, `minimum`, `maximum`, `minItems`, `uniqueItems`, `$defs`, `$ref`). We will not re-teach them; we will use them.

Here is a reminder of the two contracts, as short excerpts. The **input** is one user story (`us205_input.json`: US-205 with AC1 to AC4, `techniques` `["EP", "BVA"]`, `max_cases` 6).

The input schema (excerpt) says:

```json
"required": ["story_id", "title", "acceptance_criteria"],
"additionalProperties": false
```

So `techniques` and `max_cases` are optional, and `max_cases` has `"default": 10` with a range of 1 to 20.

The **output** schema (excerpt) says:

```json
"required": ["contract_version", "story_id", "status", "test_cases", "open_questions"],
"additionalProperties": false
```

and each test case requires `id`, `title`, `ac_ids`, `type`, `priority`, `steps` and `expected_result`, while `preconditions` is optional.

Why those choices? That is the first half of this lesson.

> **Setup.** The examples need `jsonschema` version 4 or later (for `Draft202012Validator`). Install it with `pip install "jsonschema>=4.18"`. Some machines still have the old 3.2 release, which does not support Draft 2020-12; check with `python -c "import jsonschema; print(jsonschema.__version__)"`. The examples load `tcd_input.schema.json`, `tcd_output.schema.json`, `us205_input.json` and `us205_output.json` from the current folder; these are the contract files from earlier today.

---

### 2. Four Kinds of Field: Required, Optional, Nullable, Defaulted

Every field in a contract falls into one (or a combination) of these kinds.

| Kind | Meaning | How you write it in JSON Schema | TestCaseDesigner example |
|---|---|---|---|
| **Required** | The key must be present. | List it in `"required"`. | `story_id`, `status`, `open_questions` |
| **Optional** | The key may be left out entirely. | Define it in `"properties"` but do **not** list it in `"required"`. | `preconditions`, `techniques` |
| **Nullable** | The key may be present with the value `null`. | Allow the null type: `"type": ["string", "null"]`. | None in v1.0.0 (see below) |
| **Defaulted** | If the key is missing, the consumer uses a documented value. | Optional field plus `"default": ...` (and code that applies it). | `max_cases` (default 10) |

Two points trip up almost every beginner.

**Point 1: "required" says nothing about the value.** `"required": ["open_questions"]` only means the key must exist. The *value* is checked by the property's own rules. So an empty array `[]` satisfies `required`, and whether `[]` is acceptable depends on rules such as `minItems`.

**Point 2: `default` is only a note.** In JSON Schema, `default` is an **annotation**: documentation for humans and tools. The `jsonschema` library does **not** fill in missing values for you. If the input arrives without `max_cases`, your Python code must apply the default itself:

```python
max_cases = story.get("max_cases", 10)   # the schema documents 10; the code applies it
```

If you forget this, the "default" exists only on paper.

#### Why TestCaseDesigner has no nullable fields

`null` means "this key exists, but there is no value". It is useful when you need to tell apart "we checked and there is nothing" from "we did not check". For example, a hypothetical `defect_id` field could be `null` for "no defect raised yet".

For TestCaseDesigner we chose a simpler rule: **lists are never null; an empty list means "none"**. Code that reads the output can then always write `for q in output["open_questions"]:` without first checking for `None`. This is a common, good design habit: prefer an empty collection over `null` for lists, and only use `null` when "unknown" really means something different from "none".

---

### 3. Missing vs Empty vs Null

These three states look similar to a human reading quickly, but they are different to a computer, and they usually mean different things.

| State | JSON | Plain meaning | Typical cause in agent output |
|---|---|---|---|
| **Missing** | `{}` (key absent) | "Nobody said anything." | The model forgot the field, or the prompt never asked for it. |
| **Empty** | `{"open_questions": []}` or `""` | "I looked, and there is nothing." | The agent had no questions. |
| **Null** | `{"open_questions": null}` | "There is a value slot, but it holds nothing." | The model was unsure and wrote `null`. |

Here is why the difference matters for TestCaseDesigner. Suppose the output has no `open_questions` key. Did the agent decide there were no questions, or did it simply forget the field, maybe because its answer was cut off? You cannot tell. By making `open_questions` **required** but allowing it to be **empty**, the agent must say explicitly "I have no questions" by writing `[]`. Silence is no longer ambiguous.

Let us see `jsonschema` treat the three states differently. This small schema mirrors the decisions above: `open_questions` is required, `preconditions` is optional, and a made-up `notes` field is nullable so you can see that case too.

```python
# missing_empty_null.py
from jsonschema import Draft202012Validator

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "open_questions": {"type": "array", "items": {"type": "string"}},
        "preconditions": {"type": "array", "items": {"type": "string"}},
        "notes": {"type": ["string", "null"]},
    },
    "required": ["open_questions"],
}
validator = Draft202012Validator(schema)

samples = {
    "A all present":            {"open_questions": [], "preconditions": [], "notes": None},
    "B preconditions missing":  {"open_questions": []},
    "C open_questions missing": {"preconditions": ["Cart subtotal is $50.00"]},
    "D open_questions null":    {"open_questions": None},
    "E notes null":             {"open_questions": [], "notes": None},
}
for name, doc in samples.items():
    errors = [e.message for e in validator.iter_errors(doc)]
    print(f"{name:26} -> {'VALID' if not errors else errors}")
```

Output:

```text
A all present              -> VALID
B preconditions missing    -> VALID
C open_questions missing   -> ["'open_questions' is a required property"]
D open_questions null      -> ["None is not of type 'array'"]
E notes null               -> VALID
```

Walk through it line by line:

- `Draft202012Validator(schema)` creates a validator that understands JSON Schema Draft 2020-12.
- `validator.iter_errors(doc)` returns **every** error it finds (an empty sequence if the document is valid). We turn each error into its `.message`.
- **A** and **B** pass: an empty `open_questions` list satisfies `required`, and leaving out the optional `preconditions` is fine.
- **C** fails on the `required` rule: the key is missing.
- **D** fails for a different reason: the key is present, so `required` is happy, but `null` (Python `None`) is not an array.
- **E** passes because `notes` explicitly allows `null`.

Notice that C and D fail with **different** messages. When you read a failure report on Friday, these messages tell you whether the model forgot a field or filled it badly, which point to different prompt fixes.

---

### 4. Deciding Which Fields Are Required

Making a field required is a promise from the **producer** (the agent) to the **consumer** (whatever reads the output: your code, a reviewer, a test management tool). Ask three questions for each field:

1. **Who consumes it?** Name the code or person that reads this field.
2. **Can the consumer do its job without it?** If not, it must be required.
3. **Is there a safe default?** If the field is missing and a safe, documented value exists, it can be optional (with a default). If no safe default exists, make it required.

A fourth, AI-specific question is worth adding:

4. **Can the agent always produce it honestly?** If you require a field that the source story does not support (for example `test_data_owner` when stories never name an owner), the model will **invent** a value to satisfy the schema. Requiring a field the agent cannot honestly fill encourages hallucinated filler.

#### Applying the questions to the output contract

| Field | Consumer | Works without it? | Safe default? | Decision |
|---|---|---|---|---|
| `contract_version` | Validation code, future versions | No: you cannot know which rules apply | No | **Required** (and `const "1.0.0"`) |
| `story_id` | Traceability, reports | No: cannot link tests to the story | No | **Required** |
| `status` | Code that decides what to do next | No: it drives branching | No: guessing "ok" would hide problems | **Required** |
| `test_cases` | pytest generation, reviewers | No | `[]` is honest only with `needs_clarification` | **Required** (may be empty only in that case; see R6) |
| `open_questions` | Business analyst, reviewer | Ambiguous if missing (see Section 3) | `[]` | **Required**, may be empty |
| test case `id` | Test management tool, logs | No | No | **Required** |
| test case `ac_ids` | Coverage and traceability checks | No | No | **Required**, at least one |
| test case `type`, `priority` | Run ordering, coverage review | Poorly | No sensible guess | **Required** |
| test case `steps`, `expected_result` | Tester or automation | No: a test without an oracle is not a test | No | **Required** |
| test case `preconditions` | Tester setting up | **Yes**: many tests need no special setup | Missing means "no special setup" | **Optional** |

Why is `preconditions` optional but `open_questions` required, when both are lists that are often empty? Because of what "missing" would mean:

- A missing `preconditions` has one obvious meaning: "no special setup". Nobody is misled.
- A missing `open_questions` has two possible meanings ("no questions" or "forgot"), and the wrong reading could hide an ambiguity in the requirement, such as AC4's unanswered "replace or reject a second coupon?". Requiring the key forces the agent to commit.

#### Applying the questions to the input contract

| Field | Decision | Reason |
|---|---|---|
| `story_id`, `title`, `acceptance_criteria` | **Required** | The agent cannot design tests without the story; `story_id` is needed for R1 and R4. |
| `techniques` | **Optional** | If not given, the agent chooses suitable techniques itself (as you did by hand on Tuesday). |
| `max_cases` | **Optional, default 10** | A safe, documented limit exists. |

A useful rule of thumb: **be generous with required fields on the output side and economical on the input side.**

---

### 5. Five Categories of Validation Rule

"Valid" is not one check; it is a stack of checks of increasing depth.

| # | Category | Question it answers | Example for TestCaseDesigner | Where it can live |
|---|---|---|---|---|
| 1 | **Structural** (syntactic) | Is it the right shape and type? | Output is valid JSON; `test_cases` is an array of objects; no unknown keys. | JSON Schema |
| 2 | **Field-level** | Is each single value acceptable? | `id` matches `^TC-[0-9]{3}-[0-9]{2}$`; `priority` is high/medium/low; `max_cases` is 1 to 20. | JSON Schema |
| 3 | **Cross-field** (conditional) | Do fields **within one document** agree? | If `status` is `needs_clarification`, `open_questions` must not be empty (R6). | JSON Schema (`if`/`then`, `dependentRequired`) |
| 4 | **Cross-document** (semantic) | Does the output agree with the **input**? | Every `ac_ids` entry exists in the input story (R2). | Code |
| 5 | **Business / quality** | Is it actually a *good* answer? | If BVA was requested, at least one boundary case exists; the expected result is concrete. | Code (partly) + human review |

The deeper you go, the less a schema can do on its own. Categories 1 to 3 can be written in JSON Schema. Category 4 needs a program that can see both the input and the output. Category 5 can be partly automated, but the final judgement often needs a human, using the review checklist from Wednesday's *Human validation of AI output*.

We will look at categories 3, 4 and 5 in detail, since categories 1 and 2 were the heart of the JSON Schema lesson.

---

### 6. Cross-Field Rules in JSON Schema: `if` / `then` and `dependentRequired`

#### 6.1 The rule we want: R6

Our semantic rule **R6** says:

- **R6:** status `"needs_clarification"` requires a non-empty `open_questions`; status `"ok"` requires at least one test case.

In plain words: if the agent says "I need clarification", it must say **what** it needs clarified; and if it says "ok", it must actually deliver tests. Both halves stop the agent from giving an empty, useless answer that still looks valid.

Notice that this is a rule *between two fields of the same document*. The schema keywords you already know check fields one at a time, so we need conditional keywords.

#### 6.2 How `if` / `then` works

```json
{
  "if":   { ...a schema used as a test... },
  "then": { ...a schema applied only when the test passes... }
}
```

The validator checks the document against `if`. If the document **matches** `if`, it must also match `then`. If it does not match `if`, `then` is ignored. (There is also an optional `else`, applied when `if` does not match.) Important detail: the `if` schema produces no errors itself; it is only a question.

Because R6 has two conditions, we place two `if`/`then` pairs inside `allOf`, which means "the document must satisfy all of these".

```python
# r6_if_then.py
from jsonschema import Draft202012Validator

r6_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "status": {"enum": ["ok", "needs_clarification"]},
        "test_cases": {"type": "array"},
        "open_questions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["status", "test_cases", "open_questions"],
    "allOf": [
        {   # R6a: needs_clarification -> at least one open question
            "if":   {"properties": {"status": {"const": "needs_clarification"}}},
            "then": {"properties": {"open_questions": {"minItems": 1}}},
        },
        {   # R6b: ok -> at least one test case
            "if":   {"properties": {"status": {"const": "ok"}}},
            "then": {"properties": {"test_cases": {"minItems": 1}}},
        },
    ],
}
validator = Draft202012Validator(r6_schema)

cases = {
    "ok with 1 test case":            {"status": "ok", "test_cases": [{}], "open_questions": []},
    "ok with 0 test cases":           {"status": "ok", "test_cases": [], "open_questions": []},
    "clarification with question":    {"status": "needs_clarification", "test_cases": [],
                                       "open_questions": ["AC4: replace or reject a second coupon?"]},
    "clarification with no question": {"status": "needs_clarification", "test_cases": [], "open_questions": []},
}
for name, doc in cases.items():
    errors = [f"{list(e.absolute_path)}: {e.message}" for e in validator.iter_errors(doc)]
    print(f"{name:31} -> {'VALID' if not errors else errors}")
```

Output:

```text
ok with 1 test case             -> VALID
ok with 0 test cases            -> ["['test_cases']: [] should be non-empty"]
clarification with question     -> VALID
clarification with no question  -> ["['open_questions']: [] should be non-empty"]
```

Key points in the code:

- The `if` part uses `const` to ask "is `status` exactly this value?".
- The `then` part only adds `minItems: 1` to one property. The rest of that property's rules (it must be an array) still come from the main `properties`.
- `e.absolute_path` tells us **where** in the document the error is, here `['test_cases']` or `['open_questions']`. You will use this for good error messages in Section 9.
- The test case object `{}` in the first sample is deliberately minimal. This schema only checks R6; in the real output schema, each test case is checked by `$defs/test_case`.

This is a small example of a powerful idea: **test your rules with both valid and invalid samples.** A rule you have only seen pass is a rule you have not tested. (You will recognise this from boundary value analysis: test both sides of the line.)

> **Design note.** The canonical TestCaseDesigner v1.0.0 output schema you saw this morning keeps R6 out of the schema and lists it as a semantic rule. Both choices are legitimate. Putting R6 in the schema means any JSON Schema tool enforces it; keeping it in code keeps the schema short and lets you write a friendlier message. What matters is that the rule catalogue (Section 8) records **where** each rule lives, so nobody checks it twice or not at all.

#### 6.3 `dependentRequired`: "if this key is present, that key must be too"

`dependentRequired` is a shorter way to express one common conditional: *the presence of one key requires other keys*. TestCaseDesigner v1.0.0 does not need it, so here is a **hypothetical** example. Imagine a future version where a test case may carry `test_data`; whenever it does, reviewers must know where the data came from (`data_source`), because production copies need privacy checks (Wednesday's *Responsible use of AI in QE*).

```python
# dependent_required.py  (hypothetical field, NOT part of TestCaseDesigner v1.0.0)
from jsonschema import Draft202012Validator

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "test_data": {"type": "object"},
        "data_source": {"enum": ["fixture", "generated", "production_copy"]},
    },
    "dependentRequired": {"test_data": ["data_source"]},
}
validator = Draft202012Validator(schema)

for doc in [
    {},                                                         # neither field
    {"test_data": {"subtotal": 50.00}, "data_source": "fixture"},
    {"test_data": {"subtotal": 50.00}},                         # data but no source
]:
    errors = [e.message for e in validator.iter_errors(doc)]
    print(f"{str(doc):58} -> {'VALID' if not errors else errors}")
```

Output:

```text
{}                                                         -> VALID
{'test_data': {'subtotal': 50.0}, 'data_source': 'fixture'} -> VALID
{'test_data': {'subtotal': 50.0}}                          -> ["'data_source' is a dependency of 'test_data'"]
```

Read `"dependentRequired": {"test_data": ["data_source"]}` as: "if `test_data` is present, `data_source` is required." It is one-directional: `data_source` alone does not require `test_data`. (Python prints `50.00` as `50.0`; that is just how floats are displayed.)

When to use which:

- Use **`dependentRequired`** when the condition is simply "key X is present".
- Use **`if` / `then`** when the condition depends on a **value** (such as `status == "ok"`), or when the consequence is more than "these keys must exist".

---

### 7. Cross-Document Rules: What a Schema Cannot See

A JSON Schema validates **one document at a time**. It has no idea what the input story said. That is a fundamental limit, and it is why rules R1 to R5 cannot be written into the output schema:

| Rule | Why the output schema alone cannot check it |
|---|---|
| **R1** output `story_id` equals input `story_id` | The schema can check the *format* `US-205`, but not that it is the *same* story you sent. |
| **R2** every `ac_ids` entry exists in the input | The schema can check `AC5` *looks* like an AC id, not that the story *has* an AC5. |
| **R3** every input AC is covered by a test case (or appears in `open_questions`) | Needs the list of input ACs. |
| **R4** test case ids unique and their middle part matches the story number | `uniqueItems` compares whole objects, not one field; and the story number comes from the input. |
| **R5** number of test cases `<=` `max_cases` (default 10) | `max_cases` is in the input, and may come from the default. |

These are exactly the mistakes language models make: an AI may invent an `AC5` that does not exist (a traceability error you met in Wednesday's lessons), or copy the id pattern from an example for another story (`TC-101-03` in a US-205 answer). Such output is **schema-valid but wrong**. That is the most dangerous kind, because it passes the first automated gate.

Let us see two of these rules in action. The following output is valid against the output schema (we confirmed that `iter_errors` returns no errors for an equivalent full document), yet it breaks R2 and R4. To keep the example short, each test case below shows only the two fields the rules need.

```python
# cross_doc_rules.py
def check_r2(story_input: dict, output: dict) -> list[str]:
    """R2: every ac_ids entry must exist in the input acceptance criteria."""
    known = {ac["id"] for ac in story_input["acceptance_criteria"]}
    problems = []
    for i, tc in enumerate(output["test_cases"]):
        for ac_id in tc["ac_ids"]:
            if ac_id not in known:
                problems.append(
                    f"R2 ERROR at test_cases[{i}].ac_ids: '{ac_id}' is not an "
                    f"acceptance criterion of {story_input['story_id']} "
                    f"(expected one of {sorted(known)})."
                )
    return problems

def check_r4(story_input: dict, output: dict) -> list[str]:
    """R4: test case ids are unique and use the story number (US-205 -> TC-205-NN)."""
    story_number = story_input["story_id"].split("-")[1]          # "205"
    problems, seen = [], set()
    for i, tc in enumerate(output["test_cases"]):
        tc_id = tc["id"]
        if tc_id in seen:
            problems.append(f"R4 ERROR at test_cases[{i}].id: '{tc_id}' is used more than once.")
        seen.add(tc_id)
        middle = tc_id.split("-")[1]                              # "TC-205-01" -> "205"
        if middle != story_number:
            problems.append(
                f"R4 ERROR at test_cases[{i}].id: '{tc_id}' should start with "
                f"'TC-{story_number}-' because the story is {story_input['story_id']}."
            )
    return problems

story_input = {
    "story_id": "US-205",
    "title": "Apply coupon at checkout",
    "acceptance_criteria": [{"id": f"AC{n}", "text": "..."} for n in range(1, 5)],
}
# Planted-bad output: it is VALID against the output schema, but breaks R2 and R4.
bad_output = {
    "contract_version": "1.0.0", "story_id": "US-205", "status": "ok", "open_questions": [],
    "test_cases": [
        {"id": "TC-205-01", "ac_ids": ["AC1"]},
        {"id": "TC-205-01", "ac_ids": ["AC5"]},
        {"id": "TC-101-03", "ac_ids": ["AC3"]},
    ],
}
for problem in check_r2(story_input, bad_output) + check_r4(story_input, bad_output):
    print(problem)
```

Output:

```text
R2 ERROR at test_cases[1].ac_ids: 'AC5' is not an acceptance criterion of US-205 (expected one of ['AC1', 'AC2', 'AC3', 'AC4']).
R4 ERROR at test_cases[1].id: 'TC-205-01' is used more than once.
R4 ERROR at test_cases[2].id: 'TC-101-03' should start with 'TC-205-' because the story is US-205.
```

How the code works:

- Each rule is a **small, pure function**: it takes the input and the output, and returns a list of problem messages. An empty list means the rule passed. Small functions like this are easy to unit-test with pytest, just like any other code.
- `check_r2` builds a **set** of known AC ids from the input (`{"AC1", "AC2", "AC3", "AC4"}`), then checks each `ac_ids` entry with `in`. Sets make membership checks fast and clear.
- `check_r4` keeps a `seen` set to detect duplicates, and uses `str.split("-")` to pull the middle number out of both the story id and each test case id. This is safe here **only because** the schema has already guaranteed the formats `^US-[0-9]{3}$` and `^TC-[0-9]{3}-[0-9]{2}$`. That is an important design idea: **run the schema first, then the code rules**, so the code can trust the shape of the data and stay simple.
- `enumerate` gives the index `i`, so each message points to an exact location.

R1, R3 and R5 follow the same pattern and are left for the practice exercises. Combining the schema check and all of these functions into one script that produces a single pass/fail report is Friday's work in *Building validation scripts*.

---

### 8. Business and Quality Rules

Even if the output passes the schema and R1 to R6, it can still be a poor answer. Business and quality rules capture "good", not just "well-formed". For TestCaseDesigner we will label them **Q1 to Q3** so they are not confused with the contract rules R1 to R6:

- **Q1: If the input requests BVA, at least one test case has `type` `"boundary"`.** Automatable in code. US-205 has a clear boundary at $50.00, so an answer with no boundary case ignored the request.
- **Q2: `expected_result` must be concrete and observable.** Partly automatable: code can flag vague phrases such as "works correctly", "as expected" or "should be fine", and missing numbers or messages. But only a human can confirm that "Total is $45.00" is the *right* concrete result.
- **Q3: Each expected result agrees with the acceptance criterion it traces to.** Human review. For example, a test at exactly $50.00 that expects "no discount" contradicts AC1 ("$50.00 or more"). This is the oracle check from Wednesday's review checklist.

Quality rules are usually **warnings**, not errors, because automated checks for them produce false positives (a legitimate expected result might contain the word "correctly"). The next section shows how to record this.

---

### 9. The Rule Catalogue

A **rule catalogue** is a single table listing every rule the contract relies on. It is the "source of truth" a team reviews, and it tells Friday's validation script what to check. Each row records:

- **Rule ID**: a short, stable name (used in error messages and logs).
- **Description**: the rule in one sentence.
- **Layer**: where it is enforced: **input schema**, **output schema**, **code** or **human review**.
- **Severity**: **error** (output is rejected) or **warning** (output is accepted but flagged).
- **Example violation** and the **error message** it should produce.

| Rule ID | Description | Layer | Severity | Example violation | Error message |
|---|---|---|---|---|---|
| S1 | Output is a JSON object matching the output schema (types, required fields, patterns, enums, no extra keys). | Output schema | Error | `"priority": "urgent"` | `test_cases/0/priority: 'urgent' is not one of ['high', 'medium', 'low']` |
| S2 | Input matches the input schema. | Input schema | Error | `"story_id": "US205"` | `story_id: 'US205' does not match '^US-[0-9]{3}$'` |
| R1 | Output `story_id` equals input `story_id`. | Code | Error | Input US-205, output US-101 | `R1 ERROR at story_id: expected 'US-205' (from input), got 'US-101'.` |
| R2 | Every `ac_ids` entry exists in the input ACs. | Code | Error | `"ac_ids": ["AC5"]` | `R2 ERROR at test_cases[1].ac_ids: 'AC5' is not an acceptance criterion of US-205 ...` |
| R3 | Every input AC is covered by a test case or mentioned in `open_questions`. | Code | Error | No test or question for AC4 | `R3 ERROR: AC4 is not covered by any test case or open question.` |
| R4 | Test case ids are unique and match the story number. | Code | Error | `TC-101-03` in a US-205 answer | `R4 ERROR at test_cases[2].id: 'TC-101-03' should start with 'TC-205-' ...` |
| R5 | Number of test cases `<=` `max_cases` (default 10). | Code | Error | 8 cases when `max_cases` is 6 | `R5 ERROR at test_cases: 8 test cases returned, max_cases is 6.` |
| R6 | `needs_clarification` needs questions; `ok` needs test cases. | Code (or output schema with `if`/`then`) | Error | `"status": "ok", "test_cases": []` | `R6 ERROR at test_cases: status is 'ok' but no test cases were returned.` |
| Q1 | BVA requested ⇒ at least one `boundary` test case. | Code | Warning | `techniques` has BVA, no boundary case | `Q1 WARNING: BVA was requested but no test case has type 'boundary'.` |
| Q2 | `expected_result` is concrete (no vague phrases). | Code + human | Warning | `"expected_result": "Discount works as expected"` | `Q2 WARNING at test_cases[3].expected_result: vague phrase 'as expected'; state the exact total or message.` |
| Q3 | Expected result agrees with its AC. | Human | Error (at review) | $50.00 expects "no discount" | Recorded in the correction log (Wednesday). |

Look at the **Layer** column. It answers a question teams often forget to ask: *who is responsible for checking this?* Without the catalogue, a rule tends to be checked in two places (wasted effort, and the two checks drift apart) or in none (everyone assumes someone else checks it).

#### Where should each rule live? A decision guide

1. **Can JSON Schema express it using only the one document?** Put it in the schema. Schemas are declarative, shareable with other teams and tools, and often usable by model providers' structured-output features.
2. **Does it need the input, arithmetic across items, or external data?** Put it in code, as a small named function per rule.
3. **Does it need judgement about meaning or correctness?** Assign it to human review, and optionally add a code **warning** that points the reviewer at likely problems.

And one ordering principle: **cheapest and most certain first.** Schema checks run first; code rules run only on schema-valid output; humans look only at output that passed both.

---

### 10. Validate the Input Too: Reject Early, Save Money

So far we have focused on the agent's output. But the input deserves the same care, for three reasons:

- **Cost.** Every model call costs time and money. Sending a broken story to the model wastes a call that cannot possibly produce a good answer.
- **Garbage in, garbage out.** If `acceptance_criteria` is empty, the model has nothing to test, so it will invent requirements. Wednesday showed how convincing invented requirements can look.
- **Clear blame.** An input error is the caller's problem; an output error is the agent's problem. Separating them makes debugging much faster.

Like validating a web form before submitting it: **fail at the cheapest possible point.**

```python
# input_gate.py
import json
from jsonschema import Draft202012Validator

with open("tcd_input.schema.json") as f:
    input_validator = Draft202012Validator(json.load(f))

calls_made = 0

def fake_llm(prompt: str) -> str:
    """Deterministic stand-in for a model call. We only count calls here."""
    global calls_made
    calls_made += 1
    return '{"illustrative": true}'

def run_agent(story: dict):
    errors = sorted(input_validator.iter_errors(story), key=lambda e: list(e.absolute_path))
    if errors:
        print("REJECTED before calling the model:")
        for e in errors:
            where = "/".join(str(p) for p in e.absolute_path) or "(root)"
            print(f"  - at {where}: {e.message}")
        return None
    return fake_llm(json.dumps(story))

bad_story = {
    "story_id": "US205",
    "title": "Coupon",
    "acceptance_criteria": [],
    "max_cases": 50,
}
run_agent(bad_story)

with open("us205_input.json") as f:
    good_story = json.load(f)
print("Good story result:", run_agent(good_story))
print("Model calls made:", calls_made)
```

Output:

```text
REJECTED before calling the model:
  - at acceptance_criteria: [] should be non-empty
  - at max_cases: 50 is greater than the maximum of 20
  - at story_id: 'US205' does not match '^US-[0-9]{3}$'
Good story result: {"illustrative": true}
Model calls made: 1
```

What to notice:

- The bad story had **three** problems, and the caller learns about all three at once (we will discuss why in Section 12).
- We **sort** errors by their path so the report is in a stable order every run. Stable output makes reports easy to compare and test.
- `"/".join(...)` turns a path like `['acceptance_criteria']` into readable text; `(root)` is used when the error is about the whole document.
- `fake_llm` was called **once**, only for the good story. The `{"illustrative": true}` reply is a placeholder: in this lesson we only care whether the model was called. Wiring the input gate into a working agent is part of Friday's *Implementing IO contracts*.
- `title: "Coupon"` passed (6 characters; the schema demands 5). A schema checks what you wrote, not what you meant.

---

### 11. Writing Good Validation Error Messages

An error message is a tiny piece of documentation read by someone who is already having a bad day. Its job is to make the fix obvious. A good message answers five questions:

1. **Where?** The exact location (`test_cases/0/priority`).
2. **What?** Which rule failed (`enum`, or `R2`).
3. **Expected?** What would have been acceptable.
4. **Actual?** What was found.
5. **Fix?** What to do about it.

Compare:

| Weak message | Strong message |
|---|---|
| `Validation failed.` | `R5 ERROR at test_cases: 8 test cases returned, max_cases is 6. Reduce the number of test cases or raise max_cases.` |
| `Invalid id` | `R4 ERROR at test_cases[2].id: 'TC-101-03' should start with 'TC-205-' because the story is US-205.` |

The `jsonschema` library already gives you the raw ingredients on each error object:

- `error.message`: a default human-readable message.
- `error.absolute_path`: where in the document the error is.
- `error.validator`: the keyword that failed (for example `"enum"`).
- `error.validator_value`: what the schema expected (for example the list of allowed values).
- `error.instance`: the actual value that failed.

Here is a small formatter that turns them into the five-part shape:

```python
# friendly_errors.py
import json
from jsonschema import Draft202012Validator

with open("tcd_output.schema.json") as f:
    validator = Draft202012Validator(json.load(f))

FIX_HINTS = {
    "required": "Add the missing field.",
    "enum":     "Use one of the allowed values.",
    "pattern":  "Change the value so it matches the pattern.",
    "minItems": "Add at least the minimum number of items.",
}

def friendly(error) -> str:
    where = "/".join(str(p) for p in error.absolute_path) or "(root)"
    return (
        f"WHERE:    {where}\n"
        f"WHAT:     '{error.validator}' rule failed\n"
        f"EXPECTED: {error.validator_value}\n"
        f"ACTUAL:   {json.dumps(error.instance)}\n"
        f"FIX:      {FIX_HINTS.get(error.validator, 'See the contract documentation.')}"
    )

with open("us205_output.json") as f:
    output = json.load(f)
output["test_cases"][0]["priority"] = "urgent"      # planted mistake

for error in validator.iter_errors(output):
    print("Raw:      ", error.message)
    print(friendly(error))
```

Output:

```text
Raw:       'urgent' is not one of ['high', 'medium', 'low']
WHERE:    test_cases/0/priority
WHAT:     'enum' rule failed
EXPECTED: ['high', 'medium', 'low']
ACTUAL:   "urgent"
FIX:      Use one of the allowed values.
```

We start from the valid `us205_output.json`, plant one mistake, and validate. `FIX_HINTS.get(..., default)` looks up a hint by keyword and falls back to a general hint for keywords we have not listed.

Good messages pay off twice with AI agents: later in the course an error message can be **fed back to the model** so it can correct its output, and a precise message gives it a far better chance than "invalid output".

Also: put the **rule ID** in every message so log lines trace back to the catalogue, use the contract's field names, and **never echo secrets or personal data** in a message (mask the value instead).

---

### 12. Strict vs Lenient Validation

Two separate choices are often mixed up under "strictness".

#### 12.1 Fail fast or collect all?

- **Fail fast:** stop at the first error. In `jsonschema`, `validator.validate(doc)` raises a single exception (the error the library judges most relevant) and stops there.
- **Collect all:** gather every error, then report them together. In `jsonschema`, `validator.iter_errors(doc)` gives them all. (The library also offers `jsonschema.exceptions.best_match(errors)` to pick the single most relevant one.)

| Approach | Good for | Drawback |
|---|---|---|
| Fail fast | Quick gates where any error means "stop" (for example, before an expensive call), or when later checks depend on earlier ones | Fix-one, rerun, find-the-next cycle |
| Collect all | Reports to humans; feedback to a model; review of many outputs | Can produce noisy cascades (one root cause, many messages) |

A sensible combination for agents: **collect all errors within a layer, but do not run a deeper layer if a shallower one failed.** For example, if the output fails the schema, do not run R2 and R4: their code assumes the shape is correct, and would only add confusing extra errors (or crash on a missing key).

#### 12.2 Error or warning?

- An **error** means "this output must not be used". The run fails.
- A **warning** means "usable, but a human should look". The run passes, and the warning is logged.

Make something an error when using the output would be **wrong or unsafe** (broken traceability, missing oracle, wrong story). Make it a warning when the automated check is a **heuristic** that sometimes flags good output (Q1, Q2). If you make a heuristic an error, people quickly learn to ignore or bypass the gate, which is worse than having no gate.

#### 12.3 Strict or lenient about the data itself?

For AI agent **output**, be **strict**: `additionalProperties: false`, exact enums, exact patterns. Quietly accepting `"High"` for `"high"`, or ignoring unknown keys, hides drift in the model's behaviour, and drift is exactly what you need to notice. If you normalise something (such as trimming whitespace), do it explicitly, record it in the catalogue and log it.

---

### 13. Putting It Together: The Validation Layers for TestCaseDesigner

Here is the full picture you have designed today, from left to right:

```text
 caller's story
      │
      ▼
 [1] Input schema (S2)  ── fail ──► reject, no model call
      │ pass
      ▼
   model call (agent)
      │
      ▼
 [2] Output schema (S1) ── fail ──► errors (stop: deeper rules not run)
      │ pass
      ▼
 [3] Code rules R1–R6   ── fail ──► errors
      │ pass
      ▼
 [4] Code warnings Q1–Q2 ─────────► warnings logged, run continues
      │
      ▼
 [5] Human review (Q3 + Wednesday checklist) ──► approved test cases
```

Each layer is cheaper and more certain than the next one. Each rule appears in exactly one layer, as recorded in the catalogue. Friday's lessons turn this diagram into working code and run it against real requirements.

---

## Practice Exercises

1. **Missing, empty or null?** For each output fragment, say which state it is in and whether TestCaseDesigner v1.0.0 accepts it: (a) a test case with no `preconditions` key; (b) `"open_questions": null`; (c) `"steps": []`; (d) `"preconditions": []`. Check your answers by validating each case with `Draft202012Validator` against `tcd_output.schema.json`.

2. **Required or not?** A colleague proposes adding three fields to each output test case: `estimated_minutes` (integer), `automation_candidate` (boolean) and `author` (string). For each, apply the four questions from Section 4 and decide: required, optional, optional with default, or rejected. Justify each decision in one sentence. Hint: can the agent honestly fill `author`?

3. **Write R1, R3 and R5.** Following the style of `check_r2` and `check_r4`, write `check_r1`, `check_r3` and `check_r5` as small functions that return lists of messages in the format from the rule catalogue. Remember that `max_cases` may be missing from the input (use the default 10), and that R3 is satisfied if an AC appears in `open_questions` text (a simple `"AC4" in question` check is enough for today). Test each with one passing and one failing sample.

4. **A conditional rule in schema.** Write an `if` / `then` schema for Q1: "if `techniques` contains `"BVA"`, then ..." Discover the problem: `techniques` is in the **input**, and `type: "boundary"` is in the **output**. Explain in two sentences why Q1 must live in code, not in either schema.

---

## Knowledge Check

1. What does `"required": ["open_questions"]` guarantee, and what does it **not** guarantee?

<details><summary>Answer</summary>
It guarantees that the key <code>open_questions</code> is present. It does not say anything about its value: whether it may be empty, null, or what type it has is controlled by the property's own rules (for example <code>"type": "array"</code> and, if needed, <code>minItems</code>).
</details>

2. The input arrives without `max_cases`. The schema says `"default": 10`. Does `jsonschema` add `max_cases: 10` to the input for you?

<details><summary>Answer</summary>
No. <code>default</code> is an annotation, documentation only. Your code must apply it, for example <code>story.get("max_cases", 10)</code>.
</details>

3. Why is `open_questions` required in the output even though it is often empty, while `preconditions` is optional?

<details><summary>Answer</summary>
A missing <code>open_questions</code> is ambiguous: the agent may have had no questions, or it may have forgotten or been cut off. Requiring it forces an explicit <code>[]</code>. A missing <code>preconditions</code> has one obvious meaning ("no special setup"), so it can safely be optional.
</details>

4. Name the five categories of validation rule, and say which ones JSON Schema can express on its own.

<details><summary>Answer</summary>
Structural, field-level, cross-field (conditional), cross-document (semantic), and business/quality. JSON Schema can express the first three; cross-document rules need code that sees the input; business/quality rules need code and/or human review.
</details>

5. An output contains `"ac_ids": ["AC5"]` for story US-205, which has AC1 to AC4. It passes the output schema. Which rule catches it, and why couldn't the schema?

<details><summary>Answer</summary>
R2. The schema can check that <code>AC5</code> matches the pattern <code>^AC[0-9]+$</code>, but it validates only the output document and cannot see which ACs the input story actually has.
</details>

6. When would you choose `dependentRequired` instead of `if` / `then`?

<details><summary>Answer</summary>
When the condition is simply "if key X is present, keys Y and Z must also be present". Use <code>if</code>/<code>then</code> when the condition depends on a value (such as <code>status == "ok"</code>) or the consequence is more than requiring keys.
</details>

7. Why should Q2 ("expected_result must be concrete") be a warning rather than an error?

<details><summary>Answer</summary>
Because the automated check is a heuristic: looking for vague phrases produces false positives and false negatives. Making it an error would block good output and teach people to bypass the gate; as a warning, it points a human reviewer at likely problems.
</details>

8. Give two reasons to validate the agent's **input** before calling the model.

<details><summary>Answer</summary>
Any two of: it saves the cost and time of a model call that cannot succeed; it prevents garbage in, garbage out (for example the model inventing requirements when ACs are empty); it separates caller errors from agent errors, which speeds up debugging.
</details>

---

## Glossary

- **Required field:** A key that must be present in the document; listed in the schema's `required` array.
- **Nullable field:** A field whose type allows `null`, for example `"type": ["string", "null"]`.
- **Default:** A documented value used when an optional field is missing. In JSON Schema it is only an annotation; code must apply it.
- **Cross-field (conditional) rule:** Checks that fields in the same document agree; expressed with `if`/`then` or `dependentRequired`.
- **Cross-document (semantic) rule:** Checks the output against the input or other data; needs code.
- **Business / quality rule:** Checks whether the output is *good*, not just well-formed; often a warning plus human review.
- **`if` / `then` / `else`:** JSON Schema keywords that apply a subschema only when a condition schema matches (or does not match).
- **`dependentRequired`:** JSON Schema keyword: if a given key is present, listed other keys are required.
- **Rule catalogue:** A table listing every rule with its ID, layer, severity, example violation and error message.
- **Severity:** Whether a broken rule is an **error** (reject) or a **warning** (accept and flag).
- **Fail fast / collect all:** Stop at the first error vs gather every error before reporting.

---

## Summary

- **Required** means "the key must exist", not "the value must be non-empty". **Defaults** are documentation until code applies them.
- **Missing, empty and null** mean different things. Prefer empty lists over `null`, and require fields whose absence would be ambiguous, such as `open_questions`.
- Decide required fields with four questions: **who consumes it, can they work without it, is there a safe default, and can the agent honestly produce it?** Requiring what the agent cannot know invites invented filler.
- Validation rules come in five categories. **Structural, field-level and cross-field** rules can live in JSON Schema (`if`/`then`, `dependentRequired`); **cross-document** rules (R1 to R5) need code that sees the input; **business/quality** rules (Q1 to Q3) need code warnings and human review.
- Keep a **rule catalogue** with IDs, layers, severities, example violations and messages, so every rule is checked exactly once, in the right place.
- Write error messages that say **where, what, expected, actual and how to fix**, with the rule ID; they help people now and help models correct themselves later.
- Validate **input first** (cheap), then output schema, then code rules, then warnings, then human review. Collect all errors within a layer, but do not run deeper layers on broken shapes.
- On **Friday** you combine all of this into working validation scripts and run the agent against real QA requirements.

---

## Additional Resources

- JSON Schema, *Understanding JSON Schema: Conditional schema validation* (official guide to `dependentRequired`, `dependentSchemas` and `if`/`then`/`else`, with examples): https://json-schema.org/understanding-json-schema/reference/conditionals
- python-jsonschema documentation, *Handling Validation Errors* (the `ValidationError` attributes used in this lesson, `iter_errors`, and `best_match` for choosing the most relevant error): https://python-jsonschema.readthedocs.io/en/stable/errors/
- IETF, *RFC 9457: Problem Details for HTTP APIs* (a widely used standard shape for machine-readable error responses; a good model for designing your own error format): https://www.rfc-editor.org/rfc/rfc9457.html
