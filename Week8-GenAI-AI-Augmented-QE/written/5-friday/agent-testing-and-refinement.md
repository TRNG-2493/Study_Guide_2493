# Agent Testing and Refinement

## Learning Objectives

By the end of this lesson you will be able to:

- Tell apart three different testing jobs: testing the **validator**, validating **one output**, and testing the **agent's behaviour** across many inputs and repeated runs.
- Explain, with simple arithmetic, why **one successful run proves very little** about a non-deterministic agent.
- **Test your test data first**: validate every sample pair's reference answer with the same validator the agent faces, and fix the pairs that are wrong.
- Build an **evaluation suite** from sample pairs, executable **property checks** (MUST / MUST NOT turned into code) and **many seeded runs**, and read the **scorecard** it prints.
- Carry out **error analysis**: read the failures, group them by rule, find the root cause and pick the biggest fixable cause first.
- **Refine** the agent's instructions from evidence (TestCaseDesigner v1.0.0 → v1.1.0), version the change, record it in a changelog, and **re-evaluate** to confirm the improvement and check for regressions.
- Apply the **refinement loop** as a habit: baseline → analyse → hypothesise → change → re-run → compare → record → repeat.

---

## Why This Matters

This week you went from "what is generative AI?" to a working QA agent, and earlier today you ran it across the Project 2 backlog. In that run, five stories reached the model: three passed (one with a warning), US-412 failed R2 (an invented AC4) and US-450 failed S1 (JSON wrapped in Markdown fences).

That run raises the questions every team asks next:

- *Is that a good result or a bad one?* Two failures out of five could be bad luck or a deep problem.
- *If we change the instructions, will it get better, or just different?*
- *How would we even know?*

You would never ship a checkout page because one manual click-through worked. An agent deserves the same discipline, with one twist: a language model can answer the same question differently on a different run. One green run is an anecdote, not evidence.

This lesson completes the **Weekly Epic**: you *designed* the agent's anatomy on Thursday and *built* it today; now you **test it as a system and refine it with evidence**. For **Project 2 (Test Automation Framework)** this is the habit that makes AI-generated test cases trustworthy enough to sit next to your page objects and pytest fixtures for the e-commerce app: every change to an instruction, template or contract is checked against the same suite before it is merged.

> **Scope note.** Today we test the agent with **code-based checks and human review only**, using the sample pairs from Thursday and a **simulated** model so that every number in this lesson can be reproduced offline. **Automatic retries** when an output fails validation, and **prompt chains**, are covered in **Week 9**. Using a second model to grade the first (**LLM-as-judge**), a taxonomy of hallucinations, prompt injection and context-window testing are covered in **Week 10**. Here we only name them.

---

## The Concept

### 1. Three Different Things You Can Test

Earlier lessons today each tested something different. It is worth separating them clearly, because people often mix them up and then draw the wrong conclusions.

| What is tested | Question it answers | Where you met it | Typical tool |
|---|---|---|---|
| **The validator** | "Does my checking code catch every defect it should, and only those?" | *Building validation scripts* (`tests/test_validation.py`) | pytest with planted defects |
| **One output** | "Is *this* reply acceptable?" | *Agent output validation* (`validate_reply`) | Schema + R1-R6 + Q1-Q2 |
| **The agent** | "How often, and in what ways, does the agent produce acceptable output across many inputs and repeated runs?" | **This lesson** (`evaluate.py`) | Sample pairs + property checks + many runs + scorecard |

The three layers depend on each other in order:

1. If the **validator** is wrong, every judgement built on it is wrong. That is why you tested it first.
2. If the **reference data** (the sample pairs) is wrong, the suite measures the agent against the wrong target. We check that in Section 3.
3. Only then does the **agent's score** mean something.

### 2. Why One Run Proves Very Little

Language models are **non-deterministic**: with the same instructions and the same story, they can return different answers on different runs. Even with `temperature` set to 0 (our `agent.json` does this), many providers do not guarantee identical output every time. So one run is a **sample** of the agent's behaviour, not a full description of it.

Suppose, by hand, the agent has a hidden habit: on 25% of runs it forgets to mention one acceptance criterion. You do not know this rate; you only see runs.

- Chance that **one** run looks fine: 1 − 0.25 = **0.75**, or 75%.
- Chance that **three** runs in a row all look fine: 0.75 × 0.75 × 0.75 = 0.75³ ≈ **0.42**, or 42%.
- Chance that **ten** runs all look fine: 0.75¹⁰ ≈ **0.056**, or about 6%.
- Chance that **twenty** runs all look fine: 0.75²⁰ ≈ **0.003**, or 0.3%.

With one run, a 25% failure habit stays hidden three times out of four; with twenty, it almost certainly shows up. That is the argument for **repeated runs**.

Many runs also let you **measure a rate**: 5 failures in 20 runs estimates 25%. With only 4 runs, one extra failure moves the estimate from 25% to 50%, far too noisy to compare two versions.

**How many runs?** There is no magic number. We use **20 runs per pair**. With a real model each run costs time and money, so teams often run a small suite on every change and a bigger one before a release.

### 3. Step 0: Test Your Test Data

Before we measure the agent against the sample pairs, we must check that the pairs themselves are right. A pair's `expected_output` is a **reference answer**: an example of what a good answer looks like. If the reference answer breaks our own rules, then the target is wrong. In testing language, the pair is our **oracle**, and an oracle can have bugs too.

The check is simple: run every reference answer through `validate_reply`, the same function that judges the agent. If our own example fails our own rules, either the example or the rule is wrong.

Save this as `check_pairs_rules.py` in the project folder:

