# Day 2 (Tuesday) Exercise: Number-Guess and Log-Line Scanner, Shipped via a Pull Request

**Course:** AI enabled Test Automation Engineer (QEA v1) | **Week 1:** Python Programming and Git Foundations
**Mode:** A, code lab | **Format:** individual | **Time:** 2 to 3 hours (core about 2 h 30 min, stretch goals optional)

---

## 1. Scenario

You have just joined a QA team. Two tiny tools are needed this week, and your lead wants them delivered the way real test code is delivered: small commits, a clean repository, and a **Pull Request** for review.

1. **Number-guess game.** A console game that is secretly a lesson in test design. The secret is fixed in a constant, so a checker (or a tester) can replay the same scripted guesses and expect the same output every time. Repeatable behaviour is what makes something testable.
2. **Log-line scanner.** Scans an application log, skips noise, stops at an `END` marker, counts `ERROR` / `WARN` / `INFO` lines and gives a PASS/FAIL verdict. This is the same shape as a real log triage script and the same shape as yesterday's grader demo.

You will also add a `.gitignore` so that caches, virtual environments and secrets never reach the shared repository.

## 2. Learning objectives

By the end you can:

- Build a `while True` loop that exits with `break` and ignores bad input with `continue`.
- Use `if / elif / else` chains with the checks in the right order (validate first).
- Use a `for` loop over text lines with counters, `continue`, and `break`.
- Write a `.gitignore` and prove it works with `git status` and `git check-ignore -v`.
- Clone a repo, work on a feature branch, push it, and open a Pull Request with a useful description.
- Run a self-check script and read its PASS/FAIL output.

## 3. Prerequisites

Written topics from Monday and Tuesday (re-read the section named if you get stuck):

| Topic | Use it for |
|---|---|
| *Python Environment and Development Setup* | running `python3 file.py`, indentation |
| *Variables, Data Types and Operators* | counters, comparison operators, `in`, `.strip()`, `.lower()`, `.startswith()` |
| *Input and Output Operations* | `input()`, f-strings |
| *Type Conversion and Casting* | `int()` after validating, `.isdigit()` |
| *Conditional Statements: if, elif, else* | the guess feedback chain, level checks, order of checks |
| *Loops: for and while* | scanning lines, counters (section 5) |
| *Break and Continue Statements* | the guessing-game skeleton (2.5), the log scanner preview (4) |
| *Introduction to Git and Repository Setup*, *Git Add, Commit, Status and Log* | the everyday loop |
| *Clone, Pull, Push and Fetch* | cloning, `push -u` |
| *.gitignore* | patterns, `!` exceptions, `check-ignore` |
| *Basic Pull-Request / Merge-Request Workflow* | branch, push, PR, merge, clean up |

**You need:** Python 3.8+, Git with `user.name` / `user.email` set, a GitHub account with working authentication (you tested one `git push` in the demo), VS Code.

**Not allowed / not needed today:** functions (`def`), lists, dictionaries, classes, `import`. If you feel the urge to use one, there is a simpler way with counters and `if`. (File reading is given to you ready-made: see Part 3.)

## 4. What is in the starter folder

```
starter_code/
  number_guess.py      TODO 1: the game loop
  log_scanner.py       TODOs 2 to 5: scanning loop, verdict, summary lines
  sample_app.log       the log file the scanner reads (do not edit it)
  check_exercise.py    the self-check (do not edit it)
```

## 5. Time plan (total 150 min core)

| Part | What | Minutes |
|---|---|---|
| 0 | Create the GitHub repo, clone, add starter files | 15 |
| 1 | `.gitignore`, prove it works, first commit and push of `main` | 20 |
| 2 | Number-guess game (branch, 3 commits) | 40 |
| 3 | Log scanner (3 commits) | 40 |
| 4 | Push the branch, open the PR, self-review | 20 |
| 5 | Self-check, rubric, clean up, submit | 15 |
| | **Core total** | **150** |
| S | Stretch goals (optional) | +30 |

