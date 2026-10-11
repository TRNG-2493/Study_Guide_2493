# CSS Fundamentals for Test Automation

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what HTML, the DOM, and CSS are, and how they relate to each other.
- Read an HTML page the way a test automation engineer does: as a tree of elements with tags, attributes, and text.
- Describe what a CSS selector is and why browsers (and Playwright) can reuse them to find elements.
- Break a CSS rule into selector, declaration block, property, and value.
- Understand the cascade, specificity, and inheritance at the level needed to read selectors confidently.
- Open Chrome DevTools, inspect an element, and test a selector in the Console and the Elements search box.
- Recognise the difference between selectors written for styling and selectors written for testing.

## Why This Matters

This week's epic is to convert manual test design into automation. You have spent Monday through Wednesday building PyTest skills: writing tests, using fixtures and parametrization, creating a data-driven framework with reports. All of that work tested Python code and functions. Today we turn to the thing most users actually touch: **web pages**.

To automate a web page, your test must say "click *this* button" or "type into *that* field". Computers cannot see a page the way you do. They need a precise description of the element, called a **locator**. The most common locator language on the web is the **CSS selector**, a notation originally designed to style pages that happens to be perfect for finding elements.

For **Project 1: QE Foundations**, this lesson is the base layer. Later today you will build a locator catalog for a practice site, and on Friday you will automate real UI scenarios. Badly written locators are the number one cause of flaky, high-maintenance UI tests, so learning to write good ones is a high-value skill.

Today's lessons build on each other:

1. CSS fundamentals (this lesson)
2. Basic and attribute selectors
3. Pseudo-classes
4. Combinators
5. Dynamic selectors
6. CSS vs. XPath
7. Playwright architecture and setup

---

## The Concept

### 1. HTML: The Structure of a Page

**HTML (HyperText Markup Language)** is the language that describes what is on a web page. A page is made of **elements**. An element usually has:

- a **start tag**, e.g. `<button>`
- optional **attributes**, e.g. `id="login-button"`
- **content** (text or other elements)
- an **end tag**, e.g. `</button>`

```html
<button id="login-button" class="btn primary" type="submit">Log in</button>
```

Let's label every part:

| Part | In the example | Meaning |
|------|----------------|---------|
| Tag name | `button` | What kind of element it is |
| Attribute name | `id`, `class`, `type` | The name of extra information |
| Attribute value | `"login-button"`, `"btn primary"`, `"submit"` | The value of that information |
| Text content | `Log in` | What the user reads |

Some elements have no end tag and no content. They are called **void elements**, e.g. `<input>`, `<br>`, `<img>`.

```html
<input type="text" id="username" name="user-name" placeholder="Username">
```

#### Nesting creates relationships

Elements can sit inside other elements:

```html
<form id="login-form">
  <div class="field">
    <label for="username">Username</label>
    <input id="username" type="text">
  </div>
  <button type="submit">Log in</button>
</form>
```

Here `<form>` is the **parent** of `<div>` and `<button>`. The `<div>` is the **parent** of `<label>` and `<input>`. The `<label>` and `<input>` are **siblings** (they share a parent). The `<input>` is a **descendant** of `<form>`, even though it is two levels down. These family words come back constantly in later lessons (combinators especially), so make sure they feel natural.

### 2. The DOM: The Live Tree in the Browser

When a browser loads HTML, it converts the text into a live in-memory tree called the **DOM (Document Object Model)**. JavaScript can change the DOM while the page is open: adding items to a cart, showing an error message, removing a banner.

```
document
└── html
    └── body
        └── form#login-form
            ├── div.field
            │   ├── label
            │   └── input#username
            └── button
```

**Important for testers:** what you see in "View Page Source" is the *original* HTML text. What you see in DevTools' Elements panel is the *current DOM*, which may differ because JavaScript modified it. Playwright and CSS selectors work against the **DOM**, not the original source. If an element appears only after a click, it is not in the DOM until then, and your test must account for that (Friday's auto-waiting lesson covers this).

### 3. CSS: Style Rules

**CSS (Cascading Style Sheets)** is the language that controls how elements look: colours, sizes, spacing, layout. A CSS **rule** looks like this:

```css
button.primary {
  background-color: blue;
  color: white;
}
```

Anatomy:

- `button.primary` is the **selector**: it says *which elements* the rule applies to.
- `{ ... }` is the **declaration block**.
- `background-color: blue;` is a **declaration**, made of a **property** (`background-color`) and a **value** (`blue`).

