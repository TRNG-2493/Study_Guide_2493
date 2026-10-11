# Interview Questions: Week 1 - Python Programming and Git Foundations

Self-quiz: read each question, say your answer aloud, check that you hit the keywords, then reveal the answer.

---

# Day 1 – Monday: Python Fundamentals & Git Intro

## Beginner (Foundational)

### Q1: Can you explain the difference between the Python interpreter, an editor like VS Code, and the terminal?
**Keywords:** interpreter, editor, terminal, runs code, write code
**Hint:** Think of who writes the code, who runs it, and where you type commands.
<details>
<summary>Click to Reveal Answer</summary>

The interpreter (for example `python` or `python3`) is the program that reads your `.py` file and executes it line by line. The editor or IDE (VS Code, PyCharm) is the application where you write code, adding colours, hints and error highlighting. The terminal is a text window (PowerShell, Terminal, bash) where you type commands such as `python hello.py`. You could write code in a plain notepad and still run it from a terminal.
</details>

---

### Q2: What is the REPL, and when would you use it instead of a script file?
**Keywords:** REPL, Read-Evaluate-Print-Loop, quick experiments, .py script, keep and rerun
<details>
<summary>Click to Reveal Answer</summary>

REPL stands for Read, Evaluate, Print, Loop. You start it by typing `python`, and at the `>>>` prompt it runs each line you type and shows the result straight away. It is ideal for quick experiments, such as checking what `10 / 4` gives. For anything you want to keep, repeat or share, you write a `.py` script file and run it with `python hello.py`.
</details>

---

### Q3: What is the difference between `=` and `==` in Python?
**Keywords:** assignment, comparison, boolean, store, equal
<details>
<summary>Click to Reveal Answer</summary>

`=` is the assignment operator. It stores the value on the right into the variable name on the left, for example `status = "PASS"`. `==` is a comparison operator that checks whether two values are equal and returns a boolean, for example `status == "PASS"` gives `True`. Mixing them up is the most common beginner mistake, and in testing `==` is the heart of comparing expected to actual.
</details>

---

### Q4: What is the difference between `/`, `//` and `%` in Python? Give me an example with 7 and 2.
**Keywords:** division, float, floor division, remainder, modulus
<details>
<summary>Click to Reveal Answer</summary>

`/` is normal division and always returns a float: `7 / 2` is `3.5`, and even `10 / 2` is `5.0`. `//` is floor division, which drops the decimal part: `7 // 2` is `3`. `%` is modulus, which gives the remainder: `7 % 2` is `1`, so `number % 2 == 0` is a classic even-number check.
</details>

---

### Q5: What is the difference between implicit conversion and explicit conversion (casting) in Python?
**Keywords:** implicit, explicit, casting, int(), automatic
<details>
<summary>Click to Reveal Answer</summary>

Implicit conversion (type coercion) is done by Python automatically when no information would be lost, for example `5 + 2.5` promotes the `int` to a `float` and gives `7.5`. Explicit conversion, or casting, is done by you by calling `int()`, `float()`, `str()` or `bool()`. Python does not implicitly convert between text and numbers, so `"42" + 8` raises a `TypeError`.
</details>

---

### Q6: What does `int(9.99)` return, and how is it different from `round(9.99)`? What about `int("3.5")`?
**Keywords:** truncates, round, ValueError, float first
<details>
<summary>Click to Reveal Answer</summary>

`int(9.99)` truncates (cuts off) the decimals and returns `9`, while `round(9.99)` returns the nearest whole number, `10`. `int("3.5")` raises a `ValueError` because a decimal string cannot be converted directly. The fix is to go through float first: `int(float("3.5"))` gives `3`.
</details>

---

### Q7: How do the `sep` and `end` options of `print()` work?
**Keywords:** sep, end, separator, newline, keyword argument
<details>
<summary>Click to Reveal Answer</summary>

`sep` sets what goes between multiple values; the default is a single space. `end` sets what comes at the end of the output; the default is a newline (`"\n"`). For example `print("2025", "06", "15", sep="-")` prints `2025-06-15`, and `print("Loading", end="...")` followed by `print("done")` prints `Loading...done` on one line.
</details>

---

### Q8: What type does `input()` return, and why does that matter?
**Keywords:** always string, int(), TypeError, convert
<details>
<summary>Click to Reveal Answer</summary>

`input()` always returns a string, even if the user types a number. So `age = input("Age: ")` followed by `age + 1` raises a `TypeError`. You convert it, for example `age = int(input("Age: "))`, which is read from the inside out: first collect the text, then convert it to an integer. Use `float(input(...))` for decimals.
</details>

---

### Q9: What is the difference between Git and GitHub?
**Keywords:** tool, online service, offline, host repositories, collaborate
<details>
<summary>Click to Reveal Answer</summary>

Git is a distributed version control system, a tool installed on your computer that tracks changes and history and works offline. GitHub (like GitLab or Bitbucket) is an online service that hosts Git repositories so you can share, back up, collaborate and review code. You can use Git without GitHub. The analogy is a word processor with change tracking versus a shared online drive.
</details>

---

### Q10: What are the three areas in Git, and which commands move changes between them?
**Keywords:** working directory, staging area, repository, git add, git commit
<details>
<summary>Click to Reveal Answer</summary>

The working directory holds the files you edit day to day. The staging area (also called the index) is where you collect the changes you have chosen for the next commit. The repository is the permanent history stored as commits (snapshots). `git add` moves changes from the working directory to the staging area, and `git commit` moves them from the staging area into the repository.
</details>

---

### Q11: What does `git init` actually do?
**Keywords:** hidden .git folder, repository, history, ls -a
<details>
<summary>Click to Reveal Answer</summary>

`git init` turns the current project folder into a Git repository by creating a hidden folder named `.git` inside it. That `.git` folder is the repository: it stores the full history and settings. You can see it with `ls -a`. You should never edit it by hand, because deleting `.git` loses all history and the folder becomes an ordinary folder again.
</details>

---

### Q12: What is the difference between `git add` and `git commit`?
**Keywords:** staging area, snapshot, permanent, -m message
<details>
<summary>Click to Reveal Answer</summary>

`git add` moves changes into the staging area. It saves nothing permanently; it just says "include this in my next commit". `git commit` takes everything in the staging area and records it permanently as a snapshot in the repository, for example `git commit -m "Add README and hello script"`. The `-m` flag supplies the message directly so Git does not open an editor.
</details>

---

### Q13: What does `git log --oneline` show, and what does `HEAD` mean in the output?
**Keywords:** short hash, one line per commit, HEAD, newest at top
<details>
<summary>Click to Reveal Answer</summary>

`git log --oneline` shows one compact line per commit with the short hash and the message, with the newest commit at the top. `HEAD` is a pointer meaning "where you are right now"; in `(HEAD -> main)` it points at the latest commit on `main`. It is the log option you will use most because compact history is easy to scan.
</details>

---

