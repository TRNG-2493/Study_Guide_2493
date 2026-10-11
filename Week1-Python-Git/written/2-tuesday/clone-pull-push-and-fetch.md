# Clone, Pull, Push and Fetch

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a remote repository is and why teams use one (GitHub, GitLab, Bitbucket).
- Describe the relationship between a local repository, a remote and the name `origin`.
- Create a repository on GitHub and connect your local project to it.
- Use `git clone` to copy a remote repository to your computer.
- Use `git push` to upload commits and `git pull` to download and integrate them.
- Use `git fetch` to download without integrating, and explain how it differs from `git pull`.
- Inspect remotes with `git remote -v` and understand remote-tracking branches such as `origin/main`.
- Understand the common authentication methods and recognise and resolve common push/pull errors.

---

## Why This Matters

Until now, your repository has lived only on your computer. That means:

- If your laptop breaks, the work is gone.
- Nobody else can see or contribute to it.
- A build server can't fetch your tests to run them automatically.

A **remote repository** solves all of this. It is a copy of your repository hosted on a server, which acts as the shared "source of truth" for the team. Every professional automation team works this way: engineers write tests locally, **push** them to a remote, and CI systems **pull** them to run.

Today's demo and exercise ask you to clone, push and eventually open a pull request. This lesson gives you the commands that make that possible. They build directly on Monday's `add`, `commit`, `status` and `log`, and they unlock the collaborative workflow for the rest of the program.

---

## The Concept

### 1. Local vs Remote

| | Local repository | Remote repository |
|---|---|---|
| Where | On your computer | On a server (GitHub, GitLab, Bitbucket...) |
| Who can access | You | You and your teammates, depending on permissions |
| You work in it | Yes: edit files, commit | Not directly; you send and receive commits |
| Offline | Works offline | Needs the network |

```
   YOUR COMPUTER                                   THE SERVER
 ┌────────────────────┐                       ┌────────────────────┐
 │ Local repository   │ ──── git push ──────▶ │ Remote repository  │
 │ (your commits)     │ ◀─── git pull ─────── │ (named "origin")   │
 │                    │ ◀─── git fetch ────── │                    │
 └────────────────────┘                       └────────────────────┘
        ▲
        └──── git clone  (the very first copy comes down from the server)
```

**Git vs GitHub, again:** Git is the tool. GitHub (and GitLab, Bitbucket) are services that host remote repositories and add collaboration features such as pull requests (the next lesson). The commands in this lesson work with any of them.

#### The name `origin`

A remote has a **name** and a **URL**. By convention, the main remote is called **`origin`**. The name is just a convenient nickname for a long URL, so you can type `git push origin main` instead of the entire web address. When you `clone` a repository, Git sets up `origin` for you automatically.

---

### 2. Preparing: A GitHub Account and Authentication

1. Create a free account at **https://github.com** (or use the account your organization provides).
2. Make sure your `user.email` in `git config` matches an email on your account, so commits are linked to you.

#### How does GitHub know it's you?

When you push, GitHub needs to verify your identity. Passwords for Git operations are no longer accepted. The two common methods:

| Method | URL looks like | How it works |
|---|---|---|
| **HTTPS** | `https://github.com/user/repo.git` | You sign in via a browser (Git Credential Manager, which comes with Git for Windows and is available on macOS/Linux) or use a **personal access token** (PAT) in place of a password |
| **SSH** | `git@github.com:user/repo.git` | You create an **SSH key pair**, and upload the public key to your GitHub account; no password prompts afterwards |

For beginners, **HTTPS with the credential manager** is simplest: the first `push` or `clone` of a private repo opens a browser window to sign in, and Git remembers you. Your instructor will tell you which method your team uses. If you choose a personal access token, treat it like a password: never commit it, never share it (see the secrets section of the `.gitignore` lesson).

SSH setup is a few more steps (generate a key with `ssh-keygen`, add it to GitHub). GitHub's documentation has a step-by-step guide linked in the resources.

