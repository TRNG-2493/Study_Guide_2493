# Agent Architecture

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an **AI agent** is, and how it differs from a **single prompt**, a **chatbot** and an ordinary **script**.
- Name the parts of an agent's anatomy (**model, instructions, prompt templates, input contract, output contract, validation gate, tools, context/memory, orchestration runtime, logs**) and say what job each part does.
- Describe the agent loop **perceive → reason → act → check**, and trace one request through it.
- Compare three **levels of autonomy** (assistant, workflow/pipeline, autonomous agent) and explain why QA agents usually start **narrow and low-autonomy**.
- Apply the **single-responsibility** idea to agent design.
- Follow the data flow through our running example, the **TestCaseDesigner** agent, for story **US-205**, and point to the **failure points** at each boundary and the part that guards each one.
- Read a small Python **anatomy sketch** that shows the parts as separate pieces wired together.

---

## Why This Matters

From Monday to Wednesday you used AI as a **conversation partner**: you wrote a prompt, read the answer, corrected it and moved on. That works for one task on one day. It does not work when a team wants the same kind of help **every day, from every tester, with the same quality**. Imagine ten testers each asking an LLM to "write test cases for this story" with their own wording. You would get ten different formats, ten different levels of detail and no easy way to check any of them automatically.

An **agent** is how teams turn a good prompt into a **repeatable, checkable piece of software**. The prompt wording is written down once (instructions and templates). The shape of what goes in and what comes out is agreed in writing (contracts). A program checks every answer before anyone uses it (the validation gate). Every run leaves a trace (logs). Once those parts exist, the agent can be reviewed, versioned in Git, tested and improved like any other code.

That is the second half of this week's **Epic**: *design and build your first QA agent with IO contracts and validation scripts*. Today is the **design** half. You will take an agent apart and study each organ. Tomorrow you will build one.

It also feeds **Project 2 (Test Automation Framework)**. A framework that can call a test-design agent and then **reject malformed output automatically** is far more useful than a folder of copied-and-pasted chat answers. Today's pair-programming exercise asks you to design the instructions, schema and sample pairs for a requirements agent for the Project 2 e-commerce app, and this lesson gives you the map.

> **Scope note.** This lesson is the **map** for Thursday. It names every part of an agent and shows how they connect. The other six Thursday lessons each zoom into one part: *Agent instructions*, *Prompt templates*, *Input/output contracts*, *JSON Schema*, *Required fields and validation rules* and *Sample input/output pairs*. Building complete instructions, a reusable template library, implementing contracts in a running agent, writing validation scripts, and running and refining agents against real requirements are all covered on **Friday**. Retry strategies, prompt chains and multi-agent orchestration are covered in **Week 9**.

---

## The Concept

### 1. What Is an AI Agent?

Let us start with a working definition you can use all week:

> An **AI agent** is a program that uses a language model to carry out a **defined job**, by receiving an **input**, deciding what to do, **acting** (producing output or calling tools), and **checking** the result, according to **written instructions** and **agreed contracts**.

The important words are *program*, *defined job*, *instructions* and *contracts*. An agent is not a magic personality living inside the model. It is ordinary software that **wraps** a model. The model supplies language skill and reasoning; the surrounding code supplies structure, rules and safety.

A useful analogy is a **new employee in a QA team**:

| Employee | Agent part |
| --- | --- |
| The person's general skills and knowledge | The **model** (LLM) |
| Their job description and team rules | The **instructions** |
| Standard forms they fill in (e.g. a bug-report template) | The **prompt templates** |
| What their manager agrees to hand them, and in what form | The **input contract** |
| What they must hand back, and in what form | The **output contract** |
| A senior colleague who checks their work before it ships | The **validation gate** (and the human reviewer) |
| Access to the test-management tool, the browser, the database | The **tools** |
| Their notes and the ticket history they read | **Context / memory** |
| The team process that routes work to them | The **orchestration runtime** |
| The timesheet and the change history | The **logs** |

A talented new hire with no job description, no forms and no reviewer produces unpredictable work. The same is true for a model with no structure around it.

### 2. Agent vs Single Prompt vs Chatbot vs Script

These four things are easy to confuse, so let us separate them carefully.

**A single prompt** is one message you type into a chat window: "Write test cases for the coupon feature." You read the answer yourself. Nothing checks it, nothing records it, and next time you will probably word it differently.

**A chatbot** is a conversation interface around a model. It keeps the history of the chat, so you can say "now add negative tests" and it remembers the previous turn. It is still driven by a human, turn by turn, and its answers are free text for a human to read.

**A script** is ordinary deterministic code. `apply_coupon(50.00, "SAVE10")` returns `45.00` every single time. A script is perfectly predictable, but it cannot read a user story written in English and decide which tests are needed.

**An agent** combines the two worlds: the **language understanding** of a model with the **structure and checks** of a script.