## Intermediate (Application)

### Q14: You installed Python on Windows, but typing `python --version` gives "'python' is not recognized". What is going on and how would you fix it? What if VS Code runs the wrong Python version?
**Keywords:** PATH, reinstall, py launcher, Select Interpreter, python3
**Hint:** Think about the list of folders your computer searches when you type a command.
<details>
<summary>Click to Reveal Answer</summary>

PATH is the list of folders the computer searches for a command, and Python's folder is not in it. Reinstall and tick "Add python.exe to PATH", or try the `py` launcher; on macOS and Linux the command is usually `python3`. If VS Code runs the wrong version, open the Command Palette (`Ctrl + Shift + P`), choose **Python: Select Interpreter**, and pick the Python 3 you installed.
</details>

---

### Q15: In a test, a request passes only if the status code is 200 and the response time is under 2.0 seconds. How would you write that in Python, and how does Python evaluate it?
**Keywords:** ==, <, and, boolean, comparison first
**Hint:** Comparisons give booleans, and a logical operator combines them.
<details>
<summary>Click to Reveal Answer</summary>

```python
status_code = 200
response_time = 1.2
test_passed = status_code == 200 and response_time < 2.0
print(test_passed)   # True
```

Python evaluates the two comparisons first, each giving a boolean, and then `and` combines them. `and` is `True` only when both sides are `True`. Note that `==` compares while `=` assigns.
</details>

---

### Q16: A script reads the test number and the passed/total counts with `input()`. How would you print an ID like `TC-007` and a pass rate like `88.0%`?
**Keywords:** int(), f-string, :03d, :.1%, input returns string
**Hint:** Remember what type `input()` gives you, and look at f-string format specifiers.
<details>
<summary>Click to Reveal Answer</summary>

Convert the text first with `int(input(...))`, then format with an f-string. `:03d` zero-pads an integer to width 3 and `:.1%` turns a decimal into a percentage with one decimal place.

```python
number = 7
passed, total = 22, 25
print(f"TC-{number:03d}")          # TC-007
print(f"Pass rate: {passed / total:.1%}")   # Pass rate: 88.0%
```
</details>

---

### Q17: You changed five files, but only two belong to one logical change. How would you commit just those two, and what would you check before and after?
**Keywords:** git add file, git status, git diff, focused commit, commit message
**Hint:** The staging area lets you choose what goes into the next commit.
<details>
<summary>Click to Reveal Answer</summary>

Stage only those two files by name rather than using `git add .`, then commit with a clear imperative message:

```bash
git status
git diff
git add file_a.py file_b.py
git status
git commit -m "Fix zero-padding for test IDs"
```

`git status` before and after shows what is staged, and `git diff` reviews the changes. If you staged something by mistake, `git restore --staged <file>` unstages it. This keeps each commit to one logical change.
</details>

---

## Advanced (Deep Dive)

### Q18: Why does `"10" > "9"` give `False` in Python, and what two related traps exist when converting text such as `"False"` or `"10"`? How do you fix them?
**Keywords:** character by character, text comparison, convert first, bool("False"), truthy
**Hint:** Think about how text is compared versus numbers, and what `bool()` actually checks on a string.
<details>
<summary>Click to Reveal Answer</summary>

Text is compared character by character, so `"1"` comes before `"9"` and `"10" > "9"` is `False`. Convert first: `int("10") > int("9")` is `True`. Similarly, `bool("False")` is `True` because `bool()` only checks whether the string is empty, not what it says. To get a real boolean, compare the text: `text.lower() == "true"`.
</details>

---

# Day 2 – Tuesday: Control Flow & Git

## Beginner (Foundational)

### Q1: What is a conditional statement, and what two syntax details must you get right when writing an `if`?
**Keywords:** control flow, condition, colon, indentation, block

<details>
<summary>Click to Reveal Answer</summary>

Control flow is the order in which lines execute, top to bottom by default. A conditional statement lets the program choose a path depending on a condition that is `True` or `False`. When I write `if condition:`, the colon at the end is required (forgetting it causes a `SyntaxError`), and the code that belongs to the `if` must be indented, normally 4 spaces. Python uses indentation, not curly braces, to know which lines are in the block.
</details>

---

### Q2: In an `if-elif-else` chain, how many branches can run, and why does the order of conditions matter?
**Keywords:** first match, elif, else, most specific, skipped

<details>
<summary>Click to Reveal Answer</summary>

Only one branch runs. Python checks the conditions in order, runs the first one that is true, and skips the rest of the chain. Because the first match wins, the order is part of the logic, so you order conditions from most specific to most general. You can have one `if`, any number of `elif`s, and at most one `else`, which must be last.
</details>

---

### Q3: What numbers does `range(1, 6)` produce, and what does `range(5, 0, -1)` produce?
**Keywords:** stop excluded, start, step, off-by-one, counting down
**Hint:** Think about whether the stop value is included.

<details>
<summary>Click to Reveal Answer</summary>

`range(1, 6)` produces 1, 2, 3, 4, 5. The stop value is never included, which is the classic source of off-by-one errors. `range(5, 0, -1)` uses a negative step to count down and produces 5, 4, 3, 2, 1. When counting down, the start must be larger than the stop.
</details>

---

### Q4: When would you choose a `for` loop and when a `while` loop?
**Keywords:** known count, for each, as long as, until, condition

<details>
<summary>Click to Reveal Answer</summary>

I use `for` when I know how many times to repeat or I am going through every item, such as every character of a string. I use `while` when I want to repeat as long as a condition is true and I do not know the count in advance, such as asking until the user gives valid input. A rule of thumb: "for each" or "N times" means `for`, while "as long as" or "until" means `while`. A `for` loop is usually safer because it cannot accidentally run forever.
</details>

---

### Q5: What three ingredients does a working `while` loop need, and how do you stop one that is running forever?
**Keywords:** initialization, condition, update, infinite loop, Ctrl + C

<details>
<summary>Click to Reveal Answer</summary>

It needs initialization (set up the variable the condition uses), a condition that eventually becomes false, and an update inside the loop that moves toward making it false, like `count += 1`. If you forget the update, you get an infinite loop. To stop a runaway program in the terminal, press `Ctrl + C`. A good habit is to ask: "What changes inside the loop so it will eventually stop?"
</details>

---

### Q6: What is the difference between `break` and `continue`?
**Keywords:** ends the loop, skip iteration, next iteration, after the loop

<details>
<summary>Click to Reveal Answer</summary>

`break` ends the entire loop immediately, and execution carries on with the first line after the loop. `continue` skips the rest of the current iteration and jumps to the next one, so the loop itself does not end. For example, with `break` at `number == 5` you see 1 2 3 4, but with `continue` at 5 only the 5 is skipped. Both normally sit inside an `if` within a loop.
</details>

---

### Q7: What does `git clone` do, and what is `origin`?
**Keywords:** full history, remote, origin, default branch, URL

<details>
<summary>Click to Reveal Answer</summary>

