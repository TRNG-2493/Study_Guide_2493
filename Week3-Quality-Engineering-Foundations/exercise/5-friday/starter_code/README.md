# Starter code: Project 1 release 1.1 (optional use)

A tiny, standard-library-only Python module you can run your regression ideas against. Using it is optional; the exercise can be completed on paper. If you use it, it makes the "regression" idea real: release 1.1 changed three things, and the module may or may not still behave correctly everywhere.

## Files

| File | Purpose |
|---|---|
| `project1_release.py` | Login with lockout, partner sign-in, session timeout, promo-code validation (release 1.1 rules) |
| `tests/test_release_smoke.py` | Two worked examples and one data-driven example |
| `pytest.ini` | Registers the markers `smoke`, `regression`, `bugfix` |
| `data/login_cases_starter.csv` | Five example rows for the data-driven test |
| `load_login_local.py` | Optional local load test (see the warning below) |

## Setup and run

```bash
pip install pytest            # once
cd starter_code
pytest -v                     # everything
pytest -m smoke               # Tier 1 only
pytest -m "smoke or regression"
python load_login_local.py --users 10 --think 0.2 --ramp 2 --steady 5
```

## What to do with it

1. Read the module's rules in the comments and constants (release 1.1 rules are the ones in the Part 3 change request).
2. Write more tests from YOUR own suite as pytest functions, tag them `smoke`, `regression` or `bugfix` to match your tier table, and run each tier.
3. Extend `data/login_cases_starter.csv` towards your 12-row dataset (Part 4). Add columns only if you also update the reader in the test.
4. If a test fails, decide first: is the module wrong or is your expectation wrong? Check the rule, then log a defect note in your plan.

## Load script warning

`load_login_local.py` starts its own server on 127.0.0.1 and talks only to it. It has no option to target another host, on purpose. Never point load at a third-party site, a shared environment or any system you do not own and have permission to test. Results from this toy server say nothing about a real system; use them only to practise reading p50, p95, p99, throughput and error rate.