| | Single prompt | Chatbot | Script | Agent |
| --- | --- | --- | --- | --- |
| Who starts each step? | Human | Human | Code | Code (often triggered by a human or a pipeline) |
| Understands natural language? | Yes | Yes | No | Yes |
| Wording fixed and versioned? | No | No | Yes | Yes (instructions + templates) |
| Output shape agreed in advance? | Rarely | Rarely | Yes (function signature) | Yes (output contract) |
| Output checked automatically? | No | No | Yes (tests) | Yes (validation gate) |
| Same input → same output? | No | No | Yes | Not guaranteed, but **checked** every time |
| Leaves an audit trail? | No | Partly (chat history) | If you add logging | Yes (logs) |

The last-but-one row is the key insight. A model is **not deterministic**: the same prompt can produce different answers (you saw this on Monday with temperature and sampling, and on Tuesday with common failure modes). An agent does not pretend otherwise. Instead, it **accepts variation in the wording but enforces the contract**: whatever the model writes, the result must have the agreed shape and pass the agreed rules, or it is rejected.

### 3. The Anatomy Map

Here are the ten parts we will study today. Think of this as the table of contents for the whole day.

1. **Model (LLM).** The engine that reads text and writes text. You learned how it works on Monday (tokens, next-token prediction, attention). The agent does not care much *which* model it uses, as long as the model can follow the instructions and produce the required format. Keeping the model swappable is a good design habit.

2. **Instructions (system prompt).** The agent's standing orders: its role, its goal, its rules, what it must never do, and how it must format output. They are the same for every run. On Tuesday you learned about the system message; agent instructions are a carefully designed, version-controlled system message. *Covered in depth in "Agent instructions".*

3. **Prompt templates.** The per-request message with **placeholders** such as `$story_id` and `$criteria`, filled in with the actual data at run time. Instructions say *who you are and how you work*; the template says *here is today's job*. *Covered in "Prompt templates".*

4. **Input contract.** A written agreement about what the agent accepts: which fields, which types, which are required. It protects the agent from garbage input. *Covered in "Input/output contracts".*

5. **Output contract.** A written agreement about what the agent returns. For our agents it is expressed as a **JSON Schema**, a machine-readable description of valid JSON. *Covered in "Input/output contracts" and "JSON Schema".*

6. **Validation gate.** Code that checks every output against the output contract (and extra rules the schema cannot express) **before** anything downstream uses it. If the check fails, the output is rejected, never silently passed on. *The rules are covered in "Required fields and validation rules"; building full validation scripts is Friday.*

7. **Tools.** Functions the agent is allowed to call, such as "read a story from the issue tracker", "look up the price table" or "run this pytest file". Modern model APIs support **tool use** (also called **function calling**): the model does not run the tool itself; it replies with a structured request like *"please call `get_story` with `story_id = US-205`"*, your code runs the function, and the result is sent back to the model. This is conceptually important because it is how agents **act** in the world. Our TestCaseDesigner v1.0.0 deliberately has **no tools**: the story is handed to it, and it only writes JSON. Fewer tools means fewer things that can go wrong.

