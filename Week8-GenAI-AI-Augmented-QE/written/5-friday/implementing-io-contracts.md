# Implementing IO Contracts

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what it means to **implement** an input/output (IO) contract, as opposed to **designing** one: schemas on disk, code that enforces them at the agent's boundaries, and version numbers that must agree.
- Name the four **enforcement points** in the TestCaseDesigner flow: **(A)** the input gate, **(B)** parsing the model's reply, **(C)** the output schema gate and **(D)** handing typed objects to consumers.
- Read `tcd/contract.py` line by line and explain each design choice: a project-relative `ROOT` path, checking schemas at start-up, a `ContractError` that carries a **stage** and a **list of errors**, stable error messages, and **defaults applied in one place**.
- Explain why our `parse_reply` is deliberately **strict** and what it rejects.
- Turn validated output into **typed Python objects** (`dataclasses`) that consumers such as a TestRail export or a pytest suite can use safely.
- Find every place a **contract version** is written down and check, with a script, that they all agree.
- Write and run **contract tests** with pytest that prove the contract code behaves as the contract says.
- Describe what changes together when the contract moves to a new **major** version.

---

## Why This Matters

On Thursday you **designed** the TestCaseDesigner contract. You wrote it in plain English, turned it into two JSON Schema files, chose required fields, drew the validation layers and built sample input/output pairs. That work produced a very good *description* of what the agent accepts and returns.

A description does nothing on its own. A building code written in a binder does not stop a badly built wall; an inspector who checks every wall does. In software, the inspector is **code that runs on every single call**. Until that code exists, the contract is a promise nobody checks.

Today's goal (the **Weekly Epic**) is to *build* your first QA agent. In this lesson the contract stops being a document and becomes part of the running agent:

- Every story is checked **before** we spend money on a model call.
- Every reply is parsed and checked **before** anyone reads it or stores it.
- Every consumer, for example the code that turns test cases into pytest parameters for **Project 2 (Test Automation Framework)**, receives clean, typed objects instead of a raw dictionary that may or may not contain what it expects.

For the e-commerce app in Project 2 this has a practical meaning. If the agent's output goes straight into your test suite, a single missing `expected_result` or a renamed field would crash the suite in CI, far from the real cause. With the contract implemented at the boundary, the failure happens at the right place, with a message that says exactly what is wrong.

> **Scope note.** This lesson implements the **contract layer**: loading schemas, the input gate with defaults, strict parsing, the output **schema** gate and typed objects, plus contract tests. Checking the *meaning* of the output (rules R1 to R6 and the quality warnings Q1 and Q2) is the next lesson, **Agent output validation**; packaging validation as a command-line script is **Building validation scripts**. Wiring everything into a run over a backlog is **Executing agents against QA requirements**. Automatically cleaning up or re-asking for a broken reply (**retry strategies**) is covered in **Week 9**; here a broken reply is simply rejected.

---

## The Concept

### 1. From Designed to Implemented

A short recap of Thursday, so we share the same picture. The TestCaseDesigner contract (version `1.0.0`) has:

- an **input schema**, `schemas/tcd_input.schema.json`: `story_id`, `title` and `acceptance_criteria` are required; `techniques` and `max_cases` are optional, and `max_cases` documents a default of 10;
- an **output schema**, `schemas/tcd_output.schema.json`: a closed object with `contract_version` (always `"1.0.0"`), `story_id`, `status`, `test_cases` and `open_questions`;
- **semantic rules** R1 to R6 that a schema cannot express, and quality rules Q1 to Q3.

An **implemented** contract has three ingredients:

| Ingredient | What it is | Where it lives in our project |
|---|---|---|
| **Schemas** | The machine-readable description of valid input and output | `schemas/*.schema.json` |
| **Enforcement code** | Functions that run the schemas (and related checks) at the agent's boundaries and stop bad data | `tcd/contract.py` |
| **Version agreement** | Every file that mentions the contract version names the same version | schema, `contract.py`, `agent.json`, instructions header, template |

Miss any one and the contract leaks. Schemas without enforcement are documentation. Enforcement without schemas is a pile of hand-written `if` statements that drifts from what the team agreed. Versions that disagree mean the instructions ask the model for one shape while the code checks for another.

Here is where our project stands in today's build. Each Friday lesson adds one layer to the same folder:

```text
tcd_agent/
├── agent.json                 # which instructions, template and contract the agent uses
├── instructions/              # lesson 1: tcd/instructions.py loads these
├── templates/                 # lesson 2: tcd/templates.py renders these
├── schemas/                   # THIS lesson: the two contract files...
│   ├── tcd_input.schema.json
│   └── tcd_output.schema.json
├── samples/                   # Thursday's pairs P01-P05
├── tcd/
│   ├── instructions.py
│   ├── templates.py
│   └── contract.py            # ...and the code that enforces them
└── tests/
    └── test_contract.py       # THIS lesson: contract tests
```

**Setup.** You need Python 3.11 or newer, plus two packages:

```bash
pip install "jsonschema>=4.18" pytest
python -c "import importlib.metadata as m; print(m.version('jsonschema'))"
```

The second line must print `4.18` or higher. Some machines still have `jsonschema` 3.2, which has no `Draft202012Validator`; upgrade it if so. Run every command in this lesson from the `tcd_agent/` folder.

### 2. Where the Contract Is Enforced: Four Points

Think of an airport. Your passport is checked when you enter the departure area, your bag is scanned before it goes on the plane, and the bag is checked again on arrival before it is handed over. Each check happens at a **boundary**, where something moves from one party's hands to another's. Checks in the middle of the plane would be pointless: the damage is done by then.

An agent has the same kind of boundaries. Here is the flow of one TestCaseDesigner call, with the four enforcement points marked:

```text
  caller's story (dict)
          │
          ▼
  (A) INPUT GATE ── check_input() ──── invalid ──► ContractError(stage="input")
          │ valid, defaults applied                (no model call, no cost)
          ▼
  instructions + template ──► model ──► raw reply (str)
                                           │
                                           ▼
  (B) PARSE ──────── parse_reply() ──── not one JSON object ──► ContractError(stage="parse")
          │ dict
          ▼
  (C) OUTPUT SCHEMA GATE ── check_output_schema() ── invalid ──► ContractError(stage="output")
          │ schema-valid dict
          ▼
  [ semantic rules R1-R6, Q1-Q2: next lesson ]
          │
          ▼
  (D) TYPED OBJECTS ── DesignResult.from_dict() ──► consumers (TestRail export, pytest, reports)
```

