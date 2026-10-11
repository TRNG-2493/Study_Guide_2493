# White-Box Testing: Testing from the Inside Out

## Learning Objectives

By the end of this lesson, you will be able to:

1. Define white-box (structure-based, glass-box, clear-box) testing and explain how it differs from black-box and grey-box testing.
2. Identify who performs white-box testing, at which test levels, and in which activities (unit tests, code reviews, static analysis).
3. Describe what "structure" means in code: statements, branches (decisions), conditions, paths, and loops.
4. Draw a control flow graph (CFG) from a small Python function using nodes and edges.
5. Calculate statement, branch, and condition coverage using formulas, and explain condition/decision and multiple condition coverage.
6. Calculate cyclomatic complexity using both V(G) = E - N + 2P and "decision points + 1".
7. Design loop tests (zero, one, many, maximum iterations) and explain the subsumption relationship between coverage criteria, including a counter-example.
8. Choose a minimum set of test cases to reach a given coverage target for a real Python function.
9. Run pytest with coverage.py, read a coverage report, and interpret uncovered lines and partial branches.
10. Explain why 100% coverage does not prove the software is bug-free, and why white-box and black-box techniques are used together.
11. Apply white-box thinking to the Project 1 registration logic and produce a coverage-driven test set.

---

## Why This Matters

### In the industry

Every piece of software is, at the bottom, a pile of code: `if` statements, loops, and function calls. Black-box techniques (which you learned on Thursday) test that code from the outside, using only the requirements. That is powerful, but it has a blind spot: you cannot see which parts of the code your tests never touched. A tester working only from the outside might run two hundred test cases and still never execute the error-handling code that runs when a payment gateway times out. That untested code is where many production failures hide.

White-box testing closes this gap. Development teams use it every day, usually without calling it "white-box testing":

- Developers write unit tests alongside their code, and a **continuous integration (CI)** pipeline runs those tests on every change.
- Many teams publish a **coverage report** with every build, so a reviewer can see at a glance which lines are not exercised.
- **Code reviews** and **static analysis tools** (linters) examine code without running it, catching defects before a single test executes.
- Software Development Engineers in Test (SDETs) and automation engineers read code to decide where to aim their tests, and to judge whether the existing tests are meaningful.

As an AI-enabled Test Automation Engineer, you will be expected to read a Python function and tell, within a minute or two, how many tests it needs, where the risky branches are, and what a coverage report is really saying. That skill separates someone who only runs tests from someone who designs them.

### In this week's epic

This week you have been building a quality-engineering mindset and applying it daily to **Project 1: QE Foundations**, a sample web app with User Registration and Login. On Thursday you designed black-box tests for that app using equivalence partitioning, boundary value analysis, decision tables, and state transition testing. Today you add the second lens. You will look inside a Python registration function, draw its control flow, measure coverage, and combine your white-box tests with Thursday's black-box tests. Friday's exercise asks you to complete the Project 1 test-design document and regression/risk plan; the coverage thinking from this lesson tells you which code is well tested and which code deserves extra attention in that risk plan.

---

## The Concept

### 1. What is white-box testing?

**White-box testing** is a way of designing and evaluating tests based on the **internal structure of the software**: its code, its decisions, its loops, and the paths execution can take. The tester can see inside the box.

You will meet several names for the same idea. They are all used in industry and in certification syllabi:

| Name | Where the name comes from |
|---|---|
| White-box testing | The "box" (the software) is drawn white, meaning we can see through it |
| Glass-box testing | The box is made of glass; we can see the inside |
| Clear-box testing | Same idea, different material |
| Structure-based testing | The tests are derived from the **structure** of the code |
| Structural testing | Short form of the above |
| Code-based testing | Tests designed from the code itself |

The ISTQB (International Software Testing Qualifications Board) glossary calls this family of techniques "white-box test techniques" or "structure-based test techniques". In this lesson we use "white-box testing" as the main term.

**Analogy: the mechanic and the driver.** Imagine a car. A driver tests the car from the outside: press the accelerator, turn the wheel, brake. If the car does what drivers expect, the driver is satisfied. That is black-box testing. A mechanic opens the hood. The mechanic does not just ask "does it move?" but "is every belt turning? Does the fuel pump fire? Is there a wire that is never carrying current?" That is white-box testing. The mechanic can find a worn part long before it causes a breakdown, and can notice that a part exists that the driver never exercises (a spare fuse box, say). But a mechanic who has never driven the car might miss that the steering feels wrong. You need both.

### 2. A key point: white-box testing is about how tests are chosen

White-box testing does **not** mean "the tester sees the code and then checks that it works". It means the **test cases are chosen based on structure** and **adequacy is measured against structure**. For example, "write enough tests so that every `if` statement has been taken both ways" is a white-box goal. The expected result of each test still comes from the **requirements** (the test oracle), not from reading the code. This is critical, and we will return to it in the common mistakes section: if you decide the expected result by reading what the code does, you will never detect a wrong implementation.

### 3. Black-box, white-box, and grey-box compared

You studied black-box testing on Thursday. Here is the full comparison.

| Aspect | Black-box testing | White-box testing | Grey-box testing |
|---|---|---|---|
| Knowledge of internals | None required | Full knowledge of code | Partial (for example the database schema, API contract, or architecture, but not every line) |
| Test basis | Requirements, specifications, use cases | Source code, design, control flow | Requirements plus some internal knowledge |
| Typical techniques | Equivalence partitioning, BVA, decision tables, state transition, error guessing | Statement, branch, condition, path coverage; loop testing; data-flow testing | Testing an API while checking the database afterwards; using knowledge of architecture to focus tests |
| Typical performers | Testers, business analysts, end users, QA engineers | Developers, SDETs | SDETs, API testers, security testers |
| Typical levels | System, acceptance (also integration, component) | Unit, component, integration | Integration, API, system |
| Finds | Missing features, wrong behaviour against requirements, usability issues | Dead code, untested branches, logic errors, hidden paths | Integration issues, data-handling problems |
| Cannot find | Code that is never exercised; defects in untouched structure | Missing requirements (code that was never written) | Depends on what is known |
| Programming skill needed | Low to moderate | High | Moderate |
| Coverage measured as | Requirement or test-condition coverage | Code coverage (statement, branch, etc.) | Mixed |

**Grey-box testing** is the in-between approach. The tester does not read all the code, but knows something about the internals. A simple example: you test the registration API by sending a request (black-box style), then you query the database to confirm that the password was stored **hashed** and not as plain text (an internal detail you only know because you know the design). Grey-box testing is common in API testing and security testing.

> Remember the distinction in one line: **Black-box asks "does it do what it should?" White-box asks "have we exercised what was actually built?"**

### 4. Who does white-box testing, and when?

**Who:**

- **Developers** write unit tests for their own code and review each other's code. This is the most common form of white-box testing in the real world.
- **SDETs (Software Development Engineers in Test)** and **test automation engineers** read code, write unit and integration tests, review coverage reports, and may add tests for gaps they find.
- **Security specialists** review code for vulnerabilities (conceptually; we return to this later).
- **QA engineers** with programming skills use white-box thinking when they review what developers' tests actually cover.

**When (test levels):** you learned in the V-model that testing levels mirror development levels. White-box techniques are used most heavily at the lower levels:

| Level | What is tested | White-box role |
|---|---|---|
| Unit / component | One function, class, or module in isolation | Primary level. Statement, branch, and condition coverage are all measured here |
| Integration | How modules or services work together | Structure at the interface level: which calls are made, which code paths in the interaction run |
| System | The whole application | Mostly black-box, but coverage can still be measured to see what the system tests missed |
| Acceptance | Fitness for the user's needs | Black-box |

White-box activities also occur **outside test execution**: code reviews and static analysis happen before any test runs. These are covered later in this lesson.

### 5. What does "structure" mean?

To talk about white-box testing, we need a precise vocabulary for the parts of code. Look at this small function:

```python
def check_login_attempt(failed_attempts, password_ok):
    if failed_attempts >= 3 and not password_ok:   # a decision made of two conditions
        return "locked"
    return "ok"
```

| Term | Definition | Example in the function above |
|---|---|---|
| **Statement** | One executable instruction | `return "locked"` and `return "ok"` are two statements. (The `if` line is also counted by tools as a statement.) |
| **Decision** (also **branch point**) | A point where execution can go two (or more) ways, controlled by a Boolean expression | The whole `if failed_attempts >= 3 and not password_ok` |
| **Branch** (also **decision outcome**) | One outgoing direction of a decision: the True outcome or the False outcome | "the if is taken" and "the if is not taken" |
| **Condition** | An **atomic** Boolean expression with no `and`/`or`/`not` operators splitting it further | `failed_attempts >= 3` and `password_ok` (the `not` just flips it) |
| **Path** | One complete route from the start of the function to the end | Path 1: decision True, return "locked". Path 2: decision False, return "ok" |
| **Loop** | A `for` or `while` that repeats statements | Not in this function |

Notice the difference between a **decision** and a **condition**. A decision is the entire Boolean expression that steers the flow. A condition is one of the small true/false pieces inside it. In the function above there is one decision made of two conditions joined by `and`.

### 6. Control flow graphs, step by step

A **control flow graph (CFG)** is a diagram that shows every route that execution can take through a piece of code. It is the white-box tester's map. CFGs are the foundation for coverage criteria and for cyclomatic complexity.

A CFG has two kinds of parts:

- **Nodes** (circles, or numbered boxes): each node is a statement or a block of statements that always run together in sequence, or a decision point.
- **Edges** (arrows): each edge shows that execution can move from one node to the next.