8. **Context and memory.** Everything the model can "see" on a given call. **Context** is what is in the current request: instructions, template text, the story, perhaps a few examples (Tuesday's few-shot prompting). **Memory** is information kept *between* calls, for example earlier conversation turns, or a store of past decisions the agent can look up. The model itself remembers nothing between API calls; any memory is something your code deliberately saves and sends back. Our agent is **stateless**: every run starts fresh, which makes it far easier to test.

9. **Orchestration runtime.** The code that runs the loop: load the instructions, fill the template, call the model, parse the reply, validate it, decide what happens next, and record what happened. In real projects this may be your own Python, or an agent framework or SDK. Whatever the technology, the job is the same.

10. **Logs.** A record of each run: what went in, which version of the instructions and schema was used, what came out, whether it passed validation and how long it took. Logs make debugging possible ("why did Tuesday's run produce 14 test cases?") and support the accountability you studied on Wednesday ("who approved this, and based on what?").

Two more items sit *around* the agent rather than inside it:

- **Sample input/output pairs:** worked examples of correct behaviour, used to explain, review and later test the agent. *Covered in "Sample input/output pairs".*
- **The human reviewer:** the person who approves the agent's output for use, exactly as in Wednesday's *Human validation of AI output*.

### 4. The Agent Loop: Perceive → Reason → Act → Check

Most descriptions of agents use some version of a four-step loop. We will use these names:

1. **Perceive.** Take in the input and the context. *For TestCaseDesigner:* receive the US-205 story, check it against the input contract, and assemble the instructions plus the filled-in template.
2. **Reason.** The model works out what to do. *For TestCaseDesigner:* the model reads the acceptance criteria, notices the $50.00 threshold, and decides that a boundary test at $50.00 and $49.99 is needed.
3. **Act.** Produce output or call a tool. *For TestCaseDesigner:* write the JSON answer. (A tool-using agent might instead request "fetch story US-205" and loop back to Perceive with the result.)
4. **Check.** Verify the action before trusting it. *For TestCaseDesigner:* parse the JSON, validate it against the output schema, apply the extra rules R1 to R6 (explained below), and only then hand it on.

Notice the fourth step. Many popular explanations stop at "act". In quality engineering, **check** is non-negotiable. A tester would never ship a test case without reviewing it; an agent should never pass on output without checking it. If you remember one thing from this lesson, remember that **an agent without a check step is just an expensive way to produce unverified text.**

Some agents go around this loop many times (for example: call a tool, read the result, call another tool, then answer). Our first agent goes around it **once** per story. Looping strategies such as retries and chained prompts are Week 9 topics.

### 5. Levels of Autonomy

"Agent" is used loosely in the industry, so it helps to place systems on a scale of **autonomy**: how much the system decides for itself without a human or fixed code deciding for it.

**Level 1 - Assistant.** A human drives every step and reads every answer. Example: you paste US-205 into a chat and ask for test cases. This is what you did Monday to Wednesday.

**Level 2 - Workflow (pipeline).** Code drives a **fixed** sequence of steps, and the model is used inside some steps. The model does not choose what happens next; the code does. Example: *for each story in the sprint, fill the template, call the model, validate the JSON, write approved cases to a file for review.* The path is predictable even though the model's wording varies.

**Level 3 - Autonomous agent.** The model decides **which steps to take, in which order, and which tools to call**, until it judges the goal is met. Example: "Make the checkout test suite green" - the agent reads failures, opens files, edits code, re-runs tests and decides when to stop.

| | Assistant | Workflow / pipeline | Autonomous agent |
| --- | --- | --- | --- |
| Who chooses the next step? | Human | Fixed code | The model |
| Predictability | High (human controls it) | High | Lower |
| Easy to test? | Not automated | Yes | Hard |
| Risk if the model is wrong | Human catches it | Gate catches format errors; human reviews content | Errors can compound across many steps |
| Good first QA use | Exploring a story | Test-case drafting, requirement review | Rarely a good first choice |

Industry guidance from AI vendors makes the same point: start with the **simplest** design that works, and only add autonomy when the task truly needs it (see the Anthropic link in Additional Resources).

**Why QA agents start narrow and low-autonomy.** Recall the error-propagation idea from Wednesday's *AI within the QA lifecycle*: if each step is 90% reliable, five unchecked steps in a row are only about 59% reliable (0.9^5 ≈ 0.59). Quality engineering exists to **reduce** uncertainty, so a QA agent should:

- do **one** well-defined job,
- follow a **fixed** path (workflow level),
- produce **structured** output that code can check,
- leave the final decision to a **human**.

TestCaseDesigner is exactly that: a Level 2 component with one model call, no tools, a strict output contract and a human reviewer at the end. People sometimes call this an "agent" and sometimes a "workflow"; what matters is that you can describe its anatomy and its autonomy level precisely.

### 6. Single Responsibility: One Agent, One Job

In software design, the **single-responsibility principle** says a module should have **one reason to change**. It applies to agents too.

Compare two designs:

- **Design A, "QA SuperAgent":** reads requirements, finds ambiguities, writes test cases, generates test data, writes Playwright code and files defects.
- **Design B, a set of small agents:** *RequirementReviewer* (finds ambiguities), *TestCaseDesigner* (writes test cases), *TestDataDesigner* (writes data), each with its own instructions and contract.

Design A sounds impressive but is hard to work with:

- Its instructions become long and contradictory ("be creative with test ideas" vs "never invent requirements").
- Its output contract is huge, so it is hard to validate.
- When something goes wrong, you cannot tell which "job" failed.
- A change to defect-filing rules risks breaking test-case generation.

Design B gives each agent a **small contract** you can validate fully, **short instructions** that do not conflict, and **independent testing**. If you later want the agents to work together, the output contract of one can become the input contract of the next. Connecting agents that way is a Week 9 topic; today, just notice that **clear contracts are what make small agents composable**.

A quick test for single responsibility: can you describe the agent's job in **one sentence without the word "and"**? "TestCaseDesigner turns one user story into test cases" passes. "QA SuperAgent reviews requirements and writes tests and files bugs" fails.

### 7. The Running Example: TestCaseDesigner v1.0.0

All seven Thursday lessons use the same agent so that the pieces fit together.

> **TestCaseDesigner (v1.0.0)** - a QA agent that takes **one** user story with acceptance criteria and returns **test cases as JSON**.

Its input for today's example is story **US-205** from the Project 2 e-commerce app, which you met on Wednesday:

> **US-205 Apply coupon at checkout**
> - **AC1:** SAVE10 gives 10% off a subtotal of $50.00 or more.
> - **AC2:** Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
> - **AC3:** Unknown codes show "Coupon code not recognised".
> - **AC4:** Only one coupon per order.

As JSON, matching the agent's **input contract**, it looks like this:

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

And a correct output, matching the **output contract**, looks like this (excerpt: the first test case only):

```json
{
  "contract_version": "1.0.0",
  "story_id": "US-205",
  "status": "ok",
  "test_cases": [
    {"id": "TC-205-01", "title": "SAVE10 applied at exactly $50.00", "ac_ids": ["AC1"], "type": "boundary", "priority": "high",
     "preconditions": ["Cart subtotal is $50.00"], "steps": ["Enter coupon SAVE10", "Click Apply"], "expected_result": "Total is $45.00"}
  ],
  "open_questions": ["AC4: should a second coupon replace the first or be rejected?"]
}
```

Notice a few design choices you will study later today:

- `contract_version` tells any consumer which version of the contract this output follows.
- `status` lets the agent say "I could not do this properly" (`needs_clarification`) instead of guessing.
- `ac_ids` links each test back to the acceptance criteria: the **traceability** you practised on Wednesday, now built into the format.
- `open_questions` gives the agent an honest place to put ambiguity (AC4 does not say what happens when a second coupon is entered) rather than inventing a rule.

Beyond the schema, the agent's contract has six **semantic rules** that a JSON Schema alone cannot express. You will study them in *Required fields and validation rules*; here is the list so you can recognise them:

- **R1** output `story_id` equals input `story_id`
- **R2** every `ac_ids` entry exists in the input acceptance criteria
- **R3** every input AC is covered by at least one test case (or appears in `open_questions`)
- **R4** test case ids are unique and their 3-digit middle part matches the story number (US-205 → TC-205-NN)
- **R5** number of test cases ≤ `max_cases` (default 10)
- **R6** `status` "needs_clarification" requires a non-empty `open_questions`; `status` "ok" requires at least one test case

### 8. Data Flow Through the Agent

Here is one run of TestCaseDesigner on US-205, drawn as a text diagram. Read it top to bottom. Each box is a part; each arrow is a **boundary** where data passes from one part to the next.

```text
   [ Caller: tester, CI job or Project 2 framework ]
                       |
                       |  (A) story JSON for US-205
                       v
   +----------------------------------------------+
   | 1. INPUT CHECK   (input contract)            |  PERCEIVE
   |    is it a valid story?  no -> reject early  |
   +----------------------------------------------+
                       |  (B) trusted story data
                       v
   +----------------------------------------------+
   | 2. PROMPT ASSEMBLY                           |
   |    instructions.md  (same every run)         |
   |  + user template    (slots filled with data) |
   |  = messages [system, user]                   |
   +----------------------------------------------+
                       |  (C) messages
                       v
   +----------------------------------------------+
   | 3. MODEL CALL    (LLM)                       |  REASON + ACT
   +----------------------------------------------+
                       |  (D) raw text reply
                       v
   +----------------------------------------------+
   | 4. PARSE         text -> JSON object         |
   +----------------------------------------------+
                       |  (E) Python dict
                       v
   +----------------------------------------------+
   | 5. VALIDATION GATE                           |  CHECK
   |    JSON Schema (shape)  + rules R1-R6        |
   |    fail -> reject, do not pass on            |
   +----------------------------------------------+
                       |  (F) contract-valid output
                       v
   +----------------------------------------------+
   | 6. HUMAN REVIEW  (Wednesday's checklist)     |
   |    approve / correct / reject                |
   +----------------------------------------------+
                       |  (G) approved test cases
                       v
   [ Test suite, TestRail import, pytest parametrize ]

   LOGS: every box writes a line (versions, sizes, errors, timings)
```

Walk through it slowly:

- **(A) → 1.** The caller hands over the story. Before spending money on a model call, the agent checks the input against the input contract. A story with no acceptance criteria, or an id like `"coupon-story"`, is rejected immediately with a clear message.
- **1 → 2.** The trusted data is placed into the template. The instructions do not change; only the slots do.
- **2 → 3.** The messages go to the model. This is the only step that is **not deterministic**.
- **3 → 4.** The reply is **text**. Even when we asked for JSON, it might have a friendly sentence in front, a Markdown fence, or a missing bracket (Tuesday's *format locking*).
- **4 → 5.** The parsed object is checked against the schema (are all required fields present, with the right types and patterns?) and the semantic rules (does `TC-205-01` really trace to an AC that exists?).
- **5 → 6.** Only output that passed the gate reaches a human. The gate catches **form** problems; the human catches **meaning** problems, such as a wrong expected total.
- **6 → (G).** Approved cases enter the suite.

### 9. Failure Points and Their Guards

Every arrow in the diagram is a place where things can go wrong. A good architecture puts a **guard** at each one. This table is one of the most useful things to take away from today.

| Boundary | What can go wrong (example on US-205) | Part that guards it |
| --- | --- | --- |
| (A) input arrives | Missing `acceptance_criteria`; id `"205"` instead of `"US-205"`; `max_cases` of 500 | **Input contract** + input check |
| (B)→(C) prompt assembly | A placeholder left unfilled (`$criteria` sent literally); wrong story inserted | **Prompt template** (strict substitution) + logs |
| (C) instructions | Vague or conflicting rules, so the model invents a "max one use per customer" rule | **Instructions** (clear rules, "never invent requirements") |
| (D) model reply | Prose instead of JSON; JSON wrapped in a code fence; truncated reply | **Instructions** (format rules) + **parse** step |
| (E) parsed object | `status: "done"` (not an allowed value); id `TC-1`; missing `expected_result` | **Output contract** (JSON Schema) in the **validation gate** |
| (E) semantic | Test cites `AC7` (does not exist); AC4 silently ignored; 14 cases when `max_cases` is 6 | **Validation rules R1-R6** in the validation gate |
| (F) meaning | Expected total `$44.00` instead of `$45.00`; boundary at $51 instead of $50 | **Human review** (Wednesday) |
| Whole run | "Why did yesterday's output differ?" | **Logs** with instruction/schema versions |
| Over time | Someone edits the instructions and quality drops | **Sample input/output pairs** used as reference examples, and (Friday) agent testing |

Two lessons hide in this table.

First, **no single part catches everything**. The schema cannot know that $44.00 is the wrong total; a human reviewer should not waste time spotting that `TC-1` breaks the id format. Layers work together, just like unit, integration and end-to-end tests in a test pyramid.

Second, **cheap checks go first**. Input validation costs nothing and avoids a wasted model call. Schema validation takes milliseconds. Human review is the most expensive check, so it should only see output that has already passed the automated ones.

### 10. Where the Human Stays in the Loop

On Wednesday you learned that **the AI is never accountable; the person who approves is**. Agent architecture does not change that; it **moves** the human to the place where human judgement is most valuable.

| Activity | Done by |
| --- | --- |
| Writing and approving the instructions, templates and contracts | Human (designer, reviewed like code) |
| Checking input format, output format and rules R1-R6 | Code (the gate) |
| Writing the test-case drafts | Model |
| Judging whether the drafts are **correct, complete and grounded** | Human (Wednesday's checklist) |
| Deciding what enters the suite | Human (sign-off) |
| Investigating failures using logs | Human |

A good mental model: **the gate protects the human's time, and the human protects the product.** The agent does the repetitive drafting, code rejects anything malformed, and the tester spends their attention on whether the tests are right.

### 11. An Anatomy Inventory for a Repository

Because an agent is software, its parts live as **files in a repository**, reviewed through pull requests and versioned with Git, just like the prompts you versioned on Tuesday. A typical layout for our agent might be:

```text
agents/
  test_case_designer/
    instructions.md            # standing orders (system prompt)
    templates/
      user_prompt.txt          # per-request template with placeholders
    schemas/
      tcd_input.schema.json    # input contract
      tcd_output.schema.json   # output contract
    rules.md                   # semantic rules R1-R6 in plain English
    samples/
      us205_input.json         # sample input
      us205_output.json        # matching expected output
    runtime.py                 # orchestration (built on Friday)
    CHANGELOG.md               # what changed in each version
logs/
  test_case_designer/          # one record per run
```

The **anatomy inventory** below describes every part: what it is, where it lives, who owns it, and where today you study it in depth.

| Part | What it does | Typical file(s) | Usual owner | Studied in |
| --- | --- | --- | --- | --- |
| Model | Reads and writes text | Config value (model name, temperature) | Platform / team lead | Monday lessons |
| Instructions | Role, goal, rules, boundaries, output rules | `instructions.md` | QA engineer who designs the agent | *Agent instructions* |
| Prompt template | Per-request message with placeholders | `templates/user_prompt.txt` | Agent designer | *Prompt templates* |
| Input contract | What the agent accepts | `schemas/tcd_input.schema.json` | Agent designer, agreed with callers | *Input/output contracts*, *JSON Schema* |
| Output contract | What the agent returns | `schemas/tcd_output.schema.json` | Agent designer, agreed with consumers | *Input/output contracts*, *JSON Schema* |
| Validation rules | Extra checks beyond the schema (R1-R6) | `rules.md` (code on Friday) | Agent designer + QA lead | *Required fields and validation rules* |
| Validation gate | Applies schema + rules to every output | Code in the runtime (Friday) | Agent developer | Named today; built Friday |
| Sample pairs | Worked examples of correct behaviour | `samples/*.json` | Agent designer + domain expert | *Sample input/output pairs* |
| Tools | Functions the agent may call | Tool definitions (none in v1.0.0) | Agent developer | Concept only, this lesson |
| Context / memory | What the model sees; what is kept between runs | Built in the runtime (stateless in v1.0.0) | Agent developer | Concept only, this lesson |
| Orchestration runtime | Runs the loop | `runtime.py` | Agent developer | Friday |
| Logs | Record of each run | `logs/...` | Agent developer; read by everyone | This lesson; used Friday |
| Human reviewer | Approves output for use | Review records / correction log | Named tester | Wednesday lessons |

On your team the same person may own several rows. What matters is that **every row has an owner**, because a part nobody owns is a part nobody fixes.

### 12. An Anatomy Sketch in Python

To make the map concrete, here is a short Python program in which each part is a **separate, named piece**. Read it as an **anatomy sketch**: a labelled diagram you can run, not the finished agent. On Friday you will build the real one, with proper instructions, reusable templates, an input check, all six rules and a validation script.

It uses:

- `string.Template` from the standard library for the prompt template (`$name` placeholders; more on this in *Prompt templates*).
- A deterministic `fake_llm` stand-in, as on Monday to Wednesday, so the example runs offline and gives the same output every time. Its reply is **illustrative**.
- The `jsonschema` package to check the output against the output schema. Install it with `pip install "jsonschema>=4.18"`. (Some machines still have the old version 3.2, which does **not** support the Draft 2020-12 schemas we use this week; check with `pip show jsonschema`.)

Save the full TestCaseDesigner output schema (shown in full in the *JSON Schema* lesson) as `tcd_output.schema.json` in the same folder as the script.

```python
# anatomy_sketch.py - an ANATOMY SKETCH of the TestCaseDesigner agent.
# Every part of the agent is a separate, named piece so you can see it.
# This is not the finished agent: you build that on Friday.
import json
from string import Template
from jsonschema import Draft202012Validator

# ---- Part 1: INSTRUCTIONS (the agent's standing orders) ------------------
INSTRUCTIONS = (
    "You are TestCaseDesigner, a QA agent. You receive ONE user story with "
    "acceptance criteria and return test cases as JSON that matches the "
    "TestCaseDesigner output contract v1.0.0. Never invent requirements; "
    "put anything unclear in open_questions. Return JSON only."
)

# ---- Part 2: PROMPT TEMPLATE (fixed wording + slots for the variable data) -
USER_TEMPLATE = Template(
    "Design at most $max_cases test cases for story $story_id: $title\n"
    "Acceptance criteria:\n$criteria"
)

# ---- Part 3: OUTPUT CONTRACT (a JSON Schema loaded from a file) ------------
with open("tcd_output.schema.json", encoding="utf-8") as f:
    OUTPUT_SCHEMA = json.load(f)

# ---- Part 4: MODEL (a deterministic stand-in; no network, no account) ------
def fake_llm(messages: list[dict]) -> str:
    """Stand-in for an LLM call. Returns a canned, ILLUSTRATIVE answer."""
    return json.dumps({
        "contract_version": "1.0.0",
        "story_id": "US-205",
        "status": "ok",
        "test_cases": [
            {"id": "TC-205-01", "title": "SAVE10 applied at exactly $50.00",
             "ac_ids": ["AC1"], "type": "boundary", "priority": "high",
             "steps": ["Enter coupon SAVE10", "Click Apply"],
             "expected_result": "Total is $45.00"}
        ],
        "open_questions": ["AC4: should a second coupon replace the first or be rejected?"]
    })

# ---- Part 5: ORCHESTRATION (the runtime that wires the parts together) -----
def run_agent(story: dict, log: list[str]) -> dict:
    criteria = "\n".join(f"- {ac['id']}: {ac['text']}" for ac in story["acceptance_criteria"])
    user_prompt = USER_TEMPLATE.substitute(
        max_cases=story.get("max_cases", 10), story_id=story["story_id"],
        title=story["title"], criteria=criteria)
    messages = [{"role": "system", "content": INSTRUCTIONS},
                {"role": "user", "content": user_prompt}]
    log.append(f"prompt built ({len(user_prompt)} chars)")

    raw = fake_llm(messages)                      # act: call the model
    log.append(f"model replied ({len(raw)} chars)")

    output = json.loads(raw)                      # parse text -> Python dict
    # ---- Part 6: VALIDATION GATE (check before anyone uses the output) -----
    errors = [e.message for e in Draft202012Validator(OUTPUT_SCHEMA).iter_errors(output)]
    log.append(f"schema errors: {len(errors)}")
    if errors:
        raise ValueError(f"Output broke the contract: {errors}")
    return output

if __name__ == "__main__":
    us205 = {
        "story_id": "US-205", "title": "Apply coupon at checkout", "max_cases": 6,
        "acceptance_criteria": [
            {"id": "AC1", "text": "SAVE10 gives 10% off a subtotal of $50.00 or more."},
            {"id": "AC2", "text": "Subtotals under $50.00 are unchanged and show \"Spend $50.00 to use SAVE10\"."},
            {"id": "AC3", "text": "Unknown codes show \"Coupon code not recognised\"."},
            {"id": "AC4", "text": "Only one coupon per order."}]}
    # ---- Part 7: LOGS (a record of what happened, for debugging and audit) -
    run_log: list[str] = []
    result = run_agent(us205, run_log)
    for line in run_log:
        print("LOG:", line)
    print("status:", result["status"], "| test cases:", len(result["test_cases"]))
    print("first case:", result["test_cases"][0]["id"], "-", result["test_cases"][0]["title"])
    print("open questions:", result["open_questions"])
```

Running `python anatomy_sketch.py` prints:

```text
LOG: prompt built (322 chars)
LOG: model replied (380 chars)
LOG: schema errors: 0
status: ok | test cases: 1
first case: TC-205-01 - SAVE10 applied at exactly $50.00
open questions: ['AC4: should a second coupon replace the first or be rejected?']
```

**Reading the code part by part:**

- **`INSTRUCTIONS`** is a plain string that never changes between runs. In a real agent it lives in `instructions.md` and is much longer and carefully structured (next lesson).
- **`USER_TEMPLATE`** is a `string.Template`. The `$max_cases`, `$story_id`, `$title` and `$criteria` placeholders are filled by `.substitute(...)`. If any placeholder is missing, `substitute` raises a `KeyError` rather than sending a half-filled prompt: a small but real **guard** at boundary (B)→(C).
- **`OUTPUT_SCHEMA`** is loaded from a JSON file, not written inside the code. Keeping contracts in their own files means testers, developers and other agents can all read the same agreement.
- **`fake_llm`** receives the `messages` list in the same role/content shape you saw on Tuesday (`system`, `user`) and returns a **string**. Real model APIs also return text, which is why the next step parses it.
- **`run_agent`** is the **orchestration**. Follow it line by line and you will see the loop: build the prompt (perceive), call the model (reason + act), parse, then validate (check).
- **`Draft202012Validator(OUTPUT_SCHEMA).iter_errors(output)`** checks the output against the schema and yields one error for each problem. We collect the messages into a list. An empty list means the output has the agreed shape. You will learn the schema keywords in *JSON Schema*.
- **`raise ValueError(...)`** is the gate's "reject": broken output **stops** here instead of flowing into the test suite.
- **`run_log`** collects one line per step. Real logs would also record timestamps and the versions of the instructions and schema.

Notice what the sketch **does not** do yet: it does not check the **input** against the input contract, it does not apply rules R1-R6, it does not handle a reply that is not valid JSON, and its logs are not saved anywhere. Each of those gaps maps to a row in the failure-point table in Section 9, and each is filled in on Friday.

**Seeing the gate reject output.** To see why the gate matters, feed the schema a reply that looks reasonable but breaks the contract (illustrative):

```python
import json
from jsonschema import Draft202012Validator
schema = json.load(open("tcd_output.schema.json", encoding="utf-8"))
# An ILLUSTRATIVE bad reply: plausible-looking, but it breaks the contract.
bad_reply = {
    "contract_version": "1.0.0", "story_id": "US-205", "status": "done",
    "test_cases": [{"id": "TC-1", "title": "Coupon works", "ac_ids": ["AC1"],
                    "type": "positive", "priority": "high",
                    "steps": ["Apply SAVE10"], "expected_result": "Discount applied"}],
    "open_questions": []}
for err in Draft202012Validator(schema).iter_errors(bad_reply):
    print("-", err.message)
```

Output:

```text
- 'done' is not one of ['ok', 'needs_clarification']
- 'TC-1' does not match '^TC-[0-9]{3}-[0-9]{2}$'
```

A human skimming this reply might not notice either problem: "done" sounds fine and "TC-1" looks like a test id. But a downstream program that branches on `status == "ok"`, or a TestRail import that expects `TC-205-01`-style ids, would break. The schema catches both in milliseconds.

Notice too what it does **not** catch: `"expected_result": "Discount applied"` is vague (applied how much?). The schema only knows it is a string of at least five characters. Judging whether an expected result is **specific and correct** is still the human reviewer's job from Wednesday.

### 13. Design Questions to Ask About Any Agent

When you meet an agent, in today's demo, in your pair exercise, or at work, use these questions to "dissect" it. They are the questions behind today's instructor demo.

1. **Job:** Can its job be stated in one sentence without "and"?
2. **Autonomy:** Is it an assistant, a workflow or an autonomous agent? Is that level justified?
3. **Instructions:** Where are they stored? Are they versioned? Do they say what to do when the input is unclear?
4. **Templates:** Which parts of the prompt change per request, and how are they filled?
5. **Input contract:** What does it accept? What happens to bad input?
6. **Output contract:** Is the output machine-checkable? Is there a version number? Is there a way to say "I can't"?
7. **Validation:** What is checked automatically? What rules does the schema not cover?
8. **Tools:** Which tools can it call, and could any of them change something (write, delete, send)?
9. **Context and memory:** What does the model see on each call? Is anything kept between runs?
10. **Logs:** Could you explain any given run a week later?
11. **Human:** Who approves the output, and where is that recorded?
12. **Examples:** Are there sample input/output pairs that show correct behaviour?

If you cannot answer one of these for an agent, you have found a design gap.

---

## Practice Exercises

1. **Classify the system.** For each of the following, say whether it is a single prompt, a chatbot, a script, an assistant-level use of AI, a workflow, or an autonomous agent, and justify your answer in one sentence:
   a) A pytest file that checks `apply_coupon`.
   b) A CI job that, for every new story in the sprint, fills a template, calls a model, validates the JSON and writes the drafts to a review folder.
   c) A tester chatting with a model to explore edge cases for US-310.
   d) A system that reads failing test output, decides which files to edit, edits them and re-runs the tests until they pass.

