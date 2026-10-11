# Knowledge Check: Control Flow & Git (Week 1 – Tuesday)

Answer all 72 questions, then open each "Click for Solution" to check your work and read the explanation.

---

## Part 1: Multiple Choice

### Question 1

A teammate writes this check for a test-report page:

```python
if role == "admin" or "manager":
    print("Access to reports granted")
```

What is wrong with it?

- [ ] A) Nothing; it grants access only to admins and managers
- [ ] B) It raises a `SyntaxError` because `or` cannot join a comparison and a string
- [ ] C) The condition is always true, because the non-empty string `"manager"` is truthy
- [ ] D) It grants access only when `role` is `"manager"`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** Python reads `"manager"` as its own condition, and a non-empty string is always truthy, so the whole `or` expression is always true. The fix is `role == "admin" or role == "manager"`.
- **Why others are wrong:**
  - A) Any role, even `"guest"`, would get access.
  - B) The line is valid syntax; the problem is logic, not syntax.
  - D) Admins pass the first comparison, and everyone else passes through the truthy string.
</details>

---

### Question 2

A test script runs `while count <= 5: print(count)` and the programmer forgets `count += 1`. What happens, and how do you stop it?

- [ ] A) It prints `1` once and then ends
- [ ] B) It prints `1` endlessly; press `Ctrl + C` to stop it
- [ ] C) Python raises an error before the loop starts
- [ ] D) It prints `1` to `5` and then ends

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Without an update, the condition never becomes `False`, so the loop is infinite. `Ctrl + C` in the terminal stops a runaway program.
- **Why others are wrong:**
  - A) The condition is re-checked after every pass, so the loop does not stop on its own.
  - C) Python does not detect infinite loops; it just runs.
  - D) `count` is never changed, so it never reaches `2`.
</details>

---

### Question 3

You scan a test matrix with two nested loops and put `break` inside the inner loop. What does that `break` do?

- [ ] A) Exits both loops
- [ ] B) Skips only the current iteration of the inner loop
- [ ] C) Ends the whole program
- [ ] D) Exits only the innermost loop that contains it; the outer loop keeps going

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** In nested loops, `break` and `continue` affect only the innermost loop. To leave both loops, use a flag variable and a second `break` in the outer loop.
- **Why others are wrong:**
  - A) That requires a flag variable plus a second `break`.
  - B) That describes `continue`, not `break`.
  - C) `break` never ends the program; execution continues after the loop.
</details>

---

### Question 4

In a `.gitignore`, what does the pattern `*.py[cod]` match?

- [ ] A) `.pyc`, `.pyo` and `.pyd` files
- [ ] B) Only files named exactly `*.py[cod]`
- [ ] C) `.py` files whose names contain the letters c, o or d
- [ ] D) Only `.pyc` files

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `[cod]` is a character set that matches exactly one of `c`, `o` or `d`, so the pattern covers `.pyc`, `.pyo` and `.pyd`.
- **Why others are wrong:**
  - B) The `*` and `[...]` are pattern syntax, not literal characters.
  - C) The set applies to the character right after `.py` in the extension, not to the file name.
  - D) The set also matches `o` and `d`.
</details>

---

### Question 5

You committed `debug.log` last week. Today you added `*.log` to `.gitignore`, but `git status` still shows changes to `debug.log`. What is the correct fix to stop tracking it while keeping the file on your disk?

- [ ] A) Add `*.log` to `.gitignore` a second time
- [ ] B) Run `git rm debug.log` and commit
- [ ] C) Run `git rm --cached debug.log` and commit
- [ ] D) Rename the file to `.gitignore`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `.gitignore` only affects untracked files. `git rm --cached` removes the file from Git's index only, leaving it on disk, and the commit records that it is no longer tracked.
- **Why others are wrong:**
  - A) Repeating the rule changes nothing for an already-tracked file.
  - B) Without `--cached`, `git rm` also deletes the file from your disk.
  - D) A file named `.gitignore` is a rules file, not a way to stop tracking.
</details>

---

### Question 6

What is the key difference between `git fetch` and `git pull`?

- [ ] A) `fetch` uploads your commits; `pull` downloads commits
- [ ] B) `fetch` downloads new commits without changing your branch or files; `pull` also merges them into your current branch
- [ ] C) `fetch` downloads only file contents; `pull` downloads only history
- [ ] D) They are identical; `fetch` is just the older name

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** `git pull` is `git fetch` plus `git merge`. Fetch is the safe, read-only way to look at what is new before you integrate it.
- **Why others are wrong:**
  - A) Uploading commits is `git push`.
  - C) Both download commits and branch information; neither splits content from history.
  - D) They behave differently: only `pull` changes your branch and can cause conflicts.
</details>

---

### Question 7

Your `git push` is rejected with `! [rejected] main -> main (fetch first)`. What should you do?

- [ ] A) Run `git push --force` to overwrite the remote
- [ ] B) Delete the repository and clone it again
- [ ] C) Run `git init` again
- [ ] D) Run `git pull` to bring in the remote's new commits, then `git push` again

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** The remote has commits you do not have yet, and Git will not overwrite them. Pull first, then push.
- **Why others are wrong:**
  - A) Force-pushing can destroy teammates' work; beginners should avoid it.
  - B) Re-cloning throws away your local commits and is unnecessary.
  - C) `git init` creates a new repository and does nothing for this problem.
</details>

---

### Question 8

In the pull-request workflow, what should you do first, before creating your feature branch?

