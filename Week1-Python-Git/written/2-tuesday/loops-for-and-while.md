# Loops: for and while

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a loop is and why repetition is essential in programming.
- Write `for` loops using `range()` with start, stop and step values.
- Loop over the characters of a string.
- Write `while` loops with a condition and understand how they stop.
- Use counters and accumulators (running totals) inside loops.
- Choose between `for` and `while` for a given task.
- Write nested loops and trace them step by step.
- Recognize and avoid infinite loops and off-by-one errors.

---

## Why This Matters

Computers are excellent at doing the same thing many times without getting bored or making typing mistakes. A **loop** repeats a block of code.

In test automation, repetition is everywhere:

- Run the same login check with 50 different usernames.
- Retry an unstable action up to three times.
- Scan thousands of lines in a log file looking for the word `ERROR`.
- Wait until a page finishes loading.
- Generate 100 test IDs: `TC-001`, `TC-002`, ...

Without loops, you would copy and paste the same lines over and over, which is slow, error-prone and impossible to change later. Today's exercises (a number-guessing game and a log-line scanner) both use loops heavily.

Yesterday you learned conditionals, which decide *whether* code runs. Loops decide *how many times* code runs. Combined, they let you write programs that solve real problems.

---

## The Concept

### 1. The Problem Loops Solve

Suppose you want to print the numbers 1 to 5. Without a loop:

```python
print(1)
print(2)
print(3)
print(4)
print(5)
```

Fine for 5. Now imagine 1,000. A loop does it in two lines:

```python
for number in range(1, 6):
    print(number)
```

Python has two kinds of loops:

| Loop | Use when... |
|---|---|
| **`for`** | You know in advance **how many times** to repeat, or you are going through the items of something |
| **`while`** | You want to repeat **as long as a condition stays true**, and you don't know in advance how many times |

---

### 2. The `for` Loop

Syntax:

```python
for variable in sequence:
    # block to repeat
```

- `for` and `in` are keywords.
- `variable` is a name you choose; on each repetition (called an **iteration**), it takes the next value from the sequence.
- The line ends with a **colon**, and the repeated block is **indented**, just like `if`.

#### 2.1 `range()`: generating a sequence of numbers

`range()` produces a series of whole numbers. It has three forms:

| Form | Meaning | Numbers produced |
|---|---|---|
| `range(stop)` | From 0 up to **but not including** `stop` | `range(5)` gives 0, 1, 2, 3, 4 |
| `range(start, stop)` | From `start` up to but not including `stop` | `range(2, 6)` gives 2, 3, 4, 5 |
| `range(start, stop, step)` | Jump by `step` each time | `range(0, 10, 2)` gives 0, 2, 4, 6, 8 |

**The stop value is never included.** This is the most common source of confusion, so memorize it: `range(1, 6)` gives 1 through **5**, not 6.

```python
for i in range(5):
    print(i)
```

```text
0
1
2
3
4
```

Counting starts at 0 by default. This "zero-based" counting is a standard convention in programming; we will see it again with indexing on Wednesday.

```python
for i in range(1, 6):
    print(f"Test run number {i}")
```

```text
Test run number 1
Test run number 2
Test run number 3
Test run number 4
Test run number 5
```

**Counting by steps and counting down:**

```python
for n in range(0, 21, 5):
    print(n)            # 0, 5, 10, 15, 20

for n in range(5, 0, -1):
    print(n)            # 5, 4, 3, 2, 1
print("Liftoff!")
```

A negative step counts down. When counting down, `start` must be larger than `stop`.

#### 2.2 Tracing a loop

Tracing means following the loop by hand. Let's trace this:

```python
total = 0
for n in range(1, 5):
    total = total + n
print(total)
```

| Iteration | `n` | `total` before | `total` after |
|---|---|---|---|
| 1 | 1 | 0 | 1 |
| 2 | 2 | 1 | 3 |
| 3 | 3 | 3 | 6 |
| 4 | 4 | 6 | 10 |

After the loop ends, `print(total)` shows `10`. Notice `print(total)` is **not indented**, so it runs once after the loop completes. If it were indented, it would print on every iteration.

This `total` variable is called an **accumulator**: it starts at a known value (0) and builds up a result across iterations. Accumulators are one of the most important loop patterns.

#### 2.3 Looping over a string

A string is a sequence of characters, so `for` can step through it one character at a time:

```python
test_id = "TC-042"

for character in test_id:
    print(character)
```

```text
T
C
-
0
4
2
```

Practical use: counting characters of a certain kind.

```python
test_id = "TC-042-LOGIN-07"
digit_count = 0

for ch in test_id:
    if ch.isdigit():
        digit_count += 1

print(f"{test_id} contains {digit_count} digits")
```

```text
TC-042-LOGIN-07 contains 5 digits
```

`.isdigit()` is a string method that returns `True` for characters `0` through `9`. Here we combine a **loop**, a **conditional** and a **counter**, a combination you'll use constantly.

