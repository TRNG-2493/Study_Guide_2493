# JSON Schema

## Learning Objectives

By the end of this lesson you will be able to:

- Recall the **six JSON value types** and how each one maps to a Python type when you call `json.loads`.
- Explain what **JSON Schema** is: a JSON document that describes what *other* JSON documents are allowed to look like.
- Explain what a **draft** is and why every schema in this course starts with `"$schema": "https://json-schema.org/draft/2020-12/schema"`.
- Build a schema **step by step** using the core keywords: `type`, `properties`, `required` and `additionalProperties`.
- Constrain values with **string** keywords (`minLength`, `maxLength`, `pattern`, `format`), **choice** keywords (`enum`, `const`), **number** keywords (`minimum`, `maximum`, `exclusiveMinimum`, `multipleOf`) and **array** keywords (`items`, `minItems`, `uniqueItems`, `prefixItems`).
- Read a regular expression such as `^TC-[0-9]{3}-[0-9]{2}$` character by character.
- Reuse schema parts with **`$defs` and `$ref`**, and know which keywords are only **annotations** (`title`, `description`, `default`, `examples`).
- Recognise the combining keywords **`anyOf`, `oneOf`, `allOf` and `not`**.
- Read the full **TestCaseDesigner** input and output schemas.
- Use the Python **`jsonschema`** library to check a schema, validate a document, and list **every** error with its location.
- Avoid the most common JSON Schema mistakes.

---

## Why This Matters

On Tuesday you learned **format locking**: telling a model to answer in JSON with fixed field names, then parsing that JSON in Python. That made AI output machine-readable. But "machine-readable" is not the same as "correct shape". A model can return perfectly valid JSON that still has a missing `expected_result`, a test type of `"edge"` that nobody asked for, or an ID like `TC-205-1` that breaks your reporting tool.

Earlier today, in **Input/output contracts**, you saw that an agent needs a written agreement about what goes in and what comes out. Plain English is a good start, but people read it differently and a computer cannot check it at all. **JSON Schema** is the standard way to write the *structural* part of that agreement so that a program can check it automatically, every time, in milliseconds.

This is the heart of the **Weekly Epic**: "design and build their first QA agent with **IO contracts** and **validation scripts**". Today you learn to *write and read* the contract in JSON Schema. On Friday you will use it inside validation scripts that check your agent's output. For **Project 2 (Test Automation Framework)**, JSON Schema is also everyday API-testing knowledge: many teams check that an API response matches a schema before they check individual values, so this skill pays off well beyond agents.

> **Scope note.** This lesson teaches the JSON Schema language and shows how to run a validator on a document. Expressing extra rules such as "if the status is X then field Y is required" (`if`/`then`, `dependentRequired`) and rules that a schema cannot express at all are covered in the next lesson, **Required fields and validation rules**. Full validation scripts that load agent output, report results and fit into a workflow are covered on **Friday**.

---

## The Concept

### 1. A Quick JSON Refresher

**JSON** (JavaScript Object Notation) is a text format for structured data. Every JSON value is one of exactly **six types**:

| JSON type | Example | Python type after `json.loads` |
|---|---|---|
| object | `{"story_id": "US-205"}` | `dict` |
| array | `["EP", "BVA"]` | `list` |
| string | `"US-205"` | `str` |
| number | `6` or `0.1` | `int` or `float` |
| boolean | `true` / `false` | `bool` (`True` / `False`) |
| null | `null` | `None` |

A few rules trip beginners up:

- Keys in an object must be **strings in double quotes**. `{'id': 1}` (single quotes) is valid Python but **not** valid JSON.
- JSON has only one **number** type. Python decides whether to give you an `int` or a `float` depending on whether a decimal point is present.
- `true`, `false` and `null` are lower case in JSON; Python writes them `True`, `False` and `None`.
- No trailing commas, no comments.

Here is the mapping in action:

```python
# s1_json_python.py
import json

text = '''
{
  "story_id": "US-205",
  "max_cases": 6,
  "discount_rate": 0.1,
  "urgent": false,
  "owner": null,
  "techniques": ["EP", "BVA"]
}
'''
data = json.loads(text)
for key, value in data.items():
    print(f"{key:14} -> {type(value).__name__:5} {value!r}")
```

Output:

```text
story_id       -> str   'US-205'
max_cases      -> int   6
discount_rate  -> float 0.1
urgent         -> bool  False
owner          -> NoneType None
techniques     -> list  ['EP', 'BVA']
```

`json.loads` checks only that the text is **well-formed JSON** (correct quotes, brackets and commas). It does not check whether `max_cases` is sensible, whether `story_id` follows your naming rule, or whether a required field is missing. That second kind of checking is what JSON Schema is for.

### 2. What Is JSON Schema?

**JSON Schema** is a vocabulary for describing JSON data. A schema is itself a JSON document. It says things like "this must be an object", "it must have a field called `story_id`", "that field must be a string that looks like `US-` followed by three digits".

Two terms you will see all the time:

- **Schema**: the description (the rules).
- **Instance**: the JSON document being checked against the schema (the data).

A **validator** is a program that takes a schema and an instance and answers "valid" or "invalid, and here is why".

**Analogy: a form template.** Think of a paper form at a doctor's office. The blank form says "Name (required)", "Date of birth (DD/MM/YYYY)", "Allergies (tick one: yes / no)". The blank form is the **schema**. Each filled-in form is an **instance**. The receptionist who checks each form before accepting it is the **validator**. The template does not care *who* you are; it only cares that the answers are in the right boxes, in the right format, and that no required box is empty.

