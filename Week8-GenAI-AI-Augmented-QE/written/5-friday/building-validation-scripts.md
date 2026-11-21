# Building Validation Scripts

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the difference between a validation **function**, a validation **script** and a **test suite for the validator**, and say who uses each one: a tester at the terminal, the agent runner, or a CI pipeline.
- Design a **command-line interface** (CLI) before writing code: arguments, modes, output formats and an **exit-code contract** (`0` = all valid, `1` = at least one output is bad, `2` = the check could not run).
- Explain why "the output is bad" and "the check could not run" must produce **different** exit codes, and why errors go to **stderr** while reports go to **stdout**.
- Read `validate_output.py` line by line: `argparse` with a **mutually exclusive required group**, `store_true`, `metavar`, `parser.error`, pairing files by name, the `try`/`except` block that separates "unusable" from "failed", **strict mode**, and a **JSON report** built with `dataclasses.asdict`.
- Use the `main(argv=None) -> int` plus `sys.exit(main())` pattern, and explain why it makes a CLI **testable**.
- **Test the validator itself** with pytest: a false-positive guard, a parametrized list of planted defects, and assertions on the *exact* set of rules that fire.
- Test the CLI with `main([...])`, pytest's `capsys` fixture and `tmp_path`.
- Run the tests and the validator automatically in **GitHub Actions** on every pull request.
---

## Why This Matters

In the previous lesson, *Agent output validation*, you built `validate_reply()`: a function that takes one input story and one raw model reply and returns a `ValidationReport` with findings (`S1`, `R1`-`R6`, `Q1`-`Q2`) and a verdict (`PASS`, `PASS_WITH_WARNINGS` or `FAIL`). That function is the brain of validation. But a function on its own helps nobody until something **calls** it.

Think about who needs to check TestCaseDesigner's output this week:

- **You, the tester**, sitting at a terminal after a run, asking "is this reply OK, and if not, why?"
- **The agent runner** you will build later today, which executes the agent over a whole backlog and needs a yes/no per story.
- **The CI pipeline** of your Project 2 repository, which must block a pull request if someone commits a broken sample reply, a broken schema or a broken rule.

Each of these "users" needs something slightly different. A human wants readable text. A pipeline wants a **number** (the exit code) it can act on, and often a **file** (JSON) it can store or display. A good validation script gives all three from the same code, so the human and the pipeline never disagree about what "valid" means.

There is a second reason this matters. A validator is itself software, and software has bugs. A validator that passes bad output, or fails good output, quickly does more harm than good. So in this lesson you will also **test the validator**, exactly as you would test any other QA tool.

This is the "validation scripts" part of the **Weekly Epic**: *design and build their first QA agent with IO contracts and validation scripts*. In **Project 2 (Test Automation Framework)** for the e-commerce app, the script you build today is the gate between "an AI suggested some test cases" and "these test cases are allowed into the repository".

> **Scope note.** This lesson turns the existing `validate_reply()` function into a command-line tool, tests that tool, and runs it in CI. It does **not** re-teach the validation rules themselves (that was *Agent output validation*). Running the agent over a real backlog is the next lesson, *Executing agents against QA requirements*, and measuring and improving the agent over many runs is *Agent testing and refinement*, both later today. Automatically **retrying** a model when its reply fails validation is covered in **Week 9**; using one model to grade another (**LLM-as-judge**) is covered in **Week 10**.

---

## The Concept

### 1. Function, Script, Test Suite: Three Layers

It helps to separate three things that are easy to blur together:

| Layer | File | What it does | Who uses it |
|---|---|---|---|
| **Validation function** | `tcd/validation.py` (`validate_reply`) | Applies the rules to one reply and returns a report object | Other Python code |
| **Validation script** | `validate_output.py` | Reads files, calls the function, prints a report, writes JSON, returns an exit code | Humans at a terminal, the runner, CI |
| **Tests for the validator** | `tests/test_validation.py`, `tests/test_cli.py` | Prove the function and the script behave correctly | Developers and CI |

An analogy: the validation function is a **thermometer's sensor**. The script is the **display and the alarm**: it shows a number a person can read, and it beeps (exit code) so a machine can react. The tests are the **calibration certificate**: proof that the sensor reads 100 °C in boiling water and 0 °C in ice. Without calibration, nobody should trust the display.

Keeping the layers separate means the rules live in **one** place (the script only calls `validate_reply()`), the runner can import the function without any command-line parsing, and each layer is tested on its own: rule logic in `test_validation.py`, command-line behaviour in `test_cli.py`.

### 2. Design the Interface Before Writing Code

A command-line tool has an interface just like an API: its **arguments**, its **output** and its **exit code**. Testers know that an interface you never wrote down is an interface you cannot test. So we write the spec first.

#### 2.1 What the script must support

**Single mode.** Check one reply against one story. Typical use: a tester investigating one result.

```bash
python validate_output.py --story examples/US-205.input.json --reply examples/US-205.reply.txt
```

**Batch mode.** Check every reply in a folder. The folder contains pairs of files that share a **stem** (the part of the name before the extensions): `US-205.input.json` (the story the agent received) and `US-205.reply.txt` (the raw text the model returned).

```bash
python validate_output.py --run examples
```

**Options** that work in both modes:

- `--strict`: treat warnings (`PASS_WITH_WARNINGS`) as failures. Useful in CI when the team has agreed that no Q-rule warnings may be merged.
- `--json FILE`: also write a machine-readable report to `FILE`.

Notice why the story is a separate input in both modes. The rules R1-R5 compare the reply **with the input** (does `story_id` match, do the AC IDs exist, is `max_cases` respected?). A reply on its own cannot be fully validated, so every reply must travel with its story.

#### 2.2 The exit-code contract

Every program that finishes returns a small integer to whatever started it: the **exit code** (also called exit status or return code). By long-standing convention `0` means success and anything else means "something is wrong". Shells, `make`, pytest and CI systems all read it. In a terminal you can see the last command's exit code with `echo $?` (bash/zsh) or `echo $LASTEXITCODE` (PowerShell).

