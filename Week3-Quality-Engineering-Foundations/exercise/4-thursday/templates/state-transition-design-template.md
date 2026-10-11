# State Transition Design: Account Lifecycle (ACC-01..ACC-08)

Pair: ______________

## 1. State diagram
Paste your finished diagram here (start from state-diagram-template.mermaid).

```mermaid
(your diagram)
```

## 2. State table (every state x every event)
Cell content: next state, or "refused" (and the code). Guards in brackets.

| State \ Event | verify | suspend(reason) | reactivate | close |
|---|---|---|---|---|
| Pending | | | | |
| Active | | | | |
| Suspended | | | | |
| Closed | | | | |

Counts: valid transitions = ____ ; invalid (state, event) pairs = ____ ; guards = ____

## 3. Test plan
| Test ID | Kind (valid / invalid / guard / sequence) | Start state | Event (and data) | Expected result | Expected end state | Req ID |
|---|---|---|---|---|---|---|
| ST-VAL-01 | | | | | | |

## 4. Coverage statement
- All-states covered?  - All valid transitions covered?  - Invalid transitions covered (list)?  - Guards covered (both outcomes)?
