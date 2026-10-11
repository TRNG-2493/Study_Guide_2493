# Starter code: Account Profile and Password Reset (build 0.5.0)

A small Python program that stands in for the Project 1 "Account Profile and Password Reset" feature, so you can run your test cases from a console. It needs Python 3.8 or newer and nothing else (no installs).

## Set up (2 minutes)

1. Copy this folder to your computer.
2. Open a terminal in the folder and run `python try_it.py help` (use `python3` if `python` is not found).
3. Run `python try_it.py reset-state` before each test case that needs a clean start.

## How it works

- Each run is one command. The program remembers the result in a small file (`.try_it_state.json`), so the next command continues where the last one stopped (for example, `login` and then `profile`).
- Every response is printed as `OK: ...` or `ERROR: ...` followed by the message the user would see. Copy that exact line into your execution log as evidence.
- There are two seed accounts, both with password `Pass@1234`: `anna@example.com` (name "Anna Lee") and `ben@example.com` (name "Ben Carter"). You can create more with `register`.
- Email is simulated. The page never shows the reset link; read what was "sent" with the `mailbox` command.
- Time is simulated. `advance-clock 10` moves the clock forward 10 minutes without waiting.

## Commands

| Command | What it does |
|---|---|
| `python try_it.py reset-state` | Start again with the two seed accounts, nobody logged in, empty mailbox, clock at zero |
| `python try_it.py register EMAIL NAME PASSWORD` | Create an account |
| `python try_it.py login EMAIL PASSWORD` | Log in |
| `python try_it.py logout` | Log out |
| `python try_it.py profile` | Show the logged-in user's name and email |
| `python try_it.py set-name "NEW NAME"` | Change the display name |
| `python try_it.py set-email NEW_EMAIL` | Change the email address |
| `python try_it.py reset-request EMAIL` | Ask for a password-reset link |
| `python try_it.py mailbox EMAIL` | Read the simulated emails sent to that address (shows the token) |
| `python try_it.py reset-complete TOKEN NEW CONFIRM` | Set a new password with a token, typing the new password and its confirmation |
| `python try_it.py advance-clock MINUTES` | Move the simulated clock forward |

Example session:

```
python try_it.py reset-state
python try_it.py login anna@example.com Pass@1234
python try_it.py profile
```

## Builds

- **0.5.0** is the QA build. This is the build you test in Part 3. It is the default.
- **0.5.1** is the developer's fix drop. Use it only in Part 4, for the retest of the bug you moved through the workflow: add `--build 0.5.1` before the command, for example `python try_it.py --build 0.5.1 profile`.

## Notes

- The program is deliberately small. Anything the requirements do not describe is not built.
- Do not read `account_service.py` before you finish Part 3. A real tester tests from the requirements, not from the source code, and reading it would also spoil the exercise.
