# Performance Profiling

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what "performance" means in two different senses: the speed of your **test suite** and the speed of the **code under test**.
- Find slow tests using `--durations` and `--durations-min`, and read the output including setup/call/teardown phases.
- Measure code manually with `time.perf_counter()` and Python's `timeit` module.
- Write simple performance assertions (a time budget) and understand why they can be flaky.
- Use `cProfile` and `pstats` to discover *where* time is spent inside a function.
- Apply `pytest-timeout` to stop hung tests, and know that `pytest-benchmark` exists for rigorous micro-benchmarks.
- Use practical techniques to speed up a suite: fixture scopes, mocking slow dependencies, selecting tests, and parallel execution with `pytest-xdist`.
- Avoid common profiling mistakes (premature optimisation, measuring once, measuring import time).

---

## Why This Matters

This week's epic takes you from PyTest basics to a **reporting framework** for Project 1 – QE Foundations. A good framework is not only correct; it is also **fast and observable**.

Consider what happens when a suite takes 40 minutes. Developers stop running it before committing. Bugs are found hours later. Pipelines queue up. The team starts skipping tests "just this once", and quality decays. Test speed is a quality attribute of the framework itself.

Meanwhile, the *product* has performance requirements too: "search must return in under 2 seconds". As a Quality Engineer you are expected to notice when a change makes the product slower, even before specialised load-testing tools get involved.

Today's lesson gives you the first, practical layer of both skills: **measure first, then optimise**. The golden rule of performance work is: *never guess where the time goes; measure it.*

---

## The Concept

### 1. Two meanings of "performance" in testing

| Question | What you measure | Tools in this lesson |
|----------|------------------|----------------------|
| "Why is my **test run** slow?" | Duration of each test, fixture setup, collection | `--durations`, `-v`, `--setup-show`, fixture scopes, `pytest-xdist` |
| "Is the **code under test** fast enough?" | Execution time of a function or operation | `perf_counter`, `timeit`, `cProfile`, `pytest-benchmark` (awareness) |

Keep them separate in your head. The first is about your framework's health, the second about the product's behaviour.

### 2. Finding slow tests with `--durations`

PyTest measures how long each test takes. Ask for the slowest ones:

```bash
pytest --durations=5
```

Sample output:

```
============================ slowest 5 durations ============================
2.01s call     tests/test_slow.py::test_report_generation
1.00s setup    tests/test_slow.py::test_with_database
0.52s call     tests/test_slow.py::test_retry_logic
0.01s call     tests/test_fast.py::test_add
0.00s teardown tests/test_slow.py::test_with_database
```

**Reading it:**

- `--durations=5` shows the 5 slowest *phases*. Use `--durations=0` to show **all** of them.
- Each test has three phases: **setup** (fixtures being created), **call** (the test body), **teardown** (fixtures being cleaned). The output lists the phase separately. A slow `setup` points to a heavy fixture, not to a slow test body.
- By default PyTest hides very short durations (below 0.005 s) unless you add `-vv`.
- `--durations-min=1.0` shows only entries lasting at least 1 second, useful in a big suite: `pytest --durations=0 --durations-min=1.0`.

To make this a habit, add it to `pytest.ini`:

```ini
[pytest]
addopts = -ra --durations=10 --durations-min=0.5
```

Let's create a small file to practise on:

```python
# tests/test_timing_demo.py
import time
import pytest


@pytest.fixture
def slow_resource():
    time.sleep(0.8)          # pretend this connects to a database
    yield "connection"
    time.sleep(0.1)          # pretend cleanup


def test_fast():
    assert 1 + 1 == 2


def test_slow_body():
    time.sleep(1.2)          # pretend heavy computation
    assert True


def test_uses_slow_fixture(slow_resource):
    assert slow_resource == "connection"
```

Run `pytest tests/test_timing_demo.py --durations=0`. You should see: a ~1.2 s `call` for `test_slow_body`, a ~0.8 s `setup` and a ~0.1 s `teardown` for `test_uses_slow_fixture`, and tiny entries for the rest. This tells you exactly where to optimise: shrinking `test_slow_body` is a *code* matter; the fixture cost might be fixed by changing the **scope** (see section 8).

(`time.sleep(seconds)` pauses the program; we use it only to simulate slowness. Real tests should avoid arbitrary sleeps; we will see why in the browser automation lessons later this week.)

### 3. Other helpful run-time diagnostics

