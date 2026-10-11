# Python Environment and Development Setup

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what Python is and why it is the main language used in test automation.
- Describe the difference between source code, an interpreter and an editor.
- Install Python 3 on Windows, macOS or Linux and verify the installation.
- Run Python code in two ways: interactively (the REPL) and from a script file.
- Install and configure Visual Studio Code (VS Code) with the Python extension.
- Create a project folder, write your first script, and run it from both VS Code and the terminal.
- Diagnose the most common setup problems (`python` not found, wrong version, wrong interpreter).

---

## Why This Matters

This week you go from zero to writing and versioning small Python programs. Every other topic in this program, such as writing automated tests, calling APIs, reading test data and using AI tools to generate tests, sits on top of a working Python setup. If your environment is broken, nothing else will run.

**Why Python for a Test Automation Engineer?**

| Reason | What it means for you |
|---|---|
| Readable syntax | Python reads almost like English, so test scripts are easy to review and maintain. |
| Huge ecosystem | Libraries exist for browser testing, API testing, data handling, reporting and AI. |
| Industry demand | Python is one of the most requested languages in QA and SDET job listings. |
| Beginner-friendly | You can write something useful within your first hour. |
| Works everywhere | The same script runs on Windows, macOS and Linux, including on CI servers. |

Think of setting up your environment like setting up a workshop before building furniture. You need the right tools, in the right place, and you need to know they work before you start. Spending an hour on a clean setup today saves many hours of confusing errors later.

---

## The Concept

### 1. What Is Python?

**Python** is a *high-level, general-purpose programming language* created by Guido van Rossum and first released in 1991. Let's unpack those words:

- **Programming language:** a set of rules and words you use to give instructions to a computer.
- **High-level:** it is designed for humans. You write `print("Hello")` instead of dealing with memory addresses and processor instructions.
- **General-purpose:** it is not limited to one job. People use it for web apps, data science, automation, AI, games and testing.

Python is **interpreted**. This is an important idea:

- A *compiled* language (like C) is translated all at once into a machine-code file before it runs.
- An *interpreted* language is read and executed **line by line** by a program called the **interpreter**.

So when we say "install Python", we are really installing the **Python interpreter** (plus its standard library of ready-made tools). The interpreter is the program that reads your `.py` file and carries out your instructions.

```
  You write                 Interpreter reads               Computer does
  ┌────────────┐           ┌──────────────────┐            ┌─────────────┐
  │ hello.py   │  ───────▶ │ python (program) │  ───────▶  │ prints text │
  │ (your code)│           │ translates + runs│            │ on screen   │
  └────────────┘           └──────────────────┘            └─────────────┘
```

### 2. Python 2 vs Python 3

You may see old tutorials mentioning Python 2. **Python 2 is retired** (end of life in 2020). Everything in this program uses **Python 3**. When you install, choose a recent stable Python 3 release (3.11 or newer is a safe choice; 3.12 or 3.13 are fine too).

### 3. The Three Things You Need

Beginners often mix these up, so let's separate them clearly:

| Thing | What it is | Example |
|---|---|---|
| **Interpreter** | The program that runs Python code | `python.exe`, `python3` |
| **Editor / IDE** | The application where you *write* code | VS Code, PyCharm |
| **Terminal** | A text window where you type commands | PowerShell, Terminal, bash |

You can write Python in a plain notepad and run it from a terminal. An editor like VS Code simply makes this far more comfortable by adding colors, hints, error highlighting and a built-in terminal.

---

### 4. Installing Python

#### 4.1 Check whether Python is already installed

Open a terminal:

- **Windows:** press the Windows key, type `PowerShell`, press Enter.
- **macOS:** press `Cmd + Space`, type `Terminal`, press Enter.
- **Linux:** press `Ctrl + Alt + T`.

Then type:

```bash
python --version
```

On macOS and Linux the command is often `python3`:

```bash
python3 --version
```

If you see something like `Python 3.12.4`, Python is installed. If you see an error like "command not found" or "'python' is not recognized", you need to install it. If you see a Python 2 version (such as `Python 2.7.18`), you also need to install Python 3.

> **What is a terminal?** A terminal (also called a command line or shell) lets you control the computer by typing text commands instead of clicking. You will use it every day as a test engineer, for running tests, using Git and more.

#### 4.2 Windows

1. Go to **https://www.python.org/downloads/** and click the download button for the latest Python 3 version.
2. Run the installer.
3. **Very important:** on the first screen, tick the box **"Add python.exe to PATH"** (or "Add Python to PATH"). Then click **Install Now**.
4. When it finishes, close and reopen PowerShell, then run:

```powershell
python --version
```

On Windows you also get the **Python launcher**, so this works too:

```powershell
py --version
```

**What is PATH?** PATH is a list of folders that your computer searches when you type a command. When you type `python`, the computer looks through the PATH folders for a program with that name. If Python's folder is not in the PATH, the computer says "not recognized", even though Python is installed. Ticking the "Add to PATH" box is what prevents this very common beginner problem.

#### 4.3 macOS

Option A (simple): download the macOS installer from python.org and run it.

Option B (common among developers): use Homebrew, a package manager for macOS:

```bash
brew install python
```

After installing, use `python3` (and `pip3`) in the terminal:

```bash
python3 --version
```

#### 4.4 Linux (Ubuntu/Debian)

Most Linux systems already include Python 3. To install or update:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

Verify:

```bash
python3 --version
```

> **Command name summary:** Windows usually `python` (or `py`); macOS/Linux usually `python3`. In this course, when a lesson says `python`, use whichever works on your machine.

---

### 5. Your First Python: The Interactive Shell (REPL)

Python has an interactive mode called the **REPL**, which stands for **R**ead, **E**valuate, **P**rint, **L**oop. It reads one line you type, evaluates it, prints the result, and loops back to wait for more.

Start it by typing `python` (or `python3`) and pressing Enter:

```text
$ python
Python 3.12.4 (main, ...) 
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

The `>>>` is the **prompt**; it means Python is waiting for you. Try some things:

```python
>>> 2 + 3
5
>>> print("Hello, QA world!")
Hello, QA world!
>>> 10 / 4
2.5
```

Notice that typing `2 + 3` immediately shows `5`. The REPL is perfect for experiments: "What does this do?" You type it and see.

To leave the REPL, type `exit()` and press Enter (or press `Ctrl + Z` then Enter on Windows, `Ctrl + D` on macOS/Linux).

**When to use the REPL:** quick experiments and checking how a piece of syntax behaves.
**When not to use it:** anything you want to keep, repeat or share. For that, you write a script file.

---

### 6. Your First Script File

A **script** is a text file containing Python instructions, saved with the extension **`.py`**. Python runs the instructions from top to bottom.

Create a file named `hello.py` with this content:

```python
# My first Python script
print("Hello, Test Automation!")
print("Python is installed and working.")
```

Run it from the terminal, in the same folder as the file:

```bash
python hello.py
```

Output:

```text
Hello, Test Automation!
Python is installed and working.
```

**Understanding the code:**

- `# My first Python script` is a **comment**. Python ignores everything after `#` on that line. Comments are notes for humans.
- `print(...)` is a **built-in function** that displays text on the screen. We will study functions in depth later this week, for now, just treat `print` as "show this on screen".
- `"Hello, Test Automation!"` is a **string**: text wrapped in quotation marks. Strings are covered in the next lesson.

---

### 7. Installing and Setting Up VS Code

**Visual Studio Code (VS Code)** is a free, lightweight, very popular code editor from Microsoft. We use it throughout this program.

#### 7.1 Install VS Code

1. Download from **https://code.visualstudio.com/** and install it (accept the defaults).
2. Open VS Code.

#### 7.2 Install the Python extension

An **extension** adds features to VS Code. The Python extension adds code highlighting, suggestions, error checking, and the ability to run and debug Python.

1. Click the **Extensions** icon in the left sidebar (it looks like four squares), or press `Ctrl + Shift + X` (`Cmd + Shift + X` on macOS).
2. Search for **Python**.
3. Install the one published by **Microsoft**.

#### 7.3 Open a project folder

VS Code works best when you open a **folder** rather than a single file. A folder is your project workspace.

1. Create a folder on your computer, for example `qea-week1`.
2. In VS Code: **File → Open Folder...** and choose it.
3. Click **Yes, I trust the authors** when asked (it is your own folder).

#### 7.4 Create and run a file

1. In the Explorer panel, click the **New File** icon and name the file `hello.py`.
2. Type the code from section 6.
3. Save with `Ctrl + S` (`Cmd + S` on macOS).
4. Click the **▷ Run Python File** button at the top right, **or** open the built-in terminal (**Terminal → New Terminal**) and run `python hello.py`.

#### 7.5 Select the correct interpreter

If you have several Pythons installed, VS Code must know which to use.

1. Press `Ctrl + Shift + P` (`Cmd + Shift + P` on macOS) to open the **Command Palette**.
2. Type **Python: Select Interpreter** and press Enter.
3. Choose the Python 3 version you installed.

You will see the selected interpreter in the bottom-right corner of VS Code. This is a very common fix when something "works in the terminal but not in VS Code".

---

### 8. Python's Most Important Syntax Rule: Indentation

Many languages use curly braces `{ }` to group code. Python uses **indentation** (spaces at the start of a line). This is why Python looks so clean.

You do not need grouping yet, but you must know now that **spaces at the start of a line matter**. This code causes an error:

```python
print("Line one")
    print("Line two")   # unexpected indent!
```

```text
IndentationError: unexpected indent
```

Rule for now: **start every line at the far left unless you are told otherwise.** The convention is **4 spaces** per level, and VS Code inserts them when you press `Tab`. We will use indentation for real in the conditionals and loops lessons tomorrow.

---

### 9. A Quick Note on pip and Virtual Environments

When you install Python you also get **pip**, Python's package installer. It downloads third-party libraries that other people have written:

```bash
pip --version
```

You will use `pip install <package-name>` in later weeks when we bring in testing libraries. A **virtual environment** is an isolated bundle of Python plus packages for one project, so projects do not interfere with each other. We will set one up when we first need external packages; for this week, the standard library is all you need.

---

### 10. Project Organization Best Practices

Even for small practice work, build good habits:

```text
qea-week1/
├── hello.py
├── monday/
│   └── test_case_formatter.py
└── notes.txt
```

- Use **lowercase names with underscores** for Python files: `test_case_formatter.py`, not `Test Case Formatter.py`. Spaces in names cause pain in terminals.
- Do not name your file the same as a Python library (for example, don't call your file `random.py` or `math.py`). Python may import *your* file by mistake.
- Keep one project folder per task or week. Tomorrow's Git lessons build on this: a Git repository is simply a project folder that Git is tracking.

---

### 11. Troubleshooting Guide

| Symptom | Likely cause | Fix |
|---|---|---|
| `'python' is not recognized` (Windows) | Python not on PATH | Reinstall and tick "Add python.exe to PATH", or try `py` |
| `python: command not found` (macOS/Linux) | Command is named `python3` | Use `python3` |
| `Python 2.7...` appears | Old Python is first on PATH | Use `python3`, or fix PATH |
| VS Code run button runs the wrong version | Wrong interpreter selected | Command Palette → *Python: Select Interpreter* |
| `can't open file 'hello.py'` | Terminal is in a different folder | Use `cd folder-name` to move to the file's folder, or `dir` / `ls` to look around |
| `IndentationError` | Stray spaces at the start of a line | Remove the leading spaces |
| `SyntaxError` | Typo such as a missing quote or bracket | Read the line number in the message and check it |

**Reading an error message:** Python errors look scary but are helpful. Read from the **bottom**: the last line says the *type* of error and what went wrong; the lines above show the *file name* and *line number*.

```text
  File "hello.py", line 2
    print("Hello)
          ^
SyntaxError: unterminated string literal (detected at line 2)
```

Here the message tells us line 2 has a string with a missing closing quote.

---

### 12. Practice Activities

1. **Verify your tools.** Run `python --version` (or `python3 --version`) and `pip --version`. Write down the results in a text file.
2. **REPL exploration.** Start the REPL and try `7 * 6`, `100 - 1`, `print("My name is ...")` with your own name. Exit with `exit()`.
3. **Script practice.** Create `about_me.py` that prints three lines: your name, the city you live in, and why you want to become a test automation engineer. Run it.
4. **Break it on purpose.** Remove the closing quote from one print line and read the error. Fix it. Then add a stray space at the start of a line and read the `IndentationError`. Learning to recognize errors is a skill.
5. **Comment practice.** Add a comment above each line explaining what it does.

---

## Summary

- Python is a readable, general-purpose, interpreted language and the most common choice for test automation.
- The **interpreter** runs your code, the **editor** (VS Code) is where you write it, and the **terminal** is where you issue commands.
- Install Python 3 from python.org (tick **Add to PATH** on Windows). Use `python` or `python3` depending on your system.
- The **REPL** is for quick experiments; **`.py` script files** are for anything you want to keep and rerun.
- In VS Code, install Microsoft's **Python extension**, open a **folder**, and make sure the right **interpreter** is selected.
- **Indentation matters** in Python; start lines at the far left for now.
- Read error messages from the bottom up: the type of error, then the file and line number.

---

## Additional Resources

- Python documentation: Using Python on your platform: https://docs.python.org/3/using/index.html
- VS Code: Getting Started with Python: https://code.visualstudio.com/docs/python/python-tutorial
- Real Python: Python 3 Installation & Setup Guide: https://realpython.com/installing-python/
