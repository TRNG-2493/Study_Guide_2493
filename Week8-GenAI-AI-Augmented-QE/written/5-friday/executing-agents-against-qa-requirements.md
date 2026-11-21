# Executing Agents Against QA Requirements

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **executing an agent against requirements** means: a repeatable process that turns backlog items into **reviewable, traceable evidence**, not just a model call.
- Convert a backlog **export** (CSV, one row per acceptance criterion) into input-contract documents, and apply a **readiness checklist** before running.
- Explain the **`ModelClient`** interface, use the offline `ScriptedModel`, and describe how a real adapter handles **settings**, **secrets** and **cost**.
- Read the finished `TestCaseDesigner` class and explain why the **input gate runs before the model call**.
- Run `run_requirements.py`, which records every run in a **run folder** with evidence files, a **JSON Lines** log and a **prompt fingerprint**.
- **Triage** each outcome with an action and an owner, build an **AC → test case traceability matrix**, and hand approved cases to your Project 2 framework.

---

## Why This Matters

Over the past five lessons you built every part of TestCaseDesigner: instructions, a template library, the IO contract, output validation and a validation script. Each part was tested on its own, mostly with the US-205 coupon story.

Now we put the agent to work. A real QA team does not want "an agent that once produced good tests for US-205". It wants to point the agent at **this sprint's backlog**, get draft test cases for every story, know which drafts can be trusted, and be able to answer, weeks later, "which prompt produced this test case, and did anyone review it?".

That is what **executing an agent against QA requirements** means. It is like running a test suite in CI rather than poking at one test in your IDE: a **defined set of inputs** (the backlog), every result **checked** and **recorded**, failures **triaged** with an owner, and passing results sent to **people** (review) and then into the **product** (your Project 2 framework).

This is the "run against requirements" part of the **Weekly Epic**: design and build a first QA agent with IO contracts and validation scripts. It is also exactly what you will do in today's exercise for **Project 2 (Test Automation Framework)**: run your agent over stories from the e-commerce app (login, product search, cart, checkout) and document what happened.

> **Scope note.** This lesson is about running the finished agent over a set of requirements and handling the results of **one run**. It does not measure how *reliable* the agent is across many runs, nor change its instructions to improve it: that is *Agent testing and refinement*, later today. Automatically **retrying** a failed call and **chaining** several prompts together are covered in **Week 9**. Detecting invented content in depth (the **hallucination taxonomy**), **LLM-as-judge** grading, **prompt injection** and **context-window testing** are covered in **Week 10**; here we only name them.

---

## The Concept

### 1. What "Executing an Agent" Really Means

A beginner's picture of running an agent is one line of code: send a prompt, get an answer. A professional picture has nine steps. Here they are for TestCaseDesigner:

```text
 backlog export (CSV / Jira)
        │
 [1] select & prepare requirements ── turn rows into input-contract documents
        │
 [2] input gate (S2) ──────────────── reject malformed stories; NO model call
        │
 [3] build messages ───────────────── instructions (system) + template (user)
        │
 [4] call the model ───────────────── through one ModelClient interface
        │
 [5] validate the reply ───────────── S1, R1–R6 errors; Q1–Q2 warnings
        │
 [6] record ───────────────────────── input, raw reply, versions, verdict, fingerprint
        │
 [7] triage ───────────────────────── every outcome gets an action and an owner
        │
 [8] human review ─────────────────── Wednesday's checklist and sign-off states
        │
 [9] into Project 2 ───────────────── approved cases become tests in the framework
```

Steps 2 to 5 live inside the agent itself (`tcd/agent.py`). Steps 1 and 6 live in a **runner** script (`run_requirements.py`), which loops over the backlog. Steps 7 to 9 are **people and process**, supported by small scripts.

Why so many steps? Because each one answers a question a reviewer or test lead will eventually ask: *which stories did the agent see? did we pay for a call on garbage input? which instruction version produced this? is this output safe to use? who fixes the failures? did a human approve it? where did this test in our suite come from?*

Keep this diagram in mind; the rest of the lesson walks through it from top to bottom.

### 2. Setup

Copy your project from the earlier lessons. You need this layout (new files for this lesson are marked ★):

```text
tcd_agent/
├── agent.json
├── instructions/tcd_instructions_v1.0.0.md
├── templates/            (manifest.json, partials/, tcd_user_v1.0.1.txt, ...)
├── schemas/              (tcd_input.schema.json, tcd_output.schema.json)
├── samples/              (P01–P05)
├── requirements/
│   └── backlog.csv         ★
├── replies/                ★ illustrative model replies, one per story
├── tcd/
│   ├── instructions.py  templates.py  contract.py  validation.py
│   ├── model.py            ★
│   └── agent.py            ★
├── run_requirements.py     ★
└── validate_output.py
```

You need **Python 3.11 or newer** and two packages:

```bash
pip install "jsonschema>=4.18" pytest
```

> Some lab machines still have `jsonschema` 3.2, which has no `Draft202012Validator`. Check with `python -c "import importlib.metadata as m; print(m.version('jsonschema'))"` and upgrade if needed.

Run every command from the `tcd_agent/` folder.

**About the `replies/` folder.** This lesson never calls a real model, so that everyone gets the same output and nobody needs an API key. Instead, `replies/` holds one **illustrative** reply per story, written for this lesson to show typical model behaviour, *including typical mistakes*. They are not copied from any specific model. In your own project you will replace the stand-in with a real model client (Section 5).

### 3. Preparing Requirements: From Backlog Export to Input Contract

#### 3.1 Requirements arrive as exports

Requirements rarely arrive as neat JSON. They live in a tool such as Jira, Azure Boards or a spreadsheet, and you get them out as an **export**: usually CSV. A common export shape has **one row per acceptance criterion**, repeating the story ID and title on each row. Here is our backlog for the Project 2 e-commerce app, `requirements/backlog.csv`:

```text
story_id,title,ac_id,ac_text
US-101,Log in to my account,AC1,A registered shopper who enters a valid email and password is taken to the My Account page.
US-101,Log in to my account,AC2,"A wrong email or password shows ""Invalid email or password""."
US-101,Log in to my account,AC3,The account is locked for 15 minutes after 5 failed login attempts.
US-205,Apply coupon at checkout,AC1,SAVE10 gives 10% off a subtotal of $50.00 or more.
US-205,Apply coupon at checkout,AC2,"Subtotals under $50.00 are unchanged and show ""Spend $50.00 to use SAVE10""."
US-205,Apply coupon at checkout,AC3,"Unknown codes show ""Coupon code not recognised""."
US-205,Apply coupon at checkout,AC4,Only one coupon per order.
US-310,Enter a shipping address,AC1,"Name, street, city, ZIP and phone are required."
US-310,Enter a shipping address,AC2,ZIP must be exactly 5 digits.
US-310,Enter a shipping address,AC3,Phone must be exactly 10 digits.
US-310,Enter a shipping address,AC4,The address form must be fast and user-friendly.
US-412,Search products by keyword,AC1,Searching for a keyword lists every product whose name contains that keyword.
US-412,Search products by keyword,AC2,"A search with no matches shows ""No products found""."
US-412,Search products by keyword,AC3,"A search term shorter than 2 characters shows ""Enter at least 2 characters""."
US-450,Add a product to the cart,AC1,Clicking Add to cart increases the cart badge count by 1.
US-450,Add a product to the cart,AC2,"A shopper cannot add more than 10 of one product; the 11th add shows ""Maximum 10 per product""."
US-52,Wishlist,AC1,Save for later.
```

A few things to notice before any code runs:

- **CSV quoting.** A field that contains a comma or a double quote is wrapped in double quotes, and a double quote *inside* it is written twice (`""`). So `"A wrong email or password shows ""Invalid email or password""."` means the text `A wrong email or password shows "Invalid email or password".` Python's `csv` module handles this for you; never split CSV lines with `line.split(",")`.
- **US-101, US-205, US-310** are this week's stories; **US-412 (product search)** and **US-450 (add to cart)** are new Project 2 stories.
- **US-310 AC4** ("fast and user-friendly") is **vague on purpose**: a good agent should ask about it, not test it.
- **US-52** is **malformed on purpose** (a two-digit ID, and "Save for later." is hardly a criterion), to prove the gate works.

#### 3.2 By hand first: US-101

The input contract (Thursday) wants one JSON object per story:

```json
{
  "story_id": "US-101",
  "title": "Log in to my account",
  "acceptance_criteria": [
    {"id": "AC1", "text": "A registered shopper who enters a valid email and password is taken to the My Account page."},
    {"id": "AC2", "text": "A wrong email or password shows \"Invalid email or password\"."},
    {"id": "AC3", "text": "The account is locked for 15 minutes after 5 failed login attempts."}
  ]
}
```

To build it by hand you would: read the first US-101 row and start a new story object with its ID and title and an empty AC list; append AC1; read the next row, see the **same** story ID, and append AC2 to the **existing** object; do the same for AC3; then move on when a new story ID appears. Notice that `techniques` and `max_cases` are not in the export. That is fine: they are optional, and the contract module fills in the defaults (`["EP", "BVA"]` and `10`) at the gate.

#### 3.3 The code: `load_backlog`

This function lives at the top of `run_requirements.py`:

```python
def load_backlog(path: str) -> list:
    """One CSV row per acceptance criterion -> one input-contract dict per story."""
    stories = OrderedDict()
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            story = stories.setdefault(row["story_id"], {
                "story_id": row["story_id"], "title": row["title"], "acceptance_criteria": []})
            story["acceptance_criteria"].append({"id": row["ac_id"], "text": row["ac_text"]})
    return list(stories.values())
```

Line by line:

- **`open(path, newline="", encoding="utf-8")`**. `newline=""` is what the `csv` documentation asks for: it lets the `csv` module handle line endings itself, so a quoted field containing a newline is not broken in two. `encoding="utf-8"` makes the file read the same on Windows and Linux (and handles characters such as `£` or `é`).
- **`csv.DictReader(f)`** reads the first line as the **header** and then gives you each following row as a dictionary keyed by the header names: `{"story_id": "US-101", "title": "Log in to my account", "ac_id": "AC1", "ac_text": "A registered..."}`. Using names instead of positions (`row[3]`) means the code still works if someone reorders the export's columns.
- **`OrderedDict()`** is a dictionary that remembers insertion order (plain `dict` does too since Python 3.7; `OrderedDict` just makes the intention visible: the run summary should follow the backlog order).
- **`stories.setdefault(key, default)`** is the heart of the grouping. It means: "if `key` is already in the dictionary, return its value; otherwise store `default` under `key` and return that." So the first US-101 row creates the story object; the second and third US-101 rows get the **same** object back, and their ACs are appended to it. This is exactly the by-hand procedure from 3.2, in one line.
- **`story["acceptance_criteria"].append(...)`** adds one `{"id", "text"}` object per row, in the order the rows appear.
- **`return list(stories.values())`** returns just the story objects, in backlog order.

Let us check it does what we did by hand:

```python
# peek_backlog.py
import json
from run_requirements import load_backlog

stories = load_backlog("requirements/backlog.csv")
print(len(stories), "stories:", [s["story_id"] for s in stories])
print(json.dumps(stories[0], indent=2))
```

Output:

```text
6 stories: ['US-101', 'US-205', 'US-310', 'US-412', 'US-450', 'US-52']
{
  "story_id": "US-101",
  "title": "Log in to my account",
  "acceptance_criteria": [
    {
      "id": "AC1",
      "text": "A registered shopper who enters a valid email and password is taken to the My Account page."
    },
    {
      "id": "AC2",
      "text": "A wrong email or password shows \"Invalid email or password\"."
    },
    {
      "id": "AC3",
      "text": "The account is locked for 15 minutes after 5 failed login attempts."
    }
  ]
}
```

Seventeen rows became six stories, and US-101 matches the hand-built version exactly, including the unescaped quotes around the error message.