Another analogy is a **building blueprint**: it describes what any house built from it must look like, and an inspector can compare a real house against it.

Why use a standard instead of writing `if` checks by hand?

- **One source of truth.** The same schema file can be read by people, checked by Python, used by other languages (Java, JavaScript, C#), shown in documentation, and even given to some model APIs.
- **Declarative.** You say *what* is allowed, not *how* to check it. This is shorter and harder to get wrong than dozens of `if` statements.
- **Every error at once.** A good validator reports all the problems, with their exact location, not only the first.

### 3. Drafts and the `$schema` Keyword

JSON Schema has evolved through several versions called **drafts**: Draft 4, Draft 6, Draft 7, 2019-09 and **2020-12** (the current published version). Most keywords are the same across drafts, but some changed. For example, `prefixItems` exists only from 2020-12, and the meaning of `items` with a list changed in that draft.

Because of these differences, a schema should say which draft it is written for. That is the job of the `$schema` keyword, which goes at the very top:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema"
}
```

The value is a URL that identifies the draft (a validator does not need to download it). In this course every schema uses **2020-12** because it is the current version, it is what modern libraries support, and it is the version the official documentation teaches.

You will also see `$id` in our schemas. `$id` gives the schema its own unique identifier (also written as a URL). It is useful when schemas refer to each other and for knowing which version of a contract you are looking at. It is an identifier only; nothing needs to exist at that address.

### 4. Building the `test_case` Schema Step by Step

The **TestCaseDesigner** agent returns test cases. Each test case looks like this (from our sample output for US-205):

```json
{
  "id": "TC-205-01",
  "title": "SAVE10 applied at exactly $50.00",
  "ac_ids": ["AC1"],
  "type": "boundary",
  "priority": "high",
  "preconditions": ["Cart subtotal is $50.00"],
  "steps": ["Enter coupon SAVE10", "Click Apply"],
  "expected_result": "Total is $45.00"
}
```

We will build a schema for this object from nothing, checking each step with Python. Every snippet uses this small helper, which prints `VALID` or one line per error:

```python
from jsonschema import Draft202012Validator

def check(label, schema, instance):
    """Validate instance against schema and print every error message."""
    errors = sorted(Draft202012Validator(schema).iter_errors(instance),
                    key=lambda e: list(e.path))
    if not errors:
        print(f"{label}: VALID")
    for e in errors:
        print(f"{label}: INVALID - {e.message}")
```

Do not worry about the details of `Draft202012Validator` and `iter_errors` yet; section 13 explains them. (Install the library with `pip install "jsonschema>=4.18"`.)

#### Step 1: `type`

The `type` keyword says which of the six JSON types the value must be. Python's `dict` is a JSON object, so:

```python
step1 = {"type": "object"}
check("step1 dict ", step1, {"id": "TC-205-01"})
check("step1 list ", step1, ["TC-205-01"])
```

```text
step1 dict : VALID
step1 list : INVALID - ['TC-205-01'] is not of type 'object'
```

The type names are the JSON names: `"object"`, `"array"`, `"string"`, `"number"`, `"boolean"`, `"null"`, plus `"integer"` for numbers with no fractional part. You can allow several types with a list, for example `"type": ["string", "null"]`.

#### Step 2: `properties`

`properties` is an object that maps each field name to **its own sub-schema**. This is the key idea of JSON Schema: schemas nest. The schema for the whole test case contains a small schema for `id`, another for `title`, and so on.

```python
step2 = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
    },
}
check("step2 good ", step2, {"id": "TC-205-01", "title": "SAVE10 applied at exactly $50.00"})
check("step2 wrong", step2, {"id": 205, "title": "SAVE10 applied at exactly $50.00"})
check("step2 empty", step2, {})
```

```text
step2 good : VALID
step2 wrong: INVALID - 205 is not of type 'string'
step2 empty: VALID
```

Look at the last line. An **empty object is valid**. That surprises almost everyone. `properties` only says "**if** a field called `id` is present, it must be a string". It does not say the field must be present.

#### Step 3: `required`

To insist that fields exist, list them in `required` (an array of field names, at the same level as `properties`):

```python
step3 = dict(step2, required=["id", "title"])
check("step3 empty", step3, {})
```

```text
step3 empty: INVALID - 'id' is a required property
step3 empty: INVALID - 'title' is a required property
```

Notice that the validator reports **both** missing fields, not just the first. (Choosing *which* fields should be required, optional or nullable is a design decision covered in the next lesson.)

#### Step 4: `additionalProperties: false`

By default, JSON Schema objects are **open**: any field not listed in `properties` is allowed. So a model that writes `"expected_reslt"` (a typo) would pass, and your code would later crash looking for `expected_result`. Setting `additionalProperties` to `false` **closes** the object:

```python
step4 = dict(step3, additionalProperties=False)
check("step4 typo ", step4, {"id": "TC-205-01", "title": "SAVE10 applied at exactly $50.00",
                             "expected_reslt": "Total is $45.00"})
