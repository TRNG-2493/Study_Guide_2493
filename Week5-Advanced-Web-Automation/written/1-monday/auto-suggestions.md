# Auto-Suggestions

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an auto-suggestion (autocomplete, typeahead, search-as-you-type) widget is, and describe the sequence of events that makes it work: key events, a possible debounce delay, a data lookup, and a rendered list of options.
- Explain **why `fill()` often fails** on these widgets and why `press_sequentially()` is the correct tool.
- Wait for suggestions reliably using Playwright's auto-retrying assertions instead of fixed sleeps.
- Select a suggestion with the mouse (`click`) and with the keyboard (`ArrowDown`, `Enter`).
- Assert on the **content, count, order and highlighting** of suggestions, and test the "no results" and "minimum characters" behaviours.
- Deal with the classic timing problems: a list that refreshes while you are interacting with it, slow server responses, and overlapping typing.
- Work with accessible (ARIA) combobox markup using `get_by_role("combobox")`, `get_by_role("listbox")` and `get_by_role("option")`.
- Build a small reusable helper to select a suggestion in any such widget.

---

## Why This Matters

The Week 5 epic is about mastering complex UI interactions. Auto-suggestion boxes may be the most interaction-dense small component on the web. A single search field combines keyboard events, timing (debounce and network latency), a dynamically changing list, mouse selection, keyboard navigation and accessibility attributes, all in a few square centimetres. It appears everywhere: search engines, e-commerce product search, address entry in checkout forms, city pickers on travel sites, "assign to user" fields in project tools, tag inputs.

The same component is a favourite source of flaky tests. A beginner writes `fill("Py")` followed by `click("Python")`, and the test works on Monday, fails on Tuesday and passes again on Wednesday. The cause is almost always one of three things: the widget needs real key events (so `fill` never triggered it), the test clicked before the list was ready, or the test clicked an option from a *previous* version of the list that was about to be replaced. Understanding how these widgets work lets you write tests that are stable by design.

In **Project 1: QE Foundations**, your UI milestone is a complex form flow. Address lookups, product pickers and search boxes are exactly the sort of fields that make a form "complex", so this lesson directly supports that deliverable. It also builds on the previous lessons today: typing (keyboard), clicking options (mouse), custom dropdowns (very closely related) and verifying content with `expect`.

---

## The Concept

### 1. What is an auto-suggestion widget?

An **auto-suggestion** (also called **autocomplete**, **typeahead**, or **search-as-you-type**) widget is a text field that shows a list of possible completions as the user types. The user may then pick one of the suggestions instead of typing the entire value.

There are a few flavours:

| Flavour | What happens | Example |
|---|---|---|
| **Static filter** | Options already live in the page (or a JavaScript array); typing filters them locally | A "country" field with 200 entries |
| **Server-driven** | Each keystroke (or pause) sends a request; the server returns matching suggestions | Search engine, product search |
| **Free text with hints** | You can submit anything; suggestions are just help | Search box with history |
| **Strict selection** | You must pick from the list; typed text alone is invalid | Address picker, "assign to" user field |