What each point protects:

- **(A) Input gate.** Protects the **model call**. A story with no acceptance criteria cannot produce good test cases; calling the model anyway wastes time and money and invites invented requirements. It also protects **blame**: an input error is the caller's problem, not the agent's.
- **(B) Parse.** The model returns **text**, never a Python dictionary. Something must turn text into data, and that step can fail (prose, Markdown fences, broken JSON).
- **(C) Output schema gate.** Protects everything **downstream**: no missing fields, no unknown fields, no `"priority": "urgent"`.
- **(D) Typed objects.** Protects **consumers' code**. Instead of `tc["expected_result"]` (a typo becomes a `KeyError` at run time), consumers write `tc.expected_result` on an object that is guaranteed to have that attribute.

Notice the shape of the diagram: every arrow to the right is a **rejection**. That is deliberate. The contract code never "fixes up" bad data silently; it stops it and says why.

### 3. Walking Through `tcd/contract.py`: Loading the Schemas

Let us read the module from top to bottom. First, the imports and the constants:

```python
# tcd/contract.py
"""The TestCaseDesigner IO contract, implemented: load, gate, default, parse, check."""
import json
from dataclasses import dataclass, field
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent      # the project folder
CONTRACT_VERSION = "1.0.0"
INPUT_DEFAULTS = {"techniques": ["EP", "BVA"], "max_cases": 10}
```

#### 3.1 `ROOT`: don't trust the current directory

`__file__` is a special variable that holds the path of the Python file being run, here `.../tcd_agent/tcd/contract.py`. Step by step:

| Expression | Value |
|---|---|
| `Path(__file__)` | `tcd/contract.py` (possibly relative) |
| `.resolve()` | `/home/you/tcd_agent/tcd/contract.py` (absolute, no `..`) |
| `.parent` | `/home/you/tcd_agent/tcd` |
| `.parent.parent` | `/home/you/tcd_agent` (the project folder) |

Why bother? A relative path such as `"schemas/tcd_input.schema.json"` is resolved against the **current working directory**: the folder you happened to be in when you started Python. Run pytest from the project folder and it works; run it from `tests/`, from an IDE with a different working folder, or from a CI job that starts elsewhere, and you get `FileNotFoundError`. Anchoring paths to `ROOT` makes the module find its schemas wherever it is run from.

#### 3.2 `CONTRACT_VERSION` and `INPUT_DEFAULTS`

`CONTRACT_VERSION` is the **single place in Python** that says which contract this code implements. Other modules import it instead of typing `"1.0.0"` themselves (Section 8 shows why).

`INPUT_DEFAULTS` holds the values used when the caller leaves out optional fields. The contract says `max_cases` defaults to 10, and the instructions say "If techniques is missing, use EP and BVA". Section 5 shows where these are applied and why it matters that it happens **here**.

#### 3.3 `_load_validator`: fail fast on a broken schema

```python
def _load_validator(name: str) -> Draft202012Validator:
    schema = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)        # a broken schema fails at start-up
    return Draft202012Validator(schema)


INPUT_VALIDATOR = _load_validator("tcd_input.schema.json")
OUTPUT_VALIDATOR = _load_validator("tcd_output.schema.json")
```

- `ROOT / "schemas" / name` uses the `/` operator, which `pathlib` overloads to join path parts safely on every operating system.
- `json.loads(...)` turns the file's text into a Python dictionary.
- `Draft202012Validator.check_schema(schema)` validates the **schema itself** against the official JSON Schema meta-schema (the schema that describes schemas). A schema can be valid JSON yet a broken schema, for example `"minItems": "one"`.
- `Draft202012Validator(schema)` builds a reusable validator object.
- The two module-level lines run **once, when the module is imported**. The leading underscore in `_load_validator` is a Python convention meaning "internal helper, not for other modules".

Why check the schema at start-up? Without `check_schema`, a typo in a schema can make a keyword silently ineffective, or blow up in the middle of a run on the fiftieth story. With it, the agent refuses to start. Let us prove it. In a **copy** of the project, change the `ac_ids` keyword `"minItems": 1` to `"minItems": "one"` in the output schema and import the module:

```bash
python -c "import tcd.contract"
```

Output (trimmed to the important lines):

```text
Traceback (most recent call last):
jsonschema.exceptions.SchemaError: 'one' is not of type 'integer'

Failed validating 'type' in metaschema[...]['properties']['minItems']:

On schema['$defs']['test_case']['properties']['ac_ids']['minItems']:
    'one'
```

The error names the exact location of the mistake inside the schema. This is the **fail fast** principle: the cheapest moment to find a broken contract is before the first story is processed. Put the file back and the import succeeds again.

### 4. `ContractError` and Error Messages

```python
class ContractError(Exception):
    """Raised when data breaks the contract. .errors holds one message per problem."""
    def __init__(self, stage: str, errors: list):
        super().__init__(f"{stage}: {len(errors)} contract error(s)")
        self.stage = stage
        self.errors = errors
```

This is a **custom exception**: a class that inherits from Python's built-in `Exception`, so it can be raised and caught like any error. It adds two attributes:

- **`stage`**: where the contract was broken: `"input"`, `"parse"` or `"output"`. Callers use it to decide what to do. An `"input"` error goes back to whoever sent the story; a `"parse"` or `"output"` error is the agent's failure and is logged against the agent.
- **`errors`**: a **list** of messages, one per problem. Thursday you chose **collect all errors** over **fail fast** for validation results: a story author who fixes one problem and resubmits, only to be told about the next one, will quickly lose patience.

`super().__init__(...)` calls the parent class's constructor with a short summary, so `print(exc)` shows something like `input: 2 contract error(s)`.

Notice the two different uses of "fail fast". At **start-up** (Section 3.3) we stop at the first broken schema, because nothing can work until it is fixed. For **data**, we collect every problem in one pass, because the person fixing the data wants the full list.

