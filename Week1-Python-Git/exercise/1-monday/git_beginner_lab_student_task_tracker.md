# Git Beginner Lab: Student Task Tracker

## Scenario

You are part of a team building a simple **Student Task Tracker**. The project needs a README, a list of tasks, and a way to track changes made by different contributors.

You will create a local Git repository, make and inspect commits, ignore temporary files, publish the repository remotely, and submit a change through a Pull Request (PR) or Merge Request (MR).

**Final goal:** A remote repository with at least three meaningful commits, a working `.gitignore`, a feature branch, and a PR/MR ready for review or merged into the `main` branch.

## Exercise instructions for students

**Suggested duration:** 75–90 minutes  
**Level:** Beginner  
**Format:** Individual practice, followed by a partner review  
**Tools:** Git, a terminal or Git Bash, and GitHub or GitLab

### Part 1 — Create your repository (10 minutes)

1. Create a folder named `student-task-tracker`.
2. Initialize Git in the folder.
3. Configure your Git username and email if needed.
4. Create `README.md` with the project title and a short description.
5. Check the repository status.

**Checkpoint:** You have a local Git repository and can see its status.

### Part 2 — Stage and commit changes (15 minutes)

1. Create `tasks.txt` with at least three sample tasks.
2. Run `git status` before staging.
3. Stage `README.md` and `tasks.txt`.
4. Commit them with a meaningful commit message.
5. Add a fourth task, then inspect the status and commit history.

**Checkpoint:** You have made at least two meaningful commits and can explain what `git status` and `git log` show.

### Part 3 — Use `.gitignore` (10 minutes)

1. Create a `.gitignore` file.
2. Add these rules:

   ```gitignore
   *.log
   .env
   ```

3. Create `app.log` and a sample `.env` file containing dummy data only.
4. Check which files Git shows as untracked.
5. Stage and commit `.gitignore`, but do not commit the ignored files.

**Checkpoint:** Git ignores `app.log` and `.env`, while `.gitignore` itself is tracked.

**Important:** Never put real passwords, tokens, or other secrets in a practice `.env` file. `.gitignore` does not automatically untrack a file that was committed previously.

### Part 4 — Publish and synchronize (15 minutes)

1. Create an empty remote repository on GitHub or GitLab.
2. Connect your local repository to the remote.
3. Push your `main` branch.
4. Clone the remote repository into a second folder.
5. In the cloned copy, make a small change to `README.md`.
6. Commit the change and push it to the remote.

**Checkpoint:** Your remote repository contains your commits, and the README change made in the cloned copy is pushed successfully.

### Part 5 — Fetch, pull, and PR/MR workflow (20 minutes)

1. Return to your original local repository.
2. Fetch the remote changes and inspect the remote-tracking branches or commit history.
3. Pull the remote changes and verify that the README update is present.
4. Create a feature branch named `feature/add-priority`.
5. Add a priority section to `tasks.txt`, assigning a priority to each task.
6. Commit the change with a meaningful message.
7. Push the feature branch.
8. On GitHub or GitLab, open a Pull Request or Merge Request targeting `main`.

**Checkpoint:** The feature branch is published, and a PR/MR is open with the intended changes.

**Discussion checkpoint:** Explain the difference between `git fetch` and `git pull`. Fetch downloads remote updates without integrating them into your current branch; pull fetches and integrates changes.

### Part 6 — Review and final verification (10 minutes)

1. Review the PR/MR diff and write a short description of the change.
2. Check that the change is limited to the intended files.
3. Ask a partner or instructor to review it, then merge it if permitted.
4. Verify the final commit history and repository status.

**Checkpoint:** You can show your repository, explain your commits, confirm ignored files are not tracked, and demonstrate the PR/MR workflow.

## Expected final repository structure

Your repository should contain files similar to these:

```text
student-task-tracker/
├── .git/
├── .gitignore
├── README.md
└── tasks.txt
```

The `.git/` folder is created automatically by Git and should not be manually edited. The `.env` and `app.log` files may exist locally, but they should not be tracked or appear in the PR/MR changes.

Your Git history should contain several meaningful commits, such as:

- `Add project documentation and task list`
- `Update task list`
- `Add rules for ignored files`
- `Update project README`
- `Add task priorities`

The order may differ depending on how you complete the exercise.

## Completion checklist

- [ ] Initialized a local Git repository.
- [ ] Created `README.md` and `tasks.txt`.
- [ ] Used `git status`, `git add`, `git commit`, and `git log`.
- [ ] Made multiple meaningful commits.
- [ ] Created and tested `.gitignore`.
- [ ] Connected the local repository to a remote.
- [ ] Pushed changes to the remote.
- [ ] Cloned the repository into a second folder.
- [ ] Used `git fetch` and `git pull`.
- [ ] Created and pushed `feature/add-priority`.
- [ ] Opened a PR/MR targeting `main`.
- [ ] Reviewed the changes and checked the final repository status.

## Resolve a merge conflict


1. Edit the same line of `README.md` differently in two branches or working copies.
2. Commit and push one change to `main`.
3. Try to integrate the other change.
4. Resolve the conflict manually.
5. Stage the resolved file and complete the merge.
6. Verify the final file and commit history.