2. **Draw the data flow.** Draw (on paper or as text) the data flow for a hypothetical **RequirementReviewer** agent that takes US-310 (shipping address) and returns a list of ambiguities. Label the boundaries (A) to (G) as in Section 8. Which acceptance criterion of US-310 would you expect it to flag, and in which output field should that appear?

3. **Fill the guard table.** For RequirementReviewer, write three rows of a failure-point table (boundary, what can go wrong, which part guards it). At least one row must describe a problem that only a human can catch.

4. **Split the SuperAgent.** A colleague proposes one agent that "reviews requirements, writes test cases, generates test data and writes Playwright scripts". Propose a set of single-responsibility agents instead. For each, write its one-sentence job and name its input and its output.

5. **Break the sketch (run it).** Run `anatomy_sketch.py`. Then change `fake_llm` so that `"priority"` is `"urgent"` and run it again. What happens, and which part of the anatomy stopped the bad output? Next, delete the `title=` argument from the `.substitute(...)` call. What error do you get, and at which boundary did it occur?

---

## Knowledge Check

1. In one sentence, what is the difference between a chatbot and an agent?

<details><summary>Answer</summary>

A chatbot is a conversation interface driven by a human turn by turn with free-text answers, while an agent is a program that wraps a model with fixed instructions, agreed input/output contracts, an automatic check step and logs so it can do a defined job repeatably.