`git clone <url>` downloads a complete copy of a remote repository, including all of its history, into a new folder. It sets up a remote called `origin` that points to the URL and checks out the default branch, usually `main`. `origin` is just the conventional nickname for the remote, so I can type `git push origin main` instead of the full web address. I use `git init` for a brand-new project and `git clone` for an existing one.
</details>

---

### Q8: What is the difference between `git fetch` and `git pull`?
**Keywords:** download, merge, integrate, working files, safe

<details>
<summary>Click to Reveal Answer</summary>

Both download new commits from the remote. `git fetch` only downloads and does not change my current branch or working files, so it is safe and has no risk of conflicts. `git pull` is `git fetch` plus `git merge`, so it also integrates the changes into my current branch, and conflicts are possible. I fetch when I want to look before I integrate, and pull when I am ready to update my work.
</details>

---

### Q9: What is a `.gitignore` file, where does it live, and should you commit it?
**Keywords:** patterns, untracked, repository root, commit, teammates

<details>
<summary>Click to Reveal Answer</summary>

It is a plain text file named exactly `.gitignore` (a leading dot, no extension) that lists patterns of files and folders Git should ignore. Ignored files do not show as untracked in `git status` and are skipped by `git add .`. It normally lives in the repository root, the same folder as `.git`, and yes, it should be committed so everyone who clones the project gets the same rules.
</details>

---

### Q10: What do the patterns `*.log`, `/build`, and `!important.log` mean in a `.gitignore`?
**Keywords:** wildcard, anchored to root, negation, re-include
**Hint:** Think about `*`, a leading slash, and `!`.

<details>
<summary>Click to Reveal Answer</summary>

`*.log` ignores every file ending in `.log`, because `*` matches any number of characters. `/build` has a leading slash, which anchors it to the repo root, so it matches only a top-level `build`. `!important.log` is a negation: do not ignore this file, which re-includes it after an earlier rule like `*.log`. Lines starting with `#` are comments.
</details>

---

### Q11: What is a pull request, and what are the base and compare branches?
**Keywords:** merge request, review, base, compare, checks

<details>
<summary>Click to Reveal Answer</summary>

A pull request (PR) is a request on GitHub to merge the commits of one branch into another, usually `main`. It gives the team a page for discussion, review and automated checks. The same thing on GitLab is called a merge request (MR). The base branch is the one the changes will be merged into, usually `main`, and the compare (head) branch is the one that has my changes.
</details>

---

### Q12: Walk me through the basic pull-request workflow from start to finish.
**Keywords:** update main, branch, push, open PR, review, merge, clean up

<details>
<summary>Click to Reveal Answer</summary>

First I update `main` with `git switch main` and `git pull`. Then I create a branch with `git switch -c feature/add-login-test`, make small commits, and push the branch with `git push -u origin <branch>`. Next I open the PR on GitHub, where teammates review it and CI checks run, and I push fixes to the same branch if needed. Once it is approved and green, it gets merged, and I finish by switching to `main`, pulling, and deleting the finished branch.
</details>

---

### Q13: What are the three merge options on GitHub, and how does each affect history?
**Keywords:** merge commit, squash, rebase, linear history, one commit

<details>
<summary>Click to Reveal Answer</summary>

"Create a merge commit" keeps all the branch's commits and adds a merge commit, giving complete but busier history. "Squash and merge" combines all the branch's commits into one commit on `main`, giving one commit per PR. "Rebase and merge" replays the commits on top of `main` without a merge commit, giving a linear history. Teams usually pick one default, and many choose squash.
</details>

---

## Intermediate (Application)

### Q14: A teammate's grading code always prints "Low" when `price = 500`. What is wrong, and how do you fix it?
```python
price = 500
if price > 10:
    print("Low")
elif price > 100:
    print("Medium")
elif price > 400:
    print("High")
```
**Keywords:** order, first match wins, most specific first, elif, reorder
**Hint:** Which condition is true for 500, and which one gets checked first?

<details>
<summary>Click to Reveal Answer</summary>

`price > 10` is true for 500, and since it is checked first, that branch wins and the rest of the chain is skipped. The loosest condition is first, so the order is wrong. The fix is to order from most specific to most general: check `> 400` first, then `> 100`, then `> 10`. I ran the reordered version with `price = 500` and it prints "High".
</details>

---

### Q15: This `while` loop is meant to print 1, 3, 4, 5 and skip 2, but it hangs. Why, and how do you fix it?
```python
count = 0
while count < 5:
    if count == 2:
        continue
    print(count)
    count += 1
```
**Keywords:** continue, update, count += 1, infinite loop, before continue
**Hint:** Where does the counter get updated relative to `continue`?

<details>
<summary>Click to Reveal Answer</summary>

In a `while` loop, `continue` jumps straight back to the condition check. When `count` reaches 2, `continue` runs before `count += 1`, so `count` never changes and the loop runs forever. The fix is to update the counter before the `continue`: put `count += 1` at the top of the loop, then `if count == 2: continue`, then print. That version prints 1, 3, 4, 5, which I confirmed by running it.
</details>

---

### Q16: You commit a change and run `git push`, but it is rejected with "fetch first". What happened, and what do you do?
**Keywords:** remote has commits, pull first, push again, force, overwrite
**Hint:** Someone else may have pushed while you were working.

<details>
<summary>Click to Reveal Answer</summary>

The remote contains commits I do not have locally, for example a teammate pushed, or someone edited a file on the GitHub website. Git refuses to overwrite them. The fix is to `git pull` (fetch plus merge) and then `git push` again. I should never use `git push --force` as a quick fix, because it overwrites remote history and can destroy teammates' work.
</details>

---

### Q17: A teammate added `config.json` to `.gitignore`, but `git status` still shows their changes to it. What is wrong, and how do they fix it?
**Keywords:** already tracked, untracked only, git rm --cached, commit, keeps file on disk
**Hint:** Think about when the file was first committed.

<details>
<summary>Click to Reveal Answer</summary>

`.gitignore` only affects untracked files. If `config.json` was committed before the rule was added, Git keeps tracking it. They should run `git rm --cached config.json`, which removes it from Git's index but leaves the file on disk, then commit that change. For a folder they would add `-r`. If the file held a secret, the old commits still contain it, so they must also rotate the secret.
</details>

---

## Advanced (Deep Dive)

### Q18: Predict the output of this code and explain why. Which loop does each `break` and each `else` belong to?
```python
for row in range(1, 4):
    for col in range(1, 4):
        if row * col == 4:
            break
    else:
        print("row", row, "no match")
else:
    print("outer else")
```
**Keywords:** innermost loop, loop else, without break, completed normally
**Hint:** Work out which row hits `row * col == 4`, and ask whether the outer loop ever breaks.

<details>
<summary>Click to Reveal Answer</summary>

