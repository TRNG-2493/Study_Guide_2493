# Git Merge Conflicts and Resolution

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a **merge** is and how Git performs a **three-way merge** using a common ancestor.
- Explain **why** and **when** merge conflicts happen, and why most merges do *not* produce conflicts.
- Recognise the signs of a conflict in command output (`CONFLICT`, `Automatic merge failed`) and in `git status` (`Unmerged paths`, `both modified`).
- Read **conflict markers** (`<<<<<<<`, `=======`, `>>>>>>>`) and say which side is "yours" and which is "theirs".
- Resolve a conflict step by step: inspect, edit, remove the markers, test, `git add`, `git commit`.
- Use helpful commands: `git diff`, `git diff --check`, `git checkout --ours/--theirs`, `git merge --abort`, `git log --merge`, diff3 conflict style, and merge tools.
- Handle conflicts that occur on **`git pull`** (the Monday workflow) and know the extra points that apply during a **rebase**.
- Resolve other conflict types (modify/delete, add/add) and treat special files (`requirements.txt`, test data, JSON) with care.
- Apply habits that **prevent** or **shrink** conflicts in a team that shares a test-automation repository.

---

## Why This Matters

On Monday you learned the collaborative flow: `git fetch`, `git pull` and `git push`. That flow works smoothly as long as people work on different things. Real teams, however, regularly edit the **same files**: a shared configuration file, a common test-data file, `requirements.txt`, a helper module. When two people change the **same lines** differently, Git cannot guess which version is right. It stops and asks a human. That moment is a **merge conflict**.

This is not a rare event or a sign that someone did something wrong. It is a normal part of teamwork. On a test automation team, it is *especially* common, because many engineers add tests and edit the same shared files (configuration, fixtures, page-object or helper modules, dependency lists). Therefore:

- **Fear is the main enemy.** Engineers who do not know how to resolve conflicts avoid pulling, delay merging and make their changes bigger, which makes conflicts worse. Engineers who do know how resolve them in a couple of minutes.
- **A bad resolution is a bug.** If you resolve a conflict carelessly (for example by keeping only your version), you can silently erase a colleague's work or break the test suite. Resolving correctly requires understanding both changes, then **running the tests** (today's debugging and unit-testing lessons help here).
- **Project 1 depends on it.** Today's exercise includes a *staged conflict* to resolve, and in the weeks ahead you will collaborate on the QE Foundations project in a shared repository.

This lesson fits the **Weekly Epic** ("Git moves to collaborative flows and conflict resolution"): Monday gave you the flow; today gives you the skill to keep that flow going when it is interrupted.

---

## The Concept

### 1. A quick recap: branches and merging

- A **commit** is a snapshot of your project plus a message and a pointer to its parent commit(s).
- A **branch** is a movable label pointing to a commit. Creating a branch lets you work on a change in isolation.
- **Merging** brings the work of one branch into another. You stand on the branch that should *receive* the changes (usually `main`) and run `git merge <other-branch>`.

Two shapes of merge exist:

1. **Fast-forward.** If `main` has not moved since you branched, Git simply slides the `main` label forward to your latest commit. No new commit, no possible conflict.
2. **True (three-way) merge.** If *both* branches have new commits, Git must combine the two lines of history and creates a **merge commit** with two parents.

Conflicts can only occur in the second kind.

### 2. How Git merges: the three-way merge

To merge two branches, Git finds their **merge base** (the most recent common ancestor commit) and compares three versions of every file:

```
               base  (common ancestor)
              /    \
         ours      theirs
    (current       (branch being
     branch)        merged in)
              \    /
              merged result
```

For each region of each file, Git applies simple rules:

| Base vs ours | Base vs theirs | Git's decision |
|---|---|---|
| unchanged | unchanged | Keep it |
| changed | unchanged | Take **ours** automatically |
| unchanged | changed | Take **theirs** automatically |
| changed | changed **identically** | Take that change |
| changed | changed **differently** (same lines) | **CONFLICT**: a human must decide |

So **most merges succeed automatically**, even when both branches edited the *same file*, provided they edited *different areas*. A conflict arises only when both sides changed the *same lines* (or adjacent lines, as you will see) in different ways, or when one side changed a file that the other deleted or moved.

> **Terminology: ours and theirs.** In a merge, **ours** is the branch you are *currently on* (where `HEAD` points), and **theirs** is the branch you are *merging in*. (In a rebase the meaning is reversed; see section 11.)

### 3. When do conflicts happen? Common situations