---

### 3. `git clone`: Copy a Remote Repository

`git clone` downloads a complete copy of a remote repository, including **all of its history**, and sets everything up so you can start working.

```bash
git clone https://github.com/your-username/qa-practice.git
```

What happens:

1. Git creates a new folder named after the repository (`qa-practice`).
2. It downloads all files and the full commit history.
3. It sets up a remote called `origin` pointing to the URL.
4. It checks out the default branch (usually `main`) so the files are ready to edit.

```text
Cloning into 'qa-practice'...
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
Receiving objects: 100% (12/12), done.
```

Then move in and look around:

```bash
cd qa-practice
git log --oneline
git status
```

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

`Your branch is up to date with 'origin/main'` is new. It tells you how your local `main` compares with the remote's `main` (more on this in section 7).

**Clone into a specific folder name:**

```bash
git clone https://github.com/your-username/qa-practice.git my-folder
```

**Where to get the URL:** on a GitHub repo page, click the green **Code** button and copy the HTTPS (or SSH) URL.

**Clone vs init:**

| | `git init` | `git clone` |
|---|---|---|
| Use when | Starting a brand-new project locally | Getting a copy of an existing project |
| Remote configured? | No | Yes: `origin` |
| History | Empty | Complete copy |

---

### 4. Connecting an Existing Local Repository to a Remote

What if you started locally (as on Monday) and want to put the project on GitHub?

**Step 1: create an empty repository on GitHub.**
Click **+ → New repository**, give it a name (e.g. `qa-practice`) and choose public or private. **Do not** tick "Add a README", ".gitignore" or "license" when you already have local commits; an empty remote avoids conflicting histories.

**Step 2: link your local repository to it:**

```bash
git remote add origin https://github.com/your-username/qa-practice.git
```

- `git remote add` registers a remote.
- `origin` is the nickname.
- The URL is the repo address.

**Step 3: verify:**

```bash
git remote -v
```

```text
origin  https://github.com/your-username/qa-practice.git (fetch)
origin  https://github.com/your-username/qa-practice.git (push)
```

`-v` (verbose) shows the URLs. Each remote has a fetch URL and a push URL, usually identical.

**Step 4: make sure your branch is named `main`**, then push for the first time (next section).

Other remote commands you may need:

```bash
git remote set-url origin <new-url>     # fix a wrong URL
git remote remove origin                # remove a remote
```

---

### 5. `git push`: Upload Your Commits

`git push` sends your **local commits** to the remote.

**First push of a new branch:**

```bash
git push -u origin main
```

- `git push` uploads commits.
- `origin` is where to send them.
- `main` is the branch to push.
- `-u` (short for `--set-upstream`) links your local `main` to `origin/main`, so in future you can type just `git push` and `git pull` without extra arguments.

```text
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Writing objects: 100% (9/9), 1.02 KiB | 1.02 MiB/s, done.
To https://github.com/your-username/qa-practice.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

Refresh the GitHub page, and your files and commit history appear.

**Every push after that:**

```bash
git add file.py
git commit -m "Add input validation"
git push
```

Important: **push sends commits, not uncommitted changes.** If you only saved a file but haven't committed, nothing is sent. The sequence is always edit, add, commit, push.

#### When a push is rejected

```text
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '...'
hint: Updates were rejected because the remote contains work that you do
hint: do not have locally.
```

This means someone (or you, from another computer, or by editing on the GitHub website) added commits to the remote that you don't have yet. Git refuses to overwrite them. The fix: **pull first**, then push again.

```bash
git pull
git push
```

**Never use `git push --force` as a quick fix.** It overwrites remote history and can destroy teammates' work. Beginners should avoid it entirely.

---

### 6. `git pull` and `git fetch`: Get Remote Changes

Teammates add commits to the remote while you work. You need to bring them into your local repository. There are two commands, and the difference is important.

#### 6.1 `git fetch`: download, but don't change my work

```bash
git fetch
```

`git fetch` contacts the remote and **downloads new commits and branch information**, but it does **not** change your working files or your current branch. It's a safe, read-only way to see what's new.

After fetching, you can inspect the changes:

```bash
git log --oneline main..origin/main     # commits on the remote that I don't have
git diff main origin/main               # what changed
```

(The `..` notation means "commits reachable from the second but not the first".)

#### 6.2 `git pull`: download AND integrate

```bash
git pull
```

`git pull` is a shortcut for two steps:

```
git pull  =  git fetch  +  git merge
```

1. **Fetch** the new commits from the remote.
2. **Merge** them into your current branch, so your files are updated.

Output when there are new commits:

```text
Updating 3f2a9c1..8d4b7e2
Fast-forward
 login_test.py | 12 ++++++++++++
 1 file changed, 12 insertions(+)
```

Output when there is nothing new:

```text
Already up to date.
```

**Fast-forward** means your branch had no new commits of its own, so Git simply moved your branch pointer forward to the remote's latest commit. If both you and the remote have new commits, Git creates a **merge commit** that combines them (and might ask for a message in an editor; just save and close). Merging in depth, including how to resolve conflicts, is covered on **Wednesday** in the branching lesson.

#### 6.3 fetch vs pull

| | `git fetch` | `git pull` |
|---|---|---|
| Downloads new commits | Yes | Yes |
| Changes your current branch and files | **No** | **Yes** (merges) |
| Risk of conflicts | None | Possible |
| Use when | You want to look before you integrate | You are ready to update your work |

**Analogy:** `fetch` is checking your mailbox and bringing the letters home, but leaving them unopened on the table. `pull` is bringing the letters home *and* filing them into your folders.

A good habit: **pull before you start working**, and **pull before you push**. This keeps your copy fresh and reduces conflicts.

---

### 7. Remote-Tracking Branches and `status`

When you fetch or pull, Git remembers where the remote's branches were at that moment, using **remote-tracking branches** such as `origin/main`. They are read-only bookmarks you can't commit to directly; they move only when you fetch, pull or push.

```
Remote's main:       A ── B ── C
                                │
origin/main (yours):            C    (your last-known copy of the remote)
                                │