Our contract has three values:

| Exit code | Name in the code | Meaning | What the caller should do |
|---|---|---|---|
| `0` | `EXIT_OK` | Every reply checked; none failed | Continue (merge the PR, accept the run) |
| `1` | `EXIT_FAILED` | Every reply checked; **at least one is bad** | Look at the report; fix the agent, the reply or the rule |
| `2` | `EXIT_UNUSABLE` | The check **could not run** (missing file, broken story, bad arguments, nothing to check) | Fix the command or the files; the agent has not been judged at all |

Why insist on separating `1` and `2`? Imagine a CI job that only knows "zero or not zero". One morning it goes red. Was the agent's output bad, or did someone rename a folder so the validator found nothing to read? Those need completely different people and fixes. With separate codes, a pipeline (or a dashboard) can say "3 replies failed validation" versus "validator misconfigured", and nobody wastes an hour reading agent output that was never checked.

There is an even more dangerous case: a validator that finds **no files** and reports "0 checked, 0 failed" with exit code `0`. That is a **silent pass**: the pipeline is green, yet nothing was validated. Our contract makes "nothing to check" an exit `2`, never a `0`.

#### 2.3 stdout versus stderr

Every program has two output streams:

- **stdout** (standard output): the program's **results**. Our report goes here.
- **stderr** (standard error): **diagnostics** about the program itself: "cannot read file", "bad arguments".

Keeping them separate means a user can redirect the report to a file (`python validate_output.py --run examples > report.txt`) and still see error messages on screen, and a test can check that an unusable run printed **nothing** to stdout. Rule of thumb: if the message is about the **agent's output**, it is stdout; if it is about **the validator's ability to run**, it is stderr.

### 3. Setup

You need Python 3.11 or newer and two packages:

```bash
pip install "jsonschema>=4.18" pytest
```

> Some machines still have `jsonschema` 3.2, which has no `Draft202012Validator`. Check with `python -c "import importlib.metadata as m; print(m.version('jsonschema'))"` and upgrade if needed.

Work in the `tcd_agent/` project you have been building today. By now it contains `schemas/`, `samples/`, `tcd/contract.py` (input gate and output schema check) and `tcd/validation.py` (`validate_reply`). All commands in this lesson are run **from the project folder**.

#### 3.1 A hand-made examples folder

Batch mode reads a folder of `X.input.json` + `X.reply.txt` pairs. Later today, the runner you build in *Executing agents against QA requirements* writes exactly this layout into `runs/<run-id>/`. Since we do not have a runner yet, create a small `examples/` folder by hand with four pairs:

| Stem | Story | Reply | What it should show |
|---|---|---|---|
| `US-205` | P01 coupon story (`max_cases` 6) | P01's reviewed expected output | A clean `PASS` |
| `US-101` | P02 lockout story (one AC) | P02's output, but `expected_result` changed to `"Lockout works as expected"` | A `Q2` warning |
| `US-412` | Product search, AC1 and AC2 only | Two test cases; the second traces to a non-existent `AC3` | `R2`/`R3` errors |
| `US-450` | Add to cart, AC1 only | `"Sure! Here are the test cases:"` followed by fenced JSON | An `S1` parse error |

The story files are ordinary input-contract JSON. For example `examples/US-412.input.json`:

```json
{
  "story_id": "US-412",
  "title": "Search products by keyword",
  "acceptance_criteria": [
    {"id": "AC1", "text": "Searching for a keyword lists every product whose name contains that keyword."},
    {"id": "AC2", "text": "A search with no matches shows \"No products found\"."}
  ]
}
```

