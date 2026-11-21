# Agent Output Validation

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why **every** reply from a QA agent must be validated, even when the instructions, template and contract are good, and why model output counts as **untrusted input**.
- Describe the validation step TestCaseDesigner runs on each reply (**parse → schema → R1-R6 → Q1-Q2 → human**) and why the order matters.
- Read and explain the complete `tcd/validation.py` module: the `Finding` and `ValidationReport` data classes, each rule function, the `RULES` list and the `validate_reply` function that stops early when the shape is wrong.
- Work out by hand which rule a broken output breaks, then confirm it by running the validator on a "rogues' gallery" of planted defects.
- Explain what the three verdicts **PASS**, **PASS_WITH_WARNINGS** and **FAIL** mean for the next step, and why **validation is not approval**.
- Recognise the limits of automated validation: **false positives**, **false negatives** and the class of errors only a human can catch.
- Add a new rule to the catalogue properly: ID, layer, severity, message, function, test and catalogue row.
- Decide what to record about each validation so results can be traced later.

---

## Why This Matters

On Thursday you designed TestCaseDesigner's **contract**: two JSON Schemas, a rule catalogue (S1, S2, R1-R6, Q1-Q3) and a diagram of the validation layers. Earlier today you built the agent's instructions, its template library and the code that implements the contract (`tcd/contract.py`). Everything so far has been about getting the agent to produce good output.

This lesson is about the moment **after** the model answers. A model is not a function that returns the same value every time. Run the same prompt twenty times and you may get eighteen excellent answers, one wrapped in Markdown fences and one that quietly invents an acceptance criterion called `AC5`. If your pipeline trusts all twenty, the two bad ones flow straight into your test management tool, HTML report or pytest suite.

Think of the goods-in desk at a warehouse: even from a reliable supplier, every delivery is checked (right box, right label, right count) before a person inspects the contents. Output validation is the goods-in desk for your agent.

This is the "validation" part of the **Weekly Epic** ("design and build their first QA agent with IO contracts and validation scripts"). For **Project 2 (Test Automation Framework)**, it is the gate that decides whether AI-generated test cases for the e-commerce app (login, search, cart, checkout) are allowed anywhere near your framework.

> **Scope note.** This lesson builds and explains the **validation step**: the module that checks one reply and returns a report with a verdict. Turning it into a **command-line script** with exit codes, a batch mode, a pytest suite and CI is the next lesson, *Building validation scripts*. Running the agent over a whole backlog and storing a run log comes later today in *Executing agents against QA requirements*, and measuring the agent across many runs in *Agent testing and refinement*. **Retrying** the model when a reply fails is covered in **Week 9**; the **hallucination taxonomy**, **LLM-as-judge** and **prompt injection** are covered in **Week 10**. Here we only name them.

---

## The Concept

### 1. Why Validate Every Single Output?

You might ask: "We wrote careful instructions. We locked the format. Why check every reply?" There are four reasons, and each one is a real failure you saw earlier this week.

**Reason 1: The model is non-deterministic.** On Monday you learned that a model samples each next token from a probability distribution; even at temperature 0, providers do not promise identical output. Good instructions make bad replies *rarer*, not *impossible*, and a check on only a sample misses exactly the rare bad one.

**Reason 2: Model output is untrusted input.** Security teams have a simple rule: *never trust data that crosses a boundary into your system*. A web form's input is untrusted; so is a file a user uploads. The **OWASP Top 10 for LLM Applications** applies the same rule to models in its entry **LLM05:2025 Improper Output Handling**: output from a model must be validated and, where it is displayed, **encoded** before it reaches downstream systems. For a QA agent this is not hypothetical. Suppose a test case's `expected_result` contains `<script>...</script>`, because the story text contained it or the model copied it from somewhere. If your pipeline writes test cases into an HTML report, that script runs in a teammate's browser. If it imports them into a test management tool, the tool may render it. Validation is where you notice; encoding is how you neutralise it (Section 7).

**Reason 3: "Structured output" features help, but do not finish the job.** Some model APIs can constrain a reply to a JSON Schema. That is genuinely useful: it removes most fence and prose problems. But read the small print. The Claude Platform documentation on *Structured outputs*, for example, lists JSON Schema features that are **not supported** in that mode, including `minLength`, `maxLength`, `minimum` and `maximum`, and notes that a reply can still break the schema if the model **refuses** or the reply is **cut off** at the token limit (`max_tokens`). Our output schema uses `minLength` for titles and expected results. And no API feature checks rules R1-R6, because those compare the reply with the *input*. You still need your own validation.

**Reason 4: Schema-valid but wrong is the dangerous case.** On Thursday you saw an output that passed the schema yet invented `AC5` and borrowed an ID from another story. Errors that break the shape are loud: the parser or schema stops them. Errors that keep the shape are quiet: the JSON looks perfect, the downstream code accepts it, and the mistake surfaces weeks later as a test that traces to a requirement that does not exist. Most of today's code exists to catch the quiet kind.

> **Key idea:** validation runs on **every** reply, **every** time, **before** anything else uses it. It is not a debugging tool you turn on when something looks odd.

### 2. A Quick Recap of the Rule Catalogue

Thursday's rule catalogue is the specification for today's code. Here it is in short form; the full table, with example violations and messages, is in Thursday's *Required fields and validation rules* lesson.

| Rule | Checks | Layer | Severity |
|---|---|---|---|
| S2 | Input matches the input schema | Input gate (`check_input`, earlier today) | Error |
| S1 | Reply is one JSON object matching the output schema | Output schema | Error |
| R1 | Output `story_id` equals input `story_id` | Code | Error |
| R2 | Every `ac_ids` entry exists in the input | Code | Error |
| R3 | Every input AC is covered by a test case or named in an open question | Code | Error |
| R4 | Test case IDs are unique and use the story number | Code | Error |
| R5 | Number of test cases `<=` `max_cases` (default 10) | Code | Error |
| R6 | `ok` needs test cases; `needs_clarification` needs questions | Code | Error |
| Q1 | BVA requested ⇒ at least one `boundary` case | Code | Warning |
| Q2 | `expected_result` has no vague phrases | Code + human | Warning |
| Q3 | Expected result agrees with its AC | Human | Error at review |