```

```text
step4 typo : INVALID - Additional properties are not allowed ('expected_reslt' was unexpected)
```

For agent output this is almost always what you want: it catches typos, invented fields and "helpful" extra commentary. Every object in the TestCaseDesigner contract is closed this way.

With these four keywords you can already describe the *shape* of any object. The next sections tighten the *values*.

### 5. String Keywords

#### `minLength` and `maxLength`

These limit how many characters a string may have. Our contract says a test case title is 10 to 100 characters, which blocks useless titles like `"Coupon"` and runaway paragraphs:

```python
title = {"type": "string", "minLength": 10, "maxLength": 100}
check("title 'Coupon'    ", title, "Coupon")
```

```text
title 'Coupon'    : INVALID - 'Coupon' is too short
```

#### `pattern`

`pattern` requires the string to match a **regular expression** (regex): a small language for describing text shapes. Our test case IDs must look like `TC-205-01`. The pattern is:

```text
^TC-[0-9]{3}-[0-9]{2}$
```

Read it one piece at a time:

| Piece | Meaning |
|---|---|
| `^` | Start of the string. Nothing may come before what follows. |
| `TC-` | The literal characters `T`, `C`, `-`. Upper case only. |
| `[0-9]` | Any **one** character from `0` to `9` (a digit). |
| `{3}` | Exactly **three** of the previous thing, so three digits (the story number, e.g. `205`). |
| `-` | A literal hyphen. |
| `[0-9]{2}` | Exactly two digits (the case number, e.g. `01`). |
| `$` | End of the string. Nothing may come after. |

Now test it:

```python
tc_id = {"type": "string", "pattern": "^TC-[0-9]{3}-[0-9]{2}$"}
for value in ["TC-205-01", "TC-205-1", "tc-205-01", "TC-205-01 copy"]:
    check(f"id {value!r:17}", tc_id, value)
```

```text
id 'TC-205-01'      : VALID
id 'TC-205-1'       : INVALID - 'TC-205-1' does not match '^TC-[0-9]{3}-[0-9]{2}$'
id 'tc-205-01'      : INVALID - 'tc-205-01' does not match '^TC-[0-9]{3}-[0-9]{2}$'
id 'TC-205-01 copy' : INVALID - 'TC-205-01 copy' does not match '^TC-[0-9]{3}-[0-9]{2}$'
```

`TC-205-1` fails because `{2}` demands two digits. `tc-205-01` fails because regex is case-sensitive. `TC-205-01 copy` fails only because of the `$` anchor, which forbids anything after the second digit. Section 14 shows what happens if you forget the anchors.

The other patterns in our contract work the same way: `^US-[0-9]{3}$` for story IDs, and `^AC[0-9]+$` for acceptance criterion IDs, where `+` means "**one or more**" (so `AC1`, `AC4` and `AC12` all match).

Notice what the pattern **cannot** check: that the `205` in `TC-205-01` is the same number as the story `US-205`. That relationship is between two different fields (and the input), which is rule **R4** in our contract. Schemas check each value on its own terms; rules that compare values are the subject of the next lesson.

#### `format`

`format` names a well-known string kind: `"email"`, `"date"` (`2026-10-15`), `"date-time"`, `"uri"`, `"uuid"` and others. The catch: **in Draft 2020-12, `format` is an annotation by default**. It documents intent but is **not checked** unless you turn checking on:

```python
from jsonschema import Draft202012Validator, FormatChecker

email = {"type": "string", "format": "email"}
check("format, default checker ", email, "not-an-email")
check("format, FormatChecker on", email, "not-an-email", format_checker=FormatChecker())
```

```text
format, default checker : VALID
format, FormatChecker on: INVALID - 'not-an-email' is not a 'email'
```

(For this snippet, `check` was extended to pass extra keyword arguments such as `format_checker` through to `Draft202012Validator`.) If a format really matters, either enable a format checker or use an explicit `pattern` you control. Some formats also need extra packages to be checked; the `jsonschema` documentation lists them.

### 6. `enum` and `const`

`enum` lists the **only** allowed values. It is perfect for fields that are really a choice from a fixed menu, such as test case type, priority or status:

```python
tc_type = {"enum": ["positive", "negative", "boundary"]}
check("type 'edge'       ", tc_type, "edge")
```

```text
type 'edge'       : INVALID - 'edge' is not one of ['positive', 'negative', 'boundary']
```

Models love to invent near-synonyms (`"edge"`, `"Positive"`, `"happy path"`). An `enum` turns each of those into a clear, immediate error instead of a silent mismatch in your reports. Note that `enum` comparisons are exact, so `"Positive"` with a capital P is also rejected.

`const` is an enum with exactly one value. Our output contract uses it to pin the version:

```python
version = {"const": "1.0.0"}
check("version '1.0'     ", version, "1.0")
```

```text
version '1.0'     : INVALID - '1.0.0' was expected
```

Why pin a version inside the output? Because when the contract changes to `2.0.0`, any output produced against the old contract is instantly recognisable. (Contract versioning was discussed in **Input/output contracts**.)

### 7. Number Keywords

| Keyword | Meaning |
|---|---|
| `minimum` | value >= limit |
| `maximum` | value <= limit |
| `exclusiveMinimum` | value > limit |
| `exclusiveMaximum` | value < limit |
| `multipleOf` | value divided by this has no remainder |

Our input contract says `max_cases` is a whole number from 1 to 20:

```python
max_cases = {"type": "integer", "minimum": 1, "maximum": 20}
for value in [6, 0, 21, 6.5]:
    check(f"max_cases {value!r:7}", max_cases, value)