</details>

2. Name the four steps of the agent loop used in this lesson, and say which step is most often forgotten.

<details><summary>Answer</summary>

Perceive, reason, act, check. The **check** step is most often forgotten, and in QA it is non-negotiable.

</details>

3. Why do QA agents usually start at the workflow (pipeline) level of autonomy rather than as autonomous agents?

<details><summary>Answer</summary>

Because fixed paths are predictable and testable, errors compound across unchecked steps (for example 0.9^5 ≈ 0.59), and QA work aims to reduce uncertainty. A narrow workflow agent with structured, checkable output and a human approver is safer and easier to validate.

</details>

4. TestCaseDesigner returns `"status": "done"`. Which part of the anatomy should catch this, and how?

<details><summary>Answer</summary>

The **validation gate**, using the **output contract** (JSON Schema). The schema lists `status` as an `enum` of `ok` or `needs_clarification`, so `done` produces a validation error and the output is rejected.

</details>

5. The agent returns valid JSON with `"expected_result": "Total is $44.00"` for a $50.00 subtotal with SAVE10. Will the schema catch it? Who will?

<details><summary>Answer</summary>

No. The schema only checks shape (it is a string of at least 5 characters). The **human reviewer** must catch it by deriving the expected total ($45.00) from AC1, as practised on Wednesday.

