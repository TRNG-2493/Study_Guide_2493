# Pair Programming Log

Pair: ______________________ (A)   and   ______________________ (B)
Shared repository / branch: ______________________________________

## Pair agreement (agree BEFORE slot 1 - 5 minutes)

- Roles: the **Driver** is the only one typing; the **Navigator** reviews every line, thinks ahead and keeps the checklist.
- Swap every 30 minutes, exactly at the slot boundary (set a timer). Commit before every swap.
- We talk out loud. The Navigator asks "why?" instead of grabbing the keyboard.
- If we disagree for more than 3 minutes we write both options in THREE_AMIGOS.md and ask the instructor.
- Our working rules (add one of your own): ______________________________________________

## Swap log (fill in at every swap)

| Slot | Time | Driver | Navigator | Task | Commit (author = driver) | What the navigator caught |
|---|---|---|---|---|---|---|
| 1 | 0:00-0:30 | A | B | Setup, story cards | | |
| 2 | 0:30-1:00 | B | A | Acceptance criteria and example mapping | | |
| 3 | 1:00-1:30 | A | B | login.feature + login steps | | |
| 4 | 1:30-2:00 | B | A | sort.feature + SortSteps | | |
| 5 | 2:00-2:30 | A | B | cart.feature + CartSteps + CommonSteps | | |
| 6 | 2:30-3:00 | B | A | Integrate, FeatureStyleTest green, README, retrospective | | |

> Git rule: each slot ends with a commit made **by the driver of that slot** (`git config user.name` on that machine,
> or `git commit --author`). The history must show the two authors alternating.