Other helpful string checks: `.isalpha()` (letters only), `.isupper()`, `.islower()`.

In Wednesday's lesson, you will learn that the same `for` loop also works over lists, dictionaries and other collections.

#### 2.4 The loop variable and `_`

If you don't need the loop variable, convention is to name it `_`:

```python
for _ in range(3):
    print("Retrying...")
```

#### 2.5 Using the loop variable to build things

```python
for number in range(1, 6):
    print(f"TC-{number:03d}")
```

```text
TC-001
TC-002
TC-003
TC-004
TC-005
```

This is a mini test-ID generator, using the f-string zero-padding from Monday.

---

### 3. The `while` Loop

Syntax:

```python
while condition:
    # block to repeat
```

A `while` loop checks the condition **before each iteration**. If it is `True`, the block runs, and then Python goes back and checks again. When the condition becomes `False`, the loop ends and the program continues after it.

```
         ┌────────────────┐
   ┌────▶│  condition?    │──── False ───▶ continue after loop
   │     └───────┬────────┘
   │           True
   │             ▼
   │       run the block
   └─────────────┘
```

```python
count = 1

while count <= 5:
    print(f"Count is {count}")
    count += 1

print("Loop finished")
```

```text
Count is 1
Count is 2
Count is 3
Count is 4
Count is 5
Loop finished
```

A working `while` loop needs three ingredients:

1. **Initialization:** set up the variable the condition uses (`count = 1`).
2. **Condition:** a test that eventually becomes false (`count <= 5`).
3. **Update:** something inside the loop that moves toward making the condition false (`count += 1`).

#### 3.1 Infinite loops: the classic danger

If you forget the update, the condition never becomes `False`, and the loop runs forever:

```python
count = 1
while count <= 5:
    print(count)
    # forgot count += 1
```

This prints `1` endlessly. **To stop a runaway program, press `Ctrl + C` in the terminal.** Whenever you write a `while` loop, ask: *"What changes inside the loop so that it will eventually stop?"*

#### 3.2 When `while` shines: not knowing how many times

Use `while` when the number of repetitions depends on something that happens during the program, such as user input.

**Input validation:** keep asking until the answer is acceptable:

```python
age_text = input("Enter your age (1-120): ")
age = int(age_text)

while age < 1 or age > 120:
    print("That is not a valid age.")
    age = int(input("Enter your age (1-120): "))

print(f"Age accepted: {age}")
```

The loop repeats while the answer is invalid and ends as soon as a valid number is entered. (If the user types text that is not a number, `int()` raises a `ValueError`; handling that is a topic for later in the program.)

**Halving until small:**

```python
size = 1000
steps = 0

while size > 1:
    size = size / 2
    steps += 1

print(f"Took {steps} steps")     # Took 10 steps
```

We could not have used `range()` here, because we did not know in advance how many steps were needed.

**Simulated retries (a testing pattern):**

```python
max_attempts = 3
attempt = 1
success = False

while attempt <= max_attempts and not success:
    print(f"Attempt {attempt}: trying to connect...")
    if attempt == 3:           # pretend the third attempt works
        success = True
    attempt += 1

if success:
    print("Connected")
else:
    print("Gave up after 3 attempts")
```

```text
Attempt 1: trying to connect...
Attempt 2: trying to connect...
Attempt 3: trying to connect...
Connected
```

The loop has two reasons to stop (out of attempts, or success), expressed using `and` and `not`.

---

### 4. `for` vs `while`: Which to Use?

| Question | Choose |
|---|---|
| "Do something exactly N times" | `for` with `range(N)` |
| "Go through every character/item" | `for` |
| "Keep going until something happens" | `while` |
| "Repeat until the user gives valid input" | `while` |

Rule of thumb: if you can say *"for each ..."* or *"N times"*, use `for`. If you say *"as long as ..."* or *"until ..."*, use `while`. Any `for` loop can be rewritten as a `while`, but the `for` version is usually shorter and safer, because it can't accidentally run forever.

---

### 5. Common Loop Patterns

#### 5.1 Counter (counting how many)

```python
failures = 0
for n in range(1, 11):
    if n % 3 == 0:           # pretend every third test fails
        failures += 1
print(f"Failures: {failures}")     # Failures: 3
```

#### 5.2 Accumulator (running total)

```python
total_time = 0.0
for run in range(1, 4):
    total_time += run * 1.5        # pretend durations are 1.5, 3.0, 4.5
print(f"Total: {total_time}")      # Total: 9.0
```

#### 5.3 Building a string

```python
line = ""
for i in range(1, 6):
    line += str(i) + " "
print(line)            # 1 2 3 4 5
```

#### 5.4 Finding the largest (or smallest)

```python
largest = 0
for n in range(1, 8):
    value = (n * 7) % 10        # makes a jumbled series of numbers: 7, 4, 1, 8, 5, 2, 9
    if value > largest:
        largest = value
print(f"Largest value: {largest}")     # 9
```