**How to draw a CFG: the recipe**

1. Number each statement, or group of consecutive straight-line statements, as a node.
2. Give every decision (`if`, `elif`, `while`, `for`) its own node. That node will have **two** outgoing edges: True and False.
3. Draw an arrow from each node to whatever can run next.
4. Make sure the branches of an `if` rejoin at the next statement after the `if`.
5. For loops, draw an edge from the end of the loop body **back** to the loop's decision node.
6. Add one **exit** node (we will call it "End") that every `return` leads to. A `raise` that is not caught also leads to the exit.

#### Example A: a single `if`

```python
def apply_bonus(score, is_vip):
    if is_vip:
        score = score + 10
    return score
```

Step 1: Node 1 is the decision `if is_vip`. Node 2 is `score = score + 10`. Node 3 is `return score`.
Step 2: From node 1, True goes to node 2; False skips to node 3. From node 2, execution continues to node 3.

```
        +-------------+
        | 1: if       |
        |    is_vip   |
        +------+------+
          True |  \  False
               v   \
        +-----------+ \
        | 2: score  |  \
        |  = score  |   \
        |    + 10   |    \
        +-----+-----+     \
              |            |
              v            v
        +---------------------+
        | 3: return score     |
        +----------+----------+
                   |
                   v
                 (End)
```

Edges: 1->2, 1->3, 2->3. That is **3 edges**, **3 nodes** (we count the exit separately later, or not at all, as long as we are consistent).

#### Example B: `if / elif / else`

```python
def grade(score):
    if score >= 90:
        g = "A"
    elif score >= 50:
        g = "Pass"
    else:
        g = "Fail"
    return g
```

Nodes: 1 = `if score >= 90`; 2 = `g = "A"`; 3 = `elif score >= 50`; 4 = `g = "Pass"`; 5 = `g = "Fail"`; 6 = `return g`.

```
                [1: score >= 90 ?]
                  T /        \ F
                   v          v
              [2: g="A"]   [3: score >= 50 ?]
                   |         T /       \ F
                   |          v         v
                   |   [4: g="Pass"] [5: g="Fail"]
                   |          |         |
                   +----+-----+---------+
                        v
                  [6: return g]
                        |
                        v
                      (End)
```

Edges: 1->2, 1->3, 3->4, 3->5, 2->6, 4->6, 5->6. That is **7 edges** and **6 nodes**.

There are three distinct paths: 1-2-6, 1-3-4-6, and 1-3-5-6.

#### Example C: a loop

```python
def sum_positive(numbers):
    total = 0
    for n in numbers:
        if n > 0:
            total += n
    return total
```

Nodes: 1 = `total = 0`; 2 = `for n in numbers` (loop decision: is there another item?); 3 = `if n > 0`; 4 = `total += n`; 5 = `return total`.

```
            [1: total = 0]
                  |
                  v
        +--->[2: more items?]-----F----> [5: return total] --> (End)
        |         | T
        |         v
        |    [3: n > 0 ?]
        |      F /     \ T
        |       /       v
        |      /   [4: total += n]
        |     /         |
        +----+----------+
   (both the False edge of 3 and the end of 4 go back to 2)
```

Edges: 1->2, 2->3 (True), 2->5 (False), 3->4 (True), 3->2 (False), 4->2. That is **6 edges** and **5 nodes**.

The loop shows why the number of paths can grow without limit: you can go around zero times, once, twice, a hundred times. We will return to that when we discuss path coverage and loop testing.

### 7. Statement coverage

**Coverage** is a measure of how much of the code structure your tests have exercised. It is expressed as a percentage.

**Statement coverage** (also called line coverage) asks: *has every executable statement run at least once?*

Formula:

```
Statement coverage (%) = (number of statements executed by the tests
                          / total number of executable statements) x 100
```

**Worked example.** Use `apply_bonus` from earlier. Its executable statements are the `if`, the `score = score + 10`, and the `return`. (A `def` line is also counted by coverage.py as a statement executed when the module is imported, which is why the real tool report later shows 4 statements.) For our hand calculation, count 3 statements.

- Test 1: `apply_bonus(50, True)` runs the `if`, the addition, and the `return`. That is 3 of 3.

Statement coverage = 3 / 3 x 100 = **100%** with a single test.

Now suppose the function also had an extra statement `log("bonus applied")` that is only reached from another branch, and your tests miss it. With 5 statements and 4 executed, coverage = 4 / 5 = **80%**.

**What statement coverage tells you:** every line was run at least once. **What it does not tell you:** whether every *decision outcome* was tried. We will see a famous example in a moment.

### 8. Branch (decision) coverage

**Branch coverage** (also called **decision coverage**) asks: *has every decision been taken both ways, True and False, at least once?* In terms of the CFG, it asks whether every **edge leaving a decision node** has been traversed.

Formula:

```
Branch coverage (%) = (number of decision outcomes exercised
                       / total number of decision outcomes) x 100
```

Each `if` contributes 2 outcomes. An `if / elif / else` chain with two decisions has 4 outcomes.

**Worked example: `grade`.**

Total outcomes: decision 1 (True, False) + decision 3 (True, False) = **4 outcomes**.

| Test | Input | Outcomes exercised |
|---|---|---|
| T1 | `grade(95)` | Decision 1 True |
| T2 | `grade(70)` | Decision 1 False, Decision 3 True |
| T3 | `grade(10)` | Decision 1 False, Decision 3 False |

- After T1 only: 1 of 4 = **25%**.
- After T1 and T2: 3 of 4 = **75%**.
- After T1, T2, and T3: 4 of 4 = **100%**.

So you need **three** tests for 100% branch coverage of `grade`. For statement coverage you also need all three, because each of the three assignments sits on a different branch.

### 9. The subsumption relationship, with a counter-example

One criterion **subsumes** another if achieving 100% of the stronger one guarantees 100% of the weaker one.

> **100% branch coverage implies 100% statement coverage.** The reverse is **not** true.

**Why branch implies statement:** if every decision outcome has been taken, then every statement that sits on any outcome has been executed (every statement is reachable only through some edge). Statements outside any decision run whenever the function runs at all.

**Counter-example for the reverse.** Go back to:

```python
def apply_bonus(score, is_vip):
    if is_vip:
        score = score + 10
    return score
```

A single test `apply_bonus(50, True)` runs every statement: 100% statement coverage. But the False outcome of `if is_vip` has **never** been taken. Branch coverage is only 1 of 2 = 50%. And it matters: if a developer had accidentally written the function so that non-VIP scores were also changed, this lone test would never reveal it.

Here is the real coverage tool showing exactly this (details of the tool later in this lesson):

```
$ python3 -m pytest --cov=bonus --cov-report=term-missing -q
Name       Stmts   Miss  Cover   Missing
----------------------------------------
bonus.py       4      0   100%
----------------------------------------
TOTAL          4      0   100%
1 passed in 0.02s

$ python3 -m pytest --cov=bonus --cov-branch --cov-report=term-missing -q
Name       Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------
bonus.py       4      0      2      1    83%   2->4
------------------------------------------------------
TOTAL          4      0      2      1    83%
1 passed in 0.02s
```

Without `--cov-branch`, the report says 100%. With `--cov-branch`, the same test shows a **partial branch** (`BrPart` = 1) and the line `2->4`, meaning "from line 2 (the `if`) execution never went to line 4 (the `return`) without entering the body". Adding `apply_bonus(50, False)` raises branch coverage to 100%.

This is the single most important reason to **always turn on branch measurement**.

### 10. Condition coverage

Branch coverage treats a decision as a single True/False question. But decisions are often made of several conditions:

```python
if amount >= 100 and is_member:
```

**Condition coverage** asks: *has every atomic condition been True at least once and False at least once?*

Formula:

```
Condition coverage (%) = (number of condition outcomes exercised
                          / (2 x number of conditions)) x 100
```

For `amount >= 100 and is_member`, there are 2 conditions, so 4 condition outcomes: `amount >= 100` True, `amount >= 100` False, `is_member` True, `is_member` False.

Tests (ignoring short-circuiting for the moment, as in the classic textbook model):

| Test | amount >= 100 | is_member | Whole decision |
|---|---|---|---|
| (150, False) | True | False | False |
| (50, True) | False | True | False |

Both conditions have now been True and False: **100% condition coverage**. But look at the last column: the whole decision was **False both times**. The True outcome of the decision never happened, so **branch coverage is only 50%**. This shows that condition coverage does **not** imply branch coverage.

### 11. Condition/decision coverage

Because condition coverage alone can miss decision outcomes, a combined criterion exists.

**Condition/decision coverage** requires **both**: every condition takes True and False, **and** every decision takes True and False.

For the example above, add one test where both are True:

| Test | amount >= 100 | is_member | Decision |
|---|---|---|---|
| (150, False) | T | F | F |
| (50, True) | F | T | F |
| (150, True) | T | T | T |

Now conditions are all covered and the decision has been both True and False. Three tests give condition/decision coverage here. (Two would also work: (150, True) gives T/T and True, and (50, False) gives F/F and False.)

**A Python subtlety: short-circuit evaluation.** Python evaluates `A and B` left to right and stops as soon as the answer is known. If `A` is False, `B` is never evaluated at all. So in the test (50, True) above, the condition `is_member` is not even looked at, because `amount >= 100` was already False. A tool that really measured condition coverage would record that `is_member = True` was **not observed** in that test. This is why, in practice, you design tests with the short-circuit rules in mind: to see `B` evaluated, `A` must be True (for `and`) or False (for `or`).