For a tester, **only the selector part matters**. We do not care about colours. We borrow the selector language because it is a compact, standardised, fast way to say "find me the elements that match this description". The browser already knows how to evaluate selectors extremely quickly, and the specification is maintained by the W3C.

### 4. Where CSS Lives (and Why You Should Know)

Developers attach CSS to pages in three ways:

```html
<!-- 1. External stylesheet (most common) -->
<link rel="stylesheet" href="styles.css">

<!-- 2. Internal style block -->
<style>
  .error { color: red; }
</style>

<!-- 3. Inline style on an element -->
<p style="color: red;">Error</p>
```

This matters to testers for two reasons:

1. **Class names come from styling needs.** A class like `btn-primary` exists because a designer wanted a style. Developers may rename it during a redesign without telling you. This is why class-based locators can be fragile.
2. **Visibility is controlled by CSS.** An element can be present in the DOM but hidden using `display: none` or `visibility: hidden`. A test must distinguish "exists" from "visible".

### 5. Selectors: The Heart of the Matter

A **CSS selector** is a pattern that matches zero or more elements in the DOM. Here are the simplest forms. (The next lesson, *Basic and attribute selectors*, goes deep. This is a preview so the vocabulary is familiar.)

| Selector | Meaning | Matches |
|----------|---------|---------|
| `button` | Type (tag) selector | Every `<button>` |
| `#login-button` | ID selector | The element with `id="login-button"` |
| `.primary` | Class selector | Every element with class `primary` |
| `[type="submit"]` | Attribute selector | Every element with `type="submit"` |
| `form button` | Descendant combinator | Buttons anywhere inside a form |

Notice the symbols: `#` means id, `.` means class, and `[ ]` means attribute. Combining them gives precision: `button#login-button.primary[type="submit"]` matches only a `<button>` having that id, that class, and that attribute.

### 6. The Result of a Selector: A List

A critical mindset shift: a selector does not return *the* element. It returns **all matching elements** (possibly zero, one, or many). In JavaScript:

```js
document.querySelector("button");     // the FIRST match, or null
document.querySelectorAll("button");  // a list of ALL matches
```

A good locator for a test targets **exactly one** element. If your selector matches five elements, your test needs another way to choose, or the selector needs tightening. Playwright will actually complain when an action (like `click`) is attempted on a locator that matches several elements. This is called **strict mode**, and we will meet it on Friday. For now remember: *a good test locator matches one element, the right one, every time.*

### 7. The Cascade, Specificity, and Inheritance (Just Enough)

Three concepts explain how CSS decides between conflicting rules. You do not need to master them, but they help you read selectors and avoid confusion.

**Cascade.** When multiple rules target the same element, the browser picks one by importance, specificity, and order (later rules win ties).

**Specificity.** Every selector has a weight. Roughly, from strongest to weakest:

1. Inline style
2. ID selectors (`#id`)
3. Class, attribute, and pseudo-class selectors (`.cls`, `[type]`, `:hover`)
4. Type selectors (`div`, `a`)

So `#login-button` is more specific than `.primary`, which is more specific than `button`.

**Inheritance.** Some properties (like `color` and `font-family`) pass down from parent to child automatically. Others (like `border`) do not.

**Why testers care.** Specificity is about *styling conflicts*. It does **not** affect which elements a selector matches. `button` and `#login-button` can both match the same element; neither "wins" in a locator context. The takeaway: do not worry about specificity when writing locators, but understand it when you read a stylesheet or ask a developer why an element looks different.

### 8. The Box Model and Visibility (Quick Orientation)

