# US-420 Review Report

Reviewer:
Approver (a different person):
Date:
AI tool: Claude (model name as shown in the interface):

## 1. My manual review (written BEFORE prompting; commit hash: )
| # | AC | Problem | Category |
|---|---|---|---|
| 1 | | | |

## 2. Claude's requirements findings
`python lab.py check-findings evidence/findings.run1.txt` output summary:

| # | AC | Automatic check | My verdict (keep / discard) | Why |
|---|---|---|---|---|
| | | | | |

What Claude found that I missed:
What I found that Claude missed:

## 3. Question log and PO answers
See `review/question_log.md`. Answered: _ / Open: _ / Who answered:

## 4. My oracle (written BEFORE reading the test case draft; commit hash: )
Paste `python lab.py oracle` output:

## 5. Test case review
`check-suite` trace matrix and pointers (summary):

Sign-off metrics (paste from `lab.py signoff`):

Which suite catches the bug?

| | `--impl giftcard` | `--impl giftcard_buggy` |
|---|---|---|
| Claude draft (`--unreviewed`) | | |
| Approved suite | | |

Explanation (3-5 sentences):

## 6. Test data review
`check-data` problems and my decision on each:

| Row | Problem reported | Who is right (Claude / my oracle / PO question) | Decision |
|---|---|---|---|
| | | | |

What I found by reading that no check reported:

## 7. Responsible use
- Classification I chose for `materials/qa-bug-note.txt` and why:
- My GIFT_CARD rule and what it caught:
- What the redactor still missed (I found by reading):
- Secrets that must be rotated, and who I would tell:
- Defect report: what I corrected in Claude's draft:
- Disclosure line used:

## 8. Reflection (5 bullets)
- Usable as-is vs usable at all, and what that means for trusting AI drafts:
-