| Situation | Example |
|---|---|
| Two people edit the same line(s) | Both change `TIMEOUT = 10` to different values |
| One edits a file, another deletes it | **Modify/delete** conflict |
| Two people add a file with the same name but different content | **Add/add** conflict |
| One renames or moves a file, another edits it | Git often follows the rename, but not always |
| Both edit a generated or machine-formatted file | Dependency lock files, reformatted JSON, notebooks |
| `git pull` when you have local commits and the remote also moved | The most frequent real-life trigger |
| Re-formatting a whole file | Touches every line, so it collides with everybody |

---

## Step-by-Step: Creating and Resolving a Conflict

Everything below was run in a real scratch repository, so the output is exactly what Git prints (commit hashes and paths will differ on your machine).

### 4. Part A: Create a conflict between two branches

We will build a tiny repository, change the same line on two branches, and merge.

**Step 1: create the repository and a first commit.**

```bash
mkdir merge-demo
cd merge-demo
git init -b main
```

Create `greeting.py`:

```python
def greet(name):
    return "Hello, " + name

print(greet("QA"))
```

```bash
git add greeting.py
git commit -m "Add greeting"
```

(If `git commit` complains "Please tell me who you are", set your identity once with `git config user.name "Your Name"` and `git config user.email you@example.com`.)

**Step 2: create a feature branch and change line 2.**

```bash
git switch -c feature/polite-greeting
```

Edit line 2 of `greeting.py` to:

```python
    return "Good morning, " + name
```

```bash
git commit -am "Use polite greeting"
```

`git switch -c <name>` creates a branch and switches to it (the older equivalent is `git checkout -b <name>`). `git commit -am` stages changes to already-tracked files and commits in one step.

**Step 3: go back to `main` and change the same line differently.**

```bash
git switch main
```

Edit line 2 of `greeting.py` on `main`:

```python
    return "Hi there, " + name + "!"
```

```bash
git commit -am "Use friendly greeting"
```

Now both branches have a commit that changed line 2 differently. The history looks like this:

```
$ git log --oneline --graph --all
* b5f618c Use polite greeting      <- feature/polite-greeting
| * 81c88ae Use friendly greeting  <- main (HEAD)
|/
* 9538913 Add greeting             <- the merge base
```

**Step 4: attempt the merge.**

```bash
git merge feature/polite-greeting
```

```
Auto-merging greeting.py
CONFLICT (content): Merge conflict in greeting.py
Automatic merge failed; fix conflicts and then commit the result.
```

Read that carefully:

- `Auto-merging greeting.py`: Git tried.
- `CONFLICT (content): Merge conflict in greeting.py`: it hit a **content** conflict in that file.
- `Automatic merge failed; fix conflicts and then commit the result.`: **the merge is paused** halfway. Nothing is lost; Git is waiting for you. Your repository is now in a special "merging" state.

### 5. Part B: Look at the state of the repository

**`git status`** is your map during a conflict. Always run it first.

```bash
git status
```

```
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   greeting.py

no changes added to commit (use "git add" and/or "git commit -a")
```

- **Unmerged paths** lists the files that need your attention. `both modified` means both sides changed it. (Files Git merged cleanly are listed separately as "Changes to be committed".)
- The hints tell you the three ways forward: resolve then `git add`, then `git commit`; or `git merge --abort` to cancel.
- A compact form: `git status -s` shows `UU greeting.py` (two `U`s = unmerged on both sides).

**Open the file.** Git has written both versions into it, wrapped in **conflict markers**:

```python
def greet(name):
<<<<<<< HEAD
    return "Hi there, " + name + "!"
=======
    return "Good morning, " + name
>>>>>>> feature/polite-greeting

print(greet("QA"))
```

### 6. Reading conflict markers

| Marker | Meaning |
|---|---|
| `<<<<<<< HEAD` | **Start** of the conflict. Everything until `=======` is the version from **your current branch** (ours; `HEAD`). |
| `=======` | **Divider** between the two versions. |
| `>>>>>>> feature/polite-greeting` | **End** of the conflict. Everything between `=======` and here is the version from the **branch being merged in** (theirs). The label names that branch (or a commit id when you merged a remote-tracking ref, as in the pull example later). |

So here:

- **Ours** (`HEAD`, branch `main`): `return "Hi there, " + name + "!"`
- **Theirs** (`feature/polite-greeting`): `return "Good morning, " + name`

Everything *outside* the markers (line 1 and the `print` line) merged cleanly and needs no action. The markers are just **text inside the file**. Nothing magical: you resolve the conflict by editing the file until it contains exactly what you want and **no marker lines remain**.

> **Why not just run it?** Try `python greeting.py` on the conflicted file. Python cannot parse the markers:
>
> ```
>   File "greeting.py", line 2
>     <<<<<<< HEAD
>     ^^
> IndentationError: expected an indented block after function definition on line 1
> ```
>
> A syntax error right after a merge is a classic sign that a marker was left behind.