Because the exact behaviour varies, **a good test starts by finding out which kind it is** (try it manually, then inspect it with the browser's DevTools).

**An analogy.** Imagine asking a librarian for a book. As you say the first letters of the title, the librarian starts holding up books that match. When you say more letters, the librarian puts down some books and picks up different ones. You can point at a book you want (mouse click) or say "the second one" (keyboard). The librarian might take a moment to fetch the books (network delay), and might wait until you pause speaking before reacting (debounce). If you grab a book at the exact moment the librarian is swapping them, you might end up with the wrong one. That last sentence is the heart of the testing problem.

### 2. How it works under the hood

Understanding the steps explains every testing technique that follows.

1. **The user presses a key.** The browser fires `keydown`, `keypress`/`beforeinput`, `input`, and `keyup` events on the text field.
2. **The page's JavaScript listens** to one of those events. Many widgets listen to `input`; some, particularly older ones, listen to `keyup`.
3. **Debounce (optional).** To avoid sending a request on every keystroke, many widgets wait a short time (for example 250-500 ms) after the *last* keystroke before doing anything. If another key arrives during the wait, the timer restarts. This is called **debouncing**.
4. **Lookup.** The widget filters local data or sends a request (e.g. `GET /suggest?q=py`) and waits for the response. This takes an unpredictable amount of time.
5. **Render.** The widget replaces the content of a list element with the matching options and makes the list visible. Often this is the same list element with *new children* each time: the old options are removed from the DOM and new ones inserted.
6. **Selection.** The user clicks an option, or uses ArrowDown/ArrowUp to move a highlight and presses Enter. The widget writes the chosen text (or id) into the field, closes the list, and may trigger further behaviour (e.g. load the address details).

Each of these steps matters to the test:

- Step 2 means `fill()` may never trigger the widget.
- Steps 3 and 4 mean the list will not be there instantly, so we must wait for the right content.
- Step 5 means a reference to an option can become **stale**, because the element you found may be removed from the page a moment later.
- Step 6 means there are two selection paths (mouse and keyboard) and both deserve tests.

### 3. Why `fill()` often fails here

Recall from the keyboard lesson:

- `locator.fill("Py")` sets the field's whole value in one go, then fires **one** `input` event (and no `keydown` or `keyup` events).
- `locator.press_sequentially("Py")` presses `P`, then `y`, firing the full sequence of events for each character, as a real user does.

If the widget listens to `input`, `fill` may be enough. If it listens to `keyup` or `keydown` (common in older code and many jQuery-style plugins), `fill` produces no suggestions at all, and your test will wait for a list that never comes. Some widgets also behave differently depending on whether the text arrived by typing or by paste.

**The safe default for autosuggest is `press_sequentially`**, because it is the closest imitation of what a user does. Use `delay=` to slow down when the widget is slow or sensitive to fast typing:

```python
search.press_sequentially("Pyth", delay=80)
```

A delay of 50-120 ms per character is realistic and often enough to stabilise a debounced widget. The `delay` is a property of *typing speed*, not a wait for the list. You still need a proper wait for the list (next section).

> **Terminology reminder.** In older Playwright tutorials, `press_sequentially` is called `type()`. The old name is deprecated; always use `press_sequentially`.

If the field already contains text, remember that `press_sequentially` *appends*. Clear it first with `locator.clear()` (or `fill("")`) when you need a clean start.

### 4. Waiting for suggestions: wait for **content**, not for **time**

The most important rule of this lesson:

> Do not wait for a *number of seconds*. Wait for the *condition you care about*.

Playwright's `expect(...)` assertions retry automatically (by default for 5 seconds) until the condition becomes true. Use this to wait for suggestions:

```python
options = page.get_by_role("option")
expect(options).to_have_text(["Python", "PyPy"])     # waits until EXACTLY these appear
```

This one line waits for the debounce, the network and the render, and also verifies the contents, order and count of the list. If it never becomes true, the failure message shows what the list actually contained, which is excellent for debugging.

Choose the waiting condition carefully:

| Condition | Meaning | Risk |
|---|---|---|
| `expect(listbox).to_be_visible()` | A list is showing | May be showing the *previous* term's list (stale) |
| `expect(options).to_have_count(2)` | Two options exist | Another term might also give two options |
| `expect(options).to_have_text([...])` | The list is exactly this | **Most reliable**; waits for the right content |
| `expect(options.first).to_contain_text("Py")` | First option relates to the typed text | Good when you do not know the whole list |

When you do not know the full list (a real server returns a changing list), wait for something that proves the list corresponds to *your* input, such as the first option containing your term, and then click the specific option you want:

```python
expect(options.first).to_contain_text("Pyth")
page.get_by_role("option", name="Python", exact=True).click()
```

### 5. The stale list problem (and why `expect` solves most of it)

Suppose you type "P", "y", "t", "h" with a 50 ms delay and a widget that updates its list with each debounced keystroke (say, 100 ms after the last key). While typing, the list may show results for "P", then for "Py", then for "Pyth", each replacing the previous. If you click an option *before* the final list is rendered, one of two bad things can happen:

1. You click an option from an intermediate list that is replaced a moment later; the click may land on an element that has just been detached from the DOM.
2. You click an option that exists in the intermediate list and in the final list, so the test passes by luck sometimes and fails at other times.

The cure is to wait for the *final* state before clicking: assert the expected list (or at least that the first option contains the full typed term). Playwright's locator actions also re-resolve the locator at the moment of the action, so `page.get_by_role("option", name="Python").click()` re-finds the element each time rather than holding on to an old reference. Never store `ElementHandle` objects from a suggestion list; use locators.

### 6. Selecting a suggestion with the mouse

```python
page.get_by_role("option", name="Python").click()
```

`click()` waits for the element to be visible and stable, scrolls it into view (lists can be scrollable), clicks, and returns.

A subtle difference: some widgets select on **`mousedown`** rather than `click`, because the input's `blur` event (which closes the list) would otherwise fire before `click`. Playwright's `click()` generates the whole sequence (`mousedown`, `mouseup`, `click`) so both styles work.

How do you choose which option? Several approaches:

```python
# By exact text
page.get_by_role("option", name="Python", exact=True).click()

# By partial text, using a filter (works even if the text has highlighted parts)
page.get_by_role("option").filter(has_text="Script").first.click()

# The Nth option
page.get_by_role("option").nth(2).click()

# Using a regular expression
import re
page.get_by_role("option", name=re.compile(r"^Java")).first.click()
```

Many widgets *highlight* the matching part of each option by wrapping it in `<b>` or `<mark>`: `<li><b>Py</b>thon</li>`. The element's **text content** is still `Python`, and its accessible name is usually `Python`, so locators by text still work. Do not select on the HTML structure of the highlight (`li > b`), which is an implementation detail that changes.

### 7. Selecting with the keyboard

A well-built widget supports the keyboard: **ArrowDown** moves the highlight down, **ArrowUp** up, **Enter** selects the highlighted item, **Escape** closes the list. This is a requirement for users who cannot use a mouse, so it needs its own tests.

```python
box.press_sequentially("Py")
expect(options).to_have_text(["Python", "PyPy"])
box.press("ArrowDown")
box.press("ArrowDown")
box.press("Enter")
```

Accessible widgets mark the highlighted option with `aria-selected="true"`, and Playwright can find it with `get_by_role("option", selected=True)`:

```python
expect(page.get_by_role("option", selected=True)).to_have_text("PyPy")
```

If the widget lacks ARIA attributes, assert on whatever visual state it uses, e.g. a CSS class: `expect(page.locator("li.active")).to_have_text("PyPy")`.

**Note that `press_sequentially` followed by `press("ArrowDown")` assumes focus is still in the field**, which it is, since `locator.press` focuses the element first.

### 8. Accessibility roles make locators easy

The WAI-ARIA "combobox" pattern defines a standard way to mark up autosuggest widgets. When developers follow it, you get a clean set of locators:

| Part | Role | Typical locator |
|---|---|---|
| Text field | `combobox` | `page.get_by_role("combobox", name="Language")` |
| The popup list | `listbox` | `page.get_by_role("listbox")` |
| Each suggestion | `option` | `page.get_by_role("option", name="Python")` |
| Highlighted suggestion | `option` with `aria-selected="true"` | `page.get_by_role("option", selected=True)` |
| Open/closed state | attribute `aria-expanded` | `expect(box).to_have_attribute("aria-expanded", "true")` |

If a site does not follow the pattern, fall back to CSS or test-id locators. When you control the app (as QEs often can by requesting changes), ask developers to add `data-testid` or proper ARIA roles; it benefits users of assistive technology and your tests simultaneously.

### 9. What to test about an autosuggest feature

A single "type, click, done" test is only one of many that a thorough QE writes. Consider this list:

1. **Happy path:** type a term, suggestions appear, choose one by mouse, the field holds the chosen value.
2. **Keyboard path:** the same, with arrows and Enter.
3. **Content:** suggestions match the typed prefix (or substring); the order is as specified (e.g. most popular first); the maximum number is respected (e.g. at most 10).
4. **Minimum characters:** typing one character does nothing if the rule is "two or more".
5. **No results:** an unmatched term shows "No results" (or nothing), and does not crash.
6. **Case-insensitivity:** `py` and `PY` give the same results.
7. **Special characters:** `O'Brien`, accents, emoji, SQL-like or HTML-like input. (The list must not break or execute anything.)
8. **Clearing:** selecting all text and deleting closes the list.
9. **Escape:** closes the list and keeps the typed text.
10. **Click outside:** closes the list.
11. **Strict selection:** typing a value that is not in the list and leaving the field produces a validation message.
12. **Downstream effects:** choosing a suggestion fills related fields (city fills state and ZIP).
13. **Slow responses:** the widget tolerates a delayed server reply without showing outdated results (this is an advanced scenario; later in the programme you will learn to simulate slow networks).

### 10. Where does the "wait for the network" fit in?

Playwright can also wait for a specific network response using `page.expect_response(...)`. For example, to wait for the suggestion request before asserting. This is occasionally useful, but beginners should *start* with waiting on the UI (`expect(options)...`) because that is what the user sees and it works regardless of how the data is fetched. Direct network handling and mocking are topics for later in the course, so for today we stay with UI-level waits.

---

## Code Examples

To make the examples deterministic (no reliance on a third-party server that may change), we first define a **small local autosuggest widget** as an HTML string and load it with `page.set_content()`. It behaves like a typical widget: it listens to `keyup` (so `fill` will not work), debounces by 250 ms, requires at least two characters, supports mouse and keyboard selection, and marks up accessibility roles.

### The widget used in the examples

```python
SUGGEST_HTML = """
<label for="q">Language</label>
<input id="q" role="combobox" aria-autocomplete="list" aria-expanded="false"
       aria-controls="list" autocomplete="off">
<ul id="list" role="listbox" hidden></ul>
<p id="chosen"></p>

<script>
  const DATA = ["Python", "PyPy", "Perl", "PHP", "Java", "JavaScript", "Julia",
                "Go", "Rust", "Ruby", "SQL", "Swift"];
  const q = document.getElementById('q');
  const list = document.getElementById('list');
  const chosen = document.getElementById('chosen');
  let timer = null, items = [], active = -1;

  function close() {
    list.hidden = true;
    q.setAttribute('aria-expanded', 'false');
  }
  function choose(text) {
    q.value = text;
    chosen.textContent = 'Selected: ' + text;
    close();
  }
  function highlight(i) {
    active = i;
    [...list.children].forEach((li, idx) =>
      li.setAttribute('aria-selected', String(idx === active)));
  }
  function render() {
    list.innerHTML = '';
    active = -1;
    items.forEach(text => {
      const li = document.createElement('li');
      li.setAttribute('role', 'option');
      li.setAttribute('aria-selected', 'false');
      li.textContent = text;
      li.addEventListener('click', () => choose(text));
      list.appendChild(li);
    });
    if (items.length === 0) {
      const li = document.createElement('li');
      li.textContent = 'No results';
      list.appendChild(li);
    }
    list.hidden = false;
    q.setAttribute('aria-expanded', 'true');
  }

  q.addEventListener('keyup', e => {
    if (['ArrowDown', 'ArrowUp', 'Enter', 'Escape', 'Tab'].includes(e.key)) return;
    clearTimeout(timer);
    const term = q.value.trim().toLowerCase();
    if (term.length < 2) { close(); return; }
    timer = setTimeout(() => {          // debounce: 250 ms after the last key
      items = DATA.filter(d => d.toLowerCase().startsWith(term));
      render();
    }, 250);
  });

  q.addEventListener('keydown', e => {
    const n = items.length;
    if (e.key === 'ArrowDown' && !list.hidden && n) { highlight(Math.min(active + 1, n - 1)); e.preventDefault(); }
    if (e.key === 'ArrowUp'   && !list.hidden && n) { highlight(Math.max(active - 1, 0)); e.preventDefault(); }
    if (e.key === 'Enter' && active >= 0) { choose(items[active]); e.preventDefault(); }
    if (e.key === 'Escape') { close(); }
  });
</script>
"""
```

You do not need to understand every line of the JavaScript; focus on the behaviour in the comments. Key facts: the list is **rebuilt completely** on each lookup (old `<li>` elements are discarded), a "No results" row (which is *not* an `role="option"`) appears when nothing matches, and the search is "starts with", case-insensitive.

Next, a tiny helper to open the page, so each test begins the same way:

```python
from playwright.sync_api import Page, expect


def open_widget(page: Page):
    page.set_content(SUGGEST_HTML)
    return page.get_by_role("combobox", name="Language")
```

**Explanation:** `open_widget` loads the page and returns the locator for the text field (the combobox). Its accessible name "Language" comes from the associated `<label>`. Returning the locator keeps the tests short. (On Wednesday you will learn a more structured way to package such page-specific code; for now a plain function is perfect.)

### Example 1: The classic happy path

```python
def test_select_suggestion_with_mouse(page: Page):
    box = open_widget(page)

    box.press_sequentially("Py", delay=80)

    options = page.get_by_role("option")
    expect(options).to_have_text(["Python", "PyPy"])

    page.get_by_role("option", name="Python", exact=True).click()

    expect(box).to_have_value("Python")
    expect(page.locator("#chosen")).to_have_text("Selected: Python")
    expect(page.get_by_role("listbox")).to_be_hidden()
```

**Line by line**

1. `box = open_widget(page)`: loads the widget and gets the field.
2. `box.press_sequentially("Py", delay=80)`: focuses the field and types `P` then `y`, waiting 80 ms between keys. Each key fires `keyup`, which is exactly what our widget listens for. After the last key the widget starts its 250 ms debounce timer.
3. `options = page.get_by_role("option")`: a locator for every element with role `option`. Nothing is searched yet.
4. `expect(options).to_have_text(["Python", "PyPy"])`: the wait. The assertion retries until the list of options is **exactly** `["Python", "PyPy"]`. This covers the debounce delay, the rendering and the verification of content and order, in one line.
5. `page.get_by_role("option", name="Python", exact=True).click()`: clicks the option whose accessible name is exactly "Python". `exact=True` prevents a partial match with longer names (for example if "Python 3" existed).
6. The three `expect` lines verify the outcome from three angles: the field value, the page's confirmation text, and the list closing. Each retries automatically.

### Example 2: Why `fill()` fails here (and what to learn from it)

```python
def test_fill_does_not_trigger_keyup_widgets(page: Page):
    box = open_widget(page)

    box.fill("Py")                                    # sets value, fires 'input' only
    page.wait_for_timeout(600)                        # ONLY for this demonstration
    expect(page.get_by_role("listbox")).to_be_hidden()

    box.press_sequentially("t", delay=50)            # a real key event: keyup fires
    expect(page.get_by_role("option")).to_have_text(["Python"])
```

**Explanation**

- `box.fill("Py")` puts the text in the field but the widget listens for `keyup`; no suggestions appear. We pause 600 ms (more than the 250 ms debounce) to prove nothing arrives. **This `wait_for_timeout` is only for teaching; never use fixed waits in real tests.** It is acceptable here because we are proving that something does *not* happen, which `expect` cannot do without a bounded time.
- `press_sequentially("t")` then types one real character. The field now contains "Pyt" and the keyup triggers the lookup. The list shows only "Python".
- In real projects, if suggestions "never appear", check this first: switch from `fill` to `press_sequentially`.

### Example 3: Selecting with the keyboard

```python
def test_select_suggestion_with_keyboard(page: Page):
    box = open_widget(page)

    box.press_sequentially("Ja", delay=80)
    expect(page.get_by_role("option")).to_have_text(["Java", "JavaScript"])

    box.press("ArrowDown")
    expect(page.get_by_role("option", selected=True)).to_have_text("Java")

    box.press("ArrowDown")
    expect(page.get_by_role("option", selected=True)).to_have_text("JavaScript")

    box.press("Enter")

    expect(box).to_have_value("JavaScript")
    expect(page.locator("#chosen")).to_have_text("Selected: JavaScript")
```

**Explanation**

- After the list is ready, `box.press("ArrowDown")` moves the highlight to the first option. The widget sets `aria-selected="true"` on it, and `get_by_role("option", selected=True)` finds it. Asserting at each step verifies the *navigation*, not just the final result.
- A second `ArrowDown` moves to "JavaScript".
- `box.press("Enter")` chooses the highlighted option. The assertions confirm the field and the confirmation text.
- Note that we never used the mouse; this is a keyboard-accessibility test.

### Example 4: Minimum characters, no results and case-insensitivity

```python
import pytest


def test_minimum_characters(page: Page):
    box = open_widget(page)

    box.press_sequentially("P", delay=80)
    # Wait briefly in a *condition-based* way: the listbox must stay hidden
    expect(page.get_by_role("listbox")).to_be_hidden()

    box.press_sequentially("y", delay=80)
    expect(page.get_by_role("listbox")).to_be_visible()


def test_no_results(page: Page):
    box = open_widget(page)

    box.press_sequentially("zzz", delay=50)

    expect(page.get_by_role("listbox")).to_contain_text("No results")
    expect(page.get_by_role("option")).to_have_count(0)


@pytest.mark.parametrize("typed", ["py", "PY", "Py", "pY"])
def test_case_insensitive(page: Page, typed: str):
    box = open_widget(page)

    box.press_sequentially(typed, delay=50)

    expect(page.get_by_role("option")).to_have_text(["Python", "PyPy"])
```

**Explanation**

- In `test_minimum_characters` we assert that the list is hidden after one character. Note a limitation: `to_be_hidden()` passes immediately because the list is hidden from the start, so this assertion by itself cannot prove that the widget *refused* to open; it only proves that it is hidden *now*. The second half is the stronger evidence: after the second character, the list becomes visible. For a stricter check of "nothing happens after one character" you may briefly observe for a fixed time, as in Example 2, with a comment explaining why.
- `test_no_results` types a term with no matches. Our widget shows a "No results" row, which is not a `role="option"`, so `to_have_count(0)` for options is true while the listbox contains the message text.
- `test_case_insensitive` uses `parametrize` to run the same scenario with four spellings. All must produce the same list.

### Example 5: Typing, correcting and the list refreshing

```python
def test_list_updates_as_user_refines_term(page: Page):
    box = open_widget(page)

    box.press_sequentially("J", delay=60)
    box.press_sequentially("a", delay=60)
    expect(page.get_by_role("option")).to_have_text(["Java", "JavaScript"])

    box.press_sequentially("vas", delay=60)           # now "Javas"
    expect(page.get_by_role("option")).to_have_text(["JavaScript"])

    box.press("Backspace")
    box.press("Backspace")                            # back to "Jav"
    expect(page.get_by_role("option")).to_have_text(["Java", "JavaScript"])
```

**Explanation:** The list is rebuilt after each (debounced) change. Because every `expect` waits for the *exact* expected list, the test cannot accidentally act on a stale list. `press("Backspace")` is a real key press, which fires `keyup` and therefore re-triggers the lookup. This pattern (type, assert, refine, assert) is the best way to test that a search narrows and widens correctly.

### Example 6: A reusable helper that works for most widgets

```python
import re
from playwright.sync_api import Locator, Page, expect


def choose_suggestion(page: Page, field: Locator, typed: str, option_text: str, delay: int = 80):
    """Type `typed` into `field` and click the suggestion whose text is `option_text`."""
    field.clear()
    field.press_sequentially(typed, delay=delay)

    # Wait until the list reflects THIS input: some option mentions what we typed
    first = page.get_by_role("option").first
    expect(first).to_contain_text(re.compile(re.escape(typed), re.IGNORECASE))

    page.get_by_role("option", name=option_text, exact=True).click()
    expect(field).to_have_value(option_text)


def test_helper(page: Page):
    box = open_widget(page)
    choose_suggestion(page, box, "ru", "Rust")
    expect(page.locator("#chosen")).to_have_text("Selected: Rust")
```

**Line by line**

1. `def choose_suggestion(page, field, typed, option_text, delay=80)`: a function with a default argument `delay`. Type hints document the expected types; `Locator` is the type of a Playwright locator.
2. `field.clear()`: empties the field so repeated use does not append to old text.
3. `field.press_sequentially(typed, delay=delay)`: realistic typing.
4. `first = page.get_by_role("option").first`: the first option in the list. `.first` is a locator property (no parentheses).
5. `re.compile(re.escape(typed), re.IGNORECASE)`: builds a regular expression from the typed text. `re.escape` neutralises special characters (such as `.` or `(`), so they are matched literally; `re.IGNORECASE` ignores case. `to_contain_text` accepts a compiled regex.
6. This `expect` is the "wait for the right list" step. It proves the list is for our term, so the next click cannot hit a stale option.
7. The `click` selects the exact option, and the final `expect` verifies the field's value.
8. `test_helper` shows how short a test becomes once the helper exists. Be aware that the helper assumes the widget shows options that *contain* the typed text; for widgets that show different texts (for example matching in a description), adapt the waiting condition.

### Example 7: A pattern for real-world sites (illustration)

On a real site, such as a search box on a public website, the pattern is the same. The following is an **illustration**; real sites change their markup frequently, so inspect the page with DevTools (or Playwright's `codegen` and inspector tools) and adjust the locators:

```python
import re


def test_site_search_suggestions(page: Page):
    page.goto("https://en.wikipedia.org/wiki/Main_Page")

    search = page.get_by_role("searchbox", name="Search Wikipedia")
    search.press_sequentially("Playwright", delay=100)

    suggestions = page.get_by_role("option")
    expect(suggestions.first).to_be_visible()
    expect(suggestions.first).to_contain_text("Playwright")

    search.press("ArrowDown")
    search.press("Enter")
    expect(page).to_have_url(re.compile(r"wikipedia\.org/wiki/"))
```

**Explanation:** same recipe: find the input by role and name, type with `press_sequentially`, wait for the first suggestion to be visible and relevant, choose by keyboard, and verify the navigation. Treat this as a template rather than a guaranteed script: third-party sites can change at any time, and examples that rely on them are not suitable for production test suites. For production, prefer applications you control or dedicated test environments.

---

## Real-World Scenarios

**Scenario 1: Address lookup in checkout.** The customer types "10 Downing" and the form suggests full addresses. Choosing one fills street, city and postcode. The test types, waits for the first suggestion to contain "Downing", selects it with the keyboard (to exercise accessibility) and asserts that the three dependent fields have the expected values. A second test types a nonsense address and asserts that the "We couldn't find that address" message appears, and the user can still enter the address manually.

**Scenario 2: Product search with a suggestion limit.** The requirement says "show at most 8 suggestions, ordered by popularity". The test types "shoe", waits for the list (`expect(options.first).to_contain_text("shoe")`), asserts `to_have_count(8)` and compares the texts with the expected order from the test data (later in the week you will keep such expected data in JSON files).

**Scenario 3: Assigning a ticket to a user.** In a project-management tool, typing "ann" shows teammates. Names are highlighted in bold where they match. The test must select "Ann Lee" and not "Joanne Smith", so it uses `exact=True` or a `filter(has_text="Ann Lee")`. This is also a case where the list contains avatars and email addresses in each option; selecting by the visible name rather than by position is more robust.

**Scenario 4: Tag input with multiple selections.** A "Skills" field turns each selected suggestion into a "chip". The test selects three tags in sequence using a helper, asserts the chips (`to_have_text([...])`), removes one by clicking the "x", and checks that it can be chosen again.

**Scenario 5: Search with recent history.** When the field is focused and empty, it shows the user's last five searches. The test performs two searches, clicks into the empty box, and asserts that history appears in reverse chronological order. The test depends on state from earlier actions; it creates its own data rather than relying on previous tests.

**Scenario 6: Data-protection edge case.** An organisation requires that suggestions never display other customers' personal data. A test logs in as a restricted user, types a prefix known to match another customer, and asserts that no such suggestion appears. This is a security-flavoured functional test that is easy to automate once the typing/waiting recipe is in place.

---

## Common Pitfalls and Best Practices

1. **Using `fill()` for typeahead.** If no suggestions appear, switch to `press_sequentially`.

2. **Forgetting that `press_sequentially` appends.** Clear the field first when it might contain text. Otherwise the term becomes "OldNew".

3. **Using `time.sleep()` or `wait_for_timeout()` to wait for the list.** Wait for content with `expect(...).to_have_text([...])` or `to_contain_text`. A fixed sleep is either too short (flaky) or too long (slow).

4. **Waiting only for visibility.** The list may be visible from the previous keystroke. Wait for content that proves it matches your term.

5. **Selecting by index.** `nth(0)` may select a different option when the ranking or data changes. Select by text.

6. **Partial text matches.** "Java" matches "JavaScript". Use `exact=True` or a regular expression anchored with `^...$`.

7. **Holding element handles.** Locators re-resolve each time, which handles lists that are rebuilt. Do not store `query_selector` handles.

8. **Typing too quickly for the widget.** If the result is intermittently wrong, add a `delay`, but still wait for the final content with `expect`. The delay is not a substitute for the wait.

9. **Clicking outside the list accidentally.** Some lists close on `blur`. Playwright's `click()` on an option handles `mousedown` ordering correctly, but a manual `page.mouse.click(x, y)` could land elsewhere.

10. **Not testing the keyboard path.** If only the mouse is tested, an entire user group (keyboard and screen-reader users) is unprotected.

11. **Overlooking the "No results" and "minimum characters" rules.** Negative paths find real bugs.

12. **Depending on a third-party site.** Public sites change their markup and may block automated traffic. Use controlled test environments or local mini-apps (as we did) for stable lessons and suites.

**Best practices checklist:** `press_sequentially` to type; `expect` to wait for the exact list (or at least for relevant content); select by text with `exact=True`; test mouse *and* keyboard; test negative paths; keep typing/selection logic in a helper; never store stale element references.

---

## Mini Practice Exercises

**Exercise 1 (warm-up).** Using `open_widget`, write a test that types "Ru", waits for the list, and selects "Ruby" with the mouse. Assert that both the field and the "Selected" paragraph show Ruby.

*Solution:*

```python
def test_ruby(page):
    box = open_widget(page)
    box.press_sequentially("Ru", delay=60)
    expect(page.get_by_role("option")).to_have_text(["Rust", "Ruby"])
    page.get_by_role("option", name="Ruby", exact=True).click()
    expect(box).to_have_value("Ruby")
    expect(page.locator("#chosen")).to_have_text("Selected: Ruby")
```

(Check the order of options in the widget's `DATA` array: Rust comes before Ruby.)

**Exercise 2 (Escape).** Add a test showing that after typing "Py" and pressing Escape, the list closes but the field still contains "Py".

*Hint:* `box.press("Escape")`, then `expect(page.get_by_role("listbox")).to_be_hidden()` and `expect(box).to_have_value("Py")`.

**Exercise 3 (ArrowUp).** Write a test that opens the list for "Ja", presses ArrowDown twice then ArrowUp once, and asserts that the highlighted option is "Java". Then press Enter and assert the selection.

**Exercise 4 (the stale-list experiment).** Temporarily change the helper in Example 6 so it clicks immediately without the `expect` wait, and run it 20 times in a loop with a faster delay (`delay=0`). Does it ever fail? Discuss why; then restore the wait. (*Expected observation:* with no wait, the click may happen before the debounce completes, so the option does not exist yet; Playwright's auto-wait for the locator may rescue it, but a *different* intermediate list could also be clicked on a real server-driven widget.)

**Exercise 5 (parametrised search).** Use `pytest.mark.parametrize` to test the pairs `("Ja", ["Java", "JavaScript"])`, `("Ju", ["Julia"])`, `("Pe", ["Perl"])`, `("Go", ["Go"])`, and a "No results" case with `("Qq", [])`. For the empty case assert the listbox contains "No results".

**Exercise 6 (keyboard-only completion).** Write a test that tabs from the page start into the field (`page.keyboard.press("Tab")`), types "Sw", selects the first suggestion with the keyboard only, and asserts the result. Use `expect(box).to_be_focused()` after the Tab.

**Exercise 7 (challenge: slow server).** Modify `SUGGEST_HTML` so that the lookup delay is 1500 ms for the term "ja" and 100 ms for other terms. Type "ja" and then quickly change to "ju". Write a test that proves the final list shows only Julia, and think about what could go wrong if the widget did not discard the slow "ja" response (a real-world "race condition" bug). *Hint:* the correct assertion is `expect(options).to_have_text(["Julia"])`, and a second `expect` after waiting long enough that the slow response would have arrived (use `expect(options).to_have_text(["Julia"], timeout=3000)` followed by a short bounded observation).

---

## Summary / Key Takeaways

- Auto-suggestion widgets combine key events, debouncing, lookups and a rebuilt list. Knowing the sequence explains how to test them.
- Type with `press_sequentially` (not `fill`) so real key events fire; use `delay` to mimic human speed, and `clear()` first when needed.
- **Wait for content, not time**: `expect(options).to_have_text([...])` or `to_contain_text(...)`. Waiting for mere visibility can pick up a stale list.
- Select with the mouse using `get_by_role("option", name=..., exact=True).click()`, and with the keyboard using `press("ArrowDown")` and `press("Enter")`; assert the highlighted option with `get_by_role("option", selected=True)`.
- Test more than the happy path: minimum characters, no results, case-insensitivity, special characters, Escape, click outside, strict selection, dependent fields.
- Use locators (never stored handles) so rebuilt lists do not cause stale references.
- Wrap repeated behaviour in a helper to keep tests short and consistent.

---

## External Resources

- Playwright for Python, Actions (typing characters, keys and key combinations): https://playwright.dev/python/docs/input#type-characters
- Playwright for Python, Auto-waiting and Assertions: https://playwright.dev/python/docs/actionability
- W3C WAI-ARIA Authoring Practices Guide, Combobox pattern: https://www.w3.org/WAI/ARIA/apg/patterns/combobox/
