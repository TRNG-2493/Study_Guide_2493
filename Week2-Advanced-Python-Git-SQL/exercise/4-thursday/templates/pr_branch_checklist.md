# Pull request / branch checklist

Paste this into the description of your pull request (or tick it in a file if you use a
local bare remote). Every box must be ticked or have a one-line reason.

## Branch and history
- [ ] Work is on a feature branch named `feature/sql-validation-<names>` (not `main`)
- [ ] Branch is pushed; `git status` says "up to date with origin/..."
- [ ] Both partners have commits under their own `user.name` (`git shortlog -sn`)
- [ ] At least 6 commits, each with a message that says what changed and why
      (`Add R-03 status domain check`, not `update`)
- [ ] Each partner has pulled (`git pull`) at least once during the session, and `git fetch` + `git log origin/<branch>` was used to look before pulling
- [ ] No merge-conflict markers (`<<<<<<<`) anywhere; if there was a conflict, it was resolved by both partners
- [ ] No generated files committed: `logs/`, `*.db`, `__pycache__/`

## The artifact
- [ ] `sql/validation_queries.sql` has R-01..R-12, E-01, E-02; headers and `@expect` lines untouched
- [ ] `python -m qe_foundations.validation` prints one PASS/FAIL line per rule and writes `logs/validation.log`
- [ ] `ValidationFailedError` is raised for a failing rule and covered by a test
- [ ] `python -m unittest qe_foundations.tests.test_validation` passes (>= 5 tests)
- [ ] `python check_exercise.py` shows no FAIL
- [ ] `qe_foundations/docs/`: `defect_checklist.md`, `defect_reports.md`, `pairing_log.md`, `retrospective.md` are complete

## Review (the OTHER partner ticks these after reading the diff)
- [ ] I can explain every query in plain English
- [ ] I ran the suite on my own machine after `git pull`
- [ ] I found no secrets, passwords or personal data in the diff

## PR description (3 lines)
1. What this adds:
2. How to run it:
3. Known gaps / questions:
