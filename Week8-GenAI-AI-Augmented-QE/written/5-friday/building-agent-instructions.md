# Building Agent Instructions

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the difference between **reading** a finished instruction set (Thursday) and **building** one from a blank page (today), and why building is an engineering process, not a writing exercise.
- Pitch instructions at the **right altitude**: concrete enough to steer the model, general enough to handle stories you have not seen yet.
- Follow a repeatable **seven-step method**: job card, raw material, section-by-section drafting, testable rules, desk-check, review, version and pin.
- Write a **job card** for an agent: one job, its consumer, its inputs, its outputs and its "done" criteria.
- Improve a first-draft instruction by making it **concrete, grounded, reasoned and checkable**, using three worked rewrites.
- Build a **rule-to-check traceability map** that links every instruction rule to the schema rule, code rule (R1-R6), quality rule (Q1-Q3) or human review that verifies it.
- **Desk-check** a draft by walking the sample pairs P01-P05 through it by hand, and record the gaps you find.
- Load instructions safely in Python with `tcd/instructions.py`, and keep the rule map honest with a small script, `check_rule_map.py`.

---

## Why This Matters

On Thursday you took a QA agent apart. You read the nine sections of the **TestCaseDesigner v1.0.0** instructions, saw why each line was there, critiqued a weak version line by line and checked an instruction file with `check_instructions.py`. All of that was **reading** someone else's finished work.

Today you build. Reading a good instruction set and writing one are different skills, in the same way that reviewing a test plan and writing one are different skills. When you start from a blank page, nobody tells you which rules matter, which order to write them in, or how you will know the result works. Most first drafts fail in the same ways: they are vague ("write good tests"), they contradict each other, they forget unusual inputs, or they contain rules that nobody ever checks.

So today we treat instruction writing as **engineering**: start from a **requirement** (a job card), collect **evidence** instead of guessing, make every rule **testable** and record which check verifies it, **desk-check** the draft before any model sees it, then **version** and **pin** the result.

This is the first step of today's part of the **Weekly Epic**: "design and build their first QA agent with IO contracts and validation scripts". The instructions you finish here are the file the agent loads in every later lesson today. It also feeds **Project 2 (Test Automation Framework)**: an agent that designs test cases for the e-commerce app (login, search, cart, checkout) is only useful in your framework if its behaviour is written down, reviewed and versioned like the rest of your code. In today's exercise you will use the same method on the requirements agent your pair designed on Thursday.

> **Scope note.** This lesson covers **writing** the instruction file and **loading** it safely. The user-message template library is the next lesson (*Creating reusable prompt templates*). Turning the contract into code is *Implementing IO contracts*, and the R1-R6 code checks are built in *Agent output validation*. Measuring how well the instructions work, and improving them to a v1.1.0, happens later today in *Agent testing and refinement*. Retrying a model after a bad answer is covered in **Week 9**; prompt injection is covered in **Week 10**.

---

## The Concept

### 1. From Reading Instructions to Building Them

A quick reminder of what instructions are: the agent's **standing orders**, sent as the **system message** on every call. They say who the agent is, what its one job is, how to do it, what the reply must look like and what to do when unsure. Thursday's nine sections (Role and Goal, Scope, Inputs, Process, Rules, Output, Uncertainty and Escalation, Boundaries, Style) give the file its shape.

Knowing the shape is not enough to fill it. Think of an architect: knowing that a house has walls and a roof does not tell you how big the rooms are. The architect starts from the needs of the people who will live there, designs against the building code, and checks the design before building. For an agent, the people are the **consumers** of its output, the building code is the **IO contract**, and the storm-test is **unusual input** (vague ACs, `max_cases` of 1, release notes instead of a story).

The seven-step method in Section 3 turns those needs into a file. You will apply it to TestCaseDesigner, so you can compare your result with the v1.0.0 file you studied on Thursday (`instructions/tcd_instructions_v1.0.0.md`, which we will not reprint here).

### 2. Right Altitude: Not a Script, Not a Wish

Anthropic's engineering article on context engineering (see Additional Resources) describes the **right altitude** for a system prompt as a middle zone between two failure modes:

1. **Too low (brittle script).** Case-by-case if-else logic ("If the AC mentions coupons, write 3 tests..."). It breaks when a new kind of story arrives and grows into contradictory rules.
2. **Too high (vague wish).** "Write thorough, high-quality test cases." No concrete signal, so the model's idea of "thorough" changes run to run: Wednesday's **weak words**.

The right altitude is a set of **general principles, each made concrete with an example or a measurable test**:

| Altitude | Example sentence | Problem |
|---|---|---|
| Too low | "For US-205, test $50.00 and $49.99." | Only works for one story |
| Too high | "Test the boundaries well." | "Well" cannot be checked |
| Right | "For every numeric threshold, write one test at the threshold and one just below it (for example $50.00 and $49.99)." | General rule, concrete example, checkable |

The same article recommends **minimal but sufficient** instructions: the smallest set of information that fully describes the expected behaviour. Minimal does not mean short. It means every sentence earns its place, usually because it prevents a failure you have actually seen or can name. A useful habit: next to every rule, you should be able to say **which failure it prevents**. If you cannot, the rule is a candidate for deletion.

Other vendors' guides (for example the OpenAI GPT-4.1 prompting guide in Additional Resources) recommend a very similar sectioned structure: role, instructions, reasoning steps, output format, examples, context.

### 3. The Seven-Step Method at a Glance

