# Day 4 (Thursday) Pair Project: Build a Reusable Test-Utility Library

QEA v1 | Week 1 "Python Programming and Git Foundations" | Mode A: pair programming | Time: 2 to 3 hours (plan 2 h 45 min)

**Task:** PAIR PROGRAMMING: driver/navigator build a reusable test-utility library (validators, data generators, timing decorator), swapping roles every 30 min. Each pair submits **one shared repo/branch** and **a short retrospective**.

---

## 1. Scenario

Your QE team keeps copy-pasting the same little helpers into every test script: "is this test ID valid?", "give me 20 usernames", "how long did that take?". You and your partner are asked to create **`test_utils`**, one small shared library the whole team can import:

```python
from test_utils import is_valid_test_id, generate_usernames, timer
```

The library has four parts, and every part reuses something you learned this week:

| Part | What it does | Week topics it uses |
|---|---|---|
| **validators** | yes/no checks (`True`/`False`) | conditionals, loops, string methods, defaults, `*args` |
| **generators** | reproducible fake test data | `random.Random(seed)`, lists, dicts, sets, `**kwargs` |
| **helpers** | sort / pick / count test cases | lambda, `sorted`, `max`, `Counter` |
| **decorators** | `@timer` | closures, `*args/**kwargs`, `@wraps` |

You also write a short integration script (`demo_report.py`) that uses everything, and finish with a Git pull request and a retrospective.

## 2. Objectives

By the end you can:
1. Write small functions with defaults, `*args` and `**kwargs`, that **return** values (not print them).
2. Write validators with `if/elif/else` and loops; write seedable data generators with lists, dicts and sets.
3. Use `lambda` as a `key` for sorting and picking items from lists of dicts; use `Counter`.
4. Write a decorator (closure plus `@wraps`) that times any function.
5. Work as **driver** and **navigator**, swapping every 30 minutes.
6. Collaborate in Git: one shared repo and branch, commit, push, pull at every swap, co-author trailers, a pull request.
7. Reflect on how the pairing went in a written retrospective.