Every element is drawn as a rectangular **box** (content, padding, border, margin). Playwright uses this box to decide where to click (the centre of the element's box) and whether the element is covered by another one. You do not need to compute it yourself, but be aware that:

- An element with zero width or height is usually treated as not visible.
- `display: none` removes the element from layout entirely.
- `visibility: hidden` keeps its space but hides it.
- `opacity: 0` is invisible to the eye but counts as visible for Playwright's check (a known gotcha).

### 9. Using Chrome DevTools to Explore and Test Selectors

DevTools is your lab. Practise these steps until they are automatic.

**Step 1: Open DevTools.** Press `F12` or `Ctrl+Shift+I` (`Cmd+Option+I` on macOS), or right-click an element and choose **Inspect**.

**Step 2: Use the element picker.** Click the arrow icon at the top-left of DevTools (or `Ctrl+Shift+C`), then click any element on the page. The Elements panel jumps to that element's HTML.

**Step 3: Read the element.** Look at the tag, id, classes, and other attributes. Ask yourself: *which of these is stable and meaningful?*

**Step 4: Test a selector in the Elements panel.** Press `Ctrl+F` while the Elements panel is focused. A search box appears. Type a CSS selector, e.g. `button[type="submit"]`. The box shows "1 of 1" (match count) and highlights the element. This is the fastest way to validate a selector.

**Step 5: Test in the Console.**

```js
document.querySelectorAll('button[type="submit"]').length   // how many matches?
document.querySelector('#login-button')                      // returns the element or null
```

Chrome's Console also has the shortcut `$$("css")` which behaves like `querySelectorAll` and returns an array, and `$("css")` for the first match.

**Step 6: Copy a selector.** Right-click an element in the Elements panel, then **Copy > Copy selector**. Chrome generates a selector like `#root > div > div.login_wrapper > form > input.input_error`. **Warning:** generated selectors are usually long and brittle because they encode the whole path. Treat them as a starting point, never as a final answer. We will talk about why in the *Dynamic selectors* lesson.

---

## Code Examples

### Example 1: A small practice page

Save this as `practice.html` on your computer and open it in Chrome. We will use it throughout today.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Practice Login Page</title>
  <style>
    .error { color: red; }
    .hidden { display: none; }
  </style>
</head>
<body>
  <h1>Welcome to Shop Demo</h1>

  <form id="login-form" action="#">
    <div class="field">
      <label for="username">Username</label>
      <input id="username" name="user-name" type="text" placeholder="Username" data-test="username">
    </div>
    <div class="field">
      <label for="password">Password</label>
      <input id="password" name="password" type="password" placeholder="Password" data-test="password">
    </div>
    <button id="login-button" class="btn primary" type="submit" data-test="login-button">Log in</button>
    <p class="error hidden" data-test="error">Invalid credentials</p>
  </form>

  <ul class="products">
    <li class="product">Backpack</li>
    <li class="product">Bike Light</li>
    <li class="product sale">T-Shirt</li>
  </ul>
</body>
</html>
```

### Example 2: Testing selectors in the DevTools Console

Open the page, press `F12`, go to the **Console** tab, and run each line.

```js
document.querySelectorAll("input").length          // 2
document.querySelector("#login-button").textContent // "Log in"
document.querySelectorAll(".product").length        // 3
document.querySelector(".product.sale").textContent // "T-Shirt"
document.querySelector("[data-test='error']")       // the <p> element
```

**Line-by-line:**

- `document` is the root object of the DOM; `.querySelectorAll(...)` accepts any CSS selector string and returns a `NodeList` of every match.
- `"input"` is a type selector. There are two `<input>` elements, so `.length` is `2`.
- `#login-button` uses the ID selector. `.textContent` reads the text inside, `"Log in"`.
- `.product` matches the three list items.
- `.product.sale` has **no space** between the two classes. That means "an element that has *both* classes". Only the T-Shirt item matches.
- `[data-test='error']` is an attribute selector. Single quotes are used inside the JS double quotes to avoid escaping.

### Example 3: The same selectors from Python with Playwright (preview)

You will install and understand Playwright properly in the last lesson of today. Here is just a preview so you can see that the *same* CSS selector strings work in code. Do not worry about running it yet.

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

html_file = Path("practice.html").resolve().as_uri()   # file:///.../practice.html

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(html_file)

    print(page.locator("#login-button").inner_text())   # Log in
    print(page.locator(".product").count())              # 3
    print(page.locator(".product.sale").inner_text())    # T-Shirt

    browser.close()
```

**Explanation:**

- `sync_playwright()` starts Playwright using the synchronous API (simple, top-to-bottom code, ideal for beginners).
- `p.chromium.launch()` starts a Chromium browser, headless (no visible window) by default.
- `page.goto(...)` navigates to our local file. `Path.resolve().as_uri()` turns a relative path into a proper `file://` URL.
- `page.locator("css")` creates a **locator** from a selector string. Playwright treats strings without a prefix as CSS (or XPath if they begin with `//`).
- `.inner_text()` reads visible text; `.count()` returns the number of matching elements.

The key observation: the selector strings are identical to what you tested in DevTools.

---

## Real-World Scenarios

**Scenario 1: The redesign.** A team ships a UI redesign. Class names change from `btn-blue` to `button--primary`. Fifty tests that used `.btn-blue` fail overnight, though the application still works. A tester who relied on a stable `data-test` attribute (agreed with developers) sees zero failures. The lesson: understand *why* attributes exist and choose the stable ones.

**Scenario 2: The ghost element.** A "Session expired" banner is hidden with `display: none` until a timer fires. A tester's selector `.banner` matches the element immediately, yet the test fails because the banner is not *visible*. Knowing the DOM-vs-visibility distinction speeds up debugging.

**Scenario 3: Verifying before coding.** A senior engineer never writes a locator straight into code. They prove it in DevTools first ("1 of 1" in the search box), then paste it into the test. This habit saves hours.

---

## Common Mistakes

1. **Confusing View Source with the DOM.** If you search View Source for an element created by JavaScript, you will not find it. Use DevTools Elements.
2. **Copying the generated selector blindly.** `body > div:nth-child(3) > div > form > input:nth-child(2)` breaks the moment a designer adds a banner.
3. **Assuming one match.** Always check the match count. A selector like `.field input` matches two inputs here, not one.
4. **Forgetting `#` and `.`.** `login-button` selects `<login-button>` tags (which do not exist). `#login-button` is the ID.
5. **Using spaces carelessly.** `.product .sale` (with space) means "a `.sale` *inside* a `.product`". `.product.sale` (no space) means "one element with both classes". Different meanings!
6. **Treating specificity as locator priority.** It only matters for styling.
7. **Quoting errors.** `[data-test="error"]` inside a Python string needs matching quote handling: `page.locator('[data-test="error"]')`.

---

## Practice Exercises

Use `practice.html` from above.

**Exercise 1: Vocabulary.** For the `<input id="password" ...>` element, list its tag name, each attribute name with its value, its parent, and its sibling(s).

*Solution:* Tag `input`; attributes `id="password"`, `name="password"`, `type="password"`, `placeholder="Password"`, `data-test="password"`. Parent is `<div class="field">`. Its sibling is `<label for="password">`.

**Exercise 2: Predict, then verify.** Predict how many elements each selector matches, then run it in DevTools with `$$(...)`.

1. `div`
2. `.field`
3. `li`
4. `.error`
5. `.hidden`
6. `input[type="password"]`

*Solution:* 1) 2 (both `.field` divs); 2) 2; 3) 3; 4) 1; 5) 1; 6) 1.