</details>

6. Why does TestCaseDesigner v1.0.0 have no tools?

<details><summary>Answer</summary>

Its job (turn a story that is handed to it into test-case JSON) does not need any. Every tool adds a way for things to go wrong, so a narrow, single-responsibility agent should only get the tools its job requires.

</details>

7. What does the "single-responsibility" quick test say, and does "TestCaseDesigner turns one user story into test cases" pass it?

<details><summary>Answer</summary>

Describe the agent's job in one sentence without the word "and". Yes, it passes.

</details>

8. In the anatomy sketch, what happens if a placeholder in `USER_TEMPLATE` is not supplied to `substitute`, and why is that useful?

<details><summary>Answer</summary>

`substitute` raises a `KeyError`. That is useful because it stops a half-filled prompt (with a literal `$title`, for example) from being sent to the model; it is a guard at the prompt-assembly boundary.

</details>

---

## Glossary

- **AI agent:** A program that uses a language model to carry out a defined job, following written instructions and agreed contracts, and checking its results.
- **Agent loop:** The cycle perceive → reason → act → check.
- **Autonomy level:** How much the system chooses its own next steps: assistant (human decides), workflow (code decides), autonomous agent (model decides).
- **Workflow / pipeline:** A fixed sequence of steps defined in code, with a model used inside some steps.
- **Instructions (system prompt):** The agent's standing orders, the same on every run.
- **Prompt template:** A per-request message with placeholders filled at run time.
- **Input contract / output contract:** Written agreements on what the agent accepts and returns.
- **JSON Schema:** A machine-readable description of what valid JSON looks like.
- **Validation gate:** The step that checks output against the contract and rules, and rejects anything that fails.
- **Tool use / function calling:** A model's ability to request that the surrounding code run a named function with given arguments; the code runs it and returns the result.
- **Context:** Everything the model sees on one call.
- **Memory:** Information the surrounding code deliberately keeps between calls and sends back to the model.
- **Stateless agent:** An agent that keeps no memory between runs; each run starts fresh.
- **Orchestration runtime:** The code that runs the agent loop and connects the parts.
- **Single-responsibility principle:** Each agent should have one job and one reason to change.
- **Semantic rule:** A rule about meaning or relationships (for example "every `ac_ids` entry exists in the input") that a JSON Schema cannot express on its own.

