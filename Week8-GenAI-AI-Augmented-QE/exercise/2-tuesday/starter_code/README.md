# Starter code: ShopFront prompt library (Week 8, Tuesday)

```
pip install -r requirements.txt
python -m pytest -q                 # expect: 1 failed, 4 passed, 1 skipped (intended)
python tools/score_reply.py evidence/calibration/reply_good.txt   # runs; prints a CHECK line until you add criteria
```

| Path | What it is | Edit? |
|---|---|---|
| `shopfront/shipping.py` | Code under test (correct). Requirement in the docstring. | No |
| `shopfront/shipping_buggy.py` | Same requirement, one defect (Stage 5). | Only the fix, after confirming the cause |
| `tests/test_shipping_buggy.py` | Exposes the defect: 1 failing test. | **Never** |
| `tests/test_shipping_generated.py` | Runs Claude's format-locked cases (`--cases`). | No |
| `tools/lint_prompt.py` | Specificity linter for prompt files (input check). | No |
| `tools/score_reply.py` | Your acceptance criteria for TD-1 replies (output check). | Yes: Stage 1 |
| `tools/load_shipping_cases.py` | Defensive loader for TD-2 replies. | Yes: `validate_cases()` in Stage 3 |
| `tools/check_gherkin.py` | Shape, content and leakage check for TD-3. | Yes: two constants in Stage 4 |
| `tools/check_triage.py` | Contract and evidence check for DB-2 replies. | No |
| `tools/prompt_file.py` | Reads the prompt block out of a prompt file. | No |
| `materials/` | Synthetic material you may paste into Claude. | No |
| `prompts/` | Your prompt library. Start from `_TEMPLATE.md`. | Yes |
| `evidence/` | Every Claude reply, saved as it came. | Yes |
| `REFINEMENT-LOG.md` | What each change did, with numbers. | Yes |

Run every command from this folder (the one that holds `pytest.ini`).