Reply files (US-450's starts with `Sure! Here are the test cases:` and a ```` ```json ```` fence) are **plain text**, not JSON, on purpose: the validator must see exactly what the model returned, including any prose or fences, so the parse step (part of rule `S1`) can judge it.

### 4. Walking Through `validate_output.py`

Here is the complete script, split into four parts. Read each part, then the explanation under it.

#### 4.1 Docstring, imports and exit codes

```python
# validate_output.py
"""Command-line validator for TestCaseDesigner replies.

Single:  python validate_output.py --story story.json --reply reply.txt
Batch:   python validate_output.py --run runs/demo      (pairs X.input.json with X.reply.txt)
Exit codes: 0 = all valid, 1 = at least one reply failed, 2 = the check itself could not run.
"""
import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from tcd.contract import ContractError, check_input
from tcd.validation import validate_reply

EXIT_OK, EXIT_FAILED, EXIT_UNUSABLE = 0, 1, 2
```

- **The docstring is the user manual.** It shows both modes and the exit-code contract from Section 2. Anyone who opens the file sees how to use it in five lines. Put the contract in the code, not only in a wiki.
- **`argparse`** parses command-line arguments; **`sys`** gives us `sys.exit` and `sys.stderr`; **`asdict`** turns a dataclass (our `Finding`) into a plain dictionary for JSON.
- **The script imports, it does not re-implement.** `check_input` (the input gate from *Implementing IO contracts*) and `validate_reply` (from *Agent output validation*) do the real work.
- **`EXIT_OK, EXIT_FAILED, EXIT_UNUSABLE = 0, 1, 2`** gives the magic numbers names. `return EXIT_UNUSABLE` explains itself; `return 2` does not. Tests can import these names too, so if a value ever changed, tests would follow.

#### 4.2 Pairing stories with replies

```python
def load_pairs(args) -> list:
    """Return [(story_dict, reply_path), ...] for single or batch mode."""
    if args.story:
        story = json.loads(Path(args.story).read_text(encoding="utf-8"))
        return [(story, Path(args.reply))]
    pairs = []
    for input_path in sorted(Path(args.run).glob("*.input.json")):
        reply_path = input_path.with_name(input_path.name.replace(".input.json", ".reply.txt"))
        story = json.loads(input_path.read_text(encoding="utf-8"))
        pairs.append((story, reply_path))              # a missing reply -> OSError later
    return pairs
```

Both modes produce the **same shape**: a list of `(story, reply_path)` tuples. Everything after this function is identical for one reply or a hundred. This is a common design trick: normalise different inputs into one shape as early as possible.

- **Single mode** reads the story JSON and wraps it in a one-item list. The reply is kept as a **path**, not read yet.
- **Batch mode** uses `Path(args.run).glob("*.input.json")` to find every story file in the folder. `glob` uses shell-style wildcards: `*` matches any characters.
- **`sorted(...)`** matters more than it looks. `glob` returns files in whatever order the operating system lists them, which can differ between Windows, macOS and Linux. Sorting makes the report order **deterministic**, so two runs on two machines print identical reports and tests can compare them.
- **`input_path.with_name(...)`** builds the matching reply path in the same folder: `examples/US-205.input.json` → `examples/US-205.reply.txt`. `with_name` replaces only the file name, keeping the folder.
- The comment says what happens if a reply file is **missing**: nothing yet. The error appears when the file is read in `main()`, where it is caught and reported as "could not run". We will see that path in Section 5.

#### 4.3 Parsing arguments

```python
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate TestCaseDesigner replies.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--story", help="input story JSON (single mode, needs --reply)")
    mode.add_argument("--run", help="folder of X.input.json + X.reply.txt files (batch mode)")
    parser.add_argument("--reply", help="raw reply text file (single mode)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--json", metavar="FILE", help="also write a machine-readable report")
    args = parser.parse_args(argv)
    if args.story and not args.reply:
        parser.error("--story needs --reply")           # argparse exits with code 2
```

Line by line:

- **`def main(argv=None) -> int:`** The whole program lives in a function that **returns** an exit code instead of calling `sys.exit` everywhere. `argv` is the list of command-line words (without the script name). When it is `None`, `parse_args(None)` reads the real command line (`sys.argv[1:]`). When a test passes a list, argparse uses that list instead. Section 6.3 shows why this is so useful.
- **`argparse.ArgumentParser(description=...)`** creates the parser. The description appears in `--help`, which argparse adds for free.
- **`add_mutually_exclusive_group(required=True)`** creates a group where **exactly one** member must be given: `--story` *or* `--run`, never both, never neither. argparse enforces this and prints a usage error if it is broken. This one line encodes the "two modes" design from Section 2.1.
- **`--reply`** is a normal optional argument. It cannot be in the group, because it must appear *together* with `--story`.
- **`action="store_true"`** makes `--strict` a **flag**: it takes no value. If present, `args.strict` is `True`; if absent, `False`.
- **`metavar="FILE"`** only changes how the help text shows the value: `--json FILE` instead of `--json JSON`. It is a small kindness that makes the usage line self-explaining.
- **`args = parser.parse_args(argv)`** returns a `Namespace` object: `args.story`, `args.run`, `args.reply`, `args.strict`, `args.json`. Dashes in option names become attribute names (`--story` → `args.story`).
- **`parser.error(...)`** handles the one rule argparse cannot express on its own ("`--story` needs `--reply`"). `parser.error` prints the usage line and the message to **stderr** and exits with code **2**, the same as any other usage error. Our cross-argument rule now behaves exactly like argparse's built-in ones.

#### 4.4 Checking, reporting and returning the exit code

```python
    try:
        pairs = load_pairs(args)
        results = []
        for story, reply_path in pairs:
            gated = check_input(story)                    # a bad story is a usage problem
            report = validate_reply(gated, reply_path.read_text(encoding="utf-8"))
            results.append((reply_path, report))
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(f"cannot validate: {exc}", file=sys.stderr)
        return EXIT_UNUSABLE
    if not results:
        print("cannot validate: no replies found", file=sys.stderr)
        return EXIT_UNUSABLE
```

This is the heart of the "1 versus 2" design.

- **`check_input(story)`** runs the input gate (rule S2) and applies contract defaults such as `max_cases` 10 and techniques EP and BVA. Why gate a story that is only being used as a reference? Because the rules depend on it: R5 needs `max_cases`, Q1 needs `techniques`. A broken story means the reply **cannot be judged fairly**, so it is a "could not run" situation, not a "reply is bad" one.
- **`reply_path.read_text(...)`** reads the raw reply text and hands it to `validate_reply`, which does parsing, schema and rules.
- **The `except` tuple lists exactly the "unusable" errors**:
  - `OSError`: a file could not be opened (missing file, wrong folder, no permission). `FileNotFoundError` is a subclass of `OSError`.
  - `json.JSONDecodeError`: a **story** file is not valid JSON. (A reply that is not valid JSON is *not* caught here: `validate_reply` turns that into an `S1` finding, because a broken reply is the agent's fault.)
  - `ContractError`: a story failed the input contract.
- Anything **not** in the tuple (say, a `KeyError` from a bug in a rule function) is deliberately **not** caught. The script crashes with a traceback, and Python exits with code `1`. That is acceptable: a bug in the validator should be loud, not disguised as a neat message.
- **`print(..., file=sys.stderr)`** sends the diagnostic to stderr, as Section 2.3 requires.
- **`if not results:`** is the anti-silent-pass guard. An empty folder, or a typo in the folder name that matches no files (`glob` on a non-existent folder just returns nothing), leads here and exits `2`.

Now the report:

```python
    failed = 0
    for reply_path, report in results:
        verdict = report.verdict
        if args.strict and verdict == "PASS_WITH_WARNINGS":
            verdict = "FAIL (strict)"
        failed += verdict.startswith("FAIL")
        print(f"{verdict:<19} {reply_path}")
        for f in report.findings:
            print(f"    {f.severity.upper():<7} {f.rule:<3} {f.where}: {f.message}")
    print(f"{len(results)} checked, {len(results) - failed} passed, {failed} failed")

    if args.json:
        payload = [{"reply": str(p), "verdict": r.verdict, "stopped_at": r.stopped_at,
                    "findings": [asdict(f) for f in r.findings]} for p, r in results]
        Path(args.json).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return EXIT_FAILED if failed else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
```

- **Strict mode** is applied **here, in the script**, not in the rules. The rules always say "this is a warning"; the *policy* of whether warnings block a merge belongs to whoever runs the check. Notice the original `report.verdict` is not changed; only the displayed verdict is.
- **`failed += verdict.startswith("FAIL")`**: `startswith` returns `True` or `False`, and in Python `True` counts as `1` when added to a number. Both `"FAIL"` and `"FAIL (strict)"` count.
- **`f"{verdict:<19}"`** left-aligns the verdict in 19 characters (the length of `PASS_WITH_WARNINGS` plus one), so the file names line up in a column. `{f.severity.upper():<7}` and `{f.rule:<3}` do the same for findings.
- The **summary line** (`4 checked, 2 passed, 2 failed`) always appears last, so a human can read the bottom line first and a test can check it with `endswith`.
- **The JSON report** is a list with one object per reply. `asdict(f)` converts each `Finding` dataclass into `{"rule": ..., "severity": ..., "where": ..., "message": ...}`. Note that the JSON keeps the **raw** verdict, not the strict one: the file records facts; strictness is a policy of that particular run. `str(p)` is needed because `Path` objects are not JSON-serialisable.
- **`return EXIT_FAILED if failed else EXIT_OK`**: the conditional expression picks `1` if any reply failed, otherwise `0`.
- **`if __name__ == "__main__": sys.exit(main())`**: `__name__` is `"__main__"` only when the file is run as a script, not when it is imported. So running `python validate_output.py ...` calls `main()` and passes its return value to `sys.exit`, which becomes the process exit code. Importing the module (as our tests will) defines `main` but runs nothing.

### 5. Running It for Real

All outputs below are from real runs on the `examples/` folder from Section 3.1.

#### 5.1 Single mode: a clean pass

```bash
python validate_output.py --story examples/US-205.input.json --reply examples/US-205.reply.txt
echo $?
```

```text
PASS                examples/US-205.reply.txt
1 checked, 1 passed, 0 failed
0
```

#### 5.2 Batch mode: a mixed folder

```bash
python validate_output.py --run examples
echo $?
```

```text
PASS_WITH_WARNINGS  examples/US-101.reply.txt
    WARNING Q2  test_cases[0].expected_result: vague phrase 'as expected'; state the exact total, message or state
PASS                examples/US-205.reply.txt
FAIL                examples/US-412.reply.txt
    ERROR   R2  test_cases[1].ac_ids: 'AC3' is not an acceptance criterion of US-412 (expected one of ['AC1', 'AC2'])
    ERROR   R3  test_cases: AC2 is not covered by any test case or open question
    WARNING Q1  test_cases: BVA was requested but no test case has type 'boundary'
FAIL                examples/US-450.reply.txt
    ERROR   S1  (reply): reply is not valid JSON: Expecting value at line 1 column 1
4 checked, 2 passed, 2 failed
1
```

Read it like a tester:

- **US-101** passes, but with a warning: "Lockout works as expected" is not an observable result. `PASS_WITH_WARNINGS` counts as passed by default.
- **US-412** has one wrong trace (`AC3` does not exist), and because of that AC2 ended up with no test case and no question. One model mistake, two rule failures: that is normal and useful, because each finding points at a different consequence. Notice also the `Q1` warning: our story file has no `techniques` field, so `check_input` applied the contract default (EP and BVA), and no boundary case was written. Defaults matter for validation, which is exactly why the script gates the story first.
- **US-450** stops at `S1`: the reply starts with "Sure!", so it is not JSON at all. No deeper rule ran, because rules need a valid shape (the "short-circuit" from the previous lesson).
- **Exit code `1`**: the check ran fine; some outputs are bad.

The examples folder was hand-made; a reply like US-450's is an **illustrative** model mistake, not output copied from a specific model.

#### 5.3 Strict mode

```bash
python validate_output.py --run examples --strict
echo $?
```

```text
FAIL (strict)       examples/US-101.reply.txt
    WARNING Q2  test_cases[0].expected_result: vague phrase 'as expected'; state the exact total, message or state
PASS                examples/US-205.reply.txt
...                 (US-412 and US-450 exactly as in 5.2)
4 checked, 1 passed, 3 failed
1
```

Only the US-101 line changed. Use `--strict` where a warning should block progress (for example, committed sample replies that are meant to be perfect) and the default mode where a human reviewer will look at warnings anyway.

#### 5.4 The JSON report

```bash
python validate_output.py --run examples --json report.json > /dev/null
echo $?
```

```text
1
```

`> /dev/null` throws away the text report (on Windows PowerShell use `> $null`); the exit code is still `1`. The beginning of `report.json`:

```json
[
  {
    "reply": "examples/US-101.reply.txt",
    "verdict": "PASS_WITH_WARNINGS",
    "stopped_at": "",
    "findings": [
      {
        "rule": "Q2",
        "severity": "warning",
        "where": "test_cases[0].expected_result",
        "message": "vague phrase 'as expected'; state the exact total, message or state"
      }
    ]
  },
  {
    "reply": "examples/US-205.reply.txt",
    "verdict": "PASS",
    "stopped_at": "",
    "findings": []
  },
```

The text report is for eyes; the JSON is for tools. A CI job can upload it as a build artifact, a dashboard can count findings per rule, and later today the runner and the evaluation script can aggregate such data across many runs. `stopped_at` is empty here; for US-450 it is `"parse"`, telling a tool that the reply never reached the schema.

#### 5.5 When the check cannot run

A forgotten `--reply`:

```bash
python validate_output.py --story examples/US-205.input.json
echo $?
```

```text
usage: validate_output.py [-h] (--story STORY | --run RUN) [--reply REPLY]
                          [--strict] [--json FILE]
validate_output.py: error: --story needs --reply
2
```

Look at the usage line: `(--story STORY | --run RUN)` in round brackets with a `|` is argparse's way of showing a required mutually exclusive group; square brackets mean optional. `[--json FILE]` shows our `metavar`.

Leaving out both `--story` and `--run` gives `error: one of the arguments --story --run is required`, also with exit code `2`.

A missing file:

```bash
python validate_output.py --story examples/US-999.input.json --reply examples/US-999.reply.txt
echo $?
```

```text
cannot validate: [Errno 2] No such file or directory: 'examples/US-999.input.json'
2
```

An empty folder (the silent-pass trap):

```bash
mkdir empty
python validate_output.py --run empty
echo $?
```

```text
cannot validate: no replies found
2
```

Run it again with `2>/dev/null` (hide stderr) and nothing is printed, yet `echo $?` still shows `2`: the exit code tells the truth even when the message is hidden.

One more: a story that breaks the input contract (P04's malformed input, saved as `bad_story.json`):

```text
cannot validate: input: 2 contract error(s)
```

The exit code is correctly `2`, but the message only says *how many* problems there are, not *which*. `ContractError` carries the details in its `.errors` list. Improving this message is Practice Exercise 2.

### 6. Testing the Validator Itself

Who tests the tester? We do. A validator has two ways to fail:

- **False negative**: a bad reply passes. The agent's mistake reaches your test suite. This is the dangerous one.
- **False positive**: a good reply fails. People learn to ignore the validator, which is how teams end up with tools that are always red and never read.

We guard against both with two kinds of test.

#### 6.1 `tests/test_validation.py`: good passes, planted defects are caught

```python
# tests/test_validation.py
"""Tests for the validator itself: it must accept good output and catch each planted defect."""
import copy
import json
from pathlib import Path

import pytest

from tcd.contract import check_input
from tcd.validation import validate_reply

PAIR = json.loads(Path("samples/P01-happy_path.json").read_text(encoding="utf-8"))
STORY = check_input(PAIR["input"])
GOOD = PAIR["expected_output"]


def mutate(change):
    """Return the reply text of a deep copy of GOOD after applying change(copy)."""
    out = copy.deepcopy(GOOD)
    change(out)
    return json.dumps(out)


def test_good_output_passes_with_no_findings():
    report = validate_reply(STORY, json.dumps(GOOD))
    assert report.verdict == "PASS"
    assert report.findings == []
```

- **`PAIR`, `STORY`, `GOOD`** come from sample pair P01, the human-reviewed US-205 example from Thursday. Using a reviewed pair as the "known good" baseline is important: if the baseline came from the agent, we would be testing the validator against something nobody checked.
- **`test_good_output_passes_with_no_findings`** is the **false-positive guard**. It asserts `findings == []` as well as `verdict == "PASS"`. The verdict alone is a summary; asserting "no findings at all" is the strictest possible statement about good output, and it fails with a clear diff showing exactly which finding appeared if a rule ever becomes too eager.
- **`mutate(change)`** is a small helper. `copy.deepcopy(GOOD)` makes a completely independent copy, including the nested lists and dictionaries (a plain `GOOD.copy()` would share the inner `test_cases` list, and one test's mutation would leak into the next). `change(out)` applies a small edit, and `json.dumps` turns the result back into reply **text**, because `validate_reply` takes text, just like the real model's reply.

Now the planted defects:

```python
# (description, reply text, the ONE rule we expect to fire)
PLANTED = [
    ("fenced JSON",        "```json\n" + json.dumps(GOOD) + "\n```",                                  "S1"),
    ("prose before JSON",  "Here are your tests: " + json.dumps(GOOD),                                  "S1"),
    ("bad enum",           mutate(lambda o: o["test_cases"][0].update(priority="urgent")),             "S1"),
    ("wrong story",        mutate(lambda o: o.update(story_id="US-101")),                              "R1"),
    ("invented AC",        mutate(lambda o: o["test_cases"][0].update(ac_ids=["AC1", "AC9"])),         "R2"),
    ("AC4 forgotten",      mutate(lambda o: o.update(open_questions=[])),                              "R3"),
    ("id from example",    mutate(lambda o: o["test_cases"][2].update(id="TC-101-03")),                "R4"),
    ("too many cases",     mutate(lambda o: o["test_cases"].extend(
        [dict(o["test_cases"][2], id=f"TC-205-{n:02d}") for n in range(4, 8)])),                       "R5"),
    ("ok but empty",       mutate(lambda o: o.update(test_cases=[],
        open_questions=["AC1, AC2, AC3 and AC4: are these final?"])),                                  "R6"),
    ("no boundary case",   mutate(lambda o: [tc.update(type="positive") for tc in o["test_cases"]]),   "Q1"),
    ("vague result",       mutate(lambda o: o["test_cases"][0].update(expected_result="Discount works as expected")), "Q2"),
]


@pytest.mark.parametrize("name, reply, rule", PLANTED, ids=[p[0] for p in PLANTED])
def test_each_planted_defect_is_caught_by_its_rule(name, reply, rule):
    report = validate_reply(STORY, reply)
    fired = {f.rule for f in report.findings}
    assert fired == {rule}, f"{name}: expected only {rule}, got {sorted(fired)}"
```

- **`PLANTED`** is a table: each row is one realistic mistake, the reply text containing it, and the rule that should catch it. There is at least one row per rule in the catalogue (S1 three times, because parsing and schema both live under S1). Reading the table is like reading a test-design document: each row is a test case.
- **`lambda o: ...`** is a tiny anonymous function. `lambda o: o.update(story_id="US-101")` means "given `o`, call `o.update(story_id="US-101")`". `dict.update(key=value)` changes one key in place. In "no boundary case" the lambda uses a list comprehension purely for its side effect of updating each test case; that is a compact trick, acceptable in a test table.
- **`"too many cases"`** extends the list with four copies of the third case, each with a fresh ID (`TC-205-04` to `TC-205-07`). `dict(old, id=new)` builds a new dictionary from `old` with one key replaced. `f"{n:02d}"` pads the number to two digits. The fresh IDs matter: copies with the *same* ID would also trigger R4, which is not what this row is testing. 3 + 4 = 7 cases against `max_cases` 6 fires R5 alone.
- **`@pytest.mark.parametrize("name, reply, rule", PLANTED, ...)`** tells pytest to run the test once per row, passing the row's values as arguments. `ids=[p[0] for p in PLANTED]` gives each run a readable name, so a failure says `[invented AC]` instead of `[reply6-R2]`.
- **`fired = {f.rule for f in report.findings}`** is a **set comprehension**: the set of rule IDs that fired.
- **`assert fired == {rule}`** checks the **exact** set, not just "the rule is in there". This is stricter than `assert rule in fired`, and the stricter version is the point: it catches a defect that triggers the right rule *plus* an unexpected one, which usually means a rule is too broad.

#### 6.2 When a planted defect fires two rules

The exact-set assertion paid off while these tests were being written. The first versions of two rows looked like this:

- **"invented AC"** replaced the first test case's `ac_ids` with `["AC9"]`.
- **"ok but empty"** only set `test_cases` to `[]`.

Running them gave:

```text
invented AC:  fired ['R2', 'R3']
ok but empty: fired ['R3', 'R6']
```

Neither result was a validator bug. Replacing `AC1` with `AC9` invents an AC (R2) **and** leaves AC1 uncovered (R3). Emptying `test_cases` makes `status: ok` inconsistent (R6) **and** leaves every AC uncovered (R3). The rules were right; the **test data** was testing two things at once.

The fix was to make each mutation **minimal**, so it breaks exactly one rule:

- "invented AC" now uses `["AC1", "AC9"]`: AC1 stays covered, only the invented AC9 is wrong.
- "ok but empty" also sets an open question that names every AC (`"AC1, AC2, AC3 and AC4: are these final?"`), so coverage (R3) is satisfied and only the status inconsistency (R6) remains.

This is the same idea as Tuesday's hand-rolled **mutation check**: deliberately inject one small fault and confirm the checker notices it. In mutation testing proper, a tool makes small changes ("mutants") to *code* and checks whether the tests "kill" them. Here we mutate the *data* (the reply) and check that the validator kills each mutant with the *right* rule. Each row of `PLANTED` is a mutant; a row that passes is a killed mutant. If someone later weakens a rule (say, R4 stops checking the story number), the "id from example" mutant survives, the test fails, and the weakening is caught before it ships.

#### 6.3 `tests/test_cli.py`: testing the script, not just the function

The function tests above never touch argparse, file reading, exit codes or stderr. Those are separate behaviours with separate bugs, so they get separate tests. This is where `main(argv=None) -> int` pays off: a test can call `main([...])` like any function and look at the returned number. No subprocess, no shell.

```python
# tests/test_cli.py
"""Tests for the command-line tool: exit codes and what the user sees."""
import json

import pytest

from validate_output import EXIT_FAILED, EXIT_OK, EXIT_UNUSABLE, main


def test_single_good_reply_exits_0(capsys):
    code = main(["--story", "examples/US-205.input.json", "--reply", "examples/US-205.reply.txt"])
    assert code == EXIT_OK
    assert "1 checked, 1 passed, 0 failed" in capsys.readouterr().out


def test_batch_with_failures_exits_1(capsys):
    code = main(["--run", "examples"])
    out = capsys.readouterr().out
    assert code == EXIT_FAILED
    assert "ERROR   R2" in out
    assert out.strip().endswith("4 checked, 2 passed, 2 failed")


def test_strict_turns_warnings_into_failures(capsys):
    main(["--run", "examples", "--strict"])
    assert "FAIL (strict)       examples/US-101.reply.txt" in capsys.readouterr().out


def test_json_report_is_written(tmp_path):
    report_file = tmp_path / "report.json"
    main(["--run", "examples", "--json", str(report_file)])
    report = json.loads(report_file.read_text(encoding="utf-8"))
    assert [r["verdict"] for r in report] == ["PASS_WITH_WARNINGS", "PASS", "FAIL", "FAIL"]


def test_missing_file_exits_2_and_says_why_on_stderr(capsys):
    code = main(["--story", "examples/nope.input.json", "--reply", "examples/nope.reply.txt"])
    captured = capsys.readouterr()
    assert code == EXIT_UNUSABLE
    assert captured.out == ""
    assert "cannot validate" in captured.err


def test_empty_folder_is_not_a_silent_pass(tmp_path):
    assert main(["--run", str(tmp_path)]) == EXIT_UNUSABLE


def test_usage_error_exits_2():
    with pytest.raises(SystemExit) as exc_info:
        main(["--story", "examples/US-205.input.json"])        # forgot --reply
    assert exc_info.value.code == 2
```

New pytest tools in this file:

- **`capsys`** is a built-in pytest **fixture**: name it as a test parameter and pytest captures everything printed to stdout and stderr during the test. `capsys.readouterr()` returns an object with `.out` and `.err`. This lets us assert on what a user would see, and prove that the "missing file" case printed nothing to stdout and its explanation to stderr.
- **`tmp_path`** is another built-in fixture: a fresh, empty temporary folder (a `Path`) unique to each test. It is perfect for "empty folder" and "write a report somewhere" tests, and pytest cleans it up for you, so tests never litter the project.
- **`pytest.raises(SystemExit)`**: `parser.error` does not *return* `2`; it calls `sys.exit(2)`, which raises a `SystemExit` exception. `pytest.raises` catches it, and `exc_info.value.code` is the exit code it carried.
- **`out.strip().endswith(...)`** pins the summary line to the very end of the output.
- **`[r["verdict"] for r in report]`** checks the JSON report's verdicts in order. This only works because `load_pairs` sorts the files; without sorting the order could change between machines and this test would be flaky.

#### 6.4 Run the whole suite

```bash
python -m pytest -v tests/
```

```text
collecting ... collected 19 items

tests/test_cli.py::test_single_good_reply_exits_0 PASSED                 [  5%]
tests/test_cli.py::test_batch_with_failures_exits_1 PASSED               [ 10%]
tests/test_cli.py::test_strict_turns_warnings_into_failures PASSED       [ 15%]
tests/test_cli.py::test_json_report_is_written PASSED                    [ 21%]
tests/test_cli.py::test_missing_file_exits_2_and_says_why_on_stderr PASSED [ 26%]
tests/test_cli.py::test_empty_folder_is_not_a_silent_pass PASSED         [ 31%]
tests/test_cli.py::test_usage_error_exits_2 PASSED                       [ 36%]
tests/test_validation.py::test_good_output_passes_with_no_findings PASSED [ 42%]
tests/test_validation.py::test_each_planted_defect_is_caught_by_its_rule[fenced JSON] PASSED [ 47%]
tests/test_validation.py::test_each_planted_defect_is_caught_by_its_rule[prose before JSON] PASSED [ 52%]
tests/test_validation.py::test_each_planted_defect_is_caught_by_its_rule[bad enum] PASSED [ 57%]
tests/test_validation.py::test_each_planted_defect_is_caught_by_its_rule[wrong story] PASSED [ 63%]
tests/test_validation.py::test_each_planted_defect_is_caught_by_its_rule[invented AC] PASSED [ 68%]
tests/test_validation.py::test_each_planted_defect_is_caught_by_its_rule[AC4 forgotten] PASSED [ 73%]
tests/test_validation.py::test_each_planted_defect_is_caught_by_its_rule[id from example] PASSED [ 78%]
tests/test_validation.py::test_each_planted_defect_is_caught_by_its_rule[too many cases] PASSED [ 84%]
tests/test_validation.py::test_each_planted_defect_is_caught_by_its_rule[ok but empty] PASSED [ 89%]
tests/test_validation.py::test_each_planted_defect_is_caught_by_its_rule[no boundary case] PASSED [ 94%]
tests/test_validation.py::test_each_planted_defect_is_caught_by_its_rule[vague result] PASSED [100%]

============================== 19 passed in 0.21s ==============================
```

Nineteen tests, no model calls.

> Run pytest **from the project folder**: the tests open `samples/...` and `examples/...` with relative paths, and `python -m pytest` adds the current folder to Python's import path so `import validate_output` and `import tcd` work.

### 7. Running It in CI

**Continuous integration (CI)** means every push or pull request triggers an automatic job that builds and checks the project. In Project 2 you will use it for your pytest suite; the agent's checks belong there too. Here is a GitHub Actions workflow, saved as `.github/workflows/agent-checks.yml`:

```yaml
name: agent-checks

on:
  pull_request:
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install "jsonschema>=4.18" pytest
      - name: Test the validator
        run: python -m pytest -q tests/
      - name: Validate committed sample replies
        run: python validate_output.py --run examples --strict --json validation-report.json
```

Key by key:

- **`name`**: the workflow's display name in the GitHub "Actions" tab.
- **`on`**: the **triggers**. `pull_request` runs the job for every PR (so problems are caught before merging); `push` to `main` runs it again after merging.
- **`jobs` → `validate`**: one job, named `validate`. **`runs-on: ubuntu-latest`** asks GitHub for a fresh Linux virtual machine.
- **`steps`** run in order; if one fails (non-zero exit code), later steps are skipped and the job is red.
  - **`actions/checkout@v6`** copies your repository into the machine.
  - **`actions/setup-python@v5`** installs the Python version given under `with:`. Quote the version (`"3.12"`); unquoted, YAML would read `3.10` as the number `3.1`.
  - **`run:`** executes a shell command. First install dependencies, then run the tests, then run the validator.
- **The exit-code contract does the rest.** The validator step exits `1` if a committed reply fails (or, with `--strict`, has warnings) and `2` if the folder is missing. Both turn the job red, but the log shows which one: "3 failed" versus "cannot validate: no replies found".

Note the order: **test the validator before trusting it**. If the validator's own tests fail, its verdict on the samples means nothing.

Which folder should CI validate? In this lesson, `examples/` contains replies that are **meant to fail**, so this exact workflow would be permanently red. In a real repository, point the step at a folder of replies you **expect to pass**: for example, reviewed reference replies kept next to your sample pairs. A deliberately-bad folder belongs in the **tests** (as `tests/test_cli.py` does), not in the gate.

**What CI should not do.** It should not call a live model on every pull request. Live calls cost money, are slow, need a secret API key in the pipeline, and give different answers each time, so a PR could go red because of the model's mood rather than the code change. CI checks things that are **deterministic**: the validator's tests, the schemas, the templates, committed sample replies. Running the real agent and measuring it is a separate, deliberate activity, covered later today in *Executing agents against QA requirements* and *Agent testing and refinement*.

### 8. Script Hygiene

Small habits make the difference between a script people trust and one they work around:

1. **Deterministic output.** Same inputs, same report, byte for byte. We sort file lists and keep findings in rule order. Non-deterministic output produces flaky tests and confusing diffs.
2. **Messages a stranger can act on.** "`R2 test_cases[1].ac_ids: 'AC3' is not an acceptance criterion of US-412 (expected one of ['AC1', 'AC2'])`" says what, where, and what was expected. "Validation error" says nothing. (Thursday's lesson on error messages applies to the script's own messages too.)
3. **No silent passes.** "0 checked" is never success. Exit `2` when nothing was found.
4. **Separate policy from rules.** Strictness is a command-line choice; the rules never change their severity based on who is running them.
5. **Fail loudly on your own bugs.** Catch only the errors you expect ("unusable" inputs). Let real bugs crash with a traceback.
6. **Say what version checked the output.** When a reply was accepted three weeks ago and someone asks "which rules were in force?", you want an answer: add a `--version` flag (Practice Exercise 3).
7. **A usage block in the README.** Copy the docstring's usage lines and exit-code table into the project README so people never have to open the code to use the tool.

---

## Practice Exercises

1. **Add a fifth example.** Create `examples/US-460.input.json` (a "Remove item from cart" story with two ACs) and a reply that breaks **only** R4 (one test case ID uses `TC-205-`). Run batch mode and confirm the summary now reads `5 checked, 2 passed, 3 failed`. Then update `test_batch_with_failures_exits_1` and `test_json_report_is_written` so they pass again. What does having to edit those tests tell you about using shared example folders in tests?
2. **Show which input rules failed.** When a story breaks the input contract, the script prints `cannot validate: input: 2 contract error(s)`. Change the `except` block so that, for a `ContractError`, it also prints each entry of `exc.errors` on its own line (still to stderr, still exit `2`). Add a test using P04's malformed input that asserts `"does not match"` appears in `captured.err`.
3. **Record versions.** Add a `--version` option using `parser.add_argument("--version", action="version", version="validate_output 1.0.0 (contract 1.0.0)")`. Run it and check its exit code. (Hint: argparse exits with `0` after printing the version.) Then add a `"contract_version"` key to every object in the JSON report.
4. **Find a weak rule with a mutant.** Add a `PLANTED` row where `expected_result` is `"Total is correct"`. Run the tests. Does Q2 catch it? Why (look at the phrase list in `tcd/validation.py`)? Decide whether this is a validator gap worth fixing or a false-positive risk, and write one sentence justifying your choice.
---

## Knowledge Check

1. What is the difference between exit code `1` and exit code `2` in our contract, and why should a pipeline care?
2. Why does the script send "cannot validate: ..." to stderr but the PASS/FAIL report to stdout?
3. Why does `main()` take an `argv` parameter and *return* an int instead of calling `sys.exit` itself?
4. In `load_pairs`, what would go wrong if the `sorted(...)` call were removed?
5. Why is a malformed **story** file treated as "unusable" (exit `2`), while a malformed **reply** is a `FAIL` (exit `1`)?
6. Why does `test_each_planted_defect_is_caught_by_its_rule` assert `fired == {rule}` rather than `rule in fired`?
7. The first version of the "ok but empty" mutant fired R3 and R6. Was that a validator bug? How was the row fixed?
<details>
<summary>Answers</summary>

1. `1` means every reply was checked and at least one is bad: look at the agent's output. `2` means the check could not run (bad arguments, missing or broken files, nothing found): the output has not been judged at all, so fix the setup. A pipeline that cannot tell them apart sends people to debug the wrong thing, and might even treat "nothing checked" as success.
2. Results go to stdout and diagnostics to stderr, so a user can redirect the report to a file while still seeing problems, and tools or tests can check that an unusable run produced no report.
3. So tests can call `main([...])` directly with any arguments and inspect the returned exit code, without starting a subprocess. When run as a script, `sys.exit(main())` turns the returned value into the process exit code.
4. `glob` returns files in an operating-system-dependent order, so the report order (and the JSON report's order) could differ between machines and runs. Tests that compare the order, like `test_json_report_is_written`, would become flaky.
5. The story is the reference the reply is judged against; rules R1-R5 and Q1 depend on it. If it is broken, the reply cannot be judged fairly, so the check itself cannot run. A broken reply is the agent's mistake, which is precisely what the validator exists to report.
6. The exact-set assertion also catches a defect that triggers the right rule *plus* an unexpected one, which usually means a rule is too broad or the test data tests two things at once. It makes each row prove one specific rule.
7. No. Emptying `test_cases` both breaks R6 (status `ok` with no cases) and leaves every AC uncovered (R3); both rules were right. The row was made minimal by adding an open question naming every AC, so only R6 fires.
</details>

---

## Glossary

- **CLI (command-line interface):** the arguments, output and exit code through which a program is used from a terminal or a script.
- **Exit code (exit status):** the integer a finished program returns to its caller; `0` means success by convention.
- **Exit-code contract:** a documented meaning for each exit code a tool can return (here `0`, `1`, `2`).
- **stdout / stderr:** the two output streams of a program: results versus diagnostics.
- **Silent pass:** a check that reports success even though it checked nothing.
- **Mutually exclusive group (argparse):** a set of options of which at most one (or, with `required=True`, exactly one) may be given.
- **Strict mode:** a policy option that treats warnings as failures.
- **False positive / false negative (for a validator):** good output rejected / bad output accepted.
- **Mutant:** a deliberately injected small defect used to prove a checker notices it.
- **`capsys`, `tmp_path`:** built-in pytest fixtures that capture printed output and provide a fresh temporary folder.
- **CI (continuous integration):** automatically building and checking a project on every push or pull request.
- **Workflow (GitHub Actions):** a YAML file in `.github/workflows/` describing triggers, jobs and steps.

---

## Summary

- A validation **function** holds the rules; a validation **script** makes them usable by people, the runner and CI; **tests** prove both are trustworthy. Keep the rules in one place and have the script call them.
- Design the interface first: single and batch modes, `--strict`, `--json`, and an **exit-code contract** where `0` = all valid, `1` = some output bad, `2` = the check could not run. Never let "nothing checked" look like success.
- Reports go to **stdout**, diagnostics to **stderr**.
- `validate_output.py` uses argparse's **required mutually exclusive group** for the two modes, `parser.error` for the cross-argument rule, a narrow `except` for "unusable" inputs, sorted file pairing for deterministic output, strict mode as a policy layer, and `dataclasses.asdict` for the JSON report.
- The **`main(argv=None) -> int` + `sys.exit(main())`** pattern makes the CLI testable as an ordinary function.
- Test the validator with a **false-positive guard** (good output, zero findings) and a parametrized table of **planted defects**, asserting the **exact** rule set; keep each mutant minimal. Test the CLI with `main([...])`, `capsys`, `tmp_path` and `pytest.raises(SystemExit)`.
- In **CI**, test the validator first, then validate committed replies that are expected to pass. Keep live model calls out of every-PR checks.
---

## Additional Resources

- Python documentation, *Argparse Tutorial* (a gentle, official introduction to positional and optional arguments, `store_true`, choices and mutually exclusive groups): https://docs.python.org/3/howto/argparse.html
- pytest documentation, *How to parametrize fixtures and test functions* (official guide to `@pytest.mark.parametrize`, including `ids` for readable test names): https://docs.pytest.org/en/stable/how-to/parametrize.html
- GitHub Docs, *Building and testing Python* (official tutorial for running Python tests in GitHub Actions with `actions/setup-python`, including caching and uploading artifacts): https://docs.github.com/en/actions/tutorials/build-and-test-code/python