- [ ] A) Run `git switch main` and `git pull` so you start from an up-to-date `main`
- [ ] B) Open the pull request on GitHub
- [ ] C) Delete the old branch
- [ ] D) Run `git push --force`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** The workflow starts by updating `main`, which avoids conflicts later. Then you create a branch, commit, push the branch, open the PR, review, merge and clean up.
- **Why others are wrong:**
  - B) A PR can only be opened after the branch has been created, committed to and pushed.
  - C) Deleting branches is the last step (clean up), after the merge.
  - D) Force-pushing is never part of the basic workflow.
</details>

---

### Question 9

A reviewer asks for changes on your open pull request. What is the correct way to respond?

- [ ] A) Close the PR and open a brand-new one
- [ ] B) Email the fixed file to the reviewer
- [ ] C) Commit the fixes on the same branch and `git push`; the PR updates automatically
- [ ] D) Commit the fixes directly to `main`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** A PR tracks its branch, so new commits pushed to that branch appear in the same PR automatically. Then reply to the comments and mark them resolved.
- **Why others are wrong:**
  - A) There is no need for a new PR; the existing one updates.
  - B) Review happens on the PR page, not by emailing files.
  - D) Changes should not go straight to `main`; that bypasses review.
</details>

---

### Question 10

Which merge option combines all of a branch's commits into **one** commit on `main`?

- [ ] A) Create a merge commit
- [ ] B) Squash and merge
- [ ] C) Rebase and merge
- [ ] D) Draft pull request

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Squash and merge gives a clean history of one commit per PR, which many teams choose as their default.
- **Why others are wrong:**
  - A) A merge commit keeps all the branch's commits and adds one more.
  - C) Rebase replays the commits on top of `main` without a merge commit, keeping them separate.
  - D) A draft PR is a status meaning "not ready for review", not a merge style.
</details>

---

### Question 11

A grading script gives a score of `95` the grade `C`:

```python
score = 95

if score >= 60:
    grade = "C"
elif score >= 75:
    grade = "B"
elif score >= 90:
    grade = "A"
```

What is the best fix?

- [ ] A) Reorder the chain so the most specific condition (`score >= 90`) is checked first and the loosest (`score >= 60`) last
- [ ] B) Move an `else` branch to the top so it catches everything first
- [ ] C) Add more `elif` branches after the last one
- [ ] D) Indent all three blocks one level further

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** The first matching branch wins and the rest of the chain is skipped, so `95 >= 60` is caught before the better matches are ever checked. Order conditions from most specific to most general.
- **Why others are wrong:**
  - B) `else` has no condition and must be the last branch, so it cannot go first.
  - C) Extra branches at the end are never reached, because the first branch already matched.
  - D) Indentation decides which lines belong to a block, not which condition is checked first.
</details>

---

### Question 12

Which condition correctly checks whether `status` is one of `"FAIL"`, `"ERROR"` or `"BLOCKED"`?

- [ ] A) `if status == "FAIL" or "ERROR" or "BLOCKED":`
- [ ] B) `if status == "FAIL" and status == "ERROR" and status == "BLOCKED":`
- [ ] C) `if status = "FAIL" or status = "ERROR" or status = "BLOCKED":`
- [ ] D) `if status in ("FAIL", "ERROR", "BLOCKED"):`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** The `in` operator asks "is `status` one of these values?" and is tidier than several `==` comparisons joined by `or`.
- **Why others are wrong:**
  - A) The bare strings `"ERROR"` and `"BLOCKED"` are non-empty, so they are truthy and the condition is always true.
  - B) `and` needs every part to be true, and one value cannot equal all three strings at once.
  - C) A single `=` assigns instead of comparing, which is a `SyntaxError` in a condition.
</details>

---

### Question 13

A test evaluator uses this chain. The response had status `404` **and** was also too slow, yet the report mentions only the status problem. Why?

```python
if actual_status != expected_status:
    result = "FAIL"
    reason = f"status {actual_status}, expected {expected_status}"
elif actual_time > expected_time_limit:
    result = "FAIL"
    reason = f"too slow: {actual_time}s"
else:
    result = "PASS"
    reason = "all checks passed"
```

- [ ] A) The time check contains a syntax error
- [ ] B) Once the first branch ran, the rest of the `if / elif / else` chain was skipped, so the time check was never evaluated
- [ ] C) A decimal number cannot be compared inside an `elif`
- [ ] D) The `elif` branch ran but its `reason` was overwritten by the first branch

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Only the first matching branch of a chain runs. This mirrors how many real tests stop reporting at the first failed assertion.
- **Why others are wrong:**
  - A) The `elif` line is valid; it just never gets evaluated.
  - C) Comparisons such as `actual_time > expected_time_limit` produce a boolean and work with decimal numbers.
  - D) The `elif` branch never ran at all, so nothing was overwritten.
</details>

---

### Question 14

Which call makes a loop run for the numbers 1 through 5, **including** 5?

- [ ] A) `range(5)`
- [ ] B) `range(1, 5)`
- [ ] C) `range(1, 6)`
- [ ] D) `range(6)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** The stop value of `range()` is never included, so `range(1, 6)` gives 1, 2, 3, 4 and 5.
- **Why others are wrong:**
  - A) `range(5)` gives 0, 1, 2, 3, 4; it starts at 0 and never reaches 5.
  - B) `range(1, 5)` stops at 4 because the stop value is excluded.
  - D) `range(6)` gives 0 to 5, so it includes an unwanted 0.
</details>

---

### Question 15

Which task is best suited to a `while` loop rather than a `for` loop?

- [ ] A) Printing the test IDs `TC-001` to `TC-020`
- [ ] B) Counting the digits in a test ID
- [ ] C) Running the same login check exactly 50 times
- [ ] D) Asking for an age again and again until the user enters a valid one

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** Use `while` for "keep going until something happens", where you don't know in advance how many repetitions are needed. Input validation is the classic case.
- **Why others are wrong:**
  - A) The count is known (20), so `for` with `range()` fits.
  - B) Going through every character of a string is a job for `for`.
  - C) "Exactly N times" is `for` with `range(N)`.
</details>

---

### Question 16

A teammate's loop prints the running total four times, but they wanted only the final total printed once. What is the most likely cause?

```python
total = 0
for n in range(1, 5):
    total = total + n
    print(total)
```

- [ ] A) `print(total)` is indented, so it is inside the loop; it should be unindented to run once after the loop
- [ ] B) `total = 0` should be moved inside the loop
- [ ] C) `range(1, 5)` should be `range(1, 6)` to print once
- [ ] D) The `for` line is missing its colon

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** An indented line belongs to the loop body and runs on every iteration. An unindented `print(total)` runs once, after the loop completes.
- **Why others are wrong:**
  - B) Resetting the accumulator inside the loop is a common mistake; initialize it before the loop.
  - C) The range controls how many iterations happen, not how often the print repeats per run of the loop.
  - D) The colon is present, and a missing colon would be a `SyntaxError`, not repeated output.
</details>

---

### Question 17

What happens when this loop runs?

```python
count = 0
while count < 5:
    if count == 2:
        continue
    print(count)
    count += 1
```

- [ ] A) It prints `0`, `1`, `3`, `4` and then ends
- [ ] B) It prints `0` and `1`, then runs forever without changing `count`
- [ ] C) It prints `0` and `1` and then ends
- [ ] D) It raises a `SyntaxError` because `continue` is not allowed in a `while` loop

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** When `count` is `2`, `continue` jumps back to the condition check without reaching `count += 1`, so `count` stays `2` forever. Update the counter before the `continue` to fix it.
- **Why others are wrong:**
  - A) That output needs the counter to move past `2`, but the update is skipped.
  - C) The condition `count < 5` stays true, so the loop never ends.
  - D) `continue` is valid in `while` loops; the bug is logic, not syntax.
</details>

---

### Question 18

What happens if you write a bare `break` at the top level of a script, outside any loop?

- [ ] A) The program ends quietly at that line
- [ ] B) Python skips the next line and carries on
- [ ] C) Python raises a `NameError` when the line is reached
- [ ] D) Python raises a `SyntaxError`, because `break` is only allowed inside `for` or `while`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `break` only makes sense inside a loop, so using it elsewhere is a `SyntaxError`.
- **Why others are wrong:**
  - A) `break` never ends the program; it only leaves a loop.
  - B) `break` has nothing to do with skipping lines outside a loop.
  - C) `break` is a keyword, not a name, so this is not a `NameError`.
</details>

---

### Question 19

A log scanner should ignore comment lines that start with `#` but keep processing every other line. Which statement belongs inside the `if line.startswith("#"):` block?

- [ ] A) `break`
- [ ] B) `pass`
- [ ] C) `continue`
- [ ] D) A loop `else` clause

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `continue` skips the rest of the current iteration and moves on to the next line, which is how a scanner ignores lines it doesn't care about.
- **Why others are wrong:**
  - A) `break` would end the whole loop at the first comment, so later lines would never be read.
  - B) `pass` does nothing, so the rest of the loop body would still run on the comment line.
  - D) A loop `else` runs only after the loop finishes without `break`; it does not skip lines.
</details>

---

### Question 20

Which file does the `.gitignore` pattern `file?.txt` match?

- [ ] A) `file1.txt`
- [ ] B) `file10.txt`
- [ ] C) `file.txt`
- [ ] D) `fileab.txt`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `?` matches exactly one character, so `file?.txt` matches `file1.txt` and `file2.txt` but not `file10.txt`.
- **Why others are wrong:**
  - B) `10` is two characters, and `?` matches exactly one.
  - C) There is no character between `file` and `.txt`, but `?` needs exactly one.
  - D) `ab` is two characters, so it does not match a single `?`.
</details>

---

### Question 21

You want Git to ignore everything inside `logs/` except `important.log`. Which rules work?

- [ ] A) `logs/` followed by `!logs/important.log`
- [ ] B) `logs/*` followed by `!logs/important.log`
- [ ] C) `!logs/important.log` followed by `logs/*`
- [ ] D) `logs/*` on its own

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** You cannot re-include a file when its parent folder is ignored, so ignore the folder's contents with `logs/*` and then negate the one file with `!`.
- **Why others are wrong:**
  - A) With `logs/` the whole folder is excluded, so the negation does not work.
  - C) Rules are processed top to bottom and later rules override earlier ones, so `logs/*` ignores `important.log` again.
  - D) Without the `!` rule, `important.log` is ignored too.
</details>

---

### Question 22

You accidentally committed an API key and pushed it to GitHub. What is the correct first response?

- [ ] A) Add the key's file to `.gitignore`
- [ ] B) Run `git rm --cached` on the file and commit
- [ ] C) Revoke or rotate the key immediately and treat the old one as compromised
- [ ] D) Delete the file from your own laptop

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** Once pushed, a secret can be copied by anyone with access, and automated scanners look for exposed keys within minutes. Generating a new key makes the leaked one useless.
- **Why others are wrong:**
  - A) Adding it to `.gitignore` afterwards does not remove it from history.
  - B) `git rm --cached` stops tracking, but the key remains in the repository's earlier history.
  - D) Deleting your local copy does nothing about the copy already on the remote.
</details>

---

### Question 23

`git status` shows: `Your branch is ahead of 'origin/main' by 2 commits.` What does this mean and what should you do?

- [ ] A) The remote has 2 commits you lack; run `git pull`
- [ ] B) Your clone is corrupt; clone the repository again
- [ ] C) Everything is in sync; do nothing
- [ ] D) You have 2 commits that are not pushed yet; run `git push`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** "Ahead" means your local branch has commits the remote does not, so `git push` shares them.
- **Why others are wrong:**
  - A) That describes "behind", where the remote has commits you lack.
  - B) The message is normal status information, not a sign of corruption.
  - C) "Up to date" is the message for an in-sync branch.
</details>

---

### Question 24

What does the `-u` in `git push -u origin main` do?

- [ ] A) Links your local `main` to `origin/main`, so later you can type just `git push` and `git pull`
- [ ] B) Forces the push and overwrites the remote's history
- [ ] C) Uploads changes you have saved but not committed
- [ ] D) Creates the repository on GitHub for you

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `-u` is short for `--set-upstream`. It sets up tracking between your local branch and the remote branch.
- **Why others are wrong:**
  - B) Forcing is `--force`, which beginners should avoid.
  - C) Push sends commits only, never uncommitted changes.
  - D) You create the repository on GitHub yourself before pushing.
</details>

---

### Question 25

You already have local commits and want to put the project on GitHub. Why should you leave "Add a README", ".gitignore" and "license" unticked when creating the GitHub repository?

- [ ] A) GitHub cannot store those files
- [ ] B) `git remote add` fails if the remote has a README
- [ ] C) An empty remote avoids conflicting histories, such as `refusing to merge unrelated histories`
- [ ] D) Those files can only be added later with `git clone`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** If the remote already has its own commits and your local repository has different ones, the two histories were created independently and Git refuses to merge them. An empty remote avoids that.
- **Why others are wrong:**
  - A) GitHub stores these files fine; the problem is the independent history they create.
  - B) `git remote add` only registers the name and URL; it does not care what is on the remote.
  - D) Nothing about these files requires `git clone`.
</details>

---

### Question 26

Which command creates a new branch called `feature/add-login-test` **and** switches to it?

- [ ] A) `git switch feature/add-login-test`
- [ ] B) `git branch -d feature/add-login-test`
- [ ] C) `git push -u origin feature/add-login-test`
- [ ] D) `git switch -c feature/add-login-test`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `-c` means create the branch and then switch to it. Any commits you make afterwards go onto the new branch, not `main`.
- **Why others are wrong:**
  - A) Without `-c`, `git switch` moves between branches that already exist.
  - B) `git branch -d` deletes a fully merged branch.
  - C) `git push -u` uploads an existing branch to the remote; it does not create or switch branches locally.
</details>

---

### Question 27

You open a pull request and a CI check shows a red cross. What should you do?

- [ ] A) Merge the PR anyway and fix it later
- [ ] B) Click **Details**, read the log, fix the problem locally and push again
- [ ] C) Close the PR and open a new one with the same code
- [ ] D) Commit a fix directly to `main`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** CI runs your tests or checks on every PR. Fix the problem on your branch and push; the PR updates and the checks run again.
- **Why others are wrong:**
  - A) PRs normally need passing checks before merging, and the red check is telling you something is wrong.
  - C) The existing PR updates automatically when you push, so a new one is unnecessary.
  - D) Don't push directly to `main`; that bypasses review and checks.
</details>

---

### Question 28

Which is the best branch name for a fix to a flaky search test?

- [ ] A) `fix/flaky-search-test`
- [ ] B) `my-branch`
- [ ] C) `Fix flaky search test`
- [ ] D) `test`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** Branch names should be short, lowercase, hyphenated and descriptive, often with a prefix such as `fix/` or `feature/`.
- **Why others are wrong:**
  - B) `my-branch` is vague and says nothing about the change.
  - C) Spaces should be avoided in branch names, and it is not lowercase and hyphenated.
  - D) `test` is a vague name and gives no hint of the change.
</details>

---

## Part 2: True/False

### Question 29

**True or False:** In an `if / elif / else` chain, if the `if` condition is true and a later `elif` condition is also true, both blocks run.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Once one branch runs, the rest of the chain is skipped. Separate `if` statements are checked independently, but an `elif` chain runs at most one block.
</details>

---

### Question 30

**True or False:** Adding a file name to `.gitignore` makes Git stop tracking that file even if it was already committed.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `.gitignore` only affects untracked files. For an already-committed file you must run `git rm --cached <file>` and commit.
</details>

---

### Question 31

**True or False:** `git fetch` downloads new commits from the remote but does not change your working files or your current branch.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Fetch only updates remote-tracking information such as `origin/main`. It is the safe way to look before integrating; `git pull` is what merges.
</details>

---

### Question 32

**True or False:** After a reviewer requests changes on your PR, you must close it and open a new PR for the fixes.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** You commit and push to the same branch, and the existing PR updates automatically with the new commits.
</details>

---

### Question 33

**True or False:** Python does not allow `if 18 <= temperature <= 25:`; you must write `if 18 <= temperature and temperature <= 25:`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Python supports chained comparisons, and `18 <= temperature <= 25` means exactly the same as the longer `and` version. It reads like maths.
</details>

---

### Question 34

**True or False:** A `for` loop over `range(10)` can turn into an infinite loop if you forget to update the loop variable.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A `for` loop takes its next value from the sequence automatically, so it can't accidentally run forever. Forgetting the update is the classic `while` loop mistake.
</details>

---

### Question 35

**True or False:** In nested loops, `continue` affects only the innermost loop that contains it.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Both `break` and `continue` affect only the innermost loop. The outer loop carries on as normal.
</details>

---

### Question 36

**True or False:** The `.gitignore` file itself should not be committed, because it is only a personal setting.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `.gitignore` should be committed so that everyone who clones the project gets the same rules. Rules that are only for you belong in `.git/info/exclude` or a global ignore file.
</details>

---

### Question 37

**True or False:** Git can commit an empty folder as long as you create it with `mkdir`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Git tracks files, not folders. A common convention is to put an empty placeholder file, usually named `.gitkeep`, inside the folder.
</details>

---

### Question 38

**True or False:** If `git check-ignore -v debug.log` prints nothing, the file is not being ignored.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** When a file is ignored, the command prints the rule responsible, such as `.gitignore:2:*.log`. No output means no rule matched.
</details>

---

### Question 39

**True or False:** `git clone` downloads only the latest snapshot of the files, not the commit history.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `git clone` downloads a complete copy of the remote repository, including all of its history, and sets up `origin` for you.
</details>

---

### Question 40

**True or False:** `git status` compares your branch with the *last fetched* state of the remote, so you should run `git fetch` first to see the true situation.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** `origin/main` is only your last-known copy of the remote. It moves when you fetch, pull or push, so status can be out of date until you fetch.
</details>

---

### Question 41

**True or False:** In a pull request, the **base** branch is the one that contains your changes, and the **compare** branch is where they will be merged.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It is the other way round. The base is the branch you want to merge into (usually `main`), and the compare (head) branch holds your changes.
</details>

---

### Question 42

**True or False:** If your work is not ready for review, GitHub lets you open the pull request as a draft and later mark it **Ready for review**.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** A draft PR signals "not ready for review". You convert it with **Ready for review** when you are done.
</details>

---

## Part 3: Code Prediction

### Question 43

What does this program print?

```python
failed_count = 0
username = ""

if failed_count:
    print("Some tests failed")
else:
    print("No failures")

if username:
    print(f"Hello, {username}")
else:
    print("Username cannot be empty")
```

- [ ] A) `Some tests failed` and `Hello, `
- [ ] B) `No failures` and `Hello, `
- [ ] C) `Some tests failed` and `Username cannot be empty`
- [ ] D) `No failures` and `Username cannot be empty`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** `0` and the empty string are falsy, so both `if` conditions are false and both `else` blocks run.
- **Why others are wrong:**
  - A) Both values are falsy, so neither `if` block runs.
  - B) The empty string is falsy, so the `username` `if` block does not run.
  - C) `0` is falsy, so `Some tests failed` is not printed.

**Verified output:**
```text
No failures
Username cannot be empty
```
</details>

---

### Question 44

What does this program print?

```python
x = 10

if x > 5:
    print("A")
elif x > 8:
    print("B")

if x > 8:
    print("C")
```

- [ ] A) `A`
- [ ] B) `A` and `B`
- [ ] C) `A`, `B` and `C`
- [ ] D) `A` and `C`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** In the first chain, `x > 5` is true so `A` prints and the `elif` is skipped. The second `if` is a separate statement checked on its own; `x > 8` is true so `C` prints.
- **Why others are wrong:**
  - A) The second, separate `if` still runs and prints `C`.
  - B) The `elif x > 8` never runs because the `if x > 5` branch already ran.
  - C) `B` is skipped because it is part of the chain whose first branch matched.

**Verified output:**
```text
A
C
```
</details>

---

### Question 45

What does this program print?

```python
total = 0
for i in range(2, 10, 3):
    total += i
print(total)
```

- [ ] A) `15`
- [ ] B) `20`
- [ ] C) `27`
- [ ] D) `10`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** `range(2, 10, 3)` produces 2, 5, 8 (stop is excluded, step is 3). The accumulator adds them: 2 + 5 + 8 = 15.
- **Why others are wrong:**
  - B) This would require a fourth value; `range(2, 10, 3)` produces only 2, 5 and 8.
  - C) This ignores the step of 3; it is closer to summing every number from 2 to 7 or adding extra values.
  - D) That is the result of `range(1, 5)` (1+2+3+4), not this range.

**Verified output:**
```text
15
```
</details>

---

### Question 46

What does this program print?

```python
size = 20
steps = 0

while size > 1:
    size = size / 2
    steps += 1

print(steps)
```

- [ ] A) `4`
- [ ] B) `10`
- [ ] C) `5`
- [ ] D) `6`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `size` goes 20, 10, 5, 2.5, 1.25, 0.625. After five halvings it is 0.625, which is no longer greater than 1, so the loop ends with `steps` equal to 5.
- **Why others are wrong:**
  - A) After four halvings `size` is 1.25, which is still greater than 1.
  - B) That is the answer for starting at 1000, not 20.
  - D) The loop stops as soon as `size` is 0.625; no sixth halving happens.

**Verified output:**
```text
5
```
</details>

---

### Question 47

A log scanner skips blank lines, stops at `END`, and counts the lines it reads and the errors it finds. What does this program print?

```python
log_text = """INFO Start

ERROR Disk full
WARNING Slow
END
ERROR Ignored"""

errors = 0
lines_read = 0

for line in log_text.splitlines():
    line = line.strip()
    if line == "":
        continue
    if line == "END":
        break
    lines_read += 1
    if line.startswith("ERROR"):
        errors += 1

print(lines_read, errors)
```

- [ ] A) `3 1`
- [ ] B) `4 1`
- [ ] C) `3 2`
- [ ] D) `6 2`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** The blank line is skipped by `continue` and not counted. `INFO`, `ERROR` and `WARNING` are read (3 lines), with one error. `break` at `END` means the last `ERROR` line is never examined.
- **Why others are wrong:**
  - B) The blank line is skipped, so it is not counted as a line read.
  - C) The second `ERROR` comes after `END`, and the loop has already stopped.
  - D) That would count every line and ignore both `continue` and `break`.

**Verified output:**
```text
3 1
```
</details>

---

### Question 48

What does this program print?

```python
for row in range(1, 3):
    for col in range(1, 4):
        if col == 3:
            break
        print(f"({row},{col})")

for n in range(1, 4):
    if n == 9:
        break
else:
    print("not found")
print("done")
```

- [ ] A) `(1,1)`, `(1,2)`, `(2,1)`, `(2,2)`, `done`
- [ ] B) `(1,1)`, `(1,2)`, `not found`, `done`
- [ ] C) `(1,1)`, `(1,2)`, `(1,3)`, `(2,1)`, `(2,2)`, `(2,3)`, `not found`, `done`
- [ ] D) `(1,1)`, `(1,2)`, `(2,1)`, `(2,2)`, `not found`, `done`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** The inner `break` at `col == 3` stops only the inner loop, so each of the two rows prints `col` 1 and 2. In the second loop, `n` is never 9, so no `break` happens and the loop `else` runs, printing `not found`.
- **Why others are wrong:**
  - A) The loop `else` runs when the loop finishes without `break`, so `not found` is printed.
  - B) The inner `break` does not stop the outer loop, so row 2 is printed too.
  - C) `col == 3` triggers `break` before the print, so `(1,3)` and `(2,3)` never appear.

**Verified output:**
```text
(1,1)
(1,2)
(2,1)
(2,2)
not found
done
```
</details>

---

### Question 49

A grader validates the score first. What does this program print?

```python
student = "Sam"
score = 150

if score < 0 or score > 100:
    print("Invalid score; it must be between 0 and 100")
elif score >= 50:
    print(f"{student}: PASS ({score})")
else:
    print(f"{student}: FAIL ({score})")
```

- [ ] A) `Sam: PASS (150)`
- [ ] B) `Invalid score; it must be between 0 and 100`
- [ ] C) `Sam: FAIL (150)`
- [ ] D) `Invalid score; it must be between 0 and 100` and `Sam: PASS (150)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** `150 > 100` makes the first condition true, so only that branch runs. Validating first stops a nonsense score from being treated as a pass.
- **Why others are wrong:**
  - A) The `elif` is never checked, because the first branch already matched.
  - C) `150` is not below 50, and the `else` branch is skipped anyway.
  - D) Only one block of an `if / elif / else` chain runs, so the PASS line cannot also print.

**Verified output:**
```text
Invalid score; it must be between 0 and 100
```
</details>

---

### Question 50

What does this program print?

```python
passed = 22
total = 25
result = "PASS" if passed == total else "FAIL"
print(result)

temperature = 30
if 18 <= temperature <= 25:
    print("Comfortable")
else:
    print("Out of range")
```

- [ ] A) `PASS` and `Comfortable`
- [ ] B) `PASS` and `Out of range`
- [ ] C) `FAIL` and `Out of range`
- [ ] D) `FAIL` and `Comfortable`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** `22 == 25` is false, so the one-line conditional expression picks `"FAIL"`. `30` is not between 18 and 25, so the chained comparison is false and `else` runs.
- **Why others are wrong:**
  - A) Both checks are false, so neither `PASS` nor `Comfortable` appears.
  - B) `passed == total` is false, so the expression gives `"FAIL"`.
  - D) The chained comparison needs `temperature` to be at most 25, and 30 is not.

**Verified output:**
```text
FAIL
Out of range
```
</details>

---

### Question 51

What does this program print?

```python
actual_result = None
status = "BLOCKED"
filename = "login_test.py"

if actual_result is None:
    print("Test has not run yet")
if status in ("FAIL", "ERROR", "BLOCKED"):
    print("Needs attention")
if "test" in filename:
    print("This looks like a test file")
```

- [ ] A) `Test has not run yet`, `Needs attention` and `This looks like a test file`
- [ ] B) `Needs attention` and `This looks like a test file`
- [ ] C) `Test has not run yet` and `Needs attention`
- [ ] D) `This looks like a test file`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** These are three separate `if` statements, each checked independently, and all three conditions are true. `is None` detects "no value", `in` checks membership, and `"test" in filename` checks for text inside a string.
- **Why others are wrong:**
  - B) `actual_result` is `None`, so the first `if` runs too.
  - C) `"test"` appears inside `"login_test.py"`, so the third `if` also runs.
  - D) The other two conditions are also true, and nothing stops them because they are not in a chain.

**Verified output:**
```text
Test has not run yet
Needs attention
This looks like a test file
```
</details>

---

### Question 52

What does this program print?

```python
is_logged_in = True
role = "tester"

if is_logged_in:
    if role == "admin":
        print("Show admin dashboard")
    else:
        print("Show user dashboard")