S2 runs **before** the model is called (the input gate), so today we deal with everything from S1 downwards.

### 3. The Validation Pipeline, Step by Step

Here is what happens to one reply. Read it as a series of gates; each gate only sees what the previous gate let through.

```text
 raw reply text (a string)
        │
        ▼
 [a] Parse: is it exactly one JSON object?          ── no ──►  S1 error, STOP (stopped_at = "parse")
        │ yes
        ▼
 [b] Output schema: right fields, types, patterns?   ── no ──►  S1 errors, STOP (stopped_at = "output")
        │ yes
        ▼
 [c] Contract rules R1-R6 (compare with the input)  ──────────► errors (all rules run, all collected)
        │
        ▼
 [d] Quality rules Q1-Q2                            ──────────► warnings
        │
        ▼
 verdict:  any error → FAIL;  only warnings → PASS_WITH_WARNINGS;  nothing → PASS
        │
        ▼
 [e] Human review (Q3 + Wednesday checklist)  ── only for PASS / PASS_WITH_WARNINGS
```

Three design decisions are built into this picture.

**Decision 1: Stop after a shape failure.** If the reply is not JSON, or the schema fails, the code rules cannot trust that `story_id` or `ac_ids` exist. Running R1-R6 anyway would crash (`KeyError`) or produce confusing follow-on errors. So gates [a] and [b] **fail fast**.