> **Notice what `load_backlog` does *not* do.** It does not check the stories. US-52 comes out as a perfectly ordinary dictionary. Checking is the gate's job (Section 6), and keeping "convert" and "check" separate means each is simple and testable.

#### 3.4 A readiness checklist before you run

Running an agent costs money and reviewer time. Spend two minutes on the backlog first. This is Wednesday's requirements analysis and responsible-use thinking, applied at the batch level:

1. **Every story and every AC has an ID.** Without `AC2`, nobody can say which test checks which rule.
2. **ACs are testable, or you expect questions.** Vague ACs (US-310 AC4) may go in, but expect `needs_clarification` and have a product owner ready.
3. **No personal data or secrets.** Exports can contain real customer emails or passwords in "steps to reproduce"; redact them first (Wednesday).
4. **The data is approved for the tool** (Wednesday's "shadow AI" warning).
5. **The batch is a sensible size.** 500 stories failing for the same reason is an expensive way to find a template typo.
6. **You know which agent version you are running.** Check `agent.json` before the run.

### 4. The Model Client Interface: `tcd/model.py`

#### 4.1 One method, many models

The agent should not care **which** model answers: a commercial API, a model running inside your company, or an offline stand-in for lessons and tests. We achieve that with an **interface**: an agreement that every model client offers the same method with the same inputs and outputs.

```python
# tcd/model.py
"""Model clients. Every client has the same method: complete(messages, settings) -> str."""
import re
from pathlib import Path
from typing import Protocol


class ModelClient(Protocol):
    def complete(self, messages: list, settings: dict) -> str: ...


class ScriptedModel:
    """Offline stand-in: returns a pre-written reply for each story.
    The replies in replies/ are ILLUSTRATIVE, written for this lesson to show
    typical model behaviour (including typical mistakes)."""

    def __init__(self, folder: str = "replies"):
        self.folder = Path(folder)
        self.calls = 0

    def complete(self, messages: list, settings: dict) -> str:
        self.calls += 1
        story_id = re.search(r"^ID: (US-\d{3})$", messages[-1]["content"], re.MULTILINE).group(1)
        return (self.folder / f"{story_id}.txt").read_text(encoding="utf-8")
```

**`ModelClient(Protocol)`** describes the interface. `typing.Protocol` comes from Python's type-hinting system: a class that inherits from `Protocol` lists methods that *any* compatible object must have, without anyone needing to inherit from it. The body `...` (the Ellipsis) means "no implementation here; this is only a description".

This style is called **duck typing** ("if it walks like a duck and quacks like a duck, it is a duck"). `ScriptedModel` does **not** inherit from `ModelClient`, yet it *is* a model client because it has a matching `complete` method. Type checkers such as `mypy` can use the `Protocol` to verify this; Python itself does not enforce it at run time.

The method's contract is deliberately small:

- **`messages`**: the role/content list you built on Thursday (`[{"role": "system", ...}, {"role": "user", ...}]`).
- **`settings`**: a dictionary of model settings such as `temperature` and `max_tokens`, taken from `agent.json`.
- **Returns**: the model's reply as **raw text**. Not a dictionary. Parsing and checking the text is the contract module's job, so every client, real or fake, goes through the same checks.

#### 4.2 The `ScriptedModel` stand-in

- **`self.calls = 0`** counts how many times the model was called. We will use it to prove that rejected stories never reach the model.
- **`re.search(r"^ID: (US-\d{3})$", ..., re.MULTILINE)`** finds the line `ID: US-205` in the **user** message (`messages[-1]` is the last message). The template's story block always contains that line (Thursday's template anatomy), so the stand-in can tell which story it is being asked about. `\d{3}` means exactly three digits; `( )` captures the ID; `.group(1)` returns it.
- **`read_text(...)`** returns the contents of `replies/US-205.txt` **exactly as stored**, including any mistakes in it. The stand-in does not tidy anything up.

The `settings` argument is accepted but not used: a stand-in has nothing to configure. Accepting it anyway keeps the method signature identical to a real client.

#### 4.3 How a real provider would plug in (sketch, not run)

To use a real model you write one more class with the same `complete` method. Every provider's SDK is different, so the sketch below uses **placeholders** rather than any real library call. It is **not run** in this lesson.

```python
# NOT RUN: a sketch of a real adapter. Replace the placeholders with your
# provider's documented SDK calls.
import os

class ProviderModel:
    def __init__(self):
        api_key = os.environ["MODEL_API_KEY"]           # secret comes from the environment
        self.client = make_provider_client(api_key)     # placeholder for your SDK's client
        self.calls = 0

    def complete(self, messages: list, settings: dict) -> str:
        self.calls += 1
        response = self.client.send(                    # placeholder for your SDK's call
            model=settings["model"],
            messages=messages,
            temperature=settings["temperature"],
            max_tokens=settings["max_tokens"],
        )
        return response_text(response)                 # placeholder: extract the reply text
```

The ideas that matter are independent of the provider:

- **Secrets come from environment variables**, never from code, `agent.json` or the backlog. A key written into a file ends up in Git history, logs and screenshots. If the variable is missing, `os.environ[...]` raises `KeyError` at once: a loud failure.
- **The adapter only translates** our messages and settings into the provider's request, and returns plain text. Checking, retrying and recording stay outside it, so swapping providers is a one-class change. (It also hides differences such as where the system message goes.)

#### 4.4 Model settings, and what they do *not* guarantee

Our `agent.json` contains:

```json
"model_settings": {"temperature": 0, "max_tokens": 2000}
```