> **Important:** coverage.py measures statements and branches. It does **not** measure condition coverage. Condition-level thinking is done by the tester, by hand, when designing tests for compound decisions.

### 12. Multiple condition coverage (introduced gently)

**Multiple condition coverage** (also called **combinatorial condition coverage**) is the most thorough of these criteria: it requires **every possible combination** of True/False for the conditions in a decision.

For a decision with *n* conditions, there are 2^n combinations:

| Conditions in the decision | Combinations needed |
|---|---|
| 1 | 2 |
| 2 | 4 |
| 3 | 8 |
| 4 | 16 |
| 5 | 32 |

For `amount >= 100 and is_member` the four combinations are TT, TF, FT, FF. This is very manageable. For a decision with six conditions, you would need 64 combinations, which is rarely practical.

Because of that growth, practitioners sometimes use a middle ground called **modified condition/decision coverage (MC/DC)**, which requires that each condition be shown to independently affect the decision's outcome. MC/DC is known mainly from safety-critical software such as avionics. We mention it by name only; you will not be asked to compute it in this course.

### 13. Path coverage and cyclomatic complexity

**Path coverage** asks: *has every possible path from start to end been executed?* A **path** is a complete route through the CFG.

Formula (conceptual):

```
Path coverage (%) = (number of distinct paths executed / total number of paths) x 100
```

Path coverage is the strongest of the criteria we have seen, but it has a problem: the number of paths grows quickly. Every independent `if` roughly doubles the number of paths, and a loop can create an unlimited number of paths. For this reason, 100% path coverage is realistic only for small functions.

#### Counting paths in a small function

Take `grade`: 3 paths (shown earlier). Take `apply_bonus`: 2 paths. Now take this function with two independent `if` statements in sequence:

```python
def price(amount, is_member, has_coupon):
    discount = 0
    if is_member:
        discount += 5
    if has_coupon:
        discount += 5
    return amount - amount * discount / 100
```

Each `if` can go two ways, independently: 2 x 2 = **4 paths** (TT, TF, FT, FF). Add a third independent `if` and it becomes 8; a tenth makes it 1,024 paths.

#### Cyclomatic complexity

**Cyclomatic complexity** is a number that measures how complex the control flow of a function is. It was proposed by Thomas McCabe. It also gives us the number of **linearly independent paths** through the code, which is the minimum number of tests needed to touch every edge of the graph in a systematic way (the "basis set").

There are two formulas that give the same answer for a normal single-entry, single-exit function:

**Formula 1 (from the graph):**

```
V(G) = E - N + 2P
```

- **E** = number of edges
- **N** = number of nodes
- **P** = number of connected components (for one function, P = 1)

**Formula 2 (shortcut):**

```
V(G) = number of decision points + 1
```

Count each `if`, `elif`, `while`, `for` as one decision point. (Some tools also count each `and`/`or` as an extra decision point; the classical count uses decision nodes in the graph, and tools differ. State which convention you used.)

**Worked examples**

| Function | Nodes (N) | Edges (E) | V(G) = E - N + 2 | Decision points | Decisions + 1 |
|---|---|---|---|---|---|
| `apply_bonus` | 3 | 3 | 3 - 3 + 2 = **2** | 1 | **2** |
| `grade` | 6 | 7 | 7 - 6 + 2 = **3** | 2 | **3** |
| `sum_positive` | 5 | 6 | 6 - 5 + 2 = **3** | 2 (the `for` and the `if`) | **3** |

Both formulas agree. For `grade`, V(G) = 3, and indeed there are three independent paths (1-2-6, 1-3-4-6, 1-3-5-6). That tells us at least **3 tests** are needed to exercise each independent path.

**What do the numbers mean?** A commonly quoted rule of thumb is that lower is better: small values mean simple, easy-to-test functions, and large values suggest the function is hard to understand and test and may be a candidate for splitting into smaller functions. Exact thresholds vary between organisations, so treat any specific limit as a team convention, not a law. The useful lesson is: **cyclomatic complexity tells you the minimum number of test cases for branch-level thoroughness and how risky a function is to change.**

#### The cyclomatic complexity of a larger function

Now the function we will use for the main worked example:

```python
def calculate_discount(amount, is_member, coupon):
    """Return the discount percentage for an order."""
    if amount <= 0:                       # decision 1
        raise ValueError("amount must be positive")
    discount = 0
    if amount >= 100 and is_member:       # decision 2 (two conditions)
        discount = 15
    elif amount >= 100:                   # decision 3
        discount = 10
    elif is_member:                       # decision 4
        discount = 5
    if coupon == "SAVE5":                 # decision 5
        discount = discount + 5
    return discount
```

Its business rules: orders must be positive; members spending 100 or more get 15%; non-members spending 100 or more get 10%; members spending under 100 get 5%; everyone else gets 0%; the coupon `SAVE5` adds 5 more percentage points.

Its CFG, with nodes:

- N1: `if amount <= 0`
- N2: `raise ValueError`
- N3: `discount = 0`
- N4: `if amount >= 100 and is_member`
- N5: `discount = 15`
- N6: `elif amount >= 100`
- N7: `discount = 10`
- N8: `elif is_member`
- N9: `discount = 5`
- N10: `if coupon == "SAVE5"`
- N11: `discount = discount + 5`
- N12: `return discount`
- N13: End

```
[1: amount <= 0 ?] --T--> [2: raise] ---------------------------+
        | F                                                      |
        v                                                        |
[3: discount = 0]                                                |
        |                                                        |
        v                                                        |
[4: amount>=100 and is_member ?] --T--> [5: discount = 15] --+   |
        | F                                                  |   |
        v                                                    |   |
[6: amount >= 100 ?] --T--> [7: discount = 10] --------------+   |
        | F                                                  |   |
        v                                                    |   |
[8: is_member ?] --T--> [9: discount = 5] -------------------+   |
        | F                                                  |   |
        +--------------------+-------------------------------+   |
                             v                                   |
                 [10: coupon == "SAVE5" ?] --T--> [11: += 5]     |
                             | F                       |         |
                             v                         |         |
                      [12: return discount] <----------+         |
                             |                                   |
                             v                                   |
                          [13: End] <----------------------------+
```

Edges (17 in total): 1->2, 1->3, 3->4, 4->5, 4->6, 6->7, 6->8, 8->9, 8->10, 5->10, 7->10, 9->10, 10->11, 10->12, 11->12, 2->13, 12->13.

- N = 13, E = 17, P = 1.
- V(G) = 17 - 13 + 2 = **6**.
- Decision points: decisions 1, 2, 3, 4, 5, giving 5 + 1 = **6**. Both methods agree.
- If your tool counts each `and` as an extra decision (the `and` in decision 2), it will report **7**. Both are valid conventions as long as you say which one you use.

**Number of paths (for interest):** the discount ladder (decisions 2, 3, 4) produces four outcomes (15, 10, 5, 0), multiplied by the two coupon outcomes gives 8 paths that return a value, plus 1 path that raises an error: **9 paths** in all. Notice that V(G) = 6 is the number of *independent* paths, which is fewer than all 9 *possible* paths.

### 14. Loop testing

Loops are a classic place for defects: off-by-one errors, loops that never run, and loops that never stop. **Loop testing** is a white-box technique that focuses on the loop itself. For a simple loop that can run up to *n* times, design tests for these cases:

| Case | Why it matters |
|---|---|
| **Zero iterations** (skip the loop entirely) | Checks that the code behaves correctly with empty input or when the loop condition is False immediately |
| **One iteration** | The smallest real pass through the body; catches setup and initial-value errors |
| **Many (typical) iterations** (for example 2 or a handful) | Checks that state carries correctly between iterations |
| **Maximum iterations (n)** | The loop runs the full allowed number of times; catches limit problems |
| **One less than maximum (n - 1)** and **one more than maximum (n + 1)**, where applicable | Boundary-style tests on the loop limit (off-by-one) |

Example from the login area of Project 1:

```python
def count_failed_logins(attempts, max_attempts=3):
    """Loop example: stop counting at max_attempts."""
    failures = 0
    for ok in attempts:
        if not ok:
            failures += 1
            if failures == max_attempts:
                break
    return failures
```

| Loop case | Input (`attempts`) | Expected result (from the requirement) |
|---|---|---|
| Zero iterations | `[]` | 0 |
| One iteration, success | `[True]` | 0 |
| One iteration, failure | `[False]` | 1 |
| Many iterations | `[False, True, False]` | 2 |
| Reaches the maximum (the `break`) | `[False, False, False]` | 3 |
| Beyond the maximum | `[False, False, False, False, False]` | 3 (counting stops) |

The "beyond the maximum" test is the one that proves the `break` actually works.

**Nested loops** (a loop inside a loop) multiply the possibilities. The usual advice is to test the innermost loop first, with the outer loops held at minimum values, then work outwards. We mention this at concept level only.

### 15. Data-flow testing (name level)

**Data-flow testing** is a white-box family of techniques that follows **variables** rather than decisions. For each variable, we look at where it is:

- **Defined**: given a value (`x = 5`).
- **Used**: read (`print(x)` or `if x > 3`).

A matching pair, a definition and a later use of the same variable, is called a **def-use pair**. Data-flow testing designs tests so that each def-use pair is exercised. It also helps spot **data-flow anomalies**, such as using a variable before it has been given a value, or defining a variable and never using it. Static analysis tools (next section) detect some of these automatically. In this course we only need the name and the idea: *follow the data, not just the decisions.*

### 16. Mutation testing (name level)

Coverage tells you which code your tests **ran**. It does not tell you whether your tests would **notice a bug**. **Mutation testing** attacks that question directly. A tool makes many small deliberate changes ("mutants") to the code, for example changing `>=` to `>`, `+` to `-`, or `True` to `False`, and then reruns your tests against each mutant:

- If a test fails, the mutant is **killed**: your tests noticed the change.
- If all tests still pass, the mutant **survived**: your tests did not notice the change, so they are weak around that code.

A high proportion of killed mutants suggests a stronger test suite. Python tools exist for this (for example `mutmut`), but we only need the idea here. It is a valuable answer to the question "100% coverage, but are my tests any good?", which we turn to shortly.

### 17. Building test cases from a function: the full worked example

This is the central skill of the lesson. We use `calculate_discount` from section 13. The goal: find the **minimum number of tests** to reach each coverage target, and see why the targets differ.

Remember the code (with line numbers as coverage.py counts them):

```
 1  def calculate_discount(amount, is_member, coupon):
 2      """Return the discount percentage for an order."""
 3      if amount <= 0:
 4          raise ValueError("amount must be positive")
 5      discount = 0
 6      if amount >= 100 and is_member:
 7          discount = 15
 8      elif amount >= 100:
 9          discount = 10
10      elif is_member:
11          discount = 5
12      if coupon == "SAVE5":
13          discount = discount + 5
14      return discount
```

**Step 1: List the statements to cover.** Executable lines: 1 (the `def`), 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

**Step 2: Minimum tests for 100% statement coverage.**

We need to reach lines 4, 7, 9, 11, and 13 (the lines that only run on specific paths).

| Test | Inputs (amount, is_member, coupon) | New lines reached |
|---|---|---|
| S1 | (0, False, "") | 3, 4 (raises ValueError) |
| S2 | (150, True, "SAVE5") | 5, 6, 7, 12, 13, 14 |
| S3 | (150, False, "") | 8, 9 |
| S4 | (50, True, "") | 10, 11 |

Can we do it with fewer than 4? Line 4 (the error) ends the function, so it needs its own test. Lines 7, 9, and 11 are on three mutually exclusive branches of the if/elif ladder, so they need three separate tests. Line 13 can ride along with any one of those (we attached it to S2). So the minimum is **4 tests**.

Check the formula: all 13 executable lines are reached, so 13 / 13 = **100% statement coverage**.

**Step 3: Minimum tests for 100% branch coverage.**

List the decision outcomes. There are 5 decisions, so **10 outcomes**:

| Decision | True outcome | False outcome |
|---|---|---|
| D1: `amount <= 0` | raise | continue |
| D2: `amount >= 100 and is_member` | discount 15 | go to D3 |
| D3: `amount >= 100` | discount 10 | go to D4 |
| D4: `is_member` | discount 5 | skip (no discount) |
| D5: `coupon == "SAVE5"` | add 5 | skip |

The four statement tests cover: S1 (D1 True), S2 (D1 False, D2 True, D5 True), S3 (D2 False, D3 True, D5 False), S4 (D3 False, D4 True). Outcomes covered: 7 of 10. **Not yet covered: D4 False** (a non-member with an order under 100). So we need one more test:

| Test | Inputs | New outcome |
|---|---|---|
| B5 | (50, False, "") | D4 False |

That makes **5 tests** for 100% branch coverage: (0, False, ""), (150, True, "SAVE5"), (150, False, ""), (50, True, ""), (50, False, "").

**Why 5 and not 4?** Because the final `elif is_member:` has no `else`. The code in the False direction contains no statement of its own, so statement coverage never forces you to take it. Branch coverage does. **This is the difference in action: the branch criterion found a path that the statement criterion allowed us to skip.**

**Step 4: Condition coverage on the compound decision D2.**

D2 has two conditions: `amount >= 100` (call it A) and `is_member` (call it B). We need A True and False, and B True and False. In Python, B is evaluated only when A is True.

- A True and B True: (150, True), part of S2.
- A True and B False: (150, False), part of S3.
- A False: (50, anything), part of S4.

So B takes both values (in tests S2 and S3) and A takes both values (in tests S2/S3 and S4). The 5 branch tests already achieve condition coverage for D2. The other conditions are `amount <= 0` (True in S1, False elsewhere), `amount >= 100` in D3 (True in S3, False in S4), `is_member` in D4 (True in S4, False in B5), and `coupon == "SAVE5"` (True in S2, False elsewhere). All covered. So condition coverage needs **5 tests** here too, but only because we chose our inputs thoughtfully: in general the sets of tests that satisfy each criterion differ.

**Step 5: Multiple condition coverage on D2.** The combinations of A and B: TT (150, True), TF (150, False), FT (50, True), FF (50, False). In Python, FT and FF both short-circuit at A, so B is not evaluated, but we still try both values of `is_member` with a small order. Our 5-test set already contains all four combinations, so we have it for free here.

**Step 6: Summarize.**

| Criterion | Minimum tests for this function | What forced the count |
|---|---|---|
| Statement coverage | **4** | Error line, plus three exclusive discount lines |
| Branch coverage | **5** | The implicit "no discount" False outcome of `elif is_member` |
| Condition coverage | **5** | Both values of every atomic condition (satisfied by the same set) |
| Multiple condition coverage (for D2) | **5** | All 4 combinations of A and B appear |
| Path coverage (all 9 paths) | **9** | Each discount tier crossed with coupon yes/no, plus the raise |
| Basis set (cyclomatic complexity) | **6** | V(G) = 6 independent paths |

**Step 7: Don't forget the expected results.** A coverage-driven test is only useful if each test has an **expected result taken from the requirement**:

| Test | Inputs | Expected result (from the business rules) |
|---|---|---|
| 1 | (0, False, "") | `ValueError` raised |
| 2 | (150, True, "SAVE5") | 20 (15 + 5) |
| 3 | (150, False, "") | 10 |
| 4 | (50, True, "") | 5 |
| 5 | (50, False, "") | 0 |

We will turn these into real pytest tests in the next section, and extend with a sixth test for the coupon on its own.

### 18. Unit testing: the primary white-box vehicle

A **unit test** is a small automated test that checks one small piece of code (a "unit", usually a function) in isolation. Unit tests are the main way white-box testing is carried out. Python's most popular test runner is **pytest**.

**Key conventions in pytest:**

- Test files are named `test_*.py` (or `*_test.py`).
- Test functions start with `test_`.
- A test checks results with a plain `assert` statement.
- To check that an error is raised, use `pytest.raises`.

**The Arrange-Act-Assert (AAA) pattern.** Good unit tests have three clear parts:

1. **Arrange**: set up the inputs and the starting state.
2. **Act**: call the function being tested, once.
3. **Assert**: check that the result matches the expected result.

```python
def test_non_member_large_order_gets_10():
    # Arrange
    amount, is_member, coupon = 150, False, ""
    # Act
    result = calculate_discount(amount, is_member, coupon)
    # Assert
    assert result == 10
```

For tiny tests you may collapse these into one or two lines, but you should still be able to point to the three parts.

**One assert idea per test.** Each test should check **one behaviour**. If a test fails, its name should tell you exactly what broke. A test that checks a dozen unrelated things fails with a confusing message, and a failure in the first assert hides the others. (Several `assert` lines are acceptable when they all check one idea, such as the fields of one returned record.)

**Test isolation.** Tests must be **independent**: each test should work no matter which order they run in, and no test should depend on data left behind by another. If test B only passes after test A has run, you have hidden coupling. Isolation also means testing the **unit** alone, not the database, the network, or the clock.

**Test doubles: stubs and mocks (name level).** When the unit calls something external (a database, an email service, a payment gateway), we replace that dependency with a stand-in so the test is fast and repeatable. These stand-ins are called **test doubles**. Two common kinds:

- A **stub** returns fixed answers ("always say the username is free").
- A **mock** also records how it was called so the test can check it ("verify the confirmation email was requested once").

Python provides `unittest.mock` for this. We only need the names today; you will use them in later weeks.

**Naming.** A good test name states the scenario and the expectation: `test_member_large_order_gets_15`, not `test1`.

#### The full coverage-driven test file for `calculate_discount`

Here is the test file that satisfies 100% branch coverage plus the extra coupon test (file `test_shop.py`):

```python
import pytest
from shop import calculate_discount


def test_member_large_order_gets_15():
    assert calculate_discount(150, True, "") == 15


def test_non_member_large_order_gets_10():
    assert calculate_discount(150, False, "") == 10


def test_member_small_order_gets_5():
    assert calculate_discount(50, True, "") == 5


def test_non_member_small_order_gets_0():
    assert calculate_discount(50, False, "") == 0


def test_coupon_adds_5():
    assert calculate_discount(50, False, "SAVE5") == 5


def test_zero_amount_raises():
    with pytest.raises(ValueError):
        calculate_discount(0, False, "")
```

### 19. Running a real coverage tool: pytest and coverage.py

**coverage.py** is the standard Python tool for measuring code coverage. The **pytest-cov** plugin connects it to pytest. Everything below was run for real in a scratch folder (Python 3.13, pytest 9.1.1, coverage 7.16.2, pytest-cov 7.1.0); your version numbers may differ slightly.

**Install** (if not already installed):

```bash
pip install pytest pytest-cov coverage
# On a system-managed Python you may need:
pip install --break-system-packages pytest pytest-cov coverage
```

**Our sample files** are `shop.py` (the `calculate_discount` function shown above) and `registration.py` (the `validate_registration` and `count_failed_logins` functions you will meet in the Project 1 section).

#### Step 1: a first, weak set of tests