It prints `row 1 no match`, `row 3 no match`, then `outer else` (verified by running it). The `break` affects only the innermost loop, and a loop's `else` runs only if that loop finished without hitting `break`. For row 1 and row 3 no product equals 4, so the inner loop finishes normally and its `else` prints. For row 2, `col = 2` gives 4, so the inner `break` fires and skips the inner `else`. The outer loop never breaks, so its `else` runs at the end. To stop both loops I would need a flag variable.
</details>

---

---

# Day 3 – Wednesday: Python Data Structures & Git Branching

## Beginner (Foundational)

### Q1: What is the difference between a list and a tuple in Python, and when would you pick a tuple?
**Keywords:** mutable, immutable, ordered, parentheses, fixed data
<details>
<summary>Click to Reveal Answer</summary>

Both are ordered sequences you access by index, but a list (`[ ]`) is mutable, so you can add, remove or replace items, while a tuple (`( )`) is immutable and cannot change once created. Trying `screen_size[0] = 1366` on a tuple raises `TypeError: 'tuple' object does not support item assignment`. I would pick a tuple for data that should never change by accident, such as a screen resolution, or for one record of mixed data like `("TC-001", "Login", "High")`.
</details>

---

### Q2: A dictionary lookup `test_case["owner"]` fails with a `KeyError`. What is a safer way to read that value?
**Keywords:** `.get()`, default value, `KeyError`, `in`
<details>
<summary>Click to Reveal Answer</summary>

Use `.get()`, which returns `None` if the key is missing, or a default you choose: `test_case.get("owner", "Unassigned")` gives `"Unassigned"`. You can also check first with `"owner" in test_case`, because `in` on a dictionary checks the keys.
</details>

---

### Q3: How do you create an empty set, and why does `{}` not work?
**Keywords:** `set()`, empty dictionary, curly braces, unordered
<details>
<summary>Click to Reveal Answer</summary>

You write `set()`. Empty curly braces `{}` create an empty dictionary, not a set, because curly braces with key-value pairs are the dictionary syntax. This is a common mistake. Remember a set is unordered and unique, so it also has no index.
</details>

---

### Q4: In Python, what does `items[-1]` give you, and what happens if you ask for `items[3]` on a three-item list?
**Keywords:** index starts at 0, negative index, last item, `IndexError`
<details>
<summary>Click to Reveal Answer</summary>

`items[-1]` is the standard idiom for the last item, because negative indexes count backwards from the end. Indexing starts at 0, so a three-item list has valid indexes 0, 1 and 2, and `items[3]` raises `IndexError: list index out of range`. That is the classic off-by-one bug.
</details>

---

### Q5: Given `numbers = [10, 20, 30, 40, 50, 60]`, what do `numbers[1:4]`, `numbers[-2:]` and `numbers[::-1]` return?
**Keywords:** start included, stop excluded, last n, reversed, new list
<details>
<summary>Click to Reveal Answer</summary>

`numbers[1:4]` is `[20, 30, 40]` because the start index is included and the stop index is excluded. `numbers[-2:]` is the last two items, `[50, 60]`. `numbers[::-1]` uses a negative step to give the list reversed, `[60, 50, 40, 30, 20, 10]`. Each slice returns a new list, and the original is untouched.
</details>

---

### Q6: What is the difference between `copy = original` and `copy = original[:]` for a list?
**Keywords:** alias, same list, independent copy, `.copy()`, shallow
<details>
<summary>Click to Reveal Answer</summary>

`copy = original` copies nothing, it just gives the same list a second name, so appending through one name changes what the other sees. `original[:]` (or `.copy()`) creates a new, independent list. Be aware it is a shallow copy, so any inner lists or dictionaries are still shared.
</details>

---

### Q7: What is the difference between `append` and `extend` on a list?
**Keywords:** one item, nested list, each item, in place
<details>
<summary>Click to Reveal Answer</summary>

`append(x)` adds x as one single item at the end, while `extend(iterable)` adds each item from the other collection individually. For example:

```python
a = [1, 2]; a.append([3, 4])   # [1, 2, [3, 4]]
b = [1, 2]; b.extend([3, 4])   # [1, 2, 3, 4]
```
</details>

---

### Q8: What is the difference between `my_list.sort()` and `sorted(my_list)`, and what is wrong with `numbers = numbers.sort()`?
**Keywords:** in place, returns `None`, new list, original unchanged
<details>
<summary>Click to Reveal Answer</summary>

`.sort()` sorts the list in place and returns `None`, and it works on lists only. `sorted()` returns a new sorted list, leaves the original alone and works on any collection. So `numbers = numbers.sort()` sets `numbers` to `None`. Use `numbers.sort()` or `numbers = sorted(numbers)`.
</details>

---

### Q9: What does `Counter` do, and what do you get if you look up an item that was never counted?
**Keywords:** `collections`, counts, `most_common`, returns 0, no `KeyError`
<details>
<summary>Click to Reveal Answer</summary>

`Counter` is a special dictionary that counts how often each item appears, so `Counter(["PASS", "FAIL", "PASS"])` gives `PASS: 2, FAIL: 1`. A missing item returns `0` rather than raising a `KeyError`, and it does not add the key. `most_common(n)` returns a list of `(item, count)` tuples from highest to lowest count.
</details>

---

### Q10: Why would you use `defaultdict(list)` instead of a plain dictionary to group test IDs by module?
**Keywords:** `defaultdict`, missing key, default value, no `if` check, factory without parentheses
<details>
<summary>Click to Reveal Answer</summary>

With a plain dictionary you must check `if module not in groups` and create an empty list first. `defaultdict(list)` automatically creates an empty list whenever a missing key is accessed, so you can just write `groups[module].append(test_id)`. Note you pass `list` without parentheses, as the factory.
</details>

---

### Q11: How do you remove duplicate test IDs from a list, and what do you lose by doing it?
**Keywords:** `set()`, unique, order lost, `sorted()`
<details>
<summary>Click to Reveal Answer</summary>

Convert the list to a set with `set(raw_ids)`, because sets keep only one of each item. It is fast, but a set is unordered, so you lose the original order. Wrap it in `sorted()` for a tidy ordered list: `sorted(set(["TC-3", "TC-1", "TC-3"]))` gives `['TC-1', 'TC-3']`.
</details>

---

### Q12: In Git, what is a branch, and what is `HEAD`?
**Keywords:** pointer, commit, lightweight, current branch, isolation
<details>
<summary>Click to Reveal Answer</summary>

A branch is a movable, lightweight label that points at a commit, so creating one does not copy your files. `HEAD` is a special pointer that says where you are right now, normally the current branch. When you commit, only the current branch's pointer moves forward, so `main` stays stable while you work.
</details>

---

### Q13: What is the difference between a fast-forward merge and a three-way merge?
**Keywords:** pointer moves, diverged, merge commit, common ancestor, `--no-ff`
<details>
<summary>Click to Reveal Answer</summary>