| Command | Why use it |
|---------|-----------|
| `pytest -v` | See each test with a pass/fail label as it runs; spot where it "hangs" |
| `pytest --setup-show` | Shows each fixture setup and teardown with its scope; reveals fixtures being recreated too often |
| `pytest --collect-only -q` | Lists tests without running; checks **collection time** |
| `pytest --lf` | Re-run only the last failures for a quick feedback loop |
| `pytest -x` | Stop after the first failure to avoid waiting for the rest |
| `pytest -k "pricing"` / `-m smoke` | Run a subset |

Collection can itself be slow if your modules do heavy work at import time (reading big files, connecting to services). Compare `time pytest --collect-only -q` with the total run. If collection is slow, move heavy work into fixtures.

### 4. Measuring with `time.perf_counter()`

For quick measurement of a block of code, use a **high-resolution clock**:

```python
import time


def measure(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed
```

```python
def build_list(n):
    return [i * i for i in range(n)]


result, seconds = measure(build_list, 1_000_000)
print(f"Built {len(result)} items in {seconds:.4f} s")
```

**Explanation:**

- `time.perf_counter()` returns a float number of seconds from an arbitrary starting point; only the **difference** between two calls is meaningful.
- `*args, **kwargs` lets `measure` pass any arguments through to `func`.
- `1_000_000` is just a readable way to write one million (underscores are ignored).
- `{seconds:.4f}` formats to 4 decimal places.
- Do **not** use `time.time()` for measuring durations; it follows the system clock, which can jump (for example, daylight saving or network time updates). `perf_counter` is monotonic and more precise.

A reusable context manager makes this tidier:

```python
import time
from contextlib import contextmanager


@contextmanager
def stopwatch(label="block"):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"[{label}] {elapsed * 1000:.2f} ms")


with stopwatch("sum of squares"):
    total = sum(i * i for i in range(1_000_000))
```

- `@contextmanager` converts a generator function into something usable with `with`. Code before `yield` runs on entering; code after runs on leaving.
- `try/finally` ensures the time is printed even if the block raises an error.
- To see `print` output from passing tests in PyTest, add `-s` (disable capture) or use the `capsys` fixture.

### 5. Measuring reliably with `timeit`

A single measurement is noisy: the operating system may run another process at that moment. The `timeit` module repeats a statement many times for a more stable measurement.

```python
import timeit

setup = "data = list(range(1000))"

t_loop = timeit.timeit("sum([x * 2 for x in data])", setup=setup, number=10_000)
t_gen = timeit.timeit("sum(x * 2 for x in data)", setup=setup, number=10_000)

print(f"list comprehension: {t_loop:.3f}s for 10,000 runs")
print(f"generator:          {t_gen:.3f}s for 10,000 runs")
```

- `timeit.timeit(stmt, setup, number)` runs `setup` once and `stmt` `number` times, returning the **total** seconds.
- `timeit.repeat(...)` repeats the whole measurement several times; take the **minimum** because noise only ever makes things slower.
- You can also run it from the terminal: `python -m timeit -s "data=list(range(1000))" "sum(x*2 for x in data)"`.

### 6. Performance assertions in tests

A simple "time budget" test makes sure a function does not become dramatically slower:

```python
# tests/test_performance_budget.py
import time
import pytest


def search(items, target):
    return target in items


@pytest.mark.slow
def test_search_stays_within_budget():
    items = list(range(100_000))

    start = time.perf_counter()
    for _ in range(100):
        search(items, 99_999)
    elapsed = time.perf_counter() - start

    assert elapsed < 1.0, f"100 searches took {elapsed:.3f}s; budget is 1.0s"
```

**Design notes:**

- The budget (1.0 s) should be **generous**. Timing tests are among the flakiest tests, because a busy CI machine can make the same code 3x slower. Pick a budget around 5-10 times the typical time and tighten it only if you have to.
- Repeat the operation (`range(100)`) so the measured time is large relative to timer noise.
- Mark them (`slow` or a dedicated `perf` marker) so they can be excluded from the fast run.
- Always include the measured value in the failure message, as taught in *Custom assertions*.
- Prefer **relative** comparisons ("the new approach is not more than 2x slower than the old") over absolute numbers across different machines.
- Real user-facing performance (load, concurrency, response under 1,000 users) is the job of dedicated load-testing tools; unit-level timing assertions are only a first line of defence.

### 7. Profiling: where inside the code is the time going?

Timing says **how long**. A **profiler** says **where**. Python includes `cProfile`, a deterministic profiler that records every function call and how long it took.

First, a deliberately inefficient function:

```python
# slow_report.py
def find_duplicates(values):
    duplicates = []
    for i, a in enumerate(values):
        for j, b in enumerate(values):
            if i != j and a == b and a not in duplicates:
                duplicates.append(a)
    return duplicates


def build_data(n):
    return [i % 500 for i in range(n)]


def main():
    data = build_data(3000)
    return find_duplicates(data)


if __name__ == "__main__":
    main()
```

Profile it from the terminal:

```bash
python -m cProfile -s cumulative slow_report.py
```

- `-s cumulative` sorts by cumulative time (time in a function **including** the functions it calls).
- Output columns: `ncalls` (number of calls), `tottime` (time inside the function itself, excluding sub-calls), `cumtime` (including sub-calls), `percall`, and `filename:lineno(function)`.

Typical output (numbers vary):

```
         9019 function calls in 0.9 seconds

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.9    0.9 slow_report.py:1(<module>)
        1    0.000    0.000    0.9    0.9 slow_report.py:14(main)
        1    0.9      0.9      0.9    0.9 slow_report.py:2(find_duplicates)
        1    0.000    0.000    0.0    0.0 slow_report.py:11(build_data)
```

The evidence is clear: nearly all the time is inside `find_duplicates`. The algorithm is O(n squared) because of the nested loops (and `a not in duplicates` is a linear search on a list).

Profile from inside Python, with `pstats` for tidy output:

```python
import cProfile
import pstats
import io

from slow_report import main

profiler = cProfile.Profile()
profiler.enable()
main()
profiler.disable()

stream = io.StringIO()
stats = pstats.Stats(profiler, stream=stream).sort_stats("cumulative")
stats.print_stats(5)          # top 5 lines
print(stream.getvalue())
```

- `Profile()` creates the profiler; `enable()` / `disable()` bracket the code to measure.
- `pstats.Stats(...)` formats the data; `sort_stats("cumulative")` or `"tottime"` chooses the ordering; `print_stats(5)` limits output to 5 lines.
- Python 3.8+ also supports `with cProfile.Profile() as pr: ...` as a context manager.

Now fix the algorithm and **measure again** (never assume the new version is faster):

```python
from collections import Counter


def find_duplicates_fast(values):
    counts = Counter(values)
    return [value for value, count in counts.items() if count > 1]
```

- `Counter` builds a dictionary of value -> number of occurrences in one pass (O(n)).
- The comprehension picks values seen more than once.
- Add a correctness test comparing the two functions' results (as sets) **before** you celebrate the speedup:

```python
def test_fast_version_matches_slow_version():
    data = build_data(500)
    assert set(find_duplicates(data)) == set(find_duplicates_fast(data))
```

The principle: **optimise only with a profile, and protect the behaviour with a test.**

### 8. Speeding up the test suite

Having found slow spots, here are the common remedies in order of value.

#### 8.1 Use appropriate fixture scopes (Tuesday's lesson, applied)

If an expensive resource is created for every test, widen its scope:

```python
import time
import pytest


@pytest.fixture(scope="session")
def expensive_connection():
    time.sleep(1.0)       # created ONCE for the whole run
    yield "connection"
    time.sleep(0.2)       # closed ONCE at the end
```

Use `pytest --setup-show` to verify the fixture is set up once. **Caution:** a wider scope means state can leak between tests. Share only *read-only* or *reset-able* resources; reset the state in a small function-scoped fixture when needed.

#### 8.2 Mock slow external calls (Tuesday's lesson, applied)

Unit tests should not wait for the network. Replace slow dependencies:

```python
from unittest.mock import patch

import pricing_service   # imagine this calls a remote API


def test_discount_uses_cached_rate():
    with patch.object(pricing_service, "fetch_rate", return_value=0.1):
        assert pricing_service.discounted(100) == 90
```

A test that took 800 ms because of a real HTTP call now takes microseconds, and it no longer fails when the network is down. Keep a *small* number of real integration tests for the true connections, marked `integration`.

#### 8.3 Remove arbitrary sleeps

`time.sleep(5)` "to be safe" costs 5 seconds every run. Replace with condition-based waiting (poll until ready with a timeout). Browser tooling you will learn later this week builds this in automatically; we will cover it in depth on Friday.

#### 8.4 Run less, run smarter

- `pytest -m smoke` for the quick check; the full suite on CI.
- `pytest --lf --ff` focuses on previous failures.
- `pytest -k "pricing and not slow"`.
- Keep tests small and focused; a 100-line test with 12 steps is slow and hard to diagnose.

