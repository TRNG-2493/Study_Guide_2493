# Starter code: Registration and Login target (build 0.3.0)

A tiny Python (standard library only) implementation of the feature described in
`../templates/feature-spec-registration-login-v2.md`. You are the tester: treat it as a
black box. Do not read `registration_login.py` to find problems; design your cases from the
specification, run them, and compare actual results with your expected results.

## Files

| File | Purpose |
|---|---|
| `registration_login.py` | The product under test (the build you are testing) |
| `run_cases.py` | Run one case by hand from the command line (Part 4) |
| `test_starter.py` | pytest file with two worked examples; add your 5 automated cases (Part 5) |

## Requirements

Python 3.8 or newer. For Part 5 install pytest: `pip install pytest` (or `python -m pip install pytest`).

## Run one case by hand

From this folder:

```
python run_cases.py reset
python run_cases.py register --email a@b.com --username bob --password 'Abcdef1!' --confirm 'Abcdef1!' --terms yes
python run_cases.py login --id a@b.com --password 'Abcdef1!' --remember yes
python run_cases.py mask --password 'Abcdef1!' --visible yes
python run_cases.py show
```

* Put passwords in single quotes so your shell does not treat `!` or `$` specially (on Windows
  Command Prompt use double quotes).
* The state (registered users and failed-login counters) is saved between commands, so a
  precondition such as "user alice@example.com exists" is created by running `register` first.
  Use `reset` before each case that needs a clean start.
* Each run prints `ok`, `message` and any extra fields, then the number of registered users
  (useful to check "state unchanged").

## Run the starter tests

```
python -m pytest -v
```

Both worked examples should pass on this build. When you add your tests, a failing test
means "the build does not behave as your expected result says": decide whether that is a
product defect or a mistake in your test, then record it.