#### 5.5 Printing a simple pattern

```python
for row in range(1, 6):
    print("*" * row)
```

```text
*
**
***
****
*****
```

---

### 6. Nested Loops

A loop inside another loop is a **nested loop**. For each iteration of the outer loop, the inner loop runs completely.

```python
for row in range(1, 4):
    for col in range(1, 4):
        print(f"({row},{col})", end=" ")
    print()          # new line after each row
```

```text
(1,1) (1,2) (1,3) 
(2,1) (2,2) (2,3) 
(3,1) (3,2) (3,3) 
```

Trace: when `row = 1`, the inner loop runs `col = 1, 2, 3`. Then `row = 2`, the inner loop runs again fully, and so on. Total prints: 3 × 3 = 9.

Notice `print(..., end=" ")` from Monday keeps output on one line, and the lone `print()` (at the *outer* loop's indentation) ends each row.

**Multiplication table:**

```python
for i in range(1, 4):
    for j in range(1, 6):
        print(f"{i * j:3d}", end="")
    print()
```

```text
  1  2  3  4  5
  2  4  6  8 10
  3  6  9 12 15
```

A testing example is combining every browser with every screen size in a test matrix: each outer iteration picks a browser, and the inner loop tries every size.

Nested loops multiply the work (10 × 10 = 100 iterations; 1000 × 1000 = a million), so use them thoughtfully.

---

### 7. Exiting and Skipping Within Loops (Preview)

Python offers `break` and `continue` to **exit** a loop early or **skip** an iteration. They are powerful enough to deserve their own lesson, which comes next, **Break and continue statements**. Until then, stick to loops that end naturally.

---

### 8. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Off-by-one with `range` | `range(1, 5)` gives 1-4, not 1-5 | Use `range(1, 6)` to include 5 |
| Infinite `while` loop | Forgot to update the variable | Add the update; `Ctrl + C` to stop |
| Missing colon | `for i in range(5)` | Add `:` |
| Wrong indentation | Code after the loop is indented | Unindent to run it only once |
| Resetting the accumulator inside the loop | `total = 0` inside the `for` | Initialize **before** the loop |
| Modifying `range` expectations | `range(5.0)` fails (needs integers) | Use `int()` |
| Using `=` in the `while` condition | `while x = 5:` | Use `==`, `<`, etc. |
| Printing inside vs outside the loop | Output repeated 100 times | Check indentation |

**Debugging tip:** add a `print()` inside the loop showing the loop variable and key values. Watching them change on each iteration shows you exactly what the loop is doing.

---

### 9. Practice Activities

1. **Count up and down.** Print 1 to 10, then 10 down to 1.
2. **Even numbers.** Print all even numbers from 2 to 20 using the `step` argument. Then do it again using `%` and an `if`.
3. **Sum and average.** Compute the sum of the numbers from 1 to 100 using an accumulator. Check against the formula n(n+1)/2.
4. **Test ID generator.** Print `TC-001` through `TC-020` using an f-string.
5. **Vowel counter.** Ask for a word and count its vowels using `for` over the characters and `in "aeiou"`.
6. **Factorial.** Ask for a whole number n and compute n! (n × (n-1) × ... × 1) with a loop.
7. **Password retry.** Using `while`, ask for a password until the user enters the correct one (store the secret in a variable), but stop after 3 attempts and print the right message either way.
8. **Triangle.** Print a right-angled triangle of `#` characters with a height chosen by the user.
9. **Trace by hand.** Without running it, trace `total = 0` then `for i in range(2, 10, 3): total += i`. What are the iterations and the final total? Then verify by running.
10. **Matrix.** Using nested loops, print every combination of the browsers `"C"`, `"F"` (you can write them as two strings) with screen widths 1, 2, 3, as pairs.

---

## Summary

- A **loop** repeats a block of code, vital for running many checks and processing lots of data.
- **`for variable in sequence:`** repeats once for each item; `range(stop)`, `range(start, stop)` and `range(start, stop, step)` generate numbers; the **stop value is excluded**.
- Strings can be looped over character by character; collections (Wednesday) work the same way.
- **`while condition:`** repeats as long as the condition is true. It needs initialization, a condition and an update, or it becomes an **infinite loop** (`Ctrl + C` stops it).
- Use `for` when you know the count or are going through items; use `while` for "until/as long as" situations such as validating input.
- Core patterns: **counters**, **accumulators**, building strings, finding largest/smallest.
- **Nested loops** run the inner loop completely for every pass of the outer loop.
- Next: **break** and **continue** give you finer control over loops.

---

## Additional Resources

- Python Tutorial: `for` Statements and the `range()` Function: https://docs.python.org/3/tutorial/controlflow.html#for-statements
- Python documentation: The `while` statement: https://docs.python.org/3/reference/compound_stmts.html#the-while-statement
- Real Python: Python `for` Loops (Definite Iteration): https://realpython.com/python-for-loop/
