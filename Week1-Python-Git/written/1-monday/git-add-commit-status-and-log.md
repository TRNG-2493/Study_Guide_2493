# Git Add, Commit, Status and Log

## Learning Objectives

By the end of this lesson you will be able to:

- Use `git add` to stage a single file, several files, or all changes.
- Use `git commit -m` to save a snapshot with a meaningful message.
- Read and interpret every section of `git status` output.
- View project history with `git log` and its most useful options.
- See what changed before committing using `git diff`.
- Unstage a file with `git restore --staged`.
- Write clear, professional commit messages.
- Follow the everyday Git loop: edit, status, add, commit, log.

---

## Why This Matters

In the last lesson you created a repository and learned that Git has three areas. Today you put that model to work. The four commands in this lesson, **add**, **commit**, **status** and **log**, are the core of daily Git use. Professional developers and test engineers run them dozens of times a day.

Good commit habits are also a professional skill. A repository with clear, small commits tells the story of a project. A repository with commits like "stuff" and "fix" is a puzzle. In automation teams, other engineers will read your commit history to understand why a test was changed or when a flaky check was introduced. Today's exercise asks you to commit your test-case ID formatter in **at least three meaningful commits**, which is exactly this skill.

---

## The Concept

### 1. The Everyday Git Loop

```
   edit files ──▶ git status ──▶ git add ──▶ git commit ──▶ git log
       ▲             (look)       (stage)     (save)         (review)
       └──────────────────────────────────────────────────────────┘
```

We will walk through a complete example. Make sure you are inside a repository (for example the `qa-practice` folder from the last lesson).

---

### 2. `git status`: Know Where You Stand

```bash
git status
```

`git status` compares three things: your working directory, the staging area and the last commit. It reports differences. Run it **before and after** almost every other command; it is the safest way to avoid surprises.

Suppose you have just created `hello.py` and `README.md`:

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        README.md
        hello.py

nothing added to commit but untracked files present (use "git add" to track)
```

**Sections you may see:**

| Section header | Meaning |
|---|---|
| `Untracked files` | New files Git is not yet tracking |
| `Changes to be committed` | **Staged** changes, they will be in the next commit |
| `Changes not staged for commit` | **Modified** tracked files that are not yet staged |
| `nothing to commit, working tree clean` | Everything matches the last commit |

For a shorter view, use:

```bash
git status -s
```

Short format symbols: `??` untracked, `A` added (new and staged), `M` modified. The left column is the staging area; the right column is the working directory.

---

### 3. `git add`: Stage Changes

`git add` moves changes from the working directory to the **staging area**. It does not save anything permanently; it only says "include this in my next commit".

**Stage one file:**

```bash
git add hello.py
```

**Stage several specific files:**

```bash
git add hello.py README.md
```

**Stage everything that changed in the current folder:**

```bash
git add .
```

The dot `.` means "the current folder and everything inside it".

Now check:

```bash
git status
```

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.md
        new file:   hello.py
```

Both files are now **staged** (under "Changes to be committed").

#### Be careful with `git add .`

`git add .` is convenient but stages *everything*, including files you didn't mean to commit (temporary files, large data, secrets). Always run `git status` before committing to see exactly what is staged. Tomorrow's `.gitignore` lesson will help you keep such files out entirely. When learning, prefer naming files explicitly, so you stay aware of what you commit.

---

### 4. `git commit`: Save a Snapshot

`git commit` takes everything in the staging area and permanently records it as a **commit** in the repository.

```bash
git commit -m "Add README and hello script"
```

- `git commit` creates the commit.
- `-m` (message) lets you supply the commit message directly on the command line, in quotes.

Output:

```text
[main (root-commit) 3f2a9c1] Add README and hello script
 2 files changed, 4 insertions(+)
 create mode 100644 README.md
 create mode 100644 hello.py
```

How to read it:

- `main`: the branch you committed to.
- `(root-commit)`: this is the very first commit in the repository.
- `3f2a9c1`: the short **hash**, the commit's unique ID.
- The rest is the message and a summary: 2 files changed, 4 lines added.

Run `git status` again:

```text
On branch main
nothing to commit, working tree clean
```

**Working tree clean** means everything in your working directory matches the last commit. The staging area is empty again.

#### What if you forget `-m`?

Git opens a text editor (often Vim or Nano) so you can type a message. If you are stuck in **Vim**, press `Esc`, type `:q!` and press Enter to quit without saving. (Setting `core.editor` to VS Code, as shown in the last lesson, avoids this.) As a beginner, always use `-m`.

#### A commit is permanent history