**See the three versions Git is comparing.** Git stores them in the index in numbered "stages" while the conflict is unresolved:

```bash
git ls-files -u
```

```
100644 9bc65696ed32f95fb9d0d73890165c5ffe5006e7 1	greeting.py     <- stage 1: the common ancestor (base)
100644 69db733cd0e832e67b6e9aa7dcb9730385bd29ec 2	greeting.py     <- stage 2: ours
100644 137970519c1ca48d8cc30024d31d93adee391707 3	greeting.py     <- stage 3: theirs
```

You can print any of them: `git show :1:greeting.py` (base), `:2:` (ours), `:3:` (theirs).

**See the combined diff:**

```bash
git diff
```

```
diff --cc greeting.py
index 69db733,1379705..0000000
--- a/greeting.py
+++ b/greeting.py
@@@ -1,4 -1,4 +1,8 @@@
  def greet(name):
++<<<<<<< HEAD
 +    return "Hi there, " + name + "!"
++=======
+     return "Good morning, " + name
++>>>>>>> feature/polite-greeting

  print(greet("QA"))
```

In this "combined diff" format there are two columns before each line (one per parent): a `+` in the first column means the line came from `HEAD`, in the second from the other branch.

**Seeing the original too (diff3 style).** By default Git shows only ours and theirs. Often you need to see what the line looked like *before* either change. Ask Git to include the base version:

```bash
git checkout --conflict=diff3 greeting.py      # re-create the markers with the base shown
# or set it permanently for all repositories:
git config --global merge.conflictstyle diff3   # (or "zdiff3", a tidier variant in newer Git)
```

```
def greet(name):
<<<<<<< ours
    return "Hi there, " + name + "!"
||||||| base
    return "Hello, " + name
=======
    return "Good morning, " + name
>>>>>>> theirs
```

Now you can see: the original was `Hello, `; one person made it friendlier, the other made it a time-of-day greeting. Knowing the original often makes the *intention* of each change clear, and with it the right resolution.

### 7. Part C: Resolve the conflict

#### The decision

Before touching the file, ask the questions that matter:

1. **What was each change trying to do?** (Read the commit messages: `git log --oneline --merge` shows only the commits involved in the conflict; add `-p` to see their diffs.)
2. **Are the two changes compatible?** Could both be kept? Is one obsolete?
3. **If unsure, ask the author.** A short message ("Which greeting should we use?") is far cheaper than guessing wrong.

There are four typical outcomes:

| Outcome | What you do |
|---|---|
| Keep **ours** | Delete theirs and the marker lines |
| Keep **theirs** | Delete ours and the marker lines |
| Keep **both** | Combine the lines (reorder, merge into one), remove the markers |
| Write something **new** | Replace the whole block with a fresh solution that satisfies both intentions |

Here we decide to combine: friendly **and** polite.

#### The resolution

Edit `greeting.py` so the conflicted section reads (note: no markers at all):

```python
def greet(name):
    return "Good morning, " + name + "!"

print(greet("QA"))
```

Check that nothing is left behind:

```bash
grep -n -E '^(<<<<<<<|=======|>>>>>>>)' greeting.py     # should print nothing
git diff --check                                        # warns about leftover markers
```

(Before resolving, `git diff --check` reports `greeting.py:2: leftover conflict marker` and so on, for each marker line; after resolving it should print nothing.)

**Run the code and the tests.** Merging is *code change*. Verify it:

```bash
python greeting.py
```

```
Good morning, QA!
```

In a real project, run your whole unit test suite here (`python -m unittest`), as you learned earlier today. A merge can produce code that has no markers but still does not work (for example, two correct changes that are incompatible together).

#### Mark it resolved and finish the merge

```bash
git add greeting.py
git status
```

```
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
	modified:   greeting.py
```

`git add` here has a special meaning: **"I have resolved this file."** It moves the file out of the "Unmerged paths" list. If you try to commit *before* resolving and adding, Git refuses:

```
error: Committing is not possible because you have unmerged files.
hint: Fix them up in the work tree, and then use 'git add/rm <file>'
hint: as appropriate to mark resolution and make a commit.
fatal: Exiting because of an unresolved conflict.
```

Now finish:

```bash
git commit
```

Git opens your editor with a pre-filled message (`Merge branch 'feature/polite-greeting'`). Keep it, or improve it (a good message mentions what you decided when it is not obvious). Use `git commit -m "Merge feature/polite-greeting: combine friendly and polite greeting"` to skip the editor. Then:

```bash
git log --oneline --graph
```

```
*   18cda24 Merge feature/polite-greeting
|\
| * b5f618c Use polite greeting
* | 81c88ae Use friendly greeting
|/
* 9538913 Add greeting
```