The helper that builds the messages:

```python
def _messages(validator: Draft202012Validator, doc) -> list:
    """Every schema error as 'path: message', in a stable order."""
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '(root)'}: {e.message}" for e in errors]
```

- `validator.iter_errors(doc)` yields **every** schema error (you used it on Thursday).
- `sorted(..., key=lambda e: list(e.absolute_path))` puts errors in order of their location. `iter_errors` does not promise any particular order, and a test that compares messages should not break because the order changed. A stable order makes output **reproducible**.
- `e.absolute_path` is the route from the top of the document to the bad value, for example `['test_cases', 0, 'priority']`. The expression `'/'.join(str(p) for p in ...)` turns it into `test_cases/0/priority`; `str(p)` is needed because list indexes are integers.
- `or '(root)'`: for a problem at the top level the path is empty, and `'/'.join([])` is the empty string `''`, which is "falsy", so `or` substitutes the readable `(root)`.

The result is one string per problem in the form **where: what**, the minimum Thursday's error-message lesson asked for.

### 5. Point (A): The Input Gate and Defaults in One Place

```python
def check_input(story: dict) -> dict:
    """Input gate (S2). Returns a NEW dict with defaults applied, or raises ContractError."""
    problems = _messages(INPUT_VALIDATOR, story)
    if problems:
        raise ContractError("input", problems)
    return {**INPUT_DEFAULTS, **story}        # caller's values win over defaults
```

The first three lines are Thursday's input gate (rule **S2** in the rule catalogue), now raising `ContractError` instead of printing. The new idea is the last line.

#### 5.1 How `{**INPUT_DEFAULTS, **story}` works

`**` inside a dictionary literal **unpacks** a dictionary: it copies all its key/value pairs into the new dictionary. When two unpacked dictionaries contain the same key, the **later one wins**. Work it out by hand for a story that sends `max_cases` but no `techniques`:

```text
INPUT_DEFAULTS = {"techniques": ["EP", "BVA"], "max_cases": 10}
story          = {"story_id": "US-205", "title": "...", "acceptance_criteria": [...], "max_cases": 6}

Step 1, copy INPUT_DEFAULTS:  {"techniques": ["EP","BVA"], "max_cases": 10}
Step 2, copy story on top:    story_id, title, acceptance_criteria added;
                              max_cases 10 is OVERWRITTEN by 6
Result: {"techniques": ["EP","BVA"], "max_cases": 6, "story_id": "US-205", ...}
```

So a default is used **only** when the caller did not send the field. Two more details:

- The function returns a **new** dictionary. The caller's `story` is not modified, so the caller can still see exactly what they sent, which is useful when logging.
- The order of the gate and the defaults matters: we validate the **caller's** story first, then add defaults. If we added defaults first, a wrong default (say `"max_cases": 50`) would be reported as if the caller had sent it.

#### 5.2 Why defaults belong in the contract layer

Look back at Thursday's pieces and you will find a small disagreement:

- The **instructions** (Inputs section) say: "If techniques is missing, use EP and BVA."
- Thursday's **`render.py`** wrote "choose the techniques that fit the story" into the prompt when `techniques` was missing.

Both were sensible on their own, but together they tell the model two different things for the same input. Nobody did anything wrong; the default simply lived in two places, and the two places drifted. This is the classic problem with duplicated logic.

Applying defaults **once**, in `check_input`, fixes it. Every later step works on the **gated story**, which already contains `techniques: ["EP", "BVA"]` and `max_cases: 10`. The template renders "equivalence partitioning, boundary value analysis"; the instructions' sentence now simply agrees with what the model sees; and the validator in the next lesson checks R5 against the same `max_cases` the model was told. The rule to remember: **one fact, one place**.

#### 5.3 Predict, then run

Before running anything, predict:

1. P01's story **without** `techniques` and `max_cases`: which fields will the agent use, with which values?
2. P01's story **as written** (it sends `max_cases: 6`): which `max_cases` wins?
3. P04 (`"story_id": "205"`, `"acceptance_criteria": []`): how many errors, at which paths?

Now run it:

```python
# ex_gate.py
import json
from pathlib import Path
from tcd.contract import ContractError, check_input

p01 = json.loads(Path("samples/P01-happy_path.json").read_text(encoding="utf-8"))["input"]
story = {k: v for k, v in p01.items() if k not in ("techniques", "max_cases")}
gated = check_input(story)
print("caller sent:", sorted(story))
print("agent uses: ", sorted(gated))
print("techniques =", gated["techniques"], "| max_cases =", gated["max_cases"])
print("caller's own max_cases kept:", check_input(p01)["max_cases"])

p04 = json.loads(Path("samples/P04-invalid_input.json").read_text(encoding="utf-8"))["input"]
try:
    check_input(p04)
except ContractError as exc:
    print(f"rejected at stage '{exc.stage}':")
    for msg in exc.errors:
        print("  -", msg)
```

Output:

```text
caller sent: ['acceptance_criteria', 'story_id', 'title']
agent uses:  ['acceptance_criteria', 'max_cases', 'story_id', 'techniques', 'title']
techniques = ['EP', 'BVA'] | max_cases = 10
caller's own max_cases kept: 6
rejected at stage 'input':
  - acceptance_criteria: [] should be non-empty
  - story_id: '205' does not match '^US-[0-9]{3}$'
```

- The dictionary comprehension `{k: v for k, v in p01.items() if k not in (...)}` builds a copy of the input **without** the two optional fields, to simulate a caller who leaves them out.
- `sorted(story)` sorts the dictionary's **keys**, which gives a tidy, predictable printout.
- P04 produces **both** errors in one go (collect all), each with its path. The model was never called.

Did your predictions match? If you expected `max_cases` 10 for the second line, re-read Section 5.1: the caller's 6 is copied **after** the default.

### 6. Point (B): Parsing the Reply Strictly