| Step | What you do | What you produce |
|---|---|---|
| 1. Job card | Write down the one job, the consumer, inputs, outputs, done-criteria | A half-page job card |
| 2. Raw material | Collect contract fields, pair expectations, known failure habits | A list of behaviours the agent must and must not show |
| 3. Draft | Write the sections in a deliberate order | A first draft of the nine sections |
| 4. Testable rules | Rewrite each rule so it can be checked; map it to a check | A rule-to-check map |
| 5. Desk-check | Walk P01-P05 through the draft by hand | A findings list |
| 6. Review | A second person applies Thursday's checklist | Review comments, fixes |
| 7. Version and pin | Add the header, commit, point `agent.json` at the file | `tcd_instructions_v1.0.0.md` pinned in `agent.json` |

This mirrors the testing process you know: requirement, test basis, design, traceability, static review, baseline. Instructions **are** a requirement for the agent's behaviour, so you build them like one.

### 4. Step 1: Write the Job Card

A **job card** is a short description of the agent's job, written **before** any instruction text. It is for humans, not for the model. Its purpose is to stop scope creep and to give every later decision a reference point ("does this rule serve the job?").

A job card answers five questions. Here is the job card for TestCaseDesigner:

```text
JOB CARD: TestCaseDesigner

One job:      Turn ONE user story with acceptance criteria into functional
              test cases that a tester can review and automate.
Consumer:     A QA engineer who reviews the cases, then a script that
              loads approved cases into the Project 2 pytest suite.
Inputs:       One JSON object following input contract 1.0.0
              (story_id, title, acceptance_criteria, optional techniques
              and max_cases).
Outputs:      One JSON object following output contract 1.0.0
              (contract_version, story_id, status, test_cases, open_questions).
Done when:    - every AC is covered by a test case or named in an open question
              - every test case traces to real AC IDs
              - expected results are concrete (exact totals and messages)
              - the reply validates against the output schema
Not this job: performance, security or accessibility testing; writing
              automation code; rewriting requirements.
```

Each line becomes something concrete later: **One job** becomes Role and Goal; **Not this job** becomes Scope; **Inputs** and **Outputs** point at the contract (the instructions refer to it rather than re-describing it); **Consumer** tells you what "good" means (a pytest loader needs exact expected results and stable IDs; a reviewer needs `ac_ids` for traceability); and **Done when** becomes Process and Rules. Look closely at "Done when": its four lines are almost exactly R3, R2, Q2 and S1 from Thursday's rule catalogue. The job card and the catalogue describe the same "done" from two sides.

> **Tip.** If you cannot write "One job" in one sentence, you probably have two agents. Thursday's *single responsibility* idea applies here: split the job before you write any instructions.

### 5. Step 2: Gather the Raw Material

Do not write instructions from imagination. Collect evidence first. For TestCaseDesigner there are four sources.