Suppose we have only two tests for `calculate_discount` (a member large order and the zero-amount error) and two for `validate_registration` (a valid user and a short username). Run pytest with coverage:

```
$ python3 -m pytest --cov=shop --cov=registration -q
....
================================ tests coverage ================================
Name              Stmts   Miss  Cover
-------------------------------------
registration.py      19     10    47%
shop.py              13      5    62%
-------------------------------------
TOTAL                32     15    53%
4 passed in 0.03s
```

**How to read it:**

- **Name**: the file measured.
- **Stmts**: the number of executable statements in the file.
- **Miss**: how many of those were **never executed**.
- **Cover**: the percentage, calculated as (Stmts - Miss) / Stmts. For `shop.py`: (13 - 5) / 13 = 8 / 13 = 61.5%, shown as 62%.

All four tests **passed**, yet more than a third of the code never ran. A green test run says nothing about what was *not* tested.

#### Step 2: turn on branch coverage and show missing lines

```
$ python3 -m pytest --cov=shop --cov=registration --cov-branch --cov-report=term-missing -q
....
================================ tests coverage ================================
Name              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------
registration.py      19     10     14      3    42%   7, 9, 11, 17-23
shop.py              13      5     10      2    52%   8-11, 13
-------------------------------------------------------------
TOTAL                32     15     24      5    46%
4 passed in 0.03s
```

New columns:

- **Branch**: total number of branch outcomes (for `shop.py`, 5 decisions x 2 = 10, matching our hand count).
- **BrPart**: the number of **partial branches**: decisions where only one of the two outcomes has been seen.
- **Missing**: the exact lines (and branch arrows) that were not covered. `8-11, 13` means lines 8 to 11 and line 13 of `shop.py` never ran. Looking at the numbered listing from section 17, those are the non-member large order, the member small order, and the coupon logic.

Note on the percentage: when branch coverage is on, coverage.py computes its single number as `(executed statements + executed branches) / (total statements + total branches)`. For `shop.py`, that is 52% (the exact figure depends on which branches were taken), not simply the statement percentage.

#### Step 3: the alternative command, `coverage run`

You can also use coverage.py directly, without the pytest plugin:

```
$ python3 -m coverage run --branch -m pytest -q
....
4 passed in 0.02s

$ python3 -m coverage report -m
Name                   Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------
registration.py           19     10     14      3    42%   7, 9, 11, 17-23
shop.py                   13      5     10      2    52%   8-11, 13
test_registration.py       5      0      0      0   100%
test_shop.py               7      0      0      0   100%
------------------------------------------------------------------
TOTAL                     44     15     24      5    56%
```

Two differences: you must run the two commands (`run` then `report`), and without a `--source` setting the report also lists the **test files themselves**, which inflates the total. Using `--cov=module` or `--source=.` with exclusions keeps the number honest. The `-m` after `report` is a shorthand for "show missing lines".

#### Step 4: the HTML report

```
$ python3 -m coverage html
Wrote HTML report to htmlcov/index.html
$ ls htmlcov
class_index.html  function_index.html  index.html  registration_py.html
shop_py.html  status.json  style_cb_4667309f.css  ...
```

Open `htmlcov/index.html` in a browser. It shows a table of files you can click into, and each source file is displayed with **lines highlighted**: executed lines in one colour, missed lines in another, and partially covered branches in a third. For a beginner this is the clearest way to see exactly which lines your tests missed. You can also use `pytest --cov=shop --cov-report=html` to generate it in one step.

#### Step 5: close the gaps with more tests

After adding the full test file from section 18 and the Project 1 tests from the next section, the same command gives:

```
$ python3 -m pytest --cov=shop --cov=registration --cov-branch --cov-report=term-missing -q
...............
================================ tests coverage ================================
Name              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------
registration.py      19      0     14      0   100%
shop.py              13      0     10      0   100%
-------------------------------------------------------------
TOTAL                32      0     24      0   100%
15 passed in 0.06s
```

All statements are executed, no partial branches remain, and the Missing column is empty.

#### Interpreting a report: a checklist

1. Look at **Miss** and **Missing** first. They name the exact lines.
2. Turn on **--cov-branch** and look at **BrPart**: partial branches hide in code that "looks" covered.
3. Open the **Missing** lines and ask: *what input would make execution reach here?* That question is how you design the next test.
4. Ask: *is this code reachable at all?* If not, it is **dead code**. Delete it or explain it.
5. Ask: *is this line worth testing?* Some code (for example a defensive `raise` that "can never happen") may be intentionally excluded from measurement with a comment such as `# pragma: no cover`, but use that sparingly and with a reason.

### 20. Why 100% coverage does not mean bug-free

Coverage tells you what code was **executed**. It does **not** tell you whether the results were **checked**, nor whether the code **does what the requirement says**.

**Example 1: tests with no assertions.** Here is a test file that exercises every line and every branch of `calculate_discount`, and yet checks **nothing**:

```python
from shop import calculate_discount

def test_everything_runs():
    calculate_discount(150, True, "SAVE5")
    calculate_discount(150, False, "")
    calculate_discount(50, True, "")
    calculate_discount(50, False, "")
    try:
        calculate_discount(0, False, "")
    except ValueError:
        pass
```

Real output:

```
$ python3 -m pytest --cov=shop --cov-branch --cov-report=term-missing -q
Name      Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------
shop.py      13      0     10      0   100%
-----------------------------------------------------
TOTAL        13      0     10      0   100%
1 passed in 0.02s
```

100% statement and 100% branch coverage, one green test, and **zero verification**. If a developer changed the 15% to 1,500%, this test would still pass. This is why we say: **coverage measures how much of the code your tests touch, not how good the tests are.** (Mutation testing, from section 16, would expose this test as weak: nearly all mutants would survive.)

**Example 2: a missing requirement.** Suppose the business rule says: *"The SAVE5 coupon is not valid on orders under 20."* The developer forgot to write that rule. Our code has no check for it. Our tests reach 100% coverage of the code that **exists**. But the code that **should exist** is invisible to coverage, because you cannot measure the coverage of code that was never written. Only a black-box test derived from the requirement, such as `calculate_discount(10, False, "SAVE5")` expected to return 0, reveals the gap. This is the fundamental limit of white-box testing.

**Example 3: wrong expectations.** If you choose expected results by running the code and copying what it returns, every test passes forever, even when the code is wrong. Expected results must come from the requirement.

**Example 4: right line, wrong data.** A line can be executed with one lucky input and still fail with another. Coverage records that the line ran, not that it ran correctly for all inputs, such as a boundary value of exactly 100.

#### Sensible coverage targets

What percentage should a team aim for? There is **no single correct number**; it depends on context:

- **Risk**: payment calculations, authentication, or safety-related code deserve stricter targets than a rarely used admin screen.
- **Type of code**: pure logic is easy to cover; user-interface glue and generated code are harder and less valuable to chase.
- **Team agreement**: many teams set a **minimum threshold** (a "quality gate") and fail the build if coverage drops, or use it as a trend over time. The exact value is a team decision.
- **Trend and diff coverage**: some teams care most that **new code** is well covered, rather than the overall number.

Two sound principles: (1) coverage is a **floor, not a goal**: low coverage in important code is a warning sign, but high coverage is not proof of quality; (2) when a number becomes a target, people may write low-value tests to hit it, so pair coverage with code review and with mutation-style thinking.

### 21. Static analysis and code review as white-box activities

Not all white-box activities run the code. Some examine it directly:

**Static analysis** means checking code **without executing it**. In Python, the common tools are **linters**, programs that scan source code for suspicious or non-standard constructs. The most common are:

- **flake8**: checks for style violations and common errors (it combines tools such as pycodestyle and pyflakes).
- **pylint**: a more thorough analyser that also reports design issues and gives a score.
- Others you may meet: **ruff** (a fast linter), **mypy** (type checking), **bandit** (security-focused checks).

Here is a tiny, real example. This file `sloppy.py` has four problems:

```python
import os

def total(items):
    result = 0
    unused = 5
    for i in items:
        result = result + i
    return reslt
```

Running `flake8 sloppy.py` produced:

```
sloppy.py:1:1: F401 'os' imported but unused
sloppy.py:3:1: E302 expected 2 blank lines, found 1
sloppy.py:5:5: F841 local variable 'unused' is assigned to but never used
sloppy.py:8:12: F821 undefined name 'reslt'
```

Each message gives `file:line:column: CODE description`. The most serious is `F821`: `reslt` is a typo that would crash the function with a `NameError` the moment it runs. The linter found it **without running anything**. The `F841` message is a data-flow anomaly (a variable defined and never used), connecting back to data-flow testing.

**Code review** is a human inspection of code, usually by a peer, before it is merged. A review may be informal ("pull request review") or formal (a structured inspection with defined roles). Reviewers look for logic errors, missing error handling, unclear names, security problems, and untested code. A reviewer who asks "which test covers this `else`?" is doing white-box testing with no tools at all. A simple review checklist for a test engineer:

- Does every decision have a test for both outcomes?
- Are loops tested with zero, one, and many iterations?
- Do the tests assert the right things, with expected values from the requirement?
- Is there code that can never run?
- Are error paths (exceptions, invalid input) tested?

**Security and code-level reviews (conceptual only).** A security-minded code review examines code for common weaknesses: unvalidated input, passwords or secrets written into the code, passwords stored in plain text, unsafe construction of database queries, and missing checks on who is allowed to do what. This is white-box security review. For Project 1, a reviewer reading the registration code would ask: *Is the password ever logged or stored without hashing? Is the username checked before being used in a query?* We only introduce the idea here; detailed security testing appears in later training.

