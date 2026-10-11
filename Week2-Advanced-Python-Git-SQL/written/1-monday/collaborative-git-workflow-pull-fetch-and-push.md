# Collaborative Git Workflow: Pull, Fetch and Push

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the difference between a **local** repository and a **remote** repository, and what `origin` means.
- Clone a repository and inspect its remotes with `git remote -v`.
- Explain **remote-tracking branches** (such as `origin/main`) and why they are not the same as your local branches.
- Use `git fetch` to download others' work *without* changing your files, and inspect what arrived.
- Use `git pull` (fetch plus integrate) and explain the difference between pulling with **merge** and pulling with **rebase**.
- Use `git push` to publish commits, set an upstream branch with `-u`, and understand why a push can be **rejected**.
- Follow a safe daily collaboration routine for a shared repository, including feature branches.
- Understand authentication options (HTTPS tokens, SSH keys) at a practical level, and when force-pushing is dangerous.

> **Scope note.** This lesson assumes you already know the basic local Git commands (`git init`, `git status`, `git add`, `git commit`, `git log`, and the idea of a branch). If you need a refresher, practise those commands in a throw-away folder first. When a pull or merge produces a **conflict**, we will say so and stop; resolving conflicts is the focus of its own lesson on Wednesday.

---

## Why This Matters

Test automation is a **team sport**. In a real QE team, five people may add tests, fix helper functions and update test data in the same repository every day. Git is how those contributions combine without anyone overwriting anyone else's work, and the **remote** repository (on GitHub, GitLab, Bitbucket or Azure DevOps) is the shared meeting point.

This week's epic ends with a QE Foundations capstone (Project 1) that you start today by creating a repository and structuring it. The Python modules, packages and `requirements.txt` you have just learned about are only useful to a team if they are shared: committed, pushed and pulled correctly. A teammate (or the CI server) clones your repository, creates a virtual environment, runs `pip install -r requirements.txt` and expects everything to work.

If you do not understand `fetch`, `pull` and `push`, you will hit confusing messages such as:

```
! [rejected]        main -> main (fetch first)
error: failed to push some refs to ...
```

and you may be tempted to "fix" them with dangerous commands. After this lesson, those messages will be ordinary and you will know exactly what to do.

An analogy: think of a **shared document in a team folder**. Your *local repository* is a copy on your own laptop that you edit freely. The *remote* is the master copy in the shared folder. **Fetch** is "check what changed in the shared folder and bring me copies of the new versions to look at, without touching my own working document". **Pull** is "bring in the changes and merge them into my document now". **Push** is "publish my changes to the shared folder", which is allowed only if I have seen everything others have already published.

---

## The Concept

### 1. Local vs Remote Repositories

Git is a **distributed** version control system: every clone contains the **full history** of the project. There is no central "live" connection; each person works offline against their own full copy, and you explicitly synchronise with others.

| Term | Meaning |
|------|---------|
| **Local repository** | The `.git` folder and working files on your computer |
| **Remote repository** | Another copy of the repository, usually on a hosting service (GitHub, GitLab...), used to share work |
| **Remote (name)** | A short nickname Git stores for a remote's URL. The default name is **`origin`** |
| **Clone** | Make a local copy of a remote repository (and set up `origin` automatically) |
| **Upstream branch** | The remote branch your local branch is linked to, so Git knows where to push/pull by default |

The synchronisation commands are:

| Command | Direction | Changes your files? |
|---------|-----------|--------------------|
| `git fetch` | remote -> your repository (history only) | No |
| `git pull` | remote -> your repository **and** into your current branch | Yes |
| `git push` | your repository -> remote | No (changes the remote) |

### 2. Remotes and `origin`

#### Cloning

```bash
git clone https://github.com/your-team/qe-foundations.git
cd qe-foundations
```

`git clone <url>` does several things in one step:

1. Creates a folder named after the repository.
2. Downloads **all** the history and branches.
3. Adds a remote called `origin` that points to the URL you cloned from.
4. Checks out the default branch (usually `main`) and sets it to track `origin/main`.