Once committed, a snapshot is stored safely. You can edit the file as much as you like afterwards; the old snapshot remains in history and can be viewed or restored.

---

### 5. The Cycle in Action: Modify, Stage, Commit

Let's make a change. Edit `hello.py` so it contains:

```python
print("Hello from my first repo")
print("Learning Git and Python")
```

Check status:

```bash
git status
```

```text
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   hello.py

no changes added to commit (use "git add" and/or "git commit -a")
```

The file is **modified** but **not staged**. Before staging, you can see exactly what changed:

#### `git diff`: see changes

```bash
git diff
```

```diff
diff --git a/hello.py b/hello.py
index 1b2c3d4..5e6f7a8 100644
--- a/hello.py
+++ b/hello.py
@@ -1 +1,2 @@
 print("Hello from my first repo")
+print("Learning Git and Python")
```

How to read a diff:

- Lines starting with `+` (green in most terminals) were **added**.
- Lines starting with `-` (red) were **removed**.
- Lines with neither are unchanged context.

`git diff` shows changes that are *not yet staged*. To see changes that **are** staged (what will be committed), use `git diff --staged`. Reviewing your diff before committing is a very good habit; it catches accidental edits and leftover debug lines.

Now stage and commit:

```bash
git add hello.py
git commit -m "Print a second line describing the learning goal"
```

```text
[main 8d4b7e2] Print a second line describing the learning goal
 1 file changed, 1 insertion(+)
```

You now have two commits.

---

### 6. `git log`: View History

```bash
git log
```

```text
commit 8d4b7e2a1c9f3b5d6e7f8a9b0c1d2e3f4a5b6c7d (HEAD -> main)
Author: Your Name <you@example.com>
Date:   Mon Oct 5 10:42:18 2026 +0530

    Print a second line describing the learning goal

commit 3f2a9c1b8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b
Author: Your Name <you@example.com>
Date:   Mon Oct 5 10:30:02 2026 +0530

    Add README and hello script
```

Each entry shows:

- **commit + full hash:** the commit's unique ID (40 characters).
- **`(HEAD -> main)`:** `HEAD` is a pointer meaning "where you are right now". Here it points at the latest commit on `main`.
- **Author** and **Date**: who and when.
- **Message:** your description, indented.

The newest commit is at the **top**. If the history is long, press `Space` to scroll and `q` to quit the viewer.

#### Useful `git log` options

| Command | Result |
|---|---|
| `git log --oneline` | One compact line per commit: short hash and message |
| `git log -3` | Only the last 3 commits |
| `git log --stat` | Shows which files changed in each commit and how many lines |
| `git log -p` | Shows the full diff for each commit |
| `git log --author="Name"` | Only commits by that author |

```bash
git log --oneline
```

```text
8d4b7e2 (HEAD -> main) Print a second line describing the learning goal
3f2a9c1 Add README and hello script
```

`--oneline` is the one you'll use most. Compact history is easy to scan, and the messages become a readable story of the project.

---

### 7. Unstaging: Changing Your Mind Before Committing

Suppose you staged a file by mistake:

```bash
git add notes.txt
git status
```

```text
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   notes.txt
```

Git tells you the fix right in the output. To remove it from the staging area (without deleting the file or its content):

```bash
git restore --staged notes.txt
```

The file goes back to **untracked** (or **modified**). Staging is a safe preparation area, so you can add and unstage as often as you like before you commit. (Undoing *commits* and discarding changes are bigger topics we will address later; for now, just remember `--staged` only affects the staging area.)

---

### 8. Writing Good Commit Messages

A commit message explains **what** changed and **why**. Future you and your teammates depend on it.

**Guidelines:**

1. **Short summary line**, about 50 characters or fewer.
2. **Imperative mood**, as if giving a command: "Add login test", not "Added login test" or "Adding login test". A helpful trick: the message should complete the sentence *"If applied, this commit will ___."*
3. **Be specific.** Say what changed.
4. **One logical change per commit.** Don't mix a bug fix, a rename and a new feature in one commit.
5. **No vague messages.** Avoid "update", "fix", "stuff", "changes", "final".

| Poor | Better |
|---|---|
| `update` | `Add input validation to test ID formatter` |
| `fixed stuff` | `Fix zero-padding for single-digit test numbers` |
| `final version!!` | `Add summary output with pass rate` |
| `changes` | `Rename variables to snake_case` |

Plan a "story" for your commits. For the test-case ID formatter exercise, a good history might look like:

```text
c3d9a10 Add pass-rate summary output
b7e2f44 Add zero-padded test ID formatting
a1f0c93 Add prompts for module name and test number
9d8e7f6 Add README describing the formatter
```