```

```text
max_cases 6      : VALID
max_cases 0      : INVALID - 0 is less than the minimum of 1
max_cases 21     : INVALID - 21 is greater than the maximum of 20
max_cases 6.5    : INVALID - 6.5 is not of type 'integer'
```

Note: JSON Schema decides "integer" by **value**, not by spelling, so `6.0` counts as an integer, while `6.5` does not.

A money example (not part of our contract, but common in Project 2 API tests): a price must be greater than zero and have at most two decimal places:

```python
price = {"type": "number", "exclusiveMinimum": 0, "multipleOf": 0.01}
for value in [49.99, 0, 10.005]:
    check(f"price {value!r:11}", price, value)
```

```text
price 49.99      : VALID
price 0          : INVALID - 0 is less than or equal to the minimum of 0
price 10.005     : INVALID - 10.005 is not a multiple of 0.01
```

`exclusiveMinimum: 0` rejects a free product, which `minimum: 0` would allow. Remember Wednesday's lesson on test data: floating-point numbers are imprecise, so many real APIs send money as integer **cents** (`4999`) or as strings; `multipleOf` with decimals works in this library but is not the safest design for money.

### 8. Array Keywords

| Keyword | Meaning |
|---|---|
| `items` | a schema that **every** element must match |
| `minItems` / `maxItems` | how many elements are allowed |
| `uniqueItems: true` | no two elements may be equal |
| `prefixItems` | a list of schemas for elements **by position** (a "tuple") |

The `ac_ids` field links a test case to the acceptance criteria it covers. It must have at least one entry, each must look like an AC ID, and duplicates make no sense:

```python
ac_ids = {"type": "array", "items": {"type": "string", "pattern": "^AC[0-9]+$"},
          "minItems": 1, "uniqueItems": True}
for value in [["AC1", "AC2"], [], ["AC1", "AC1"], ["AC1", "ac2"]]:
    check(f"ac_ids {str(value):14}", ac_ids, value)
```

```text
ac_ids ['AC1', 'AC2']: VALID
ac_ids []            : INVALID - [] should be non-empty
ac_ids ['AC1', 'AC1']: INVALID - ['AC1', 'AC1'] has non-unique elements
ac_ids ['AC1', 'ac2']: INVALID - 'ac2' does not match '^AC[0-9]+$'
```

Notice `items` holds a full sub-schema, so everything you learned about strings applies to each element. Again, the schema can check that `"AC9"` *looks like* an AC ID, but not that US-205 actually has an AC9. That is rule **R2**, a cross-check against the input, covered in the next lesson.

**`prefixItems`** (new in 2020-12) is for arrays where each **position** means something different, like `["US-205", 3]` meaning "story, story points". You give one schema per position, and you can set `"items": false` to forbid anything after the last position. Our contract does not use tuples (objects with named fields are clearer for agent output), but you will meet them in other schemas. An example follows in the next section.

### 9. Reuse with `$defs` and `$ref`

The story ID pattern appears in both the input and the output, and might appear several times in one schema. Copying it is risky: change one copy and forget the others, and your contract disagrees with itself. JSON Schema lets you define a piece **once** under `$defs` and point to it with `$ref`:

```python
from jsonschema import Draft202012Validator

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "story_id": {"$ref": "#/$defs/story_id"},
        "related_stories": {"type": "array", "items": {"$ref": "#/$defs/story_id"}},
        # prefixItems: position 0 must be a story id, position 1 a positive integer
        "story_and_points": {
            "type": "array",
            "prefixItems": [{"$ref": "#/$defs/story_id"}, {"type": "integer", "minimum": 1}],
            "items": False,
        },
    },
    "$defs": {
        "story_id": {"type": "string", "pattern": "^US-[0-9]{3}$"}
    },
}
instance = {"story_id": "US-205",
            "related_stories": ["US-101", "US-31"],
            "story_and_points": ["US-205", 3, "extra"]}
for e in sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.path)):
    print(list(e.path), "-", e.message)
```

```text
['related_stories', 1] - 'US-31' does not match '^US-[0-9]{3}$'
['story_and_points'] - Expected at most 2 items but found 1 extra: 'extra'
```

How to read `"$ref": "#/$defs/story_id"`:

- `#` means "this same document".
- `/$defs/story_id` is a **path** into it: go to the `$defs` key, then the `story_id` key.

The validator replaces the `$ref` with whatever it finds there. Our output contract uses exactly this for test cases: the `test_cases` array says `"items": {"$ref": "#/$defs/test_case"}`, and the long test case schema lives once under `$defs`. This keeps the top level short and readable.

### 10. Annotations: `title`, `description`, `default`, `examples`

Some keywords do not validate anything. They are **annotations**: information for humans and tools.

- `title` and `description` explain what a schema or field is for. Editors show them as tooltips, and documentation generators turn them into pages. A model reading the schema benefits from them too.
- `examples` gives sample valid values.
- `default` documents the value a **consumer** should assume when the field is missing.

The important trap is `default`. **Validation never fills in defaults.** Our input contract says `max_cases` has `"default": 10`, but look:

```python
schema = {"type": "object",
          "properties": {"max_cases": {"type": "integer", "default": 10}}}
data = {}
check("default                 ", schema, data)
print("data after validation   :", data)
```

```text
default                 : VALID
data after validation   : {}
```

The data is still empty. If your agent code needs `max_cases`, it must apply the default itself, for example with `data.get("max_cases", 10)`. The schema only documents the agreement.

### 11. Combining Schemas: `anyOf`, `oneOf`, `allOf`, `not`

Sometimes one rule is not enough. Four keywords combine sub-schemas:

| Keyword | Valid when... | Everyday meaning |
|---|---|---|
| `anyOf` | at least one sub-schema matches | "OR" |
| `oneOf` | **exactly** one sub-schema matches | "either, but not both" |
| `allOf` | every sub-schema matches | "AND" |
| `not` | the sub-schema does **not** match | "NOT" |

```python
# anyOf: a subtotal may be a number OR a string like "49.99"
subtotal = {"anyOf": [{"type": "number", "minimum": 0},
                      {"type": "string", "pattern": "^[0-9]+\\.[0-9]{2}$"}]}
check("anyOf 49.99    ", subtotal, 49.99)
check("anyOf '49.99'  ", subtotal, "49.99")
check("anyOf 'cheap'  ", subtotal, "cheap")

# oneOf: EXACTLY one branch must match
one = {"oneOf": [{"type": "integer"}, {"type": "number", "minimum": 0}]}
check("oneOf 5        ", one, 5)      # matches both branches
check("oneOf -2.5     ", one, -2.5)   # matches neither branch
check("oneOf 2.5      ", one, 2.5)    # matches only the second

# allOf + not: a title of at least 10 characters that is not a placeholder
title = {"allOf": [{"type": "string", "minLength": 10},
                   {"not": {"pattern": "^(TODO|TBD)"}}]}
check("allOf/not title", title, "TODO write this title")
```

```text
anyOf 49.99    : VALID
anyOf '49.99'  : VALID
anyOf 'cheap'  : INVALID - 'cheap' is not valid under any of the given schemas
oneOf 5        : INVALID - 5 is valid under each of {'type': 'number', 'minimum': 0}, {'type': 'integer'}
oneOf -2.5     : INVALID - -2.5 is not valid under any of the given schemas
oneOf 2.5      : VALID
allOf/not title: INVALID - 'TODO write this title' should not be valid under {'pattern': '^(TODO|TBD)'}
```

The `oneOf 5` result is the classic surprise: `5` is an integer **and** a non-negative number, so it matches two branches and `oneOf` rejects it. Use `anyOf` unless you truly mean "exactly one". Also notice the combined error messages are less friendly than single-keyword messages; keep combinations to a minimum in contracts that humans must debug.

There is one more pair of combining keywords, `if` / `then` / `else`, for conditional rules such as "if `status` is `needs_clarification`, then `open_questions` must not be empty" (rule **R6**). That is covered in the next lesson, **Required fields and validation rules**.

### 12. The Full TestCaseDesigner Contract

You now know every keyword in our two schemas. Here they are in full. Read them slowly, top to bottom, and say out loud what each line means. That habit is the core skill of today's demo, where your instructor dissects a QA agent's contract.

**Output schema** (`tcd_output.schema.json`):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/tcd/output/1.0.0",
  "title": "TestCaseDesigner output",
  "type": "object",
  "properties": {
    "contract_version": {"const": "1.0.0"},
    "story_id": {"type": "string", "pattern": "^US-[0-9]{3}$"},
    "status": {"enum": ["ok", "needs_clarification"]},
    "test_cases": {
      "type": "array",
      "items": {"$ref": "#/$defs/test_case"}
    },
    "open_questions": {"type": "array", "items": {"type": "string", "minLength": 5}}
  },
  "required": ["contract_version", "story_id", "status", "test_cases", "open_questions"],
  "additionalProperties": false,
  "$defs": {
    "test_case": {
      "type": "object",
      "properties": {
        "id": {"type": "string", "pattern": "^TC-[0-9]{3}-[0-9]{2}$"},
        "title": {"type": "string", "minLength": 10, "maxLength": 100},
        "ac_ids": {"type": "array", "items": {"type": "string", "pattern": "^AC[0-9]+$"}, "minItems": 1, "uniqueItems": true},
        "type": {"enum": ["positive", "negative", "boundary"]},
        "priority": {"enum": ["high", "medium", "low"]},
        "preconditions": {"type": "array", "items": {"type": "string"}},
        "steps": {"type": "array", "items": {"type": "string", "minLength": 3}, "minItems": 1},
        "expected_result": {"type": "string", "minLength": 5}
      },
      "required": ["id", "title", "ac_ids", "type", "priority", "steps", "expected_result"],
      "additionalProperties": false
    }
  }
}
```

A plain-English reading:

- The output is a **closed object** with five required fields.
- `contract_version` must be exactly `"1.0.0"`; `story_id` must look like `US-` plus three digits; `status` is `ok` or `needs_clarification`.
- `test_cases` is an array (it **may** be empty, there is no `minItems`), and each element must match the `test_case` definition.
- `open_questions` is an array of strings of at least 5 characters (it may also be empty).
- Each test case is a closed object. Seven fields are required; `preconditions` is the only optional one (it is in `properties` but not in `required`).

**Input schema** (`tcd_input.schema.json`):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/tcd/input/1.0.0",
  "title": "TestCaseDesigner input",
  "description": "One user story sent to the TestCaseDesigner agent.",
  "type": "object",
  "properties": {
    "story_id": {"type": "string", "pattern": "^US-[0-9]{3}$"},
    "title": {"type": "string", "minLength": 5, "maxLength": 120},
    "acceptance_criteria": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "string", "pattern": "^AC[0-9]+$"},
          "text": {"type": "string", "minLength": 10}
        },
        "required": ["id", "text"],
        "additionalProperties": false
      }
    },
    "techniques": {
      "type": "array",
      "items": {"enum": ["EP", "BVA", "decision_table", "state_transition"]},
      "uniqueItems": true
    },
    "max_cases": {"type": "integer", "minimum": 1, "maximum": 20, "default": 10}
  },
  "required": ["story_id", "title", "acceptance_criteria"],
  "additionalProperties": false
}
```

Points worth noticing:

- Three fields are required; `techniques` and `max_cases` are optional. `max_cases` documents a `default` of 10, which the agent's code must apply itself.
- A story must have **at least one** acceptance criterion, and each criterion is a small closed object with `id` and `text`. The schema is nested three levels deep (object → array → object), which is perfectly normal.
- `techniques` uses `enum` inside `items`: each element must be one of four technique names, and none may repeat. These are the test design techniques from Tuesday's **AI-assisted test design** lesson.
- The input schema does not use `$defs`. It could define `story_id` once and share it with the output, but the two schemas are separate files, so each states the pattern directly. (Sharing definitions across files with `$ref` to another schema's `$id` is possible; we keep things simple here.)

**What the schemas cannot say.** Rules R1 to R6 in our contract (for example, "output `story_id` equals input `story_id`", "every `ac_ids` entry exists in the input", "at most `max_cases` test cases") compare values across fields or across the input and output. A single JSON Schema checks one document by itself, so these need a little Python on top. That is the subject of the next lesson.

### 13. Validating in Python with `jsonschema`

The `jsonschema` library is the most widely used JSON Schema validator for Python.

**Install and version caveat.**

```text
pip install "jsonschema>=4.18"
```

Draft 2020-12 support (`Draft202012Validator`) arrived in version **4.0**. Some machines, including some training laptops, still have **3.2** installed as a dependency of another tool. On 3.2 the line `from jsonschema import Draft202012Validator` fails with `ImportError: cannot import name 'Draft202012Validator'`. Check your version with:

```text
python -c "import importlib.metadata as m; print(m.version('jsonschema'))"
```

The examples in this lesson were run with version 4.26.

The library gives you three tools you need today:

1. **`Draft202012Validator.check_schema(schema)`** checks that your **schema** is itself valid JSON Schema (for example, that you did not write `"type": "strng"`). It raises `SchemaError` if not.
2. **`validate(instance, schema)`** checks an instance and raises `ValidationError` for **one** error (the library picks the most relevant one) or returns `None` if valid. Good for a quick yes/no.
3. **`Draft202012Validator(schema).iter_errors(instance)`** yields **every** error. Each error object has:
   - `message`: a human-readable description,
   - `path`: where in the instance the problem is, as a sequence of keys and list indexes (for example `test_cases`, `0`, `id`),
   - `validator`: which keyword failed (for example `"pattern"`).

Now validate the real sample output, then a broken copy with **four planted mistakes**:

```python
# s7_validate_output.py
import copy
import json

from jsonschema import Draft202012Validator, ValidationError, validate

# 1. Load the contract and the sample output
with open("tcd_output.schema.json", encoding="utf-8") as f:
    schema = json.load(f)
with open("us205_output.json", encoding="utf-8") as f:
    good = json.load(f)

# 2. Is the schema itself a valid JSON Schema? (raises SchemaError if not)
Draft202012Validator.check_schema(schema)
print("Schema is a valid Draft 2020-12 schema")

# 3. validate(): raises ONE error, returns None if valid
validate(instance=good, schema=schema, cls=Draft202012Validator)
print("us205_output.json is valid")

# 4. Plant four mistakes in a copy
bad = copy.deepcopy(good)
bad["status"] = "done"                         # not in the enum
bad["test_cases"][0]["id"] = "TC-205-1"        # breaks the id pattern
bad["test_cases"][1]["type"] = "edge"          # not in the enum
del bad["test_cases"][2]["expected_result"]    # required field missing

try:
    validate(instance=bad, schema=schema, cls=Draft202012Validator)
except ValidationError as err:
    print("\nvalidate() reported only one error:")
    print("  ", err.message)

# 5. iter_errors(): collect ALL errors, sorted by their location
validator = Draft202012Validator(schema)
errors = sorted(validator.iter_errors(bad), key=lambda e: list(e.path))
print(f"\niter_errors() found {len(errors)} errors:")
for e in errors:
    location = "/".join(str(part) for part in e.path) or "(root)"
    print(f"  {location:22} {e.message}")
```

Output:

```text
Schema is a valid Draft 2020-12 schema
us205_output.json is valid

validate() reported only one error:
   'done' is not one of ['ok', 'needs_clarification']

iter_errors() found 4 errors:
  status                 'done' is not one of ['ok', 'needs_clarification']
  test_cases/0/id        'TC-205-1' does not match '^TC-[0-9]{3}-[0-9]{2}$'
  test_cases/1/type      'edge' is not one of ['positive', 'negative', 'boundary']
  test_cases/2           'expected_result' is a required property
```

Walk through the code:

- `json.load(f)` reads a file into Python objects (`json.loads` reads a string). The schema file and the instance file are both just JSON.
- `cls=Draft202012Validator` tells `validate` which draft to use. Without it the library reads the `$schema` keyword to decide; being explicit is clearer.
- `copy.deepcopy(good)` makes a fully independent copy, so planting mistakes does not damage the good sample. (A plain `good.copy()` would share the inner test case objects.)
- `sorted(..., key=lambda e: list(e.path))` orders errors by location, so the report reads top to bottom like the document. `iter_errors` does not promise any order on its own.
- `"/".join(str(part) for part in e.path)` turns `["test_cases", 0, "id"]` into `test_cases/0/id`, a readable address. `or "(root)"` handles errors on the whole document, whose path is empty.

Two things to notice in the output. First, `validate()` reported only **one** of the four problems; a reviewer fixing one error at a time would need four round trips, so `iter_errors()` is the better tool when you want to know everything that is wrong. Second, the "missing field" error is reported at `test_cases/2` (the object that is missing something), not at `test_cases/2/expected_result` (which does not exist).

> This is a single, illustrative validation. Turning it into a reusable **validation script** (command-line arguments, validating many files, combining schema errors with rules R1-R6, exit codes and reports) is covered on **Friday** in **Building validation scripts**.

### 14. Common Mistakes

Every one of these passes silently, which is what makes them dangerous. A schema that is too loose looks like it is working because "everything is valid".

```python
# 1. "format" is an annotation by default
# 2. "default" never fills in missing values
# (both shown in sections 5 and 10)

# 3. A pattern without ^ and $ matches anywhere in the string
loose = {"type": "string", "pattern": "TC-[0-9]{3}-[0-9]{2}"}
check("unanchored pattern      ", loose, "see TC-205-01 or whatever")

# 4. A misspelled keyword is silently ignored
typo = {"type": "string", "minLenght": 10}
check("misspelled minLength    ", typo, "short")
```

```text
unanchored pattern      : VALID
misspelled minLength    : VALID
```

| Mistake | What happens | Fix |
|---|---|---|
| Forgetting `required` | `properties` alone lets every field be missing; `{}` is valid. | List every must-have field in `required`. |
| Leaving objects open | `additionalProperties` defaults to `true`, so typos like `expected_reslt` and invented fields pass. | Add `"additionalProperties": false` to every object in an agent contract. |
| Misspelled keyword (`minLenght`, `requried`) | Unknown keywords are ignored, so the rule simply does not exist. `check_schema` does not catch this either. | Test the schema with an instance that **should** fail; use an editor with schema support. |
| Unanchored `pattern` | Regex matches anywhere, so `"see TC-205-01 or whatever"` passes. | Start with `^` and end with `$`. |
| Relying on `format` | Not checked by default. | Enable a `FormatChecker`, or use a `pattern`. |
| Expecting `default` to fill values | Data is unchanged after validation. | Apply defaults in code (`data.get("max_cases", 10)`). |
| `oneOf` where `anyOf` is meant | Values matching two branches are rejected. | Use `anyOf` unless branches are truly exclusive. |
| `required` inside `properties` | Writing `"required": true` on a field (old Draft 3 style) is not a 2020-12 rule: validation ignores it, and only `check_schema` complains (`True is not of type 'array'`). | `required` is an **array** at the object level; always run `check_schema`. |
| No `$schema` | The validator may guess a different draft. | Always declare `2020-12`. |

The single best habit: for every rule you add, write **one instance that must pass and one that must fail**, and check both. That is just testing applied to the contract itself, which you will do systematically with sample input/output pairs later today.

### 15. Tooling and Where Else You Will Meet JSON Schema

- **Online validators.** Sites linked from json-schema.org's tools page let you paste a schema and an instance and see errors instantly. Useful for quick experiments; never paste confidential data (Wednesday's **Responsible use of AI in QE** applies to any website, not just AI tools).
- **Editor support.** VS Code and JetBrains IDEs understand JSON Schema. If a JSON file contains a `"$schema"` key, or you map files to a schema in settings, the editor underlines invalid values and auto-completes field names as you type. This is a great way to write sample input/output pairs.
- **API testing.** OpenAPI (Swagger) documents describe request and response bodies with a dialect of JSON Schema, so the same keywords appear when you test REST APIs in Project 2.
- **Model APIs.** Several LLM providers offer **structured outputs** features where you pass a JSON Schema with the request and the model is constrained to produce JSON matching it. These features usually support only a **subset** of keywords and may have their own limitations, so you still validate the result yourself. Contracts and validation stay your responsibility; how an agent uses them is part of **Friday's** build.

