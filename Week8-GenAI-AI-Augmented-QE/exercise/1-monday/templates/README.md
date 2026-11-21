# Templates for Monday's Exercise

Copy this whole `templates/` folder into your submission folder `week8-monday-<yourname>/` and fill the files in place. Do not rename them; the grader looks for these names.

| File | Stage | What you do with it |
|---|---|---|
| `system-brief.md` | All | Read only. The system you are proposing use cases for. |
| `materials/` | 1, 5 | Read only. Synthetic stories, code, logs and notes you may paste into Claude. |
| `candidate-longlist.md` | 1 | Your long list of candidate tasks, mapped to STLC activities. |
| `tool-choice-worksheet.md` | 2 | No AI, classic ML/NLP or GenAI for every candidate, with reasons. |
| `rank_use_cases.py` | 3 | Score your GenAI candidates and rank them. |
| `research-log.md` | 4 | Sources you found, and proof you checked each one. |
| `claude-evidence-log.md` | 5, 6 | Every Claude prompt you sent, what came back and your review of it. |
| `use-case-card.md` | 6 | One card per selected use case (copy the card three times inside the file). |
| `presentation-outline.md` | 7 | Your 5-minute talk. |

Run the ranking script with Python 3.10+ (no extra packages): `python rank_use_cases.py`.
If you write tests or a checker in Stage 5, you need `pytest` (`pip install pytest`).
