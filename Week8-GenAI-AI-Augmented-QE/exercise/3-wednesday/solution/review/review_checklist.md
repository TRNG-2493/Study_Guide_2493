# Human Review Checklist for AI-Generated QA Artifacts

Use this for every AI draft before it enters the project: requirement findings, test cases, test data, automation code, defect drafts. Source: `written/3-wednesday/human-validation-of-ai-output.md`, section 4. The "Code can point" column names the helper in `qa_flow/` that flags candidates. Code points; the reviewer decides.

**Before you open the AI draft:** write your own expected results from the requirement (anti-anchoring). For US-420 run `python lab.py oracle`.

| # | Check | Ask | Code can point | You still must |
|---|---|---|---|---|
| C1 | Correct | Does every expected result match the requirement (the oracle), not just look plausible? | `check_expected` recomputes from `stories.oracle_us420` | Recompute by hand for anything money, security or legal. Never use the app as the oracle. |
| C2 | Complete | Is every AC covered, including error paths and boundaries? | `trace_matrix` (NOT COVERED), `boundary_values_present` | Walk the story, not the draft. Add missing cases with NEW ids. |
| C3 | Grounded | Is every rule, field and message in the source? Nothing invented? | `check_expected` (story does not decide), `check_finding` (quote not in story) | Turn each invented rule into a question; park the item. Do not flip it to the opposite guess. |
| C4 | Relevant | Does each item matter for this story and its risk? | nothing | Judge it. Generic padding is a reject. |
| C5 | Consistent | Same terms, ids, messages and formats as the story and the app? | `check_messages` (word for word) | Compare message text character by character. |
| C6 | Executable | Could another tester or a script run it without guessing? | `check_fields` (missing fields, no expected result, vague wording) | Read the steps and preconditions as a new joiner would. |
| C7 | Traceable | Does each item point to a real AC? | `check_fields`, `trace_matrix` (backward) | Confirm the AC is the right one, not just an existing one. |
| C8 | Safe | No real personal data, secrets or confidential details? | `responsible.preflight` / `redact` on what you paste; `check_rows` (QATEST prefix) | Read for names, addresses, ids and famous real places. Redaction misses them. |
| C9 | Non-duplicated | Each item unique, no near-copies? | `find_duplicates` (same inputs) | Look for same partition, different numbers. |

## Decisions and categories

| Decision | When | Needs |
|---|---|---|
| ACCEPTED | All nine checks pass | Nothing failed. Evidence (an AC) still recorded. |
| EDITED | Worth keeping, at least one check failed | Failed checks, category, evidence, the corrected fields (`patch`). |
| REJECTED | Adds nothing or enforces an undecided rule | Failed checks, category, evidence. Parked items link to an OPEN question. |
| ADDED | The human wrote a case the AI missed | A new id (never reuse an AI id), category MISSING_COVERAGE, evidence. |

Categories: `WRONG_EXPECTED`, `INVENTED_REQUIREMENT`, `WRONG_TRACE`, `DUPLICATE`, `MISSING_INFO`, `WRONG_WORDING`, `MISSING_COVERAGE`.

## Sign-off rules (enforced by `lab.py signoff`)

1. Every AI item has exactly one human decision. Nothing passes silently.
2. Every non-accepted item has a category and evidence.
3. A named reviewer. For high-risk stories (money, login, checkout) a different named approver.
4. Only a signed-off suite (`"status": "APPROVED"`) runs in `tests/test_suite_rows.py` by default.
5. AI-assisted files carry the disclosure header: `python lab.py disclose ...`.
