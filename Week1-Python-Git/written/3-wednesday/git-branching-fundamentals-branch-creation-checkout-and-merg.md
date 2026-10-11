# Git Branching Fundamentals: Branch Creation, Checkout and Merge; Working With Remote Repositories

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a branch is and why teams use branches.
- Describe how Git implements branches (commits and pointers) and what `HEAD` is.
- Create, list, rename and delete branches with `git branch` and `git switch -c`.
- Move between branches with `git switch` and `git checkout`.
- Merge a branch into another and tell a **fast-forward** merge from a **three-way** merge.
- Recognise, understand and resolve a **merge conflict**.
- Visualise history with `git log --graph --oneline --all`.
- Work with branches on a remote: push, track, fetch, prune and delete remote branches.
- Follow a safe feature-branch workflow for the test-data manager exercise.

---

## Why This Matters

Imagine you are halfway through adding a feature to your test framework: the code is broken for the next hour. Meanwhile, a teammate needs a working version of the project to run tests. Or you want to try a risky idea and be able to throw it away safely.

**Branches** solve this. A branch is an independent line of development: you can experiment, commit and break things on your branch while `main` stays stable. When your work is ready, you **merge** it back.

On Tuesday you used `git switch -c` and a pull request without a full explanation. Today you learn what was really happening, and you learn to merge locally and resolve conflicts, which is a skill every team member needs. Today's exercise has you build the test-data manager **on a feature branch and merge** it, so these are the exact skills you'll practise.

---

## The Concept

### 1. What Is a Branch?

A **branch** is a movable **label that points at a commit**. That's it. Creating a branch doesn't copy your files; it just creates a new, lightweight pointer. This is why Git branches are cheap and fast, and why professionals create them constantly.

Recall that commits form a chain, each pointing to its parent:

```
 A ◀── B ◀── C
              ▲
            main
```

`main` is a pointer to commit `C`. Now create a branch called `feature` at the same commit:

```
 A ◀── B ◀── C
              ▲
         main, feature
```

Both labels point to `C`. Which one are you "on"? Git keeps a special pointer called **`HEAD`** that says "where you are right now": it points at the *current branch*.

```
 A ◀── B ◀── C
              ▲
         main, feature
                ▲
              HEAD   (→ feature, if you are on it)
```

When you commit while on `feature`, the new commit is added and only the **current branch's pointer moves**:

```
 A ◀── B ◀── C ◀── D
              ▲     ▲
            main  feature  ← HEAD
```

Now `feature` has a commit `D` that `main` doesn't. The two lines of work have **diverged**, and `main` is untouched.

**Analogy:** think of writing a document. `main` is the published version. A branch is a private draft copy where you can write freely. When the draft is good, you merge it into the published version.

#### Why branch?

- **Isolation:** unfinished work doesn't affect the stable branch.
- **Parallel work:** several people (or you, on several tasks) work at once.
- **Safety:** an experiment that fails can simply be deleted.
- **Review:** changes arrive on `main` through pull requests (Tuesday), not directly.

---

### 2. Seeing and Creating Branches

#### 2.1 List branches

```bash
git branch
```

```text
* main
```

The `*` marks the current branch. Useful variants:

| Command | Shows |
|---|---|
| `git branch` | Local branches |
| `git branch -v` | Local branches with the last commit on each |
| `git branch -r` | Remote-tracking branches (such as `origin/main`) |
| `git branch -a` | Both local and remote |

Your current branch also appears in `git status` ("On branch main").

#### 2.2 Create a branch

```bash
git branch feature/data-manager
```

This creates the branch but you **stay on your current branch**. List again:

```text
  feature/data-manager
* main
```

#### 2.3 Create and switch in one step

Most of the time you want to create a branch and start working on it immediately:

```bash
git switch -c feature/data-manager
```

or the older form that does the same:

```bash
git checkout -b feature/data-manager
```

You can also create a branch from a specific starting point:

```bash
git switch -c fix/typo main          # start from main, whatever you are on now
```

**Naming:** lowercase, hyphens, optional prefix like `feature/`, `fix/`, `docs/`. Branch names can't contain spaces.