```python
# check_pairs_rules.py
"""Step 0: validate every pair's reference answer with the SAME validator the agent faces."""
import json
from pathlib import Path

from tcd.contract import check_input
from tcd.validation import validate_reply

for path in sorted(Path("samples").glob("P0*.json")):
    pair = json.loads(path.read_text(encoding="utf-8"))
    if pair["expected_output"] is None:                 # P04: no agent output expected
        print(f"{pair['pair_id']}  SKIP  (invalid input, no reference answer)")
        continue
    report = validate_reply(check_input(pair["input"]), json.dumps(pair["expected_output"]))
    print(f"{pair['pair_id']}  {report.verdict}")
    for f in report.findings:
        print(f"      {f.rule} {f.where}: {f.message}")
```

How it works:

- P04 has `expected_output: null` (Python `None`), because the correct behaviour for invalid input is that the **gate rejects it** before any model call. There is nothing to validate, so we skip it.
- `check_input(pair["input"])` runs the input gate and applies defaults (`max_cases` 10, techniques EP and BVA), exactly as the agent does. R5 and Q1 need those defaults.
- `json.dumps(pair["expected_output"])` turns the reference answer back into **text**, because `validate_reply` expects a raw reply string, just like the model's.

Run it with `python check_pairs_rules.py`:

```text
P01  PASS
P02  PASS
P03  FAIL
      R3 test_cases: AC1 is not covered by any test case or open question
      R3 test_cases: AC3 is not covered by any test case or open question
P04  SKIP  (invalid input, no reference answer)
P05  FAIL
      R3 test_cases: AC1 is not covered by any test case or open question
```

Two of our five pairs fail **R3** ("every input AC is covered by a test case or mentioned in `open_questions`"). Let us look at why, by hand.

**P03 (US-310, shipping address).** The story has four ACs: AC1 (required fields), AC2 (5-digit ZIP), AC3 (10-digit phone) and AC4 ("fast and user-friendly"). The reference answer contains one test case (for AC2) and two open questions (both about AC4). AC1 and AC3 are perfectly testable, yet they have no test case and no question. That breaks R3, and it also breaks the agent's own instructions: *Process step 3* says "Write at least one test case for every acceptance criterion that can be tested." The pair's MAY list said "include test cases for the clear ACs (AC1-AC3)", but our automated rules say they are required, not optional. The rule is right; the example is too thin.

**P05 (US-999, release notes).** The reference answer correctly refuses to design test cases, but its question ("The input looks like release notes ...") does not name **AC1**. R3 looks for the AC ID inside the questions, so AC1 counts as neither covered nor questioned. Here the rule and the example disagree on a detail; naming the AC in the question is cheap and makes the traceability explicit, so we fix the example.

Nobody did bad work here: Thursday's pairs were written **before** R3 was automated, and the moment the rule became code it found where examples and rules had drifted apart. That is why you validate pairs too: **the bug may be in the test, not in the system under test**.

#### Fixing the pairs

We revise the two pair files. P03 gets test cases for AC1 and AC3; P05's question names AC1. We also add a `revision` number to each changed pair, so anyone can see the pair changed even though the **contract** did not (`contract_version` stays `1.0.0`: the shape of the data did not change, only one example).

```python
# fix_pairs.py
"""Revise P03 and P05 so their reference answers obey R3 (pair revision 2)."""
import json
from pathlib import Path

def update(path: str, change) -> None:
    p = Path(path)
    pair = json.loads(p.read_text(encoding="utf-8"))
    change(pair)
    pair["revision"] = 2                       # the PAIR changed; contract_version stays 1.0.0
    p.write_text(json.dumps(pair, indent=2) + "\n", encoding="utf-8")

def fix_p03(pair):
    pair["expected_output"]["test_cases"] = [
        {"id": "TC-310-01", "title": "Missing phone number blocks saving", "ac_ids": ["AC1"],
         "type": "negative", "priority": "medium",
         "steps": ["Fill name, street, city and ZIP with valid data", "Leave phone empty", "Click Save"],
         "expected_result": "Address is not saved and the phone field is marked as required"},
        {"id": "TC-310-02", "title": "ZIP with 4 digits is rejected", "ac_ids": ["AC2"],
         "type": "boundary", "priority": "medium",
         "steps": ["Fill all fields with valid data", "Enter ZIP 1234", "Click Save"],
         "expected_result": "Address is not saved and the ZIP field shows an error"},
        {"id": "TC-310-03", "title": "Phone with 9 digits is rejected", "ac_ids": ["AC3"],
         "type": "boundary", "priority": "medium",
         "steps": ["Fill all fields with valid data", "Enter phone 555123456", "Click Save"],
         "expected_result": "Address is not saved and the phone field shows an error"},
    ]

def fix_p05(pair):
    pair["expected_output"]["open_questions"] = [
        "AC1 reads like release notes, not a user story. Which behaviour should be tested?"]

update("samples/P03-clarification.json", fix_p03)
update("samples/P05-out_of_scope.json", fix_p05)
print("P03 and P05 updated to revision 2")
```

In a real project you would simply edit the two JSON files by hand in a pull request; the script keeps the lesson reproducible. Run `python fix_pairs.py`, then `python check_pairs_rules.py` again:

```text
P03 and P05 updated to revision 2
P01  PASS
P02  PASS
P03  PASS
P04  SKIP  (invalid input, no reference answer)
P05  PASS
```

All reference answers now obey our rules. Make `check_pairs_rules.py` part of your routine: run it whenever a pair or a rule changes.

### 4. Anatomy of the Evaluation Suite

An **evaluation suite** (an **eval** for short) is a repeatable test of the agent's behaviour. Ours has four ingredients:

1. **Inputs**: the sample pairs P01 to P05 (Thursday's design, now with honest reference answers).
2. **Checks**: the full validator (schema, R1-R6, Q1-Q2) **plus** pair-specific **property checks** that encode each pair's MUST / MUST NOT expectations.
3. **Repetition**: each pair is run many times (20), each time with a different **seed**.
4. **A scorecard**: pass counts per pair, an overall pass rate, and how often each rule failed.

#### 4.1 From MUST / MUST NOT prose to code

On Thursday you wrote expectations in plain English. Many of them can be turned into small Python functions that return `True` or `False` for one output. Each such function is a **property check**: it checks a *property* of the answer ("has a boundary case at $50.00") rather than comparing the whole answer to an exact expected text. That matters because two good answers can word titles and steps differently (a MAY in P01).

Here is how P01's expectations became code (from `evaluate.py`):

```python
def text_of(out: dict) -> str:
    """All human-readable text in an output, for 'does it mention ...' checks."""
    return json.dumps(out)


# Executable versions of each pair's MUST / MUST NOT expectations.
PAIR_CHECKS = {
    "P01": [
        ("status is ok",                 lambda o: o["status"] == "ok"),
        ("boundary case at $50.00",      lambda o: any(tc["type"] == "boundary" and "$50.00" in json.dumps(tc) for tc in o["test_cases"])),
        ("boundary case at $49.99",      lambda o: any(tc["type"] == "boundary" and "$49.99" in json.dumps(tc) for tc in o["test_cases"])),
        ("AC3 message copied exactly",   lambda o: "Coupon code not recognised" in text_of(o)),
        ("MUST NOT invent expiry rules", lambda o: "expir" not in text_of(o).lower()),
    ],
    # ... P02, P03 and P05 follow the same pattern
}
```

Line by line:

- `PAIR_CHECKS` maps a pair ID to a **list of (description, function) tuples**: the description is for humans reading a failure, the function for the computer.
- `lambda o: o["status"] == "ok"` is a tiny **anonymous function** that takes the parsed output `o` and returns `True` or `False`.
- `any(... for tc in o["test_cases"])` is `True` if **at least one** test case is a boundary case mentioning `$50.00` anywhere in its text (`json.dumps(tc)` makes the whole test case one searchable string).
- `"Coupon code not recognised" in text_of(o)` checks the exact message, British spelling included; a model that "corrects" it to "recognized" fails, as it should.
- `"expir" not in text_of(o).lower()` is the MUST NOT: no invented expiry rule ("expiry", "expires", "expired" all contain `expir`). `.lower()` makes the check case-insensitive.

The prose-to-code mapping for all pairs:

| Pair | Expectation (prose) | Became code? |
|---|---|---|
| P01 | status is ok | Yes |
| P01 | boundary cases at $50.00 and $49.99 | Yes (two checks) |
| P01 | AC3 message copied exactly | Yes |
| P01 | MUST NOT invent rules (e.g. expiry dates) | **Partly**: we can catch the known example "expiry"; we cannot list every possible invented rule |
| P01 | MUST NOT exceed 6 test cases | Already covered by **R5** in the validator |
| P02 | exactly 1 test case, tracing to AC3 | Yes |
| P03 | needs_clarification; a question names AC4; AC4 not tested as if clear | Yes |
| P03 | MUST NOT invent a number for "fast" | **Partly** (the "AC4 not in any ac_ids" check catches the usual form) |
| P04 | input rejected, model never called | Yes (handled separately, Section 4.3) |
| P05 | needs_clarification, no test cases | Yes |
| All | expected results agree with the AC they trace to (Q3) | **No: human review** |

The last row matters. Whether "Total is $45.00" is the *right* answer for a $50.00 cart with 10% off needs someone who understands the requirement. Code can check shape, traceability and known patterns; a human still checks meaning. (Using a second model as a grader is a Week 10 topic; in this course, for now, that judgement belongs to people.)

#### 4.2 The simulated model

To test the agent we need a model to call. A real model needs an account, costs money and gives slightly different answers on every run, so your numbers would not match the lesson's. Instead, `tcd/simulated.py` provides a **simulated model**. Read its docstring carefully:

```python
# tcd/simulated.py
"""A SIMULATED model for practising agent testing offline.

It starts from a correct answer for each story and then injects typical mistakes
at rates WE CHOSE for teaching. The rates fall when the instructions contain the
rule that targets the mistake. The numbers are illustrative, not measurements
of any real model.
"""
import copy
import json
import random
import re
from pathlib import Path

# mistake: (rate without the rule, rate with the rule, phrase that marks the rule)
MISTAKES = {
    "fences":        (0.08, 0.08, None),        # no instruction change targets this
    "invented_ac":   (0.25, 0.03, "never create an ID such as AC5"),
    "dropped_ac":    (0.30, 0.05, "check that every acceptance criterion ID appears"),
    "vague_result":  (0.20, 0.04, 'Never write "works correctly"'),
    "over_limit":    (0.15, 0.15, None),
}
```

So the simulated model:

- Starts from a **correct answer** for each story (stored in `sim_answers.json`; its US-310 answer is identical to the revised P03 reference answer).
- With some probability, injects one of five **typical mistakes**: wrapping the JSON in fences, inventing an `AC5` test case, dropping the open questions (so an AC is no longer covered), writing a vague expected result, or adding one test case too many.
- Uses a **lower rate** for a mistake if the instructions it receives contain a specific phrase. This imitates what we hope a real instruction change will do, in a controlled way.

The mistakes are realistic (you met all of them earlier this week: format drift on Tuesday, invented requirements and vague oracles on Wednesday, traceability on Thursday), but **the rates are invented for teaching**. Do not quote them as facts about any real model. The point of the simulation is to let you practise the *method* with numbers you can reproduce exactly.

The heart of the class:

```python
class SimulatedModel:
    def __init__(self, seed: int, answers: str = "sim_answers.json"):
        self.seed = seed
        self.answers = json.loads(Path(answers).read_text(encoding="utf-8"))
        self.calls = 0

    def complete(self, messages: list, settings: dict) -> str:
        self.calls += 1
        system, user = messages[0]["content"], messages[-1]["content"]
        story_id = re.search(r"^ID: (US-\d{3})$", user, re.MULTILINE).group(1)
        max_cases = int(re.search(r"Return at most (\d+) test cases", user).group(1))
        rng = random.Random(f"{self.seed}-{story_id}")          # same seed -> same reply
        out = copy.deepcopy(self.answers[story_id])

        def happens(name):
            without, with_rule, phrase = MISTAKES[name]
            rate = with_rule if phrase and phrase in system else without
            return rng.random() < rate
        # ... each mistake is applied if happens(...) returns True
```

It has the same `complete(messages, settings)` method as every model client, so the agent cannot tell it apart from a real one. It finds the story ID and the case limit in the rendered user message, counts its calls in `self.calls` (so the eval can prove the model was never called for invalid input), copies the correct answer with `copy.deepcopy` so the stored original is never damaged, and lets each mistake happen when `rng.random()` (a number between 0 and 1) falls below that mistake's rate.

#### Seeds: making randomness repeatable

`random.Random(f"{self.seed}-{story_id}")` creates a random number generator from a **seed**, here a string such as `"7-US-205"`. The same seed always produces the same sequence of numbers. So run 7 for US-205 makes the same "decisions" every time you run the eval, on any computer. Your numbers will match this lesson's.

There is a second, subtler benefit. Because the seed depends only on the run number and the story, **version 1.0.0 and version 1.1.0 of the instructions receive exactly the same random draws**. If run 7 drew 0.12 for "invented AC", it draws 0.12 under both versions. Under v1.0.0 the rate is 0.25, so the mistake happens; under v1.1.0 the rate is 0.03, so it does not. Any difference between the two scorecards is therefore caused by the **instruction change**, not by luck. Statisticians call this a **paired comparison** (or "common random numbers"). With a real model you cannot control the dice this way, which is one more reason to use enough runs.

#### 4.3 Walking through `evaluate.py`

Here is the evaluation function:

```python
def evaluate(config: str, runs: int) -> dict:
    pairs = {p["pair_id"]: p for p in
             (json.loads(f.read_text(encoding="utf-8")) for f in sorted(Path("samples").glob("P0*.json")))}
    scores, rule_failures, rule_warnings = {}, Counter(), Counter()

    # P04 (invalid input) is checked once: the gate must reject it and the model must not be called.
    model = SimulatedModel(seed=0)
    result = TestCaseDesigner(model, config).run(pairs["P04"]["input"])
    scores["P04"] = (int(result.outcome == "rejected_input" and model.calls == 0), 1)

    for pair_id, checks in PAIR_CHECKS.items():
        passed = 0
        for seed in range(runs):
            run = TestCaseDesigner(SimulatedModel(seed), config).run(pairs[pair_id]["input"])
            rule_failures.update(f.rule for f in run.report.errors)
            rule_warnings.update(f.rule for f in run.report.warnings)
            ok = run.outcome != "FAIL"
            if ok:                                     # property checks need a valid output
                out = json.loads(run.reply)
                ok = all(check(out) for _, check in checks)
            passed += ok
        scores[pair_id] = (passed, runs)
    return {"scores": scores, "rule_failures": rule_failures, "rule_warnings": rule_warnings}
```

Step by step:

1. **Load the pairs** into a dictionary keyed by `pair_id`: `{"P01": {...}, "P02": {...}, ...}`.
2. **Prepare counters.** `Counter` (from `collections`) counts things: `rule_failures.update(["R3", "R6"])` adds 1 for R3 and 1 for R6.
3. **P04 once.** The input gate is deterministic code, so one run is enough. It passes only if the outcome is `"rejected_input"` **and** `model.calls == 0`: rejecting the input but still paying for a model call would be a bug. `int(True)` is 1.
4. **Every other pair, many times.** For each seed, build a fresh agent with a fresh simulated model and run the pair's input. `config` chooses `agent.json` (v1.0.0) or `agent_v1.1.0.json`. Every error and warning is counted.
5. **Pass or fail.** A run passes only if the validator did not say `FAIL` **and** `all(...)` property checks return `True` (`_` names the unused description). The checks run only on non-FAIL outputs, because fenced JSON would crash `json.loads`.
6. **`passed += ok`** works because `True` counts as 1 and `False` as 0.

`main()` prints one line per pair, an overall line and the two counters. The overall rate mixes P04's single run with 20 runs per other pair, so treat it as a rough summary; the per-pair lines are the ones to study.

### 5. The Baseline: How Good Is v1.0.0?

Before changing anything, measure. This first measurement is the **baseline**: the reference point every later version is compared with. Without it, "the new version looks better" is just a feeling.

Run:

```bash
python evaluate.py
```

Output (instructions v1.0.0, 20 runs per pair):

```text
config agent.json, 20 runs per pair
  P01: 10/20    50%
  P02: 13/20    65%
  P03: 11/20    55%
  P04:  1/1    100%
  P05: 12/20    60%
  overall: 47/81 = 58%
  errors by rule:   {'R2': 11, 'R3': 18, 'R5': 7, 'R6': 11, 'S1': 5}
  warnings by rule: {'Q2': 9}
```

(`evaluate.py` does not use the pairs' `expected_output` at all, only their inputs and the property checks, so the pair fixes from Section 3 do not change these numbers. They mattered for the honesty of our data, and they matter to anyone who reads the pairs as examples or uses them as few-shot examples.)

How to read it:

- **P04 is 100%.** The input gate works every time, as it should; it is plain code.
- **Every other pair passes only 50-65% of the time.** In other words, on roughly two runs out of five, the agent produces output our pipeline would reject. A reviewer looking at one run could easily see a perfect answer and conclude "the agent is great".
- **The error counts tell you *how* it fails.** R3 (an AC neither tested nor questioned) is the most common error with 18; R6 (`needs_clarification` with no questions) and R2 (an invented AC ID) follow with 11 each; then R5 (too many cases, 7) and S1 (fenced JSON, 5).
- **Q2 warnings (9)** are vague expected results such as "The feature works correctly". They do not fail a run, but each one costs a reviewer time.

Save this output. It is your baseline.

### 6. Error Analysis: Read the Failures, Then Count Them

Counts tell you *where* to look; reading tells you *why*. Never skip reading. A small helper prints every failing run for one pair:

```python
# show_failures.py
"""Error analysis: print every failing run for one pair, so a human can READ them."""
import json
import sys
from pathlib import Path

from tcd.agent import TestCaseDesigner
from tcd.simulated import SimulatedModel

config, pair_id = sys.argv[1], sys.argv[2]
pair = json.loads(next(Path("samples").glob(f"{pair_id}-*.json")).read_text(encoding="utf-8"))
for seed in range(20):
    run = TestCaseDesigner(SimulatedModel(seed), config).run(pair["input"])
    if run.outcome == "FAIL":
        rules = sorted({f.rule for f in run.report.errors})
        print(f"seed {seed:>2}: {', '.join(rules):<8} {run.report.errors[0].message}")
```

- `sys.argv[1]` and `sys.argv[2]` are the config file and pair ID typed after the script name.
- `next(Path("samples").glob(f"{pair_id}-*.json"))` takes the first (and only) file whose name starts with that pair ID.
- `{f.rule for f in ...}` is a **set comprehension**, so a rule that fired twice is listed once.

Run `python show_failures.py agent.json P01`:

```text
seed  0: S1       reply is wrapped in Markdown fences; the contract forbids them
seed  1: R2       'AC5' is not an acceptance criterion of US-205 (expected one of ['AC1', 'AC2', 'AC3', 'AC4'])
seed  4: R2       'AC5' is not an acceptance criterion of US-205 (expected one of ['AC1', 'AC2', 'AC3', 'AC4'])
seed  5: R3       AC4 is not covered by any test case or open question
seed  8: R2, R3   'AC5' is not an acceptance criterion of US-205 (expected one of ['AC1', 'AC2', 'AC3', 'AC4'])
seed 10: R3       AC4 is not covered by any test case or open question
seed 11: R3       AC4 is not covered by any test case or open question
seed 12: R3       AC4 is not covered by any test case or open question
seed 14: R3       AC4 is not covered by any test case or open question
seed 16: R3       AC4 is not covered by any test case or open question
```

Reading the ten failures (the 10/20 on the scorecard), three patterns jump out:

1. **AC4 silently disappears** (seeds 5, 8, 10, 11, 12, 14, 16). The agent drops the open question about "Only one coupon per order", so AC4 is neither tested nor questioned. A reviewer would never notice something that is *absent*; the rule notices.
2. **An invented `AC5` test case** (seeds 1, 4, 8). The agent tests something the story never says.
3. **Fenced JSON** (seed 0). Once in twenty for this pair.

Seed 8 shows two mistakes in one run. One run can break several rules, which is why rule counts add up to more than the number of failed runs.

#### 6.1 From symptoms to root causes

Now group every rule failure by its **root cause**: the part of the agent you would have to change to prevent it. A useful set of categories for agents:

| Root-cause category | Meaning | Example from our scorecard |
|---|---|---|
| **Instructions** | The rule is missing, vague or easy to skip | R3/R6: nothing tells the model to *check* coverage before replying; R2: nothing explicitly forbids inventing IDs; Q2: nothing defines a concrete expected result |
| **Template** | The per-call wording is wrong or ambiguous | None found this time |
| **Contract** | The schema or rules are wrong or too strict | None this time (the rules were right; we checked in Section 3) |
| **Pair / oracle** | The test data is wrong | P03 and P05, fixed in Section 3 |
| **Model habit (format)** | The model's formatting habits break the contract regardless of wording | S1 fenced JSON, R5 one case too many |

Then prioritise. A simple rule: **fix the biggest cause you can actually fix, first.**

- **Dropped coverage (R3 + R6, 29 errors)** is the biggest group. Note that R6 is the same mistake seen from another angle: on P03 and P05 (status `needs_clarification`), dropping the open questions breaks both R3 and R6. One cause, two rules.
- **Invented AC IDs (R2, 11 errors)** is next, and it is dangerous: a test for a non-existent requirement fails on correct software.
- **Vague expected results (Q2, 9 warnings)** cost reviewers time and are cheap to address.
- **Fences (S1, 5) and over-limit (R5, 7)** are real, but the instructions already forbid both, and repeating a sentence louder rarely helps. The validation gate already rejects them; retry strategies come in **Week 9**. Today we **accept and document** them.

#### 6.2 Write a hypothesis before you change anything

Turn each chosen cause into a testable statement:

- **H1:** If the Process section tells the agent to *check* that every AC ID appears in a test case or an open question before replying, R3 and R6 errors will fall.
- **H2:** If the Rules section explicitly forbids AC IDs that are not in the input, R2 errors will fall.
- **H3:** If the Style section defines a concrete expected result and names the banned phrases, Q2 warnings will fall.
- **And for all three:** no pair will get worse (no **regression**), and S1/R5 will stay roughly where they are (we did not target them).

Writing it first stops you inventing a story after seeing a different number.

### 7. Refine: From v1.0.0 to v1.1.0

The fix lives in a **new file**, `instructions/tcd_instructions_v1.1.0.md`. The old file stays untouched, so you can always re-run the old version, compare and roll back. Here is the real `diff` between the two files:

```bash
diff instructions/tcd_instructions_v1.0.0.md instructions/tcd_instructions_v1.1.0.md
```

```text
3c3
< Version: 1.0.0 | Output contract: 1.0.0 | Owner: QE team
---
> Version: 1.1.0 | Output contract: 1.0.0 | Owner: QE team
25a26,27
>    Before replying, check that every acceptance criterion ID appears in the
>    ac_ids of a test case or is named in an open question.
38a41,42
>   Use only IDs that appear in the input story; never create an ID such as AC5
>   for an idea the story does not state.
49,50c53,55
< - If no criterion can be tested, set status to "needs_clarification" and return
<   an empty test_cases list. Otherwise set status to "ok".
---
> - If any criterion needs clarification, set status to "needs_clarification" and
>   still return test cases for the criteria that can be tested. If no criterion
>   can be tested, return an empty test_cases list. Otherwise set status to "ok".
60a66,67
> - expected_result names the exact total, message, page or state a tester will
>   see. Never write "works correctly" or "as expected".
```

How to read `diff` output: `3c3` means "line 3 **c**hanged"; lines starting with `<` are the old text, `>` the new. `25a26,27` means "after old line 25, **a**dd new lines 26-27".

Why each change:

- **Header.** Instructions move to 1.1.0; the output contract stays 1.0.0, so the loader from *Building agent instructions* still accepts the file.
- **Process step 3 (H1).** Adds a **self-check** before replying, worded in the same terms as R3, so the model's rule and the automated check say the same thing.
- **Rules (H2).** Names the exact failure (`AC5`) and gives the reason, following Thursday's "concrete examples and reasons" principle.
- **Style (H3).** Defines "concrete" (total, message, page or state) and names the vague phrases we saw, mirroring Q2.
- **Uncertainty (closes desk-check finding F-02).** In *Building agent instructions* the desk-check found that v1.0.0 says `ok` when some ACs are testable, while pair P03 expects `needs_clarification`. The QE lead decided the pair is right: a story with any unclear AC must go back to the product owner, so the status has to say so. This change is a decision, not an eval fix; our simulation does not exercise it, so it does not move the numbers.

Each new line is **testable**: you can point to the rule in the catalogue (R3, R2, Q2) that checks it. That is the test of a good instruction you met on Thursday.

#### 7.1 Versioning and the changelog

Why 1.1.0 and not 1.0.1 or 2.0.0? By our team's convention:

- **Not MAJOR (2.0.0):** consumers of the output see exactly the same contract (1.0.0). Nothing they parse changes.
- **Not PATCH (1.0.1):** this is not a typo fix; we added three new rules and clarified the status rule, which changes the agent's behaviour in ways consumers can rely on.
- **MINOR (1.1.0):** new guaranteed behaviour, same contract.

Teams draw these lines differently; write your convention down and apply it consistently.

Record the change with its **evidence**, so a future reader knows why each line exists:

```text
# CHANGELOG – TestCaseDesigner instructions

## 1.1.0 – 2026-10-23
- Process step 3: added a coverage self-check before replying.
  Evidence: baseline eval (20 runs/pair) had 18 R3 and 11 R6 errors from dropped open questions.
- Rules: only AC IDs from the input; never invent IDs such as AC5.
  Evidence: 11 R2 errors (invented AC5 test cases).
- Style: expected_result must name an exact total, message, page or state.
  Evidence: 9 Q2 warnings ("works correctly").
- Uncertainty: status is needs_clarification whenever any AC needs clarification.
  Evidence: desk-check finding F-02 (decision by QE lead; P03 expectation confirmed).
- Not addressed: S1 fenced JSON (5), R5 over max_cases (7). Kept behind the validation gate;
  retry handling is planned (Week 9).
```

Finally, the agent's configuration points to the new file. `agent_v1.1.0.json`:

```json
{
  "agent": "TestCaseDesigner",
  "version": "1.1.0",
  "instructions": "instructions/tcd_instructions_v1.1.0.md",
  "template": {"name": "tcd_user", "version": "1.0.1"},
  "contract_version": "1.0.0",
  "model_settings": {"temperature": 0, "max_tokens": 2000}
}
```

Only `version` and `instructions` changed. The template (`tcd_user@1.0.1`), the contract and the model settings are identical, so if the scores move, the instructions are the only explanation.

#### 7.2 One change at a time (and when we bent the rule)

The cleanest experiment changes **one thing**. We bundled three targeted changes because each targets a *different* rule (R3/R6, R2, Q2), so the scorecard still shows which part helped (the F-02 status clarification is a recorded decision, not part of the experiment). To attribute effects properly, use **ablation**: remove one change at a time and re-run (practice exercise 4).

### 8. Re-Evaluate and Compare

Run the **same suite**, with the **same seeds**, on the new configuration:

```bash
python evaluate.py --config agent_v1.1.0.json
```

```text
config agent_v1.1.0.json, 20 runs per pair
  P01: 16/20    80%
  P02: 17/20    85%
  P03: 17/20    85%
  P04:  1/1    100%
  P05: 18/20    90%
  overall: 69/81 = 85%
  errors by rule:   {'R2': 3, 'R3': 2, 'R5': 3, 'R6': 1, 'S1': 5}
  warnings by rule: {'Q2': 2}
```

Put the two runs side by side:

| | v1.0.0 | v1.1.0 | Change |
|---|---|---|---|
| P01 | 10/20 (50%) | 16/20 (80%) | +30 points |
| P02 | 13/20 (65%) | 17/20 (85%) | +20 |
| P03 | 11/20 (55%) | 17/20 (85%) | +30 |
| P04 | 1/1 (100%) | 1/1 (100%) | same |
| P05 | 12/20 (60%) | 18/20 (90%) | +30 |
| **Overall** | **47/81 (58%)** | **69/81 (85%)** | **+27** |
| R3 errors | 18 | 2 | H1 confirmed |
| R6 errors | 11 | 1 | H1 confirmed |
| R2 errors | 11 | 3 | H2 confirmed |
| Q2 warnings | 9 | 2 | H3 confirmed |
| S1 errors | 5 | 5 | not targeted, unchanged |
| R5 errors | 7 | 3 | not targeted (see below) |

Check the hypotheses one by one: all three targeted rules fell sharply. **No pair got worse**, so there is no regression. S1 is unchanged, as predicted.

R5 dropped from 7 to 3 although we did not target it: in the simulation, an invented `AC5` case could push P02 (limit 1) over its limit, so fixing R2 removed some R5 errors too. Always look for such **knock-on effects**; a fix can also make another rule worse.

You can also watch individual runs change. `python show_failures.py agent_v1.1.0.json P01`:

```text
seed  0: S1       reply is wrapped in Markdown fences; the contract forbids them
seed  1: R2       'AC5' is not an acceptance criterion of US-205 (expected one of ['AC1', 'AC2', 'AC3', 'AC4'])
seed  4: R2       'AC5' is not an acceptance criterion of US-205 (expected one of ['AC1', 'AC2', 'AC3', 'AC4'])
seed 10: R3       AC4 is not covered by any test case or open question
```

Thanks to paired seeds, the failures that remain are a **subset** of the old ones: seeds 5, 8, 11, 12, 14 and 16 are now fixed, and seed 0's fenced JSON is still there. Seeds 1 and 4 still invent `AC5`, because their random draws were below even the new, lower rate of 3%. A better instruction makes a mistake **rarer**, not impossible. That is exactly why the validation gate stays in place.

#### 8.1 Did we break anything else?

Re-run the full test suite after **any** change, as you would your Project 2 regression suite:

```bash
python -m pytest -q tests
```

```text
............                                                             [100%]
12 passed in 0.13s
```

The validator's own tests still pass.

#### 8.2 Is v1.1.0 good enough to ship?

A score is only useful if you decided **in advance** what "good enough" means. These are **acceptance criteria** for the agent, written exactly like acceptance criteria for a user story. An example set for TestCaseDesigner:

| Criterion | Target | v1.1.0 | Met? |
|---|---|---|---|
| Invalid input rejected without a model call | 100% | 100% | Yes |
| Every pair passes at least 80% of runs | ≥ 80% | lowest is P01 at 80% | Yes (just) |
| No pair worse than the previous version | no regression | all improved | Yes |
| Contract errors trending down | fewer than baseline | 14 vs 52 | Yes |
| Human spot-check: 10 passing outputs reviewed with the Wednesday checklist (Q3: expected results agree with their ACs) | 0 meaning errors | to be done by a reviewer | Pending |

The last row is not optional. Our automated checks cannot see whether an expected result is *correct*; only a reviewer can. A passing scorecard says "the output is well-formed, traceable and avoids known mistakes", not "the tests are right".

Assuming the spot-check is clean, the decision might read: *Ship v1.1.0 for internal use. Output continues to pass through the validation gate and human review (Wednesday's sign-off states). Known remaining issues: fenced JSON in about 1 run in 16 and occasional over-limit output; both are rejected by the gate and are planned for retry handling (Week 9).*

### 9. The Refinement Loop as a Habit

Everything you did in this lesson follows one loop. Write it on a sticky note:

```text
      ┌──────────────────────────────────────────────────────────────┐
      ▼                                                              │
 1. Baseline ──► 2. Read failures ──► 3. Group by root cause ──►     │
 (same suite)    (show_failures)      (instructions/template/        │
                                       contract/pair/format)         │
      ──► 4. Hypothesis ──► 5. Change ONE thing ──► 6. Re-run SAME ──┤
          (written first)    (new version file)    suite + tests     │
      ──► 7. Compare & check regressions ──► 8. Record (changelog) ──┘
```

Some habits that keep the loop healthy:

- **Same suite, same seeds, same settings.** Change the suite in its own step (as with P03 and P05) and re-baseline; never change suite and agent together.
- **Keep old versions**, so "was it better before?" is answered with a re-run, not a memory.
- **Every real failure becomes a pair.** Last lesson's run invented an AC4 ("Search ignores upper and lower case") for **US-412**. A new pair **P06** with a MUST NOT "test case-insensitive search" puts that failure into every future evaluation, just as a bug report becomes a regression test in Project 2.
- **Know when to stop.** Stop when the acceptance criteria are met and the next improvement costs more than it saves. Then switch to **monitoring**: run the suite on every change to instructions, templates, contract or model, ideally in CI next to the validator tests.
- **Re-baseline when the model changes.** A new model version is a new system under test.

---

## Practice Exercises

1. **One run vs many, by hand.** An agent fails 10% of the time. Calculate the chance that 1, 5 and 20 runs in a row all pass. How many runs do you need before the chance of seeing *zero* failures drops below 20%? (Hint: try 0.9ⁿ for increasing n.)
2. **Step 0 on your own pairs.** Run `check_pairs_rules.py` against the pairs you designed for your requirements agent in Thursday's pair-programming exercise (adapting the validator calls to your agent's rules). Record every pair that fails, decide whether the **pair** or the **rule** is wrong, and fix it with a revision note.
3. **Turn prose into checks.** Write property checks for P06 (US-412, from Section 9): status `ok`; the message "No products found" copied exactly; a boundary case for the 2-character rule; MUST NOT mention case-insensitivity. Add P06 to `PAIR_CHECKS` and the samples folder (you will also need a correct US-412 answer in `sim_answers.json`), then re-run `evaluate.py` for both versions.
4. **Ablation.** Make three instruction files (plus configs), each with **only one** v1.1.0 change. Evaluate each; tabulate which rule counts moved. Did any change help a rule it did not target?
5. **More runs.** Run both versions with `--runs 50`. Do the per-pair percentages move? Which conclusions from the 20-run comparison still hold?
---

## Knowledge Check

1. What is the difference between testing the validator, validating one output and testing the agent?

<details><summary>Answer</summary>
Testing the validator checks that the checking code catches each defect it should (and no others), using planted defects. Validating one output decides whether a single reply is acceptable. Testing the agent measures how often, and in which ways, the agent produces acceptable output across many inputs and repeated runs.
</details>

2. An agent fails 25% of the time. What is the chance that three runs in a row all look fine?

<details><summary>Answer</summary>
0.75 × 0.75 × 0.75 = 0.75³ ≈ 0.42, about 42%. So a serious habit stays hidden in almost half of all three-run checks.
</details>

3. Why do we validate the sample pairs' reference answers before evaluating the agent?

<details><summary>Answer</summary>
Because the pairs are the oracle. If a reference answer breaks our own rules (as P03 and P05 broke R3), the suite measures the agent against the wrong target. The bug can be in the test data, not the system under test.
</details>

4. Why is P04 evaluated only once, and what two things must be true for it to pass?

<details><summary>Answer</summary>
The input gate is plain, deterministic code, so repeating it adds no information. It passes only if the outcome is `rejected_input` and the model was never called (`model.calls == 0`).
</details>

5. What does seeding the simulated model with `f"{seed}-{story_id}"` give us when comparing v1.0.0 with v1.1.0?

<details><summary>Answer</summary>
Repeatable results, and a paired comparison: both versions receive exactly the same random draws, so differences in the scorecard come from the instruction change, not from luck.
</details>

6. Why were the S1 (fenced JSON) and R5 (too many cases) failures not addressed with new instruction text?

<details><summary>Answer</summary>
The instructions already state both rules clearly; repeating them rarely helps. These formatting habits are better handled by the pipeline: the validation gate rejects them today, and retry strategies (Week 9) will handle them later.
</details>

7. After refining, which acceptance criterion can only be checked by a human, and why?

<details><summary>Answer</summary>
Whether each expected result agrees with the acceptance criterion it traces to (Q3). Code can check shape, traceability and known patterns, but not whether "Total is $45.00" is the correct result for the requirement.
</details>

---

## Glossary

- **Acceptance criteria (for an agent):** Pre-agreed, measurable conditions the evaluation results must meet before a version is used.
- **Baseline:** The first measurement of the current version, used as the reference for every later comparison.
- **Error analysis:** Reading failed outputs, grouping them by rule and root cause, and deciding what to fix first.
- **Evaluation suite (eval):** A repeatable test of an agent's behaviour: inputs, checks, repeated runs and a scorecard.
- **Oracle:** The source of truth for what a correct result is; here, the pairs' reference answers and expectations.
- **Paired comparison (common random numbers):** Comparing two versions under exactly the same random conditions, so differences come from the versions themselves.
- **Property check:** A small function that checks one property of an output (for example "a question names AC4") instead of comparing the whole output to an exact expected text.
- **Simulated model:** A stand-in model that produces answers with mistakes injected at chosen rates, used here to practise testing offline. Its rates are illustrative, not measurements.

---

## Summary

- Three testing jobs: the **validator**, **one output**, and the **agent** across inputs and runs. Today was the third.
- **One run proves little**: a 25% failure habit hides in 75% of single runs and 42% of three-run checks.
- **Test your test data first**: validating the reference answers found P03 and P05 breaking R3; both were revised (revision 2, contract still 1.0.0).
- The **eval suite** = sample pairs + full validator + **property checks** + many **seeded** runs + a **scorecard**. Q3 stays with humans.
- The **simulated model** injects mistakes at chosen, illustrative rates; seeding gives reproducible numbers and a fair **paired comparison**.
- **Baseline v1.0.0: 58%**; main causes dropped AC coverage (R3/R6), invented AC IDs (R2) and vague results (Q2).
- **v1.1.0** adds three targeted, testable rules plus the F-02 status decision; MINOR version, changelog with evidence, `agent_v1.1.0.json`.
- **Re-evaluation: 85%**, no regressions. Fenced JSON and over-limit output stay behind the validation gate until Week 9.
- Make the **refinement loop** a habit: same suite, one change at a time, keep old versions, turn real failures into pairs.

---

## Additional Resources

- OpenAI API documentation, *Evaluation best practices* (how to design evals for LLM applications, avoid "vibe-based" evaluation and evaluate continuously): https://developers.openai.com/api/docs/guides/evaluation-best-practices
- Hamel Husain, *Your AI Product Needs Evals* (2024; a practitioner's guide to unit-test-style checks, looking at your data and iterating on an AI product): https://hamel.dev/blog/posts/evals/