Your main:           A ── B ── C ── D     (you have 1 extra commit)
```

`git status` compares your branch with its tracking branch:

| Message | Meaning | Action |
|---|---|---|
| `Your branch is up to date with 'origin/main'.` | Same as the last known remote state | Nothing |
| `Your branch is ahead of 'origin/main' by 2 commits.` | You have 2 commits not pushed | `git push` |
| `Your branch is behind 'origin/main' by 3 commits.` | The remote has 3 commits you lack | `git pull` |
| `Your branch and 'origin/main' have diverged` | Both have new commits | `git pull` (merge), then `git push` |

Because the comparison uses the *last fetched* information, run `git fetch` first to see the true situation.

`git log` also shows these pointers:

```text
8d4b7e2 (HEAD -> main, origin/main) Add input validation
```

Here local `main` and `origin/main` are on the same commit: you're in sync.

---

### 8. A Typical Daily Workflow

```bash
git pull                              # 1. start fresh
# ... edit files ...
git status                            # 2. see what changed
git add login_test.py                 # 3. stage
git commit -m "Add invalid login test"   # 4. commit
git pull                              # 5. get anything new from teammates
git push                              # 6. share your work
```

Repeat this loop in small increments. Tomorrow and Wednesday you'll refine it with branches, so changes can be reviewed before they reach `main`.

---

### 9. Walkthrough: Starting From GitHub

1. On GitHub create a repository `qa-clone-demo`, tick **Add a README file**.
2. Clone it:
   ```bash
   git clone https://github.com/your-username/qa-clone-demo.git
   cd qa-clone-demo
   ```
3. Create `hello.py` with `print("Hello from clone")`.
4. Commit and push:
   ```bash
   git add hello.py
   git commit -m "Add hello script"
   git push
   ```
5. Edit `README.md` directly on GitHub's website (pencil icon) and commit there.
6. Back in the terminal, observe the difference between:
   ```bash
   git fetch
   git status        # now says "behind by 1 commit"
   git pull          # brings in the README change
   ```

---

### 10. Common Problems

| Problem | Likely cause | Fix |
|---|---|---|
| `fatal: repository not found` | Wrong URL, or no permission | Check the URL and your account's access |
| `Authentication failed` | Wrong credentials or expired token | Re-authenticate; create a new token; check SSH key |
| `rejected ... fetch first` | Remote has commits you lack | `git pull`, then `git push` |
| `fatal: The current branch main has no upstream branch` | First push of a branch | `git push -u origin main` |
| `fatal: remote origin already exists` | Added `origin` twice | `git remote set-url origin <url>` |
| `refusing to merge unrelated histories` | Local and remote were created independently (e.g. README added on GitHub plus local commits) | Start with an empty remote, or ask your instructor about `--allow-unrelated-histories` |
| Pushed, but nothing appears on GitHub | You didn't commit, or pushed a different branch | `git status`, `git log`; check the branch name |
| Merge editor opens after `git pull` | Git needs a merge-commit message | Save and close the editor |
| Merge conflict message | Same lines changed in both places | Covered on Wednesday; ask for help rather than guessing |

---

### 11. Practice Activities

1. **Account check.** Sign in to GitHub and create a new empty repository named `week1-practice`. Copy its HTTPS URL.
2. **Local to remote.** Use the repository from Monday. Add the remote, verify with `git remote -v`, and push with `git push -u origin main`. Confirm commits on GitHub.
3. **Clone.** Clone your repo into a *different* folder (for example `week1-practice-copy`). Compare `git log --oneline` in both folders.
4. **Simulate a teammate.** In the copy folder, make a commit and push it. Return to the original folder and run `git fetch`, then `git status`. What does it say? Then run `git pull`.
5. **Rejected push.** Make a commit in both folders (different files). Push from the first, then try to push from the second. Read the error, fix it by pulling, and push again.
6. **Fetch vs pull.** Explain, in three sentences, the difference and when you'd choose each. Show with `git log --oneline main..origin/main` what `fetch` lets you see.
7. **Reading status.** Make two local commits without pushing. Run `git status`: what does it say? Push and check again.
8. **Explain it.** Draw a diagram showing working directory, staging, local repo and remote, and label the commands (`add`, `commit`, `push`, `fetch`, `pull`, `clone`) on the arrows.
9. **Safety.** Verify your `.gitignore` is pushed and that `.env` (a fake one) never reaches GitHub.

---

## Summary

- A **remote repository** (GitHub, GitLab, Bitbucket) is a shared copy on a server for backup, collaboration and CI. By convention the main remote is called **`origin`**.
- **`git clone <url>`** copies a remote repo (full history) and sets up `origin`. Use `git init` for new projects, `git clone` for existing ones.
- **`git remote add origin <url>`** connects an existing local repo; **`git remote -v`** lists remotes.
- **`git push`** uploads **committed** work. The first push uses `git push -u origin main`; later pushes need just `git push`.
- **`git fetch`** downloads remote changes without touching your work; **`git pull`** = fetch + merge.
- `origin/main` is your last-known snapshot of the remote's `main`; `git status` tells you if you are ahead, behind or diverged.
- A rejected push usually means: **pull first**, then push. Avoid `--force`.
- Pull before you start, and before you push. Never commit secrets or tokens.
- Next: the **pull-request workflow**, the standard way teams review and merge changes.

---

## Additional Resources

- Pro Git book: Working with Remotes: https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes
- GitHub Docs: About remote repositories: https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories
- GitHub Docs: Connecting to GitHub with SSH: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