---

### 3. Switching Branches (Checkout)

```bash
git switch main
git switch feature/data-manager
```

`git switch` changes `HEAD` to the other branch **and updates your files** to match that branch's latest commit. This is genuinely visible: if `feature` has a file `manager.py` that `main` lacks, the file **disappears** from your folder when you switch to `main` and reappears when you switch back. Nothing is lost; Git is just showing you a different snapshot.

`git checkout <branch>` is the older command. It does the same job but also does other things (such as restoring files), which confused many people. That's why `switch` (for branches) and `restore` (for files) were introduced. You'll see `checkout` in many tutorials, and both are valid.

Go back to the previous branch quickly:

```bash
git switch -
```

#### Switching with uncommitted changes

If you have **uncommitted changes**:

- If they don't conflict with the other branch's files, Git carries them along.
- If they would be overwritten, Git refuses and warns you:

```text
error: Your local changes to the following files would be overwritten by checkout:
        manager.py
Please commit your changes or stash them before you switch branches.
```

The easiest fix for a beginner: **commit** your work (even as a small work-in-progress commit) before switching. (There's also `git stash`, a temporary shelf for changes, which you'll meet later.)

> **Golden habit:** run `git status` before switching or merging. Know which branch you're on.

---

### 4. Working on a Branch

```bash
git switch -c feature/data-manager

# create manager.py and edit it
git add manager.py
git commit -m "Add test data list and print function"

# edit again
git add manager.py
git commit -m "Add duplicate removal"
```

Meanwhile `main` hasn't changed. Confirm with:

```bash
git log --oneline --graph --all
```

```text
* 5c6d7e8 (HEAD -> feature/data-manager) Add duplicate removal
* 3b4c5d6 Add test data list and print function
* 1a2b3c4 (main) Add README
```

#### The most useful history view

```bash
git log --oneline --graph --all
```

- `--oneline`: one compact line per commit.
- `--graph`: draws the branch structure with ASCII lines.
- `--all`: includes all branches, not just the current one.

Many people create an alias: `git config --global alias.lg "log --oneline --graph --all"`, and then type `git lg`.

---

### 5. Merging

**Merging** brings the commits of one branch into another. You always run the command **while on the branch that should receive the changes** (the *target*).

```bash
git switch main               # go to the branch that will receive the work
git merge feature/data-manager
```

Git picks one of two strategies depending on the shape of the history.

#### 5.1 Fast-forward merge

If `main` has **not moved** since you branched off, Git just slides the `main` pointer forward along the straight line of commits:

```
 Before:                                After:
 A ◀── B ◀── C ◀── D ◀── E              A ◀── B ◀── C ◀── D ◀── E
        ▲           ▲                                          ▲
      main     feature                                 main, feature
```

```text
Updating 1a2b3c4..5c6d7e8
Fast-forward
 manager.py | 25 +++++++++++++++++++++++++
 1 file changed, 25 insertions(+)
```

No new commit is created; history stays perfectly linear.

#### 5.2 Three-way merge (merge commit)

If **both** branches have new commits (they have *diverged*), Git can't just move a pointer. It combines the two lines of work and records the result in a new **merge commit** with two parents:

```
 Before:                              After:
        D ◀── E   feature                    D ◀── E
       /                                    /        \
 A ◀── B ◀── C   main                 A ◀── B ◀── C ◀── M   main
                                                              (M = merge commit)
```

Git uses three snapshots to decide the result: the two branch tips and their **common ancestor** (`B`), hence the name "three-way merge". Changes made in only one branch are applied automatically; changes to different parts of the same file are combined.

```text
Merge made by the 'ort' strategy.
 manager.py | 25 +++++++++++++++++++++++++
 1 file changed, 25 insertions(+)
```

Git opens an editor for the merge commit message, offering a default such as `Merge branch 'feature/data-manager'`. Save and close it. (Or use `git merge --no-edit` to accept the default.)

#### 5.3 Forcing a merge commit

To always record a merge commit, even when a fast-forward is possible (which keeps a visible record that a branch existed):

```bash
git merge --no-ff feature/data-manager
```

