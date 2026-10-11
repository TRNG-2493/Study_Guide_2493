# Logging

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **logging** is, and why it is better than scattering `print()` calls through your code.
- Name and choose between the five standard **log levels**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
- Configure Python's built-in `logging` module quickly with `logging.basicConfig()`, and know its limitations (and the "ignored second call" trap).
- Create named **loggers** with `logging.getLogger(__name__)` and explain the logger hierarchy and propagation.
- Explain the roles of **loggers, handlers, formatters and filters**, and build a logger that writes to both the console and a file at different levels.
- Write useful **log messages**: use lazy `%s` formatting, include context, log exceptions with tracebacks (`logger.exception`), and avoid logging secrets.
- Use `logging` effectively in **test automation**: a per-run log file, step-by-step logs, and attaching logs to failure reports.
- Describe log rotation and configuration with `dictConfig` at an introductory level.

---

## Why This Matters

In the previous lesson you debugged with `print()` and with `pdb`. Those are tools for *you*, sitting at your desk, looking at a failing run right now. But many failures happen when you are **not** watching: an overnight test run, a CI/CD pipeline, a test on a remote machine, a bug a colleague hit yesterday. In those cases the only thing you have is the **record** the program left behind. That record is the **log**.

Logging answers questions after the fact:

- *What* was the program doing when it failed?
- *What values* did it have? (the user, the URL, the test data)
- *When* did it happen, and in what order?
- *How long* did each step take?

For a test automation engineer, logs are a primary source of evidence. A test that reports only "FAILED" is nearly useless. A test that leaves a timeline, such as "opened page; entered user `ann`; clicked Submit; response status 500; body `{...}`", lets anyone diagnose the failure without re-running anything.

This also connects to the weekly epic ("harden your Python"). Hardened code *explains itself*. Tuesday's exceptions tell you *that* something failed; logging tells you *the story leading up to it*. And in the unit-testing lesson that follows today, you will see that tests can even check that the right messages were logged.

Compared with `print()`, the `logging` module gives you:

| Need | `print()` | `logging` |
|---|---|---|
| Turn noisy detail on or off without editing code | No (edit and remove lines) | Yes (change the level) |
| Severity (is this a warning? an error?) | No | Yes (5 levels) |
| Timestamps, module name, line number | Manual | Automatic via a format string |
| Send output to a file, console, network at once | Manual | Handlers |
| Full traceback of a caught exception | Manual | `logger.exception()` |
| Different behaviour for different parts of the app | No | Named, hierarchical loggers |
| Safe to leave in production code | No | Yes |

---

## The Concept

### 1. What is logging?

**Logging** means recording events that happen while a program runs. Each record (a *log record*) usually contains a time, a severity level, the source (which module or component) and a message. Python's standard library provides the `logging` module for this, so there is nothing to install, and almost every Python library and framework you will use later (including test frameworks) uses it too.

**Analogy.** Think of an aircraft's flight recorder ("black box"), or a restaurant's order tickets. Nobody reads them while everything is fine. But when something goes wrong, they let you reconstruct exactly what happened and in what order.

### 2. Log levels

Every log message has a **level** expressing its importance. The module defines five standard levels, from least to most severe, each with a number:

| Level | Number | Use it for | Example |
|---|---|---|---|
| `DEBUG` | 10 | Detailed diagnostic information, normally only wanted while investigating | `Request payload: {...}`; loop variable values |
| `INFO` | 20 | Confirmation that things are working as expected; key milestones | `Test test_login started`; `Loaded 250 rows` |
| `WARNING` | 30 | Something unexpected, or a problem is likely, but the program continues | `Response took 4.2s (limit 2s)`; `Using default timeout` |
| `ERROR` | 40 | A serious problem: an operation failed | `Could not read config file` |
| `CRITICAL` | 50 | A severe error; the program may be unable to continue | `Database connection lost; aborting run` |

