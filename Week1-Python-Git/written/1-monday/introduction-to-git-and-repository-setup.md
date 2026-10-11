# Introduction to Git and Repository Setup

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what version control is and the problems it solves.
- Describe what Git is, and explain the difference between **Git** and **GitHub**.
- Install Git and verify the installation.
- Configure your identity (`user.name`, `user.email`) and a default branch name.
- Explain the three areas of Git: **working directory**, **staging area** and **repository**.
- Create a new repository with `git init` and describe what the hidden `.git` folder is.
- Use `git status` to inspect a new repository.
- Use `git help` to look up commands.

---

## Why This Matters

Imagine you are writing a test script. It works on Monday. On Tuesday you "improve" it, and now it is broken. You can't remember exactly what you changed. Or you and a teammate both edit the same file and one of you overwrites the other's work. Or a manager asks, "Who changed this test, and why?"

Without version control, people cope with folders called `tests_final`, `tests_final_v2`, `tests_final_v2_REALLY_FINAL`. That is slow, error-prone and impossible for a team.

**Git** solves these problems. It is the industry-standard tool for tracking changes in files, and nearly every software team, including every QA and automation team, uses it. Test automation code is *real code*: it lives in repositories, is reviewed by teammates and runs in automated pipelines that fetch it from Git.

This week you will build a Git habit alongside learning Python. Today's lessons give you the foundation: create a repository and record history. Later this week (and in later weeks) you will collaborate with others using remote repositories, branches and pull requests.

---

## The Concept

### 1. What Is Version Control?

**Version control** (also called source control) is a system that records changes to files over time so that you can:

- **See history:** what changed, when, by whom and why.
- **Go back:** restore an earlier working version if something breaks.
- **Compare:** see exactly what is different between two versions.
- **Collaborate:** let many people work on the same project without overwriting each other.
- **Experiment safely:** try an idea and discard it without risk (this uses branches, covered later this week).

**Analogy:** think of a video game with save points. Each time you reach a good state, you save. If you later fall into a trap, you reload the last save instead of starting over. Git "save points" are called **commits**, and you decide when to make them.

### 2. What Is Git?

**Git** is a **distributed version control system**, created in 2005 by Linus Torvalds (who also created Linux).

- **Version control system:** it tracks changes to files.
- **Distributed:** every developer's computer holds a **complete copy of the project's entire history**, not just the latest files. This means you can work offline, commit locally, and nothing is lost if one machine or server fails.
- **Free and open source.**

#### Git vs GitHub (a very common confusion)

| | Git | GitHub (and GitLab, Bitbucket) |
|---|---|---|
| What is it? | A **tool** installed on your computer | An **online service** that hosts Git repositories |
| Works offline? | Yes | No, it is a website/service |
| Purpose | Track changes and history | Share, back up, collaborate and review code |
| Analogy | A word processor with change tracking | A shared online drive for your documents |

You can use Git without GitHub. Today, we use only Git on your own computer. Tomorrow, you will connect to a remote service.

---

### 3. Installing Git

Open a terminal and check whether Git is already installed:

```bash
git --version
```

If you see something like `git version 2.45.1`, you are ready. Otherwise install it:

- **Windows:** download **Git for Windows** from https://git-scm.com/downloads and run the installer. The defaults are fine. It also includes **Git Bash**, a terminal that supports Linux-style commands.
- **macOS:** run `git --version` in Terminal; if Git is missing, macOS offers to install the developer tools. Or use Homebrew: `brew install git`.
- **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install git`

After installing, **close and reopen your terminal**, then run `git --version` again.

---

### 4. A Few Terminal Commands You Need

Git is used from the terminal, so you need a handful of basic navigation commands. These work in Git Bash, macOS Terminal and Linux (PowerShell has equivalents for most):

| Command | What it does |
|---|---|
| `pwd` | Print the folder you are currently in |
| `ls` | List files in the current folder (`dir` on Windows CMD) |
| `ls -a` | List files **including hidden ones** (names starting with `.`) |
| `cd folder_name` | Move into a folder |
| `cd ..` | Move up one folder |
| `mkdir folder_name` | Create a new folder |

---

### 5. One-Time Configuration

Every commit records **who made it**. Tell Git who you are, once per computer:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

- `git config` reads or changes Git's settings.
- `--global` means "apply to every repository on this computer for my user". (Without it, the setting applies only to the current repository.)
- Use the same email you will use for GitHub later so your commits are linked to your account.

Set the name of the default first branch to `main` (the modern standard; older Git defaulted to `master`):

```bash
git config --global init.defaultBranch main
```

Verify your settings:

```bash
git config --list
```

or check a single one:

```bash
git config user.name
```

Optionally, set VS Code as Git's editor (useful if Git ever opens an editor for you):

```bash
git config --global core.editor "code --wait"
```

---

### 6. How Git Thinks: The Three Areas

This is the most important mental model in this lesson. A file in a Git project lives in one of three places:

```
  Working Directory          Staging Area              Repository
  (your project folder)      (a "waiting room")        (the saved history)
 ┌─────────────────────┐   ┌─────────────────────┐   ┌────────────────────┐
 │ files you edit      │   │ changes you have    │   │ permanent snapshots│
 │ every day           │──▶│ chosen to include   │──▶│ called commits     │
 │                     │   │ in the next commit  │   │                    │
 └─────────────────────┘   └─────────────────────┘   └────────────────────┘
        git add ──────────────▶     git commit ───────────────▶
```

1. **Working directory:** the actual files and folders on your disk. This is where you create, edit and delete files.
2. **Staging area (also called the index):** a preparation area. You choose which changes to include in your next save point.
3. **Repository:** the permanent history, stored as a series of commits. Each commit is a **snapshot** of your project at one moment, with a message describing it.

**Analogy: taking a group photo.**
- *Working directory* is everyone milling around.
- *Staging area* is people you have called to stand in the frame.
- *Commit* is pressing the shutter, capturing the picture permanently.

Why have a staging area at all? It lets you make *focused* commits. If you've changed five files but only two belong to one logical change, you can stage and commit just those two. This keeps history clean and understandable. You'll practice staging in the next lesson.

#### The file lifecycle

Every file in your project is in one of these states:

| State | Meaning |
|---|---|
| **Untracked** | Git has never seen this file |
| **Unmodified** | Tracked, and unchanged since the last commit |
| **Modified** | Tracked, changed since the last commit, not yet staged |
| **Staged** | Marked to be included in the next commit |

Commands move files through these states: `git add` (untracked or modified to staged) and `git commit` (staged to unmodified, that is, saved).

#### Commits are snapshots

Each commit stores a snapshot of your project, along with: who made it, when, a message, and a reference to the commit before it. Because every commit points back to its parent, commits form a **chain of history**. Each commit gets a unique ID called a **hash**, a long code like `a3f9c2e1d4b5...`. You usually use just the first 7 characters.

---

### 7. Creating a Repository with `git init`

A **repository** (or **repo**) is a project folder that Git is tracking, together with the full history Git stores about it.

**Step 1: create a project folder and enter it**

```bash
mkdir qa-practice
cd qa-practice
```

**Step 2: initialize Git**

```bash
git init
```

Output:

```text
Initialized empty Git repository in /home/you/qa-practice/.git/
```

That's it. The folder is now a Git repository.

**What actually happened?** Git created a hidden folder named **`.git`** inside your project. List hidden files to see it:

```bash
ls -a
```

```text
.  ..  .git
```

The `.git` folder **is** the repository. It stores the entire history, your settings and everything Git needs. Your normal files outside it are the working directory.

> **Warning:**
> - Never edit or delete files inside `.git` manually. If you delete `.git`, you lose all history, and the folder becomes an ordinary folder again.
> - Don't run `git init` inside a folder that is already inside another repository, and avoid running it in huge folders like your home directory or Desktop. Create a dedicated project folder first.

#### Checking the state with `git status`

`git status` tells you what Git sees. It is the command you'll run most often. Try it in your empty repo:

```bash
git status
```

```text
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

Read it line by line:

- `On branch main`: you are on a branch named `main`. (Branches are covered on Wednesday; for now `main` is simply the default line of history.)
- `No commits yet`: no save points exist yet.
- `nothing to commit`: no files to track.

Now create a file. In VS Code, create `hello.py` in this folder, containing:

```python
print("Hello from my first repo")
```

Run `git status` again:

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        hello.py

nothing added to commit but untracked files present (use "git add" to track)
```

Git notices `hello.py` but says it is **untracked**; it isn't recording changes to it yet. In the next lesson you'll use `git add` and `git commit` to start tracking it.

---

### 8. Repository Setup Best Practices

1. **One repository per project.** Don't put unrelated projects in one repository.
2. **Use clear folder names** (lowercase with hyphens or underscores, no spaces).
3. **Add a `README.md`** describing what the project is and how to run it. A README is the first thing teammates (and you, later) will read. Create one right away:

   ```markdown
   # QA Practice

   Practice scripts for my Python and Git training.
   ```

4. **Do not store secrets** (passwords, API keys, tokens) in a repository. Anything committed can stay in history forever. (Tomorrow's `.gitignore` lesson shows how to keep some files out of Git.)
5. **Keep your repository outside cloud-sync folders** (like OneDrive or Dropbox) where possible; they can interfere with the `.git` folder.

A typical beginner project layout:

```text
qa-practice/
├── .git/            (created by git init; hidden)
├── README.md
├── hello.py
└── monday/
    └── test_id_formatter.py
```

---

### 9. Getting Help

Git has built-in documentation:

```bash
git help init        # opens the manual page for 'init'
git init -h          # prints a short summary in the terminal
git help -a          # lists available commands
```

Documentation is a skill: professionals look commands up all the time.

---

### 10. Common Problems

| Problem | Likely cause | Fix |
|---|---|---|
| `git: command not found` | Git is not installed or the terminal wasn't restarted | Install Git; reopen the terminal |
| `fatal: not a git repository` | You are not inside a repo folder | `cd` into the project folder, or run `git init` |
| Commit fails with "Please tell me who you are" | `user.name`/`user.email` not set | Run the `git config --global` commands |
| `ls -a` doesn't show `.git` | Wrong folder, or `git init` not run | Check with `pwd`; run `git init` |
| Created a repo inside another repo by mistake | `git init` run in a sub-folder of a repo | Delete the inner `.git` folder (only if it's brand new and empty) |

---

### 11. Practice Activities

1. **Install check.** Run `git --version` and record the version.
2. **Identity.** Configure your name, email and default branch, then run `git config --list` and find your three settings in the output.
3. **Create a repository.** Make a folder `git-practice`, enter it and run `git init`. Use `ls -a` to find `.git`.
4. **Observe.** Run `git status` in the empty repo. Add a file `notes.txt` with one line of text and run `git status` again. Describe, in your own words, what changed in the output.
5. **Mental model.** Draw the three areas (working directory, staging area, repository) on paper and write which command moves a file between them.
6. **Explain it.** In two sentences, explain the difference between Git and GitHub as you would to a friend.
7. **Help.** Run `git help status` (or `git status -h`) and find one option you hadn't seen before.

---

## Summary

- **Version control** records the history of changes so you can review, restore and collaborate.
- **Git** is a free, distributed version control tool on your computer; **GitHub** is an online service for hosting Git repositories.
- Configure your identity once with `git config --global user.name` and `user.email`; set `init.defaultBranch main`.
- Git has three areas: the **working directory** (your files), the **staging area** (changes selected for the next commit) and the **repository** (permanent history of commits).
- A **commit** is a snapshot with a message, author and unique hash.
- `git init` turns a folder into a repository by creating a hidden `.git` folder, which holds all history; never delete or edit it by hand.
- `git status` shows the current state: untracked, modified and staged files.
- Next lesson: you will record your first commits using `git add`, `git commit`, `git status` and `git log`.

---

## Additional Resources

- Pro Git book: What is Git?: https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F
- Pro Git book: Getting a Git Repository: https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository
- Pro Git book: First-Time Git Setup: https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup
