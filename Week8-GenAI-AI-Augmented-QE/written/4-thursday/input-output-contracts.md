# Input/Output Contracts

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an **input/output (IO) contract** is, using everyday and software analogies, and describe its three classic parts from **design by contract**: **preconditions**, **postconditions** and **invariants**.
- Explain **why an AI agent needs a contract even more than ordinary code does**, and show with a small Python example how a consumer breaks when an agent's output shape drifts.
- Identify the **producers** and **consumers** of an agent's input and output, and distinguish the **input contract** from the **output contract**.
- List the eight things a good contract specifies: field names, types, required/optional, allowed values, formats, ranges, meaning, the error/clarification shape and the version.
- Write a contract **in plain English first** (a contract table) for the TestCaseDesigner agent, and recognise how the same rules are expressed in **JSON Schema**.
- Use the **`status` + `open_questions`** pattern so an agent can say "I can't" instead of guessing.
- Explain how a contract becomes a **testable QA artifact** (contract testing, consumer-driven contracts), and how to **version** a contract with semantic versioning, telling breaking changes from non-breaking ones.

---

## Why This Matters

Earlier today you met the **anatomy of an agent**: a model, its instructions, its prompt templates and the pieces that connect it to the rest of your system. This lesson is about the **edges** of that agent: exactly what goes **in** and exactly what comes **out**.

On Tuesday you used **format locking** to ask a model for JSON instead of prose. That was a good first step, but a prompt that says "return JSON" is a *request*, not a *promise*. The model may still rename a field, skip one, change a list into a string or add a chatty sentence before the JSON. When a person reads that output, they shrug and adapt. When **code** reads it, such as a pytest file, a CSV exporter for your test-management tool or another agent, it crashes, or worse, it quietly does the wrong thing.

An **IO contract** turns "please return JSON like this" into a **written, versioned, checkable agreement** that everyone (the agent, the code around it and the humans who review it) can rely on. It is the piece that makes an agent safe to plug into an automated pipeline.

This is the "design and build their first QA agent **with IO contracts**" part of the **Weekly Epic**. It also feeds **Project 2 (Test Automation Framework)**: in today's pair exercise you design a contract for a requirements agent, and on Friday you build an agent around one. A contract is also a very natural artifact for a QA engineer to own: it is a specification you can test against, just like a requirement.

> **Scope note.** This lesson is about **what a contract is, what it contains and how to design one**. You will see the TestCaseDesigner contract written in plain English and in JSON Schema, and a couple of one-line validation calls that show a contract catching problems. The keyword-by-keyword explanation of JSON Schema is the next lesson, **JSON Schema**; rules that a schema cannot express (R1-R6) are in **Required Fields and Validation Rules**; example inputs with expected outputs are in **Sample Input/Output Pairs**. **Implementing IO contracts in a running agent**, **agent output validation** and **building validation scripts** are covered on **Friday**.

---

## The Concept

### 1. What Is a Contract?

A **contract** is an agreement between two parties about **what each side will provide and what each side can expect**. You use contracts every day without calling them that.

**The restaurant order slip.** When a waiter takes your order, they do not write "the customer would like something tasty". They write on a slip with fixed boxes: table number, dish, quantity, side, special requests. The kitchen knows exactly where to look for each piece of information. If the slip says "Table: 7, Dish: Margherita, Qty: 2", the kitchen can act without asking. If the waiter wrote a poem instead, the kitchen would stall.

The slip works because both sides agreed in advance on:

- **What goes in** (the order): which boxes exist, which must be filled, what values are allowed ("Qty" must be a number; "Dish" must be on the menu).
- **What comes out** (the plates): the right dish, the right quantity, delivered to the right table.
- **What happens when something is wrong**: if the kitchen is out of an ingredient, they do not invent a substitute; they send the waiter back to **ask**.

**The API contract.** In software you have already met the same idea in the REST API testing you have done before this week. A REST endpoint such as `POST /cart/coupon` has a contract: the request must include certain fields of certain types, and the response will have a documented status code and a documented JSON body. API testers check that the real service honours that contract. Teams often write it down formally, for example in an OpenAPI specification.

An **agent IO contract** is the same idea applied to an AI agent:

> An **input/output contract** is a precise, written agreement that defines what an agent **accepts** as input, what it **promises** to return as output, and what it returns when it **cannot** do the job.

### 2. Design by Contract: Preconditions, Postconditions, Invariants

In the 1980s Bertrand Meyer popularised a style of programming called **design by contract**. It describes any component (a function, a class, a service or an agent) using three kinds of rule. These three words are worth learning because they give you a precise vocabulary for reviewing any contract.

| Term | Plain meaning | Who must honour it | TestCaseDesigner example |
|---|---|---|---|
| **Precondition** | What must be true **before** the component runs | The **caller** | The input has a `story_id` like `US-205` and at least one acceptance criterion. |
| **Postcondition** | What the component guarantees will be true **after** it runs | The **component** | The output has `contract_version`, `story_id`, `status`, `test_cases` and `open_questions`, each with the right type. |
| **Invariant** | What is **always** true, no matter which input or run | The **component**, every time | Test case IDs always look like `TC-205-01`; the output is always one JSON object, never prose. |

The neat thing about this split is that it tells you **whose fault a failure is**:

- If a precondition is broken (someone sends a story with no acceptance criteria), the **caller** made the mistake. The agent should not even be called; the input should be **rejected at the door**.
- If a postcondition is broken (the agent's output is missing `story_id`), the **agent** made the mistake. The output should be **rejected before anyone uses it**.

For a tester, this is gold. When something goes wrong in an agent pipeline, the contract tells you where to look and who must fix it.

### 3. Why Agents Need Contracts More Than Ordinary Code Does

An ordinary Python function such as `apply_coupon(subtotal, code)` has a fairly stable shape. If it returns a `Decimal` today, it returns a `Decimal` tomorrow, because the code is the same. An LLM-based agent is different in two important ways you learned about on Monday and Tuesday:

1. **Its output is generated, not computed.** The model predicts tokens. Even with the same prompt, a different run, a different model version or a small wording change can produce a different shape: `testCases` instead of `test_cases`, `"AC1"` instead of `["AC1"]`, an extra `"notes"` field, a missing `story_id`.
2. **Its output is free text by default.** The model can always write *something*. It never "crashes" the way a function does; it produces plausible-looking text even when it has misunderstood. Problems therefore show up **downstream**, in whichever code consumes the output.

Let us see this with a real consumer. Imagine the TestCaseDesigner's output feeds a helper that builds parameters for `@pytest.mark.parametrize`. We use a deterministic `fake_llm` stand-in (as on Monday to Wednesday) so the example runs offline and gives the same answer every time. The two replies are **illustrative**: the "tuesday" variant shows the kind of drift real models produce.

```python
# consumer_demo.py
import json

def fake_llm(prompt: str, variant: str = "monday") -> str:
    """Deterministic stand-in for an LLM. Returns canned, ILLUSTRATIVE replies.
    'monday' = the shape we expect; 'tuesday' = the same agent drifting."""
    if variant == "monday":
        return json.dumps({
            "story_id": "US-205",
            "test_cases": [
                {"id": "TC-205-01", "title": "SAVE10 applied at exactly $50.00",
                 "ac_ids": ["AC1"], "expected_result": "Total is $45.00"},
                {"id": "TC-205-02", "title": "SAVE10 rejected at $49.99",
                 "ac_ids": ["AC2"], "expected_result": "Total stays $49.99"},
            ],
        })
    return json.dumps({
        "storyId": "US-205",
        "testCases": [
            {"id": "TC-205-01", "title": "SAVE10 applied at exactly $50.00",
             "ac": "AC1", "expected": "Total is $45.00"},
        ],
    })

def to_pytest_params(reply_text: str) -> list[tuple[str, str]]:
    """The CONSUMER: turns the agent reply into (id, expected_result) pairs
    for @pytest.mark.parametrize. It silently relies on the reply's shape."""
    data = json.loads(reply_text)
    return [(tc["id"], tc["expected_result"]) for tc in data["test_cases"]]

for day in ["monday", "tuesday"]:
    reply = fake_llm("Design test cases for US-205", variant=day)
    try:
        print(day, "->", to_pytest_params(reply))
    except KeyError as err:
        print(day, "-> KeyError:", err)
```

Output:

```
monday -> [('TC-205-01', 'Total is $45.00'), ('TC-205-02', 'Total stays $49.99')]
tuesday -> KeyError: 'test_cases'
```

**How the code works:**

- `json.loads(reply_text)` turns the JSON text into a Python dictionary. On Tuesday you saw that this step alone can fail if the model adds prose around the JSON; here both replies are valid JSON, so parsing succeeds.
- `data["test_cases"]` and `tc["expected_result"]` are the consumer's **hidden assumptions**. Nothing in the code *declares* them; they are buried in square brackets.
- On "tuesday" the reply is perfectly valid JSON and perfectly readable to a human, yet the consumer crashes with `KeyError: 'test_cases'` because the key is now called `testCases`. Had it got past that, it would have crashed again on `expected_result` (now `expected`).

Notice three uncomfortable facts:

1. The **agent did not fail**. It returned confident, well-formed JSON.
2. The failure appeared **far away** from its cause, inside the test-generation helper.
3. The consumer's expectations were **never written down**, so nobody could check the reply against them before using it.

A contract fixes all three. It writes the expectations down **once**, in one place, in a form both humans and code can check, and it lets you reject a bad reply **at the boundary**, with a clear message, before any consumer touches it.

### 4. Producers and Consumers

Every contract has two sides:

- The **producer** creates the data.
- The **consumer** uses the data.

An agent sits in the middle, so it is a **consumer** of its input and a **producer** of its output:

```
  PRODUCERS of input                AGENT                    CONSUMERS of output
  ------------------           -----------------           ----------------------
  Story exporter (Jira CSV) --> |                 | -->  pytest parametrize helper
  A tester's script         --> | TestCaseDesigner| -->  TestRail CSV exporter
  Another agent (Week 9)    --> |                 | -->  Human reviewer (Wednesday checklist)
                               -----------------           A dashboard / report
         ^ input contract                ^ output contract ^
```

Why does this matter?

- The **input contract** protects the agent from bad callers. If a script sends `"story_id": "205"`, the input contract rejects it before you pay for a model call that would produce nonsense.
- The **output contract** protects every consumer from a bad agent. One check at the boundary protects the pytest helper, the CSV exporter and the dashboard at once, instead of each consumer writing its own defensive code.
- Consumers often have **different needs**. The pytest helper needs `id` and `expected_result`; the CSV exporter also needs `priority` and `steps`; the reviewer needs `ac_ids` for traceability. The output contract must satisfy **all** of them. Keep a list of consumers next to the contract so you know who is affected when it changes (section 11).

### 5. Input Contract vs. Output Contract

Both halves are needed, and they answer different questions:

| | Input contract | Output contract |
|---|---|---|
| **Question it answers** | "What may I send to the agent?" | "What will the agent send back?" |
| **Design-by-contract role** | Preconditions | Postconditions and invariants |
| **Who breaks it** | The caller | The agent (the model) |
| **When to check** | Before calling the model | After the model replies, before anything uses the reply |
| **Typical failure** | Missing acceptance criteria, malformed story ID, `max_cases` of 500 | Renamed fields, missing fields, wrong types, invented values, prose instead of JSON |
| **What to do on failure** | Reject with a clear message; do not call the model | Reject the reply; do not pass it to consumers (what happens next is covered on Friday and in Week 9) |

A common beginner mistake is to design only the output contract ("I just want good JSON back"). But **garbage in, garbage out** applies strongly to LLMs: a story with no acceptance criteria invites the model to invent requirements, which you saw on Wednesday is one of the most dangerous AI mistakes. A strict input contract is your first defence against invented requirements.

### 6. What a Contract Specifies

A useful contract answers eight questions for **every** field. Use this as a checklist when you design or review one.

| # | Element | Question it answers | Example from TestCaseDesigner |
|---|---|---|---|
| 1 | **Field name** | What exactly is it called, including spelling and case? | `story_id` (snake_case, not `storyId`) |
| 2 | **Type** | String, integer, number, boolean, array, object, null? | `max_cases` is an integer, not `"6"` |
| 3 | **Required / optional** | Must it always be present? | `story_id` required; `techniques` optional |
| 4 | **Allowed values** | Is it limited to a fixed set? | `type` is one of `positive`, `negative`, `boundary` |
| 5 | **Format** | Does a string follow a pattern? | Test IDs look like `TC-205-01` |
| 6 | **Range / size** | Minimum, maximum, length, number of items? | `max_cases` between 1 and 20; at least one acceptance criterion |
| 7 | **Meaning (semantics)** | What does the value *mean*, and how does it relate to other fields? | `ac_ids` lists the input ACs this test case verifies, and must refer to ACs that really exist |
| 8 | **Error / clarification shape** | What does the agent return when it cannot do the job? | `status: "needs_clarification"` plus `open_questions` |

And for the contract as a whole:

- **Version**: which version of the contract is this? (`contract_version: "1.0.0"`, section 12.)
- **Extra fields**: are unknown fields allowed or rejected? (TestCaseDesigner rejects them, so typos like `expectedResult` are caught instead of silently ignored.)

Elements 1 to 6 are about **shape** and can be checked mechanically with JSON Schema. Element 7, **meaning**, is partly beyond what a schema can check. Keep that distinction in mind; it comes back in section 10.

### 7. Writing the TestCaseDesigner Contract in Plain English First

A strong habit: **write the contract for humans before you write it for machines.** A plain-English table is easy to discuss with a product owner, a developer and your pair partner. Only once everyone agrees do you translate it into JSON Schema. If you start with the schema, the conversation becomes about curly braces instead of about what the agent should do.

#### 7.1 The agent in one sentence

> **TestCaseDesigner v1.0.0** takes **one** user story with acceptance criteria and returns **test cases as JSON**, or a list of clarifying questions when the story is too vague to test.

#### 7.2 Input contract (preconditions)

| Field | Type | Required | Rules | Meaning | Example |
|---|---|---|---|---|---|
| `story_id` | string | Yes | `US-` followed by exactly 3 digits | Identifier of the story being tested | `"US-205"` |
| `title` | string | Yes | 5 to 120 characters | Short human title of the story | `"Apply coupon at checkout"` |
| `acceptance_criteria` | array of objects | Yes | At least 1 item; each item has only `id` and `text` | The testable rules of the story | see below |
| `acceptance_criteria[].id` | string | Yes | `AC` followed by digits | Label used for traceability | `"AC1"` |
| `acceptance_criteria[].text` | string | Yes | At least 10 characters | The criterion, copied from the story | `"SAVE10 gives 10% off a subtotal of $50.00 or more."` |
| `techniques` | array of strings | No | Each one of `EP`, `BVA`, `decision_table`, `state_transition`; no duplicates | Test design techniques to apply (from Tuesday) | `["EP", "BVA"]` |
| `max_cases` | integer | No | 1 to 20; default 10 | Upper limit on the number of test cases | `6` |
| *(any other field)* | | Not allowed | Rejected | Prevents typos such as `acceptanceCriteria` slipping through | |

#### 7.3 Output contract (postconditions and invariants)

| Field | Type | Required | Rules | Meaning |
|---|---|---|---|---|
| `contract_version` | string | Yes | Exactly `"1.0.0"` | Which contract this reply follows |
| `story_id` | string | Yes | `US-` + 3 digits; must equal the input `story_id` | Which story these tests belong to |
| `status` | string | Yes | `ok` or `needs_clarification` | Whether the agent could do the job |
| `test_cases` | array | Yes (may be empty) | Each item is a test case (below) | The designed tests |
| `open_questions` | array of strings | Yes (may be empty) | Each at least 5 characters | Questions for the product owner instead of guesses |
| *(any other field)* | | Not allowed | Rejected | Keeps the shape predictable |

Each **test case**:

| Field | Type | Required | Rules | Meaning |
|---|---|---|---|---|
| `id` | string | Yes | `TC-` + 3 digits + `-` + 2 digits, e.g. `TC-205-01` | Unique test ID; middle digits match the story number |
| `title` | string | Yes | 10 to 100 characters | What the test checks |
| `ac_ids` | array of strings | Yes | At least 1; `AC` + digits; no duplicates | Which acceptance criteria this test verifies (traceability) |
| `type` | string | Yes | `positive`, `negative` or `boundary` | Kind of test |
| `priority` | string | Yes | `high`, `medium` or `low` | Execution priority |
| `preconditions` | array of strings | No | | State needed before the steps |
| `steps` | array of strings | Yes | At least 1; each at least 3 characters | Actions to perform |
| `expected_result` | string | Yes | At least 5 characters | The observable outcome that decides pass or fail |

#### 7.4 A valid input and output

Here is a valid input for US-205 (this is the canonical sample used in all of today's lessons):

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

And a reply that honours the output contract (illustrative):

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

Read the reply against the tables. Every required field is present, every value has the right type, every test ID matches the `TC-205-NN` pattern, and AC4, which really is ambiguous, shows up as an **open question** rather than an invented rule. That last point deserves its own section.

### 8. Saying "I Can't": The `status` + `open_questions` Pattern

On Wednesday you saw that one of the worst things an AI can do with a requirement is **fill a gap with a confident guess**. A contract that only describes the "happy" output quietly encourages this: if the only valid reply is a list of test cases, the model will produce test cases, even for a story it cannot test.

So a good agent contract gives the agent an **honest way out**. TestCaseDesigner does this with two fields:

- `status` is either `"ok"` (I designed tests) or `"needs_clarification"` (the story is too vague for me to design trustworthy tests).
- `open_questions` holds the specific questions a human must answer.

Both fields are **always present**, even when empty, so consumers never need to check whether they exist. Here is a valid reply (illustrative) for a story whose only criterion is the deliberately vague US-310 AC4, "the form must be fast and user-friendly":

```json
{
  "contract_version": "1.0.0",
  "story_id": "US-310",
  "status": "needs_clarification",
  "test_cases": [],
  "open_questions": [
    "AC4: what response time counts as \"fast\" (for example, under 2 seconds at the 95th percentile)?",
    "AC4: which checks define \"user-friendly\" (for example, inline error messages, keyboard navigation)?"
  ]
}
```

This is the restaurant kitchen sending the waiter back to ask, instead of inventing a dish.

There are two levels of "I can't":

1. **Partly unclear** (US-205 AC4): `status` stays `"ok"`, the clear ACs get test cases, and the unclear one goes into `open_questions`.
2. **Not testable at all** (vague US-310 AC4 on its own): `status` is `"needs_clarification"`, `test_cases` may be empty, and `open_questions` must say why.

Consumers can now behave sensibly. The pytest helper only uses replies with `status == "ok"`; a reporting script collects every `open_questions` entry and sends them to the product owner. The rule that ties these together ("`needs_clarification` requires at least one question; `ok` requires at least one test case") is rule **R6**, which you will meet properly in *Required Fields and Validation Rules*.

> **Design tip.** Never let the error shape be "anything goes", such as a free-text apology. The error path is part of the contract, so it gets the same fixed fields as the success path. A consumer should be able to handle **every** possible reply with one `if status == ...` branch.

### 9. From Plain English to JSON Schema

Tables are great for people, but code cannot read them. The industry-standard way to write a JSON contract that code **can** check is **JSON Schema**: a JSON document that describes the allowed shape of other JSON documents. You will learn its keywords one by one in the next lesson. For now, simply notice that **every row of the tables in section 7 appears in the schema**.

Here is the canonical input contract, `tcd_input.schema.json`:

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

And the canonical output contract, `tcd_output.schema.json`:

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

A quick translation guide from the plain-English table to the schema (details next lesson):

| Plain English (section 7) | Where it shows up in the schema |
|---|---|
| "Field names and types" | `properties` with a `type` for each field |
| "Required: Yes" | the `required` list |
| "Allowed values" | `enum` (a fixed list) or `const` (exactly one value) |
| "Format" | `pattern` (a regular expression) |
| "Range / size" | `minimum`, `maximum`, `minLength`, `maxLength`, `minItems` |
| "Any other field: not allowed" | `"additionalProperties": false` |
| "Each test case looks like..." | a reusable definition in `$defs`, referenced with `$ref` |

#### 9.1 The contract catches the drift

Now go back to the drifted "tuesday" reply from section 3. Instead of letting the pytest helper crash, check the reply against the output contract **first**. The `jsonschema` library does this; install it with `pip install "jsonschema>=4.18"`. (Some machines still have the old version 3.2, which does not understand Draft 2020-12 schemas; check with `pip show jsonschema`.)

```python
# contract_check.py  (needs: pip install "jsonschema>=4.18")
import json
from jsonschema import Draft202012Validator

with open("tcd_output.schema.json", encoding="utf-8") as f:
    output_contract = json.load(f)

drifted_reply = {
    "storyId": "US-205",
    "testCases": [{"id": "TC-205-01", "ac": "AC1", "expected": "Total is $45.00"}],
}

validator = Draft202012Validator(output_contract)
for error in sorted(validator.iter_errors(drifted_reply), key=lambda e: e.message):
    print("-", error.message)
```

Output:

```
- 'contract_version' is a required property
- 'open_questions' is a required property
- 'status' is a required property
- 'story_id' is a required property
- 'test_cases' is a required property
- Additional properties are not allowed ('storyId', 'testCases' were unexpected)
```

**How the code works:**

- `Draft202012Validator(output_contract)` creates a validator that understands the 2020-12 version of JSON Schema, which our `$schema` line declares.
- `iter_errors(...)` checks the data and yields **every** problem it finds (rather than stopping at the first), so you see the whole picture at once.
- We sort the messages only so the printed order is stable for this lesson.

Compare this with the original `KeyError: 'test_cases'`. The contract check:

- fails **at the boundary**, before any consumer runs;
- names **every** problem, including the renamed fields, in plain words;
- uses one shared definition, so the pytest helper, the CSV exporter and the dashboard are all protected by the same check.

#### 9.2 The same idea guards the input

The input contract works the same way, as a **precondition check** before you call the model:

```python
# precondition_check.py  (needs: pip install "jsonschema>=4.18")
import json
from jsonschema import Draft202012Validator

with open("tcd_input.schema.json", encoding="utf-8") as f:
    input_contract = Draft202012Validator(json.load(f))

good_input = {
    "story_id": "US-205",
    "title": "Apply coupon at checkout",
    "acceptance_criteria": [
        {"id": "AC1", "text": "SAVE10 gives 10% off a subtotal of $50.00 or more."}
    ],
}
bad_input = {"story_id": "205", "title": "Coupons", "acceptance_criteria": []}

for name, candidate in [("good_input", good_input), ("bad_input", bad_input)]:
    problems = [e.message for e in input_contract.iter_errors(candidate)]
    if problems:
        print(f"{name}: REJECTED before calling the agent")
        for p in problems:
            print("   -", p)
    else:
        print(f"{name}: accepted, safe to send to the agent")
```

Output:

```
good_input: accepted, safe to send to the agent
bad_input: REJECTED before calling the agent
   - '205' does not match '^US-[0-9]{3}$'
   - [] should be non-empty
```

The bad input never reaches the model, so you never pay for (or have to review) test cases designed for a story with **no** acceptance criteria. Notice that `good_input` leaves out `techniques` and `max_cases`; they are optional, so the input is still valid.

These two tiny checks only *show* the contract in action. Wiring them into a running agent, deciding what to do with a rejected reply and turning them into proper validation scripts with reports are **Friday's** topics.

### 10. Shape Is Not Meaning

A JSON Schema checks the **shape** of data very well. It cannot check everything a contract *means*. Look at this reply (illustrative). It was produced for **US-205**:

```python
# shape_vs_meaning.py  (needs: pip install "jsonschema>=4.18")
import json
from jsonschema import Draft202012Validator

with open("tcd_output.schema.json", encoding="utf-8") as f:
    validator = Draft202012Validator(json.load(f))

reply = {
    "contract_version": "1.0.0",
    "story_id": "US-101",          # we asked about US-205!
    "status": "ok",
    "test_cases": [
        {"id": "TC-205-01", "title": "SAVE10 applied at exactly $50.00",
         "ac_ids": ["AC9"],         # US-205 has no AC9
         "type": "boundary", "priority": "high",
         "steps": ["Enter coupon SAVE10", "Click Apply"],
         "expected_result": "Total is $45.00"}
    ],
    "open_questions": [],
}
print("Schema errors:", len(list(validator.iter_errors(reply))))
```

Output:

```
Schema errors: 0
```

Zero errors, yet the reply is wrong in three ways: it claims to be about the wrong story, it traces to an acceptance criterion that does not exist, and AC2 to AC4 are not covered at all. Every one of these problems involves **comparing the output with the input**, and a schema only ever looks at one document at a time.

This is why the TestCaseDesigner contract has, alongside its schema, six **semantic rules** written in plain English:

- **R1** output `story_id` equals input `story_id`
- **R2** every `ac_ids` entry exists in the input `acceptance_criteria`
- **R3** every input AC is covered by at least one test case (or appears in `open_questions`)
- **R4** test case IDs are unique and their 3-digit middle part matches the story number (US-205 → `TC-205-NN`)
- **R5** number of test cases <= `max_cases` (default 10)
- **R6** `status` `"needs_clarification"` requires a non-empty `open_questions`; `status` `"ok"` requires at least one test case

The reply above breaks R1, R2 and R3. A complete contract therefore has **two layers**: the **schema** (shape, checkable by a generic tool) and the **semantic rules** (meaning, written down and checked separately). How to design and express these rules is the topic of *Required Fields and Validation Rules* later today. And remember Wednesday: even a reply that passes both layers still needs **human review** of whether the expected results are actually correct. A contract is a safety net, not a substitute for a reviewer.

### 11. The Contract as a Testable QA Artifact

As a QA engineer, you should look at a contract and immediately think: **"This is a specification. I can test against it."**

**Contract testing** means checking that a producer and a consumer agree on the shape of the data they exchange, **without** running the whole system end to end. In the API world, tools like Pact let each side be tested separately against a shared contract file. For an agent, contract testing looks like this:

| Test | What it checks | Example |
|---|---|---|
| Valid input accepted | The input contract is not too strict | `us205_input.json` passes |
| Invalid input rejected | The input contract is strict enough | `story_id: "205"` is rejected |
| Agent output conforms | The agent honours its postconditions | Every reply passes the output schema and R1-R6 |
| Consumer handles every valid shape | Consumers rely only on what the contract promises | The pytest helper handles `status: "needs_clarification"` with an empty `test_cases` list |
| Contract examples are valid | The documentation does not lie | Every sample in the contract folder passes its own schema |

The last row is easy to forget and very common in real projects: a contract document whose own examples do not validate. Checking examples against the schema is a simple, valuable test (you will see more in *Sample Input/Output Pairs*).

**Consumer-driven contracts** are a useful idea from microservice testing. Instead of the producer deciding the output shape alone, **each consumer states what it needs**, and the contract is the union of those needs. For TestCaseDesigner:

- The pytest helper needs: `status`, `test_cases[].id`, `test_cases[].expected_result`.
- The TestRail CSV exporter needs: `id`, `title`, `steps`, `expected_result`, `priority`, `preconditions`.
- The human reviewer needs: `ac_ids` (traceability) and `open_questions`.

Writing these needs down has two benefits. First, it **justifies every required field**: if no consumer needs a field, why make the model produce it? Second, it tells you **who to warn** when the contract changes: removing `priority` would break only the CSV exporter, and you would know that in advance.

This is very close to the API testing you already know. The agent is just another service with a request and a response; the only difference is that the "server code" is a language model, which makes conformance checks **more** important, not less.

### 12. Versioning a Contract

Contracts change. A product owner asks for a `test_data` field; a consumer wants `priority` to have a `critical` level. If the contract changes silently, consumers break silently. That is why TestCaseDesigner's output includes `"contract_version": "1.0.0"`, and why the schema pins it with `const`: a reply that claims to follow a different version is rejected.

The widely used convention for version numbers is **Semantic Versioning (SemVer)**, `MAJOR.MINOR.PATCH`:

- **MAJOR** goes up when you make a **breaking** change (old consumers or producers may fail).
- **MINOR** goes up when you **add** something in a backward-compatible way.
- **PATCH** goes up for backward-compatible **fixes**, such as a clearer description.

The key skill is telling which changes are **breaking**. The answer depends on which side you look at, so think about both producers and consumers:

| Change to the **output** contract | Breaking? | Why | New version |
|---|---|---|---|
| Fix a typo in a `description` | No | Shape and meaning unchanged | 1.0.1 |
| Add an **optional** field `notes` | No (with care) | Old consumers ignore it; old replies without it are still valid. But because v1.0.0 uses `additionalProperties: false`, a v1.0.0 validator would reject replies that include `notes`, so consumers must upgrade their schema copy before the agent starts sending it | 1.1.0 |
| **Rename** `expected_result` to `expected` | **Yes** | Every consumer reading `expected_result` crashes (exactly our `KeyError` demo) | 2.0.0 |
| Make an optional field **required** (e.g. `preconditions`) | **Yes** | Old replies without it now fail validation | 2.0.0 |
| **Tighten** an enum: remove `low` from `priority` | **Yes** | Replies that use `low` now fail | 2.0.0 |
| **Loosen** an enum: add `critical` to `priority` | **Yes for consumers** | Old consumers (e.g. a CSV exporter mapping three priorities) receive a value they do not understand | 2.0.0 (or 1.1.0 only if every consumer is confirmed to cope) |
| Change the **meaning** of a field (e.g. `max_cases` now counts only positive tests) | **Yes** | Shape is identical but behaviour changes, the sneakiest kind of break | 2.0.0 |

Notice the last two rows. "Adding" can be breaking, and a change with **no shape difference at all** can be breaking. Versioning is about promises, not just about JSON structure. When in doubt, ask the consumer list from section 11: "Would any of them behave differently?"

Practical habits:

- Put the version **in the data** (`contract_version`) and **in the schema ID** (`.../output/1.0.0`), so both a reply and a schema file say which version they are.
- Keep the old version's files when you release a new **major** version, so consumers can migrate one at a time.
- Record each change in a short **changelog** next to the contract.
- Changing the agent's instructions or prompt templates in a way that changes the output shape is a contract change too, and must bump the version.

### 13. Where Contracts Live in the Repository

A contract is code-adjacent documentation. It belongs in **version control**, next to the agent, reviewed through pull requests like any other change (you already version prompts in Git from Tuesday). A simple, clear layout for Project 2:

```
project2-test-automation/
├── agents/
│   └── test_case_designer/
│       ├── instructions.md              # agent instructions (earlier today)
│       ├── templates/                   # prompt templates (earlier today)
│       └── contract/
│           ├── README.md                # plain-English contract tables + consumer list
│           ├── CHANGELOG.md             # 1.0.0 – initial contract
│           ├── tcd_input.schema.json    # input contract (preconditions)
│           ├── tcd_output.schema.json   # output contract (postconditions)
│           └── samples/
│               ├── us205_input.json     # sample pairs (later today)
│               └── us205_output.json
└── tests/
    └── ...                              # your pytest suite (consumers)
```

Why this layout works:

- **One source of truth.** Every consumer loads the schema from the same file; nobody copies field names into their own code.
- **Human and machine views side by side.** `README.md` holds the tables from section 7; the `.schema.json` files hold the checkable version. When you change one, the pull request reviewer can check you changed the other.
- **Samples next to the contract.** The examples document the contract and are themselves testable.

### 14. Connecting to Project 2

In Project 2 you are building a test automation framework for a generic e-commerce web app (login, search, cart and checkout). Any AI agent you add to that framework, whether it designs tests, analyses requirements or produces data, should have an IO contract before it produces a single line of output that code depends on. In today's pair exercise you will design the instructions, the schema and sample pairs for a **requirements agent**, and the habits from this lesson apply directly: plain-English table first, then schema; an honest "needs clarification" path; semantic rules written next to the schema; and a version number from day one.

---

## Practice Exercises

1. **Precondition, postcondition or invariant?** Classify each rule for TestCaseDesigner and say who must honour it: (a) `max_cases` is between 1 and 20; (b) the reply is always a single JSON object; (c) the reply's `story_id` equals the input's; (d) every acceptance criterion has an `id` and `text`.
2. **Find the drift.** Write three more "drifted" replies for `consumer_demo.py` (for example, `ac_ids` as a string `"AC1"`, `priority` as `"HIGH"`, a missing `steps`). Predict which ones the pytest helper would *not* notice, then run them through `contract_check.py` and compare.
3. **Plain English first.** For US-101 (login), write the plain-English input table for a *different* agent that returns only negative test cases. Which fields would you keep from TestCaseDesigner, and which would you change?
4. **Consumer needs.** Add a fourth consumer: a Slack notifier that posts "N tests designed for US-205, M open questions". Which output fields does it need? Does the current contract satisfy it?
5. **Version it.** For each change, decide MAJOR, MINOR or PATCH and justify: (a) add optional `estimated_minutes` to each test case; (b) rename `open_questions` to `questions`; (c) add `"exploratory"` to `type`; (d) correct the `title` description.

---

## Knowledge Check

1. In one sentence, what is an input/output contract for an AI agent?

<details><summary>Answer</summary>
A precise, written (and ideally machine-checkable) agreement defining what the agent accepts as input, what it promises to return, and what it returns when it cannot do the job.
</details>

2. Why does an LLM-based agent need a contract more than an ordinary Python function does?

<details><summary>Answer</summary>
Its output is generated rather than computed, so its shape can drift between runs or model versions, and it always produces plausible text instead of crashing. Without a contract, problems surface far downstream in consumers instead of at the boundary.
</details>

3. A script sends `{"story_id": "205", ...}` to the agent. Which part of the contract is broken, and who must fix it?

<details><summary>Answer</summary>
A precondition in the input contract (`story_id` must match `^US-[0-9]{3}$`). The caller must fix it; the input should be rejected before the model is called.
</details>

4. What problem does the `status` + `open_questions` pattern solve?

<details><summary>Answer</summary>
It gives the agent an honest, structured way to say "I can't design trustworthy tests for this" instead of guessing or inventing requirements, and lets every consumer handle every reply with the same fixed fields.
</details>

5. A reply passes the output JSON Schema with zero errors. Can you conclude it honours the contract?

<details><summary>Answer</summary>
No. The schema checks shape only. Semantic rules such as R1 (same story_id as input), R2 (ac_ids exist in the input) and R3 (every AC covered) need comparison with the input, and the content still needs human review.
</details>

6. Is adding `"critical"` to the `priority` enum a breaking change? Explain.

<details><summary>Answer</summary>
For consumers, yes: an old consumer that maps only high/medium/low receives a value it does not understand. It is safe as a minor change only if every consumer is confirmed to cope. Loosening an output enum is a classic "looks harmless" breaking change.
</details>

7. What is the main idea of consumer-driven contracts, and what two benefits does it bring?

<details><summary>Answer</summary>
Each consumer states the fields it needs, and the contract is built from those needs. It justifies every required field, and it tells you exactly which consumers are affected when the contract changes.
</details>

---

## Glossary

- **IO contract:** A written, versioned agreement on what an agent accepts and returns, including its error/clarification shape.
- **Input contract:** The rules the input must satisfy before the agent is called (preconditions).
- **Output contract:** The rules the agent's reply must satisfy before anyone uses it (postconditions and invariants).
- **Precondition / postcondition / invariant:** What must be true before a component runs / what it guarantees after / what is always true.
- **Design by contract:** A style of specifying components with preconditions, postconditions and invariants, popularised by Bertrand Meyer.
- **Producer / consumer:** The party that creates data / the party that uses it.
- **Drift:** An agent's output shape or content changing between runs, prompts or model versions.
- **Shape vs. meaning:** Structure and types (checkable with JSON Schema) vs. what values mean and how they relate to the input (semantic rules).
- **Contract testing:** Checking that producers and consumers honour a shared contract without running the whole system.
- **Consumer-driven contract:** A contract assembled from the stated needs of each consumer.
- **Semantic Versioning (SemVer):** `MAJOR.MINOR.PATCH` version numbers, where MAJOR signals a breaking change.
- **Breaking change:** A change after which some existing producer or consumer may fail or behave differently.

---

## Summary

- An **IO contract** is a precise agreement about what an agent **accepts**, what it **returns**, and what it returns when it **cannot** do the job. Think of the restaurant order slip, or the API contracts you have tested before.
- Design by contract gives you the vocabulary: **preconditions** (the caller's duty), **postconditions** and **invariants** (the agent's duty). This tells you whose fault a failure is.
- Agents need contracts **more** than ordinary code because LLM output **drifts** and never "crashes"; without a contract, failures surface far away in consumers, as the `KeyError` demo showed.
- A good contract specifies, for every field: **name, type, required/optional, allowed values, format, range, meaning**, plus the **error/clarification shape** and a **version**.
- Write the contract in **plain English first**, agree on it, then express it in **JSON Schema** (next lesson). Keep semantic rules (**R1-R6**) alongside the schema, because **shape is not meaning**.
- Give the agent an honest way out with **`status` + `open_questions`**, so it asks instead of guessing.
- Treat the contract as a **testable QA artifact**: contract tests, valid sample files, and a **consumer list** in the spirit of consumer-driven contracts.
- **Version** contracts with SemVer; renaming, removing, tightening, loosening an output enum and changing meaning are all **breaking**. Keep contracts in Git next to the agent.
- Implementing contracts in a running agent, output validation and validation scripts follow on **Friday**.

---

## Additional Resources

- Ian Robinson, *Consumer-Driven Contracts: A Service Evolution Pattern* (martinfowler.com; the classic article on letting consumers' needs shape a contract and evolving it safely): https://www.martinfowler.com/articles/consumerDrivenContracts.html
- Pact Docs, *How Pact works* (a short, visual introduction to contract testing between a consumer and a provider, tested separately against a shared contract): https://docs.pact.io/getting_started/how_pact_works
- *Semantic Versioning 2.0.0* (the official SemVer specification: when to bump MAJOR, MINOR and PATCH): https://semver.org/