A **logger has a threshold level**. Messages *below* the threshold are ignored; messages at or above it are processed. If the threshold is `INFO`, then `INFO`, `WARNING`, `ERROR` and `CRITICAL` are shown and `DEBUG` is dropped. This single setting is how you turn detail up while investigating a problem and back down for normal runs, **without touching the code that writes the messages**.

**The default threshold is `WARNING`.** This surprises beginners: out of the box, `logging.info("...")` prints nothing.

```python
import logging

logging.debug("d")
logging.info("i")
logging.warning("w")
logging.error("e")
logging.critical("c")
```

Output:

```
WARNING:root:w
ERROR:root:e
CRITICAL:root:c
```

Only the last three appear. The default format is `LEVEL:LOGGER_NAME:MESSAGE`, and `root` is the name of the default top-level logger.

### 3. Quick start: `logging.basicConfig()`

`basicConfig` is a one-call setup that is perfect for scripts and small programs. Its important parameters:

| Parameter | Meaning |
|---|---|
| `level` | Threshold: `logging.DEBUG`, `logging.INFO`, ... |
| `format` | A template string for each line (see the table below) |
| `datefmt` | How `%(asctime)s` is displayed |
| `filename` | Write to this file instead of the console |
| `filemode` | `"a"` (append, default) or `"w"` (overwrite) |
| `encoding` | File encoding, e.g. `"utf-8"` |
| `force` | `True` removes and replaces existing configuration (Python 3.8+) |

Example:

```python
# lg3.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

logger.debug("debug msg")
logger.info("user %s logged in", "alice")
logger.warning("slow: %.1fs", 2.5)
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("calc failed")
```

Output (the times will differ):

```
12:48:44 | DEBUG    | __main__ | debug msg
12:48:44 | INFO     | __main__ | user alice logged in
12:48:44 | WARNING  | __main__ | slow: 2.5s
12:48:44 | ERROR    | __main__ | calc failed
Traceback (most recent call last):
  File "lg3.py", line 6, in <module>
    1 / 0
    ~~^~~
ZeroDivisionError: division by zero
```

Line-by-line:

- `level=logging.DEBUG` lowers the threshold so that everything is shown.
- `format=...` is a template; each `%(name)s` placeholder is replaced by a field of the record (see the table below). `%(levelname)-8s` pads the level name to width 8, left-aligned, so columns line up.
- `logging.getLogger(__name__)` creates (or fetches) a logger named after the current module. When the file is run directly `__name__` is `"__main__"` (you learned about this on Monday).
- `logger.info("user %s logged in", "alice")` is the **lazy formatting** style: you pass the template and the arguments separately (explained in section 7).
- `logger.exception("calc failed")` logs at `ERROR` level **and** appends the full traceback. Call it inside an `except` block.

#### Useful format fields

| Placeholder | Meaning |
|---|---|
| `%(asctime)s` | Human-readable time of the event |
| `%(levelname)s` | `DEBUG`, `INFO`, ... |
| `%(name)s` | Logger name (e.g. `qa.api`) |
| `%(message)s` | The message after formatting |
| `%(filename)s`, `%(module)s` | Source file / module |
| `%(funcName)s` | Function that logged |
| `%(lineno)d` | Line number of the log call |
| `%(process)d`, `%(threadName)s` | Process id / thread name (useful with parallel tests) |

#### Trap: `basicConfig` is only effective once

`basicConfig` does nothing if the root logger already has handlers. Calling `logging.warning(...)` (the module-level functions) *before* `basicConfig` automatically sets up a default handler, and your later `basicConfig` call is silently ignored:

```python
import logging

logging.warning("first")
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s")
logging.debug("not shown: basicConfig was ignored")
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s", force=True)
logging.debug("now shown")
```

Output:

```
WARNING:root:first
DEBUG now shown
```

Rules: call `basicConfig` **once, as early as possible**, in your entry point (not in every module). Use `force=True` if you must reconfigure. Library or helper modules should **never** call `basicConfig`; they should just create a logger and log to it, leaving configuration to the application.

### 4. Loggers, handlers, formatters, filters: the architecture