You can choose a different folder name: `git clone <url> my-folder`.

#### Listing remotes

```bash
git remote -v
```

Output (example):

```
origin  https://github.com/your-team/qe-foundations.git (fetch)
origin  https://github.com/your-team/qe-foundations.git (push)
```

`-v` means *verbose*: show the URLs. There are two lines because Git can use different URLs for downloading (fetch) and uploading (push), though they are normally identical.

#### Adding a remote to a repository you created locally

Suppose you started a project with `git init` (as you will in today's exercise) and then created an empty repository on GitHub. Connect them:

```bash
git remote add origin https://github.com/your-name/qe-foundations.git
git remote -v
git push -u origin main
```

- `git remote add <name> <url>` registers a nickname for a URL. Nothing is transferred yet.
- `origin` is only a convention; you could call it anything, and a repository can have several remotes (for example `origin` for your fork and `upstream` for the original project).
- You can change a URL with `git remote set-url origin <new-url>`, and remove a remote with `git remote remove <name>`.

> **Branch name check:** Many repositories use `main` as the default branch; older ones use `master`. You can see yours with `git branch`. When you create a new repository you can start with the right name using `git init -b main`, or rename with `git branch -M main`.

### 3. Remote-Tracking Branches: `origin/main`

This idea is the key to understanding everything else, so read it slowly.

When you clone, you do not just get a local branch `main`. Git also keeps a **read-only bookmark** called `origin/main` which records **where the remote's `main` branch was the last time you talked to the remote**. These bookmarks are called **remote-tracking branches**.

So in your local repository there are two different things:

- `main`: your own local branch. You move it by committing.
- `origin/main`: Git's *memory* of the remote `main`. You cannot commit onto it directly; it only moves when you `fetch`, `pull` or `push`.

See both:

```bash
git branch -a      # all branches: local and remote-tracking
git branch -vv     # local branches with their upstream and ahead/behind counts
```

Example of `git branch -vv`:

```
* main bdb4169 [origin/main] Initial commit
```

The text `[origin/main]` says that your `main` is tracking `origin/main`. When you are out of sync, Git adds `ahead` and/or `behind` counts, such as `[origin/main: ahead 1, behind 2]`:

- **ahead 1:** you have 1 commit the remote does not have (you need to **push**).
- **behind 2:** the remote has 2 commits you do not have (you need to **fetch/pull**).
- **both (diverged):** you must combine the work before you can push.

`git status` shows the same information in friendlier words, and `git status -sb` shows a short form: `## main...origin/main [ahead 1, behind 1]`.

**Important consequence:** `origin/main` is only as fresh as your last contact. It does *not* update automatically in the background. To learn what teammates have done, you must `fetch`.

### 4. `git fetch`: Download Without Changing Your Work

```bash
git fetch
```

(`git fetch origin` is the explicit form; with one remote they are equivalent.)

What it does:

1. Contacts the remote and finds commits you do not have.
2. Downloads them into your repository.
3. Moves the **remote-tracking branches** (`origin/main`, ...) to match the remote.
4. Does **nothing** to your local branches or your working files.

That last point makes `fetch` completely **safe**. You can run it any time without risk of breaking or conflicting with your work in progress. Typical output:

```
From https://github.com/your-team/qe-foundations
   bdb4169..8116ac8  main       -> origin/main
```

This reads "on the remote, `main` moved from commit `bdb4169` to `8116ac8`, and I updated my `origin/main` bookmark accordingly".

#### Inspecting what arrived

After fetching, look before you integrate:

```bash
git status -sb                      # ahead/behind summary
git log --oneline HEAD..origin/main # commits on the remote that I don't have
git log --oneline origin/main..HEAD # commits I have that the remote doesn't
git diff --stat HEAD...origin/main  # which files changed on the remote side (summary)
git diff HEAD...origin/main         # the actual changes made on the remote side
git log --oneline --graph --all     # a picture of how the branches relate
```

How to read `A..B`: "commits reachable from B but not from A". So `HEAD..origin/main` means "what's on the remote that I lack". The three-dot form `HEAD...origin/main` in `git diff` compares the remote's latest commit to the *common ancestor*, showing what the other side changed since you diverged, which is usually what you want to review.

Example output of the graph command after both you and a teammate have committed:

```
* 88914b4 Bob adds file          <- my local commit
| * 8116ac8 Alice adds file      <- teammate's commit, now visible as origin/main
|/
* bdb4169 Initial commit
```

The lines splitting apart show that history has **diverged**.

#### When to use `fetch`

- To see what teammates have done before deciding how to integrate it.
- Before starting new work or before a push, to check whether you are behind.
- In scripts and automation, since it is safe and read-only for your files.

#### Handy variants

```bash
git fetch --all      # fetch from every configured remote
git fetch --prune    # also remove remote-tracking branches that were deleted on the remote
```

Teams often delete a branch on the remote after merging a pull request; `--prune` tidies the stale `origin/feature-x` bookmark from your list. (You can make it automatic with `git config fetch.prune true`.)

### 5. `git pull`: Fetch Plus Integrate

```bash
git pull
```

`git pull` is a shortcut for **two** steps:

```
git pull  =  git fetch   (download and update origin/<branch>)
          +  integrate   (merge or rebase origin/<branch> into your current branch)
```

Because it changes your current branch and working files, it can fail or create conflicts if you have uncommitted changes in the same files or if the remote's changes overlap with yours.

#### Cases

**Case 1: you are behind and have no local commits: a fast-forward.**
Your branch is simply "older" than the remote's. Git moves your branch pointer forward to match. No new commit is created.

```
Before:   A---B            (main, origin/main was B; remote now has C, D)
                \
Remote:           C---D

After pull:  A---B---C---D   (main fast-forwarded)
```

Output includes `Fast-forward` and a list of changed files.

**Case 2: you have local commits and the remote has new commits: diverged.**
Git must combine the two lines of work. It can do so in two ways: **merge** or **rebase**.

```
Local:      A---B---X          (your commit X)
                 \
Remote:           C---D        (teammates' commits)
```

##### Pull with merge (`git pull --no-rebase`)

Git creates a **merge commit** that has two parents, tying the histories together:

```
A---B---X-------M
     \         /
      C-------D
```

History keeps the true shape (parallel work), at the cost of extra merge commits in the log.

##### Pull with rebase (`git pull --rebase`)

Git temporarily sets aside your commits, fast-forwards to the remote's latest, then **replays** your commits on top:

```
A---B---C---D---X'
```

`X'` is a *new* commit with the same changes as `X` but a different parent (and therefore a different commit ID). The history is a straight line, which many teams find easier to read. The rule of thumb: **only rebase commits that you have not yet shared.** Rebasing commits that others already have forces them into messy repair work. Pull-with-rebase rewrites only *your own unpublished* commits, so it is safe in this specific use.

##### Which should you use?

Both are valid, and **teams choose a convention**. Know what your team's is. For this course, treat either as acceptable, but be consistent.

| | Merge | Rebase |
|---|-------|--------|
| History | Preserves the branching shape; adds merge commits | Linear and tidy |
| Safety | Never rewrites existing commits | Rewrites your local, unpublished commits |
| Conflict handling | Resolve once, in the merge commit | May need to resolve at each replayed commit |

**Git requires you to choose** when histories have diverged. Since Git 2.27 you will see a message like this if you have not configured a default:

```
hint: You have divergent branches and need to specify how to reconcile them.
fatal: Need to specify how to reconcile divergent branches.
```

This is not an error in your repository; Git is asking which strategy you want. Options:

```bash
git pull --rebase          # this time, rebase
git pull --no-rebase       # this time, merge
git pull --ff-only         # only if a fast-forward is possible; otherwise stop (the safest)

# set a default so you are not asked again (for this repository):
git config pull.rebase false     # merge
git config pull.rebase true      # rebase
git config pull.ff only          # fast-forward only
# add --global to apply it to all your repositories
```

**`git pull --ff-only` is a good beginner habit**: if it can fast-forward, it does; if histories diverged, it stops and says "Not possible to fast-forward, aborting.", leaving everything untouched. Then you can decide consciously between merge and rebase.

#### What if there are conflicts?

If you and a teammate changed the *same lines* of the same file, Git cannot decide whose version wins. The pull stops in the middle and marks the problem files; Git prints something like `CONFLICT (content): Merge conflict in <file>`. **Do not panic and do not delete anything.** Resolving conflicts is a skill we teach in depth on **Wednesday** (merge conflicts and resolution). Until then, the safe way out of a pull gone wrong is `git merge --abort` (if you were merging) or `git rebase --abort` (if you were rebasing), which returns you to the state before the pull. And the best way to *avoid* conflicts for now is to pull often and keep commits small.

#### Fetch then merge, the explicit way

`git pull` is convenient but does two things at once. Many experienced developers prefer the explicit form, which lets them inspect between the steps:

```bash
git fetch
git log --oneline HEAD..origin/main     # what's new?
git merge origin/main                    # or: git rebase origin/main
```

You can think of `git pull` as `git fetch` followed by `git merge origin/<current-branch>` (or `git rebase ...` when configured for rebase).

#### Uncommitted changes and pull

If you have uncommitted edits in files that the pull would change, Git refuses (`error: Your local changes to the following files would be overwritten by merge`). Options: commit your work first (best), or temporarily set it aside with `git stash`, then `git pull`, then `git stash pop`. (Stash is a handy command to know; use it for short-lived parking of work.)

### 6. `git push`: Publish Your Commits

```bash
git push
```

Push uploads your local commits to the remote branch and moves the remote branch (and your `origin/main` bookmark) forward. Syntax: `git push <remote> <branch>`, for example `git push origin main`.

#### The very first push of a branch: `-u`

A brand-new local branch has no upstream. The first time you push it:

```bash
git push -u origin feature/login-tests
```

`-u` is short for `--set-upstream`. It does two things: pushes the branch, and records that your local `feature/login-tests` tracks `origin/feature/login-tests`. After that, plain `git push` and `git pull` on that branch know where to go. If you forget `-u`, Git reminds you with a message containing `git push --set-upstream origin <branch>`.

#### Why a push can be rejected

Git only allows a push that results in a **fast-forward** of the remote branch: the remote's latest commit must already be part of your history. If a teammate has pushed since you last synced, your history lacks their commit, so the push would erase it from the remote branch. Git protects them by refusing:

```
To https://github.com/your-team/qe-foundations.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/your-team/qe-foundations.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
```

Read it as a helpful instruction rather than a failure. The standard resolution:

```bash
git pull --rebase     # (or git pull, per your team's convention) to bring in their commits
# resolve conflicts if any (Wednesday's topic), run your tests
git push              # now it is a fast-forward and succeeds
```

Sometimes you will see `(non-fast-forward)` in place of `(fetch first)`: the same idea, for the case where you already fetched but have not integrated.

#### Force pushing: a dangerous tool

`git push --force` overwrites the remote branch with your version, **deleting teammates' commits from it** if you have not integrated them. Rules for now:

1. Never force-push to a shared branch (`main`, `develop`, a colleague's branch).
2. It is occasionally legitimate on your *own* feature branch, after you rebased commits that only you have pushed. In that case prefer **`git push --force-with-lease`**, which refuses to overwrite if the remote contains commits you have not seen.
3. If a push is rejected, the answer is nearly always "pull first", not "force".

#### What `push` does not do

- It pushes **commits**, not uncommitted files. If you forgot to `git add`/`git commit`, nothing new will be uploaded ("Everything up-to-date").
- It pushes only the branch you name (or the current branch's upstream), not every branch. `git push --all` exists but is rarely needed.
- It does not push **tags** by default: use `git push origin v1.0`, or `git push --tags`.

#### Deleting a remote branch

```bash
git push origin --delete feature/login-tests
```

Usually done after a branch has been merged. Teammates then clean up their stale bookmark using `git fetch --prune`.

### 7. A Safe Daily Collaboration Routine

Here is a habit-forming routine for working in a shared repository:

```bash
# 1. START OF DAY / before new work: get up to date
git switch main
git pull --ff-only              # update my local main (stops if something unusual happened)

# 2. Make a branch for your task
git switch -c feature/add-email-validator

# 3. Work in small steps; commit often with clear messages
git add src/qa_toolkit/validators.py
git commit -m "Add is_valid_email validator"

# 4. Before publishing: see what changed upstream
git fetch
git status -sb                  # ahead/behind?
git pull --rebase origin main   # (or merge) bring main's latest into my branch

# 5. Run the tests / check the code still works

# 6. Publish
git push -u origin feature/add-email-validator

# 7. Open a pull request (merge request) on the hosting service for review
```

(`git switch` and `git switch -c` are the modern equivalents of `git checkout <branch>` and `git checkout -b <branch>`; both styles work.)

**Why branches?** Pushing every change straight to `main` means a half-finished change can break everyone. A short-lived **feature branch** isolates your work; teammates review it through a **pull request** (called a *merge request* on GitLab); only then does it join `main`. Many teams also protect `main` so that direct pushes are blocked. This is exactly how a team protects a shared automation suite from broken tests.

**Pull request in one paragraph.** A pull request (PR) is a feature of the hosting service, not of Git itself: it says "I have commits on branch X; please review and merge them into `main`". Reviewers comment on the lines, CI may run your tests automatically, and when approved, someone clicks "Merge". Afterwards you update your local `main` with `git pull` and delete the feature branch.

### 8. Authentication: How the Remote Knows It Is You

To push (and to pull from private repositories), the hosting service must verify your identity. The two main methods:

**HTTPS with a personal access token.**
URL looks like `https://github.com/user/repo.git`. When Git asks for a password, services no longer accept your account password; you create a **personal access token** in your account settings and use it as the password. A **credential helper** stores it so you do not retype it (Git for Windows and macOS include one; or `git config --global credential.helper store` on Linux, which saves in plain text, so use a proper helper where possible).

**SSH keys.**
URL looks like `git@github.com:user/repo.git`. You generate a key pair on your computer:

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```

You then upload the **public** key (the `.pub` file) to your account. The **private** key stays on your machine and must never be shared or committed. Test the connection with `ssh -T git@github.com`.

Switch an existing clone between the two by changing the URL: `git remote set-url origin git@github.com:user/repo.git`.

**Security reminders for QE work:** never commit passwords, API keys, tokens or `.env` files. Add them to `.gitignore` before the first commit. If a secret is ever pushed, consider it compromised and rotate it; deleting it in a later commit does not remove it from history.

### 9. Identity Settings Reminder

Commits are labelled with a name and email. Set them once:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --list --show-origin     # review your settings (and where they come from)
```

### 10. Troubleshooting Table

| Message / Situation | Meaning | What to do |
|---------------------|---------|-----------|
| `! [rejected] main -> main (fetch first)` or `(non-fast-forward)` | Remote has commits you lack | `git pull --rebase` (or merge), then `git push` |
| `fatal: Need to specify how to reconcile divergent branches` | Diverged histories; no default strategy set | Use `--rebase`, `--no-rebase` or `--ff-only`; set `pull.rebase` |
| `fatal: Not possible to fast-forward, aborting.` | `--ff-only` and history diverged | Choose merge or rebase deliberately |
| `fatal: The current branch X has no upstream branch` | First push of a new branch | `git push -u origin X` |
| `Everything up-to-date` but you expected changes | You did not commit, or you are on a different branch | `git status`, `git log`, `git branch` |
| `fatal: Authentication failed` / `Permission denied (publickey)` | Wrong or expired token; key not uploaded | Create a new token; check SSH key setup |
| `error: Your local changes would be overwritten by merge` | Uncommitted edits conflict with incoming changes | Commit or stash first |
| `CONFLICT (content): Merge conflict in ...` | Overlapping edits | Wednesday's lesson; for now `git merge --abort` / `git rebase --abort` to back out |
| `fatal: refusing to merge unrelated histories` | Two repositories with no common ancestor (for example, an initial commit created on both GitHub and locally) | Usually clone the remote instead; ask for help before using `--allow-unrelated-histories` |
| `remote: Permission to ... denied` | You lack write access | Ask the owner for access, or work on a fork and open a pull request |
| `error: src refspec main does not match any` | Branch `main` doesn't exist locally (maybe it is `master`), or no commits yet | `git branch`; make a commit first |

---

## Code Examples (Shell Commands)

All examples below use a **local bare repository** as a stand-in for GitHub, so you can practise on one computer with no accounts and no network. A "bare" repository has no working files; it is what a hosting service holds.

### Example 1: Simulate a team on your own computer

```bash
# Create a workspace
mkdir git-collab-lab && cd git-collab-lab

# The "remote" (like GitHub): a bare repository
git init --bare -b main remote.git

# Two team members, each with a clone
git clone remote.git alice
git clone remote.git bob
```

(Git will warn "You appear to have cloned an empty repository". That is expected.)

**Alice makes the first commit and pushes** (in a second terminal or after `cd alice`):

```bash
cd alice
git config user.name "Alice"
git config user.email "alice@example.com"
git switch -c main            # the empty clone may have no branch yet; this creates 'main'
echo "# QE Foundations" > README.md
git add README.md
git commit -m "Initial commit"
git push -u origin main
git remote -v
git branch -vv
```

Expected from `push`: lines such as `* [new branch]  main -> main` and `branch 'main' set up to track 'origin/main'.` The `branch -vv` shows `[origin/main]`.

**Bob gets it:**

```bash
cd ../bob
git config user.name "Bob"
git config user.email "bob@example.com"
git pull                       # first pull brings in Alice's commit
git log --oneline              # one commit: Initial commit
```

### Example 2: Provoke and fix a rejected push

Both people now commit **different files** (so there will be no conflict) and Alice pushes first.

```bash
# Bob (still in ./bob)
echo "bob's notes" > bob.txt
git add bob.txt
git commit -m "Bob adds notes"

# Alice
cd ../alice
echo "alice's notes" > alice.txt
git add alice.txt
git commit -m "Alice adds notes"
git push                       # succeeds: remote moves forward
```

Now Bob tries to push:

```bash
cd ../bob
git push
```

Result: `! [rejected] main -> main (fetch first)`. Bob follows the safe procedure:

```bash
git fetch                              # download Alice's commit; origin/main moves
git status -sb                         # ## main...origin/main [ahead 1, behind 1]
git log --oneline HEAD..origin/main    # shows: Alice adds notes
git diff --stat HEAD...origin/main     # alice.txt | 1 +
git log --oneline --graph --all        # shows the fork in history
git pull --rebase                      # replay Bob's commit on top of Alice's
git log --oneline --graph              # now a straight line
git push                               # succeeds
```

**What to notice:**

- `fetch` changed nothing in Bob's working folder (no `alice.txt` appeared) but updated the `origin/main` bookmark; only `pull` changed his files.
- After `pull --rebase`, Bob's commit has a **new ID** (it was replayed), and the history is linear.
- If Bob had run `git pull` with no configuration, Git 2.27+ would have stopped with the "need to specify how to reconcile divergent branches" message; Bob would add `--rebase`, `--no-rebase` or `--ff-only`.

### Example 3: Try the merge strategy instead

Repeat the same scenario (new commits by both) but have Bob run:

```bash
git pull --no-rebase --no-edit
```

Output: `Merge made by the 'ort' strategy.` and a diffstat. `git log --oneline --graph` now shows a diamond shape with a **merge commit**. (`--no-edit` accepts the default merge message without opening an editor.) Compare this graph with the linear one from Example 2. Both are correct; they differ in style.

### Example 4: Feature branch publish and clean-up

```bash
cd bob
git switch -c feature/login-tests
echo "def test_login(): pass" > test_login.py
git add test_login.py
git commit -m "Add login test placeholder"

git push                              # fails: no upstream branch (Git prints the exact command to use)
git push -u origin feature/login-tests   # works and sets the upstream
git branch -vv                        # shows [origin/feature/login-tests]
git branch -r                         # remote-tracking branches

# later, after the work is merged on the hosting service:
git switch main
git pull --ff-only
git branch -d feature/login-tests                 # delete the local branch
git push origin --delete feature/login-tests      # delete the remote branch
git fetch --prune                                 # (teammates) remove stale origin/feature/login-tests
```

(`git branch -d` refuses to delete a branch whose work is not merged into your current branch, a useful safety check. In this local simulation, make sure the branch has been merged into `main` first, or the command will tell you so.)

### Example 5: Sharing today's Python project

Putting this lesson together with the earlier ones, here is the sequence for Project 1's kickoff (the exercise gives full details):

```bash
mkdir qe-foundations && cd qe-foundations
git init -b main
python -m venv .venv
# .gitignore must exist BEFORE the first commit so .venv is never tracked
printf ".venv/\n__pycache__/\n*.pyc\n" > .gitignore
mkdir -p src/qa_toolkit tests
touch src/qa_toolkit/__init__.py
printf "requests>=2.31,<3\n" > requirements.txt
git add .gitignore requirements.txt src
git commit -m "Project skeleton: package, requirements, gitignore"
git remote add origin <your-empty-repository-url>
git push -u origin main
```

(On Windows PowerShell use an editor or `Set-Content` to create the files, as `printf` and `touch` are Unix tools. Git Bash supports them.) Note that `git add src` only adds files; an empty `tests/` folder is not tracked by Git until it contains a file (a common convention is to put a placeholder `.gitkeep` file in it).

---

## Practice Questions and Mini-Exercises

**Q1.** What is `origin`? Is it special to Git, or just a name?

**Q2.** Explain the difference between `main` and `origin/main`.

**Q3.** `git branch -vv` shows `[origin/main: ahead 2, behind 3]`. What does each number mean, and what are the next steps?

**Q4.** Why is `git fetch` considered safe? Name two commands to inspect what it brought in.

**Q5.** `git pull` equals which two operations? What difference does `--rebase` make?

**Q6.** You get `! [rejected] main -> main (fetch first)`. Write the sequence of commands to resolve it and explain why a plain `git push --force` is the wrong answer.

**Q7.** What does `git push -u origin feature/x` do that `git push origin feature/x` does not?

**Q8.** Name two situations where `git pull --ff-only` would refuse to proceed. Why might a beginner prefer it?

**Q9 (hands-on).** Using the local bare repository setup from Example 1: (a) have Alice and Bob both clone it; (b) Alice creates `validators.py` and pushes; (c) Bob pulls and sees it; (d) Bob adds `formatters.py` while Alice adds `README.md` and pushes first; (e) Bob resolves the rejected push with `fetch`, inspection commands and `pull --rebase`; (f) show the final `git log --oneline --graph`.

**Q10 (scenario).** A teammate says "I fixed the failing test and pushed, but you can't see it on my machine's `main` because I only committed, not pushed." What mistake is this, and how do they verify what is on the remote?

**Q11 (design).** Your team protects `main` so nobody pushes directly. Describe the end-to-end flow for adding one new test helper from your laptop to `main`.

**Q12 (safety).** You accidentally committed an API token and pushed. List your actions in order.

---

### Answers

**A1.** `origin` is the default *name* Git gives to the remote repository you cloned from. It is just a nickname for a URL; you can rename it or add other remotes.

**A2.** `main` is your local branch, which you move by committing. `origin/main` is a remote-tracking branch: Git's record of where the remote `main` was at your last fetch/pull/push. You do not commit on it directly, and it only updates when you communicate with the remote.

**A3.** Your local branch has 2 commits the remote does not have (ahead 2), and the remote has 3 commits you do not have (behind 3). Histories have diverged: integrate the remote's commits (`git pull --rebase`, or `git pull` with a merge) and then `git push`.

**A4.** It only downloads data and updates remote-tracking branches; it never touches your local branches or working files. To inspect: `git log --oneline HEAD..origin/main` and `git diff --stat HEAD...origin/main` (also `git status -sb` and `git log --oneline --graph --all`).

**A5.** `git fetch` followed by integrating `origin/<branch>` into the current branch. By default the integration is a merge; with `--rebase` your local commits are replayed on top of the fetched ones, giving a linear history.

**A6.**

```bash
git fetch
git log --oneline HEAD..origin/main     # review what you're missing
git pull --rebase                        # or: git pull --no-rebase
# run the tests; resolve conflicts if any
git push
```

A forced push would overwrite the remote branch with your history and delete your teammate's commits from it.

**A7.** `-u` (`--set-upstream`) also records that the local branch tracks `origin/feature/x`, so later `git push`/`git pull` need no arguments and `git status` can report ahead/behind. Without it, a new branch's plain `git push` fails with "no upstream branch".

**A8.** When your branch has diverged (you have local commits and the remote has new ones), and in other cases where a fast-forward is impossible. A beginner may prefer it because it never creates surprise merges or rewrites; it stops, and you choose consciously.

**A9.** A sample sequence follows the commands in Examples 1 and 2, with files `validators.py`, `formatters.py` and `README.md` instead. The final graph should be a straight line (after `pull --rebase`) containing: Initial/validators commit, Alice's README commit, Bob's formatters commit.

**A10.** The teammate committed but never pushed. Committing only records history locally. They should run `git push`, then check with `git status -sb` (no `ahead`), `git log origin/main --oneline`, or by viewing the branch on the hosting website.

**A11.** (1) `git switch main && git pull --ff-only` (2) `git switch -c feature/new-helper` (3) write the helper and its tests, commit in small steps (4) `git fetch` and `git pull --rebase origin main` to include recent changes, re-run tests (5) `git push -u origin feature/new-helper` (6) open a pull request, respond to review comments with further commits and pushes, wait for CI to pass (7) a reviewer merges; you `git switch main`, `git pull`, delete the feature branch locally and remotely.

**A12.** (1) **Revoke/rotate the token immediately** at the provider; this is the essential step. (2) Remove it from the code and use an environment variable or untracked config instead; add the file to `.gitignore`. (3) Inform your team/security contact per company policy. (4) Optionally rewrite history to purge the secret (a specialised operation; seek help). Remember that deleting it in a new commit does not remove it from earlier commits.

---

## Summary / Key Takeaways

- Git is distributed: each clone is a full repository. The **remote** (default name `origin`) is the shared copy; `git clone` sets it up and `git remote -v` shows it.
- **Remote-tracking branches** such as `origin/main` record where the remote was at your last contact; they update only when you fetch, pull or push. `git branch -vv` and `git status -sb` show ahead/behind counts.
- **`git fetch`** downloads without touching your files, so it is safe. Inspect with `git log HEAD..origin/main`, `git diff HEAD...origin/main`, and `git log --graph --all`.
- **`git pull`** = fetch + integrate (merge by default; `--rebase` for a linear history; `--ff-only` to refuse anything but a fast-forward). Choose and set a team-consistent strategy. Conflicts (covered on Wednesday) can be aborted with `git merge --abort` or `git rebase --abort`.
- **`git push`** publishes commits. Use `-u` for a branch's first push. A rejected push means "integrate the remote's work first": **fetch/pull, then push**; do not force-push shared branches.
- Work on **feature branches**, pull often, commit small, and publish through pull requests. Keep secrets, `.venv` and other generated files out of Git with `.gitignore`.
- Authenticate with a personal access token (HTTPS) or SSH keys.

---

## Additional Resources

- Pro Git book - Working with Remotes: https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes
- Git documentation - `git pull`: https://git-scm.com/docs/git-pull
- Git documentation - `git push`: https://git-scm.com/docs/git-push