### 22. White-box testing on Project 1: registration validation

Now we apply everything to Project 1. Here is a Python version of the registration rule check, in `registration.py`:

```python
def validate_registration(username, password, age):
    """Return a list of error messages (empty list means valid)."""
    errors = []
    if len(username) < 3 or len(username) > 20:
        errors.append("username must be 3-20 characters")
    if len(password) < 8:
        errors.append("password too short")
    elif password.isalpha():
        errors.append("password needs a digit or symbol")
    if age < 18:
        errors.append("must be 18 or older")
    return errors
```

The requirements (which any black-box test would be built from): usernames 3 to 20 characters; passwords at least 8 characters and not made of letters only; users must be 18 or older. Each broken rule adds an error message; a fully valid registration returns an empty list.

#### Step 1: find the decisions

| Decision | Line | Conditions | Outcomes |
|---|---|---|---|
| D1 | `if len(username) < 3 or len(username) > 20` | C1: `len(username) < 3`; C2: `len(username) > 20` | True (error), False (ok) |
| D2 | `if len(password) < 8` | 1 condition | True (too short), False (go to D3) |
| D3 | `elif password.isalpha()` | 1 condition | True (letters only), False (ok) |
| D4 | `if age < 18` | 1 condition | True (underage), False (ok) |

Four decisions, so **8 branch outcomes**. Cyclomatic complexity V(G) = 4 + 1 = **5**. (With each `or` counted as an extra decision point, tools report 6.)

#### Step 2: control flow graph

```
[1: errors = []]
       |
       v
[2: D1: len<3 or len>20 ?] --T--> [3: append username error]
       | F                                   |
       +------------------+------------------+
                          v
[4: D2: len(password) < 8 ?] --T--> [5: append "too short"]
       | F                                   |
       v                                     |
[6: D3: password.isalpha() ?] --T--> [7: append "needs digit"]
       | F                                   |
       +------------------+------------------+
                          v
[8: D4: age < 18 ?] --T--> [9: append "18 or older"]
       | F                                   |
       +------------------+------------------+
                          v
                  [10: return errors]
```

Count: N = 10 (plus an End node, 11). Edges: 1->2, 2->3, 2->4, 3->4, 4->5, 4->6, 5->8, 6->7, 6->8, 7->8, 8->9, 8->10, 9->10, 10->End = 14. With N = 11: V(G) = 14 - 11 + 2 = **5**. This agrees with decisions + 1.

#### Step 3: how many tests for each criterion?

**Statement coverage.** The four `append` lines are the targets. A single test can trigger several of them at once, since the errors are independent. For example, input `("ab", "abc1", 17)` triggers the username, password-too-short, and age errors. The password-letters-only error needs the other arm of the `if/elif`, so a second test is required. So the minimum is **2 tests**:

- Test A: `("ab", "abc1", 17)` runs lines 5, 7, and 11 in the numbered listing of the file.
- Test B: `("alice", "abcdefgh", 25)` runs line 9 (letters-only).

Real tool output with only these two tests, with branch measurement on, shows that statement coverage reached its limit but branch coverage did not:

```
Name              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------
registration.py      19      7     14      2    55%   4->6, 8->10, 17-23
```

The missing arrows `4->6` and `8->10` mean: "the False outcome of the username check (line 4) never happened" and "the False outcome of the letters-only check (line 8) never happened". Lines 17-23 are the loop function, which these tests do not touch.

**Branch coverage.** We need every decision True and False. The minimum is **3 tests**:

| Test | Inputs | D1 | D2 | D3 | D4 |
|---|---|---|---|---|---|
| T1 | `("ab", "abc1", 17)` | T | T | (not evaluated) | T |
| T2 | `("a"*21, "abcdefgh", 25)` | T | F | T | F |
| T3 | `("alice", "secret123", 25)` | F | F | F | F |

Every decision has taken both outcomes. (Remember the `elif` is evaluated only if D2 is False, so D3 is exercised by T2 and T3.)

**Condition coverage on D1.** The two conditions are `len(username) < 3` (C1) and `len(username) > 20` (C2). Because of short-circuiting, C2 is evaluated only when C1 is False.

- C1 True: T1 (username "ab").
- C1 False and C2 True: T2 (username of 21 characters).
- C1 False and C2 False: T3 ("alice").

All four condition outcomes occur. We chose T2's username deliberately as a 21-character string so that it also covers C2 True. If we had used another short username in T2, we would have hit 100% branch coverage but **missed C2 True**. This is a real-world example of why choosing inputs carefully matters.

So **3 tests** achieve statement, branch, and condition coverage here. The three minimum tests, written with proper assertions:

```python
from registration import validate_registration


def test_all_three_errors_short_username_short_password_underage():
    errors = validate_registration("ab", "abc1", 17)
    assert errors == [
        "username must be 3-20 characters",
        "password too short",
        "must be 18 or older",
    ]


def test_long_username_and_letters_only_password():
    errors = validate_registration("a" * 21, "abcdefgh", 25)
    assert errors == [
        "username must be 3-20 characters",
        "password needs a digit or symbol",
    ]


def test_valid_registration_returns_no_errors():
    assert validate_registration("alice", "secret123", 25) == []
```

Real coverage for just these three tests (the loop function is untested, so lines 17-23 are reported):

```
Name              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------
registration.py      19      7     14      0   61%   17-23
```

**No partial branches** (`BrPart` is 0): all 8 branch outcomes of `validate_registration` are covered. The only uncovered code is the login-attempts loop function.

> **Design note.** These three tests pack several errors into each input to minimize test count. That is efficient for coverage but poor for **diagnosis**: when a combined test fails, you do not know which rule broke. In day-to-day practice you often prefer one rule per test (the "one assert idea per test" rule) and accept a few more tests. The 15-test file in this lesson's sample project does exactly that, while the 3-test set shows the theoretical minimum.

#### Step 4: the loop function

`count_failed_logins` (shown in section 14) has a loop, an `if not ok`, and an inner `if failures == max_attempts` with a `break`. Its CFG has decisions for the `for`, `if not ok`, and `if failures == ...`, so V(G) = 3 + 1 = **4**. The six loop-test cases from section 14 (zero, one success, one failure, many, reaching the maximum, beyond the maximum) cover all loop behaviours, all branches, and the `break`.

In our sample project, the full file includes these loop tests:

```python
from registration import count_failed_logins


def test_loop_zero_attempts():
    assert count_failed_logins([]) == 0


def test_loop_stops_at_max():
    assert count_failed_logins([False, False, False, False, False]) == 3


def test_loop_mixed():
    assert count_failed_logins([True, False, True]) == 1
```

and, as a practice task, you can add the missing "one iteration" and "exactly at max" tests.

### 23. White-box and black-box together

Neither approach is enough on its own. They find **different kinds of defects**, and they check **different questions**.

| Question | Answered by |
|---|---|
| Did we build the right thing? Does it match the requirement? | Black-box |
| Did our tests exercise all the code we built? | White-box (coverage) |
| Are the boundaries correct? | Black-box (BVA), confirmed by white-box branch coverage |
| Is there dead code, or logic nobody ever runs? | White-box |
| Is there a requirement with no code? | Black-box only |

#### Worked comparison on the same function: `calculate_discount`