`basicConfig` hides a small machine with four kinds of parts. Understanding them lets you build exactly the logging setup you need.

```
   your code:  logger.info("msg")
                    |
                    v
              +-----------+   level check (is INFO >= logger threshold?)
              |  LOGGER   |-----------------------------------------+
              +-----------+                                         |
                    | creates a LogRecord                           |
                    v                                               |
        +-----------+-----------+                                   |
        |                       |                                   |
   +----v-----+           +-----v----+       each HANDLER has its own level and FORMATTER
   | HANDLER  |           | HANDLER  |
   | console  |           |  file    |
   | INFO+    |           | DEBUG+   |
   +----+-----+           +-----+----+
        | FORMATTER             | FORMATTER
        v                       v
   screen output           test_run.log
```

| Part | Responsibility |
|---|---|
| **Logger** | The object your code calls (`logger.info(...)`). Has a *name* and a *level*. Decides whether a record is created. |
| **LogRecord** | The event itself: message, level, time, module, line number, exception info, etc. |
| **Handler** | Sends records to a destination: `StreamHandler` (console), `FileHandler` (file), `RotatingFileHandler` (file that rolls over), `NullHandler` (discard), and more. Each handler has its **own level**. |
| **Formatter** | Decides what the final text looks like (the format string). Attached to a handler. |
| **Filter** | Optional extra rule to accept or reject records, or to add information (e.g. a test id) to them. |

Because each handler has its own level, you can show only `INFO` and up on the screen while saving full `DEBUG` detail to a file. The logger's level is the *first* gate; the handler's level is a *second* gate.

### 5. Named loggers and the hierarchy

Logger names are dot-separated and form a tree:

```
root
 `-- qa
      |-- qa.api
      `-- qa.db
```

- `logging.getLogger("qa.api")` is a *child* of `logging.getLogger("qa")`, which is a child of the root logger.
- A child with no level of its own **inherits** the effective level from its parent.
- By default records **propagate** upward: after a child's own handlers, the record is passed to the parent's handlers. This is why configuring the root logger once (e.g. via `basicConfig`) is enough for every module's logger.
- Calling `getLogger("qa")` twice returns the *same* object, so you never need to pass loggers around.

The standard idiom at the top of every module is:

```python
import logging

logger = logging.getLogger(__name__)
```

Since `__name__` is the module's dotted path (for example `framework.api.client`), your logs automatically say where they came from, and you can control whole areas at once:

```python
logging.getLogger("framework.api").setLevel(logging.DEBUG)   # verbose for the API layer only
logging.getLogger("urllib3").setLevel(logging.WARNING)       # quieten a noisy third-party library
```

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logging.getLogger("a").setLevel(logging.ERROR)
logging.getLogger("a.b").info("silenced")     # inherits ERROR from "a": dropped
logging.getLogger("a.b").error("shown")       # ERROR:a.b:shown
```

### 6. Building a logger by hand: console plus file

For test frameworks you usually want: short, readable output on screen, and a complete detailed log file saved with the test results.

```python
# lg2.py
import logging
import sys


def build_logger(name="qa", logfile="test_run.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)              # logger lets everything through...
    if logger.handlers:                         # guard: avoid adding handlers twice
        return logger

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
    )

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)              # ...but the console only shows INFO and above
    console.setFormatter(fmt)

    file_handler = logging.FileHandler(logfile, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)        # the file records everything
    file_handler.setFormatter(fmt)

    logger.addHandler(console)
    logger.addHandler(file_handler)
    logger.propagate = False                    # do not also pass records to the root logger
    return logger


log = build_logger()
log.debug("config loaded: %s", {"retries": 3})
log.info("test started")
log.warning("slow response: %.2fs", 3.456)
log.error("assertion failed")