The merge commit has **two parents**, joining the two lines of work. The conflict is resolved and recorded in history.

### 8. The three exits from a conflicted merge

At any time during the conflict you have three choices:

| Goal | Command |
|---|---|
| **Finish** | Fix the files, then `git add <file>` for each, then `git commit` |
| **Cancel everything** and return to how things were before the merge | `git merge --abort` |
| **Take a whole file from one side** | `git checkout --ours <file>` or `git checkout --theirs <file>` (then `git add <file>`) |

`git merge --abort` is your safety net. Use it freely when you are unsure; you lose only the conflict-resolving work you did *so far*, and you can start the merge again:

```bash
git merge --abort
git status -sb
```

```
## main
```

#### Taking one side wholesale

If, for a given file, you decide one side is entirely right:

```bash
git checkout --theirs greeting.py     # whole file from the branch being merged in
cat greeting.py                       # now contains "Good morning, ", no markers
git add greeting.py
git commit
```

```bash
git checkout --ours greeting.py       # whole file from the current branch
```

Be careful: this discards the *other* side's changes to the **entire file**, including non-conflicting improvements. Use it only when you are sure (for example for a generated file you will regenerate).

*Modern equivalent:* in recent Git versions `git restore --ours <file>` / `git restore --theirs <file>` do the same job, and `git restore --merge <file>` recreates the conflict markers if you want to start over on one file.

### 9. Part D: Conflicts after `git pull` (the Monday workflow)

On Monday you learned that `git pull` is `git fetch` followed by an integration of the remote's changes into your branch (by default a merge). So conflicts show up here too, and this is the one you will meet most often at work.

**Scenario.** Alice and Bob share a repository with a `settings.py` for test configuration:

```python
BASE_URL = "https://staging.example.com"
TIMEOUT = 10
RETRIES = 3
BROWSER = "chrome"
```

1. Bob changes the timeout and retries for a slow CI server, commits, and **pushes first**: `TIMEOUT = 30`, `RETRIES = 5`.
2. Meanwhile Alice (starting from the same original file) changes `TIMEOUT = 20` and switches to `BROWSER = "firefox"`, and commits locally.
3. Alice tries to push:

```bash
git push
```

```
To /path/to/remote.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '/path/to/remote.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
```

This is **not a conflict yet**, only Git protecting the shared branch: your history and the remote's history have **diverged** (each has a commit the other lacks). Git will not let you overwrite Bob's work. You must integrate first.

```bash
git status
```

```
On branch main
Your branch and 'origin/main' have diverged,
and have 1 and 1 different commits each, respectively.
```

4. Alice pulls. (Recent Git versions require you to say how to reconcile divergent branches. If you see `fatal: Need to specify how to reconcile divergent branches`, run `git config pull.rebase false` for a merge, or pass `--no-rebase`. Your instructor or team will say which style the team uses.)

```bash
git pull
```

```
Auto-merging settings.py
CONFLICT (content): Merge conflict in settings.py
Automatic merge failed; fix conflicts and then commit the result.
```

5. `settings.py` now looks like this:

```python
BASE_URL = "https://staging.example.com"
<<<<<<< HEAD
TIMEOUT = 20
RETRIES = 3
BROWSER = "firefox"
=======
TIMEOUT = 30
RETRIES = 5
BROWSER = "chrome"
>>>>>>> b25a0a069dde262996c7eebb2bb9de816634fea0
```

Notice two things.

- **Everything is one big conflict block**, although Alice and Bob changed *different* lines in places (Alice alone changed `BROWSER`; Bob alone changed `RETRIES`). Git merges line by line and treats **adjacent changed lines as a single region**: it will not auto-merge when changed lines touch each other. So in the *conflict block* you must re-assemble the file yourself, thinking line by line.
- The end marker shows a **commit id** (`b25a0a0...`) instead of a branch name, because `git pull` merged the fetched remote commit rather than a named local branch.

6. **Decide, line by line.**

| Line | Alice (ours) | Bob (theirs) | Decision and reason |
|---|---|---|---|
| `TIMEOUT` | 20 | 30 | **30**: Bob's value is needed for the slow CI server (we confirm by messaging Bob) |
| `RETRIES` | 3 | 5 | **5**: only Bob changed it |
| `BROWSER` | `"firefox"` | `"chrome"` | **`"firefox"`**: only Alice changed it intentionally; Bob's side is just the old value |

Resolved file:

```python
BASE_URL = "https://staging.example.com"
TIMEOUT = 30
RETRIES = 5
BROWSER = "firefox"
```

7. Finish, then **push**:

```bash
git add settings.py
git commit -m "Merge origin/main: keep CI timeout 30 and firefox"
git push
```