**Decision 2: Collect everything after that.** Once the shape is valid, every rule runs and every finding is kept, so a reviewer sees that a reply broke R2 *and* R3 at once (Thursday's "collect all errors").

**Decision 3: Warnings never block on their own.** Q1 and Q2 are judgement calls that code can only approximate. A warning says "a human should look here first"; it does not reject the reply.

### 4. What Each Verdict Means for the Next Step

A verdict is only useful if everyone agrees what happens next. For TestCaseDesigner:

| Verdict | Meaning | What the pipeline does |
|---|---|---|
| **FAIL** | At least one error: the reply breaks the contract | Reject the reply. Do **not** pass it to any consumer. Log the report with the raw reply as evidence. (Asking the model again automatically is a **retry strategy**, covered in **Week 9**; today a failed reply is simply rejected and recorded.) |
| **PASS_WITH_WARNINGS** | Contract satisfied, but quality concerns found | Send to human review with the warnings shown **first**, so the reviewer starts where the risk is. |
| **PASS** | No automated finding | Send to human review as normal. |

**PASS does not mean approved.** It means "no automated rule found a problem". Wednesday's sign-off states and review checklist still apply: validation decides what is *worth a human's time*; the human decides what is *correct* (Section 8 shows a wrong answer that passes every rule).

### 5. Walking Through `tcd/validation.py`

**Setup.** Work in your `tcd_agent/` project folder from earlier today. You need Python 3.11 or newer and:

```bash
pip install "jsonschema>=4.18" pytest
```

> Some machines still have `jsonschema` 3.2, which has no `Draft202012Validator`. Check with `python -c "import importlib.metadata as m; print(m.version('jsonschema'))"` and upgrade if needed.

The module builds on `tcd/contract.py` (earlier today), which gives us `parse_reply`, `check_output_schema` and `ContractError`. We will read the module in five parts.

#### 5.1 The data classes: `Finding` and `ValidationReport`

```python
# tcd/validation.py
"""Agent output validation: parse -> schema (S1) -> rules R1-R6 -> warnings Q1-Q2."""
import re
from dataclasses import dataclass, field

from tcd.contract import ContractError, check_output_schema, parse_reply

ERROR, WARNING = "error", "warning"
VAGUE_PHRASES = ["as expected", "works correctly", "correctly", "should be fine",
                 "properly", "successfully"]


@dataclass
class Finding:
    rule: str          # "S1", "R3", "Q2" ...
    severity: str      # "error" or "warning"
    where: str         # "test_cases[2].id", "(root)" ...
    message: str


@dataclass
class ValidationReport:
    story_id: str
    findings: list = field(default_factory=list)
    stopped_at: str = ""     # "parse" or "output" if validation could not go deeper

    @property
    def errors(self) -> list:
        return [f for f in self.findings if f.severity == ERROR]

    @property
    def warnings(self) -> list:
        return [f for f in self.findings if f.severity == WARNING]

    @property
    def verdict(self) -> str:
        if self.errors:
            return "FAIL"
        return "PASS_WITH_WARNINGS" if self.warnings else "PASS"
```

Line by line:

- `ERROR, WARNING` are **constants**: a typo such as `EROR` becomes a `NameError` you notice at once, instead of a finding that silently counts as neither. `VAGUE_PHRASES` (behind Q2) sits at the top so it is easy to review.
- `@dataclass` (from the standard library) writes the boring parts of a class for you: `__init__`, a readable `__repr__` and `==` comparison. `Finding("R1", ERROR, "story_id", "...")` creates one finding with four fields.
- A **finding** is one problem: *which rule*, *how serious*, *where* in the output, and a *message* a human can act on. These four fields match Thursday's advice on error messages: say what failed, where, what was expected and what was found.
- `ValidationReport` collects all findings for one reply. `findings: list = field(default_factory=list)` gives every report its **own** empty list.
- `stopped_at` stays an empty string when validation went all the way through, and becomes `"parse"` or `"output"` when it had to stop early. That tells a reader *why* there are no R-rule findings: not because the rules passed, but because they never ran.
- `@property` turns a method into something you read like an attribute: `report.errors`, not `report.errors()`. Each property is computed from `findings` every time, so it can never get out of step with them.
- `verdict` encodes the table from Section 4 in three lines: any error means `FAIL`; otherwise warnings mean `PASS_WITH_WARNINGS`; otherwise `PASS`.

Notice there is no "score": a reply with one R2 error is not "90% valid", it is invalid. Scores belong to measuring the *agent* across many runs, later today.

#### 5.2 Contract rules R1, R2 and R4

Each rule is a small function with the same **signature**: it takes the gated input `story` and the parsed output `out`, and returns a list of findings (empty means the rule passed). The identical shape is what lets us loop over all rules later.

```python
# ---- R rules: need the input as well as the output (code layer) ------------
def check_r1(story: dict, out: dict) -> list:
    if out["story_id"] != story["story_id"]:
        return [Finding("R1", ERROR, "story_id",
                        f"expected '{story['story_id']}' (from input), got '{out['story_id']}'")]
    return []
```

**R1** adds the one thing the schema cannot know about `story_id`: that it is the **same** story we sent. A model that has seen another story (for example in a few-shot example) can label its answer with the wrong one, and the answer is then filed under the wrong requirement.

`check_r2` and `check_r4` are the functions you met on Thursday, now returning `Finding` objects instead of strings:

```python
def check_r2(story: dict, out: dict) -> list:
    known = {ac["id"] for ac in story["acceptance_criteria"]}
    return [Finding("R2", ERROR, f"test_cases[{i}].ac_ids",
                    f"'{ac_id}' is not an acceptance criterion of {story['story_id']} "
                    f"(expected one of {sorted(known)})")
            for i, tc in enumerate(out["test_cases"]) for ac_id in tc["ac_ids"] if ac_id not in known]


def check_r4(story: dict, out: dict) -> list:
    number = story["story_id"].split("-")[1]
    findings, seen = [], set()
    for i, tc in enumerate(out["test_cases"]):
        if tc["id"] in seen:
            findings.append(Finding("R4", ERROR, f"test_cases[{i}].id", f"'{tc['id']}' is used more than once"))
        seen.add(tc["id"])
        if tc["id"].split("-")[1] != number:
            findings.append(Finding("R4", ERROR, f"test_cases[{i}].id",
                                    f"'{tc['id']}' should start with 'TC-{number}-' because the story is {story['story_id']}"))
    return findings
```

`check_r2` is one **list comprehension** with two `for` clauses; read it left to right like nested loops: *for each test case, for each `ac_id` in it, if unknown, make a Finding*. `check_r4` is unchanged from Thursday apart from the return type: a `seen` set catches duplicates, and `split("-")` safely pulls out the story number because the schema has already guaranteed both ID formats.

#### 5.3 Contract rules R3, R5 and R6

```python
def check_r3(story: dict, out: dict) -> list:
    covered = {ac_id for tc in out["test_cases"] for ac_id in tc["ac_ids"]}
    asked = " ".join(out["open_questions"])
    findings = []
    for ac in story["acceptance_criteria"]:
        mentioned = re.search(rf"\b{ac['id']}\b", asked)
        if ac["id"] not in covered and not mentioned:
            findings.append(Finding("R3", ERROR, "test_cases",
                                    f"{ac['id']} is not covered by any test case or open question"))
    return findings
```

**R3** catches **silent omission**: the model simply forgets an acceptance criterion. Humans miss omissions because there is nothing on the page to look at; a computer is good at exactly this.

How it works:

1. `covered` is a **set comprehension**: every AC ID that appears in any test case's `ac_ids`. For the US-205 reference answer this is `{"AC1", "AC2", "AC3"}`.
2. `asked` glues all open questions into one string with spaces between them, so we can search them all at once.
3. For each AC in the **input**, the AC is fine if it is covered by a test case **or** mentioned in a question. That "or" comes straight from the instructions' *Uncertainty and Escalation* section: asking about an unclear AC is a legitimate alternative to testing it.
4. `re.search(rf"\b{ac['id']}\b", asked)` looks for the AC ID as a **whole word**. `\b` is a word boundary, so `AC1` matches in "AC1: is this final?" but **not** inside `AC10` or `AC12`. Without `\b`, a story with twelve ACs would wrongly treat `AC1` as mentioned whenever a question names `AC12`. (The `r` in `rf"..."` makes it a **raw string**, so `\b` reaches the regular-expression engine instead of being turned into a backspace character; the `f` lets us insert the ID.)

```python
def check_r5(story: dict, out: dict) -> list:
    limit = story.get("max_cases", 10)
    count = len(out["test_cases"])
    if count > limit:
        return [Finding("R5", ERROR, "test_cases", f"{count} test cases returned, max_cases is {limit}")]
    return []
```

**R5** enforces the case limit. `story.get("max_cases", 10)` falls back to the contract default of 10; `check_input` normally applies that default already, so this is a safety net. The message states both numbers, so nobody has to count.

```python
def check_r6(story: dict, out: dict) -> list:
    if out["status"] == "ok" and not out["test_cases"]:
        return [Finding("R6", ERROR, "test_cases", "status is 'ok' but no test cases were returned")]
    if out["status"] == "needs_clarification" and not out["open_questions"]:
        return [Finding("R6", ERROR, "open_questions",
                        "status is 'needs_clarification' but open_questions is empty")]
    return []
```

**R6** keeps the `status` field honest, and it has two branches because there are two ways to lie:

- `"ok"` with no test cases claims success but delivers nothing.
- `"needs_clarification"` with no questions asks for help but never says what about.

`not out["test_cases"]` is true for an empty list, because empty containers count as false in Python. Note the `where` field differs between the branches: it points at the field the reviewer should look at.

#### 5.4 Quality rules Q1 and Q2

```python
# ---- Q rules: quality warnings (a human makes the final call) --------------
def check_q1(story: dict, out: dict) -> list:
    if "BVA" in story.get("techniques", []) and out["test_cases"] \
            and not any(tc["type"] == "boundary" for tc in out["test_cases"]):
        return [Finding("Q1", WARNING, "test_cases", "BVA was requested but no test case has type 'boundary'")]
    return []
```

**Q1** reads as one sentence: *if BVA was requested, and there are test cases, and none of them is a boundary case, warn*. The middle condition matters: a `needs_clarification` reply with no test cases at all is not ignoring BVA, so it should not be warned about. `any(...)` returns `True` as soon as one element passes the test. The backslash `\` at the end of the first line continues the expression onto the next line.

Why only a warning? Because the `type` label is a weak signal. A test at exactly $50.00 labelled `"positive"` is still a boundary test in substance. The warning sends the reviewer to look; it does not reject a reply that may be fine.

```python
def check_q2(story: dict, out: dict) -> list:
    findings = []
    for i, tc in enumerate(out["test_cases"]):
        text = tc["expected_result"].lower()
        for phrase in VAGUE_PHRASES:
            if re.search(rf"\b{re.escape(phrase)}\b", text):
                findings.append(Finding("Q2", WARNING, f"test_cases[{i}].expected_result",
                                        f"vague phrase '{phrase}'; state the exact total, message or state"))
                break                      # one warning per test case is enough
    return findings
```

**Q2** hunts for the "it works" kind of expected result you learned to distrust on Wednesday. "Discount works as expected" cannot fail, so a test built on it checks nothing.

- `.lower()` makes the search case-insensitive; `re.escape(phrase)` protects regex special characters a future phrase might contain; `\b...\b` matches whole words, so "correctly" does not match inside "incorrectly".
- `break` leaves the inner loop after the **first** matching phrase. "The feature works correctly and properly" would otherwise produce three warnings about one sentence. One warning per test case is enough to send the reviewer there.

#### 5.5 The `RULES` list and `validate_reply`

```python
RULES = [check_r1, check_r2, check_r3, check_r4, check_r5, check_r6, check_q1, check_q2]


def validate_reply(story: dict, reply: str) -> ValidationReport:
    """Validate one raw model reply against one (already gated) input story."""
    report = ValidationReport(story_id=story["story_id"])
    try:
        out = check_output_schema(parse_reply(reply))
    except ContractError as exc:
        for msg in exc.errors:                          # S1 covers parsing AND the schema
            where = "(reply)" if exc.stage == "parse" else msg.split(":")[0]
            report.findings.append(Finding("S1", ERROR, where, msg))
        report.stopped_at = exc.stage                   # "parse" or "output"
        return report                                   # deeper rules need a valid shape
    for rule in RULES:
        report.findings.extend(rule(story, out))
    return report
```

- **`RULES` is a list of functions.** In Python a function is an ordinary value you can store and call later, so adding a rule means one function plus one name here. The order is the catalogue order.
- **`validate_reply` takes the raw reply as a string**, because parsing is part of validation: a fenced reply must become a clean S1 finding, not crash the caller.
- `check_output_schema(parse_reply(reply))` runs gates [a] and [b] from Section 3 in one line. Both raise `ContractError` on failure; `exc.stage` tells us which (`"parse"` or `"output"`), and `exc.errors` holds one message per problem.
- **Why is a parse failure also called S1?** Thursday's catalogue defines S1 as "Output is a JSON object matching the output schema". Not being JSON at all is the most extreme way to fail that rule. Keeping one rule ID avoids inventing a new catalogue row, and `stopped_at` still tells you exactly which gate failed.
- `where` is `"(reply)"` for parse errors; schema messages from `contract.py` look like `"path: message"`, so `msg.split(":")[0]` recovers the path.
- **`return report` inside `except`** is the fail-fast stop. The `for rule in RULES` loop below it only runs when the shape is valid.
- `report.findings.extend(rule(story, out))` adds whatever list each rule returns. Because empty lists add nothing, passing rules leave no trace.

### 6. Rogues' Gallery: Planted Defects, by Hand First

Now let us use the validator on real data. Our known-good answer is the reviewed US-205 reference output from sample pair **P01** (Thursday). We will make one change at a time to a copy of it, as if a model had made that mistake. These broken replies are **illustrative**: we planted the defects ourselves, choosing mistakes that models commonly make.

As a reminder, the US-205 input has four ACs and `max_cases` 6, requests EP and BVA, and the good answer has three test cases (TC-205-01 boundary at $50.00, TC-205-02 boundary at $49.99, TC-205-03 unknown code) plus one open question about AC4.

#### 6.1 Predict first

Before running anything, cover the right-hand column and predict which rule each change breaks. This is the same skill you will use when reading a real failure report.

| # | Planted change | Your prediction | Answer |
|---|---|---|---|
| 1 | Whole reply wrapped in ` ```json ... ``` ` | | S1, stops at parse |
| 2 | Reply cut off after 110 characters (as if `max_tokens` ran out) | | S1, stops at parse |
| 2b | First test case has `"priority": "urgent"` | | S1, stops at schema |
| 3 | `story_id` changed to `US-101` | | R1 |
| 4 | `open_questions` emptied (the AC4 question disappears) | | R3 for AC4 |
| 5 | Four extra test cases appended (7 in total) | | R5 (7 > 6) |
| 6 | `test_cases` emptied, status still `ok`, but a question names all four ACs | | R6 only |
| 7 | Every `type` changed to `positive` | | Q1 warning |
| 8 | First `expected_result` becomes "Discount works as expected" | | Q2 warning |
| 9 | First test case's `ac_ids` changed from `["AC1"]` to `["AC9"]` | | R2 **and** R3 |

Two of these deserve a moment of thought.

- **Row 6.** The planted question names all four ACs so that R3 does not fire as well as R6. When you plant defects, think about what *else* your change breaks.
- **Row 9.** One defect, two rules. `AC9` does not exist (R2). And because the only test case that covered AC1 now points at AC9, AC1 is no longer covered by anything (R3). Neither finding is wrong: they describe two consequences of the same mistake. When you read a real report, look for this pattern before assuming the model made two separate mistakes.

#### 6.2 Run it

Create `rogues_gallery.py` in the project folder:

```python
# rogues_gallery.py
import copy
import json
from pathlib import Path

from tcd.contract import check_input
from tcd.validation import validate_reply

PAIR = json.loads(Path("samples/P01-happy_path.json").read_text(encoding="utf-8"))
STORY = check_input(PAIR["input"])          # the gated US-205 input
GOOD = PAIR["expected_output"]              # the reviewed reference answer


def show(name: str, reply: str) -> None:
    """Validate one reply and print the report in a readable form."""
    report = validate_reply(STORY, reply)
    stop = f"  (stopped at {report.stopped_at})" if report.stopped_at else ""
    print(f"{name:<22} {report.verdict}{stop}")
    for f in report.findings:
        print(f"    {f.rule} {f.severity:<7} at {f.where}")
        print(f"        {f.message}")


def bad(change) -> str:
    """Deep-copy GOOD, apply one change, return it as reply text."""
    out = copy.deepcopy(GOOD)
    change(out)
    return json.dumps(out)


show("0 good answer", json.dumps(GOOD))
show("1 fenced reply", "```json\n" + json.dumps(GOOD) + "\n```")
show("2 cut-off reply", json.dumps(GOOD)[:110])
show("2b bad priority", bad(lambda o: o["test_cases"][0].update(priority="urgent")))
show("3 wrong story", bad(lambda o: o.update(story_id="US-101")))
show("4 AC4 forgotten", bad(lambda o: o.update(open_questions=[])))
show("5 over the limit", bad(lambda o: o["test_cases"].extend(
    [dict(o["test_cases"][2], id=f"TC-205-{n:02d}") for n in range(4, 8)])))
show("6 ok but empty", bad(lambda o: o.update(
    test_cases=[], open_questions=["AC1, AC2, AC3 and AC4: are these final?"])))
show("7 no boundary case", bad(lambda o: [tc.update(type="positive") for tc in o["test_cases"]]))
show("8 vague result", bad(lambda o: o["test_cases"][0].update(expected_result="Discount works as expected")))
show("9 AC1 -> AC9", bad(lambda o: o["test_cases"][0].update(ac_ids=["AC9"])))
```

How the helpers work:

- `check_input(PAIR["input"])` returns the story **with defaults applied**: always validate against what the model actually received.
- `bad` takes a **function** called `change`, applies it to a deep copy of the good answer and returns JSON text. `copy.deepcopy` matters: a plain `copy.copy` would share the nested `test_cases` list, and the first mutation would damage `GOOD` for every later example.
- Each `lambda o: ...` is a tiny one-line function that makes one change. `dict.update(...)` sets keys in place; `dict(o["test_cases"][2], id=...)` copies a test case and overrides its `id`, which is how row 5 makes four extra cases with fresh IDs `TC-205-04` to `TC-205-07` (so R4 does not fire as well).
- `json.dumps(GOOD)[:110]` keeps only the first 110 characters, simulating a reply cut off at the token limit.

Run `python rogues_gallery.py`:

```text
0 good answer          PASS
1 fenced reply         FAIL  (stopped at parse)
    S1 error   at (reply)
        reply is wrapped in Markdown fences; the contract forbids them
2 cut-off reply        FAIL  (stopped at parse)
    S1 error   at (reply)
        reply is not valid JSON: Expecting ':' delimiter at line 1 column 111
2b bad priority        FAIL  (stopped at output)
    S1 error   at test_cases/0/priority
        test_cases/0/priority: 'urgent' is not one of ['high', 'medium', 'low']
3 wrong story          FAIL
    R1 error   at story_id
        expected 'US-205' (from input), got 'US-101'
4 AC4 forgotten        FAIL
    R3 error   at test_cases
        AC4 is not covered by any test case or open question
5 over the limit       FAIL
    R5 error   at test_cases
        7 test cases returned, max_cases is 6
6 ok but empty         FAIL
    R6 error   at test_cases
        status is 'ok' but no test cases were returned
7 no boundary case     PASS_WITH_WARNINGS
    Q1 warning at test_cases
        BVA was requested but no test case has type 'boundary'
8 vague result         PASS_WITH_WARNINGS
    Q2 warning at test_cases[0].expected_result
        vague phrase 'as expected'; state the exact total, message or state
9 AC1 -> AC9           FAIL
    R2 error   at test_cases[0].ac_ids
        'AC9' is not an acceptance criterion of US-205 (expected one of ['AC1', 'AC2', 'AC3', 'AC4'])
    R3 error   at test_cases
        AC1 is not covered by any test case or open question
```

Every prediction holds. A few observations:

- **Rows 1, 2 and 2b stop early.** In row 2b the R rules never ran because the schema failed first; `stopped_at` makes that visible, so an empty R-rule section is not mistaken for a pass.
- **Row 2 is a real-world failure**: a reply cut off by the token limit, reported as "reply is not valid JSON".
- **Rows 7 and 8 pass with warnings.** The reply is contract-valid and goes to a human, flagged.

### 7. Validation Is Not Encoding: a Note on Untrusted Text

The output schema checks that `expected_result` is a string of at least five characters. It does not care what the characters *are*. `"<script>alert(1)</script>"` is a perfectly valid string.

OWASP's guidance for LLM05 has two halves: **validate** model output, and **encode** it for the place it is going. Validation answers "is this acceptable?" Encoding answers "how do I display this safely?" They are different jobs:

- **HTML report:** escape every text field with `html.escape` when writing the page.
- **CSV import:** neutralise values starting with `=`, `+`, `-` or `@` (spreadsheet formulas).
- **File paths, SQL, shell:** use the safe API for that context, never string concatenation.

Validation can help by **flagging** suspicious content so a human notices it. Section 9 adds a rule that does exactly that. But the real protection lives in the code that consumes the output. A validator flag is a smoke alarm; encoding is the fire door.

### 8. The Limits of Automated Validation

A validator is a set of tests, and like all tests it can be wrong in two directions. Let us demonstrate both with `limits.py`:

```python
# limits.py
import copy
import json
from pathlib import Path

from tcd.contract import check_input
from tcd.validation import validate_reply

PAIR = json.loads(Path("samples/P01-happy_path.json").read_text(encoding="utf-8"))
STORY = check_input(PAIR["input"])

# False negative: a WRONG expected total that every automated rule accepts.
wrong = copy.deepcopy(PAIR["expected_output"])
wrong["test_cases"][0]["expected_result"] = "Total is $40.00"     # 10% of $50.00 is $5.00, not $10.00
print("wrong total     ->", validate_reply(STORY, json.dumps(wrong)).verdict)

# False positive: a concrete, correct result that happens to use a "vague" word.
fine = copy.deepcopy(PAIR["expected_output"])
fine["test_cases"][0]["expected_result"] = "Coupon SAVE10 is applied successfully and the total is $45.00"
report = validate_reply(STORY, json.dumps(fine))
print("concrete result ->", report.verdict, [f.message for f in report.warnings])
```

Output:

```text
wrong total     -> PASS
concrete result -> PASS_WITH_WARNINGS ["vague phrase 'successfully'; state the exact total, message or state"]
```

**The false negative is the important one.** Work it by hand: 10% off $50.00 is $5.00, so the correct total is $45.00. The planted answer says $40.00. It has the right shape, traces to a real AC, uses a correct ID, is under the limit and contains a concrete number. Every automated rule is satisfied, and the reply gets a clean **PASS**. Yet a test built on it would **fail against correct software**, and a tester might "fix" the application to match. This is rule **Q3**, "expected result agrees with its AC", and it is assigned to **human review** in the catalogue for exactly this reason: checking it requires understanding what the requirement *means*.

**The false positive is a nuisance, not a danger.** The result is concrete; "successfully" just happens to be on the list. Because Q2 is a **warning**, it costs a reviewer a few seconds. A rule you know is sometimes wrong should never block on its own.

In short, code can check **shape**, **traceability**, **coverage**, **counts** and some **wording**; it cannot check whether a result is *correct*, whether the steps reach the described state, whether a question is a good one, or whether the set of tests is the right set. Those are the Wednesday review checklist. Automated validation shrinks the reviewer's job; it never removes it.

### 9. Extending the Catalogue: Adding a Rule Properly

Sooner or later you will find a problem the current rules miss. Add the rule in seven steps, so you never create the duplicated or orphaned checks Thursday warned about:

1. **Name the problem with an example.** Not "bad content", but a concrete reply that shows it.
2. **Give it an ID** that will never be reused (we will use **B1**, for the *Boundaries* section of the instructions).
3. **Choose the layer** using Thursday's decision guide: schema if one document is enough and the check is declarative; code if it needs logic or the input; human if it needs judgement.
4. **Choose the severity.** Ask: *if this fires wrongly, what does it cost?* and *if it is real and we only warn, what does it cost?*
5. **Write the message** before the code: what, where, and how to fix.
6. **Write the function** with the standard `(story, out) -> list` signature, plus at least one test that it fires and one that it does not.
7. **Add the catalogue row** and register the rule, in the same change.

#### 9.1 Worked example: B1, markup in test case text

1. **Example.** A reply whose step reads `Enter coupon <script>alert(1)</script>`. Real stories occasionally contain markup (copied from a ticket or a web page), and a model may carry it into a test case.
2. **ID:** B1.
3. **Layer: code.** A schema `pattern` could forbid `<` entirely, but that would also reject the placeholders the instructions *require*, such as `<valid_password>`. We need a smarter match, so it belongs in code.
4. **Severity: warning.** A story about formatting product reviews could legitimately mention a `<b>` tag in a test step. Blocking such replies would be a false positive with a real cost. The danger, on the other hand, is handled by **encoding** downstream (Section 7); the warning's job is to make a human look.
5. **Message:** "contains markup '<script'; escape it before it reaches a report".
6. **Function and tests:** below.
7. **Catalogue row:** at the end of this section.

We put the rule in a separate file, `extra_rules.py`, so you can try it without editing `tcd/validation.py`. In your own project you would add `check_b1` to the module and to `RULES` directly.

```python
# extra_rules.py
"""B1: markup in test case text. Added beside tcd/validation.py without editing it."""
import copy
import html
import json
import re
from pathlib import Path

from tcd.contract import check_input
from tcd.validation import WARNING, Finding, validate_reply

# Real HTML tag names only, so placeholders such as <valid_password> are NOT flagged.
HTML_TAG = re.compile(r"<\s*/?\s*(script|iframe|img|svg|style|a|b|i|div|span)\b", re.IGNORECASE)


def check_b1(story: dict, out: dict) -> list:
    findings = []
    for i, tc in enumerate(out["test_cases"]):
        texts = {"title": tc["title"], "expected_result": tc["expected_result"]}
        texts.update({f"steps[{n}]": s for n, s in enumerate(tc["steps"])})
        texts.update({f"preconditions[{n}]": p for n, p in enumerate(tc.get("preconditions", []))})
        for field_name, text in texts.items():
            match = HTML_TAG.search(text)
            if match:
                findings.append(Finding("B1", WARNING, f"test_cases[{i}].{field_name}",
                                        f"contains markup '{match.group(0)}'; escape it before it reaches a report"))
    return findings


def validate_extended(story: dict, reply: str):
    report = validate_reply(story, reply)          # S1, R1-R6, Q1-Q2 exactly as before
    if not report.stopped_at:                      # B1 also needs a valid shape
        report.findings.extend(check_b1(story, json.loads(reply)))
    return report


if __name__ == "__main__":
    pair = json.loads(Path("samples/P01-happy_path.json").read_text(encoding="utf-8"))
    story = check_input(pair["input"])
    out = copy.deepcopy(pair["expected_output"])
    out["test_cases"][2]["steps"][0] = "Enter coupon <script>alert(1)</script>"
    out["test_cases"][0]["steps"][0] = "Log in with <valid_email> and <valid_password>"
    report = validate_extended(story, json.dumps(out))
    print(report.verdict)
    for f in report.findings:
        print(f"  {f.rule} {f.severity} at {f.where}: {f.message}")
    print(html.escape(out["test_cases"][2]["steps"][0]))
```

How it works:

- **The regular expression** `<\s*/?\s*(script|iframe|...)\b` means: a `<`, optional spaces, an optional `/` (for closing tags), optional spaces, then one of a list of real tag names as a whole word. `re.compile` builds it once; `re.IGNORECASE` also catches `<SCRIPT>`. Because `valid_password` is not in the tag list, the required placeholders pass untouched. (`<b` followed by `\b` matches `<b>` but not `<basket_id>`, because `\b` needs a non-word character after the `b`.)
- **`texts`** maps a field label to its text, so a finding says exactly where the markup is (`steps[0]`). `tc.get("preconditions", [])` handles the optional field.
- **`validate_extended`** runs the standard validation and adds B1 only if the shape was valid (fail fast again); `json.loads(reply)` is safe then because parsing already succeeded.

Run `python extra_rules.py`:

```text
PASS_WITH_WARNINGS
  B1 warning at test_cases[2].steps[0]: contains markup '<script'; escape it before it reaches a report
Enter coupon &lt;script&gt;alert(1)&lt;/script&gt;
```

The script tag is flagged with an exact location; the placeholders are not. The last line shows what encoding does: `html.escape` turns `<` and `>` into `&lt;` and `&gt;`, so a browser displays the text instead of running it.

Step 6 also asks for tests. Two small ones prove the rule fires when it should and stays quiet when it should:

```python
# test_extra_rules.py
from extra_rules import check_b1

def case(step: str) -> dict:
    return {"test_cases": [{"title": "Title of the case", "steps": [step],
                            "expected_result": "Total is $45.00"}]}

def test_b1_flags_script_tag():
    assert [f.rule for f in check_b1({}, case("Enter <script>x</script>"))] == ["B1"]

def test_b1_ignores_placeholders():
    assert check_b1({}, case("Enter <valid_email> and <valid_password>")) == []
```

`python -m pytest -q test_extra_rules.py`:

```text
..                                                                       [100%]
2 passed in 0.05s
```

The helper `case` builds the smallest output the function needs. Unit-testing a rule function directly, with tiny hand-made data, is fast and pinpoints failures. Building a full **pytest suite for the whole validator**, with a planted defect for every rule, is part of the next lesson.

And step 7, the new catalogue row:

| Rule ID | Description | Layer | Severity | Example violation | Error message |
|---|---|---|---|---|---|
| B1 | Test case text contains HTML markup (placeholders such as `<valid_password>` allowed). | Code | Warning | Step `Enter coupon <script>...` | `B1 WARNING at test_cases[2].steps[0]: contains markup '<script'; escape it before it reaches a report` |

### 10. Recording What Validation Found

A verdict printed to the screen helps today. A verdict **stored** helps next week, when someone asks "why did this test case come from the agent with no AC4 coverage?" For each validation, record at least:

- the **story ID** and the **verdict**;
- **`stopped_at`**, so nobody mistakes "R rules never ran" for "R rules passed";
- **every finding** (rule, severity, location, message), not just a count;
- the **versions** that produced the reply: instructions, template and contract. Without these, you cannot tell whether a failure belongs to the old prompt or the new one.

Because `Finding` is a dataclass, turning a report into JSON is short:

```python
# record.py
import json
from dataclasses import asdict
from pathlib import Path

from tcd.contract import check_input
from tcd.validation import validate_reply

pair = json.loads(Path("samples/P01-happy_path.json").read_text(encoding="utf-8"))
story = check_input(pair["input"])
reply = json.dumps({**pair["expected_output"], "story_id": "US-101"})
report = validate_reply(story, reply)

record = {
    "story_id": report.story_id,
    "verdict": report.verdict,
    "stopped_at": report.stopped_at,
    "findings": [asdict(f) for f in report.findings],
    "versions": {"instructions": "1.0.0", "template": "tcd_user@1.0.1", "contract": "1.0.0"},
}
print(json.dumps(record, indent=2))
```

Output:

```text
{
  "story_id": "US-205",
  "verdict": "FAIL",
  "stopped_at": "",
  "findings": [
    {
      "rule": "R1",
      "severity": "error",
      "where": "story_id",
      "message": "expected 'US-205' (from input), got 'US-101'"
    }
  ],
  "versions": {
    "instructions": "1.0.0",
    "template": "tcd_user@1.0.1",
    "contract": "1.0.0"
  }
}
```

`asdict(f)` converts a dataclass into a plain dictionary that `json.dumps` can write. `{**pair["expected_output"], "story_id": "US-101"}` copies the good answer and overrides one key, a compact way to plant the R1 defect. Notice that the report's `story_id` is **US-205**: the report is filed under the story we *asked about*, which is exactly why R1 fired.

Here the versions are typed by hand; reading them from the agent's configuration and writing a run log is done later today in *Executing agents against QA requirements*, and JSON reports for CI in *Building validation scripts*.

### 11. Connecting to Project 2

In your Project 2 repository, `validate_reply` sits between the agent and everything that consumes its output. FAIL replies are rejected and logged and never reach the framework; PASS and PASS_WITH_WARNINGS replies go to human review, and only **approved** test cases become pytest parameters or TestRail imports. A requirements-review agent (Thursday's pair-programming exercise) needs the same structure: its own catalogue, rule functions with the `(input, output) -> list` signature, a `RULES` list and a `validate_reply` that stops early on a broken shape.

---

## Practice Exercises

1. **Predict, then run.** For each change to the US-205 good answer, predict every rule that fires, then check with `show()`: (a) TC-205-02's `id` becomes `TC-205-01`; (b) `status` becomes `needs_clarification` (nothing else changes); (c) the AC4 question is reworded to "Can a shopper use two coupons?"; (d) TC-205-03's `ac_ids` becomes `["AC3", "AC3"]`. (Hint for (c): what does R3 look for? For (d): which layer catches duplicates inside one array?)
2. **Twelve criteria.** Build a story input with ACs `AC1` to `AC12` and `max_cases` 10, and an output whose test cases cover `AC2` to `AC11` and whose only question mentions `AC12`. Confirm that R3 reports `AC1` as uncovered. Then change `\b` to nothing in a copy of `check_r3` and explain the different result.
3. **Tune Q2.** Collect ten realistic expected results (from Wednesday's exercises or your Project 2 stories). Run Q2 over them, count false positives and false negatives, and propose one change to `VAGUE_PHRASES`. Write down the trade-off you accepted.
4. **Add a rule end to end.** Write **B2: no real-looking email addresses** (anything matching an email pattern whose domain is not `example.com`), following the seven steps in Section 9: ID, layer, severity (justify it against the instructions' *Boundaries* section), message, function, two tests and a catalogue row.
---

## Knowledge Check

1. Why does `validate_reply` accept the reply as a **string** rather than a parsed dictionary?
<details><summary>Answer</summary>Because parsing is part of validation. A fenced, truncated or prose-wrapped reply must produce a clean S1 finding inside the report, not crash the caller before validation starts.</details>

2. A report has no R-rule findings and `stopped_at` is `"output"`. Did R1-R6 pass?
<details><summary>Answer</summary>No. They never ran. The schema failed, so validation stopped early (fail fast) because the code rules cannot trust the shape of the data.</details>

3. Which rule catches a model that silently forgets an acceptance criterion, and why is code better than a human at this?
<details><summary>Answer</summary>R3. Omission leaves nothing on the page to look at, so humans easily miss it; code can compare the full list of input ACs against what is covered or questioned.</details>

4. Why does `check_r3` search for the AC ID with `\b` word boundaries?
<details><summary>Answer</summary>So that `AC1` is not counted as "mentioned" when a question only names `AC10`, `AC12` and so on. `\b` makes the match whole-word.</details>

5. Replacing `AC1` with `AC9` in one test case produced two findings. Is that a bug in the validator?
<details><summary>Answer</summary>No. One defect has two consequences: `AC9` does not exist (R2) and AC1 is no longer covered (R3). Both findings are true.</details>

6. A reply gets **PASS**. Can its test cases go straight into the Project 2 pytest suite?
<details><summary>Answer</summary>No. PASS means no automated rule found a problem. It still goes to human review (Q3 and the Wednesday checklist); validation is not approval. The "$40.00 total" example passes every rule and is wrong.</details>

7. Why are Q1, Q2 and the new B1 **warnings** rather than errors?
<details><summary>Answer</summary>Their automated checks have known false positives (for example "applied successfully and the total is $45.00", or a legitimate `<b>` in a story about formatting). A rule that will sometimes be wrong should flag for a human, not block on its own.</details>

8. Structured-output features constrain the model's reply to a schema. Name two reasons you still validate.
<details><summary>Answer</summary>Any two of: some schema keywords (e.g. `minLength`, `minimum`) may not be supported in that mode; refusals or a `max_tokens` cut-off can still break the schema; and no such feature checks rules that compare output with input (R1-R6) or meaning (Q3).</details>


---

## Glossary

| Term | Meaning |
|---|---|
| **Output validation** | Checking every agent reply against its contract and quality rules before anything uses it. |
| **Validation report** | All findings for one reply, plus `stopped_at` and a derived verdict. |
| **Verdict** | PASS, PASS_WITH_WARNINGS or FAIL, derived from the findings' severities. |
| **Untrusted input** | Data from outside your control, including model output, that must be validated and encoded before use. |
| **Encoding** | Converting text so it is displayed safely in a context, e.g. `html.escape` for HTML. |
| **False positive** | A rule fires on output that is actually fine. |
| **False negative** | A rule stays silent on output that is actually wrong. |

---

## Summary

- Validate **every** reply: models are non-deterministic, their output is **untrusted input** (OWASP LLM05), structured-output features do not check everything, and **schema-valid but wrong** is the dangerous case.
- TestCaseDesigner's validation runs **parse → schema (S1)** with **fail fast**, then **R1-R6** (errors) and **Q1-Q2** (warnings) with **collect all**, then hands over to a **human** for Q3.
- `tcd/validation.py` models this with two data classes (`Finding`, `ValidationReport` with `errors`, `warnings`, `verdict`), one small function per rule with the same `(story, out) -> list` signature, a `RULES` list and `validate_reply`, which records `stopped_at` when it cannot go deeper.
- **FAIL** means reject and log; **PASS_WITH_WARNINGS** means review with warnings first; **PASS** still means review. **Validation is not approval.**
- One defect can fire several rules; read reports for shared causes.
- Code cannot judge correctness: a wrong but plausible expected total passes every rule. That is why Q3 belongs to a human.
- Add rules properly: example, ID, layer, severity, message, function, tests and catalogue row, in one change. Validation flags dangerous text; **encoding** in the consuming code neutralises it.
- Record verdict, `stopped_at`, every finding and the versions that produced the reply.

---

## Additional Resources

- OWASP Gen AI Security Project, *LLM05:2025 Improper Output Handling* (why model output must be treated as untrusted, validated and encoded before downstream use, with prevention strategies): https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/
- Claude Platform Docs, *Structured outputs* (how schema-constrained output works, which JSON Schema features such as `minLength` and `minimum` are unsupported, and how refusals or `max_tokens` can still break the schema, all reasons to validate in your own code): https://platform.claude.com/docs/en/build-with-claude/structured-outputs