**Source A: the IO contract (Thursday).** Every required output field (`contract_version`, `story_id`, `status`, each test case's `id`, `ac_ids`, `type`, `priority`, `steps`, `expected_result`, and `open_questions`) needs a sentence somewhere that tells the model how to fill it. Input defaults also come from the contract: `max_cases` defaults to 10, and missing `techniques` means EP and BVA.

**Source B: the sample pairs P01-P05 (Thursday).** Each pair's MUST and MUST NOT lists are behaviour you promised. For example P01 says "a boundary case at subtotal $50.00" and "MUST NOT invent rules not in the story"; P03 says "at least one open question that names AC4"; P05 says the agent must recognise release notes as out of scope.

**Source C: the correction log (Wednesday).** Reviewers kept fixing the same things: invented values, paraphrased messages, vague results such as "works correctly", missing boundaries. Each repeated correction is a rule waiting to be written.

**Source D: known model habits (Tuesday).** Markdown fences around JSON, a friendly sentence before it, ignored count limits, details copied from an example.

Now turn the evidence into a plain list of behaviours. This list is your raw material:

```text
MUST
  M1  reply with one JSON object, nothing else              (Source A, D)
  M2  copy story_id; contract_version "1.0.0"                (A)
  M3  test at and just below every numeric threshold         (B: P01; C)
  M4  copy messages exactly                                  (B: P01; C)
  M5  cover every AC with a case or an open question         (A, B: P03)
  M6  respect max_cases, even when it is 1                   (B: P02; D)
  M7  use needs_clarification when nothing can be tested     (B: P05)
MUST NOT
  N1  invent rules, values, messages or screens              (B: P01; C)
  N2  test a vague AC as if it were clear                    (B: P03)
  N3  put real customer data or passwords in a test case     (Wednesday responsible use)
```

Every rule in the final file should trace back to an item on this list, and every item on the list should end up in the file. That two-way link is the same **bidirectional traceability** you used for requirements and tests on Wednesday.

### 6. Step 3: Draft Section by Section

You now have nine empty sections to fill. The **order in which you write them** matters more than you might expect. We recommend this order:

1. **Output** and **Inputs** first: the contract fixes them, so they are easiest to get exactly right, and everything else depends on them.
2. **Process**: the "how" of the job (M3, M5, M6).
3. **Rules**: non-negotiable constraints at every step (N1, M4, the ID pattern).
4. **Uncertainty and Escalation**: what to do when the Process cannot be followed (M7, N2).
5. **Boundaries**: out-of-scope requests and safety (N3).
6. **Scope**, **Style** and finally **Role and Goal**, which are easier to write once you know what the agent actually does. Writing the role last also avoids a grand opening ("You are a world-class QA expert...") that promises more than the file delivers.

The **file order** stays Thursday's order (Role and Goal first), because that is the order in which a reader, human or model, needs the information. Writing order and reading order do not have to be the same; a test plan is often written body-first and summary-last too.

Here is what the first drafted section looks like. The **Output** section comes almost directly from rows M1 and M2:

```markdown
## Output
- Reply with exactly one JSON object that follows the TestCaseDesigner output
  contract 1.0.0. No Markdown fences and no text before or after the JSON.
- Set contract_version to "1.0.0" and copy story_id from the input.
```

The section **names** the contract and its version instead of re-describing every field (duplicates drift apart), and it names the two most common format failures (fences, text around the JSON) because Source D says models really do this.

**Where does a sentence go: instructions or template?** Thursday's test still applies: if a sentence is true for **every** story the agent will ever handle, it belongs in the instructions (the system message). If it mentions **this** story or a per-call option, it belongs in the user-message template. "Number test cases TC-<story number>-<two digits>" is true for every story, so it is an instruction. "Return at most 6 test cases" depends on this call's `max_cases`, so it is template text. You will build the template library in the next lesson.

### 7. Three Rewrites: First Draft to Improved

First drafts are always weaker than they look. Here are three real-world style first drafts for TestCaseDesigner and how each one was improved. For each, notice **what kind** of improvement was made, because the same four kinds apply to any agent: **make it concrete, ground it, give the reason, make it checkable**.

#### Rewrite 1: the boundary step (make it concrete)

**First draft:**

```text
2. Use boundary value analysis where appropriate.
```

**Problems:** "where appropriate" is a weak word, so the model decides when BVA applies. "Boundary value analysis" is a technique name, not an action; models apply it inconsistently (sometimes testing $50.01 instead of $49.99, sometimes testing only the threshold).

**Improved (as in v1.0.0):**

```text
2. Apply the requested techniques. For every numeric threshold, write one test at
   the threshold and one just below it (for example $50.00 and $49.99).
```

**What changed:** "where appropriate" became a **trigger** the model can find ("for every numeric threshold"); the technique name became an **action** ("one test at the threshold and one just below it"); and an **example with real numbers** pins down "just below" for money as one cent, not $49.00. "Apply the requested techniques" ties the step to the `techniques` input, so it also works when a caller asks for decision tables.

#### Rewrite 2: the grounding rule (ground it and give the reason)

**First draft:**

```text
- Be accurate and do not hallucinate.
```

**Problems:** "be accurate" is a wish, not an instruction. "Do not hallucinate" names an outcome the model cannot observe in itself. Neither says what the model is allowed to use as a source.

**Improved (as in v1.0.0):**

```text
- Use only facts stated in the acceptance criteria. Do not invent rules, values,
  messages or screens. Reason: an invented expectation produces a test that fails
  on correct software.
```

**What changed:** the rule names the **only permitted source** (the acceptance criteria), which the model can act on; it lists the four **kinds** of invention seen in the correction log (rules such as coupon expiry dates, values, paraphrased messages, invented screens); and it gives a **reason** in testing terms: an invented expectation creates a **false failure** on correct software. Thursday explained why reasons help: a model that knows *why* a rule exists applies it more sensibly to cases the rule does not mention.

#### Rewrite 3: the escalation rule (make it checkable)

**First draft:**

```text
- If something is unclear, ask the user.
```

**Problems:** There is no "user" in a pipeline run; nobody will answer. "Something" is undefined. "Ask" does not say **where** the question goes, so it may appear as prose before the JSON (breaking M1) or not at all.

**Improved (as in v1.0.0):**

```text
- If a criterion is ambiguous, contradictory or untestable, do not guess. Add a
  question to open_questions that names the criterion ID.
- If no criterion can be tested, set status to "needs_clarification" and return
  an empty test_cases list. Otherwise set status to "ok".
```

**What changed:** "something" became three named conditions from Wednesday (**ambiguous, contradictory, untestable**); "ask the user" became a **contract field**, `open_questions`, so the question travels with the output to the reviewer; "names the criterion ID" makes the rule **checkable by code** (that is exactly how R3 works); and the `status` bullet gives a clear condition, which makes R6 checkable.

> **Pattern to remember.** For every rule ask four questions: *Can the model find the trigger in the input? Does the rule name a concrete action or source? Does it say why? Could a script or a reviewer tell whether it was followed?* If any answer is "no", rewrite.

### 8. Step 4: Make Every Rule Testable and Map It to a Check

A rule that nobody checks is a rule you only **hope** is followed. On Thursday you built a **rule catalogue**: S1 (output schema), S2 (input schema), R1-R6 (code rules), Q1-Q3 (quality rules), each assigned to a layer (schema, code or human). Now connect the two documents: for every instruction rule, record which catalogue rule verifies it. We call this the **rule-to-check map** (or traceability map).

Build it by hand first. Take each instruction bullet and ask: "If the model broke this rule, which check would notice?"

| Instruction rule (short) | Section | Verified by |
|---|---|---|
| Test at and just below every threshold | Process | Q1, human |
| Never return more than max_cases | Process | R5 |
| Use only facts stated in the ACs | Rules | R2, human |
| Copy messages exactly | Rules | human |
| ID pattern TC-<story number>-<NN> | Rules | S1, R4 |
| List the AC IDs a case checks | Rules | R2, R3 |
| One action per step | Rules | human |
| Exactly one JSON object | Output | S1 |
| Copy story_id | Output | S1, R1 |
| Do not guess; name the AC in a question | Uncertainty | R3, human |
| No testable AC → needs_clarification | Uncertainty | R6 |
| No real customer data | Boundaries | ? |

Look at the last row. When we first built this table, **no check verified the data-safety rule**. It is a perfectly good rule, but nothing would notice if it were broken. That is a **smell**: either add a check, or consciously assign it to human review and add it to the reviewer's checklist. We chose human review for v1.0.0 (an automated check for real-looking emails or card numbers is a sensible later improvement).

Two more lessons from the table. Rules checked only by **humans** must appear on the reviewer's checklist (Wednesday's C1-C9), otherwise "human" quietly means "nobody". And **writing the map changes the instructions**: R3 can only work if questions contain the literal AC ID, which is why Rewrite 3 insists on it.