- **`temperature`** controls randomness in choosing the next token (Monday's generative AI concepts). `0` makes replies **much more repeatable** but not identical: providers can still vary run to run, and may update the model behind a name. Treat every run as a sample.
- **`max_tokens`** caps the length of the reply. A reply that hits the cap is **cut off mid-JSON** and the parser rejects it; the fix is a larger cap or a smaller `max_cases`, not a looser parser.
- **Cost and rate limits.** Providers charge by tokens and limit requests per minute. The instructions are sent on **every** call, so a rejected story that never reaches the model costs nothing.

### 5. The Agent, Wired Together: `tcd/agent.py`

Here is the complete agent class. Every import is something you built earlier this week.

```python
# tcd/agent.py
"""TestCaseDesigner: instructions + template + contract + model + validation, wired together."""
import json
from dataclasses import dataclass, field
from pathlib import Path

from tcd.contract import CONTRACT_VERSION, ContractError, check_input
from tcd.instructions import load_instructions
from tcd.templates import TemplateLibrary, story_values
from tcd.validation import ValidationReport, validate_reply

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class AgentRun:
    story_id: str
    outcome: str                     # "rejected_input" | "FAIL" | "PASS" | "PASS_WITH_WARNINGS"
    messages: list = field(default_factory=list)
    reply: str = ""
    report: ValidationReport = None
    input_errors: list = field(default_factory=list)
    story: dict = None               # the gated input, with defaults applied


class TestCaseDesigner:
    def __init__(self, model, config: str = "agent.json"):
        self.config = json.loads((ROOT / config).read_text(encoding="utf-8"))
        if self.config["contract_version"] != CONTRACT_VERSION:
            raise ValueError("agent.json and tcd/contract.py disagree on the contract version")
        self.instructions = load_instructions(ROOT / self.config["instructions"],
                                              expected_contract=CONTRACT_VERSION)
        self.templates = TemplateLibrary(ROOT / "templates")
        self.model = model

    def build_messages(self, story: dict) -> list:
        name, version = self.config["template"]["name"], self.config["template"]["version"]
        available = {**story_values(story), "agent_name": self.config["agent"],
                     "contract_version": CONTRACT_VERSION}
        wanted = self.templates.variables(name, version)       # pass only what it uses
        user = self.templates.render(name, version, {k: v for k, v in available.items() if k in wanted})
        return [{"role": "system", "content": self.instructions.text},
                {"role": "user", "content": user}]

    def run(self, raw_story: dict) -> AgentRun:
        story_id = str(raw_story.get("story_id"))
        try:
            story = check_input(raw_story)                     # 1. input gate
        except ContractError as exc:
            return AgentRun(story_id, "rejected_input", input_errors=exc.errors)
        messages = self.build_messages(story)                  # 2. instructions + template
        reply = self.model.complete(messages, self.config["model_settings"])   # 3. model
        report = validate_reply(story, reply)                  # 4. output validation
        return AgentRun(story_id, report.verdict, messages, reply, report, story=story)
```

#### 5.1 `ROOT` and `AgentRun`

- **`ROOT = Path(__file__).resolve().parent.parent`** is the project folder (`agent.py` → `tcd/` → project), so files are found wherever you start Python.
- **`AgentRun`** is a `@dataclass`: a class whose `__init__` Python writes for you from the annotated fields. It is the agent's **result object**: one per story, holding everything the runner records.
- **`field(default_factory=list)`** gives each `AgentRun` its **own** new empty list. Writing `messages: list = []` would be a bug (and dataclasses refuse it): every object would share one list.
- Fields with defaults (`reply=""`, `report=None`, `story=None`) let a **rejected** run be created with only three values, because a rejected story never gets messages, a reply or a report.

#### 5.2 `__init__`: fail at start-up, not halfway through a batch

The constructor loads everything **once** and checks that the pieces agree: it reads `agent.json` (the agent's manifest), refuses to start if its `contract_version` differs from the one `tcd/contract.py` implements, loads the instructions with `load_instructions(..., expected_contract=CONTRACT_VERSION)` (which rejects a missing header, missing sections or a mismatched contract), and loads the template library (which checks its manifest against the files). Finally it **stores the model client it was given** rather than creating one: this is **dependency injection**, and it is what lets us test the agent offline with `ScriptedModel` and later pass in a real adapter.

All these checks happen **before the first story is processed**. A broken instruction file should stop the run in the first second, not after 40 stories were sent with the wrong text.

#### 5.3 `build_messages`: only the values the template needs

- **`available`** collects every value we *could* supply: the story values (`story_id`, `title`, `acceptance_criteria`, `techniques`, `max_cases`, from `story_values`) plus `agent_name` and `contract_version` for the `output_reminder` partial. `{**a, "k": v}` builds a new dictionary from `a` plus extra keys.
- **`wanted = self.templates.variables(name, version)`** asks the library which values this template (and its partials) actually uses.
- **The dictionary comprehension** `{k: v for k, v in available.items() if k in wanted}` keeps only those. Why? Because the template library treats an **unused value** as an error (Thursday's "extra variable" failure mode). Filtering here lets the same agent code work with `tcd_user@1.0.0` (no partials, no `agent_name`) and `tcd_user@1.0.1` (with partials) without any `if` statements.
- **The return value** is the familiar two-message list: instructions as the **system** message, exactly as stored in the file; the rendered template as the **user** message.

#### 5.4 `run`: four steps, in a deliberate order

1. **Input gate.** `check_input` validates the raw story against the input schema and returns a copy with defaults applied. If it raises `ContractError`, the method returns a `rejected_input` result immediately.
2. **Build messages** from the *gated* story (so defaults such as `max_cases: 10` appear in the prompt).
3. **Call the model** through the client interface, passing the settings from `agent.json`.
4. **Validate the reply** against the gated story, producing a `ValidationReport` whose `verdict` becomes the run's `outcome`.

**Why does the gate come before the model call?** **Cost** (a doomed call wastes money and time), **quality** (given a broken story, a model happily invents requirements) and **blame** (a rejected input is the caller's problem, a failed output is the agent's, and keeping them apart saves debugging time).

Notice also what `run` does **not** do: it never edits the reply, never strips fences, never retries. It reports what happened honestly. Deciding what to do about a failure belongs to triage (Section 8) and, for automatic retries, to Week 9.

### 6. The Runner: `run_requirements.py`

The agent handles **one** story. The runner handles **a batch**: it loads the backlog, runs the agent on each story and records everything. You have already seen `load_backlog`; here is the rest.

```python
# run_requirements.py
"""Execute TestCaseDesigner against every story in a requirements file and record the run."""
import argparse
import csv
import hashlib
import json
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

from tcd.agent import TestCaseDesigner
from tcd.model import ScriptedModel

# ... load_backlog (Section 3.3) ...


def fingerprint(messages: list) -> str:
    """Short hash of exactly what the model was sent: same prompt -> same fingerprint."""
    joined = "\n".join(f"{m['role']}:{m['content']}" for m in messages)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run TestCaseDesigner over a backlog.")
    parser.add_argument("backlog", help="CSV file: story_id,title,ac_id,ac_text")
    parser.add_argument("--run-id", default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    args = parser.parse_args()

    model = ScriptedModel("replies")
    agent = TestCaseDesigner(model)
    run_dir = Path("runs") / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for story in load_backlog(args.backlog):
        result = agent.run(story)
        record = {
            "run_id": args.run_id, "story_id": result.story_id, "outcome": result.outcome,
            "agent_version": agent.config["version"],
            "instructions_version": agent.instructions.version,
            "template": f"{agent.config['template']['name']}@{agent.config['template']['version']}",
            "contract_version": agent.config["contract_version"],
            "model_settings": agent.config["model_settings"],
            "prompt_fingerprint": fingerprint(result.messages) if result.messages else None,
            "errors": result.input_errors or [f"{f.rule} {f.where}: {f.message}" for f in result.report.errors],
            "warnings": [] if result.report is None else
                        [f"{f.rule} {f.where}: {f.message}" for f in result.report.warnings],
        }
        if result.reply:                                   # keep the evidence: what went in, what came out
            (run_dir / f"{result.story_id}.input.json").write_text(
                json.dumps(result.story, indent=2), encoding="utf-8")
            (run_dir / f"{result.story_id}.reply.txt").write_text(result.reply, encoding="utf-8")
        records.append(record)

    with open(run_dir / "run.jsonl", "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

    print(f"run {args.run_id}: {len(records)} stories, {model.calls} model calls")
    print(f"{'story':<8} {'outcome':<19} {'err':>3} {'warn':>4}  fingerprint")
    for r in records:
        print(f"{r['story_id']:<8} {r['outcome']:<19} {len(r['errors']):>3} {len(r['warnings']):>4}  {r['prompt_fingerprint']}")


if __name__ == "__main__":
    main()
```

#### 6.1 Command-line arguments and the run ID

- **`parser.add_argument("backlog", ...)`** is a **positional** argument: the first thing after the script name is the CSV path. (You used `argparse` in depth in *Building validation scripts*.)
- **`--run-id`** is optional. Its default is the current **UTC** time, such as `20261023T101500Z` (`%Y%m%d`, a `T`, `%H%M%S`, `Z` for UTC): the same for every time zone, and it sorts in date order.
- In this lesson we pass `--run-id demo` so that your output matches the text exactly.

#### 6.2 The run folder

`run_dir = Path("runs") / args.run_id` and `mkdir(parents=True, exist_ok=True)` create `runs/demo/` (and `runs/` if needed). Every run gets **its own folder**, which is the simplest way to never mix up evidence from two runs. (`exist_ok=True` means re-using a run ID does not crash; Section 10 explains why you should still avoid it for real runs.)

#### 6.3 The prompt fingerprint

`fingerprint` turns the exact messages into a short code:

- It joins every message as `role:content` with newlines, so both the role and the text count.
- **`hashlib.sha256(...)`** computes a **cryptographic hash**: a 256-bit "summary" of the bytes. Change one character, even a trailing space, and the hash changes completely. `.encode("utf-8")` turns the string into bytes, which is what hash functions work on.
- **`.hexdigest()[:12]`** writes the hash as 64 hexadecimal characters and keeps the first 12. Twelve hex characters (48 bits) are plenty to tell prompts apart in a QA project; we are not using it for security.

A quick demonstration that one extra space produces a different fingerprint:

```python
from run_requirements import fingerprint
m = [{"role": "system", "content": "A"}, {"role": "user", "content": "B"}]
print(fingerprint(m))
m[1]["content"] = "B "
print(fingerprint(m))
```

```text
809a338b9c7b
c52bd12c2f48
```

**Why bother?** Versions in `agent.json` tell you which *files* were meant to be used. The fingerprint tells you what was *actually sent*. Same fingerprint in two runs means byte-for-byte identical prompts, so any difference in replies came from the model. A changed fingerprint with unchanged versions means a file was edited without a version bump, or the story text changed.

#### 6.4 The run record

For each story the runner builds one dictionary, the **record**: what was run and what happened (`run_id`, `story_id`, `outcome`), which version of every part produced it (`agent_version`, `instructions_version`, `template`, `contract_version`), the `model_settings`, the `prompt_fingerprint` (`None` if nothing was sent), and the `errors` and `warnings`.

Two lines deserve a closer look:

- **`result.input_errors or [...]`**: `or` returns the left side if it is "truthy" (a non-empty list), otherwise the right side. So rejected stories record their input errors, and every other story records its validation errors as readable strings like `"R2 test_cases[3].ac_ids: ..."`.
- **`[] if result.report is None else [...]`**: a **conditional expression**. A rejected story has no report, so it has no warnings.

#### 6.5 Evidence files and the JSON Lines log

- For every story that reached the model (`if result.reply:`), the runner saves **two evidence files**: `<story>.input.json`, the **gated** input including defaults (exactly what the agent worked from), and `<story>.reply.txt`, the **raw** reply exactly as the model returned it, mistakes and all. Never save only a "cleaned" version: when someone disputes a result, the raw reply is the evidence.
- These two files use exactly the `X.input.json` + `X.reply.txt` layout that `validate_output.py --run` expects. That is deliberate.
- **`run.jsonl`** is the run log in **JSON Lines** format: one complete JSON object per line. `json.dumps(record)` (without `indent`) produces a single line, and `+ "\n"` ends it. JSON Lines is popular for logs because you can append a line at a time, read the file line by line without loading it all, and process it with ordinary tools (`grep US-412 runs/demo/run.jsonl`).

### 7. Running It for Real

```bash
python run_requirements.py requirements/backlog.csv --run-id demo
```

Output:

```text
run demo: 6 stories, 5 model calls
story    outcome             err warn  fingerprint
US-101   PASS_WITH_WARNINGS    0    1  1c00aa5c9c05
US-205   PASS                  0    0  94e1b85d69cf
US-310   PASS                  0    0  2214461a100a
US-412   FAIL                  1    0  5e789d76109f
US-450   FAIL                  1    0  16b248b7db56
US-52    rejected_input        1    0  None
```

Read the first line carefully: **6 stories, 5 model calls**. The gate rejected US-52 before the model was ever called, and its fingerprint is `None` because nothing was sent. On a real provider that is one call you did not pay for.

The run folder:

```bash
ls runs/demo
```

```text
US-101.input.json
US-101.reply.txt
US-205.input.json
US-205.reply.txt
US-310.input.json
US-310.reply.txt
US-412.input.json
US-412.reply.txt
US-450.input.json
US-450.reply.txt
run.jsonl
```

Five pairs of evidence files (no files for US-52, which never reached the model) and one log. Here is the first line of `run.jsonl`, pretty-printed with `head -1 runs/demo/run.jsonl | python -m json.tool`:

```json
{
    "run_id": "demo",
    "story_id": "US-101",
    "outcome": "PASS_WITH_WARNINGS",
    "agent_version": "1.0.0",
    "instructions_version": "1.0.0",
    "template": "tcd_user@1.0.1",
    "contract_version": "1.0.0",
    "model_settings": {
        "temperature": 0,
        "max_tokens": 2000
    },
    "prompt_fingerprint": "1c00aa5c9c05",
    "errors": [],
    "warnings": [
        "Q2 test_cases[0].expected_result: vague phrase 'works correctly'; state the exact total, message or state"
    ]
}
```

The US-52 line has `"outcome": "rejected_input"`, `"prompt_fingerprint": null` and one error: `story_id: 'US-52' does not match '^US-[0-9]{3}$'`. Notice that "Save for later." (15 characters) passes the schema's `minLength: 10`: the schema checks shape, not quality, so the human readiness check is still needed.

#### 7.1 Re-checking the evidence independently

The runner already validated each reply. Why validate again? Because **evidence should be checkable by someone who does not trust the runner**: a reviewer, a CI job, or you next week after changing a rule. The validation script from the previous lesson reads only the files on disk:

```bash
python validate_output.py --run runs/demo
```

```text
PASS_WITH_WARNINGS  runs/demo/US-101.reply.txt
    WARNING Q2  test_cases[0].expected_result: vague phrase 'works correctly'; state the exact total, message or state
PASS                runs/demo/US-205.reply.txt
PASS                runs/demo/US-310.reply.txt
FAIL                runs/demo/US-412.reply.txt
    ERROR   R2  test_cases[3].ac_ids: 'AC4' is not an acceptance criterion of US-412 (expected one of ['AC1', 'AC2', 'AC3'])
FAIL                runs/demo/US-450.reply.txt
    ERROR   S1  (reply): reply is wrapped in Markdown fences; the contract forbids them
5 checked, 3 passed, 2 failed
```

The exit code is `1` because two replies failed. The independent check agrees with the runner's summary, story by story. If it ever disagreed, that would itself be a bug worth investigating (for example, a validator rule changed between the run and the re-check).

You can also check reproducibility: running the same command again with `--run-id demo2` prints exactly the same fingerprints (`1c00aa5c9c05` for US-101, and so on), because the backlog, instructions and template did not change.

### 8. Triage: Every Outcome Gets an Action and an Owner

A run is not finished when the summary prints. Each outcome needs a decision. Let us go through them one by one.

**US-101: `PASS_WITH_WARNINGS`.** Every rule passed, but `TC-101-01` says `"expected_result": "Login works correctly"`, which a tester cannot observe; AC1 says the shopper "is taken to the My Account page". **Action:** human review with the warning highlighted; the reviewer rewrites the expected result and records the correction (Wednesday's correction log). Warnings do not block output; they tell the reviewer where to look first.

**US-205: `PASS`.** Includes the $50.00 / $49.99 boundary pair and an open question about AC4. **Action:** normal review, and the AC4 question goes to the product owner. `PASS` means "no rule found a problem", not "correct": a human still checks meaning (Q3).

**US-310: `PASS`, status `needs_clarification`.** Tests for AC1 to AC3 and two questions about the vague AC4. This is the agent doing exactly what its instructions say: ask, don't guess. **Action:** questions to the **product owner**, test cases to review; re-run once AC4 has measurable targets.

**US-412: `FAIL` (R2).** Look at test case 4 in the raw reply:

```json
{"id": "TC-412-04", "title": "Search ignores upper and lower case", "ac_ids": ["AC4"],
 "type": "positive", "priority": "low", "steps": ["Search for \"LAMP\""],
 "expected_result": "Same results as searching for \"lamp\""}
```

(Shown compactly; the file stores it indented.) US-412 has only AC1 to AC3. The agent **invented** a requirement (case-insensitive search) and an ID for it. The JSON is perfectly shaped, so only a cross-document rule could catch it, and R2 did. **Action:** reject the whole output, do not hand-edit it, and log it as a candidate for refinement. Above all, **never "fix" the requirement to match the agent**: case-insensitive search may be a good idea, but that is the product owner's decision, raised as a question, not a rule smuggled into the backlog because a model suggested it.

**US-450: `FAIL` (S1).** The reply is wrapped in a Markdown fence. The JSON inside may be fine, but the contract forbids fences. **Action:** reject and count it as format drift; automatic re-asking is a **retry strategy** (Week 9).

**US-52: `rejected_input`.** The model was never called. **Action:** a backlog problem, returned to the backlog owner to fix the ID and write real criteria.

The same decisions as a **triage table**, which you can reuse in your exercise write-up:

| Outcome | What it means | Action | Owner |
|---|---|---|---|
| `rejected_input` | Story broke the input contract; no model call | Fix the story in the backlog, re-run | Backlog owner (BA / product owner) |
| `FAIL` (S1, parse/schema) | Reply unusable as data | Reject; re-run later; count it (retries: Week 9) | Agent owner (QE) |
| `FAIL` (R1–R6) | Shape fine, meaning broken (e.g. invented AC) | Reject; log for refinement; never hand-patch | Agent owner (QE) |
| `PASS_WITH_WARNINGS` | Usable, with flagged quality risks | Human review, starting with the warnings | Reviewer (tester) |
| `PASS` + `ok` | Usable, nothing flagged | Normal human review | Reviewer (tester) |
| `PASS` + `needs_clarification` | Usable; agent asked questions | Questions to PO; test cases to review | PO + reviewer |

Why "reject and never hand-patch" a failed output? Because a patched output **looks** like agent output in the run folder but is not. The evidence would lie, and your measure of how well the agent works (later today) would be wrong.

### 9. From Run to Review to Project 2

#### 9.1 Human review

Only outputs that passed validation go to people. On Wednesday you learned the review checklist (C1 to C9) and the sign-off states. Apply them here: each test case from US-101, US-205 and US-310 is reviewed, corrected if needed, and marked approved or rejected. Only **approved** cases go any further. Keep the review decision next to the run (for example `runs/demo/review.csv` with test case ID, reviewer, state, correction), so the chain from requirement to test stays unbroken.

#### 9.2 A traceability matrix from the run

Before review, it helps to see at a glance which ACs are covered by which test cases, and which are waiting on a question. The run folder has everything we need:

```python
# trace_matrix.py
"""Build an AC -> test case traceability matrix from the PASSING outputs of one run."""
import json
import sys
from pathlib import Path

run_dir = Path(sys.argv[1])
records = [json.loads(line) for line in (run_dir / "run.jsonl").read_text(encoding="utf-8").splitlines()]

print(f"{'story':<8} {'AC':<4} {'test cases':<24} open question?")
for rec in records:
    if not rec["outcome"].startswith("PASS"):
        continue                                   # only validated outputs are traced
    sid = rec["story_id"]
    story = json.loads((run_dir / f"{sid}.input.json").read_text(encoding="utf-8"))
    output = json.loads((run_dir / f"{sid}.reply.txt").read_text(encoding="utf-8"))
    questions = " ".join(output["open_questions"])
    for ac in story["acceptance_criteria"]:
        cases = [tc["id"] for tc in output["test_cases"] if ac["id"] in tc["ac_ids"]]
        asked = "yes" if ac["id"] in questions else ""
        print(f"{sid:<8} {ac['id']:<4} {', '.join(cases) or '-':<24} {asked}")
```

Run it with `python trace_matrix.py runs/demo`:

```text
story    AC   test cases               open question?
US-101   AC1  TC-101-01                
US-101   AC2  TC-101-02, TC-101-03     
US-101   AC3  TC-101-04, TC-101-05     
US-205   AC1  TC-205-01                
US-205   AC2  TC-205-02                
US-205   AC3  TC-205-03                
US-205   AC4  -                        yes
US-310   AC1  TC-310-01                
US-310   AC2  TC-310-02                
US-310   AC3  TC-310-03                
US-310   AC4  -                        yes
```

How it works:

- **`sys.argv[1]`** is the run folder given on the command line.
- **Reading `run.jsonl`**: `.splitlines()` gives one line per record, and `json.loads` parses each.
- **`startswith("PASS")`** keeps `PASS` and `PASS_WITH_WARNINGS` only. Tracing US-412 would put its invented AC4 into a coverage report; and `json.loads` on the reply is safe only *because* validation already parsed it. Validate first, then trust.
- **The list comprehension** collects every test case whose `ac_ids` contain this AC; `', '.join(cases) or '-'` prints `-` for an empty list (an empty string is "falsy").
- **`ac["id"] in questions`** is a simple substring check. It is good enough for this backlog, but note a limitation: `"AC1" in "AC10 ..."` is also `True`. The validator's R3 uses a regular expression with word boundaries (`\bAC1\b`) for exactly this reason; Practice Exercise 4 asks you to fix this script the same way.

The matrix shows full coverage: every AC has at least one test case or an open question. That is rule R3, viewed from a reviewer's side. It also makes the gaps that matter to the business obvious: two ACs are blocked on the product owner.

#### 9.3 Into the Project 2 framework

Once cases are approved, they move into your test automation framework. On Wednesday you saw the main routes; briefly:

- **Data-driven pytest.** Approved test cases (or their data) are written to a JSON fixture file, and a test uses `@pytest.mark.parametrize` with `ids=[tc["id"] for tc in cases]`. Each pytest result is then labelled `TC-205-01`, `TC-205-02` and so on, so a failing CI test points straight back to its test case, its AC and the run that designed it.
- **Test management import.** The same approved cases can be exported to a TestRail-style CSV for manual execution or tracking.
- **Page objects and automation code** are written (or AI-assisted, with review) per Wednesday's automation lesson; the agent designs the *tests*, it does not write the automation.

Keep the IDs stable all the way through. The ID chain `US-205 → AC1 → TC-205-01 → test_apply_coupon[TC-205-01]` is your traceability.

### 10. Operating Notes: Running Agents Like a Professional

- **Make runs re-runnable.** Everything except the model's reply (backlog snapshot, instructions, templates, schemas, `agent.json`) is in version control, so the same inputs give the same fingerprints.
- **Never overwrite evidence.** Use a fresh run ID per real run (the timestamp default does this); we used `demo` only for reproducible lesson output.
- **Keep run folders out of Git, but keep them.** Add `runs/` to `.gitignore`; store real runs as CI artifacts or in shared storage with a retention period.
- **Log what helps, not what hurts.** Log versions, fingerprints, outcomes and rule IDs; never API keys, passwords or personal data. The standard `logging` module (see resources) is the next step after `print`.
- **Watch batch size and cost.** Run a few stories first, read the results, then run the rest; track model calls per run.
- **One run is one sample.** Whether the agent is *reliable* needs many runs over known pairs: *Agent testing and refinement*, later today.

---

## Practice Exercises

1. **Add a story to the backlog.** Add US-520 "Remove a product from the cart" to `requirements/backlog.csv` with two ACs (for example: removing the last item shows "Your cart is empty"; the badge count decreases by 1). Write a matching illustrative reply in `replies/US-520.txt` that should **pass**. Run with `--run-id ex1` and confirm US-520 shows `PASS` and 6 model calls.
2. **Prove the gate saves calls.** Add one more row for a story with a malformed ID, `US-7`, and an AC of fewer than 10 characters (`Fast.`). Predict before you run: what outcome will US-7 get, how many errors will its `run.jsonl` line list, and how many model calls will the summary report? Then run with `--run-id ex2` and check your prediction.
3. **Fingerprints as detectives.** Run the backlog with `--run-id fp1`. Change one word in `instructions/tcd_instructions_v1.0.0.md` **without** changing its version, then run again with `--run-id fp2`. Compare the two `run.jsonl` files. Which fields changed and which did not? What does that tell you about the team's versioning discipline?
4. **Fix the matrix's substring bug.** In `trace_matrix.py`, replace `ac["id"] in questions` with a regular expression using word boundaries, like R3 in `tcd/validation.py`. Test it with a fake question text containing `AC10` and an AC with ID `AC1`.
5. **Triage write-up.** For your own Project 2 agent run in today's exercise, fill in a triage table like Section 8's, one row per story, with outcome, action and owner.

---

## Knowledge Check

1. Name the nine steps of executing an agent against requirements, and say which ones live inside `TestCaseDesigner.run`.

<details><summary>Answer</summary>Select and prepare requirements, input gate, build messages, call the model, validate the reply, record, triage, human review, hand over to Project 2. The gate, message building, model call and validation (steps 2 to 5) live inside <code>run</code>; preparing and recording are in the runner; triage, review and hand-over are people and process.</details>


2. `ScriptedModel` does not inherit from `ModelClient`. Why can the agent still use it?

<details><summary>Answer</summary>Because of duck typing: the agent only needs an object with a <code>complete(messages, settings)</code> method that returns a string. <code>ModelClient</code> is a <code>typing.Protocol</code> that documents this shape and lets type checkers verify it; it does not have to be inherited.</details>

3. Why does the gate run before the model call? Give three reasons.

<details><summary>Answer</summary>Cost (a doomed call is wasted money and time), quality (broken input makes the model invent requirements), and blame (input problems belong to the caller, output problems to the agent, so separating them speeds up debugging).</details>

4. With `temperature` set to 0, are two runs guaranteed to return identical replies?

<details><summary>Answer</summary>No. Temperature 0 makes replies much more repeatable but many providers still show small differences, and the model behind a name can be updated. Treat each run as a sample.</details>

5. Two runs of US-205 have identical version fields but different `prompt_fingerprint` values. What are the likely causes?

<details><summary>Answer</summary>Something in the exact text sent changed: the story text in the backlog, or an instruction or template file edited without bumping its version. The fingerprint records what was actually sent; versions record what was meant to be sent.</details>

6. US-412's reply is valid JSON that matches the output schema. Why did it fail, and what should you **not** do about it?

<details><summary>Answer</summary>It failed R2: test case TC-412-04 traces to AC4, which does not exist in US-412 (the agent invented a case-insensitive search rule). You should not hand-patch the output, and you should not add the invented rule to the requirement; raise it with the product owner as a question if it seems valuable.</details>

7. Why is `PASS` with status `needs_clarification` a success for US-310?

<details><summary>Answer</summary>Because the agent followed its instructions: it tested the clear ACs and asked about the vague one (AC4) instead of inventing a number for "fast". The questions go to the product owner.</details>



---

## Glossary

- **Execution run**: one pass of the agent over a defined set of requirements, producing recorded, checkable evidence.
- **Readiness checklist**: checks done on requirements before a run (IDs, testability, no secrets or personal data, approved tool, batch size, agent version).
- **Model client**: an object with a `complete(messages, settings)` method that returns the model's reply as text.
- **Protocol (`typing.Protocol`)**: a description of methods an object must have, used for type checking without inheritance.
- **Prompt fingerprint**: a short SHA-256 hash of the exact messages sent; identical prompts give identical fingerprints.
- **JSON Lines (`.jsonl`)**: a format with one JSON value per line, convenient for logs.
- **Traceability matrix**: a table linking each acceptance criterion to the test cases (or open questions) that cover it.

---

## Summary

- Executing an agent against requirements is a **process**, not a call: prepare → gate → build messages → call → validate → record → triage → review → into Project 2.
- Backlog exports become input-contract documents with `csv.DictReader` and `setdefault`; **converting** and **checking** are separate steps, and a short **readiness checklist** comes before any run.
- The agent talks to models through one small **`ModelClient`** interface. `ScriptedModel` keeps lessons offline; a real adapter only translates, gets secrets from **environment variables**, and passes **settings** that reduce, but do not remove, variation.
- `TestCaseDesigner` checks its parts agree **at start-up** and puts the **gate before the model**: 6 stories cost 5 calls.
- `run_requirements.py` records versions, settings, a **prompt fingerprint**, errors and warnings in a **JSON Lines** log, and saves the gated input and **raw reply** as evidence that `validate_output.py --run` can re-check independently.
- Every outcome gets an **action and an owner**: reject failures without hand-patching, send questions to the product owner, send passing output to human review, never let an agent quietly rewrite a requirement.
- A **traceability matrix** from passing outputs links ACs to test cases; stable IDs carry the link into Project 2.
- One run is one sample. Measuring and improving the agent across many runs comes next, in *Agent testing and refinement*.

---

## Additional Resources

- Python documentation, *Logging HOWTO* (official tutorial on log levels, loggers, handlers and logging to files; the next step after `print` in a runner): https://docs.python.org/3/howto/logging.html
- *JSON Lines* (the short specification for one-JSON-value-per-line files, as used for `run.jsonl`): https://jsonlines.org/
- Python documentation, *hashlib: Secure hashes and message digests* (reference for `sha256` and `hexdigest`, used for the prompt fingerprint): https://docs.python.org/3/library/hashlib.html