**The black-box view** (Thursday's techniques). Reading only the requirement ("orders of 100 or more get a higher discount; members get extra; SAVE5 adds 5; amount must be positive"):

- **Equivalence partitioning:** partitions for amount (invalid: 0 or less; small: 1 to 99; large: 100 or more), membership (yes/no), coupon (valid `SAVE5`/none/invalid).
- **Boundary value analysis:** amounts of 0, 1, 99, 100, 101.
- **Decision table:** combinations of large order, member, coupon, with expected discount.
- **Error guessing:** a negative amount, a lowercase coupon `"save5"`, a `None` coupon, an extremely large amount.

A sample black-box set: (0, F, ""), (1, F, ""), (99, T, ""), (100, T, ""), (100, F, ""), (101, F, "SAVE5"), (50, F, "save5").

**The white-box view.** The coverage-driven set: (0, F, ""), (150, T, "SAVE5"), (150, F, ""), (50, T, ""), (50, F, "").

**What each finds:**

| Defect scenario | Found by black-box? | Found by white-box? |
|---|---|---|
| The developer wrote `amount > 100` instead of `>= 100` (a boundary bug) | **Yes**: BVA test at exactly 100 fails | **Not necessarily**: tests at 150 and 50 reach 100% branch coverage and pass, as both sides of the boundary behave correctly away from the edge |
| The SAVE5 rule "not valid under 20" was never implemented | **Yes**: a requirement-based test for (10, F, "SAVE5") fails | **No**: coverage of existing code is 100% and tests pass |
| A block of code that handles "seasonal sale" exists but can never be reached | Probably **not**: no requirement refers to it | **Yes**: coverage shows the lines are never executed |
| A branch for a rare input (say, `is_member` is `None`) is never tried | Only if someone thought of the case | **Yes**: a partial branch is reported |
| Tests have no assertions | No | Not by coverage; by review or mutation testing |

The pattern is clear. The boundary bug and the missing requirement are black-box wins. The unreachable code and the untested branch are white-box wins. **Use black-box techniques to decide what the software should do, then use coverage to find out which of the code your tests have not yet examined, and add tests for the gaps.** A practical workflow:

1. Design tests from the requirements (equivalence partitioning, BVA, decision tables).
2. Run them with coverage turned on.
3. Read the uncovered lines and partial branches.
4. For each gap, decide: add a test, remove dead code, or explain why it is excluded.
5. Re-run and record the results.

### 24. Advantages and disadvantages

| Advantages | Disadvantages |
|---|---|
| Finds defects hidden in code that black-box tests never reach | Cannot find missing requirements (code that was never written) |
| Gives a measurable, objective coverage figure | Requires programming skill and access to source code |
| Encourages tests that exercise error handling and rare branches | Tests can become brittle: they may break when code is refactored even though behaviour is unchanged |
| Reveals dead code and unreachable logic | Can create false confidence, since high coverage does not mean good tests |
| Works early, at unit level, where fixing defects is cheapest | Needs detailed knowledge of implementation; time-consuming for large systems |
| Supports refactoring safely (a good unit test suite catches regressions) | Path coverage explodes in size, so full thoroughness is impractical for complex code |
| Helps estimate risk through complexity measures | The tester may unconsciously test "what the code does" rather than "what it should do" |

### 25. Common mistakes

1. **Equating coverage with quality.** 100% coverage with no assertions proves nothing, as demonstrated earlier.
2. **Deriving the expected result from the code.** The oracle must be the requirement. If you copy the output of the code into the assertion, you test that the code equals itself.
3. **Measuring only statement coverage.** Always switch on branch measurement. Statement coverage alone can hide untaken `else` outcomes.
4. **Ignoring compound conditions.** A decision of three conditions joined by `or` needs thought about which combinations to try; branch coverage alone may test only the easy two.
5. **Forgetting short-circuiting.** In Python, the second operand of `and`/`or` may never be evaluated, so a test you thought covered it did not.
6. **Chasing a number.** Writing meaningless tests to push a percentage up, or marking everything `# pragma: no cover`.
7. **Skipping black-box tests because "coverage is high".** Missing requirements and boundary mistakes still slip through.
8. **Writing one giant test.** If one test calls the function ten times with ten asserts, a failure cannot be diagnosed quickly. Prefer one idea per test.
9. **Tests that depend on each other.** Violating isolation makes failures random and hard to reproduce.
10. **Testing private implementation details.** If a test breaks every time someone renames an internal variable, it is too tightly bound to structure. Test behaviour through the function's public interface.
11. **Counting test files as source.** Including `test_*.py` files in the coverage total inflates the percentage (as in the `coverage run` example above, where the tests themselves showed 100%).
12. **Not reading the Missing column.** The report tells you exactly which lines to target; treat it as a to-do list.

---

## Examples

### Example 1: choose tests for statement coverage

```python
def shipping_cost(weight, express):
    cost = 5
    if weight > 10:
        cost = cost + 10
    if express:
        cost = cost * 2
    return cost
```

Statements: `cost = 5`, `if weight > 10`, `cost = cost + 10`, `if express`, `cost = cost * 2`, `return cost` (6 statements).

**One test** `shipping_cost(20, True)` runs every statement: **100% statement coverage**. The expected result (from the requirement) is (5 + 10) x 2 = 30.

**Branch coverage:** 4 outcomes (two decisions, two outcomes each). The single test covers `weight > 10` True and `express` True. We still need `weight > 10` False and `express` False: one more test, `shipping_cost(5, False)`, expected 5, covers both. **Two tests give 100% branch coverage.** Paths: 4, so path coverage needs two more (`(20, False)` -> 15 and `(5, True)` -> 10). V(G) = 2 + 1 = 3.

### Example 2: an `or` condition

```python
def can_book(is_member, has_voucher):
    if is_member or has_voucher:
        return True
    return False
```

Conditions: `is_member` (A), `has_voucher` (B). Because of short-circuit, B is evaluated only if A is False.

| Test | A | B evaluated? | Decision |
|---|---|---|---|
| (True, False) | T | no | T |
| (False, True) | F | yes, T | T |
| (False, False) | F | yes, F | F |

These 3 tests give branch coverage (decision True and False), and every condition outcome that can be observed (A True, A False, B True, B False). Count: V(G) = 1 + 1 = 2 (or 3 if `or` is counted as an extra decision).

### Example 3: reading a partial-branch report

A report line reads:

```
cart.py      40      2     12      1    93%   27, 35->38
```

Interpretation: line 27 never ran (a missing statement), and the branch from line 35 to line 38 was never taken, so the decision on line 35 has only been seen going one way. Open the HTML report, find those lines, and ask what input would trigger them.

---

## Try It: White-Box Testing on Project 1

**Goal:** apply white-box thinking to the registration logic, then combine it with your Thursday black-box tests as part of finishing the Project 1 test-design document.

**What you need:** Python 3, `pip install pytest pytest-cov`, a scratch folder (not your project repository), and your Thursday black-box test cases for registration.

**Steps**

1. **Create the files.** In a new folder, save `registration.py` from section 22 (the `validate_registration` function). Create an empty `test_registration.py`.

2. **Write a first black-box test set.** Using your Thursday work, write at least five pytest tests derived only from the requirement (usernames 3 to 20 characters, password at least 8 characters and not letters only, age 18 or over). Include boundary values: usernames of 2, 3, 20, and 21 characters; passwords of 7 and 8 characters; ages 17 and 18. Each test needs an assertion with an expected value from the requirement.

3. **Run with coverage and branch measurement.**
   ```
   python3 -m pytest --cov=registration --cov-branch --cov-report=term-missing -q
   ```
   Record the percentage, the Missing column, and the BrPart count.

4. **Draw the control flow graph** for `validate_registration` by hand, on paper or in a text editor. Label each node. Compute V(G) using both formulas and confirm they match.

5. **Close the gaps.** For each missing line or partial branch, write down the input that would reach it, add a test (with an expected result from the requirement), and re-run until branch coverage is 100%.

6. **Apply loop testing.** Add `count_failed_logins` from section 14 to your file. Write the six loop-case tests and confirm 100% coverage of that function.

7. **Generate the HTML report.** Run `python3 -m coverage html` (or `--cov-report=html`), open `htmlcov/index.html`, and find the file view for `registration.py`.

8. **Break the code on purpose.** Change `len(password) < 8` to `len(password) <= 8` and re-run. Does a test fail? If none does, your boundary tests are weak even though coverage may still be 100%. Fix the tests, then undo the change.

9. **Document it.** In your Project 1 test-design document, add a short "Structural coverage" section: the function name, V(G), number of tests, final coverage numbers, the list of code areas that are high-risk (high complexity or recently changed), and one sentence on how the white-box tests complement your black-box tests. Feed the high-risk areas into your regression/risk plan.

**Success check:** you can state, without looking, why your set needs more tests for branch coverage than for statement coverage, and which defect your black-box tests found that coverage alone would not.

---

## Practice Exercises

Try each exercise yourself before reading the answer key.

### Exercise 1: Draw a control flow graph

Draw the CFG, number the nodes, list the edges, and compute V(G) with both formulas.

```python
def ticket_price(age, is_student):
    if age < 5:
        price = 0
    elif age >= 65 or is_student:
        price = 8
    else:
        price = 12
    return price
```

### Exercise 2: Compute cyclomatic complexity

Compute V(G) using "decision points + 1" and state how many tests you need at minimum for the basis set.

```python
def process(orders):
    count = 0
    for order in orders:
        if order > 0:
            count += 1
        if order > 1000:
            count += 5
    while count > 100:
        count -= 100
    return count
```

### Exercise 3: Tests for 100% branch coverage

Choose the minimum tests for 100% branch coverage of `ticket_price` from Exercise 1. List the inputs and expected results (age and student status determine price: under 5 free; 65 or older, or students, pay 8; otherwise 12).

### Exercise 4: Statement versus branch

```python
def clamp_score(score):
    result = score
    if score > 100:
        result = 100
    return result
```

(a) What single test gives 100% statement coverage? (b) What is the branch coverage of that test? (c) What second test completes branch coverage?

### Exercise 5: Loop test design

Write loop tests for this function. List the inputs and expected results for zero, one, many, and maximum iterations.

```python
def total_first_three(values):
    total = 0
    count = 0
    for v in values:
        total += v
        count += 1
        if count == 3:
            break
    return total
```

### Exercise 6: Condition coverage

For `if age >= 18 and has_id:`, give a set of tests that achieves condition/decision coverage. Then say how many tests multiple condition coverage would need, and note any short-circuit effect.

### Exercise 7: Spot what coverage cannot see

A function `withdraw(balance, amount)` is tested with a suite that reaches 100% statement and branch coverage. The requirement also says "amounts above the daily limit of 500 must be refused", but the developer never implemented a daily limit. Explain why coverage did not reveal this and which kind of test would.

### Answer Keys

**Answer 1.**

Nodes: N1 = `if age < 5`; N2 = `price = 0`; N3 = `elif age >= 65 or is_student`; N4 = `price = 8`; N5 = `price = 12`; N6 = `return price`; N7 = End.

```
[1: age < 5 ?] --T--> [2: price = 0] -----------+
      | F                                        |
      v                                          |
[3: age>=65 or is_student ?] --T--> [4: price=8] |
      | F                              |         |
      v                                |         |
[5: price = 12] ---------------------- +---------+
                                       |
                                       v
                                [6: return price] --> [7: End]
```

Edges: 1->2, 1->3, 3->4, 3->5, 2->6, 4->6, 5->6, 6->7 = 8 edges. N = 7.

V(G) = E - N + 2 = 8 - 7 + 2 = **3**. Decision points: `if` and `elif` = 2; 2 + 1 = **3**. (If the `or` is counted as another decision, a tool reports 4.)

**Answer 2.**

Decision points: the `for` (1), `if order > 0` (2), `if order > 1000` (3), the `while` (4). V(G) = 4 + 1 = **5**. At least **5** tests are needed for the basis set (5 independent paths). A suitable set: `[]` (loop skipped, while skipped); `[0]` (loop once, both ifs False); `[5]` (first if True, second False); `[2000]` (both ifs True, count becomes 6, while skipped); and a case where the `while` runs, which needs `count > 100`: for example a list of 101 positive numbers such as `[1] * 101` (count becomes 101, the while loop runs once, leaving 1). Note that this shows how a `while` loop's body can need a lot of input to reach.

**Answer 3.**

Decision outcomes: D1 (`age < 5`) True/False; D2 (`age >= 65 or is_student`) True/False. 4 outcomes, so **3 tests** suffice.

| Test | Inputs (age, is_student) | D1 | D2 | Expected price |
|---|---|---|---|---|
| 1 | (3, False) | T | not evaluated | 0 |
| 2 | (70, False) | F | T | 8 |
| 3 | (30, False) | F | F | 12 |

For condition coverage on `age >= 65 or is_student` we also want `is_student` True: add (20, True) expecting 8. That gives 4 tests for condition/decision coverage. Black-box boundary tests would add ages 4, 5, 64, 65.

**Answer 4.**

(a) `clamp_score(150)` runs `result = score`, the `if`, `result = 100`, and the `return`: 100% statement coverage; expected 100.
(b) Only the True outcome of the decision was taken: 1 of 2 outcomes = **50%**.
(c) `clamp_score(50)`, expected 50, takes the False outcome and completes branch coverage. This is a direct instance of "100% statement does not imply 100% branch".

**Answer 5.**

| Case | Input | Expected |
|---|---|---|
| Zero iterations | `[]` | 0 |
| One iteration | `[4]` | 4 |
| Many (fewer than the break) | `[1, 2]` | 3 |
| Maximum (exactly 3) | `[1, 2, 3]` | 6 |
| Beyond the maximum (break must stop the loop) | `[1, 2, 3, 4, 5]` | 6 |

The last test proves that the `break` prevents extra values being added. The requirement ("total the first three values") is the source of the expected results.

**Answer 6.**

Conditions: A = `age >= 18`, B = `has_id`. Condition/decision coverage needs A and B each True and False, and the decision both True and False.

- Test 1: (20, True): A T, B T, decision T.
- Test 2: (20, False): A T, B F, decision F.
- Test 3: (10, True): A F, B not evaluated (short-circuit), decision F.

These three tests give A T/F, B T/F, and decision T/F. Multiple condition coverage needs all four combinations TT, TF, FT, FF, so **4 tests**; add (10, False) for FF. In Python, FT and FF both short-circuit at A, so B is never evaluated in them. Tools and testers still design them separately because the behaviour would matter if the expression were reordered.

**Answer 7.**

Coverage measures which **existing code** has been executed. A daily-limit check that was never written does not appear in the code, so it cannot appear as an uncovered line or partial branch. The code that exists was fully exercised, so the report was clean. Only a **requirement-based (black-box) test** reveals it: for example `withdraw(1000, 600)` where the requirement expects a refusal. The lesson: white-box testing cannot find omissions. This is why both approaches are needed.

---

## Knowledge Check

1. What is the difference between white-box and black-box testing in terms of how test cases are designed?
2. Name three synonyms for white-box testing.
3. Who typically performs white-box testing, and at which test levels is it most common?
4. In code, what is the difference between a *decision* and a *condition*?
5. What are the two parts of a control flow graph, and what does each represent?
6. A function has 10 executable statements and tests run 8 of them. What is the statement coverage?
7. A function has 3 `if` statements with no loops. What is its cyclomatic complexity using "decisions + 1"?
8. A control flow graph has 9 edges, 8 nodes, and 1 connected component. What is V(G)?
9. Why does 100% branch coverage imply 100% statement coverage, but not the other way round? Give a counter-example.
10. List the loop-testing cases for a simple loop.
11. What does the `BrPart` column in a coverage.py report mean?
12. What does `--cov-branch` change in a pytest-cov report?
13. Give two reasons why 100% coverage does not mean the software is bug-free.
14. What is a linter, and name two Python linters.
15. What is the Arrange-Act-Assert pattern?
16. What is the difference between a stub and a mock (name level)?
17. What is mutation testing trying to measure, and what does a "surviving mutant" mean?
18. Why do we use black-box and white-box testing together?
19. Why must a test's expected result come from the requirement and not from the code?
20. In Python, why might the second condition of `A and B` not be evaluated in a test?

### Answers

1. Black-box test cases are designed from the **requirements and specification** without looking at the code (techniques such as equivalence partitioning and BVA). White-box test cases are designed from the **code's internal structure** (statements, branches, conditions, paths, loops), and adequacy is measured by coverage. Expected results in both come from the requirements.
2. Glass-box testing, clear-box testing, structure-based (or structural) testing. Code-based testing is also used.
3. Developers (unit tests, code reviews) and SDETs/automation engineers. Most common at unit/component and integration levels, plus code reviews and static analysis.
4. A decision is the whole Boolean expression that steers the flow (for example `a > 1 and b`). A condition is one atomic true/false piece within it (`a > 1`, `b`).
5. Nodes represent statements, blocks of statements, or decision points; edges (arrows) represent possible transfers of control from one node to the next.
6. 8 / 10 x 100 = 80%.
7. 3 + 1 = 4.
8. V(G) = E - N + 2P = 9 - 8 + 2 = 3.
9. If every decision outcome has been taken, every statement reachable through any outcome has run, so branch coverage 100% gives statement coverage 100%. The reverse fails: `def f(x, v): if v: x = x + 10 ; return x` tested only with `v = True` runs every statement but never takes the False outcome, so branch coverage is 50%.
10. Zero iterations, one iteration, many (typical) iterations, maximum iterations, and boundaries around the maximum (n - 1, n + 1) where applicable.
11. The number of partial branches: decisions where only one of the two outcomes has been exercised.
12. It adds branch measurement: the Branch and BrPart columns, and the percentage then combines statements and branches. Missing branches appear as arrows such as `2->4`.
13. Any two of: tests may have no assertions; code that should exist (a missing requirement) is invisible to coverage; expected results may be wrong; a line can run with one input and fail with another (boundaries); coverage shows execution, not correctness.
14. A linter is a static analysis tool that scans source code without running it to find style issues and likely errors. Examples: flake8 and pylint (also ruff).
15. Arrange (set up inputs and state), Act (call the code under test), Assert (check the result against the expected value).
16. A stub supplies canned answers to the unit under test; a mock additionally records how it was called so the test can verify the interaction.
17. It measures how good the tests are at detecting changes (bugs) by making small deliberate changes to the code and checking whether tests fail. A surviving mutant is a changed version of the code that no test noticed, showing a weakness in the tests.
18. They find different defects. Black-box checks that the software meets requirements (catching missing features and boundary mistakes); white-box shows which code the tests never exercised (catching dead code and untested branches). Together they give broader confidence.
19. Because the code may be wrong. If you copy what the code produces, the test only confirms that the code does what it does, so a faulty implementation passes.
20. Python uses short-circuit evaluation: if A is False in `A and B`, the answer is already known (False), so B is never evaluated. (For `or`, B is skipped if A is True.)

---

## Key Takeaways

- **White-box testing** (structure-based, glass-box, clear-box) designs and measures tests using the **internal structure** of the code. Black-box asks "does it do what it should?"; white-box asks "have we exercised what we built?"
- Developers and SDETs do it, mostly at **unit, component, and integration** level, and through **code reviews** and **static analysis**.
- Know the vocabulary: **statement, decision, branch, condition, path, loop**. A **control flow graph** (nodes and edges) maps all routes through a function.
- **Statement coverage** = executed statements / total statements. **Branch coverage** = executed decision outcomes / total outcomes. **Condition coverage** = condition outcomes seen / (2 x conditions). **Multiple condition coverage** needs all 2^n combinations.
- **100% branch coverage implies 100% statement coverage, not the reverse.** Always measure branches with `--cov-branch`.
- **Cyclomatic complexity** V(G) = E - N + 2P = decision points + 1; it gives the number of independent paths and a risk signal.
- **Loop tests:** zero, one, many, maximum (and just beyond).
- **Data-flow testing** follows variables (definitions and uses); **mutation testing** checks whether tests can detect small deliberate bugs.
- Use **pytest and coverage.py**: `pytest --cov=module --cov-branch --cov-report=term-missing`, and `coverage html` to see missed lines highlighted.
- **100% coverage is not bug-free**: no assertions, wrong expectations, and missing requirements all slip through. Coverage targets are context dependent and best treated as a floor.
- **Unit tests** follow Arrange-Act-Assert, one idea per test, and isolation; stubs and mocks replace external dependencies.
- **Use both** black-box and white-box techniques: requirements decide what to test; coverage shows what you have not yet looked at.

---

## Additional Resources

- **Coverage.py documentation**: https://coverage.readthedocs.io/ (installation, branch coverage, reports, and configuration).
- **pytest documentation**: https://docs.pytest.org/ (test discovery, assertions, `pytest.raises`, and fixtures).
- **ISTQB Glossary and syllabi**: https://www.istqb.org/ (official definitions of white-box testing, statement coverage, decision coverage, and related terms; look for the Foundation Level syllabus).
- **pytest-cov plugin documentation**: https://pytest-cov.readthedocs.io/ (options for `--cov`, `--cov-branch`, and report formats).
