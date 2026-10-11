# Basic Pull-Request / Merge-Request Workflow

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a pull request (PR) or merge request (MR) is and why teams use them.
- Describe the full PR workflow from updating `main` to cleaning up after the merge.
- Create a working branch, commit to it and push it to the remote.
- Open a pull request on GitHub (or a merge request on GitLab) with a clear title and description.
- Understand code review: how to give and respond to comments, and how to update a PR.
- Describe the three common merge options (merge commit, squash, rebase) at a high level.
- Sync your local repository after a PR is merged.
- Follow good PR etiquette and avoid common mistakes.

---

## Why This Matters

Imagine a team of ten engineers all pushing straight to `main`. One person's half-finished change breaks the tests everyone depends on. Nobody reviewed it. Nobody knows why it was done.

Professional teams solve this with the **pull-request workflow**: nobody changes `main` directly. Instead, each change is made on a separate **branch**, proposed through a **pull request**, **reviewed** by teammates, checked by **automated tests** and only then merged.

For a test automation engineer this matters twice:

1. **Your own test code goes through PRs.** Teammates review your tests for quality, readability and correctness.
2. **PRs run automated checks.** When you open a PR, a CI pipeline typically runs the test suite. This is a place where your automation work directly protects the product.

Today's demo and exercise end with you pushing work through a PR. This lesson connects what you learned on Monday (commits) and earlier today (clone, push, pull, `.gitignore`) into one complete workflow.

---

## The Concept

### 1. Key Terms

| Term | Meaning |
|---|---|
| **Branch** | A separate line of development, an independent copy of the work where you can make changes without affecting `main` |
| **Pull Request (PR)** | A request, on GitHub, to merge the commits of one branch into another (usually `main`). A page for discussion, review and checks |
| **Merge Request (MR)** | The same thing on **GitLab** |
| **Review** | Teammates read your changes and comment, approve or request changes |
| **Merge** | Combining the branch's commits into the target branch |
| **Base branch** | The branch you want to merge *into* (usually `main`) |
| **Head / compare branch** | The branch that has your changes |

The name "pull request" can be confusing: you are *requesting* that the maintainers *pull* your changes into their branch.

> **Branches preview:** this lesson uses just two branch commands so you can complete the workflow. **Wednesday's lesson covers branching in depth**: how branches work internally, switching between them, merging and resolving conflicts.

---

### 2. The Workflow at a Glance

```
 1. Update main          git switch main, git pull
        │
 2. Create a branch      git switch -c feature/login-test
        │
 3. Make changes         edit → git add → git commit (repeat)
        │
 4. Push the branch      git push -u origin feature/login-test
        │
 5. Open a PR            on GitHub: base main ← compare feature/login-test
        │
 6. Review + checks      teammates comment; CI runs; you push fixes
        │
 7. Merge                a maintainer (or you) clicks Merge
        │
 8. Clean up             git switch main, git pull, delete the branch
```

We'll go through each step.

---

### 3. Step 1: Start From an Up-to-Date `main`

```bash
git switch main
git pull
```

- `git switch main` moves you onto the `main` branch.
- `git pull` makes sure your local `main` has the latest commits.

Starting from a fresh `main` avoids a lot of conflicts later.

> Older tutorials use `git checkout` for switching branches. `git switch` is the newer, clearer command. Both work.

---

### 4. Step 2: Create a Branch

```bash
git switch -c feature/add-login-test
```

- `-c` means **create** the branch, then switch to it.
- `feature/add-login-test` is the branch name.

Confirm where you are:

```bash
git status
```

```text
On branch feature/add-login-test
nothing to commit, working tree clean
```

Any commits you make now go onto this branch, **not** `main`.

#### Branch naming conventions

Names should be short, lowercase, hyphenated and descriptive. Many teams add a prefix:

| Prefix | Use for | Example |
|---|---|---|
| `feature/` | New functionality or tests | `feature/add-login-test` |
| `fix/` or `bugfix/` | Fixing a problem | `fix/flaky-search-test` |
| `docs/` | Documentation | `docs/update-readme` |
| `chore/` | Maintenance | `chore/add-gitignore` |

Avoid spaces and vague names like `my-branch` or `test`. Follow your team's convention if it has one.

---

### 5. Step 3: Make Changes and Commit

Do your work exactly as you learned on Monday. Make **small, focused commits** with good messages:

```bash
# edit login_test.py
git add login_test.py
git commit -m "Add test for valid login"

# edit login_test.py again
git add login_test.py
git commit -m "Add test for invalid password"
```

Keep the PR **focused on one purpose**. If you notice an unrelated problem, fix it in a separate branch and PR.

---

### 6. Step 4: Push the Branch

```bash
git push -u origin feature/add-login-test
```

This uploads your branch to the remote, where it appears as a new branch. `-u` links your local branch to the remote one (as you saw with `main` in the last lesson).

The output often includes a helpful link:

```text
remote: Create a pull request for 'feature/add-login-test' on GitHub by visiting:
remote:      https://github.com/your-username/qa-practice/pull/new/feature/add-login-test
```

You can click that link, or follow the next step.

---

### 7. Step 5: Open the Pull Request

On GitHub:

1. Open your repository page. A yellow banner usually shows **"Compare & pull request"** for a recently pushed branch. Click it. (Otherwise: **Pull requests → New pull request**.)
2. Check the two branch selectors:
   - **base:** `main` (where the changes will go)
   - **compare:** `feature/add-login-test` (your changes)
3. Fill in the **title** and **description** (see below).
4. Review the **Files changed** tab to see exactly what you are proposing, in diff form. Read it yourself first, as if you were the reviewer.
5. Click **Create pull request**.

On **GitLab** the equivalent is **Merge requests → New merge request**; the steps and ideas are identical.

#### Writing a good PR title and description

**Title:** a short, specific summary, like a commit message in the imperative mood.

| Weak | Strong |
|---|---|
| `Update` | `Add login tests for valid and invalid credentials` |
| `Fixes` | `Fix flaky timeout in search test` |

**Description:** help the reviewer understand quickly. A simple template:

```markdown
## What
Adds two tests for the login page: valid login and invalid password.

## Why
Login had no automated coverage (see issue #12).

## How to test
Run `python login_test.py` and confirm both tests print PASS.

## Notes
No changes to existing files.
```

Useful extras:

- **Link an issue**: writing `Closes #12` in the description automatically links and closes issue 12 when the PR is merged.
- **Screenshots or output** showing the result.
- **Draft PR**: GitHub lets you open a **draft** if work is not yet ready for review. Convert it with **Ready for review** when done.

---

### 8. Step 6: Review and Checks

After opening a PR, two things typically happen:

#### Automated checks

Many repositories run **CI (continuous integration)**, an automated process that runs tests, linting, or builds on every PR. You'll see green ticks or red crosses near the bottom of the PR page. If a check fails, click **Details**, read the log, fix the problem locally and push again. CI is covered later in the program.

#### Human review

Reviewers read your changes in the **Files changed** tab and can:

- **Comment** on specific lines (hover over a line and click the **+**).
- **Approve** the PR.
- **Request changes**, indicating that something must be fixed before merging.

**Responding to feedback:**

1. Read each comment carefully and assume good intent; review is about the code, not about you.
2. Make the fixes **on the same branch** locally:

   ```bash
   # edit the file as requested
   git add login_test.py
   git commit -m "Rename test functions as suggested in review"
   git push
   ```

3. The PR **updates automatically** with your new commits. No need to open a new one.
4. Reply to the comments ("Done", or explain if you disagree politely) and mark conversations resolved.

**Giving a review** (you will review a partner's PR this week):

- Be specific and kind: "Could we rename `x` to `response_time`? It would make the check clearer."
- Distinguish **must fix** from **optional suggestions**.
- Check: Does it do what the title says? Is it readable? Are there leftover debug prints or secrets? Are tests included?
- Say what is good too.

---

### 9. Step 7: Merge

When the PR is approved and the checks are green, it can be merged. GitHub offers three styles:

| Option | What it does | Resulting history |
|---|---|---|
| **Create a merge commit** | Keeps all commits from the branch and adds a merge commit | Complete history, a bit busier |
| **Squash and merge** | Combines all the branch's commits into **one** commit on `main` | Clean, one commit per PR |
| **Rebase and merge** | Replays commits on top of `main` without a merge commit | Linear history |

You don't need to master these today. Teams usually choose one default (many choose **squash**), and your instructor or team lead will tell you which to use. If the repository has **branch protection**, it may require approvals and passing checks before the **Merge** button is enabled.

What if GitHub says **"This branch has conflicts that must be resolved"**? It means that someone changed the same lines on `main`. We'll learn how to resolve conflicts properly on Wednesday; until then, ask for help rather than guessing.

---

### 10. Step 8: Clean Up and Sync

After the merge, `main` on GitHub contains your work, but your local `main` doesn't know yet:

```bash
git switch main
git pull
```

Now delete the finished branch, locally and on the remote:

```bash
git branch -d feature/add-login-test             # local
git push origin --delete feature/add-login-test  # remote
```

(GitHub also offers a **Delete branch** button right after merging, which handles the remote copy.)

`git branch -d` only deletes a branch that has been fully merged, so it's safe. List your branches any time with `git branch`.

Then start the next task from step 1.

---

### 11. Full Example, End to End

```bash
git switch main
git pull
git switch -c fix/zero-padding-in-test-ids

# edit formatter.py
git add formatter.py
git commit -m "Fix zero-padding for single-digit test numbers"

git push -u origin fix/zero-padding-in-test-ids
# open the PR on GitHub, wait for review, merge it there

git switch main
git pull
git branch -d fix/zero-padding-in-test-ids
```

---

### 12. Good PR Habits

- **Keep PRs small** (ideally a few hundred lines at most). Small PRs are reviewed faster and more carefully.
- **One purpose per PR.**
- **Review your own PR first** in the *Files changed* tab.
- **Don't commit secrets or generated files**: check that your `.gitignore` is doing its job.
- **Run your code/tests before** requesting a review.
- **Respond promptly**, and be gracious about feedback.
- **Don't push directly to `main`** unless your team says so; many repositories block it.
- **Don't force-push** to a branch others are reviewing.

---

### 13. Common Problems

| Problem | Cause | Fix |
|---|---|---|
| The "Compare & pull request" banner doesn't appear | Branch not pushed | `git push -u origin <branch>` |
| PR shows far more changes than expected | Branch created from an outdated or wrong branch | Check `git log`; start again from an updated `main` |
| Commit went onto `main` instead of the branch | You forgot to switch first | Ask for help before trying to undo; undoing commits is covered later |
| PR has conflicts | `main` changed the same lines | Wednesday's lesson; ask for help until then |
| CI check is red | Test failure, or style problem | Open the log, fix locally, push again |
| Wrong base branch | PR targets the wrong branch | Edit the PR's base branch at the top of the page |
| Local `main` is behind after merge | You haven't pulled | `git switch main` then `git pull` |
| Can't push to the repo (403) | No write permission | Ask the owner for access; or fork the repository (advanced) |

---

### 14. Practice Activities

Work in your `week1-practice` repository from the last lesson. (If you work in pairs, take turns being author and reviewer.)

1. **Branch.** From an updated `main`, create `feature/add-readme-details`. Confirm with `git status`.
2. **Commits.** Add a longer description to `README.md` in two separate commits with clear messages.
3. **Push.** Push the branch with `-u`. Find it on GitHub's branch list.
4. **Open a PR.** Use the **Compare & pull request** button. Write a title and a description with *What*, *Why* and *How to test* sections. Read the *Files changed* tab.
5. **Review.** Ask a partner (or your instructor) to comment on at least one line. Respond by pushing another commit to the same branch and watch the PR update.
6. **Merge.** Merge the PR (using your team's default style). Note which merge style you chose and how it affects `git log --oneline`.
7. **Sync and clean up.** Switch to `main`, pull, confirm your commits arrived and delete the local and remote branch.
8. **Review a PR.** Review a partner's PR: leave one specific comment, one positive comment and either approve or request changes.
9. **Explain it.** Write down, in your own words, why a team would use PRs rather than pushing everything directly to `main`.

---

## Summary

- A **pull request** (GitHub) or **merge request** (GitLab) proposes merging one branch into another and creates a space for **review, discussion and automated checks**.
- The workflow: **update `main` → create a branch → commit → push the branch → open a PR → review and fix → merge → pull `main` and clean up**.
- Create a branch with `git switch -c <name>`, move between branches with `git switch <name>`, and push with `git push -u origin <name>`. Branching in depth comes **Wednesday**.
- Good PRs are **small, focused**, and have a clear **title and description** (what, why, how to test), and may link issues (`Closes #12`).
- Update a PR by committing and pushing to the **same branch**; reviewers can comment, approve or request changes; CI checks must usually pass.
- Merge styles (merge commit, squash, rebase) differ in how history looks; follow your team's default.
- After merging, **pull `main`** and **delete the branch**.
- Together with clone, push, pull and `.gitignore`, you now have the complete day-to-day collaboration loop that you will use throughout this program.

---

## Additional Resources

- GitHub Docs: About pull requests: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
- GitHub Docs: Creating a pull request: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
- GitLab Docs: Merge requests: https://docs.gitlab.com/ee/user/project/merge_requests/