A fast-forward happens when the target branch has not moved since you branched, so Git just slides its pointer forward and creates no new commit. A three-way merge happens when both branches have new commits (diverged), so Git uses the two tips and their common ancestor and records a new merge commit with two parents. You can force a merge commit even when a fast-forward is possible with `git merge --no-ff`.
</details>

---

## Intermediate (Application)

### Q14: Your plan says 5 tests should run and the results show which ran. How would you find the tests that were missed and any that ran but were not planned?
**Keywords:** sets, difference, `-` operator, planned, executed
**Hint:** Which data structure answers "what is in one group but not the other"?
<details>
<summary>Click to Reveal Answer</summary>

Put both in sets and use set maths. `planned - executed` gives the tests you forgot to run, and `executed - planned` gives tests that ran unexpectedly. `planned & executed` gives the completed ones.

```python
planned  = {"TC-001", "TC-002", "TC-003"}
executed = {"TC-002", "TC-099"}
print(sorted(planned - executed))   # ['TC-001', 'TC-003']
print(sorted(executed - planned))   # ['TC-099']
```
</details>

---

### Q15: You want to print the last two log lines before an ERROR appears, without keeping the whole log in memory. What would you use?
**Keywords:** `deque`, `maxlen`, old items fall off, `append`
**Hint:** Think of a container that automatically drops its oldest item when full.
<details>
<summary>Click to Reveal Answer</summary>

Use `collections.deque(maxlen=2)`. When a new item is appended and it is full, the oldest one falls off automatically. Before appending each line, check whether it starts with `ERROR` and, if so, print `list(history)`:

```python
history = deque(maxlen=2)
for line in ["INFO start", "INFO login", "INFO search", "ERROR crash"]:
    if line.startswith("ERROR"):
        print(list(history))   # ['INFO login', 'INFO search']
    history.append(line)
```
</details>

---

### Q16: You run `git merge feature/firefox` and Git reports `CONFLICT (content)`. Walk me through what happened and how you resolve it.
**Keywords:** same lines, conflict markers, edit, `git add`, `git commit`, `--abort`
**Hint:** Think about the three marker lines Git puts into the file and what you must do before committing.
<details>
<summary>Click to Reveal Answer</summary>

Both branches changed the same lines differently, so Git cannot decide and asks a human. It is not an error and nothing is broken. I open the file, decide the final code and remove the `<<<<<<< HEAD`, `=======` and `>>>>>>>` marker lines, then run `git add <file>` and `git commit` to complete the merge, and finally run the tests. If unsure, `git merge --abort` returns to the state before the merge.
</details>

---

### Q17: You have default settings and a smaller set of per-run overrides. How do you merge them without changing the defaults?
**Keywords:** `.copy()`, `update`, overwrite, new keys, defaults unchanged
**Hint:** Which dictionary method adds new keys and overwrites existing ones, and what should you do first to protect the original?
<details>
<summary>Click to Reveal Answer</summary>

Copy the defaults first, then call `update` on the copy, which adds new keys and overwrites existing ones:

```python
defaults  = {"browser": "Chrome", "timeout": 30, "headless": False}
overrides = {"browser": "Firefox", "headless": True}
settings = defaults.copy()
settings.update(overrides)
# {'browser': 'Firefox', 'timeout': 30, 'headless': True}; defaults is unchanged
```
</details>

---

## Advanced (Deep Dive)

### Q18: A list of test-case dictionaries has two rows with the same `id`. Why does `set(rows)` fail, and how do you de-duplicate by ID while keeping the first occurrence in order?
**Keywords:** unhashable, mutable, `seen` set, `continue`, first-seen order
**Hint:** Ask what kind of objects a set is allowed to hold, then track just one field of each record.
<details>
<summary>Click to Reveal Answer</summary>

`set(rows)` raises `TypeError: unhashable type: 'dict'` because dictionaries are mutable, and set members must be immutable (hashable). Instead keep a `seen` set of just the IDs and a result list. Skip any row whose ID was already seen, so the first one wins and the original order is kept:

```python
seen_ids, unique_rows = set(), []
for row in rows:
    if row["id"] in seen_ids:
        continue
    seen_ids.add(row["id"])
    unique_rows.append(row)
```
</details>

---

# Day 4 – Thursday: Functions & Reusable Programming

## Beginner (Foundational)

### Q1: What is the difference between defining a function and calling it, and what happens if you try to call a function before it is defined?
**Keywords:** def, call, parentheses, NameError, top to bottom
**Hint:** Think about what Python does when it reads a `def` line versus `name()`.
<details>
<summary>Click to Reveal Answer</summary>

Defining a function with `def` only makes Python remember it under that name; nothing inside runs. Calling it, by writing the name followed by parentheses, is what actually executes the body. Without the parentheses you just refer to the function object and nothing happens. Python reads top to bottom, so calling `greet()` before its `def` raises a `NameError`.
</details>

---

### Q2: What is a docstring, where does it go, and how is it different from a comment?
**Keywords:** triple quotes, first statement, help(), describes function, comment
<details>
<summary>Click to Reveal Answer</summary>

A docstring is a triple-quoted string placed as the first statement in a function body that documents what the function does. Editors show it on hover and `help(function_name)` prints it. A comment (`#`) explains one specific line of code, whereas a docstring describes the whole function from the outside. A good one starts with a short imperative summary like "Return the pass rate."
</details>

---

### Q3: What is local scope? If I create a variable inside a function and print it outside, what happens, and why is that considered a feature?
**Keywords:** local, NameError, disappears, global, LEGB
<details>
<summary>Click to Reveal Answer</summary>

A variable created inside a function is local: it exists only while the function runs, so using it outside raises a `NameError`. This is a feature because two functions can each have their own `count` without overwriting each other. Globals can be read inside a function, but assigning to the name creates a new local, which can give an `UnboundLocalError`. Python looks names up in the order Local, Enclosing, Global, Built-in (LEGB).
</details>

---

### Q4: Explain the difference between a parameter and an argument. How do positional and keyword arguments differ?
**Keywords:** parameter, argument, positional, keyword, order
<details>
<summary>Click to Reveal Answer</summary>

A parameter is the variable name in the `def` line, like `name` in `def greet(name)`. An argument is the actual value you pass in the call, like `"Priya"`. Positional arguments are matched by order, so swapping them silently swaps their meaning. Keyword arguments (`status="PASS"`) are matched by name so order does not matter, and when mixing them, positional ones must come first.
</details>

---

### Q5: What is the difference between `print` and `return` in a function? What does a function give back if it has no `return`?
**Keywords:** return, print, None, reuse, ends the function
**Hint:** Which one lets the caller store and reuse the result?
<details>
<summary>Click to Reveal Answer</summary>

`print` only displays text for a human, while `return` sends a value back to the caller and ends the function immediately. A returned value can be stored, calculated with, or asserted in a test. A function with no `return` quietly gives back `None`, which is why this classic bug happens:

```python
def square(n):
    n * n          # calculated then thrown away

print(square(4))   # None
```