Section 13 turns this table into a JSON file and a script, so the map cannot silently drift away from the instruction file.

### 9. Step 5: Desk-Check the Draft with the Sample Pairs

A **desk-check** is a manual walk-through: you play the part of the model, take each sample input, and for each decision the agent must make you point at **the line in the instructions** that tells it what to do. If you cannot point at a line, you have found a gap. It is the instruction equivalent of a code walkthrough, and it costs nothing: no model, no tokens.

Here is the desk-check of the v1.0.0 draft against P01-P05:

| Pair | Decision the agent must make | Line that decides it | Finding |
|---|---|---|---|
| P01 (US-205) | Which values to test for AC1/AC2 | Process 2 ($50.00 / $49.99) | Covered |
| P01 | What to do with AC4 ("one coupon per order") | Uncertainty bullet 1 | Covered: AC4 is ambiguous, so a question naming AC4 |
| P01 | Exact text of AC3's message | Rules: copy messages exactly | Covered |
| P02 (US-101, 1 AC, `max_cases` 1) | How many cases | Process 5: never more than max_cases | Covered |
| P02 | Which boundary to pick: 5th failure or 15-minute unlock? | none | **Gap, accepted**: the pair says either is allowed (MAY), so no rule is needed |
| P03 (US-310, AC4 vague) | Test AC4 or ask? | Uncertainty bullet 1 | Covered |
| P03 | Which `status`? | Uncertainty bullet 2: `needs_clarification` only if **no** criterion can be tested | **Conflict**: AC1-AC3 are testable, so the instructions say `ok`; the pair expects `needs_clarification` |
| P04 (malformed input) | Anything | none needed | Not the instructions' job: the input gate rejects P04 before the model is called |
| P05 (release notes) | Recognise out-of-scope input | Boundaries bullet 1 | Covered: `needs_clarification` with one open question |

Three kinds of finding came out, each handled differently:

1. **Accepted gap (P02).** Not every decision needs a rule. The pair's MAY list allows either boundary, so a rule would add length without improving the agent: "minimal but sufficient" in practice.
2. **Not the instructions' job (P04).** Malformed input never reaches the model; the input gate rejects it (implemented later today in *Implementing IO contracts*). A rule for it would duplicate the gate and waste tokens.
3. **Conflict (P03).** The valuable one. For a story where **some** ACs are testable and one is vague, the instructions say `ok` and the pair says `needs_clarification`. Neither document is automatically right; the team decides. Record it with an owner and do **not** silently edit either document during a desk-check. We keep v1.0.0 unchanged; measured changes, and the decision that closes F-02, come later today in *Agent testing and refinement*.

```text
DESK-CHECK FINDINGS – TestCaseDesigner instructions 1.0.0 (draft)
F-01  P02  Boundary choice for AC3 not specified.        Accepted: pair allows either (MAY).
F-02  P03  status rule (Uncertainty 2) says "ok" when any  Open: team decision needed;
           AC is testable; pair P03 expects                 owner QE lead; do not change
           "needs_clarification".                           v1.0.0 before measuring.
F-03  P04  Malformed input.                                 Not an instruction concern: input gate.
F-04  -    Boundaries data-safety rule has no check.        Assigned to human review checklist.
```

> **Why desk-check before running the model?** A capable model often does something sensible even when the instructions are silent, so a gap stays invisible until the day it does something different. A desk-check finds it while it is cheap to discuss.

### 10. Step 6: Review

The author of the instructions is the worst person to review them, for the same reason a developer is the worst person to test their own code: they read what they meant, not what they wrote. Ask a teammate to review the draft with Thursday's ten-point instruction review checklist, and run Thursday's `check_instructions.py` (sections present, weak words) as a quick first filter.

Give the reviewer three things along with the draft:

- the **job card** (so they can judge whether each rule serves the job),
- the **rule-to-check map** (so they can spot rules nobody verifies),
- the **desk-check findings** (so they do not re-discover known gaps, and can challenge the decisions).

Not every comment leads to a change. What matters is that every comment gets a **recorded decision** (changed, or kept with a reason).

### 11. Step 7: Version, Freeze and Pin

When review is done, three things turn the draft into a **release**:

1. **Header line.** The first lines after the title carry the version, the output contract version it was written for, and the owner:

   ```text
   Version: 1.0.0 | Output contract: 1.0.0 | Owner: QE team
   ```

   The version follows semantic versioning (Thursday). The contract version is a promise: "this text produces output for contract 1.0.0".

2. **Freeze.** Save the file with the version in its name, `instructions/tcd_instructions_v1.0.0.md`, and commit it. From now on, any change, even a typo fix, creates a new file and a new version with a changelog entry. Old versions stay in the folder so you can compare and roll back.