child = logging.getLogger("qa.api")             # child inherits the parent's handlers (propagation)
child.info("child logger")
```

Console output (note: no `DEBUG` line):

```
2026-10-07 12:48:36,251 | INFO     | qa:21 | test started
2026-10-07 12:48:36,251 | WARNING  | qa:22 | slow response: 3.46s
2026-10-07 12:48:36,251 | ERROR    | qa:23 | assertion failed
2026-10-07 12:48:36,251 | INFO     | qa.api:24 | child logger
```

Content of `test_run.log` (has the extra `DEBUG` line):

```
2026-10-07 12:48:36,251 | DEBUG    | qa:20 | config loaded: {'retries': 3}
2026-10-07 12:48:36,251 | INFO     | qa:21 | test started
2026-10-07 12:48:36,251 | WARNING  | qa:22 | slow response: 3.46s
2026-10-07 12:48:36,251 | ERROR    | qa:23 | assertion failed
2026-10-07 12:48:36,251 | INFO     | qa.api:24 | child logger
```

Key points:

- The two gates: `logger.setLevel(DEBUG)` lets everything into the system; `console.setLevel(INFO)` filters what appears on screen.
- `if logger.handlers: return logger` prevents the classic **duplicate-lines bug**: if a function that adds handlers is called twice, every message is printed twice.
- `logger.propagate = False` stops records from also bubbling up to the root logger, which would cause duplicates if the root has its own handler.
- `FileHandler(..., mode="w")` creates a fresh log for each run; `"a"` appends. Using `with`-style closing is handled for you: logging closes handlers at interpreter exit (you can call `logging.shutdown()` explicitly).
- Notice `qa:21` shows the **line number** of the logging call; invaluable when hunting a message.

### 7. Writing good log messages

#### 7.1 Use lazy `%s` formatting, not f-strings, in log calls

```python
logger.info("user %s logged in from %s", username, ip)      # recommended
logger.info(f"user {username} logged in from {ip}")          # works, but less ideal
```

With the first form, the string is only built **if the message will actually be emitted**. If the level is disabled, no work is done. That matters when the argument is expensive to render:

```python
class Big:
    def __repr__(self):
        print("(expensive repr executed)")
        return "Big()"

log.debug("value: %r", Big())   # INFO threshold: DEBUG disabled -> repr is NOT executed
log.info("value: %r", Big())    # prints '(expensive repr executed)' then the INFO line
```

Linters often flag f-strings inside logging calls for this reason. It is a good habit, although for small programs the difference is negligible.

#### 7.2 Include context, not just a vague statement

| Weak | Strong |
|---|---|
| `"error"` | `"Login failed for user=%s status=%s"` |
| `"done"` | `"Loaded %d rows from %s in %.2fs"` |
| `"retrying"` | `"Retry %d/%d for GET %s after %s"` |

Include identifiers (test name, user, order id, URL, status code), counts, durations and values you would want if you had to diagnose the problem from the log alone. Use `%r` for values where whitespace or type matters (just like `repr` when debugging).

#### 7.3 Log exceptions with tracebacks

Inside an `except` block, use `logger.exception("what we were doing")`: it logs at `ERROR` and includes the traceback. Equivalent: `logger.error("...", exc_info=True)`. Do not do this:

```python
except Exception as e:
    logger.error("failed")                   # no reason, no traceback
    print(e)                                 # lost when no one watches the console
```

Preferred pattern, combining Tuesday's exception lessons with logging:

```python
import logging
logger = logging.getLogger(__name__)