#### 8.5 Parallel execution with `pytest-xdist`

Independent tests can run on several CPU cores at once. Install the plugin:

```bash
python -m pip install pytest-xdist
pytest -n auto          # one worker per CPU core
pytest -n 4             # exactly four workers
```

- `-n auto` chooses the number of workers automatically.
- Parallel runs **require independent tests**: no shared files, ports, or database rows; no reliance on order. This is another reason to apply the isolation principles from *Test organization and reusable templates*.
- Session-scoped fixtures run **once per worker**, not once overall.
- HTML reports still work with xdist; the plugin merges worker results.
- Typical gain: close to linear for CPU-bound or I/O-bound tests, with diminishing returns beyond the number of physical cores.

### 9. Stopping hung tests with `pytest-timeout`

A test waiting forever on a network or an infinite loop blocks the entire pipeline. Install:

```bash
python -m pip install pytest-timeout
```

Use it globally and per test:

```ini
[pytest]
timeout = 60
```

```python
import time
import pytest


@pytest.mark.timeout(2)
def test_must_finish_quickly():
    time.sleep(5)   # will be stopped after 2 seconds and reported as a failure
```

- `timeout = 60` in `pytest.ini` sets a default limit of 60 seconds per test.
- `@pytest.mark.timeout(2)` overrides it for one test.
- On timeout the test **fails** with a clear message, instead of hanging the pipeline.
- Do not confuse this with a performance assertion: the timeout is a safety net, not a measurement.

### 10. A first look at `pytest-benchmark` (awareness)

For rigorous micro-benchmarks, the `pytest-benchmark` plugin provides a `benchmark` fixture which runs your function many times, computes statistics (min, mean, standard deviation, rounds) and can compare against saved runs.

```bash
python -m pip install pytest-benchmark
```

```python
def test_sum_speed(benchmark):
    result = benchmark(sum, range(10_000))
    assert result == sum(range(10_000))
```

`benchmark(func, *args)` calls the function repeatedly, returns its result, and prints a statistics table at the end. This is more reliable than hand-made timers but optional for Project 1; know it exists and read its documentation if you need to track performance across releases.

### 11. Memory and other resources (brief)

Performance is not only time. The standard-library `tracemalloc` module tracks memory allocations:

```python
import tracemalloc

tracemalloc.start()
data = [str(i) * 10 for i in range(100_000)]
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"current={current / 1024 / 1024:.1f} MB, peak={peak / 1024 / 1024:.1f} MB")
```

- `get_traced_memory()` returns `(current, peak)` in bytes. Dividing by `1024 * 1024` converts to megabytes.
- Memory-growth checks help find leaks in long-running services; for now treat this as awareness.

### 12. A step-by-step profiling workflow

1. **Define the goal.** "The suite should finish in under 5 minutes" or "checkout must complete under 300 ms".
2. **Measure the baseline** (`--durations`, `timeit`). Write the number down.
3. **Find the biggest contributor** (the slowest phase, or the top of the profile).
4. **Change one thing.**
5. **Measure again** under the same conditions. Keep the change only if the number improves meaningfully.
6. **Protect behaviour** with tests. Faster-but-wrong is not an improvement.
7. **Repeat** until the goal is reached, then stop. (Optimisation beyond the goal wastes effort and often reduces readability.)

---

## Real-World Scenarios

1. **Slow nightly pipeline.** Using `--durations=20`, the team discovers that 15 of 20 slowest entries are `setup` phases of a fixture that creates a user via the API for every test. Changing that fixture to session scope with per-test cleanup cuts the run from 45 to 12 minutes.
2. **Regression in a search function.** A release makes search twice as slow. A budget test with a generous threshold fails, a `cProfile` run points to a newly added `sorted()` call inside a loop, and the fix is a one-line move outside the loop.
3. **Hung pipeline.** A test waits for a service that never answers. With `pytest-timeout` the build fails in 60 seconds instead of hanging for the job's two-hour limit.
4. **Browser tests (later this week).** UI tests are naturally slower than unit tests. The tools and discipline above (marking, parallelism, avoiding sleeps) will matter even more; we will cover browser automation in depth on Thursday and Friday.

---

## Common Mistakes