else:
    print("Redirect to login page")

is_logged_in = False
if is_logged_in and role == "admin":
    print("Show admin dashboard")
elif is_logged_in:
    print("Show user dashboard")
else:
    print("Redirect to login page")
```

- [ ] A) `Show admin dashboard` and `Redirect to login page`
- [ ] B) `Show user dashboard` and `Show user dashboard`
- [ ] C) `Show user dashboard`
- [ ] D) `Show user dashboard` and `Redirect to login page`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** In the first block the user is logged in but the role is not `"admin"`, so the inner `else` prints the user dashboard. In the second block `is_logged_in` is `False`, so the first two conditions fail and the final `else` redirects to login.
- **Why others are wrong:**
  - A) `role` is `"tester"`, not `"admin"`, so the admin message never prints.
  - B) After `is_logged_in = False`, neither `and` nor `elif is_logged_in` is true.
  - C) The second block still runs and ends in its `else`.

**Verified output:**
```text
Show user dashboard
Redirect to login page
```
</details>

---

### Question 53

A test matrix tries every browser with every screen width. How many combinations does this program count?

```python
count = 0
for browser in "CF":
    for width in range(1, 4):
        count += 1
print(count)
```

- [ ] A) `5`
- [ ] B) `6`
- [ ] C) `8`
- [ ] D) `3`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** For each of the 2 browsers (the characters `C` and `F`), the inner loop runs fully through `range(1, 4)`, which is 3 widths. That gives 2 × 3 = 6.
- **Why others are wrong:**
  - A) Nested loops multiply the iteration counts; they do not add them.
  - C) That would need the inner loop to run 4 times, but `range(1, 4)` gives 1, 2 and 3.
  - D) That counts only the widths and ignores that the inner loop repeats for each browser.

**Verified output:**
```text
6
```
</details>

---

### Question 54

What does this program print?

```python
test_id = "QA-2024-v2"
letters = 0
digits = 0

for ch in test_id:
    if ch.isalpha():
        letters += 1
    if ch.isdigit():
        digits += 1

print(letters, digits)
```

- [ ] A) `3 5`
- [ ] B) `5 3`
- [ ] C) `3 7`
- [ ] D) `3 4`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A

**Explanation:** The letters are `Q`, `A` and `v` (3), and the digits are `2`, `0`, `2`, `4` and `2` (5). The hyphens are neither letters nor digits.
- **Why others are wrong:**
  - B) The numbers are swapped; there are 3 letters and 5 digits.
  - C) The two hyphens do not pass `.isdigit()`, so they are not counted.
  - D) The final `2` in `v2` is a digit too, so there are 5 digits.

**Verified output:**
```text
3 5
```
</details>

---

### Question 55

A simulated retry loop is written like this. What does it print?

```python
max_attempts = 3
attempt = 1
success = False

while attempt <= max_attempts and not success:
    print(f"Attempt {attempt}")
    if attempt == 2:
        success = True
    attempt += 1

print(attempt, success)
```

- [ ] A) `Attempt 1`, `Attempt 2`, `Attempt 3` and `4 True`
- [ ] B) `Attempt 1`, `Attempt 2` and `2 True`
- [ ] C) `Attempt 1`, `Attempt 2` and `3 True`
- [ ] D) `Attempt 1`, `Attempt 2`, `Attempt 3` and `4 False`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** On attempt 2, `success` becomes `True`, but `attempt += 1` still runs, making `attempt` 3. The condition `not success` is now false, so the loop ends without a third attempt.
- **Why others are wrong:**
  - A) Once `success` is `True`, `not success` is false, so attempt 3 never starts.
  - B) The update `attempt += 1` still runs after `success` is set, so `attempt` is 3, not 2.
  - D) Attempt 3 never runs, and `success` is `True`, not `False`.

**Verified output:**
```text
Attempt 1
Attempt 2
3 True
```
</details>

---

### Question 56

What does this program print?

```python
for n in range(1, 6):
    if n == 3:
        break
    print(n)
for n in range(1, 6):
    if n == 3:
        continue
    print(n)
```

- [ ] A) `1`, `2`, `1`, `2`
- [ ] B) `1`, `2`, `4`, `5`, `1`, `2`
- [ ] C) `1`, `2`, `1`, `2`, `3`, `4`, `5`
- [ ] D) `1`, `2`, `1`, `2`, `4`, `5`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D

**Explanation:** In the first loop, `break` at `n == 3` ends the loop, so only `1` and `2` print. In the second loop, `continue` skips just `3`, so `1`, `2`, `4` and `5` print.
- **Why others are wrong:**
  - A) `continue` does not end the second loop, so `4` and `5` still print.
  - B) The loops run one after the other in the order written, and the first loop prints `1` and `2` first.
  - C) `continue` skips the rest of the iteration for `3`, so `3` is not printed.

**Verified output:**
```text
1
2
1
2
4
5
```
</details>

---

### Question 57

A test scanner looks for the first cell where `row * col == 8` and stops both loops with a flag. What does this program print?

```python
found = False
checked = 0

for row in range(1, 6):
    for col in range(1, 6):
        checked += 1
        if row * col == 8:
            print(f"Found: row={row}, col={col}")
            found = True
            break
    if found:
        break