Commit checkpoints are marked **CHECKPOINT**. If you are more than 15 minutes behind at the end of Part 2, skip straight to Part 3 and ask for help (Part 2's WIN path alone is enough to continue).

---

## 6. Core tasks

### Part 0: Repository setup (15 min)

1. On GitHub create a **new repository** named `qea-week1-day2-<your-github-username>`. Tick **Add a README file**. Public is simplest.
2. Clone it (*Clone, Pull, Push and Fetch*, section 3):
   ```bash
   git clone https://github.com/<you>/qea-week1-day2-<you>.git
   cd qea-week1-day2-<you>
   ```
3. Copy the four starter files from `starter_code/` into the **root** of the clone (next to `README.md`). The folder should now contain `number_guess.py`, `log_scanner.py`, `sample_app.log`, `check_exercise.py`.
4. Run `python3 check_exercise.py`. **Everything FAILS.** That is the expected starting point. Read the first failure message and the last line of output.

**CHECKPOINT 0:** `git status` shows 4 untracked files and you can see the failing check output.

### Part 1: `.gitignore` and the first commit (20 min)

Read *.gitignore* sections 3 to 7 first.

1. Create `.gitignore` in the repository root with patterns for:
   - Python caches: `__pycache__/` and `*.pyc`
   - Virtual environments: `.venv/` (and `venv/`)
   - Secrets: `.env`
   - Logs: `*.log`
   - Optional but wise: editor and OS junk (`.vscode/`, `.DS_Store`, `Thumbs.db`)
2. **Trap to solve:** `*.log` also matches `sample_app.log`, which your scanner needs and your teammates need too. Add an exception line **after** `*.log` (see *.gitignore* section 4, "...but keep this one").
3. **Prove it works.** Create throwaway files and check that Git ignores them (do not commit them):
   ```bash
   mkdir __pycache__ && echo x > __pycache__/demo.pyc
   echo "API_KEY=not-a-real-key" > .env
   echo "noise" > debug.log
   git status                                  # none of the three may appear
   git check-ignore -v .env debug.log __pycache__/demo.pyc
   git check-ignore -v sample_app.log          # must print NOTHING (exit code 1)
   git status                                  # sample_app.log MUST appear as untracked
   ```
   Then delete `debug.log` (keep `.env`, it is now a good test that secrets stay local).
4. Commit the setup straight on `main` (solo repo, this is the project scaffold, not a feature) and push:
   ```bash
   git add .gitignore number_guess.py log_scanner.py sample_app.log check_exercise.py
   git commit -m "Add exercise starter files and .gitignore"
   git push
   ```
   (`git status` first. If `.env` or `__pycache__` shows up, your `.gitignore` is wrong: fix it before committing.)

**CHECKPOINT 1:** GitHub shows the starter files and `.gitignore` on `main`, and **no** `.env`, `__pycache__`, or `debug.log`.

### Part 2: Number-guess game (40 min)

1. Create the feature branch (PR workflow step 2):
   ```bash
   git switch -c feature/number-guess-and-log-scanner
   ```
2. Open `number_guess.py` and read the docstring and the TODO 1 comment block. Note the **fixed** `SECRET_NUMBER = 42` and `MAX_ATTEMPTS = 7`: do not rename them and keep each on its own line.
3. Sketch the decision flow on paper first (draw first, code second, like Phase 1 of the demo): which diamond comes first? Why must `q` and validation come **before** comparing to the secret?
4. Implement TODO 1 in small steps. Run it by hand after each step (`python3 number_guess.py`):
   - **Step A (the happy path):** `while True`, read the guess, `int()`, `attempts += 1`, `Too low` / `Too high` / `Correct! You needed N attempts.` + `break`. This is *Break and Continue* section 2.5. Set `result = "WIN"`.
     **Commit:** `Add guess loop with too low / too high / correct`
   - **Step B (bad input):** `.isdigit()` check with `continue`, then the range check with `continue`. Bad input must **not** use up an attempt.
     **Commit:** `Reject non-numeric and out-of-range guesses`
   - **Step C (ending the game):** `q` to quit, and the `MAX_ATTEMPTS` limit that sets `result = "LOSE"`. Remember: a correct guess on the last attempt is still a WIN.
     **Commit:** `Add quit and max-attempts handling`

**Exact messages (the checker compares them, case-insensitively):**

| Situation | Printed message |
|---|---|
| guess below secret | `Too low` |
| guess above secret | `Too high` |
| correct | `Correct! You needed 3 attempts.` (3 = attempts so far) |
| not a whole number (letters, empty, `-5`) | `Invalid input: please type a whole number.` |
| number outside 1 to 100 | `Out of range: choose a number from 1 to 100.` |
| `q` or `Q` | `You quit. The number was 42.` |
| wrong guess used the last attempt | `Out of attempts! The number was 42.` |
| last line always | `RESULT: WIN attempts=3` (also `LOSE` / `QUIT`) |

**Hand test.** Play a game with secret 42: `50`, `25`, `abc`, `0`, `42` should give two hints, one Invalid, one Out of range, and `RESULT: WIN attempts=3`.

**CHECKPOINT 2:** `python3 check_exercise.py` shows all `number_guess:` checks passing.

### Part 3: Log-line scanner (40 min)

1. Read the docstring in `log_scanner.py`. The block that loads the file is **provided** (reading files comes later in the course). All you need to know today: after it runs, `log_text` is one big string, exactly like the triple-quoted string in *Break and Continue* section 4.
2. Look at `sample_app.log`. Find, by eye: a comment, a blank line, an `ERROR`, an `INFO` line that contains the word "Error" in its message, a garbage line, `END`, and a line **after** `END`. Predict what each should do before you code. Write your predicted counts on paper.
3. Implement in small steps, running `python3 log_scanner.py` after each:
   - **Step A:** the `for raw_line in log_text.splitlines():` loop, `line_number += 1`, `.strip()`, skip blank/`#` lines with `continue`, stop at `END` with `break`.
     **Commit:** `Add log loop with skip and END handling`
   - **Step B:** the `if / elif / else` that counts levels. Test for `"| ERROR |"` (with the bars) so the INFO line "Error handler registered" is **not** counted as an error. Remember the first ERROR's line number and print each error as `ERROR on line N: <line>`.
     **Commit:** `Count ERROR, WARN, INFO and unknown lines`
   - **Step C:** TODO 3, 4 and 5: verdict (`PASS` only if there are zero errors) and the `First ERROR:` line.
     **Commit:** `Add verdict and first-error report`

**Expected output for the provided `sample_app.log`** (your counts must match; do not just copy, understand why):

```text
ERROR on line 6: 2026-03-02 09:15:12 | ERROR | Database connection refused
ERROR on line 9: ...
ERROR on line 14: ...
END marker reached, stopping.

Log scan summary
Lines scanned: 10
Skipped: 4
ERROR: 3
WARN: 2
INFO: 4
UNKNOWN: 1
First ERROR: line 6
Verdict: FAIL
```

**CHECKPOINT 3:** `python3 check_exercise.py` shows no FAIL for `number_guess`, `log_scanner` and `.gitignore`. (The two `git:` checks pass when you run it from inside your repo.)

### Part 4: Push the branch and open the Pull Request (20 min)

Read *Basic Pull-Request / Merge-Request Workflow*, sections 6 to 9 and 12.

1. Review your own work before anyone else sees it:
   ```bash
   git status                     # clean, nothing unexpected
   git log --oneline              # about 7 small commits with clear messages
   git diff main --stat           # only number_guess.py and log_scanner.py changed
   ```
2. Push the branch the first time with upstream tracking:
   ```bash
   git push -u origin feature/number-guess-and-log-scanner
   ```
3. On GitHub, **Compare and pull request** (base `main`, compare your branch). Title in the imperative, for example `Add number-guess game and log scanner`. Use this description template:

   ```markdown
   ## What
   - Number-guess game: `while True` loop with Too low / Too high / Correct, quit with q,
     max attempts, invalid and out-of-range input ignored.
   - Log scanner: reads sample_app.log, skips blanks and comments, stops at END,
     counts ERROR / WARN / INFO / unknown, prints PASS/FAIL verdict.
   - .gitignore for caches, virtual envs, secrets and logs (sample_app.log kept).

   ## Why
   Week 1 Day 2 exercise: practise control flow and the branch-push-PR workflow.
   The secret number is a constant so the game can be tested without a human.

   ## How to test
   1. `python3 check_exercise.py`  (expect: 0 failed)
   2. `python3 number_guess.py` and try: 50, 25, abc, 0, 42
   3. `python3 log_scanner.py` (expect Verdict: FAIL, 3 errors, first on line 6)

   ## Notes
   - Edge case I thought about: a correct guess on the last attempt counts as a WIN.
   - The word "Error" inside an INFO message is not counted as an ERROR line.
   - Anything I was unsure about: <one honest sentence>
   ```
4. Read the **Files changed** tab as a reviewer. Is there anything you would not want in the repo (a `.env`, a `__pycache__`)? There must not be.

**CHECKPOINT 4:** the PR is open, the description follows the template, and the Files changed tab lists only your two programs.

### Part 5: Self-check, clean-up, submit (15 min)

1. Run `python3 check_exercise.py` one last time inside your repo. Aim for `0 failed, 0 skipped`.
2. Score yourself with the rubric (section 11) and add the score as a PR comment.
3. Submit (section 10). **Do not merge until your trainer has reviewed** unless they told you otherwise. After the merge: `git switch main`, `git pull`, `git branch -d feature/number-guess-and-log-scanner` (PR workflow step 8).

---

## 7. Hints (try for 10 minutes before opening)

<details><summary>Number guess: my loop never ends</summary>

Every path out of the loop needs a `break`: correct, quit, and out of attempts. Print `attempts` and `answer` inside the loop to see what is happening. Stop a running program with Ctrl+C.
</details>

<details><summary>Number guess: "Out of attempts" appears even when I guess right on the last try</summary>

Order matters. Do the Too low / Too high / Correct chain **first** (Correct has a `break`), and only afterwards check `attempts >= MAX_ATTEMPTS`. That line is only reached by wrong guesses.
</details>

<details><summary>Number guess: ValueError on letters</summary>

`int("abc")` crashes. Validate with `answer.isdigit()` and `continue` **before** calling `int()`. See *Type Conversion and Casting*.
</details>

<details><summary>Log scanner: Lines scanned is too high or too low</summary>

`lines_scanned += 1` goes **after** the `continue` and `break` checks (so noise and END are not counted) and **before** the level chain. The `END` line itself is neither skipped nor scanned.
</details>

<details><summary>Log scanner: the INFO line "Error handler registered" counts as an error</summary>

You are testing for the word. Test for the level with its bars: `"| ERROR |" in line`. Strings are case-sensitive, so `"Error"` never equals `"ERROR"` but do not depend on luck.
</details>

<details><summary>Log scanner: first error line is wrong (off by one or zero)</summary>

`line_number += 1` must be the **first** statement in the loop, before any `continue`, so blank lines and comments still count as positions. Set `first_error_line` only when `error_count` has just become 1.
</details>

<details><summary>Git: sample_app.log is ignored</summary>

Add `!sample_app.log` **below** `*.log`. A later rule overrides an earlier one. If the file was already tracked it stays tracked. Verify with `git check-ignore -v sample_app.log`: no output means "not ignored".
</details>

<details><summary>Git: I committed __pycache__ or .env by mistake</summary>

Fix `.gitignore`, then `git rm -r --cached __pycache__` (or `git rm --cached .env`), commit. See *.gitignore* section 7. If `.env` held a **real** secret, tell your trainer: the secret must be changed, deleting the file is not enough because history keeps it.
</details>

<details><summary>Git: push rejected / no upstream</summary>

First push of a branch: `git push -u origin <branch>`. If rejected because the remote has commits you lack: `git pull`, then push again (*Clone, Pull, Push and Fetch*, section 10).
</details>

---

## 8. Stretch goals (optional, about 30 min, add commits to the same PR or a second PR)

1. **Random secret.** Replace the fixed number by a random one *while keeping a single line starting with* `SECRET_NUMBER =` so the checker still works. You will need to look up `import random` and `random.randint(1, 100)`; this is new material, so read the official docs and note in the PR that you looked it up. Test that the checker still passes.
2. **Hot / cold.** After Too low / Too high, print `Very close!` when the guess is within 3 of the secret (two comparisons, or look up `abs()`).
3. **Warning budget.** In the scanner, print `Verdict: FAIL` also when `warn_count` is more than 3, and print `Verdict: PASS with warnings` when there are warnings but no errors. Update the PR description's "How to test" accordingly.
4. **Critical level.** Treat `| CRITICAL |` as its own counter that `break`s the scan immediately and prints `CRITICAL found, aborting scan.`. Do not edit `sample_app.log` (the checker expects the original). Make a copy `critical_demo.log`, point `LOG_FILE` at it while testing, and notice that `*.log` keeps that copy out of Git.
5. **Git extra.** Run `git log --oneline --graph --all` and paste the output in the PR. Then create a second small branch, make a one-line README change, open a second PR and merge it.
6. **Reflection (3 sentences in the PR):** which `break`/`continue` was hardest to place, and what bug did the checker catch for you?

## 9. Definition of Done

- [ ] `.gitignore` committed with `__pycache__/`, `*.pyc`, `.venv/`, `.env`, `*.log` and the `!sample_app.log` exception
- [ ] `git check-ignore -v` proved `.env`, `debug.log` and `__pycache__` are ignored, and `sample_app.log` is not
- [ ] `number_guess.py` passes every `number_guess:` check, with `while True`, `break`, `continue`, and `if/elif/else`
- [ ] `log_scanner.py` passes every `log_scanner:` check, with `for`, `continue`, `break`, and `if/elif/else`
- [ ] `python3 check_exercise.py` run inside your repo: 0 failed
- [ ] Work done on a feature branch (not directly on `main`) with at least 6 commits that have clear, imperative messages
- [ ] No `.env`, `__pycache__`, `.pyc`, `.venv` or stray `.log` files in the repository (check on GitHub, not only locally)
- [ ] Branch pushed with `-u`; Pull Request open against `main` with the What / Why / How to test / Notes template filled in
- [ ] PR "Files changed" shows only the intended changes
- [ ] Self-score posted as a PR comment

## 10. Submission

1. Share the **Pull Request URL** (not the repository URL) with your trainer in the course channel/LMS by the end of the session. Format: `Name - Day 2 - <PR link>`.
2. The repository must be **public**, or add your trainer as a collaborator (Settings, Collaborators).
3. Leave the PR **open** for review. If your trainer leaves comments, fix them with new commits on the same branch and push again: the PR updates itself. Merge only after approval.
4. Paste the last line of your checker output (for example `17 passed, 0 failed, 0 skipped`) in the PR.

## 11. Self-check rubric (100 points)

| Area | Points | Full marks when |
|---|---|---|
| Number-guess behaviour | 25 | all `number_guess:` checks pass |
| Log-scanner behaviour | 25 | all `log_scanner:` checks pass |
| Control-flow quality | 10 | break/continue/elif used where they simplify; checks in a sensible order (validate first); no repeated copy-pasted blocks |
| Code readability | 5 | clear names, short comments explaining *why*, no leftover TODO comments |
| `.gitignore` | 10 | all required patterns, exception works, proven with `check-ignore` |
| Git history | 10 | feature branch, 6+ small commits, imperative messages, no junk files ever committed |
| Pull Request | 15 | pushed with `-u`, clear title, all four template sections filled, tidy diff |

**Bands:** 90 to 100 ready to merge; 70 to 89 solid, tidy one or two things; 50 to 69 re-read the topic named in the failing check and retry; below 50 ask for help early tomorrow, before Wednesday's data structures build on this.

**Common reasons for lost points:** `int()` before `isdigit()`; counting `END`; word-matching `error` instead of the level; `__pycache__` committed; PR opened from `main`; committing everything in one giant commit.
