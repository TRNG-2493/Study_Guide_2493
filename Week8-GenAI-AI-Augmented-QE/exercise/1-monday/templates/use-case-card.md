# Use-Case Cards

Fill in one card per selected use case (three in total, in ranked order). Copy the card block below twice more.

---

## Use case 1: <short name>

| Field | Your answer |
|---|---|
| ShopFront part (page, flow, layer or pipeline step) | |
| STLC activity | |
| Pain point it addresses (brief section 3, number) | |
| What Claude produces (the exact artefact: a list, a CSV, a test file, a summary) | |
| Value (what gets faster or better, and for whom) | |
| Why GenAI beats No AI and classic ML/NLP here (one sentence) | |
| Who verifies the output (a role, not "someone") | |
| How they verify it (the concrete check, and how long it takes) | |
| What could go wrong (at least 2 failure modes) | |
| Mechanism behind each failure mode (hallucination, non-determinism, knowledge cut-off, context window, no access to your context, sensitivity to wording, counting errors) | |
| Data sensitivity (what must never go in the prompt, and how the team prevents it) | |
| Scores (value / frequency / verifiability / risk / sensitivity) and total | |
| Evidence from Stage 5 (prompt ids, what Claude got right, what you corrected) | |
| Source(s) (research-log row) | |
| How the team would know it is working after a month (one measure) | |

---

## Ranking decision

- Final order:
- Does it match `rank_use_cases.py`? If not, why did you override it?

## Claude challenge (Stage 6)

Paste the critique prompt id from your evidence log, then decide on each point Claude raised.

| # | Claude's critique (short quote) | Accept / Reject | Reason |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
