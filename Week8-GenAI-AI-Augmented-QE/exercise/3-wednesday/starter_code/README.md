# Starter code: AI-augmented QA lifecycle for ShopFront US-420 (Week 8, Wednesday)

```
pip install -r requirements.txt
python lab.py lint                 # works now
python -m pytest -q                # expect: 5 failed (NotImplementedError: your oracle), 1 skipped
```

Run everything from this folder. Same flow and commands as the Wednesday demo's `lifecycle_lab.py`.

| Path | What it is | Edit? |
|---|---|---|
| `qa_flow/stories.py` | US-420, your manual review, PO answers, open questions, **your oracle** | Yes: Stages 1 and 2 |
| `qa_flow/reqs_review.py` | Weak-word linter, review prompt, grounding checks, question log | No |
| `qa_flow/suite_checks.py` | Test case prompt and review aids (trace matrix, pointers) | No |
| `qa_flow/review_log.py` | Sign-off gate, correction log, metrics | No |
| `qa_flow/data_checks.py` | Data prompt and independent data checks | No |
| `qa_flow/responsible.py` | Redaction, pre-flight, disclosure | Yes: the GIFT_CARD rule in Stage 6 |
| `lab.py` | Command line for every step | No |
| `shopfront/giftcard.py` | The application (correct) | No |
| `shopfront/giftcard_buggy.py` | The application with one defect | No |
| `tests/test_oracle.py` | Sanity tests for your oracle | No |
| `tests/test_suite_rows.py` | Runs a signed-off suite against the app | No |
| `materials/` | PO answers (sealed: read the rule at the top) and a raw bug note | No |
| `evidence/` | Every Claude reply, saved exactly as it came | Yes |
| `review/` | Checklist, question log, decisions, approved suite, correction log, usage log, `REVIEW.md` | Yes |
