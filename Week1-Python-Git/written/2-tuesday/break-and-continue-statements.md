# Break and Continue Statements

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what `break` and `continue` do and how they differ.
- Use `break` to exit a loop as soon as a goal is reached.
- Use `continue` to skip the rest of the current iteration.
- Build `while True` loops that exit with `break`.
- Understand how `break` and `continue` behave inside nested loops.
- Use the loop `else` clause to detect "the loop finished without a break".
- Decide when `break`/`continue` make code clearer and when they make it harder to read.

---

## Why This Matters

Normally a loop runs until its natural end: `for` finishes its sequence, or `while` sees its condition become false. But real programs often need to be smarter:

- **Stop early.** Once you've found the first failing test, there's no need to check the other 9,999. Once a user guesses the right number, the game should end.
- **Skip some items.** When scanning a log, ignore blank lines and comments, but keep processing everything else.

`break` and `continue` give you that fine-grained control. Today's exercise, a number-guessing game and a log-line scanner, uses them directly: the guessing game ends with `break` when the guess is right, and the scanner uses `continue` to skip lines it doesn't care about.

You learned `for` and `while` earlier today, and conditionals before that. `break` and `continue` are almost always used together with an `if` inside a loop.

---

## The Concept

### 1. The Big Picture

| Statement | What it does | Analogy |
|---|---|---|
| `break` | **Ends the entire loop immediately**; execution continues after the loop | Leaving a building when you find what you were looking for |
| `continue` | **Skips the rest of the current iteration** and jumps to the next one | Skipping a song and moving to the next track |

```
loop start ──▶ iteration ──▶ [continue] ──▶ jump to next iteration
                   │
                [break] ──▶ jump out of the loop entirely
```

---

### 2. The `break` Statement

#### 2.1 Basic use

```python
for number in range(1, 11):
    if number == 5:
        break
    print(number)

print("Loop ended")
```

```text
1
2
3
4
Loop ended
```

Trace:

- `number = 1` to `4`: the condition is false, so the number is printed.
- `number = 5`: the condition is true, so `break` runs. The loop stops **immediately**, `print(number)` doesn't run for 5, and numbers 6 to 10 are never visited.
- Python continues with the first line **after** the loop: `print("Loop ended")`.

#### 2.2 Searching: stop at the first match

```python
target = "TC-007"

for number in range(1, 20):
    current_id = f"TC-{number:03d}"
    if current_id == target:
        print(f"Found {current_id} at position {number}")
        break
```

```text
Found TC-007 at position 7
```

Once you've found it, continuing would waste time. Searching loops are the most common use of `break`.

#### 2.3 `while True` with `break`

A `while True` loop would be infinite on its own, because `True` never becomes `False`. But with a `break`, it becomes a clean way to write "keep going until something specific happens":

```python
while True:
    answer = input("Type 'quit' to exit: ").strip().lower()
    if answer == "quit":
        break
    print(f"You typed: {answer}")

print("Goodbye")
```

```text
Type 'quit' to exit: hello
You typed: hello
Type 'quit' to exit: QUIT
Goodbye
```

This pattern is common for menus, prompts, and any loop where the exit condition is discovered *in the middle* of an iteration rather than at the top.

**Always make sure that a `while True` has a reachable `break`.** If you forget, you have an infinite loop (stop it with `Ctrl + C`).

#### 2.4 Input validation using `while True`

Compare with the validation loop from the previous lesson. This version asks only once in the code:

```python
while True:
    text = input("Enter a number from 1 to 10: ")
    number = int(text)
    if 1 <= number <= 10:
        break
    print("Out of range, try again.")

print(f"You chose {number}")
```

#### 2.5 A guessing-game skeleton