```
To /path/to/remote.git
   b25a0a0..0fc5841  main -> main
```

The push now succeeds because Alice's history *contains* Bob's. The graph shows the diamond shape of the merge:

```
*   0fc5841 Merge origin/main: keep CI timeout 30 and firefox
|\
| * b25a0a0 Increase timeout and retries for slow CI
* | 7412254 Tune timeout and switch browser
|/
* 84cc0aa Add settings
```

**A safer habit: `fetch` first.** Instead of `git pull`, run `git fetch` and look before you merge (Monday's lesson on why fetch and pull differ pays off here):

```bash
git fetch
git log --oneline main..origin/main    # what did others do that I do not have?
git diff main origin/main              # how do their changes differ from mine?
git merge origin/main                  # now integrate, knowing what is coming
```

### 10. Other conflict types

#### Modify/delete

One branch changed a file; the other deleted it.

```
CONFLICT (modify/delete): old.txt deleted in feat and modified in HEAD.  Version HEAD of old.txt left in tree.
Automatic merge failed; fix conflicts and then commit the result.
```

`git status` shows:

```
Unmerged paths:
  (use "git add/rm <file>..." as appropriate to mark resolution)
	deleted by them: old.txt
```

There are no markers in the file; you decide:

```bash
git rm old.txt       # accept the deletion
# or
git add old.txt      # keep the file (with the modifications)
```

then `git commit`. Talk to the person who deleted it: was the file really obsolete?

#### Add/add

Both branches created a file with the same path but different content:

```
Auto-merging f.txt
CONFLICT (add/add): Merge conflict in f.txt
```

`git status -s` shows `AA f.txt`. The file contains conflict markers just like a content conflict; resolve it the same way. (Here a `git checkout --theirs f.txt` followed by `git add f.txt` is one way to finish.)

#### Rename conflicts and others

Git detects many renames automatically; rename/rename, rename/delete and directory-related conflicts exist and are reported with a `CONFLICT (...)` line naming the kind. The approach is always the same: read the message, `git status`, decide, `git add`/`git rm`, commit.

### 11. Conflicts during a rebase (brief preview)

Some teams use **rebase** instead of merge to bring in other people's work (`git pull --rebase`). A rebase *replays your commits one by one* on top of the updated branch, so a conflict can occur at each replayed commit. Resolving is the same edit-and-`git add` routine, but the finishing command differs:

```bash
git rebase main
```

```
Rebasing (1/1)Auto-merging g.txt
CONFLICT (add/add): Merge conflict in g.txt
error: could not apply 483cfd5... r1 g
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
```

Then edit the file, `git add g.txt`, and run `git rebase --continue` (or `--skip` / `--abort`). Two differences to remember:

- You do **not** run `git commit` to finish; you run `git rebase --continue`.
- **ours and theirs swap.** During a rebase, `HEAD` ("ours") is the branch you are rebasing *onto*, and "theirs" is *your own commit* being replayed. In the markers you will see `>>>>>>> 483cfd5 (r1 g)`: your commit's id and message. Do not let this trip you up when using `--ours`/`--theirs`.

We will not go deeper into rebasing here; the merge workflow above is the core skill for this week. If you ever get lost, `git rebase --abort` (or `git merge --abort`) returns you to safety.

### 12. Tools that help

- **`git status`**, **`git diff`**, **`git log --merge`** (commits involved in the conflict), **`git ls-files -u`** (unmerged files).
- **`git merge --abort`** to cancel.
- **Editors with built-in merge UI.** Visual Studio Code shows "Accept Current Change | Accept Incoming Change | Accept Both Changes | Compare Changes" links above each conflict block, and has a three-pane *merge editor*. PyCharm and other IDEs have similar three-way merge windows. These just edit the text for you; you are still responsible for deciding correctly. After using one, **re-read the result**.
- **`git mergetool`**: launches a configured external three-way merge program (for example `vimdiff`, `meld`, `kdiff3`). Configure with `git config merge.tool <name>`. It writes `.orig` backup files unless you disable that.
- **`git config rerere.enabled true`**: "reuse recorded resolution" makes Git remember how you resolved a given conflict and re-apply it automatically if the same conflict recurs (helpful in long-lived branches).

### 13. Special files in test-automation repositories

| File | Typical conflict | How to handle |
|---|---|---|
| `requirements.txt` (Monday) | Two people each add a different library on the same line area | Usually **keep both** lines; keep the list sorted; if both pin *different versions of the same package*, pick one deliberately, then re-install in a clean virtual environment and run the tests |
| Test data files (JSON, CSV) | Both add rows at the end of the file | Keep both rows; check commas in JSON (a missing or extra comma makes the file invalid). Validate by loading it with `json.load` or your loader |
| Config files | Different environment URLs or timeouts | Decide with the team which value is right; do not overwrite someone else's environment setting silently |
| Shared helper modules / fixtures | Two people extend the same function | Combine intentions; run unit tests |
| Generated or lock files (e.g. a dependency lock file, compiled output, reports) | Huge conflicts in machine-written content | **Do not hand-edit.** Take one side, then **regenerate** with the tool. Better: do not commit generated artifacts (`.gitignore`) |
| Binary files (screenshots, spreadsheets) | Cannot be merged line by line | Choose one side with `--ours`/`--theirs`, or ask the author for the correct version |

A JSON example of the "both added an item" conflict:

```
[
  {"id": 1, "user": "ann"},
<<<<<<< HEAD
  {"id": 2, "user": "bob"}
=======
  {"id": 3, "user": "cara"}
>>>>>>> origin/main
]
```

Resolution must keep both **and** fix the punctuation:

```
[
  {"id": 1, "user": "ann"},
  {"id": 2, "user": "bob"},
  {"id": 3, "user": "cara"}
]
```

Validate it afterwards:

```python
import json
with open("users.json", encoding="utf-8") as fh:
    users = json.load(fh)            # raises json.JSONDecodeError if a comma is wrong
print(len(users))                    # 3
```

(This uses the file-handling and JSON skills from Tuesday.)

### 14. Preventing conflicts (or at least making them small)

1. **Pull/fetch often.** The longer you wait, the more others' changes pile up. Start each work session with `git pull` (or `git fetch` + merge).
2. **Commit small and often; push frequently.** Small changes collide less and are easier to resolve.
3. **Use short-lived feature branches** and merge them back quickly.
4. **Talk to your team.** "I am refactoring `helpers.py` this morning" prevents two people editing it in incompatible ways.
5. **Divide the work by file/area** where possible: separate test modules per feature rather than everyone appending to one giant file.
6. **Avoid drive-by reformatting.** Re-indenting or auto-formatting a whole file touches every line and collides with everybody. Do reformatting in its own commit, announced to the team.
7. **Keep generated files out of Git** with `.gitignore` (virtual environments, `__pycache__/`, logs, reports).
8. **Keep files focused** and functions short; sprawling files attract simultaneous edits.
9. **Pull before you push** and make sure the tests pass after merging.

### 15. Common mistakes and how to avoid them

| Mistake | Consequence | Avoid it by |
|---|---|---|
| Committing the file **with markers still inside** | Broken code in the repository (`IndentationError`/`SyntaxError`, or worse, silent text in config/data) | `git diff --check`, `grep` for `<<<<<<<`, run the tests before `git add` |
| Always choosing `--ours` or `--theirs` blindly | Erases a colleague's work or your own | Read both sides; ask the author; use the tools only for whole-file decisions |
| Forgetting `git add` after fixing | Git says you are still merging and refuses to commit | `git status` after resolving |
| Not running tests after resolving | The merged code may be broken even though there were no markers | Run the suite (and the program) every time |
| Panicking and deleting the repository folder | Lose unpushed work | `git merge --abort` is the safe way out |
| Resolving while a lot of unrelated changes are uncommitted | Messy, hard to separate | Commit or stash your work **before** you merge or pull |
| Force-pushing (`git push --force`) to "get rid of" a rejected push | Overwrites others' commits on the shared branch | Never force-push a shared branch; integrate via pull/merge instead |

### 16. A conflict-resolution checklist

1. Read the Git message. Run `git status`. Note every file under **Unmerged paths**.
2. For each file: open it, find the markers, read both sides (use diff3 style if the original helps).
3. Understand each change's intent (`git log --merge -p`); ask the author if unsure.
4. Edit the file to the correct final content. **Remove all markers.**
5. Verify: `git diff --check`, run the program and the tests.
6. `git add <file>` for each resolved file; `git status` shows "All conflicts fixed".
7. `git commit` with a clear message (not needed in a rebase; use `git rebase --continue`).
8. `git push` (after pulling again if the remote moved while you worked).
9. If it all goes wrong: `git merge --abort` and start over.

---

## Code Examples

Everything in this lesson was demonstrated as shell and Git commands; the files being merged were small Python files. For quick reference, here is the whole "create and resolve a conflict" sequence as one script you can paste into a terminal (use a scratch folder):

```bash
# --- set up -------------------------------------------------------------
mkdir merge-demo && cd merge-demo
git init -b main
git config user.name "Demo"; git config user.email "demo@example.com"

printf 'def greet(name):\n    return "Hello, " + name\n\nprint(greet("QA"))\n' > greeting.py
git add greeting.py
git commit -m "Add greeting"

# --- branch: polite greeting --------------------------------------------
git switch -c feature/polite-greeting
sed -i 's/return "Hello, " + name/return "Good morning, " + name/' greeting.py
git commit -am "Use polite greeting"

# --- main: friendly greeting --------------------------------------------
git switch main
sed -i 's/return "Hello, " + name/return "Hi there, " + name + "!"/' greeting.py
git commit -am "Use friendly greeting"

# --- merge: conflict! ---------------------------------------------------
git merge feature/polite-greeting        # CONFLICT (content) ...
git status
cat greeting.py                          # see the markers

# --- resolve ------------------------------------------------------------
printf 'def greet(name):\n    return "Good morning, " + name + "!"\n\nprint(greet("QA"))\n' > greeting.py
git diff --check                         # no output = no leftover markers
python greeting.py                       # Good morning, QA!
git add greeting.py
git commit -m "Merge feature/polite-greeting: combine friendly and polite greeting"
git log --oneline --graph
```

(The `sed -i` commands are for Linux/macOS or Git Bash. On Windows without Git Bash, make the same edits manually in an editor.)

Explanation of the key parts:

- `git init -b main` starts a repository with a branch named `main`.
- `git switch -c feature/polite-greeting` creates and switches to a feature branch; `git switch main` goes back.
- The two `sed -i` edits change **the same line** in different ways on two branches. That is the essential recipe for a conflict: *same lines, different changes, both committed*.
- `git merge` fails with `CONFLICT`; the file now contains markers.
- Overwriting the file with `printf` is just a quick way of "editing the file to the correct final content" in a script.
- `git diff --check` and running the program are the verification step.
- `git add` marks it resolved, and `git commit` creates the merge commit.

---

## Summary / Key Takeaways

- A **merge** combines two lines of history using a **three-way** comparison against their common ancestor. Most merges succeed automatically.
- A **conflict** happens when both sides changed the *same (or adjacent) lines* differently, or one side deleted/renamed what the other changed. Git then **pauses** the merge and waits for you.
- Telltale signs: `CONFLICT (...)`, `Automatic merge failed`, and `git status` showing **Unmerged paths** / `both modified`.
- **Markers:** `<<<<<<< HEAD` ... `=======` ... `>>>>>>> other`. Above the divider is **ours** (current branch, `HEAD`); below is **theirs** (the incoming branch/commit). (Reversed in a rebase.)
- **Resolve** by editing the file to the correct final content, **removing every marker**, then **testing**, `git add <file>` (meaning "resolved"), and `git commit`.
- `git merge --abort` safely cancels. `git checkout --ours/--theirs <file>` takes a whole file from one side. `git diff --check` finds leftover markers. `git log --merge`, `git ls-files -u` and diff3 style (`merge.conflictstyle`) help you understand the situation.
- Conflicts after `git pull` are the most common. A rejected `git push` ("fetch first") means histories diverged; pull (merge), resolve, then push. `git fetch` + inspect first is safer.
- In test-automation repos, take extra care with `requirements.txt`, JSON/CSV test data (punctuation!), shared config, and generated files (regenerate, do not hand-merge).
- **Prevent** pain: pull often, commit small, use short branches, communicate, avoid mass reformatting, keep generated files out of Git.
- A resolution is **code you wrote**: verify it with the program and the unit tests before you commit.

---

## Practice Questions and Mini-Exercises

**Q1.** In your own words: why can Git merge two branches that edited the *same file* without a conflict, yet stops in other cases?

**Q2.** You see this in a file after a merge on `main` of branch `login-fix`:

```
<<<<<<< HEAD
timeout = 15
=======
timeout = 45
>>>>>>> login-fix
```

(a) Which value comes from `main`? (b) Which command do you run after editing the file? (c) What must the final file *not* contain?

**Q3.** `git commit` after a conflicted merge says `Committing is not possible because you have unmerged files`. What did you most likely forget?

**Q4.** What is the safest way to completely undo a merge that went wrong, as long as you have not yet committed it?

**Q5.** Your `git push` is rejected with `(fetch first)`. Is this a merge conflict? What are your next steps?

**Q6 (hands-on).** Reproduce the lesson's conflict in a scratch repository. Then (a) resolve it by keeping *only* the feature branch's line using `git checkout --theirs`, (b) abort and redo it by *combining* both greetings manually, and (c) compare the two histories with `git log --oneline --graph`.

**Q7 (hands-on, two folders simulating two teammates).** Create a bare "remote" and two clones:

```bash
git init --bare remote.git
git clone remote.git alice
git clone remote.git bob
```

In `alice`, create `settings.py` containing the four lines from section 9, commit and `git push -u origin main`. In `bob`, `git pull`. Make conflicting edits in both (same `TIMEOUT` line, different values), push from `bob`, and then try to push from `alice`. Pull, resolve the conflict, test by importing the file in Python (`python -c "import settings; print(settings.TIMEOUT)"`), commit and push.

**Q8.** This is the conflict block in `requirements.txt` after a merge. Show a correct resolution and explain what you must do afterwards.

```
requests==2.31.0
<<<<<<< HEAD
pytest==8.0.0
=======
python-dotenv==1.0.1
>>>>>>> origin/main
```

**Q9.** A teammate resolved a conflict in a Python module, committed and pushed. Now the build fails with `IndentationError` at a line that reads `=======`. What happened, and how do you prevent it?

**Q10.** Why is `git push --force` the wrong response to a rejected push on a shared branch?

**Q11.** During `git rebase main` you open the conflicted file and see markers. Which command do you run after `git add`? How does the meaning of "ours" differ from a merge?

### Answers

**A1.** Git compares each file with the **common ancestor**. If only one side changed a region, Git takes that change automatically. If both changed *different* regions (not touching each other), both changes are applied. Only when both sides changed the **same or adjacent lines** differently (or one deleted what the other changed) can it not decide which is correct, so it asks you.

**A2.** (a) `timeout = 15` (above `=======`, the `HEAD` side, the branch you are on). (b) `git add <file>` to mark it resolved, followed by `git commit` (and ideally running tests first). (c) It must not contain any marker lines (`<<<<<<<`, `=======`, `>>>>>>>`).

**A3.** You did not mark the conflicted file(s) as resolved with `git add <file>` (or `git rm <file>` for a deleted file), or you did not finish editing it. Check `git status` for "Unmerged paths".

**A4.** `git merge --abort`. It restores the state from before the merge started.

**A5.** It is not a conflict yet. It means the remote branch has commits you do not have (histories diverged). Next: `git pull` (or `git fetch` then `git merge origin/main`). If that reports a conflict, resolve it as in this lesson, commit the merge, run the tests, then `git push`.

**A6.** (a) After the conflict appears: `git checkout --theirs greeting.py`, `git add greeting.py`, `git commit -m "Merge, keep polite greeting"`. The result is `return "Good morning, " + name`. (b) Reset the demo (`git reset --hard HEAD~1` removes that merge commit in your scratch repo; do not use `--hard` casually on real work), merge again, edit the file by hand to `"Good morning, " + name + "!"`, `git add`, `git commit`. (c) Both histories have the diamond-shaped merge commit; the difference is only in the final file content. Choosing `--theirs` is fast but discards the friendly "!" from `main`; manual merging preserves both intentions.

**A7.** One possible sequence in `alice` after both pushed and pulled: `git pull` reports `CONFLICT (content): Merge conflict in settings.py`. Edit the block so only one `TIMEOUT` line remains (for example `TIMEOUT = 30` after agreeing with Bob), verify with `python -c "import settings; print(settings.TIMEOUT)"` (prints `30`), then `git add settings.py`, `git commit -m "Merge origin/main"`, `git push`. If Git says `Need to specify how to reconcile divergent branches`, run `git config pull.rebase false` first.

**A8.** Both libraries are independent additions, so **keep both** lines and remove the markers:

```
requests==2.31.0
pytest==8.0.0
python-dotenv==1.0.1
```

Afterwards, recreate or update your virtual environment (Monday) with `pip install -r requirements.txt`, check there are no version clashes, and run the tests before committing. (Keeping the list alphabetical makes future conflicts less likely.)

**A9.** The teammate committed a file that still contained a conflict marker line. Python cannot parse `=======` in the middle of code. Fix it by editing the file correctly and committing. Prevent it with `git diff --check` or `grep -rn '<<<<<<<\|>>>>>>>' .` before committing, by running the tests before `git add`, and by team habits such as code review and continuous checks.

**A10.** A force push overwrites the remote history with yours, **deleting your colleague's commits** from the shared branch (they might not even notice until later). The correct response is to integrate their work with `git pull`/`git merge` (resolving any conflicts), then push normally.

**A11.** `git rebase --continue` (not `git commit`). In a rebase, "ours" (`HEAD`) is the branch you are rebasing *onto*, and "theirs" is *your* commit that is being replayed, the opposite of a merge, where ours is your current branch.

---

## Additional Resources

- Pro Git book, "Basic Branching and Merging" (includes a section on basic merge conflicts): https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
- Git documentation, `git merge` (conflict markers, `--abort`, merge strategies): https://git-scm.com/docs/git-merge
- Git documentation, `git mergetool` (using external merge tools): https://git-scm.com/docs/git-mergetool
