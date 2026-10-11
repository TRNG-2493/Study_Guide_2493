# Starter Code: Project 1 - Account Membership and Promo Codes

This folder is your pair's starting repository. Copy it, then follow the main exercise README.

## Contents

| Path | Purpose |
|---|---|
| `membership.py` | The module under test (stdlib only). Treat it as a black box. |
| `tests/test_example.py` | Worked examples of the expected test format (one per technique style). |
| `tests/conftest.py` | Shared fixture (`new_account`). |
| `design/` | Placeholders for your design documents. |
| `pytest.ini`, `requirements.txt`, `.gitignore` | Tooling files. |

## Set up (once per partner machine)

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
```

You should see 5 passing test items (the BVA example runs as 3 items). Your own tests go into new files in `tests/`
(for example `test_bva_ep.py`, `test_decision_table.py`, `test_state_transition.py`).

## Rules for the module

Do not edit `membership.py` on your main branch. To try a fix, copy it to `membership_fixed_try.py` and describe the fix in `DEFECTS_FOUND.md`.