The rule of thumb is that functions that calculate or decide should return, and the caller decides whether to print.
</details>

---

### Q6: How do default parameter values work, and what is the ordering rule for parameters with and without defaults?
**Keywords:** default, optional, required, SyntaxError, keyword
<details>
<summary>Click to Reveal Answer</summary>

A default is set in the `def` line with `=`, and Python uses it when the caller doesn't supply that argument, so the common case stays short. Parameters without defaults must come before those with defaults, otherwise you get a `SyntaxError`. For example, `def greet(name, greeting="Hello")` is fine, but `def broken(greeting="Hello", name)` is not. Keyword arguments let you override just one default and leave the others alone.
</details>

---

### Q7: What do `*args` and `**kwargs` do in a function definition, and what types are they inside the function?
**Keywords:** *args, **kwargs, tuple, dictionary, extra arguments
<details>
<summary>Click to Reveal Answer</summary>

`*args` gathers all extra positional arguments into a tuple, and `**kwargs` gathers all extra keyword arguments into a dictionary. Zero extra arguments is fine; you just get an empty tuple or dict. The required order is: required, defaults, `*args`, keyword-only, `**kwargs`. A caution is that `**kwargs` hides which options are valid, so a typo like `rol="admin"` passes silently.
</details>

---

### Q8: What is the mutable default argument trap, and how do you fix it?
**Keywords:** mutable, default, evaluated once, None, shared list
**Hint:** When does Python create the default value, at definition time or at call time?
<details>
<summary>Click to Reveal Answer</summary>

Default values are created once, when the function is defined, not on every call. With a mutable default like `results=[]`, every call that doesn't pass its own list shares the same list, so results leak between calls. The fix is to use `None` as the default and create the list inside:

```python
def add_result(result, results=None):
    if results is None:
        results = []
    results.append(result)
    return results
```

Each call now gets a fresh list.
</details>

---

### Q9: What is a lambda function, and what are its syntax rules?
**Keywords:** anonymous, one expression, no return, lambda parameters, automatically returned
<details>
<summary>Click to Reveal Answer</summary>

A lambda is a small anonymous function written in a single expression: `lambda parameters: expression`. The expression's value is returned automatically, so you never write `return`. It can take zero, one or several parameters, and can use a one-line conditional such as `lambda s: "PASS" if s >= 50 else "FAIL"`. It cannot contain statements like loops, assignments or `if` blocks.
</details>

---

### Q10: When would you choose a regular `def` over a lambda? Name some limitations of lambdas.
**Keywords:** one expression, docstring, readability, reuse, `<lambda>`
<details>
<summary>Click to Reveal Answer</summary>

Use a lambda when the logic is one short, obvious expression used once inline, like a sort key. Use `def` when you need several statements, a docstring, a descriptive name, or reuse in several places. Lambdas allow only one expression, have no docstrings or annotations, and show up as `<lambda>` in tracebacks, which makes debugging harder. A good test is that if you have to think hard to read the lambda, write a named function.
</details>

---

### Q11: What is a closure? Can you give a simple example and say what `nonlocal` is for?
**Keywords:** inner function, enclosing scope, remembers, nonlocal, outer function finished
**Hint:** Think about `make_multiplier(2)`. The outer function has finished, so how does the result still know the factor?
<details>
<summary>Click to Reveal Answer</summary>

A closure is an inner function that remembers the variables of the enclosing scope it was created in, even after the outer function has finished. Each call to the outer function creates a separate inner function with its own remembered values.

```python
def make_range_checker(lo, hi):
    def check(v):
        return lo <= v <= hi
    return check

is_valid_port = make_range_checker(1, 65535)
is_valid_port(8080)    # True
```

Inner functions can read outer variables freely, but to reassign one you must declare it `nonlocal`, as in a counter that does `count += 1`.
</details>

---