def read_config(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        logger.exception("Config file missing: %s", path)
        raise                                  # still let the caller decide what to do
```

Log **or** re-raise, but avoid doing both at every layer, or the same error will appear in the log many times. A common rule: log at the place where the exception is finally *handled*.

#### 7.4 Choose the right level

- `DEBUG`: step details, payloads, variable values. Fine to be chatty.
- `INFO`: the story at a high level: "suite started", "test X passed", "uploaded report".
- `WARNING`: "something is off but we can continue", e.g. a missing optional setting, a retry, slowness.
- `ERROR`: an operation failed (and probably a test failed).
- `CRITICAL`: the whole run is in trouble.

A frequent mistake is logging everything as `INFO` or everything as `ERROR`. Levels exist so readers (and tools) can filter; use them honestly.

#### 7.5 Never log secrets or personal data

Logs are copied around, attached to bug reports and stored in CI systems. Do not log passwords, API keys, tokens, full credit card numbers or personal data. Mask or omit them: `"token=%s"` should be `"token=***"`. This is an important professional habit for test engineers who often handle realistic data.

### 8. Where logs go: files, rotation and configuration files

- **Console (`StreamHandler`)**: defaults to `stderr`; pass `sys.stdout` if you want standard output.
- **File (`FileHandler`)**: persistent record. Always set `encoding="utf-8"`.
- **Rotating file (`logging.handlers.RotatingFileHandler`)**: when the file reaches a size, it is renamed (`app.log.1`) and a new one starts. Prevents unbounded growth on long-running systems. `TimedRotatingFileHandler` rotates by time (e.g. daily).

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
```

For larger projects, handlers, formatters and loggers are described in a dictionary (or YAML/JSON/INI file) and loaded with `logging.config.dictConfig`. A small example:

```python
import logging
import logging.config

config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"std": {"format": "%(levelname)-8s %(name)s: %(message)s"}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "std", "level": "INFO"}
    },
    "loggers": {"qa": {"handlers": ["console"], "level": "DEBUG", "propagate": False}},
}
logging.config.dictConfig(config)

logging.getLogger("qa.api").info("hi")       # INFO     qa.api: hi
logging.getLogger("qa.api").debug("hidden")  # below the handler's INFO level: not shown
```

Keeping configuration in one place lets operators change log levels per environment without changing code.

### 9. Logging versus `print()`: when is `print` still fine?

- `print` is the right tool for a program's **intended output** to the user (a report, a result table, the answer a command-line tool is asked for).
- `logging` is the right tool for **diagnostic information** about what the program is doing.
- Quick throwaway debugging while you are at the keyboard: `print` or `pdb`.
- Anything you might want next week, in CI, or in a bug report: `logging`.

### 10. Logging in test automation

In real test frameworks logging typically looks like this:

1. **One configuration at the start of the run** (in the entry point or test setup): console `INFO`, file `DEBUG`, a log file per run named with a timestamp, e.g. `logs/run_2026-10-07_09-30.log`.
2. **Every module has `logger = logging.getLogger(__name__)`.**
3. **Log the test story.** At `INFO`: test start and end, each major step ("Opening login page", "Submitting credentials"), the final verdict. At `DEBUG`: request and response details, data used, timings.
4. **Log before asserting.** If an assertion fails, the log already contains the actual values that led to it:

   ```python
   logger.info("Checking order total for order %s", order_id)
   logger.debug("expected=%r actual=%r", expected_total, actual_total)
   assert actual_total == expected_total, f"total mismatch: {actual_total!r} != {expected_total!r}"
   ```
5. **Attach the log** to the failure report so that a developer can read the story without re-running.
6. **Keep logs consistent**: one line per event, key=value pairs, so they can be searched with `grep` or a log-analysis tool later.
7. **Parallel runs**: include `%(process)d` or `%(threadName)s` in the format so interleaved lines can be separated.

Python's `unittest` library (next lesson) can even verify logging: `self.assertLogs("qa", level="WARNING")` is a context manager that fails the test if no matching message was logged. You will see it in action when we cover unit testing.

---

## Code Examples

### Example A: Minimal script-level setup

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

def divide(a, b):
    logger.debug("divide(%r, %r)", a, b)       # hidden at INFO level
    if b == 0:
        logger.error("Division by zero requested: a=%r", a)
        return None
    return a / b

logger.info("Starting calculations")
print(divide(10, 2))
print(divide(5, 0))
logger.info("Finished")
```

Output:

```
INFO | Starting calculations
5.0
ERROR | Division by zero requested: a=5
None
INFO | Finished
```

(Change `level=logging.INFO` to `logging.DEBUG` and the `divide(...)` lines appear: the *code did not change*, only the threshold.)

### Example B: A tiny reusable test-run logger

```python
# qa_logging.py
import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logging(log_dir="logs", console_level=logging.INFO):
    """Configure root logging: concise console output, detailed file output."""
    Path(log_dir).mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logfile = Path(log_dir) / f"run_{stamp}.log"

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()                      # make setup safe to call more than once

    fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(console_level)
    console.setFormatter(fmt)

    file_handler = logging.FileHandler(logfile, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    root.addHandler(console)
    root.addHandler(file_handler)
    return logfile


if __name__ == "__main__":
    path = setup_logging()
    log = logging.getLogger("demo")
    log.info("hello")
    log.debug("detail only in the file")
    print("log written to", path)
```

How it works: `Path(log_dir).mkdir(exist_ok=True)` creates the folder if needed (the `pathlib` and file skills from Tuesday); a timestamp in the file name means each run gets its own log; `root.handlers.clear()` prevents duplicate handlers when the function is called again. Every module that uses `logging.getLogger(__name__)` now logs through this one setup.

### Example C: Logging a test's steps and failure evidence

```python
import logging

logger = logging.getLogger("qa.tests")

def check_discount(price, percent, expected):
    logger.info("Test start: discount price=%s percent=%s", price, percent)
    actual = price - price * percent / 100
    logger.debug("expected=%r actual=%r", expected, actual)
    if actual != expected:
        logger.error("MISMATCH expected=%r actual=%r", expected, actual)
        return False
    logger.info("Test passed")
    return True

logging.basicConfig(level=logging.DEBUG, format="%(levelname)-7s %(message)s")
check_discount(15.0, 20, 12.0)
check_discount(15.0, 20, 13.0)
```

Output:

```
INFO    Test start: discount price=15.0 percent=20
DEBUG   expected=12.0 actual=12.0
INFO    Test passed
INFO    Test start: discount price=15.0 percent=20
DEBUG   expected=13.0 actual=12.0
ERROR   MISMATCH expected=13.0 actual=12.0
```

Even without a failing stack trace, the log tells the whole story.

---

## Summary / Key Takeaways

- **Logging** records what a program does while it runs, producing evidence you can read later. It beats `print` because of levels, timestamps, destinations, tracebacks and the ability to switch detail on and off without editing code.
- Five levels: `DEBUG` (10) < `INFO` (20) < `WARNING` (30) < `ERROR` (40) < `CRITICAL` (50). The default threshold is `WARNING`, so `info` and `debug` are hidden until you lower it.
- `logging.basicConfig(level=..., format=..., filename=...)` is the quick setup. Call it **once**, early, in the entry point. It is ignored if logging is already configured (use `force=True` to override).
- Create loggers with `logging.getLogger(__name__)` in each module; names form a hierarchy, children inherit levels and propagate records to their parents.
- The pieces: **logger** (your API and first level gate), **handler** (destination plus second level gate), **formatter** (appearance), **filter** (extra rules).
- Use lazy formatting (`logger.info("x=%s", x)`), include meaningful context, and log exceptions with `logger.exception()` inside `except`.
- Choose levels honestly, and **never log secrets or personal data**.
- In automation, use one setup per run, console `INFO` plus file `DEBUG`, log steps and values before assertions, and attach logs to failure reports.
- Libraries and helper modules create loggers but never configure handlers; the application does the configuration.

---

## Practice Questions and Mini-Exercises

**Q1.** What does this print, and why?

```python
import logging
logging.info("starting")
logging.warning("careful")
```

**Q2.** You set `logging.basicConfig(level=logging.INFO)` but your `logger.debug(...)` lines do not appear. Why, and what is the one-line fix?

**Q3.** Which level would you choose for each? (a) "Loaded 120 test cases from cases.csv" (b) "Response body: {...}" (full payload) (c) "Database connection failed, aborting the run" (d) "Optional setting `timeout` missing, using default 30" (e) "Could not parse row 17, skipping it"

**Q4.** Why is `logger.info("user %s", name)` preferred over `logger.info(f"user {name}")`?

**Q5.** A teammate's output shows every log line **twice**. Name two probable causes and fixes.

**Q6.** What is the difference between `logger.error("failed")` and `logger.exception("failed")` inside an `except` block?

**Q7 (mini-exercise).** Write a script that logs to a file `app.log` (mode `"w"`) at `DEBUG` level using the format `LEVEL - message`, logs one message at each of the five levels, then reads and prints the file.

**Q8 (mini-exercise).** Extend `build_logger` from this lesson so that the console shows only `WARNING` and above while the file records everything. Prove it with one message of each level.

**Q9 (mini-exercise).** Write a function `parse_age(text)` that returns an `int`. On invalid text it should log a `WARNING` that includes the offending value (use `%r`) and return `None`. Test it with `"42"`, `"4x"` and `None`.

**Q10.** Why should a reusable helper module avoid calling `logging.basicConfig()`?

### Answers

**A1.** Only `WARNING:root:careful`. The default threshold is `WARNING`, so the `INFO` message is dropped. The first call to a module-level logging function auto-configures the root logger with default settings.

**A2.** `basicConfig(level=INFO)` sets the threshold to `INFO`, which is *above* `DEBUG`, so debug messages are filtered out. Fix: `level=logging.DEBUG`.

**A3.** (a) `INFO`. (b) `DEBUG`. (c) `CRITICAL` (or `ERROR` if the run can continue other work). (d) `WARNING`. (e) `WARNING` (the run continues but data was lost); `ERROR` is also defensible if skipping rows invalidates the result. The key skill is justifying the choice.

**A4.** The `%s` form defers formatting: the message string is built only if the record will actually be emitted, saving work for disabled levels. It also keeps the message template constant, which helps log-analysis tools group similar messages.

**A5.** (1) Handlers were added more than once (a setup function was called repeatedly). Fix: check `if logger.handlers:` or clear handlers before adding. (2) The logger has its own handler **and** propagates to a root logger that also has a handler. Fix: `logger.propagate = False`, or configure only the root logger.

**A6.** `logger.error("failed")` records only the message. `logger.exception("failed")` records it at `ERROR` level **and** appends the current exception's full traceback. Use `exception` in `except` blocks.

**A7.**

```python
import logging

logging.basicConfig(filename="app.log", filemode="w", level=logging.DEBUG,
                    format="%(levelname)s - %(message)s", encoding="utf-8")
log = logging.getLogger("demo")
log.debug("debug"); log.info("info"); log.warning("warning")
log.error("error"); log.critical("critical")
logging.shutdown()                      # flush and close the file
print(open("app.log", encoding="utf-8").read())
```

Output:

```
DEBUG - debug
INFO - info
WARNING - warning
ERROR - error
CRITICAL - critical
```

**A8.** Change `console.setLevel(logging.INFO)` to `console.setLevel(logging.WARNING)`. Logging one message at each level shows only warning, error and critical on screen, while `test_run.log` holds all five.

**A9.**

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def parse_age(text):
    try:
        return int(text)
    except (ValueError, TypeError):
        logger.warning("Invalid age value: %r", text)
        return None

print(parse_age("42"))   # 42
print(parse_age("4x"))   # WARNING: Invalid age value: '4x'  then None
print(parse_age(None))   # WARNING: Invalid age value: None  then None
```

**A10.** `basicConfig` configures the whole application's root logger. If a helper module did that on import it could override or conflict with the application's chosen settings (and it silently does nothing if already configured, creating order-dependent behaviour). Configuration belongs to the application entry point; libraries only create and use their own named logger.

---

## Additional Resources

- Python Standard Library, `logging` module reference: https://docs.python.org/3/library/logging.html
- Python HOWTO, "Logging HOWTO" (basic and advanced tutorials): https://docs.python.org/3/howto/logging.html
- Python HOWTO, "Logging Cookbook" (practical recipes, multiple handlers, rotation): https://docs.python.org/3/howto/logging-cookbook.html