---

## Summary

- An **agent** is ordinary software that wraps a model with **instructions, templates, contracts, a validation gate, (optional) tools, context/memory, an orchestration runtime and logs**. The model gives language skill; the structure gives repeatability and safety.
- Unlike a single prompt or a chatbot, an agent's wording is **fixed and versioned**, its input and output are **agreed in advance**, and every output is **checked automatically**.
- The agent loop is **perceive → reason → act → check**. In QA, the check step is never optional.
- Place agents on an **autonomy scale**. QA agents usually start as narrow **workflow-level** components with one job, structured output and a human approver.
- Keep agents **single-responsibility**: small contracts are easy to validate and agents with clear contracts can later be combined.
- Every boundary in the data flow has a **failure point** and a **guard**. Cheap automated checks go first; the human reviewer focuses on meaning.
- Our running example, **TestCaseDesigner v1.0.0**, turns US-205 into test-case JSON governed by an input contract, an output contract and rules **R1-R6**. The rest of today zooms into each part; on **Friday** you build it.

---

## Additional Resources

- Anthropic, *Building effective agents* (the difference between workflows and agents, and why to start with the simplest design that works): https://www.anthropic.com/research/building-effective-agents
- Claude Platform Docs, *Tool use with Claude* (how tool use / function calling works: the model requests a tool, your code runs it and returns the result): https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- Google Cloud, *What are AI agents?* (a vendor-neutral overview of agent components such as model, tools, memory and reasoning): https://cloud.google.com/discover/what-are-ai-agents