---

## Practice Exercises

1. **Read it aloud.** Without running code, decide whether each instance is valid against the `test_case` definition in the output schema, and name the keyword that fails if not:
   a) `{"id": "TC-205-07", "title": "Second coupon is rejected", "ac_ids": ["AC4"], "type": "negative", "priority": "medium", "steps": ["Apply SAVE10", "Apply WELCOME5"], "expected_result": "Second coupon rejected"}`
   b) the same, but `"priority": "urgent"`
   c) the same as (a), but with `"notes": "check with PO"` added
   d) the same as (a), but `"ac_ids": []`
   Then check your answers with Python.
2. **Build a schema from scratch.** Write a Draft 2020-12 schema for a bug report with: `bug_id` (pattern `BUG-` plus 4 digits, required), `severity` (`critical`, `major`, `minor`, required), `steps_to_reproduce` (non-empty array of strings, required), `browser` (optional string) and no other fields. Write two passing and three failing instances and validate them with `iter_errors`.
3. **Plant your own errors.** Copy `us205_output.json`, plant five different mistakes (include one inside `ac_ids`, one in `open_questions` and one extra field), and predict the exact error paths before running the validation from section 13.
4. **Refactor with `$defs`.** Rewrite the input schema so the acceptance criterion object lives under `$defs/acceptance_criterion` and is referenced with `$ref`. Confirm `us205_input.json` still validates.
5. **Find the hole.** A teammate's schema for `priority` is `{"type": "string", "pattern": "high|medium|low"}`. Find two invalid values that pass, then give two different fixes.