### Q12: What is a decorator, and what does the `@` line above a function actually do? Why should you use `@wraps`?
**Keywords:** decorator, wrapper, func = decorator(func), *args/**kwargs, functools.wraps
<details>
<summary>Click to Reveal Answer</summary>

A decorator is a function that takes a function, wraps extra behaviour around it, and returns the wrapper. The `@decorator` line is just shorthand for `func = decorator(func)` after the definition. The standard template has a `wrapper(*args, **kwargs)` that does something before, calls `func`, does something after, and returns the result. Always add `@wraps(func)` to the wrapper, otherwise the decorated function's `__name__` becomes `wrapper` and its docstring is lost.
</details>

---

### Q13: What does `if __name__ == "__main__":` do, and why is it useful in a utility module?
**Keywords:** `__name__`, `__main__`, imported, run directly, library and script
<details>
<summary>Click to Reveal Answer</summary>

When you run a file directly, `__name__` is `"__main__"`; when another file imports it, `__name__` is the module's name. So code under this guard runs only when the file is executed directly, not on import. That lets one file be both a library and a script, and stops demo or self-check code from running every time someone imports your module.
</details>

---

## Intermediate (Application)

### Q14: A teammate writes `add_test(queue, test_id)` that does `queue.append(test_id)`, and is surprised when their original list changes. Why does this happen, and how would you rewrite it so the original is untouched?
**Keywords:** mutable, same object, reference, copy, return new value
**Hint:** Reassigning a parameter and mutating the object it points to behave differently.
<details>
<summary>Click to Reveal Answer</summary>

Parameters are local names, but with mutable objects like lists the function receives a reference to the same object, so in-place operations like `append` change the caller's list. Reassigning the parameter itself would only rebind the local name and not affect the caller. To avoid surprises, work on a copy and return a new value:

```python
def with_extra(ids, extra):
    new_list = ids.copy()
    new_list.append(extra)
    return new_list
```

If a function must modify its input, say so in its name and docstring.
</details>

---

### Q15: You have a list of test-case dictionaries with `priority` and `duration` keys. How would you sort them by priority ascending and, within each priority, longest duration first? How would you find the slowest test?
**Keywords:** sorted, key, lambda, tuple, negate, max
**Hint:** Python compares tuples element by element. How can you flip one number's direction?
<details>
<summary>Click to Reveal Answer</summary>

Pass a lambda as the `key` that returns a tuple, negating the number you want descending:

```python
sorted(cases, key=lambda c: (c["priority"], -c["duration"]))
max(cases, key=lambda c: c["duration"])   # slowest test
```

The tuple lets the second item break ties in the first. `sorted` returns the original items, and the key only decides the order. Note that you pass the function (`key=lambda...`), you don't call it.
</details>

---

### Q16: You're asked to write `is_valid_test_id` for IDs like `TC-007`. Walk me through the checks and which edge cases you would test with `assert`.
**Keywords:** startswith, isdigit, len, edge cases, assert
**Hint:** Think normal, boundary, invalid and empty inputs.
<details>
<summary>Click to Reveal Answer</summary>

I'd use guard clauses: return `False` if it doesn't start with `"TC-"`, then check the rest is all digits and has exactly 3 characters.

```python
def is_valid_test_id(test_id, prefix="TC", digits=3):
    start = f"{prefix}-"
    if not test_id.startswith(start):
        return False
    number = test_id[len(start):]
    return number.isdigit() and len(number) == digits
```

I'd assert the normal case (`"TC-007"`), and that `"TC-7"`, `"TC-ABC"`, `"XX-007"`, `""` and a trailing-space `"TC-007 "` are rejected. Whether lowercase `"tc-007"` is valid is a decision I'd make, document, and keep consistent.
</details>

---

### Q17: Your test uses random data and fails only sometimes, and nobody can reproduce it. How would you fix that in a data generator?
**Keywords:** seed, reproducible, random.Random, same data, log the seed
**Hint:** How can "random" output repeat exactly?
<details>
<summary>Click to Reveal Answer</summary>

Use a seed so the random sequence is repeatable, and either log the seed or let the caller pass one in. A private generator keeps your function from interfering with the global one:

```python
def generate_usernames(count, seed=None):
    rng = random.Random(seed)
    return [f"user{rng.randint(1000, 9999)}" for _ in range(count)]
```

Calling it with `seed=7` always gives the same three names, so a failing run can be replayed with identical data. `random` is fine for test data but not secure for real passwords.
</details>

---

## Advanced (Deep Dive)

### Q18: Explain how `@max_seconds(0.1)` works when a decorator takes its own argument. Why does it need three nested functions, and what is it equivalent to?
**Keywords:** three layers, returns decorator, closure, `repeat(3)(func)`, wrapper
**Hint:** `@repeat(3)` first calls something, then applies the result to your function. What does the first call return?
<details>
<summary>Click to Reveal Answer</summary>

There are three layers: the outer function receives the decorator's argument (`limit`), it returns the real decorator that receives the function, and that returns the wrapper that receives the call's arguments. `@max_seconds(0.1)` first calls `max_seconds(0.1)`, which returns `decorator`, and Python then applies that to the function, so it equals `func = max_seconds(0.1)(func)`. The wrapper is a closure that remembers both `limit` and `func`, which is how it can time the call and print a warning if `elapsed > limit`. A common mistake is writing `@max_seconds` without the parentheses, which passes the function in as the limit.
</details>

---

# Day 5 – Friday: Object-Oriented Programming

## Beginner (Foundational)

### Q1: In your own words, what is the difference between a class and an object?
**Keywords:** blueprint, instance, instantiation, own data, TestCase
**Hint:** Think of a house plan versus the actual houses built from it.
<details>
<summary>Click to Reveal Answer</summary>

A class is a blueprint or template that defines what data (attributes) and behaviour (methods) its objects have. An object, also called an instance, is one concrete thing built from that class by calling it, for example `case_1 = TestCase()`. One class can produce as many objects as you like, and each object has its own data.
</details>

---

### Q2: What is `self` in a method, and do you pass it when you call the method?
**Keywords:** first parameter, the object, passed automatically, convention
**Hint:** Compare `case_1.mark_passed()` with `TestCase.mark_passed(case_1)`.
<details>
<summary>Click to Reveal Answer</summary>

`self` is the first parameter of every instance method, and inside the method it refers to the object the method was called on. You write it in the `def` line but you do not pass it, because Python passes the object automatically. That is why `self.status = "PASS"` changes the status of that particular test case. `self` is a naming convention rather than a keyword, but everyone uses it.
</details>

---

### Q3: What is the difference between `is` and `==` for two objects of your own simple class?
**Keywords:** identity, same object, equal, default, reference
**Hint:** What happens to `y` after `y = x` and then `y.status = "PASS"`?
<details>
<summary>Click to Reveal Answer</summary>

`is` checks identity, meaning whether two names refer to literally the same object. For your own simple classes `==` also defaults to identity unless you define equality yourself, so two separate objects holding the same data are not equal. And `y = x` is not a copy: both names point to one object, so a change through `y` shows up through `x`.
</details>

---

### Q4: What does `__init__` do, and why do we write `self.id = test_id` rather than just `id = test_id`?
**Keywords:** constructor, runs automatically, parameter, attribute, local variable
**Hint:** Which one disappears when the method ends?
<details>
<summary>Click to Reveal Answer</summary>

`__init__` is the constructor. Python runs it automatically when you create an object, and its job is to set up the object's starting attributes. `test_id` is a parameter, a local variable that disappears when `__init__` ends, while `self.id` is an attribute attached to the object that lives as long as the object does. Writing `id = test_id` without `self.` only creates a throw-away local, so you would later get an `AttributeError`. Also, `__init__` should not return a value.
</details>

---

### Q5: What is the difference between `__str__` and `__repr__`? If you can only define one, which should it be?
**Keywords:** readable, developer, print, list, debugging
**Hint:** Think about what you see when you print a list of objects.
<details>
<summary>Click to Reveal Answer</summary>

`__str__` is the friendly, human-readable description used by `print()`, `str()` and f-strings. `__repr__` is the developer description, used when the object appears inside a list, in the REPL or in debugging output, and by convention it looks like the code that would recreate the object. If you define only one, define `__repr__`, because it is the most useful for debugging and `print` falls back to it. Both must return a string rather than print one.
</details>

---

### Q6: What is the difference between a class variable and an instance variable?
**Keywords:** class body, `self`, shared, one copy, per object
**Hint:** Where in the code is each one defined?
<details>
<summary>Click to Reveal Answer</summary>

An instance variable is created with `self.name = ...`, usually in `__init__`, and each object gets its own copy. A class variable is assigned directly in the class body, outside any method, and there is one copy shared by all objects. Use instance variables for data that differs per object (ID, title, status) and class variables for things common to all, like constants, defaults and counters.
</details>

---

### Q7: When you read `case.valid_statuses`, in what order does Python look for the attribute?
**Keywords:** instance, class, parent classes, first match, `__dict__`
<details>
<summary>Click to Reveal Answer</summary>

Python searches the instance itself first (`case.__dict__`), then the instance's class (`TestCase.__dict__`), then the parent classes following the MRO, and stops at the first match. For a class variable that was never assigned on the instance, the instance lookup misses and the class supplies the value. This lookup order explains every class-variable surprise.
</details>

---

### Q8: How does Python signal public, protected and private attributes? Is `__name` truly private?
**Keywords:** underscore, convention, name mangling, `_ClassName__name`, not enforced
**Hint:** Look at what `__dict__` shows for a double-underscore attribute.
<details>
<summary>Click to Reveal Answer</summary>

Python relies on convention: `name` is public, `_name` is protected (internal, a polite warning that is not enforced), and `__name` is private-ish. A double underscore triggers name mangling, so Python renames it to `_ClassName__name`. It is still reachable (`acc._Account__balance`), so it is not truly private or secure. Beginners should default to a single underscore for internals.
</details>

---

### Q9: How do you make an attribute read-only in Python, and what happens if someone tries to assign to it?
**Keywords:** `@property`, getter, no setter, `AttributeError`, underscore attribute
<details>
<summary>Click to Reveal Answer</summary>

Store the real value in an internal attribute like `_test_id` and expose it with a `@property` getter only. Because no setter is defined, assigning to it raises an `AttributeError` (for example "property 'test_id' of 'TestResult' object has no setter"). It is a simple way to say "this must never change after creation", such as for an ID. Note you read it without parentheses: `result.test_id`.
</details>

---

### Q10: What is inheritance, and why do we call `super().__init__(...)` in a child's constructor?
**Keywords:** is-a, parent, child, `super()`, parent attributes
**Hint:** What would be missing from the object if the parent's setup never ran?
<details>
<summary>Click to Reveal Answer</summary>

Inheritance lets a child (subclass) reuse and extend a parent (base class), modelling an "is-a" relationship such as `UITest` is a `TestCase`. If the child defines its own `__init__`, it must call `super().__init__(...)` so the parent's constructor runs on the same object and sets up inherited attributes like `id`, `title` and `status`. Forgetting it means those attributes are never created, and you get an `AttributeError` later. Do not pass `self` explicitly to `super().__init__`.
</details>

---

### Q11: What is polymorphism, and why does it make a test framework easier to extend?
**Keywords:** same method call, different behaviour, overriding, `run()`, no `if` chain
<details>
<summary>Click to Reveal Answer</summary>

Polymorphism means the same method call behaves differently depending on the object's class, which is the payoff of overriding. You can put `UITest` and `APITest` objects in one list and call `test.run()` on each without checking their types. Adding a new kind of test, such as `DatabaseTest`, needs only a new class with its own `run`, and the loop does not change.
</details>

---

### Q12: What are the three kinds of methods in a class, and what does each receive as its first argument?
**Keywords:** instance method, `self`, `@classmethod`, `cls`, `@staticmethod`
<details>
<summary>Click to Reveal Answer</summary>

An instance method has no decorator and receives `self`, the object, so it works with one object's data. A class method uses `@classmethod` and receives `cls`, the class itself, which makes it good for alternative constructors and class-level data. A static method uses `@staticmethod` and receives nothing automatic, so it is a plain helper function filed inside the class.
</details>

---

### Q13: When would you write a static method such as `TestCase.is_valid_id(test_id)` instead of a normal function outside the class?
**Keywords:** `@staticmethod`, no `self`, related to the class, namespacing, module-level function
**Hint:** Does the check need a particular test case object?
<details>
<summary>Click to Reveal Answer</summary>

Use a static method when the helper needs neither the object nor the class but is closely tied to that class. `TestCase.is_valid_id("TC-007")` tells the reader which concept the check belongs to, and it travels with the class. It can be called on the class or on an instance. If the helper is general-purpose and used by many unrelated classes, keep it as a module-level function instead.
</details>

---

## Intermediate (Application)

### Q14: A teammate's `TestCase.__init__` sets `id`, `title` and `status`, but `failure_reason` is only created inside `mark_failed()`. What goes wrong, and how do you fix it?
**Keywords:** `AttributeError`, `__init__`, same shape, starting value, all attributes
**Hint:** What does a Reporter see for a test that passed and never called `mark_failed`?
<details>
<summary>Click to Reveal Answer</summary>

Only failed tests would have `failure_reason`, so any code (say a `Reporter` printing reasons for every test) hits an `AttributeError` on tests that passed or were never run. The rule is to define all of an object's attributes in `__init__` so every object has the same shape. Fix it by adding `self.failure_reason = ""` in the constructor, and `mark_failed(self, reason="")` then simply updates it.
</details>

---

### Q15: Your team keeps finding reports with a status like `"PSAS"`. How would you make `TestCase.status` reject bad values, and where must the constructor assign it?
**Keywords:** `@property`, `@status.setter`, `ValueError`, `_status`, `VALID_STATUSES`
**Hint:** Which attribute holds the real data, and which name does the outside world use?
<details>
<summary>Click to Reveal Answer</summary>

Store the real value in `self._status` and expose `status` as a `@property` with an `@status.setter` that checks the value against `VALID_STATUSES` and raises `ValueError` if it is not allowed. Then `case.status = "PSAS"` fails loudly at the exact line where the typo happens, and the old value is kept. In `__init__`, assign through the public name (`self.status = ...`) so the construction is validated too. The getter must return `self._status`, not `self.status`, or you get infinite recursion.
</details>

---

### Q16: You have a `TestSuite.run_all()` that loops over tests and calls `test.run()`. Someone adds a `DatabaseTest` subclass but forgets to define `run`. What happens, and what do you change in the base class to make the failure obvious?
**Keywords:** `NotImplementedError`, override, base class, polymorphic call, clear message
**Hint:** What should the parent's `run()` do when it has no sensible default?
<details>
<summary>Click to Reveal Answer</summary>

`TestSuite` does not need to change, since it only relies on each test having `run()`. If the base `TestCase.run` raises `NotImplementedError("Subclasses must implement run()")`, then calling `run()` on the incomplete subclass fails immediately with that clear message instead of mysteriously later. If a subclass does override `run` properly, the suite just works with no edits.
</details>

---

### Q17: You write `TestCase.from_dict(data)` that ends with `return TestCase(...)`. A teammate calls `UITest.from_dict(...)`. What type do they get, and how do you fix it?
**Keywords:** `cls`, factory method, `@classmethod`, subclass, hard-coded class name
**Hint:** What does `cls` refer to when a subclass calls an inherited class method?
<details>
<summary>Click to Reveal Answer</summary>

They get a plain `TestCase`, because the class name is hard-coded, so subclasses wrongly receive parent objects. Make it `@classmethod def from_dict(cls, data): return cls(data["id"], data["title"], ...)`. When called through `UITest`, `cls` is `UITest`, so the factory builds a `UITest`. This is why alternative constructors should use `cls(...)`.
</details>

---

## Advanced (Deep Dive)

### Q18: A `Counter` class has `count = 0` in the class body and `increment(self)` does `self.count += 1`. After `a.increment()` twice and `b.increment()` once, what do `a.count`, `b.count` and `Counter.count` print, and why? How do you fix it?
**Keywords:** shadowing, instance variable, class variable, `self.count = self.count + 1`, `ClassName.count`, `__dict__`
**Hint:** `+=` first reads, then assigns. Which name does the assignment create, and where?
<details>
<summary>Click to Reveal Answer</summary>

It prints `2 1 0`. `self.count += 1` means `self.count = self.count + 1`: Python reads `count`, finding the class value 0, then assigns to `self.count`, which creates a new instance variable that shadows the class variable. So `a.__dict__` is `{'count': 2}`, `b` gets its own count of 1, and `Counter.count` never changes. To change the shared counter, modify it through the class name: `Counter.count += 1` (or via a class method using `cls`).
</details>

---

---