**Exercise 3: Write the selector.** Write a selector for each target and confirm "1 of 1" in the Elements search box.

1. The Log in button
2. The username field
3. The T-Shirt list item
4. The error message paragraph

*Hint:* use `#`, `[data-test=...]`, `.product.sale`. Sample answers: `#login-button`, `[data-test="username"]`, `.product.sale`, `[data-test="error"]`.

**Exercise 4: Source versus DOM.** In the Console, run `document.querySelector('.error').classList.remove('hidden')`. Watch the message appear. Now open View Source and check whether the class `hidden` is still on that element. Explain what you saw.

*Answer:* View Source still shows `hidden` because it displays the original text; the live DOM no longer has it.

**Exercise 5: Reflection.** Why might `[data-test="login-button"]` be a better locator than `.btn.primary`? Write 3 sentences.

*Hint:* think about who owns each attribute, and what happens during redesigns.

---

## Summary

- HTML describes the structure of a page; the browser turns it into the live **DOM tree**; CSS styles it.
- A **CSS selector** is a pattern that matches elements; testers borrow it as a locator language.
- A CSS rule has a selector, a declaration block, properties, and values. Only the selector matters for locators.
- A selector returns a **list**; a good locator matches exactly one element.
- Specificity, cascade, and inheritance matter for styling, not for locating elements.
- Class names exist for styling and can change; stable attributes make better test hooks.
- DevTools lets you inspect, search (`Ctrl+F` in Elements), and test selectors (`$$("css")`) before you write code.
- Next up: *Basic and attribute selectors*, where we systematically learn the selector syntax.

---

## Additional Resources

- MDN Web Docs, CSS selectors: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Basic_selectors
- MDN Web Docs, Introduction to the DOM: https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction
- W3C Selectors Level 4 specification: https://www.w3.org/TR/selectors-4/