Many teams use this (or squash merges on GitHub). Use whichever your team prefers.

#### 5.4 After merging: clean up

```bash
git branch -d feature/data-manager
```

`-d` deletes a branch only if it has been merged (safe). `-D` forces deletion even if unmerged: **only use it when you are certain you want to throw the work away**. Deleting a branch doesn't delete the commits that were merged: they are now part of `main`.

---

### 6. Merge Conflicts

Sometimes Git can't combine changes automatically: the **same lines** were changed differently on both branches, or one branch changed a file that the other deleted. Git stops and asks **you** to decide. This is a **merge conflict**. It is not an error and nothing is broken. It's Git asking for a human decision.

#### 6.1 Creating a conflict (a practice recipe)

Start with a file `config.py` on `main`:

```python
browser = "chrome"
timeout = 30
```

Commit it. Then:

```bash
git switch -c feature/firefox
# change line 1 to: browser = "firefox"
git commit -am "Use Firefox"

git switch main
# change line 1 to: browser = "edge"
git commit -am "Use Edge"

git merge feature/firefox
```

(`-a` stages all modified *tracked* files; combined with `-m` it's a shortcut for `add` + `commit`, only for files Git already tracks.)

Output:

```text
Auto-merging config.py
CONFLICT (content): Merge conflict in config.py
Automatic merge failed; fix conflicts and then commit the result.
```

#### 6.2 Reading the conflict

`git status` says:

```text
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   config.py
```

Open `config.py`. Git has inserted **conflict markers**:

```text
<<<<<<< HEAD
browser = "edge"
=======
browser = "firefox"
>>>>>>> feature/firefox
timeout = 30
```

| Marker | Meaning |
|---|---|
| `<<<<<<< HEAD` | Start of **your current branch's** version (here `main`) |
| `=======` | Divider between the two versions |
| `>>>>>>> feature/firefox` | End of the **incoming** branch's version |

Everything outside the markers (`timeout = 30`) merged cleanly.

#### 6.3 Resolving it

1. **Decide** what the final code should be: keep one version, keep the other, or combine them. Talk to the teammate if you aren't sure.
2. **Edit the file**: remove all three marker lines and leave only the final code:

   ```python
   browser = "firefox"
   timeout = 30
   ```

3. **Stage** the resolved file:

   ```bash
   git add config.py
   ```

4. **Complete the merge** with a commit:

   ```bash
   git commit
   ```

   (Git pre-fills a message like "Merge branch 'feature/firefox'".) Save and close.

5. Run your code or tests to make sure the combined result actually works.

VS Code helps: it highlights conflicts and offers clickable options such as **Accept Current Change**, **Accept Incoming Change**, **Accept Both Changes** above each conflict. Always review the final result: "Accept Both" can produce invalid code.

#### 6.4 Aborting a merge

If you're unsure or things look wrong, you can back out and return to the state before the merge:

```bash
git merge --abort
```

#### 6.5 Avoiding conflicts

- Keep branches **short-lived** and **small**.
- **Pull `main` often** and merge it into your branch regularly (`git switch feature; git merge main`) so you resolve small differences early.
- Communicate: tell teammates which files you are changing.
- Avoid reformatting entire files, which touches every line.

#### 6.6 Final checks and mistakes to avoid

- **Never leave conflict markers in the file.** A stray `<<<<<<<` will break your Python code (`SyntaxError`).
- Don't resolve conflicts by blindly choosing "mine": you may erase a teammate's work.

---

### 7. Working With Remote Repositories and Branches

Tuesday's lesson introduced remotes (`origin`), `push`, `pull` and `fetch`. Now we combine them with branches.

#### 7.1 Local vs remote-tracking branches

| Kind | Example | What it is |
|---|---|---|
| **Local branch** | `main`, `feature/data-manager` | Your own branches that you commit to |
| **Remote-tracking branch** | `origin/main`, `origin/feature/data-manager` | Read-only bookmarks showing where the remote's branches were at your last fetch |
| **Remote branch** | `main` on GitHub | The real branch on the server |

```bash
git branch -a
```

```text
* feature/data-manager
  main
  remotes/origin/main
  remotes/origin/feature/data-manager
```

#### 7.2 Pushing a new branch

```bash
git push -u origin feature/data-manager
```

`-u` sets the **upstream**: it links your local branch to `origin/feature/data-manager`, so later `git push` and `git pull` need no arguments. You'll see `git status` messages like "Your branch is ahead of 'origin/feature/data-manager' by 1 commit".

#### 7.3 Getting a teammate's branch

A colleague pushed `feature/api-tests`. To see it:

```bash
git fetch
git branch -r                          # now lists origin/feature/api-tests
git switch feature/api-tests           # creates a local branch tracking origin's
```

(`git switch <name>` automatically creates a local tracking branch if exactly one remote has a branch with that name.)

#### 7.4 Keeping your branch up to date with `main`

While you work on a feature, `main` may receive other people's changes. Bring them into your branch:

```bash
git switch main
git pull                               # update local main
git switch feature/data-manager
git merge main                         # bring main's new commits into your branch
```

or in fewer steps:

```bash
git fetch
git merge origin/main                  # while on your feature branch
```

Resolve any conflicts on **your feature branch**, where it is safe, rather than on `main`.

(There is another way to integrate changes called **rebase**, which rewrites history to make it linear. It's powerful but easy to misuse, so we'll leave it for later in the program. For now, merge.)

#### 7.5 Merging locally vs via pull request

There are two ways to finish a feature:

| Way | Steps | When |
|---|---|---|
| **Merge locally** | `git switch main`, `git merge feature`, `git push` | Solo projects, practice and learning (today's exercise) |
| **Pull request** | Push the branch, open and review a PR, merge on GitHub (Tuesday) | Team projects; this is the professional default |

Either way, the result in `main` is the same kind of merge. If `main` is **protected** on GitHub, pushing directly is refused, which forces the PR route.

After a PR is merged on GitHub, update your local repo:

```bash
git switch main
git pull
git branch -d feature/data-manager
```

#### 7.6 Deleting and tidying remote branches

```bash
git push origin --delete feature/data-manager     # delete the branch on the remote
git fetch --prune                                 # remove stale remote-tracking references locally
```

If a teammate deleted a remote branch, your `origin/...` bookmark remains until you prune. `git fetch --prune` (or `git remote prune origin`) tidies them. You can make this automatic: `git config --global fetch.prune true`.

#### 7.7 Renaming a branch

```bash
git branch -m old-name new-name        # rename a local branch
git branch -m new-name                 # rename the current branch
```

If it was already pushed, you'd also need to push the new name and delete the old one on the remote.

---

### 8. Complete Workflow for the Exercise

You will build the test-data manager on a feature branch and merge it:

```bash
# 1. Start fresh
git switch main
git pull

# 2. Create the feature branch
git switch -c feature/test-data-manager

# 3. Build in small, committed steps
git add manager.py
git commit -m "Add test case data and display"
git add manager.py
git commit -m "Add duplicate removal with a set"
git add manager.py
git commit -m "Add grouping by module with defaultdict"
git add manager.py
git commit -m "Add lookup by test ID"

# 4. Share the branch (backup, review)
git push -u origin feature/test-data-manager

# 5. Merge into main (locally, as practice)
git switch main
git merge feature/test-data-manager
git push

# 6. Clean up
git branch -d feature/test-data-manager
git push origin --delete feature/test-data-manager

# 7. Review the history
git log --oneline --graph --all
```

---

### 9. Command Cheat Sheet

| Task | Command |
|---|---|
| List local branches | `git branch` |
| List all branches | `git branch -a` |
| Create a branch | `git branch name` |
| Create and switch | `git switch -c name` |
| Switch | `git switch name` |
| Merge `name` into current branch | `git merge name` |
| Abort a merge | `git merge --abort` |
| Delete a merged branch | `git branch -d name` |
| Force-delete a branch | `git branch -D name` |
| Visual history | `git log --oneline --graph --all` |
| Push a new branch | `git push -u origin name` |
| Delete a remote branch | `git push origin --delete name` |
| Fetch and prune | `git fetch --prune` |
| Rename current branch | `git branch -m new-name` |

---

### 10. Common Problems

| Problem | Cause | Fix |
|---|---|---|
| Committed on `main` by accident | Forgot to switch or create a branch | Ask for help before trying to undo; undoing commits is covered later |
| "Your local changes would be overwritten" when switching | Uncommitted edits conflict | Commit them first, then switch |
| My file disappeared! | You switched to a branch that lacks it | Switch back; the file is safe in the other branch |
| `CONFLICT (content)` during merge | Same lines changed in both branches | Edit, `git add`, `git commit`; or `git merge --abort` |
| Conflict markers left in code | Forgot to clean the file | Search for `<<<<<<<` and remove markers |
| `error: The branch is not fully merged` | `-d` refuses to delete unmerged work | Merge it first, or use `-D` only if you really want to discard it |
| Merged the wrong way round | Ran `git merge` on the wrong branch | Check `git status` before merging; `merge` always brings others *into the current* branch |
| `fatal: A branch named ... already exists` | Name in use | Choose a different name or switch to it |
| Remote branch still listed after deletion | Stale remote-tracking ref | `git fetch --prune` |
| Push rejected after merging | Remote has new commits | `git pull`, then push |

---

### 11. Practice Activities

Work in a practice repository with at least one commit on `main`.

1. **Branch tour.** Run `git branch`, create `feature/one` with `git branch`, then `git switch` to it and confirm in `git status`.
2. **The disappearing file.** On `feature/one`, create and commit `one.txt`. Switch to `main` and run `ls`. Switch back. Explain what you saw.
3. **Fast-forward.** Merge `feature/one` into `main`. Check the output for "Fast-forward" and look at `git log --oneline --graph --all`.
4. **Three-way merge.** Create `feature/two` and commit a new file `two.txt`. Then switch to `main` and commit a different new file `main.txt`. Merge `feature/two` into `main`. Look at the graph and find the merge commit.
5. **Create and resolve a conflict.** Follow the recipe in section 6.1. Resolve it, commit, and confirm the markers are gone.
6. **Abort.** Create another conflict and use `git merge --abort`. Check `git status`.
7. **Clean up.** Delete merged branches with `-d`. Try `-d` on an unmerged branch and read the message.
8. **Remote branches.** Push a branch with `-u`, find it on GitHub, delete it on the remote, then run `git fetch --prune` and `git branch -a`.
9. **Pair activity.** With a partner, both edit the same line of the same file on different branches, push both, and have one person merge and resolve the conflict.
10. **Explain.** In your own words: What is a branch? What is `HEAD`? Why is a fast-forward merge different from a three-way merge? What does a conflict marker mean?

---

## Summary

- A **branch** is a lightweight, movable pointer to a commit; **`HEAD`** says which branch you are on. Branches let you work in isolation while `main` stays stable.
- Create with `git switch -c name` (or `git branch name`); list with `git branch` (`-a` for remote ones); switch with `git switch name` (older: `git checkout name`). Commit or stash changes before switching.
- **Merge** while on the *receiving* branch: `git merge feature`. A **fast-forward** just moves the pointer; a **three-way merge** creates a merge commit; `--no-ff` forces a merge commit.
- A **merge conflict** happens when both branches changed the same lines. Open the file, resolve the `<<<<<<<` / `=======` / `>>>>>>>` section, remove the markers, `git add`, `git commit`. `git merge --abort` cancels.
- View structure with `git log --oneline --graph --all`.
- **Remote branches:** `git push -u origin name` publishes a branch; `git fetch` reveals teammates' branches; `origin/name` is a read-only bookmark; delete remote branches with `git push origin --delete name` and tidy with `git fetch --prune`.
- Keep branches **short and small**, merge `main` into them regularly, and pull before you push.
- Locally merged or via **pull request**, the professional default is the PR you learned on Tuesday.
- Tomorrow: Python **functions**, the tools that make code reusable, with Git as your safety net.

---

## Additional Resources

- Pro Git book: Branches in a Nutshell: https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell
- Pro Git book: Basic Branching and Merging: https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
- Pro Git book: Remote Branches: https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches
