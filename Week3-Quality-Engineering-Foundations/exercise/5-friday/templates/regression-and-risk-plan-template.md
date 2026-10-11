# Project 1 Regression and Risk Plan v1.0 (Release 1.1)

Author: <name> | Date: <date> | Linked document: `project1-test-design-document.md`

## 1. Scope and goal
Change request (copy it here):
- (a)
- (b)
- (c)

## 2. Risk register
Scale: L (likelihood) 1 to 5, I (impact) 1 to 5, Score = L x I. Say how you chose the numbers in one sentence.

| ID | Risk (if X then Y) | Related change | L | I | Score | Mitigation | Owner (role) |
|---|---|---|---|---|---|---|---|
| R-01 | | | | | | | |
| R-02 | | | | | | | |
| R-03 | | | | | | | |
| R-04 | | | | | | | |
| R-05 | | | | | | | |
| R-06 | | | | | | | |
| R-07 | | | | | | | |
| R-08 | | | | | | | |

## 3. Impact analysis
| ID | Change | Item touched | Touched how (direct / calls shared code / indirect) | Why it matters | Linked tests or charters |
|---|---|---|---|---|---|
| IA-1 | (a) | | | | |
| IA-2 | (a) | | | | |
| IA-3 | (b) | | | | |
| IA-4 | (b) | | | | |
| IA-5 | (c) | | | | |
| IA-6 | (c) | | | | |
| IA-7 | none | Not connected (state one area you rule out) | | | |

## 4. Selection rule
State the rule in 2 or 3 lines (for example: risk-based using L x I, plus history-based for earlier defects, plus impact analysis).
Tier thresholds used: smoke = score >= __, core = __ to __, full = below __.

## 5. Selected tests and tiers
| Test ID | Test (short) | Req | Change (a/b/c/none) | Risk score | Tier | Justification | Automated? |
|---|---|---|---|---|---|---|---|

## 6. Suites, triggers and time estimate
| Tier | Purpose | pytest command (if used) | Trigger | Tests | Est. minutes | Assumption behind the estimate |
|---|---|---|---|---|---|---|
| Smoke | | | | | | |
| Core | | | | | | |
| Full | | | | | | |

## 7. Automation candidates
| Test or area | Automate? | Reason |
|---|---|---|
| | | |

Kept manual or exploratory (with reason):

## 8. Entry and exit criteria
Entry criteria:
- [ ]

Exit criteria:
- [ ]

## 9. Release 1.1 go/no-go checklist
| # | Check | Threshold | Result | Go / No-go |
|---|---|---|---|---|
| 1 | Smoke tier passes | 100 percent | | |
| 2 | Core tier passes | | | |
| 3 | Open critical or high defects | | | |
| 4 | All three changes have at least one test run | | | |
| 5 | Exploratory sessions done | | | |
| 6 | Performance target for login | | | |
| 7 | Known risks accepted by (role) | | | |

Decision and signatures (roles):

## 10. Maintenance
Who updates the suite after the release, and when.