| Mistake | Why it is wrong | Better |
|---------|-----------------|--------|
| Optimising without measuring | You fix the wrong thing | Profile first |
| Measuring once | Noise dominates | Repeat; use `timeit`, take the minimum |
| Using `time.time()` for durations | Not monotonic | `time.perf_counter()` |
| Tight timing assertions (e.g. `< 0.01s`) | Flaky on busy machines | Generous budgets, relative comparisons |
| Profiling with other heavy programs running | Skewed results | Close other applications; compare on the same machine |
| Counting import/collection time as test time | Misleading | Compare `--collect-only` separately |
| Widening fixture scope without thinking about shared state | Tests start to interfere | Reset state, or keep function scope for mutable objects |
| Running parallel (`-n auto`) with non-independent tests | Random failures | Fix isolation first |
| Adding `sleep` to fix flaky tests | Slower suite, still flaky | Wait for a condition |
| Leaving profilers or `print` timing in committed tests | Noise | Remove or turn into proper assertions/markers |

---

## Practice Exercises

### Exercise 1: Find the slow phase

Create `test_timing_demo.py` from section 2 and run `pytest --durations=0`. Answer: which test has the longest `call`? Which has the longest `setup`? Change the fixture to `scope="module"` and add a second test using it. Use `--setup-show` to prove the fixture is created once, and observe how the total time changes.

<details>
<summary>Expected observation</summary>
With module scope the 0.8 s setup and 0.1 s teardown happen once for both tests instead of twice, saving about 0.9 s.
</details>

### Exercise 2: Build a stopwatch test

Write a pytest test for the `stopwatch` context manager from section 4: use `capsys` (a built-in fixture that captures printed output) to check the output matches the pattern `[label] <number> ms`.

<details>
<summary>Solution</summary>

```python
import re
import time
from contextlib import contextmanager


@contextmanager
def stopwatch(label="block"):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"[{label}] {elapsed * 1000:.2f} ms")


def test_stopwatch_prints_label_and_milliseconds(capsys):
    with stopwatch("demo"):
        time.sleep(0.01)

    out = capsys.readouterr().out
    assert re.fullmatch(r"\[demo\] \d+\.\d{2} ms\n", out)
```
</details>

### Exercise 3: Compare two implementations

Use `timeit` to compare `"".join(...)` against repeated `+=` string concatenation for building a string of 20,000 numbers. Record both timings and explain which is faster and why (hint: strings are immutable, so `+=` can copy repeatedly).

### Exercise 4: Profile and improve

Profile `find_duplicates` from section 7 with `cProfile` for n = 3000. Record `tottime` of the function. Implement `find_duplicates_fast`, profile again, and confirm the improvement. Write a test proving both functions return the same set of duplicates.

### Exercise 5: Time budget test

Write a test for a function in your Project 1 utilities that asserts 1,000 calls complete under a generous budget. Mark it `slow`. Run it five times and note the variation. Then make the budget unrealistically tight (for example 1 ms) and observe the failure message to see why you must include the measured value in it.

### Exercise 6: Timeout safety net

Install `pytest-timeout`. Write a test with an infinite loop (`while True: pass`) and mark it with `@pytest.mark.timeout(1)`. Confirm it fails quickly. Then remove the loop. (Warning: without the timeout marker the run would never finish, so be sure the marker is present before running.)

### Exercise 7: Suite speed report for Project 1

Run your complete Project 1 suite with `--durations=10`. Create a short table with the five slowest phases, their cause (fixture, sleep, real I/O, heavy computation) and a proposed remedy for each. Apply one remedy and record the new total time.

---

## Summary

- "Performance" has two meanings: the speed of the **test suite** and the speed of the **code under test**. Measure each with suitable tools.
- `--durations=N` (with `--durations-min`) shows the slowest setup/call/teardown phases; `--setup-show` reveals fixture lifetimes.
- `time.perf_counter()` and `timeit` measure code; repeat and take the minimum for stability.
- Budget tests catch gross regressions but must be generous and informative to avoid flakiness.
- `cProfile`/`pstats` show where time is spent; always measure before and after a change and protect behaviour with tests.
- Speed up suites with right-sized fixture scopes, mocking slow dependencies, removing arbitrary sleeps, selective runs and `pytest-xdist`.
- `pytest-timeout` prevents hung tests; `pytest-benchmark` offers rigorous micro-benchmarking.
- Follow the workflow: goal, baseline, find the biggest cost, change one thing, re-measure, stop when the goal is met.

---

## Additional Resources

- PyTest documentation - Profiling test execution duration (`--durations`): https://docs.pytest.org/en/stable/how-to/usage.html#profiling-test-execution-duration
- Python documentation - The Python Profilers (`cProfile`, `pstats`): https://docs.python.org/3/library/profile.html
- Python documentation - `timeit` module: https://docs.python.org/3/library/timeit.html
