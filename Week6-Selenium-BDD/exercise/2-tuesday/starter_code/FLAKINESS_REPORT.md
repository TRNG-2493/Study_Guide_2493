# Flakiness Report - Tuesday (fill in during Part 1)

Run command (use your own numbers for `times`):

    mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.FlakinessRun -Dtimes=5 -Dheadless=true

## Pass rates

| Scenario | Baseline (before fixes) | After fixes (target 10/10) |
|---|---|---|
| S1 dynamic loading (hidden element) | /5 | /10 |
| S2 dynamic loading (element added later) | /5 | /10 |
| S3 dynamic controls (remove + enable) | /5 | /10 |
| S4 SauceDemo bad-login error | /5 | /10 |
| S5 Monday LoginSearchFlow (after Task 2.1) | /5 | /10 |
| S6 SortFlow (after Task 2.3) | /5 | /10 |

## Root-cause diagnosis (one row per failure you observed)

| Scenario | Exception or wrong value you saw | Root cause (one sentence) | Wait you chose and why |
|---|---|---|---|
| S1 | | | |
| S2 | | | |
| S3a | | | |
| S3b | | | |
| S4 | | | |

## Decision questions

1. Why can `getText()` return an empty string with **no exception** in S1, and why is that more dangerous than an exception?
2. Why did you pass a `By` into `WaitUtils` instead of a `WebElement`?
3. Why must an implicit wait never be combined with explicit waits?
4. Where (if anywhere) did you need a custom or fluent condition, and what was it?