```python
def parse_reply(reply: str) -> dict:
    """Turn the model's raw text into a dict. The contract says: one JSON object, nothing else."""
    text = reply.strip()
    if text.startswith("```"):
        raise ContractError("parse", ["reply is wrapped in Markdown fences; the contract forbids them"])
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ContractError("parse", [f"reply is not valid JSON: {exc.msg} at line {exc.lineno} column {exc.colno}"])
    if not isinstance(data, dict):
        raise ContractError("parse", [f"reply must be a JSON object, got {type(data).__name__}"])
    return data
```

Line by line:

- `reply.strip()` removes leading and trailing whitespace and newlines. That is harmless: whitespace around a JSON document does not change its meaning.
- `text.startswith("```")` detects a Markdown code fence, the most common format failure you met in Tuesday's failure-modes lesson. We give it its **own** message because it is so common and so easy to recognise in a log.
- `json.loads(text)` raises `json.JSONDecodeError` for anything that is not valid JSON, such as a chatty sentence before the object. The exception object carries `msg`, `lineno` and `colno`, which we copy into the message so a person can find the problem in the raw reply.
- `isinstance(data, dict)` checks that the JSON is an **object**. `json.loads("[1, 2]")` happily returns a list and `json.loads("42")` returns an integer; both are valid JSON but not what the contract promises. `type(data).__name__` gives the readable type name, such as `list`.

#### 6.1 Why strict?

On Tuesday you wrote a **defensive parser** that stripped fences and searched for the first `{`. That is a reasonable tool when *you* are at the keyboard. Inside the contract layer we choose the opposite, for three reasons:

1. **The contract says so.** The output rule in the instructions is "No Markdown fences and no text before or after the JSON." If the code quietly accepts fences, it is enforcing a different contract from the one written down, and nobody will notice the model ignoring that rule.
2. **Measurement.** When you test the agent later today, you want to **count** how often the model breaks the format. A forgiving parser hides that number.
3. **Clear responsibility.** Repairing or re-asking for a broken reply is a separate, deliberate decision with its own trade-offs (cost, latency, risk of masking a real problem). That is **retry strategies**, covered in **Week 9**. Today, a broken reply is rejected and recorded.

#### 6.2 Point (C): The output schema gate

```python
def check_output_schema(output: dict) -> dict:
    """Output gate (S1): shape only. Meaning-level rules come later."""
    problems = _messages(OUTPUT_VALIDATOR, output)
    if problems:
        raise ContractError("output", problems)
    return output
```

This is rule **S1** from the catalogue. It returns the same dictionary when it passes, which lets callers chain the steps in one readable line: `check_output_schema(parse_reply(reply))`.

#### 6.3 Predict, then run: four bad replies

Predict the **stage** and the message for each reply below. Then run:

```python
# ex_replies.py
from tcd.contract import ContractError, check_output_schema, parse_reply

BAD_REPLIES = {
    "fenced": '```json\n{"story_id": "US-205"}\n```',
    "prose":  'Sure! Here are your test cases: {"story_id": "US-205"}',
    "list":   '[{"id": "TC-205-01"}]',
    "wrong object": '{"story_id": "US-205", "tests": []}',
}

for name, reply in BAD_REPLIES.items():
    try:
        check_output_schema(parse_reply(reply))
        print(f"{name}: accepted")
    except ContractError as exc:
        print(f"{name}: stage={exc.stage}")
        for msg in exc.errors:
            print("    ", msg)
```

Output:

```text
fenced: stage=parse
     reply is wrapped in Markdown fences; the contract forbids them
prose: stage=parse
     reply is not valid JSON: Expecting value at line 1 column 1
list: stage=parse
     reply must be a JSON object, got list
wrong object: stage=output
     (root): 'contract_version' is a required property
     (root): 'status' is a required property
     (root): 'test_cases' is a required property
     (root): 'open_questions' is a required property
     (root): Additional properties are not allowed ('tests' was unexpected)
```

Points to notice:

- The first three never reach the schema: you cannot schema-check text that is not a JSON object. That is why `stage` differs.
- "Expecting value at line 1 column 1" for the prose reply means the JSON decoder expected a value at the very first character but found `S`. It is a cryptic message, which is exactly why our message begins with the plain-English "reply is not valid JSON".
- The "wrong object" reply is a JSON object, so parsing succeeds, but the schema gate collects **five** problems at once, with the made-up field `tests` named explicitly (thanks to `"additionalProperties": false`).

### 7. Point (D): Typed Objects for Consumers

After the gates, the output is a plain dictionary that **we know** has the right shape. The last step turns it into objects with named attributes:

```python
# ---- typed objects for consumers (built ONLY from validated output) --------
@dataclass(frozen=True)
class TestCase:
    id: str
    title: str
    ac_ids: list
    type: str
    priority: str
    steps: list
    expected_result: str
    preconditions: list = field(default_factory=list)


@dataclass(frozen=True)
class DesignResult:
    contract_version: str
    story_id: str
    status: str
    test_cases: list
    open_questions: list

    @classmethod
    def from_dict(cls, data: dict) -> "DesignResult":
        cases = [TestCase(**tc) for tc in data["test_cases"]]
        return cls(data["contract_version"], data["story_id"], data["status"],
                   cases, list(data["open_questions"]))
```

#### 7.1 What a dataclass gives you

`@dataclass` is a **decorator** from Python's standard library. You list the fields with type annotations (`id: str`), and Python writes the boring code for you: an `__init__` that takes those fields, a readable `__repr__` for printing, and `__eq__` for comparing two objects. `frozen=True` makes instances **read-only**: assigning `tc.priority = "low"` raises `FrozenInstanceError`. Output from the agent is evidence; consumers should read it, not quietly change it.

Compare the two ways a consumer might read a test case:

```python
tc["expeced_result"]      # typo -> KeyError, only when this line runs
tc.expeced_result         # typo -> AttributeError, and your editor underlines it as you type
```

Editors and type checkers know a dataclass's fields, so many mistakes are caught before the code even runs.

#### 7.2 `TestCase(**tc)` and the optional field

`TestCase(**tc)` uses `**` again, this time in a **function call**: it passes every key of the dictionary `tc` as a **keyword argument**. A test case dictionary `{"id": "TC-205-01", "title": "...", ...}` becomes `TestCase(id="TC-205-01", title="...", ...)`. Because the arguments are passed by **name**, the order of keys in the JSON does not matter.

Two things make this safe:

- **The schema gate has already run.** The output schema says each test case is a **closed** object (`"additionalProperties": false`) with exactly these eight possible fields, seven of them required. So `**tc` can never pass an unexpected keyword (which would raise `TypeError`) or omit a required one. This is why `from_dict` must **only** be called on validated output; the comment above the classes says so.
- **`preconditions` is the only optional field, and it is last.** In a dataclass, fields with defaults must come after fields without defaults, otherwise Python raises `TypeError: non-default argument follows default argument`. That is exactly the shape of the contract: one optional field, so it sits at the end. `field(default_factory=list)` creates a **new empty list** for each test case that has no preconditions. (Writing `= []` directly is forbidden for dataclasses, because one shared list object would be used by every instance.)

`from_dict` is a **class method** (`@classmethod`): it is called on the class, `DesignResult.from_dict(data)`, and receives the class as `cls`, which it calls to build the instance. It is a common Python pattern for "alternative constructors". `list(data["open_questions"])` makes a copy, so the object does not share a list with the original dictionary.

> **pytest tip.** pytest tries to collect any class whose name starts with `Test` from your **test files**. If you import `TestCase` into a test module, pytest may warn that it "cannot collect test class 'TestCase' because it has a `__init__` constructor". It is harmless; import the module (`import tcd.contract as contract`) or the class under an alias if the warning bothers you.

#### 7.3 A consumer in action

Here is a small consumer that does two things a Project 2 framework really needs: list pytest IDs, and print rows in a TestRail-style layout (Wednesday you exported test cases to CSV for TestRail). It reads the **illustrative** US-205 reply stored in `replies/US-205.txt`, written for this course rather than copied from a real model.

```python
# ex_consumer.py
from pathlib import Path
from tcd.contract import DesignResult, check_output_schema, parse_reply

reply = Path("replies/US-205.txt").read_text(encoding="utf-8")   # illustrative reply
result = DesignResult.from_dict(check_output_schema(parse_reply(reply)))

print(f"{result.story_id}: status={result.status}, {len(result.test_cases)} test cases")
print("pytest ids:", [tc.id for tc in result.test_cases])
print("Title | Priority | Steps | Expected")
for tc in result.test_cases:
    print(f"{tc.title} | {tc.priority} | {' > '.join(tc.steps)} | {tc.expected_result}")
for q in result.open_questions:
    print("OPEN:", q)
```

Output:

```text
US-205: status=ok, 3 test cases
pytest ids: ['TC-205-01', 'TC-205-02', 'TC-205-03']
Title | Priority | Steps | Expected
SAVE10 applied at exactly $50.00 | high | Enter coupon SAVE10 > Click Apply | Total is $45.00
SAVE10 rejected at $49.99 | high | Enter coupon SAVE10 > Click Apply | Total stays $49.99 and message "Spend $50.00 to use SAVE10" is shown
Unknown coupon code is rejected | medium | Enter coupon BOGUS > Click Apply | Message "Coupon code not recognised" is shown and total stays $80.00
OPEN: AC4: should a second coupon replace the first or be rejected?
```

The consumer contains **no** checks of its own: no `if "steps" in tc`, no `try/except KeyError`. It can be this simple because the contract layer has already guaranteed the shape. That is the real payoff of implementing the contract at the boundary: **every consumer gets simpler**. Notice also that the open question is printed for a human; it is part of the result, not an error.

> **Shape is not meaning.** This reply is schema-valid, and in this case it is also a good answer. But schema-valid output can still trace a test to an acceptance criterion that does not exist, or forget one entirely. Before results reach consumers in the finished agent, the semantic rules R1 to R6 run between points (C) and (D). That is the next lesson, *Agent output validation*.

### 8. Version Agreement: One Version, Many Places

A contract version is written in more places than people expect. For TestCaseDesigner:

| Where | What it says | Who reads it |
|---|---|---|
| Output schema `contract_version` (`"const": "1.0.0"`) | Every reply must carry exactly this version | The output schema gate |
| Output schema `$id` (`.../output/1.0.0`) | Identifies this schema file | People and tools that reference the schema |
| `tcd/contract.py` `CONTRACT_VERSION` | The version the code implements | Other Python modules |
| `agent.json` `contract_version` | The version this agent build promises | The agent loader, run logs |
| Instructions header `Output contract: 1.0.0` | The version the instructions describe | `load_instructions(..., expected_contract=...)` from lesson 1, and the model |
| `tcd_user_v1.0.0.txt` reminder `contract_version "1.0.0"` | The version the prompt asks for | The model |

The newer template `tcd_user_v1.0.1` (from the template-library lesson) does not hard-code the version: its `output_reminder` partial has a `$contract_version` placeholder, which the agent fills from `CONTRACT_VERSION`. Every hard-coded copy you remove is one copy that can no longer drift. You cannot remove them all, though: JSON Schema files cannot import Python constants. So for the copies that remain, we **check** that they agree.

```python
# check_versions.py
"""Every place that names the contract version must name the SAME version."""
import json
import re
from pathlib import Path

from tcd.contract import CONTRACT_VERSION

def found_versions() -> dict:
    schema = json.loads(Path("schemas/tcd_output.schema.json").read_text(encoding="utf-8"))
    config = json.loads(Path("agent.json").read_text(encoding="utf-8"))
    instructions = Path(config["instructions"]).read_text(encoding="utf-8")
    reminder_v100 = Path("templates/tcd_user_v1.0.0.txt").read_text(encoding="utf-8")
    return {
        "tcd/contract.py CONTRACT_VERSION": CONTRACT_VERSION,
        "output schema contract_version const": schema["properties"]["contract_version"]["const"],
        "output schema $id (last part)": schema["$id"].rsplit("/", 1)[1],
        "agent.json contract_version": config["contract_version"],
        "instructions header": re.search(r"Output contract: (\d+\.\d+\.\d+)", instructions).group(1),
        "tcd_user_v1.0.0.txt reminder": re.search(r'contract_version "(\d+\.\d+\.\d+)"', reminder_v100).group(1),
    }

if __name__ == "__main__":
    versions = found_versions()
    for place, version in versions.items():
        print(f"{version:<7} {place}")
    distinct = set(versions.values())
    print("AGREE" if len(distinct) == 1 else f"DISAGREE: {sorted(distinct)}")
```

Output:

```text
1.0.0   tcd/contract.py CONTRACT_VERSION
1.0.0   output schema contract_version const
1.0.0   output schema $id (last part)
1.0.0   agent.json contract_version
1.0.0   instructions header
1.0.0   tcd_user_v1.0.0.txt reminder
AGREE
```

How it works:

- `schema["$id"].rsplit("/", 1)[1]` splits the `$id` URL once, from the **right**, at the last `/` and takes the last part: `1.0.0`.
- `re.search(r"Output contract: (\d+\.\d+\.\d+)", ...)` finds the version in the instructions header. `\d+` means one or more digits, `\.` is a literal dot, and the parentheses **capture** the version so `.group(1)` returns it.
- `set(versions.values())` keeps only the **distinct** versions. One distinct value means everyone agrees.

Now simulate a common slip: someone bumps `agent.json` to `1.1.0` and forgets the rest. The last two lines become:

```text
1.0.0   tcd_user_v1.0.0.txt reminder
DISAGREE: ['1.0.0', '1.1.0']
```

The script costs nothing to run and catches the mistake in seconds. In the next lessons you will run checks like this automatically, in a test suite and in CI.

### 9. Contract Tests with pytest

A **contract test** checks that the code enforcing a contract behaves as the contract says. It does not call a model and runs in a fraction of a second, so it can run on every change. Our tests use Thursday's sample pairs as test data, which keeps the pairs and the code honest with each other.

```python
# tests/test_contract.py
"""Contract tests: the code that enforces the contract behaves as the contract says."""
import json
from pathlib import Path

import pytest

from tcd.contract import (ContractError, DesignResult, check_input,
                          check_output_schema, parse_reply)

PAIRS = [json.loads(p.read_text(encoding="utf-8"))
         for p in sorted(Path("samples").glob("P0*.json"))]


@pytest.mark.parametrize("pair", PAIRS, ids=[p["pair_id"] for p in PAIRS])
def test_input_gate_matches_pair_intention(pair):
    if pair["input_should_be_valid"]:
        check_input(pair["input"])                    # must not raise
    else:
        with pytest.raises(ContractError) as info:
            check_input(pair["input"])
        assert info.value.stage == "input"


def test_defaults_are_applied_when_missing():
    story = {"story_id": "US-101", "title": "Log in to my account",
             "acceptance_criteria": [{"id": "AC1", "text": "A valid login opens My Account."}]}
    gated = check_input(story)
    assert gated["techniques"] == ["EP", "BVA"]
    assert gated["max_cases"] == 10
    assert "max_cases" not in story                   # the caller's dict is untouched


def test_caller_value_wins_over_default():
    p01 = PAIRS[0]["input"]                           # sends max_cases 6
    assert check_input(p01)["max_cases"] == 6


@pytest.mark.parametrize("reply", [
    '```json\n{"story_id": "US-205"}\n```',
    'Here you go: {"story_id": "US-205"}',
    '[{"id": "TC-205-01"}]',
    '',
], ids=["fences", "prose", "array", "empty"])
def test_parse_reply_rejects_non_contract_text(reply):
    with pytest.raises(ContractError) as info:
        parse_reply(reply)
    assert info.value.stage == "parse"


@pytest.mark.parametrize("pair", [p for p in PAIRS if p["expected_output"]],
                         ids=lambda p: p["pair_id"])
def test_reference_outputs_pass_the_schema_gate(pair):
    reply = json.dumps(pair["expected_output"])
    assert check_output_schema(parse_reply(reply)) == pair["expected_output"]


def test_extra_field_is_rejected_by_schema_gate():
    out = dict(PAIRS[0]["expected_output"], confidence=0.9)
    with pytest.raises(ContractError) as info:
        check_output_schema(out)
    assert info.value.stage == "output"
    assert "'confidence' was unexpected" in info.value.errors[0]


def test_dataclass_round_trip():
    data = PAIRS[2]["expected_output"]                # P03: test case without preconditions
    result = DesignResult.from_dict(check_output_schema(data))
    assert result.story_id == "US-310"
    assert result.test_cases[0].preconditions == []   # optional field gets its default
    assert [tc.id for tc in result.test_cases] == [tc["id"] for tc in data["test_cases"]]
```

Run from the project folder:

```bash
python -m pytest -q tests/test_contract.py
```

```text
.................                                                        [100%]
17 passed in 0.22s
```

Seventeen tests from seven functions, because parametrization expands each parametrized function into one test per value. What each test protects:

1. **`test_input_gate_matches_pair_intention`** (5 tests, one per pair). Uses the pair field `input_should_be_valid` that you added on Thursday precisely so a checker could tell a deliberate negative sample from a typo. P04 must be rejected **at the input stage**; the other four must pass.
2. **`test_defaults_are_applied_when_missing`** pins the defaults, and also checks that `check_input` did not modify the caller's dictionary (the "returns a NEW dict" promise in its docstring).
3. **`test_caller_value_wins_over_default`** pins the precedence rule from Section 5.1. If someone accidentally swapped the order to `{**story, **INPUT_DEFAULTS}`, every caller's `max_cases` would silently become 10, and this test would fail.
4. **`test_parse_reply_rejects_non_contract_text`** (4 tests). Includes the **empty** reply, which models sometimes return when a call is cut short; `json.loads("")` raises, so it is rejected at the parse stage.
5. **`test_reference_outputs_pass_the_schema_gate`** (4 tests: P01, P02, P03, P05; P04 has no output). `ids=lambda p: p["pair_id"]` shows another way to name parametrized tests: a function that builds the ID from each value. If a schema edit ever made a reviewed reference answer invalid, you would learn it here, before the model is blamed.
6. **`test_extra_field_is_rejected_by_schema_gate`**. `dict(original, confidence=0.9)` makes a copy with one extra key, simulating a model that "helpfully" adds a confidence score. The closed schema must reject it.
7. **`test_dataclass_round_trip`** uses P03, whose test case has **no** `preconditions`, to prove the optional field gets its default and that IDs survive the conversion.

Note what these tests do **not** prove: that the reference outputs are *correct*. A schema-valid answer can still break a semantic rule such as "every acceptance criterion is covered or questioned". Those rules, and how to check them, are the subject of *Agent output validation*, and later today *Agent testing and refinement* turns the same checks on the pairs themselves.

### 10. Optional: Sharing Definitions Between Schemas

Both of our schemas repeat the `story_id` pattern `^US-[0-9]{3}$`. On Thursday we kept each file self-contained, which is simpler to read, and our project keeps it that way. As contracts grow, though, teams often move shared definitions into a common schema and point to it with `$ref`. If the story ID format ever changes, there is then one place to edit.

The `jsonschema` library resolves such references through a **registry** from the `referencing` package (installed with `jsonschema` 4.18+). This standalone example does not touch the project files:

```python
# shared_defs_demo.py  (optional: one definition, used by two schemas)
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

COMMON = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.com/schemas/tcd/common/1.0.0",
    "$defs": {"story_id": {"type": "string", "pattern": "^US-[0-9]{3}$"}},
}
MINI_INPUT = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {"story_id": {"$ref": "https://example.com/schemas/tcd/common/1.0.0#/$defs/story_id"}},
    "required": ["story_id"],
}

registry = Registry().with_resource(COMMON["$id"], Resource.from_contents(COMMON))
validator = Draft202012Validator(MINI_INPUT, registry=registry)

for doc in [{"story_id": "US-205"}, {"story_id": "205"}]:
    errors = [e.message for e in validator.iter_errors(doc)]
    print(doc, "->", errors or "valid")
```

Output:

```text
{'story_id': 'US-205'} -> valid
{'story_id': '205'} -> ["'205' does not match '^US-[0-9]{3}$'"]
```

- `Resource.from_contents(COMMON)` wraps the dictionary as a schema resource; it reads `$schema` to know which draft it is.
- `Registry().with_resource(uri, resource)` returns a **new** registry containing it (registries are immutable, so you always use the returned value).
- The `$ref` value is the common schema's `$id` plus `#/$defs/story_id`, a pointer to the definition inside it. The registry means the validator **never downloads** anything: `example.com` is just a name.

**A note on model-side structured outputs.** Some model APIs can constrain a reply to a JSON Schema you send with the request. That is useful, because it reduces format failures, but it does **not** replace your contract code. Providers support only a subset of JSON Schema (for example, Claude's structured outputs documentation lists `minLength` and `minimum` among unsupported keywords), a reply can still be cut short by a token limit or replaced by a refusal, and you may switch models or providers later. Keep the gates in your own code; they are the part of the contract you control.

### 11. When the Contract Breaks: Moving to 2.0.0

On Thursday you learned that a **major** version change breaks consumers: for example, renaming `ac_ids` to `traces_to`. Now that the contract is implemented, you can list concretely what has to change **together**, in one pull request:

1. **Schemas:** the field rename, the `contract_version` const → `"2.0.0"`, the `$id` → `.../2.0.0`.
2. **`tcd/contract.py`:** `CONTRACT_VERSION = "2.0.0"`; the `TestCase` dataclass field `ac_ids` → `traces_to`.
3. **Instructions:** header `Output contract: 2.0.0`, and every rule that mentions `ac_ids`. Bump the instruction version too.
4. **Templates:** any hard-coded version (the old `tcd_user_v1.0.0` reminder) or field name; release new template versions.
5. **`agent.json`:** `contract_version` and the pinned instruction/template versions.
6. **Sample pairs:** every expected output and the pairs' `contract_version`.
7. **Consumers:** every place that reads `tc.ac_ids`. Because consumers use the dataclass, your editor or type checker can find each one.
8. **Checks:** run `check_versions.py` (must print `AGREE`) and the contract tests (must pass).

Old outputs saved from earlier runs still say `"contract_version": "1.0.0"`. That is a feature, not a problem: anyone reading an old file knows which contract it followed.

---

## Practice Exercises

1. **Predict the defaults.** For each input, write down by hand what `check_input` returns for `techniques` and `max_cases`, then check with Python: (a) P02's input; (b) P03's input; (c) P01's input with `"max_cases": 20`; (d) P01's input with `"max_cases": 21`. Explain (d).
2. **A new parse failure.** Some models reply with two JSON objects in a row (`{...}{...}`). Predict which stage rejects it and what the message says. Add it as a fifth parametrized case to `test_parse_reply_rejects_non_contract_text` and run the tests.
3. **Typed consumer.** Write `to_pytest_params(result: DesignResult) -> list[tuple]` that returns `(tc.id, tc.expected_result)` for every **high**-priority test case. Run it on the US-205 reply. Why does your function need no `try/except`?
4. **Version drift drill.** In a copy of the project, change the output schema's `$id` to `.../output/1.0.1` and run `check_versions.py`. Then turn the script into a pytest test (`assert len(set(found_versions().values())) == 1`) and watch it fail and pass.
5. **Break the schema on purpose.** In a copy, change `"type": "object"` at the top of the input schema to `"type": "objct"`. What happens on `import tcd.contract`, and why is that better than finding out during a run?
6. **Stretch: shared definitions.** Extend `shared_defs_demo.py` with a second mini-schema for the output that references the same `story_id` definition. Change the pattern in `COMMON` to `^US-[0-9]{4}$` and confirm both validators change behaviour.

---

## Knowledge Check

1. Name the four enforcement points in the TestCaseDesigner flow and what each one protects.

<details><summary>Answer</summary>
(A) The input gate protects the model call and makes input errors the caller's responsibility. (B) Parsing turns the reply text into data and rejects anything that is not one JSON object. (C) The output schema gate protects everything downstream from missing, unknown or badly typed fields. (D) Typed objects protect consumers' code: they get named attributes guaranteed to exist.
</details>

2. Why does `contract.py` build paths from `ROOT` instead of using `"schemas/tcd_input.schema.json"`?

<details><summary>Answer</summary>
A relative path is resolved against the current working directory, which differs between your terminal, an IDE, pytest and CI. `ROOT` is computed from the module's own location (`Path(__file__).resolve().parent.parent`), so the schemas are found wherever the code is run from.
</details>

3. A caller sends `max_cases: 4`. What does `{**INPUT_DEFAULTS, **story}` produce for `max_cases`, and why?

<details><summary>Answer</summary>
4. When two unpacked dictionaries share a key, the later one wins; `story` is unpacked after `INPUT_DEFAULTS`, so the caller's value overwrites the default 10.
</details>

4. What small inconsistency does applying defaults in `check_input` resolve?

<details><summary>Answer</summary>
The instructions said "If techniques is missing, use EP and BVA", while Thursday's renderer wrote "choose the techniques that fit the story" for a missing `techniques`. With defaults applied once at the input gate, every later step (template, model, validator) sees the same `techniques` and `max_cases` values.
</details>

5. Why is `parse_reply` strict about Markdown fences, when Tuesday's defensive parser removed them?

<details><summary>Answer</summary>
The contract (and the instructions) forbid fences, so accepting them would enforce a different contract from the written one; strictness also lets you measure how often the model breaks the format; and repairing or re-asking for broken replies is a separate design decision (retry strategies, Week 9).
</details>

6. Why is it safe to write `TestCase(**tc)` in `from_dict`, and when would it be unsafe?

<details><summary>Answer</summary>
It is safe after the output schema gate: the closed schema guarantees each test case has exactly the allowed keys, with all required ones present. On unvalidated data an extra key would raise `TypeError` (unexpected keyword argument) and a missing required key would raise `TypeError` (missing argument).
</details>

7. Why must `preconditions` be the last field of the `TestCase` dataclass, and why `default_factory=list` rather than `= []`?

<details><summary>Answer</summary>
Dataclass fields with defaults must come after fields without defaults. `default_factory=list` creates a new empty list per instance; a plain `[]` default is rejected by dataclasses because one list object would be shared by every instance.
</details>

8. `check_versions.py` prints `DISAGREE: ['1.0.0', '1.1.0']`. What does that tell you, and what is the fix?

<details><summary>Answer</summary>
At least one place names a different contract version from the others, so the agent may ask for, check or log a different contract than intended. Find the odd one out in the printed list and make all places agree in the same change (or, if the contract really changed, update every place together).
</details>

9. Does a reply that passes `check_output_schema` mean the agent's answer is correct? Explain.

<details><summary>Answer</summary>
No. The schema checks shape only. A schema-valid reply can reference an acceptance criterion that does not exist, skip one, use the wrong story number in IDs, or state a wrong expected result. Semantic rules (R1-R6), quality warnings and human review handle those; the next lesson implements the automated ones.
</details>

---

## Glossary

| Term | Meaning |
|---|---|
| **Implemented contract** | A contract whose schemas are enforced by code at the agent's boundaries on every call, with all version references in agreement. |
| **Enforcement point** | A boundary where data is checked before it moves on: input gate, parse, output schema gate, typed objects. |
| **Fail fast** | Stop at the first sign of a problem that makes further work pointless (for example, a broken schema at start-up). |
| **Collect all errors** | Gather every problem in one pass so the person fixing data sees the full list. |
| **`ContractError`** | Our custom exception; carries a `stage` (`input`, `parse`, `output`) and a list of `errors`. |
| **Meta-schema** | The schema that describes valid JSON Schemas; `check_schema` validates against it. |
| **Dictionary unpacking (`**`)** | Copies a dictionary's key/value pairs into a new dictionary or into a function call's keyword arguments; later keys win. |
| **Strict parsing** | Accepting only exactly what the contract allows (here: one JSON object, no fences or prose), rejecting everything else. |
| **Dataclass** | A class whose `__init__`, `__repr__` and `__eq__` are generated from annotated fields by the `@dataclass` decorator; `frozen=True` makes it read-only. |
| **Class method** | A method called on the class (`DesignResult.from_dict(...)`) that receives the class as `cls`; often used as an alternative constructor. |
| **Contract test** | A fast test that checks the contract-enforcing code behaves as the contract says, without calling a model. |
| **Registry (`referencing`)** | An immutable collection of schemas that lets the validator resolve `$ref` to other schemas without downloading them. |

---

## Summary

- An IO contract is **implemented** when three things exist together: **schemas**, **enforcement code** at the boundaries, and **versions that agree** everywhere they are written.
- TestCaseDesigner enforces its contract at four points: **(A)** input gate, **(B)** strict parse, **(C)** output schema gate, **(D)** typed objects for consumers. Every failure is a rejection with a reason, never a silent fix.
- `tcd/contract.py` anchors paths to the project with `ROOT`, checks both schemas **at start-up**, raises `ContractError` with a **stage** and a **list** of `path: message` errors in a stable order.
- **Defaults are applied once**, in `check_input`, with `{**INPUT_DEFAULTS, **story}` (the caller's values win). This removes the earlier disagreement between the instructions and the renderer about the default techniques.
- `parse_reply` is **strict** by design: fences, prose, arrays and invalid JSON are rejected at the `parse` stage. Repair and re-ask strategies are a Week 9 topic.
- `DesignResult` and `TestCase` dataclasses, built **only** from validated output, make consumers such as a TestRail export or pytest parametrization short and safe.
- A small script checks that every copy of the **contract version** agrees; removing hard-coded copies (as the `$contract_version` placeholder does) is even better.
- **Contract tests** (17 passing here) use the sample pairs as data and pin the gate, the defaults, the parser, the schema gate and the dataclasses.
- Schema-valid is not the same as correct: the semantic rules come next, in **Agent output validation**.

---

## Additional Resources

- python-jsonschema documentation, *JSON (Schema) Referencing* (how to build a `Registry` with `Resource.from_contents` so `$ref` can point to other schema files without network access): https://python-jsonschema.readthedocs.io/en/stable/referencing/
- Python documentation, *dataclasses — Data Classes* (the official reference for `@dataclass`, `field(default_factory=...)`, `frozen=True` and the rule about default field order): https://docs.python.org/3/library/dataclasses.html
- Claude Platform Docs, *Structured outputs* (how a model API can constrain replies to a JSON Schema, and which schema keywords it does not support, which is why your own validation still matters): https://platform.claude.com/docs/en/build-with-claude/structured-outputs