3. **Pin.** The agent never "finds" its instructions; it loads exactly the file named in its configuration. In our project that is `agent.json`:

   ```json
   {
     "agent": "TestCaseDesigner",
     "version": "1.0.0",
     "instructions": "instructions/tcd_instructions_v1.0.0.md",
     "template": {"name": "tcd_user", "version": "1.0.1"},
     "contract_version": "1.0.0",
     "model_settings": {"temperature": 0, "max_tokens": 2000}
   }
   ```

   `agent.json` pins **every** moving part (instructions, template, contract version, model settings), so a behaviour change always shows up as a reviewed change to this file or a file it names. The template entry is explained in the next lesson.

Why pin an exact file instead of "latest"? For the same reason you pin library versions in `requirements.txt`: a run today and a run next week use the same text, and when an output looks wrong you know exactly which instructions produced it.

### 12. In Code: Loading the Instructions Safely

The instruction file is now an important input to the agent. If it is broken (a missing section, a missing header, written for the wrong contract), we want the agent to **refuse to start**, loudly, instead of sending a broken system message to the model. This is the "fail fast" principle you met with the input gate on Thursday, applied to our own configuration.

**Setup.** Python 3.11 or newer. Create the project folder `tcd_agent/` with `instructions/tcd_instructions_v1.0.0.md` (Thursday's file, unchanged) and an empty `tcd/__init__.py` (the empty file makes `tcd` a Python **package**, so other code can write `from tcd.instructions import ...`). Run all commands from inside `tcd_agent/`. Later lessons need `pip install "jsonschema>=4.18" pytest`; this lesson uses only the standard library.

```python
# tcd/instructions.py
"""Load a versioned instruction file and check it before the agent uses it."""
import re
from dataclasses import dataclass
from pathlib import Path

REQUIRED_SECTIONS = [
    "Role and Goal", "Scope", "Inputs", "Process", "Rules", "Output",
    "Uncertainty and Escalation", "Boundaries", "Style",
]
HEADER = re.compile(
    r"^Version: (?P<version>\d+\.\d+\.\d+) \| "
    r"Output contract: (?P<contract>\d+\.\d+\.\d+) \| Owner: (?P<owner>.+)$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class Instructions:
    path: str
    version: str
    contract_version: str
    owner: str
    text: str
    sections: dict          # heading -> body text


def split_sections(text: str) -> dict:
    """Return {heading: body} for every '## Heading' in the file."""
    parts = re.split(r"^##\s+(.+)$", text, flags=re.MULTILINE)
    # parts = [preamble, heading1, body1, heading2, body2, ...]
    return {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts), 2)}


def load_instructions(path: str, expected_contract: str) -> Instructions:
    """Read the file, parse its header, and refuse to load a broken or mismatched file."""
    text = Path(path).read_text(encoding="utf-8")
    header = HEADER.search(text)
    if header is None:
        raise ValueError(f"{path}: header line 'Version: x.y.z | Output contract: x.y.z | Owner: ...' not found")
    sections = split_sections(text)
    missing = [s for s in REQUIRED_SECTIONS if not sections.get(s)]
    if missing:
        raise ValueError(f"{path}: missing or empty sections: {missing}")
    if header["contract"] != expected_contract:
        raise ValueError(
            f"{path}: written for output contract {header['contract']}, "
            f"but the agent uses contract {expected_contract}"
        )
    return Instructions(path, header["version"], header["contract"],
                        header["owner"].strip(), text, sections)


if __name__ == "__main__":
    ins = load_instructions("instructions/tcd_instructions_v1.0.0.md", expected_contract="1.0.0")
    print(f"loaded {ins.path}")
    print(f"version {ins.version}, contract {ins.contract_version}, owner {ins.owner}")
    for name, body in ins.sections.items():
        print(f"  {name:<28} {len(body.splitlines()):>2} lines")
```

Run it as a module (the `-m` flag runs a file inside a package, so the `tcd.` imports work):

```bash
python -m tcd.instructions
```

Output:

```text
loaded instructions/tcd_instructions_v1.0.0.md
version 1.0.0, contract 1.0.0, owner QE team
  Role and Goal                 3 lines
  Scope                         3 lines
  Inputs                        4 lines
  Process                       9 lines
  Rules                         7 lines
  Output                        3 lines
  Uncertainty and Escalation    4 lines
  Boundaries                    4 lines
  Style                         2 lines
```

How the code works, piece by piece:

- **`REQUIRED_SECTIONS`** is Thursday's list of nine sections. Keeping it in one constant means there is exactly one place to change if your team's section list changes.
- **`HEADER`** is a compiled regular expression for the header line. `(?P<version>...)` is a **named group**: after a match, `header["version"]` returns the text it captured. `\d+\.\d+\.\d+` means "digits, dot, digits, dot, digits", a semantic version such as `1.0.0`. `\|` is a literal `|` (escaped, because `|` alone means "or" in a regex). `re.MULTILINE` lets `^` and `$` match at the start and end of every line, so the header can sit on line 3.
- **`@dataclass(frozen=True)`** creates a small class whose fields are set once and then cannot change. `ins.version = "9.9.9"` would raise an error. Frozen is the right choice here: the instructions loaded at start-up must be exactly what every call sends, so nothing in the program should be able to edit them.
- **`split_sections`** uses `re.split` with a capturing group. When the pattern contains `( )`, `re.split` keeps the captured text in the result. For the tiny text `"# T\nintro\n## A\none\n## B\ntwo\nthree\n"` it returns `['# T\nintro\n', 'A', '\none\n', 'B', '\ntwo\nthree\n']`: the preamble, then heading, body, heading, body. The dictionary comprehension walks the odd positions (1, 3, 5, ...) as headings and takes the next item as the body, giving `{'A': 'one', 'B': 'two\nthree'}`.
- **`load_instructions`** checks three things in order, cheapest first: the header exists, all nine sections exist **and are not empty** (`not sections.get(s)` is true for a missing key, which returns `None`, and for an empty string), and the contract version matches what the agent expects. Any failure raises `ValueError` with a message that names the file and the problem.
- **`expected_contract`** is passed in by the caller rather than hard-coded. Later today, the agent code passes the contract version from its configuration, so the instructions and the contract can never silently disagree.
- **`text`** keeps the file content exactly as stored. The agent sends this string as the system message; the loader never edits it. Thursday's principle stands: the file in Git is precisely what the model sees.

#### What happens with a broken file

Let us prove that the loader refuses broken files. Create three damaged copies in a `scratch/` folder: one where the `## Boundaries` heading was renamed to `## Limits`, one whose header says `Output contract: 0.9.0`, and one whose header lost its `Version: 1.0.0 | ` part. Then:

```python
# try_broken.py
from tcd.instructions import load_instructions

for path in ["scratch/no_boundaries.md", "scratch/old_contract.md", "scratch/no_header.md"]:
    try:
        load_instructions(path, expected_contract="1.0.0")
        print(f"LOADED  {path}")
    except ValueError as exc:
        print(f"REFUSED {exc}")
```

Output:

```text
REFUSED scratch/no_boundaries.md: missing or empty sections: ['Boundaries']
REFUSED scratch/old_contract.md: written for output contract 0.9.0, but the agent uses contract 1.0.0
REFUSED scratch/no_header.md: header line 'Version: x.y.z | Output contract: x.y.z | Owner: ...' not found
```

- `try` / `except ValueError as exc` catches the error so the loop continues; printing `exc` shows our message, which names the file and the problem.
- The alternative is worse: the agent starts, the model never sees a Boundaries section, and weeks later someone notices that out-of-scope requests produce test cases. A clear refusal at start-up is far cheaper.
- The loader does **not** judge whether the rules are good. That is the job of review, the desk-check and the rule map.

### 13. In Code: Keeping the Rule Map Honest

The rule-to-check table from Section 8 is useful only while it matches the instruction file. Files change; tables in documents rot. So we store the map as **data** next to the instructions and check it with a script, the same way you test a template on Thursday.

The map file, `instructions/rule_map_v1.0.0.json`, lists each rule by a **short phrase** that must appear in its section, plus the IDs of the checks that verify it (`HUMAN` means "on the reviewer's checklist"):

```json
{
  "instructions_version": "1.0.0",
  "entries": [
    {"section": "Process", "phrase": "one test at the threshold and one just below it", "checks": ["Q1", "HUMAN"]},
    {"section": "Process", "phrase": "Never return more than max_cases", "checks": ["R5"]},
    {"section": "Rules", "phrase": "Use only facts stated in the acceptance criteria", "checks": ["R2", "HUMAN"]},
    {"section": "Rules", "phrase": "Copy expected messages exactly", "checks": ["HUMAN"]},
    {"section": "Rules", "phrase": "Number test cases TC-<story number>-<two digits>", "checks": ["S1", "R4"]},
    {"section": "Rules", "phrase": "List in ac_ids the ID of every acceptance criterion", "checks": ["R2", "R3"]},
    {"section": "Rules", "phrase": "Write each step as one action", "checks": ["HUMAN"]},
    {"section": "Output", "phrase": "Reply with exactly one JSON object", "checks": ["S1"]},
    {"section": "Output", "phrase": "copy story_id from the input", "checks": ["S1", "R1"]},
    {"section": "Uncertainty and Escalation", "phrase": "do not guess", "checks": ["R3", "HUMAN"]},
    {"section": "Uncertainty and Escalation", "phrase": "If no criterion can be tested", "checks": ["R6"]},
    {"section": "Boundaries", "phrase": "Never put real customer data", "checks": ["HUMAN"]}
  ]
}
```

Why a **phrase** and not a line number? Line numbers change whenever someone adds a line above; a phrase survives harmless edits but disappears when the rule itself is reworded. That is exactly when we want a human to look again.

The checker answers two questions: **map → file** (does every phrase still exist, with valid, non-empty check IDs?) and **file → map** (does every bullet in Rules, Output and Uncertainty have an entry?).

```python
# check_rule_map.py
"""Check that every instruction rule is mapped to a check, and that the map still matches the file."""
import json
import sys
from pathlib import Path

from tcd.instructions import split_sections

KNOWN_CHECKS = {"S1", "S2", "R1", "R2", "R3", "R4", "R5", "R6", "Q1", "Q2", "Q3", "HUMAN"}
BULLET_SECTIONS = ["Rules", "Output", "Uncertainty and Escalation"]   # every bullet here needs an entry


def bullets(body: str) -> list[str]:
    """Split a section body into bullets; a bullet's continuation lines are joined to it."""
    items = []
    for line in body.splitlines():
        if line.startswith("- "):
            items.append(line[2:].strip())
        elif items and line.strip():
            items[-1] += " " + line.strip()
    return items


def flat(text: str) -> str:
    """Collapse all runs of whitespace (including line breaks) to one space."""
    return " ".join(text.split())


def check(instructions_path: str, map_path: str) -> int:
    text = Path(instructions_path).read_text(encoding="utf-8")
    sections = split_sections(text)
    entries = json.loads(Path(map_path).read_text(encoding="utf-8"))["entries"]
    problems = 0

    for e in entries:                                       # 1. map -> file
        body = flat(sections.get(e["section"], ""))
        if flat(e["phrase"]) not in body:
            print(f"DRIFT     [{e['section']}] phrase not found: \"{flat(e['phrase'])}\"")
            problems += 1
        unknown = set(e["checks"]) - KNOWN_CHECKS
        if unknown:
            print(f"BAD ID    [{e['section']}] unknown check IDs {sorted(unknown)}")
            problems += 1
        if not e["checks"]:
            print(f"NO CHECK  [{e['section']}] \"{flat(e['phrase'])}\" is verified by nothing")
            problems += 1

    for name in BULLET_SECTIONS:                            # 2. file -> map
        for b in bullets(sections.get(name, "")):
            if not any(e["section"] == name and flat(e["phrase"]) in b for e in entries):
                print(f"UNMAPPED  [{name}] \"{b[:60]}...\"")
                problems += 1

    print(f"{len(entries)} map entries, {problems} problem(s)")
    return problems


if __name__ == "__main__":
    sys.exit(1 if check(sys.argv[1], sys.argv[2]) else 0)
```

How it works:

- **It reuses `split_sections`** from `tcd/instructions.py` instead of writing a second parser. Two parsers for one file format would eventually disagree.
- **`bullets`** turns a section body into a list of bullets. A line starting with `"- "` begins a new bullet; any other non-empty line is a **continuation** and is joined to the previous bullet, because our rules wrap over two or three lines. `items and line.strip()` means "there is already a bullet, and this line is not blank".
- **`flat`** collapses whitespace. `"a  b\n   c".split()` gives `['a', 'b', 'c']`, and `" ".join(...)` gives `"a b c"`. Comparing flattened text means a phrase still matches when the rule was re-wrapped onto different lines, a harmless edit.
- **Part 1 (map → file)** reports three problems: **DRIFT** (the phrase no longer exists in its section, so the rule was reworded or deleted), **BAD ID** (a typo such as `R7`; set subtraction `set(e["checks"]) - KNOWN_CHECKS` leaves only unknown IDs), and **NO CHECK** (an empty list: a rule nobody verifies).
- **Part 2 (file → map)** reports **UNMAPPED** bullets: rules someone added without deciding how they will be checked. `any(...)` is true if at least one map entry belongs to this section and its phrase appears in the bullet. `b[:60]` shortens long bullets for printing.
- **`sys.exit(1 if ... else 0)`** gives the script an **exit code**: 0 for "no problems", 1 for "problems found". Exit codes let other tools (and CI pipelines) react to the result; *Building validation scripts* later today uses the same idea at a larger scale.

**Run 1: the first version of the map.** Our first map had `"checks": []` for the Boundaries data-safety rule, exactly the gap from Section 8:

```bash
python check_rule_map.py instructions/tcd_instructions_v1.0.0.md scratch/rule_map_first_try.json
```

```text
NO CHECK  [Boundaries] "Never put real customer data" is verified by nothing
12 map entries, 1 problem(s)
```

The script found the smell for us. We resolved it as decided in the desk-check findings (F-04): assign it to human review, `"checks": ["HUMAN"]`.

**Run 2: the released map.**

```bash
python check_rule_map.py instructions/tcd_instructions_v1.0.0.md instructions/rule_map_v1.0.0.json
```

```text
12 map entries, 0 problem(s)
```

**Run 3: someone edits the instructions.** Imagine a teammate makes two small changes in a copy (`scratch/edited.md`): they shorten "Copy expected messages exactly, character for character, from the criteria." to "Copy expected messages word for word from the criteria.", and add a new bullet, "Prefer negative tests when a criterion names an error message."

```bash
python check_rule_map.py scratch/edited.md instructions/rule_map_v1.0.0.json
```

```text
DRIFT     [Rules] phrase not found: "Copy expected messages exactly"
UNMAPPED  [Rules] "Copy expected messages word for word from the criteria...."
UNMAPPED  [Rules] "Prefer negative tests when a criterion names an error messag..."
12 map entries, 3 problem(s)
```

The script cannot judge whether "word for word" is as strong as "character for character" (it is not: "word for word" allows a model to change punctuation or spelling such as "recognised" to "recognized"). What it **can** do is force a human to look at every changed rule and decide how it will be checked, before the change is merged. The new "Prefer negative tests" rule also contains a weak word ("Prefer"), which Thursday's `check_instructions.py` would not flag but a reviewer should.

**Know the limits.** Like Wednesday's weak-word linter, this is a **review aid**. It checks that rules are **mapped**, not that the mapped check really catches violations (proving that is the job of the validator's own tests, later today in *Building validation scripts*). Numbered Process steps are not scanned in part 2, so we map the important ones by hand. And choose distinctive phrases: a short phrase can match the wrong rule by accident.

### 14. What You Have Built

The result is not "a prompt that seems to work". It is a **versioned artifact** with a stated purpose, evidence for every rule, a map of how each rule is verified, a record of known gaps and decisions, and code that refuses to run with a damaged copy. When the first measured results show where the agent still goes wrong, you will change this file in a controlled way and produce a v1.1.0, later today in *Agent testing and refinement*.

---

## Practice Exercises

1. **Job card for your pair's agent.** Write a job card for the requirements agent your pair designed on Thursday (one job, consumer, inputs, outputs, done when, not this job). Check: can you state "One job" in one sentence? Does every "Done when" line correspond to a field in your output contract?
2. **Raw material list.** For the same agent, list at least five MUST and three MUST NOT behaviours, each tagged with its source (contract, a sample pair, the correction log, a known model habit). Find one behaviour that has no source and decide whether it belongs.
3. **Rewrite three rules.** Improve these first drafts using the four questions (trigger, concrete action, reason, checkable): (a) "Flag unclear requirements as appropriate." (b) "Make sure the output is in the right format." (c) "Don't make up stuff." Write the improved rule and the check (S/R/Q ID or human) that would verify it.
4. **Extend the rule map.** Add entries to `rule_map_v1.0.0.json` for Process steps 3 and 4 (cover every testable AC; set priority). Choose the check IDs, run `check_rule_map.py`, and explain why step 4 (priority) has only a human check.
---