This is the heart of the number-guessing exercise. (Here the secret number is fixed; in the exercise you'll make it random.)

```python
secret = 7
attempts = 0

while True:
    guess = int(input("Guess the number (1-10): "))
    attempts += 1

    if guess < secret:
        print("Too low")
    elif guess > secret:
        print("Too high")
    else:
        print(f"Correct! You needed {attempts} attempts.")
        break
```

```text
Guess the number (1-10): 3
Too low
Guess the number (1-10): 9
Too high
Guess the number (1-10): 7
Correct! You needed 3 attempts.
```

Here, the loop's exit decision is made inside a conditional, which is exactly when `break` is the best tool. Notice how many ideas are combined: a loop, a counter, `input`, type conversion, an `if/elif/else` chain and `break`.

---

### 3. The `continue` Statement

`continue` skips the **remaining lines of the current iteration** and goes straight to the next iteration. The loop does not end.

#### 3.1 Basic use

```python
for number in range(1, 8):
    if number % 2 == 0:
        continue
    print(number)
```

```text
1
3
5
7
```

When `number` is even, `continue` jumps back to the top of the loop for the next value, so the `print` is skipped. Only the odd numbers are printed.

> **Break vs continue on the same loop:**
> - With `break` at `number == 5`, output is `1 2 3 4`: the loop *ends*.
> - With `continue` at `number == 5`, output is `1 2 3 4 6 7 8 ...`: only 5 is *skipped*.

#### 3.2 Filtering: skip what you don't want

```python
test_id = "TC-042-LOGIN-07"
digits = ""

for ch in test_id:
    if not ch.isdigit():
        continue          # ignore anything that isn't a digit
    digits += ch

print(digits)             # 04207
```

Without `continue`, you'd write `if ch.isdigit(): digits += ch`, and both are fine. `continue` is helpful when it lets you handle "uninteresting" cases early and keep the main logic un-indented.

#### 3.3 `continue` in a `while` loop: be careful!

In a `while` loop, `continue` jumps straight back to the condition check. If your counter update is *after* the `continue`, it gets skipped, and the loop can run forever:

```python
# BUG: infinite loop
count = 0
while count < 5:
    if count == 2:
        continue          # jumps back without ever changing count
    print(count)
    count += 1
```

Fix by updating before the `continue`:

```python
count = 0
while count < 5:
    count += 1
    if count == 2:
        continue
    print(count)          # prints 1, 3, 4, 5
```

---

### 4. Using Both Together: A Log Scanner Preview

Imagine each line of a log contains a level such as `INFO`, `WARNING` or `ERROR`. Your job is to count the errors, ignore blank lines and stop reading when you find the line `END`.

First, a small piece of text to work with. A triple-quoted string can span many lines, and the `.splitlines()` method splits it so that a `for` loop can go through it **line by line**. (`.splitlines()` produces a collection of lines. Collections such as lists are the topic of tomorrow's lessons; for now, just use it with `for`.)

```python
log_text = """INFO Server started
INFO User logged in

WARNING Slow response
ERROR Database timeout
INFO Retrying
ERROR Connection refused
END
ERROR This line is after the end"""

error_count = 0
lines_read = 0

for line in log_text.splitlines():
    line = line.strip()

    if line == "":
        continue                 # skip blank lines

    if line == "END":
        break                    # stop reading entirely

    lines_read += 1

    if line.startswith("ERROR"):
        error_count += 1
        print(f"Error found: {line}")

print(f"Lines read: {lines_read}")
print(f"Errors found: {error_count}")
```

```text
Error found: ERROR Database timeout
Error found: ERROR Connection refused
Lines read: 6
Errors found: 2
```

Walkthrough:

1. The blank line is skipped by `continue` (it isn't counted in `lines_read`).
2. When the `END` line appears, `break` stops the loop, so the final `ERROR This line is after the end` is never examined.
3. `.startswith("ERROR")` is a string method that returns `True` if the text begins with the given text.
4. `error_count` is a counter; `lines_read` is another.

This is almost exactly what you'll build in the exercise, but reading from keyboard input or a defined text block.

---

### 5. `break` and `continue` in Nested Loops

In nested loops, `break` and `continue` affect **only the innermost loop** that contains them.

```python
for row in range(1, 4):
    for col in range(1, 4):
        if col == 2:
            break              # exits the INNER loop only
        print(f"({row},{col})")
```

```text
(1,1)
(2,1)
(3,1)
```

For each `row`, the inner loop prints `col = 1`, then hits `col == 2` and breaks out of the inner loop. The outer loop keeps going, so we see all three rows.

To stop **both** loops, use a flag variable (a boolean that remembers "we're done"):

```python
found = False

for row in range(1, 6):
    for col in range(1, 6):
        if row * col == 12:
            print(f"Found: row={row}, col={col}")
            found = True
            break              # leave inner loop
    if found:
        break                  # leave outer loop
```

```text
Found: row=3, col=4
```

---

### 6. The Loop `else` Clause

Python loops (both `for` and `while`) can have an `else` block. It runs **only if the loop finished normally, without hitting `break`**. This is perfect for "search, and tell me if you didn't find it".

```python
target = "TC-099"

for number in range(1, 21):
    if f"TC-{number:03d}" == target:
        print("Found it")
        break
else:
    print(f"{target} was not found")
```

```text
TC-099 was not found
```

If the target had been found, `break` would skip the `else`. Many Python programmers find this feature surprising, so use it sparingly and add a comment if it helps your readers. A flag variable (`found = False`) is an equally valid alternative.

---

### 7. When to Use (and Not Use) Them

**Good uses:**

- Exit when a search succeeds.
- Exit a `while True` loop when a user chooses to quit or provides valid data.
- Skip invalid or irrelevant data early with `continue`.

**Be careful when:**

- A loop has many `break`s and `continue`s scattered around. It becomes hard to follow which path the code takes. Consider restructuring.
- You could express the stopping rule clearly in the loop condition itself. This:

  ```python
  count = 0
  while count < 5:
      count += 1
  ```
  is cleaner than a `while True` with a `break` at `count == 5`.

Remember: the goal is **readable** code. Both styles are valid; choose the clearer one.

---

### 8. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| `break` outside a loop | `break` at the top level | `SyntaxError`: only use inside `for`/`while` |
| Forgetting the `if` | `break` unconditionally on the first line | Wrap in a condition |
| `continue` skipping the counter update in `while` | Infinite loop | Update before `continue` |
| Expecting `break` to leave all nested loops | Outer loop continues | Use a flag |
| Confusing `break` and `continue` | Loop ends when you wanted a skip | `break` = stop; `continue` = skip this one |
| `while True` with no `break` | Never ends | Make sure an exit is reachable; `Ctrl + C` to stop |
| Indentation | `else` aligned with `if` instead of `for` | Align `else` with the loop to get the loop-`else` |

---

### 9. Practice Activities

1. **First multiple.** Using a loop and `break`, find and print the first number between 1 and 100 that is divisible by both 7 and 9.
2. **Skip multiples.** Print the numbers 1 to 20 but skip multiples of 3 using `continue`.
3. **Quit loop.** Write a `while True` loop that asks for numbers and keeps a running total. When the user types `done`, print the total and stop. (Hint: check for `"done"` *before* converting with `int()`.)
4. **Guessing game.** Extend the skeleton from section 2.5: limit the player to 5 attempts; print `Out of attempts` if they fail (the loop `else` or a flag can help).
5. **Break vs continue.** In your own words, predict the output, then run:
   ```python
   for n in range(1, 6):
       if n == 3:
           break
       print(n)
   for n in range(1, 6):
       if n == 3:
           continue
       print(n)
   ```
6. **First failure.** Given `results = "PPPFPPFP"` (P = pass, F = fail), loop over the characters and report the position (starting from 1) of the first failure, then stop. If there are none, say so.
7. **Log scanner.** Modify the log scanner in section 4 to also count `WARNING` lines and to skip lines that start with `#` (comments).
8. **Nested exit.** In a 5×5 grid of `(row, col)` pairs, stop both loops when `row + col == 7` and print where it happened.
9. **Menu.** Write a text menu with options 1 (Say hello), 2 (Show the time of day as the text `"morning"`), 3 (Quit). Loop until option 3 is chosen; handle invalid choices with a message and `continue`.

---

## Summary

- **`break`** ends the loop immediately; execution resumes after the loop.
- **`continue`** skips the rest of the current iteration and moves on to the next one.
- Both normally appear inside an `if` within a loop.
- **`while True` + `break`** is a standard pattern for "repeat until something happens inside the loop".
- In a `while` loop, make sure `continue` doesn't skip your update statement.
- In nested loops, they affect only the **innermost** loop; use a flag to exit several levels.
- A loop's **`else`** block runs only if the loop completed without `break`, useful for "not found" handling.
- Use them to make code clearer, not more tangled. Today's exercise (number guess + log-line scanner) puts all of these to work.

---

## Additional Resources

- Python Tutorial: `break` and `continue` Statements, and `else` Clauses on Loops: https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops
- Python documentation: The `break` statement: https://docs.python.org/3/reference/simple_stmts.html#the-break-statement
- Real Python: Python `while` Loops (includes `break` and `continue`): https://realpython.com/python-while-loop/