---

## Knowledge Check

1. What is the difference between a schema and an instance?
2. An object schema has `properties` for `id` and `title` but no `required`. Is `{}` valid? Why?
3. What does `additionalProperties: false` protect against in agent output?
4. In `^TC-[0-9]{3}-[0-9]{2}$`, what do `{3}` and `$` mean?
5. You set `"default": 10` on `max_cases`. After validating `{}`, what is the value of `max_cases` in your data?
6. Why does `{"oneOf": [{"type": "integer"}, {"type": "number"}]}` reject `5`?
7. What is the practical difference between `validate()` and `iter_errors()`?
8. Can the output schema check that every `ac_ids` entry exists in the input story? Why or why not?

<details>
<summary>Answers</summary>

1. The schema is the JSON document describing the rules; the instance is the JSON data being checked against those rules.
2. Yes. `properties` only constrains fields **if they are present**. Without `required`, every field is optional.
3. Typos in field names (`expected_reslt`), invented extra fields and unrequested commentary. Without it, such fields pass silently and downstream code may break or ignore them.
4. `{3}` means exactly three of the previous item (three digits). `$` means end of string, so nothing may follow.
5. There is no `max_cases` in the data; validation never fills defaults. Code must apply the default itself.
6. `5` is both an integer and a number, so it matches **two** branches, and `oneOf` requires exactly one.
7. `validate()` raises a single `ValidationError` (or returns `None`); `iter_errors()` yields every error, each with a `path` and `message`, so you can report everything at once.
8. No. A schema checks one document on its own; it cannot look at another document (the input). That cross-check (rule R2) needs extra code, covered in the next lesson.

</details>

---

## Glossary

- **JSON Schema:** A JSON-based vocabulary for describing and validating the structure of JSON data.
- **Schema / instance:** The rules, and the data checked against them.
- **Validator:** A program that checks an instance against a schema and reports errors.
- **Draft:** A published version of the JSON Schema specification; this course uses 2020-12.
- **`$schema`:** Keyword declaring which draft a schema uses.
- **`$id`:** Keyword giving a schema a unique identifier (URL-shaped).
- **Keyword:** A named rule or annotation inside a schema, such as `type` or `pattern`.
- **Sub-schema:** A schema nested inside another, for example under `properties` or `items`.
- **Closed object:** An object schema with `additionalProperties: false`, which rejects unlisted fields.
- **Regular expression (regex):** A pattern language for text; `^` and `$` anchor it to the start and end.
- **Annotation:** A keyword that documents but does not validate (`title`, `description`, `default`, `examples`, and `format` by default).
- **`$defs` / `$ref`:** A place to define reusable sub-schemas, and a pointer that reuses one.
- **Error path:** The location of a validation error inside the instance, for example `test_cases/0/id`.
- **Structured outputs:** A model-API feature that constrains a model's response to match a supplied JSON Schema (usually a subset of keywords).

---

## Summary

- JSON has six value types; `json.loads` checks only that text is well-formed, not that it has the right **shape**.
- **JSON Schema** describes the allowed shape of JSON in JSON. Declare the draft with `$schema` (2020-12 in this course).
- Build object schemas in four steps: `type`, `properties`, `required`, `additionalProperties: false`. Without `required`, fields are optional; without closing the object, extra fields pass.
- Tighten values with string (`minLength`, `maxLength`, anchored `pattern`), choice (`enum`, `const`), number (`minimum`, `maximum`, `exclusiveMinimum`, `multipleOf`) and array (`items`, `minItems`, `uniqueItems`, `prefixItems`) keywords.
- Reuse with `$defs` and `$ref`. `title`, `description`, `examples` and `default` are annotations; **`default` never fills data**, and `format` is not checked unless you enable it.
- `anyOf`/`oneOf`/`allOf`/`not` combine schemas; prefer `anyOf` unless you mean "exactly one". Conditional `if`/`then` rules are next.
- In Python, use `Draft202012Validator.check_schema`, `validate` for a quick yes/no, and `iter_errors` to list **all** errors with their paths. You need `jsonschema` 4.x.
- Schemas check one document at a time; cross-field and input-versus-output rules (R1-R6) need extra code, covered in **Required fields and validation rules**. Full validation scripts come on **Friday**.

---

## Additional Resources

- JSON Schema, *Creating your first schema* (official step-by-step tutorial that builds a schema keyword by keyword; verified live 2026-10-18): https://json-schema.org/learn/getting-started-step-by-step
- JSON Schema, *Understanding JSON Schema – reference* (official guide to every keyword, with draft-specific notes; verified live 2026-10-18): https://json-schema.org/understanding-json-schema
- python-jsonschema, *Schema Validation* (library docs for `Draft202012Validator`, `iter_errors`, `FormatChecker`; shows version 4.26.0; verified 2026-10-18): https://python-jsonschema.readthedocs.io/en/stable/validate/