print(checked)
```

- [ ] A) `Found: row=2, col=4` and `4`
- [ ] B) `Found: row=2, col=4` and `9`
- [ ] C) `Found: row=2, col=4` and `25`
- [ ] D) `Found: row=2, col=4`, `Found: row=4, col=2` and `21`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B

**Explanation:** Row 1 checks all 5 columns (5 checks). In row 2, the match happens at column 4 after 4 checks, giving 9 in total. The inner `break` leaves the inner loop, and `if found: break` then leaves the outer loop.
- **Why others are wrong:**
  - A) The 5 checks of row 1 count too, not only the 4 in row 2.
  - C) That would be a full 5 × 5 scan, but both loops stop early.
  - D) That is what happens without the flag, because an inner `break` alone lets the outer loop continue; with the flag, it stops after the first match.

**Verified output:**
```text
Found: row=2, col=4
9
```
</details>

---

### Question 58

What does this program print?

```python
count = 0
while count < 6:
    count += 1
    if count == 3:
        continue
    print(count)
```

- [ ] A) `1`, `2`, `3`, `4`, `5`, `6`
- [ ] B) `1` and `2`
- [ ] C) `1`, `2`, `4`, `5`, `6`
- [ ] D) `0`, `1`, `2`, `4`, `5`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C

**Explanation:** The counter is updated before the `continue`, so skipping the print for `3` does not stop the loop from progressing. The loop prints 1, 2, 4, 5 and 6, and ends when `count` reaches 6.
- **Why others are wrong:**
  - A) `continue` skips the `print` when `count` is 3, so `3` is missing.
  - B) `continue` only skips one iteration; it does not end the loop.
  - D) `count` is incremented before it is printed, so `0` is never printed, and the loop goes on to 6.

**Verified output:**
```text
1
2
4
5
6
```
</details>

---

## Part 4: Fill-in-the-Blank

### Question 59

To count down from 5 to 1, complete the call: `for n in range(5, 0, ____):`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-1`

**Explanation:** A negative step counts down, and when counting down the start must be larger than the stop. The stop value `0` is excluded, so the loop gives 5, 4, 3, 2, 1.
</details>

---

### Question 60

A loop's ____ clause runs only if the loop finished normally without hitting `break`. It is useful for "search, and tell me if you did not find it" logic.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `else`

**Explanation:** The loop `else` block is skipped when `break` runs, so it can print a "not found" message after a search loop that completes without a match.
</details>

---

### Question 61

To stop Git tracking `debug.log` but keep the file on your disk, run: `git rm ____ debug.log`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `--cached`

**Explanation:** `--cached` limits the removal to Git's index, so the file stays on disk. Commit afterwards to record that it is no longer tracked.
</details>

---

### Question 62

`git pull` is a shortcut for `git ____` followed by `git merge`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `fetch`

**Explanation:** `git pull = git fetch + git merge`: it downloads the new commits and then merges them into your current branch.
</details>

---

### Question 63

To generate the test IDs `TC-001`, `TC-002`, ... `TC-005`, complete the f-string: `print(f"TC-{number:____}")`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `03d`

**Explanation:** The format `03d` pads the whole number with zeros to a width of 3, so `1` becomes `001`.
</details>

---

### Question 64

A `while True:` loop must contain a reachable ____ statement, otherwise it runs forever (and you would need `Ctrl + C` to stop it).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `break`

**Explanation:** `True` never becomes `False`, so only a `break` can end the loop. This pattern suits menus, prompts and loops where the exit is decided in the middle of an iteration.
</details>

---

### Question 65

To find out which rule is ignoring `debug.log`, run: `git ____ -v debug.log`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `check-ignore`

**Explanation:** `git check-ignore -v <file>` prints the rule, and the line of `.gitignore` it comes from, that is responsible for ignoring the file.
</details>

---

### Question 66

In the `.gitignore` pattern `____build/`, a leading character anchors the pattern to the repository root, so only the top-level `build` folder is ignored. Which character completes it?

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `/`

**Explanation:** A leading `/` anchors the pattern to the repo root, so `/build/` matches only the top-level `build` folder, not `src/build`.
</details>

---

### Question 67

To list the remotes configured for your repository, together with their URLs, run: `git ____ -v`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `remote`

**Explanation:** `git remote -v` (verbose) shows each remote's fetch and push URLs, for example `origin https://github.com/user/repo.git (fetch)`.
</details>

---

### Question 68

On the first push of a branch, add this flag to link your local `main` to `origin/main` so later you can type just `git push`: `git push ____ origin main`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-u`

**Explanation:** `-u` (short for `--set-upstream`) sets up tracking, so future `git push` and `git pull` need no extra arguments.
</details>

---

### Question 69

To get a copy of an existing remote repository, including its history, on your computer, run: `git ____ https://github.com/your-username/qa-practice.git`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `clone`

**Explanation:** `git clone` downloads all files and the full commit history, and sets up the remote called `origin` automatically. Use `git init` only for brand-new local projects.
</details>

---

### Question 70

Writing ____ #12 in a pull request description links issue 12 and automatically closes it when the PR is merged.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `Closes`

**Explanation:** `Closes #12` links the PR to issue 12 and closes the issue when the PR is merged.
</details>

---

### Question 71

After your PR is merged, delete the finished local branch with: `git ____ -d feature/add-login-test`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `branch`

**Explanation:** `git branch -d` only deletes a branch that has been fully merged, so it is safe. The remote copy is removed with `git push origin --delete <branch>` or GitHub's **Delete branch** button.
</details>

---

### Question 72

A pull request that is not yet ready for review can be opened as a ____ PR, and later converted with **Ready for review**.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `draft`

**Explanation:** A draft PR tells reviewers the work is still in progress. Converting it signals that it is ready for review.
</details>

---