## Knowledge Check

1. What is the difference between instructions at the "right altitude" and instructions that are "too low"?

<details><summary>Answer</summary>
Right-altitude instructions state general principles, each made concrete with an example or a measurable test (for example, "for every numeric threshold, test at the threshold and just below it, e.g. $50.00 and $49.99"). Too-low instructions hard-code case-by-case logic for specific stories, which breaks as soon as a new kind of story arrives and grows into contradictory rules.
</details>

2. Which four questions turn a first-draft rule into a good rule?

<details><summary>Answer</summary>
Can the model find the trigger in the input? Does the rule name a concrete action or source? Does it say why? Could a script or a reviewer tell whether it was followed?
</details>

3. In the rule-to-check map, the data-safety rule first had no check. Why is that a smell, and how was it resolved?

<details><summary>Answer</summary>
A rule nobody verifies is only a hope; violations would go unnoticed. It was resolved by consciously assigning it to human review (adding it to the reviewer's checklist), with an automated check noted as a possible later improvement.
</details>

4. The desk-check found that P04 (malformed input) has no instruction line. Why is that correct rather than a gap?

<details><summary>Answer</summary>
Malformed input is rejected by the input gate before the model is called, so the instructions never see it. Adding a rule for it would duplicate the gate and waste tokens.
</details>

5. The desk-check found a conflict between the instructions and pair P03 about `status`. What should you do in the desk-check, and what should you not do?

<details><summary>Answer</summary>
Record it as a finding with an owner and get a team decision. Do not silently edit either the instructions or the pair, because neither is automatically right, and any change should be measured (covered later today in Agent testing and refinement).
</details>

6. Why does `load_instructions` take `expected_contract` as a parameter instead of trusting the file's header?

<details><summary>Answer</summary>
So the caller (the agent, using its configuration) states which contract it uses, and the loader refuses a file written for a different contract. Instructions and contract can then never silently disagree.
</details>

---

## Glossary

- **Job card**: a short, human-facing description of an agent's one job, consumer, inputs, outputs, done-criteria and out-of-scope work, written before any instruction text.
- **Right altitude**: the level of detail between brittle case-by-case scripting and vague wishes; general principles made concrete with examples.
- **Rule-to-check map (traceability map)**: a record linking each instruction rule to the schema rule, code rule, quality rule or human check that verifies it.
- **Desk-check**: a manual walk-through of sample inputs against a draft, pointing at the line that decides each behaviour, to find gaps and conflicts without running a model.
- **Pin**: to reference an exact, versioned file in configuration (`agent.json`) instead of "the latest".
- **Frozen dataclass**: a Python class created with `@dataclass(frozen=True)` whose fields cannot be reassigned after creation.

---

## Summary

- Building instructions is **engineering**: start from a requirement (the job card), gather evidence, draft, make rules testable, desk-check, review, version and pin.
- Aim for the **right altitude**: general principles with concrete examples, not brittle if-else scripts and not vague wishes. Keep the file **minimal but sufficient**.
- Draft in a **writing order** that follows dependencies (Output and Inputs first, Role last), while keeping Thursday's **reading order** in the file.
- Improve each rule with four moves: **concrete trigger and action, grounded source, reason, checkable wording**.
- Link every rule to a check in a **rule-to-check map**; a rule with no check is a smell to resolve, not ignore.
- **Desk-check** the draft against P01-P05 by hand. Expect three kinds of finding: accepted gaps, things that are not the instructions' job, and real conflicts that need a team decision.
- Release the file with a **version header**, **freeze** it under a versioned file name and **pin** it in `agent.json`.
- In code, `load_instructions` **refuses** a file with a missing header, a missing or empty section, or the wrong contract version; `check_rule_map.py` keeps the map and the file in step.

---

## Additional Resources

- Anthropic Engineering, *Effective context engineering for AI agents* (Sept 2025; explains the "right altitude" for system prompts, organising them into clear sections, and starting minimal then adding rules for observed failures): https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- OpenAI Cookbook, *GPT-4.1 Prompting Guide* (its "Prompt Structure" section proposes a starting layout of Role and Objective, Instructions, Reasoning Steps, Output Format, Examples and Context, plus reminders for agent prompts): https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
- Claude Platform Docs, *Prompting best practices* (vendor guidance on clear, direct instructions, roles in the system prompt, structuring with tags, and controlling output format): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/system-prompts