Each commit is small, self-contained and describes a step forward.

For longer explanations, you can add a body using a second `-m`:

```bash
git commit -m "Fix zero-padding for test IDs" -m "IDs below 10 were printed as TC-7. Now padded to TC-007 using the :03d format."
```

---

### 9. How Often Should You Commit?

Commit **often**, whenever you complete a small, working step. Small commits are:

- easier to understand and review,
- easier to find problems in,
- safer: you can always return to a recent working state.

Don't commit code that is completely broken, but don't wait until "everything is finished" either.

---

### 10. Complete Walkthrough

Here's an entire session, from nothing to three commits:

```bash
mkdir id-formatter
cd id-formatter
git init

# create formatter.py with a first version of the script, then:
git status
git add formatter.py
git commit -m "Add prompts for module name and test number"

# edit formatter.py to build the ID, then:
git diff
git add formatter.py
git commit -m "Add zero-padded test ID generation"

# add a README.md, then:
git status
git add README.md
git commit -m "Add README with usage instructions"

git log --oneline
```

Result:

```text
5a1b2c3 (HEAD -> main) Add README with usage instructions
4d3e2f1 Add zero-padded test ID generation
1c2d3e4 Add prompts for module name and test number
```

---

### 11. Cheat Sheet

| Task | Command |
|---|---|
| Check what changed | `git status` |
| See line-by-line changes (unstaged) | `git diff` |
| See staged changes | `git diff --staged` |
| Stage one file | `git add file.py` |
| Stage everything | `git add .` |
| Unstage a file | `git restore --staged file.py` |
| Commit with a message | `git commit -m "message"` |
| View history | `git log` |
| Compact history | `git log --oneline` |

---

### 12. Common Problems

| Problem | Cause | Fix |
|---|---|---|
| `nothing to commit` | Nothing is staged or changed | Edit a file, then `git add` it |
| `Changes not staged for commit` after `git commit` | You forgot to `git add` the modified file | `git add file`, then commit again |
| Committed a wrong file | You used `git add .` carelessly | Check `git status` before committing; we will cover undoing commits later |
| `Please tell me who you are` | Identity not configured | `git config --global user.name` and `user.email` |
| Stuck in a text editor | Forgot `-m` | In Vim: `Esc`, then `:q!`, then retry with `-m` |
| `fatal: not a git repository` | Wrong folder | `cd` to the repo folder |
| Terminal looks frozen after `git log` | The pager is waiting | Press `q` to quit |

---

### 13. Practice Activities

Work in a fresh practice repository.

1. **First commit.** Create a repo, add `README.md` with a title and one description line, and commit it with a clear message. Run `git log` and identify the hash, author, date and message.
2. **Staging in steps.** Create two files, `a.py` and `b.py`. Stage only `a.py` and run `git status`. Which files are under which heading? Commit, then check status again.
3. **Diff reading.** Modify `a.py` (add two lines, remove one). Run `git diff` and explain every `+` and `-`.
4. **Unstage.** Stage `b.py`, then unstage it using `git restore --staged b.py`. Confirm with `git status`.
5. **Three meaningful commits.** Write a small Python script that asks for a name and prints a greeting. Build it in three commits: (1) prompts, (2) formatted greeting, (3) README. Use imperative commit messages.
6. **Compact history.** Run `git log --oneline`, `git log -2` and `git log --stat`. Describe the difference between them.
7. **Improve messages.** Rewrite these into good commit messages: `stuff`, `fixed it`, `update file`, `v2`. Invent what the change could have been.
8. **Self-check quiz.** Without looking, list the command that moves a change (a) from working directory to staging and (b) from staging to the repository.

---

## Summary

- The everyday loop: **edit, `git status`, `git add`, `git commit`, `git log`**.
- `git status` reports untracked, modified, staged and clean states. Run it often.
- `git add <file>` (or `git add .`) moves changes to the staging area; `git diff` shows what changed before you stage, and `git diff --staged` shows what you staged.
- `git commit -m "message"` permanently saves the staged snapshot; each commit has a hash, author, date and message.
- `git log` shows history, newest first; `--oneline`, `-n`, `--stat` and `-p` change the view. `q` quits the viewer.
- `git restore --staged <file>` removes a file from the staging area without losing your edits.
- Write commit messages in the imperative mood: short, specific, one logical change per commit.
- Commit small and often. Tomorrow we use `.gitignore` to keep unwanted files out and begin working with remote repositories.

---

## Additional Resources

- Pro Git book: Recording Changes to the Repository: https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository
- Pro Git book: Viewing the Commit History: https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History
- Git documentation: `git log` reference: https://git-scm.com/docs/git-log