You only need what was taught Monday to Thursday. Keep the written lessons open (especially Thursday's *Writing Reusable Utility Functions*, section 8 "Working as a Pair").

## 3. Files you are given

```
starter_code/
  test_utils/
    __init__.py        PROVIDED (do not edit): lets you write `from test_utils import ...`
    validators.py      TODO
    generators.py      TODO
    helpers.py         TODO
    decorators.py      TODO
  demo_report.py       TODO (integration script)
  check_exercise.py    self-check (plain asserts, no pytest): read it, it is the spec
  templates/RETROSPECTIVE.md
```

Run the self-check any time, from the folder that contains `test_utils/`:

```
python3 check_exercise.py
```

At the start almost every check says FAIL (the functions are empty). Your goal: **all checks PASS**. Each FAIL tells you the call, what was expected and what you returned.

## 4. Pairing rules

1. **Two roles, always:** one **driver** (keyboard) and one **navigator** (eyes and brain). Never two typists.
2. **Swap every 30 minutes by the timer, even in the middle of a function.** Put a visible timer on a phone or screen. Use the timetable in section 5.
3. The navigator **speaks in intentions** ("let's check the prefix first"), not characters ("type i, f, space..."). The driver **thinks aloud**.
4. Both of you must **understand every line**. If one of you cannot explain it, stop and explain it.
5. Disagree politely and **try the suggestion** before rejecting it. The check script and `print()` settle arguments.
6. Every swap uses the same **hand-off routine** (section 7): save, run check, commit, push; then the new driver pulls before typing.
7. Working remotely: the driver shares the screen, the navigator keeps a second editor open only for reading hints, **not** for typing code. Working in person: one computer is fine; if you move the keyboard, change `git config user.name` / `user.email` at the swap (or each use your own laptop and `git pull`).
8. Help each other first. Ask the instructor only after you tried the hints (section 11) together.

## 5. Role-swap timetable (150 minutes of building plus 15 minutes of wrap-up)

Call your partners **Partner A** and **Partner B**. A drives first.

| Minutes | Block | Driver | Navigator | Milestones in this block | Checkpoint at the swap |
|---|---|---|---|---|---|
| 0-30 | 1 | **A** | B | M0 Setup and Git; M1 `is_in_range`, `is_valid_test_id`, `is_valid_status_code` | the three M1 validator checks PASS |
| **30** | | | **SWAP 1** | A: commit, push. B: `git pull` | |
| 30-60 | 2 | **B** | A | M2 `is_valid_email`, `is_strong_password`, `all_pass` | **Checkpoint 1:** all six validators PASS |
| **60** | | | **SWAP 2** | B: commit, push. A: `git pull` | |
| 60-90 | 3 | **A** | B | M3 `generate_username`, `generate_usernames`, `generate_password`, `generate_test_id` | those four generator checks PASS |
| **90** | | | **SWAP 3** | A: commit, push. B: `git pull` | |
| 90-120 | 4 | **B** | A | M3 `make_test_case`, `generate_test_cases`; M4 `timer` | **Checkpoint 2:** all generators and `timer` PASS |
| **120** | | | **SWAP 4** | B: commit, push. A: `git pull` | |
| 120-150 | 5 | **A** | B | M5 `sort_cases`, `slowest`, `count_by`, `build_demo_report` | **Checkpoint 3:** `18/20` or more; only the two file checks may remain |
| 150-165 | wrap-up | both | both | M6 pull request, retrospective, final check, submit (B drives the PR review, A types the retro, both talk) | `20/20 checks passed` |
| 165-180 | optional | swap every 30 | | stretch goals (section 10) | |

If you are ahead, use the spare time for stretch goals. If you are behind at a checkpoint, do **not** skip swaps: reduce scope (leave `generate_password`, `count_by` for the end) and tell the instructor.

## 6. Driver and navigator: responsibilities and sentence starters

| | **Driver** | **Navigator** |
|---|---|---|
| Focus | the **current line / function** | the **bigger picture**: design, edge cases, naming, what comes next |
| Hands | types all code, runs the commands | no typing in the project; may look up docs and hints, takes notes |
| Voice | says what they are doing and why | says the intention; asks questions; spots typos and off-by-one errors |
| Git | makes the commits at their swap, pushes | reads the diff (`git diff`) before the commit; checks the message |
| Quality | keeps functions short, adds docstrings | checks against the spec in the function docstring and `check_exercise.py` |

**Driver sentence starters**
- "I'm going to write ... because ..."
- "I'm not sure about this line, can you check it?"
- "Let me run the check to see what it says."
- "I'll name this variable ... is that clear?"
- "Can you say that again in different words? I want to be sure I understand."

**Navigator sentence starters**
- "Let's first handle the case where ..."
- "What should happen if the input is empty / has a space / is exactly the limit?"
- "Could we reuse the function we wrote earlier instead of repeating it?"
- "I think we have an off-by-one here: should it be `<` or `<=`?"
- "Before we commit, let's run the check and read the diff."
- "That's a good idea, let's try it. If it fails, we try mine."

## 7. Required Git collaboration

**One shared repository and one shared branch.** Both partners push to the same branch: `feature/test-utils`. A pull request merges it into `main`.

### M0: setup (Block 1, about 15 minutes, A drives, B navigates and then clones)

1. A creates an empty repository on GitHub/GitLab (for example `qe-test-utils-<pair-names>`) and adds B as a collaborator.
2. A clones it, copies the contents of `starter_code/` into the repo root, then **creates `.gitignore` first** (Tuesday): at least `__pycache__/`, `*.pyc`, `venv/`, `.vscode/`.
3. A commits the starter on `main` and pushes: `git add .`, `git commit -m "Add starter code and .gitignore"`, `git push`.
4. A creates the shared branch and pushes it: `git switch -c feature/test-utils`, then `git push -u origin feature/test-utils`.
5. B clones the repo and runs `git switch feature/test-utils` (use `git fetch` first if needed). Check: both see the same `git log --oneline`.

### Hand-off routine at every swap (about 2 minutes)

Outgoing **driver**:
```
python3 check_exercise.py          # note how many checks pass
git status
git diff                           # navigator reads this out loud
git add .
git commit -m "Add is_valid_email with domain rules" -m "Co-authored-by: Partner Name <partner@example.com>"
git push
```
Incoming **driver**:
```
git pull
git log --oneline -3               # you see the last commit
python3 check_exercise.py          # same result as your partner had
```

### Rules

- **Small commits**: at least one commit per group of functions (aim for 10 or more commits in total) with clear messages like `Add generate_usernames with unique names`.
- **Alternating authors**: each partner commits from their own identity (`git config user.name`, `user.email`). `git shortlog -sne` must show **both** partners, each with at least 4 commits.
- **Co-author trailer**: every commit message ends with `Co-authored-by: <navigator name> <navigator email>` (the navigator at that moment).
- **Never commit `__pycache__/`** (check with `git ls-files`).
- If you hit a **merge conflict**, resolve it together (Wednesday), then commit the merge.
- **Pull request** at the end (M6): from `feature/test-utils` to `main`, with the Tuesday template: **What / Why / How to test / Notes**. The partner who did **not** open the PR reviews it (one real comment on a line or on the whole PR), then merges.

## 8. Step-by-step build milestones

The function **docstrings in the starter files are the spec**. The tables below give the exact behaviour and which checkpoint to use.

### M0 Setup and Git (Block 1, first 15 min)
Done when: both partners can `git pull` the branch and `python3 check_exercise.py` runs (with failures) for both.

### M1 Validators, part 1 (Block 1)
Open `test_utils/validators.py`.
| Function | Behaviour |
|---|---|
| `is_in_range(value, low, high)` | `True` if `low <= value <= high` (ends included) |
| `is_valid_test_id(test_id, prefix="TC", digits=3)` | `"TC-007"` True; `"TC-7"`, `"tc-007"`, `"TC-00a"`, `"TC007"` False; works with `prefix="QA", digits=2` |
| `is_valid_status_code(code)` | `True` for 100 to 599; **must call `is_in_range`** (reuse) |

Checkpoint: `is_in_range`, `is_valid_test_id`, `is_valid_status_code` PASS.

### M2 Validators, part 2: conditionals, loops, `*args` (Block 2)
| Function | Behaviour |
|---|---|
| `is_valid_email(email)` | simple shape check: no spaces, exactly one `@`, something before it, domain contains `.` but does not start or end with `.` (use early `return False` with `if`) |
| `is_strong_password(password, min_length=8)` | long enough **and** at least one uppercase, one lowercase, one digit (use a **loop** over the characters) |
| `all_pass(value, *checks)` | `True` only if every function in `checks` returns true for `value`; `True` when no checks given. **This is your `*args` function.** |

Checkpoint 1: all six validator checks PASS (section "Milestone 1-2").

### M3 Generators: collections and seeds (Blocks 3 and 4)
Open `test_utils/generators.py`. **Rule:** every generator uses a private generator `rng = random.Random(seed)` and **never** `random.seed(...)` (the check detects this).
| Function | Behaviour |
|---|---|
| `generate_username(prefix="user", length=4, seed=None)` | `"user4821"`; same seed gives the same result |
| `generate_usernames(count, seed=None)` | list of `count` **unique** names like `"user4821"` (use a list plus a **set** to detect repeats) |
| `generate_password(length=12, seed=None)` | exactly `length` characters, always contains upper, lower and digit (assume `length >= 4`); test data only |
| `generate_test_id(number, prefix="TC", digits=3)` | `7` gives `"TC-007"`; `42, prefix="API", digits=4` gives `"API-0042"` |
| `make_test_case(test_id, name, **options)` | **new** dict `{"id","name","priority":"Medium","status":"New","duration":0.0}` updated with the options (**your `**kwargs` function**) |
| `generate_test_cases(count, seed=None)` | list of cases `TC-001...`, names `"Test case 1"...`, random `priority` (from `PRIORITIES`), `status` (from `STATUSES`), `duration` 0.10 to 5.00 with 2 decimals |

Checkpoint 2 (end of Block 4): generators and `timer` PASS.

### M4 Timing decorator (Block 4)
Open `test_utils/decorators.py`. Implement `timer(func)`: wrapper with `*args, **kwargs`, `@wraps(func)`, measures with `time.perf_counter()`, **returns the original result**, appends `(func.__name__, seconds)` to `TIMING_LOG`, prints `[timer] name took 0.0500 seconds`.
Checkpoint: `timer` PASS.

### M5 Lambda helpers and the integration report (Block 5)
Open `test_utils/helpers.py` (the **lambda** functions) and `demo_report.py`.
| Function | Behaviour |
|---|---|
| `sort_cases(cases, field, reverse=False)` | **new** sorted list; `key=lambda case: case[field]`; original list unchanged |
| `slowest(cases)` | case with largest `"duration"` (`max` with a lambda key), `None` for an empty list |
| `count_by(cases, field)` | plain dict of counts, e.g. `{"High": 2, "Low": 1}` (use `Counter`) |
| `build_demo_report(count=6, seed=7)` in `demo_report.py` | returns a string, see its docstring (header, total, slowest, by-priority, one line per case slowest first); already decorated with `@timer` |

Run `python3 demo_report.py` and read the report together.
Checkpoint 3: 18 or more of 20 checks PASS.

### M6 Pull request, retrospective, submit (wrap-up, 15 min)
1. Copy `templates/RETROSPECTIVE.md` to the repo root as `RETROSPECTIVE.md` and fill in **every** section.
2. Final run: `python3 check_exercise.py` shows `20/20 checks passed`.
3. Commit, push, open the pull request, review it, merge (or leave it open if your instructor asks).

## 9. Definition of Done (tick every box)

- [ ] `python3 check_exercise.py` prints `20/20 checks passed`
- [ ] Every function has a docstring; names are clear; no copy-pasted duplicate logic (`is_valid_status_code` reuses `is_in_range`)
- [ ] Validators **return** booleans (no `print`); generators accept `seed`; no mutable default arguments
- [ ] `timer` returns the original result and keeps the function name (`@wraps`)
- [ ] `python3 demo_report.py` prints the report
- [ ] One shared repo, one shared branch `feature/test-utils`; `.gitignore` present; no `__pycache__` in `git ls-files`
- [ ] At least 10 commits; `git shortlog -sne` shows **both** partners with 4+ commits each; navigator co-author trailers in commit messages
- [ ] Pull request opened with What / Why / How to test / Notes and reviewed by the other partner
- [ ] `RETROSPECTIVE.md` complete (no `[WRITE HERE]` left), including the role-swap log
- [ ] Roles were swapped every 30 minutes, and each partner can explain any function in the library

## 10. Stretch goals (only after the Definition of Done, or if you are ahead)

1. `log_calls` decorator: records `(function_name, args, kwargs)` in a `CALL_LOG` list (practise `*args/**kwargs`).
2. `repeat(times)` decorator (a decorator **with an argument**, three layers).
3. `sort_by_priority(cases)`: High, Medium, Low using a rank dict and a lambda.
4. `group_ids_by(cases, field)` using `defaultdict(list)`: `{"High": ["TC-002", ...]}`.
5. `pass_rate(cases, decimals=1)`: percent of cases with status `"Passed"`; `0.0` for an empty list.
6. `format_duration(seconds)`: `125` gives `"2m 5s"` (see Thursday's demo).
7. `failed_checks(value, *checks)`: list of the **names** of the checks that failed.
8. Merge-conflict drill: each partner changes the same docstring line on separate local commits, then `git pull` and resolve the conflict together.
9. Add a `usage` section to a `README.md` in the repo with three import examples.

## 11. Hints (try for 5 minutes together before opening)

<details><summary>M1: is_in_range / test ID</summary>

Python allows chained comparisons: `low <= value <= high`. For the test ID: build `start = f"{prefix}-"`, return `False` if `test_id` does not `.startswith(start)`, slice the rest with `test_id[len(start):]`, then check `.isdigit()` and `len(...) == digits`. Thursday's demo has this exact pattern.
</details>

<details><summary>M2: email, password, all_pass</summary>

Email: do the cheap rejections first with early `return False`: `" " in email`, `email.count("@") != 1`. Then `name, domain = email.split("@")`. Password: before the loop create three flags set to `False`; inside the loop use `ch.isupper()`, `ch.islower()`, `ch.isdigit()` and set the flag to `True`. `all_pass`: `for check in checks:` (a tuple of functions); call `check(value)`; `return False` inside the loop; `return True` **after** the loop.
</details>

<details><summary>M3: generators and seeds</summary>

`rng = random.Random(seed)`, then use `rng.choice(...)`, `rng.randint(...)`, `rng.shuffle(...)` (never `random.choice`). Usernames: `"".join(rng.choice(string.digits) for _ in range(length))`. Unique names: keep `names = []` and `seen = set()`, `while len(names) < count:` and add only names not in `seen`. Password: start with one random uppercase (`string.ascii_uppercase`), one lowercase, one digit in a list, fill with `string.ascii_letters + string.digits` until `length`, then `rng.shuffle(chars)` and `"".join(chars)`. Test ID padding: `"0" * (digits - len(text))`. `make_test_case`: create the defaults dict, then `case.update(options)`; building it **inside** the function keeps every call independent (no shared dict). Duration: `round(rng.randint(10, 500) / 100, 2)`.
</details>

<details><summary>M4: timer</summary>

Copy the shape from Thursday's decorators lesson: `def timer(func):` then `@wraps(func)` `def wrapper(*args, **kwargs):` ... `return wrapper`. Inside `wrapper` the three steps are: time before, `result = func(*args, **kwargs)`, time after. Do not forget `return result`.
</details>

<details><summary>M5: helpers and report</summary>

`sorted(cases, key=lambda case: case[field], reverse=reverse)` returns a new list. `max(cases, key=lambda case: case["duration"])`. `Counter(case[field] for case in cases)`, then wrap in `dict(...)`. Report: build `lines = [...]` and finish with `"\n".join(lines)`; for the priority line use `", ".join(f"{name}={counts[name]}" for name in sorted(counts))`.
</details>

<details><summary>Git: push rejected / conflicts</summary>

"rejected, fetch first" means your partner pushed: run `git pull`, then `git push`. A conflict shows `<<<<<<<` markers: decide together which lines stay, remove the markers, `git add`, `git commit`. Forgot the co-author line: `git commit --amend` (only before you push).
</details>

## 12. Time budget

| Part | Minutes |
|---|---|
| Setup and Git (M0) | 15 |
| Validators (M1, M2) | 45 |
| Generators (M3) | 50 |
| Timer decorator (M4) | 15 |
| Helpers and report (M5) | 25 |
| Hand-offs (4 swaps x 2 min) | 8 |
| Pull request, retrospective, final check (M6) | 15 |
| **Core total** | **about 2 h 45 min** (inside the 2-3 h budget) |
| Stretch goals | optional, only if time remains; hard stop at 3 h |

## 13. Submission

Submit these four things to your instructor (channel, form or LMS, as announced):
1. **Repository URL** (shared repo, both partners have push access).
2. **Branch name** (`feature/test-utils`) and **pull request URL**.
3. `RETROSPECTIVE.md` committed in the repo root (the link to it is enough).
4. The final line of `python3 check_exercise.py` (for example `20/20 checks passed`) and the output of `git shortlog -sne`.

Both partners submit the same links, and each names their partner. Do not submit `__pycache__`, virtual environments or secrets.

## 14. Pair-work rubric (100 points)

### Code (50 points)
| Criterion | Points | Full marks when |
|---|---|---|
| Self-check results | 25 | points = 25 x (checks passed / 20) |
| Function quality | 10 | clear names, docstrings kept, small functions, `is_valid_status_code` reuses `is_in_range`, returns not prints |
| Correct use of week topics | 10 | loop plus flags in password check; set for uniqueness; private `random.Random(seed)`; `*args` in `all_pass`; `**kwargs` in `make_test_case`; lambda keys; `timer` with `@wraps` and `return result` |
| Edge cases and defaults | 5 | no mutable defaults; each call returns a fresh dict/list; boundary values handled |

### Collaboration (50 points)
| Criterion | Points | Full marks when |
|---|---|---|
| Git: shared repo and branch | 8 | one shared repo, branch `feature/test-utils`, `.gitignore`, no `__pycache__` committed |
| Git: commits and authorship | 10 | 10+ small commits with clear messages; both partners 4+ commits; co-author trailers present |
| Git: pull request | 7 | What / Why / How to test / Notes; reviewed by the other partner; merged or ready to merge |
| Pairing evidence | 10 | commit history shows alternation roughly every 30 minutes; swap log in retrospective matches the history; both explain code when asked |
| Retrospective | 15 | every section answered with **specific** examples (a bug, a disagreement, something learned from the partner), honest self-rating, no placeholders |

| Band | Meaning |
|---|---|
| 90-100 | Professional: all checks pass, clean history, insightful retrospective |
| 75-89 | Solid: minor gaps (one or two checks, thin commit messages, generic retro answers) |
| 60-74 | Developing: several checks failing or unbalanced pairing (one author dominates) |
| below 60 | Needs a re-do of the pairing routine and a review with the instructor |

Individual adjustment: if the history shows one partner wrote more than 80 percent of the commits, the instructor discusses it with the pair and may adjust the collaboration points per person.
