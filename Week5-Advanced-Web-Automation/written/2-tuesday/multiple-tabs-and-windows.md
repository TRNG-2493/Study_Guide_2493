# Multiple Tabs and Windows

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the Playwright object model: browser, browser context, page, and how "a tab" and "a window" are both represented as a `Page`.
- Explain why Playwright has no "switch to window" command, and why that makes multi-tab tests more reliable than in older tools.
- Capture a popup or new tab opened by a click using `page.expect_popup()` and `context.expect_page()`, and choose between them.
- Wait for the new page to load, interact with it, close it, and return to the original page.
- Work with several pages at once, list them with `context.pages`, and bring a tab to the front.
- Handle links with `target="_blank"`, `window.open()`, pop-up login windows (OAuth style), and links that open in the same tab.
- Understand browser context isolation (cookies, storage) and use multiple contexts to simulate two different users.
- Recognise and handle related events: `page.on("popup")`, `context.on("page")`, `page.on("close")`.
- Avoid common problems: race conditions, capturing the wrong page, forgetting to wait for load, and orphaned pages.

---

## Why This Matters

Users rarely stay in a single browser tab. They click "Terms and Conditions" and a new tab opens. They choose "Sign in with Google" and a small pop-up window appears. A product page might offer "Compare in a new window". An admin tool might open a report in a separate tab to allow side-by-side viewing. Print previews, document viewers, and help pages are also common examples.

If your test framework cannot follow the user into the new tab, entire journeys cannot be automated: you click a link, the new tab opens, and your script is left staring at the old page, asserting on content that never changes. In the Week 5 epic, *complex UI interactions* include exactly this class of flow, and your **Project 1 - QE Foundations** UI tests will almost certainly include at least one "opens in a new tab" step (for instance, checking that a terms link opens the right page).

Tabs are also where **race conditions** appear in test code. The new tab opens *asynchronously*, a short time after the click. If you ask for "the new tab" before it exists, you get nothing, or worse, the wrong thing. Playwright's `expect_popup` and `expect_page` APIs solve this by letting you register interest in the event *before* you cause it. Learning that "register first, then act" pattern is useful far beyond tabs: you will see it again with downloads, file choosers, and responses later today.

---

## The Concept

### 1. The object model: browser, context, page

Playwright organises a browser session into three nested levels:

```
Browser
 └── BrowserContext   (an isolated "profile": its own cookies, storage, cache, permissions)
      ├── Page        (a tab or a pop-up window)
      ├── Page
      └── Page
```

- **Browser**: one browser process (Chromium, Firefox, or WebKit).
- **BrowserContext**: like a brand-new incognito profile. It has its own cookies, local storage, cache, permissions, geolocation, and so on. Contexts are cheap, fully isolated from each other, and the foundation of Playwright's test isolation.
- **Page**: a single tab or pop-up window. In Playwright a "tab" and a "window" are the same thing: a `Page`.

When you call `browser.new_page()`, Playwright quietly creates a new context and one page in it. When you want more control, you create the context yourself:

```python
context = browser.new_context()
page = context.new_page()
```

All pages in the same context **share cookies and storage**. This matters for multi-tab flows: if you log in on tab 1, tab 2 (in the same context) is also logged in, exactly as in a real browser. Pages in different contexts do not share anything.

### 2. No "switch to window"

If you have used Selenium, you will recall `driver.window_handles` and `driver.switch_to.window(handle)`. Selenium has a single "current window" pointer that you must move; forgetting to move it back is a classic bug.

Playwright has no such pointer. Each `Page` object is an independent handle. If you hold `page` (the original tab) and `new_page` (the popup), you can use either at any time:

```python
page.get_by_role("link", name="Terms").click()   # opens a new tab
# ... capture it as new_page ...
new_page.get_by_role("heading").inner_text()
page.get_by_role("button", name="Continue").click()   # still works on the original tab
```

The mental model is "two remote controls, two TVs" rather than "one remote that must be pointed at one TV at a time".

### 3. The "register first, then act" pattern

A new tab opens as a *consequence* of an action (a click). Playwright's solution is a **context manager** (`with ...:`) that starts listening before the action and gives you the result after:

```python
with page.expect_popup() as popup_info:
    page.get_by_role("link", name="Terms").click()
popup = popup_info.value
```

Step by step:

1. `page.expect_popup()` starts listening for a "popup" event on `page`. The listener is active inside the `with` block.
2. Inside the block, you perform the action that triggers the popup (here a click).
3. When the block ends, Playwright waits for the event if it has not arrived yet (up to the default timeout of 30 seconds).
4. `popup_info.value` is the new `Page` object.

If you wrote it the other way round (click first, then ask for the popup), there would be a window of time in which the event could fire before you started listening, and you would miss it. The `with` structure eliminates that race.

### 4. `page.expect_popup()` versus `context.expect_page()`

Both capture a new page. They differ in scope.

| API | Fires when | Best for |
| --- | --- | --- |
| `page.expect_popup()` | A **popup** is opened *by that page* (via `target="_blank"` link, `window.open()`) | Links and buttons clicked in your page; the popup is clearly related to that page |
| `context.expect_page()` | **Any** new page is created in the context (by any page, or even `context.new_page()`) | Flows where the new tab's origin is unclear, or when the action is performed from another new tab, or opener relationship is broken |

A practical tip: `page.expect_popup()` is the clearer choice for "I clicked a link in this page". `context.expect_page()` is the fallback when popups do not fire for some reason, for example links created with certain `rel` attributes or tabs opened by browser extensions or keyboard shortcuts (Ctrl+Click).

```python
with context.expect_page() as new_page_info:
    page.get_by_role("link", name="Docs").click(modifiers=["ControlOrMeta"])   # Ctrl/Cmd+Click opens a background tab
new_tab = new_page_info.value
```

`modifiers=["ControlOrMeta"]` presses Ctrl on Windows/Linux and Cmd on macOS, a convenient cross-platform way to simulate "open link in new tab". (Monday's keyboard and mouse lesson showed modifier keys; this is a practical use.)

### 5. Waiting for the new page to load

The new `Page` object exists as soon as the tab is created, but its content may still be loading. Playwright's auto-waiting will wait for elements on it just as for any page, so often you can interact immediately. But there are times you want to be explicit:

```python
popup.wait_for_load_state()                       # waits for "load" by default
popup.wait_for_load_state("domcontentloaded")     # earlier: HTML parsed
```

Typical states:

| State | Meaning |
| --- | --- |
| `"domcontentloaded"` | The HTML has been parsed. |
| `"load"` (default) | Page and sub-resources (images, scripts) have loaded. |
| `"networkidle"` | No network connections for 500 ms; **discouraged** for tests because it is slow and flaky on pages with analytics or polling. |

Better than waiting for a load state is asserting something you actually need:

```python
expect(popup).to_have_title(re.compile("Terms"))
expect(popup).to_have_url(re.compile(r"/terms$"))
expect(popup.get_by_role("heading", name="Terms of Service")).to_be_visible()
```

These assertions retry until they pass, so they double as waits.

### 6. Working with the new tab

Once you have the `Page`, everything you know applies:

```python
popup.get_by_role("link", name="Privacy").click()
popup.get_by_label("Search").fill("refund")
print(popup.url, popup.title())
```

Useful properties and methods:

| Member | Purpose |
| --- | --- |
| `page.url` | Current URL (property) |
| `page.title()` | Document title (method) |
| `page.bring_to_front()` | Activate the tab (visible in headed mode) |
| `page.close()` | Close the tab |
| `page.is_closed()` | Whether the tab is closed |
| `page.opener()` | The page that opened this one (may be `None`) |
| `page.context` | The owning BrowserContext |
| `page.on("close", handler)` | Run code when the tab closes |

After you finish with the popup, close it if appropriate (`popup.close()`) and carry on with the original page. In many flows (such as a payment pop-up), the popup closes itself; then wait for that with `popup.wait_for_event("close")` or `page.on("close")`.

### 7. Listing and finding pages

`context.pages` returns a list of all open pages in the context:

```python
print(len(context.pages))
for p in context.pages:
    print(p.url)
```

This is useful for debugging and for assertions such as "clicking the link opened exactly one extra tab":

```python
before = len(context.pages)
with context.expect_page():
    page.get_by_role("link", name="Docs").click()
assert len(context.pages) == before + 1
```

You can find a page by URL:

```python
target = next((p for p in context.pages if "docs" in p.url), None)
```

`next(generator, default)` returns the first match or `None`. Remember that `context.pages` is a **snapshot** list; do not store it and expect it to update.

### 8. Event listeners: `on("popup")` and `on("page")`

Instead of a `with` block, you can attach a listener:

```python
popups = []
page.on("popup", lambda p: popups.append(p))
context.on("page", lambda p: print("New page:", p.url))
```

Listeners are useful for **logging** or for apps that open pop-ups unpredictably. They are less suitable for flows where you need the page right after a specific click, because you would have to wait and poll a list. The `expect_*` pattern is the cleaner choice there. Event handlers run in Playwright's event loop; keep them short.

(`page.on("popup", ...)` and `context.on("page", ...)` receive a Page that may still be at `about:blank`; the real URL appears after navigation. Call `new_page.wait_for_load_state()` before reading `url`.)

### 9. Pop-up login windows and `window.open()`

An OAuth-style login opens a small window, you sign in, and it closes itself, handing a token back to the opener. The test pattern:

```python
with page.expect_popup() as popup_info:
    page.get_by_role("button", name="Sign in with Provider").click()
login = popup_info.value
login.get_by_label("Email").fill("student@example.com")
login.get_by_label("Password").fill("secret")
login.get_by_role("button", name="Sign in").click()
login.wait_for_event("close")                        # popup closes itself
expect(page.get_by_text("Welcome, student")).to_be_visible()
```

In practice, real third-party providers (Google, Facebook) block automated logins and may trigger CAPTCHAs or 2FA. For tests, use a **stubbed or test identity provider**, or authenticate through the API and reuse saved login state (`storage_state`). Authentication reuse is beyond today's scope; here you only need to know the popup mechanics.

### 10. Same-tab navigation versus new-tab navigation

Not every link opens a new tab. `<a href="...">` without `target="_blank"` navigates in place; calling `expect_popup()` for it would time out. Clues that a link opens a new tab:

- `target="_blank"` attribute.
- `rel="noopener"` or `noreferrer` (often paired with `_blank`).
- An icon indicating "opens in new window".
- JavaScript handlers that call `window.open(...)`.

Testing a link with `target="_blank"` is also a legitimate assertion on its own:

```python
expect(page.get_by_role("link", name="Terms")).to_have_attribute("target", "_blank")
```

A very common pattern is to **avoid** opening the tab entirely, when the check only needs the destination URL:

```python
href = page.get_by_role("link", name="Terms").get_attribute("href")
assert href.endswith("/terms")
```

This is faster and more stable, but it does not prove that the link works when clicked, so combine both approaches as needed.

### 11. Multiple contexts: two users at once

For chat applications, collaboration tools, or admin/user interactions, two independent logged-in users are needed. Use two contexts:

```python
alice_ctx = browser.new_context()
bob_ctx = browser.new_context()
alice = alice_ctx.new_page()
bob = bob_ctx.new_page()

alice.goto(URL); bob.goto(URL)
alice.get_by_label("Message").fill("Hello Bob")
alice.get_by_role("button", name="Send").click()
expect(bob.get_by_text("Hello Bob")).to_be_visible()
```

Cookies and storage are isolated between contexts, so Alice and Bob really are separate users. This is a powerful technique that is not possible with two tabs in one context (they would share a session).

### 12. Browser dialogs versus new windows

Do not confuse a **new tab/window** with a **JavaScript dialog** (`alert`, `confirm`, `prompt`) that you handled on Monday. Dialogs do not create new `Page` objects; they are handled with `page.on("dialog", ...)` or `page.once("dialog", ...)`. New windows are handled with `expect_popup`/`expect_page`.

### 13. Headless mode and "bring to front"

In headless runs there is no visible window, but each page still exists and works. `bring_to_front()` is mostly relevant in headed mode (watching the browser) or for features that depend on page visibility (for instance, pages that pause timers in background tabs). If a page behaves differently when hidden, call `bring_to_front()` on it.

---

## Code Examples

The examples serve their own pages with `page.route()` so you can run them offline. First, a small helper that registers routes for a fake site `http://test.local`:

```python
from playwright.sync_api import sync_playwright, expect
import re

PAGES = {
    "/": """
        <h1>Home</h1>
        <a id="terms" href="/terms" target="_blank">Terms</a>
        <a id="plain" href="/about">About (same tab)</a>
        <button id="pop" onclick="window.open('/help', '_blank', 'width=400,height=300')">Help popup</button>
        <button id="login"
          onclick="const w = window.open('/login', 'login', 'width=400,height=300');
                   window.addEventListener('message', e => { document.getElementById('who').textContent = e.data; });">
          Sign in</button>
        <p id="who"></p>
    """,
    "/terms": "<title>Terms of Service</title><h1>Terms of Service</h1><p>Be kind.</p>",
    "/about": "<title>About</title><h1>About us</h1>",
    "/help":  "<title>Help</title><h1>Help centre</h1>",
    "/login": """
        <title>Login</title><h1>Login</h1>
        <button onclick="window.opener.postMessage('Welcome, student', '*'); window.close();">Approve</button>
    """,
}

def serve(route):
    path = route.request.url.split("test.local", 1)[1] or "/"
    body = PAGES.get(path)
    if body is None:
        route.fulfill(status=404, body="Not found")
    else:
        route.fulfill(status=200, content_type="text/html", body=body)
```

**Explanation of the setup**

- `PAGES` maps paths to HTML. The home page has a `target="_blank"` link, a normal same-tab link, a button that calls `window.open`, and a login button that opens a pop-up which later messages back its opener.
- `window.open('/help', '_blank', 'width=400,height=300')`: the third argument asks for a pop-up *window* with a size; Playwright treats it as a `Page` all the same.
- `window.opener.postMessage(...)` and the `message` listener: a simplified version of how OAuth pop-ups communicate. `window.close()` closes the pop-up.
- `serve(route)`: the route handler, which looks up the path and fulfils the request with our HTML or a 404.
- `route.request.url.split("test.local", 1)[1] or "/"`: takes everything after the host name; an empty string (for `http://test.local`) becomes `/`.

Important: when you register the route on the **context** (`context.route(...)`), it applies to *all* pages in that context, including the new tabs. If you registered it only on `page.route(...)`, popups would not be covered. We use the context below.

### Example 1: A link that opens a new tab

```python
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    context.route("http://test.local/**", serve)
    page = context.new_page()
    page.goto("http://test.local/")

    with page.expect_popup() as popup_info:
        page.get_by_role("link", name="Terms").click()
    terms = popup_info.value

    terms.wait_for_load_state()
    expect(terms).to_have_title("Terms of Service")
    expect(terms.get_by_role("heading", name="Terms of Service")).to_be_visible()
    print("Open pages:", len(context.pages))     # 2

    terms.close()
    expect(page.get_by_role("heading", name="Home")).to_be_visible()
    browser.close()
```

**Line-by-line**

- `context = browser.new_context()`: we make the context explicitly because we want to attach a route to it and later inspect `context.pages`.
- `context.route("http://test.local/**", serve)`: every request from any page in the context matching the glob goes through `serve`. The `**` matches any number of path segments.
- `page = context.new_page()`: the first tab. `page.goto(...)` loads the home page.
- `with page.expect_popup() as popup_info:`: starts listening for popups from `page`.
- `page.get_by_role("link", name="Terms").click()`: the click that opens the new tab. (The role is `link` because it is an `<a href>`.) Note "Terms" is also a substring match; there is only one such link on our page so it is unambiguous.
- `terms = popup_info.value`: after the `with` block, the popup `Page` is available. `.value` is a property, not a method.
- `terms.wait_for_load_state()`: waits for the `load` event of the new tab.
- `expect(terms).to_have_title("Terms of Service")`: a **page assertion** (as opposed to a locator assertion). It retries until the title matches.
- `expect(terms.get_by_role("heading", ...)).to_be_visible()`: element assertion on the new tab.
- `len(context.pages)`: two, the original and the popup.
- `terms.close()`: closes the new tab. The original `page` object was never invalidated, so we can use it immediately. The assertion confirms the home page content is still there.

### Example 2: `window.open()` and a regular same-tab link

```python
    page.goto("http://test.local/")

    # window.open: the same expect_popup pattern works
    with page.expect_popup() as info:
        page.get_by_role("button", name="Help popup").click()
    help_page = info.value
    expect(help_page.get_by_role("heading", name="Help centre")).to_be_visible()
    help_page.close()

    # Same-tab link: NO popup; use wait_for_url instead
    page.get_by_role("link", name="About (same tab)").click()
    page.wait_for_url("**/about")
    expect(page.get_by_role("heading", name="About us")).to_be_visible()
    print(len(context.pages))     # 1
```

- A button calling `window.open` produces a popup event just as a `target="_blank"` link does.
- The About link has no `target`, so the **same page** navigates. No popup is created, and wrapping the click in `expect_popup()` would hang until timeout. Instead use `page.wait_for_url("**/about")` or an assertion such as `expect(page).to_have_url(...)`. (`**` is a glob wildcard that matches any characters including slashes. Navigation waiting is the focus of another lesson today.)
- `len(context.pages)` is 1 because the popup was closed.

### Example 3: `context.expect_page()` and Ctrl+Click

```python
    page.goto("http://test.local/")

    with context.expect_page() as new_page_info:
        page.get_by_role("link", name="Terms").click(modifiers=["ControlOrMeta"])
    background = new_page_info.value
    expect(background).to_have_url("http://test.local/terms")   # a background tab may still be at about:blank until it loads
    background.close()
```

- A Ctrl/Cmd+Click opens the link in a new background tab. The `modifiers` argument holds modifier keys down during the click.
- Because the tab was opened via a keyboard shortcut rather than `window.open`, the page-level popup event may not describe it as you expect, so `context.expect_page()` is the safer capture.

### Example 4: Pop-up login that closes itself

```python
    page.goto("http://test.local/")

    with page.expect_popup() as info:
        page.get_by_role("button", name="Sign in").click()
    login = info.value
    login.get_by_role("button", name="Approve").click()
    login.wait_for_event("close")       # wait until the popup has closed itself
    expect(page.locator("#who")).to_have_text("Welcome, student")
```

- `login.get_by_role("button", name="Approve").click()` runs `postMessage` and `window.close()`.
- `login.wait_for_event("close")` blocks until the `close` event on that page. If the popup had already closed, this would hang until timeout; in real flows you can use `login.is_closed()` and a conditional, or use the `with login.expect_event("close"):` form around the click:

```python
with login.expect_event("close"):
    login.get_by_role("button", name="Approve").click()
```

This is the safer pattern: the listener is registered *before* the click, mirroring `expect_popup`.

- The final assertion proves that the opener received the message and updated the DOM.

### Example 5: Multiple tabs in parallel, shared state, and `bring_to_front`

```python
    tab_a = context.new_page()
    tab_b = context.new_page()
    tab_a.goto("http://test.local/terms")
    tab_b.goto("http://test.local/about")

    tab_a.bring_to_front()
    print([pg.url for pg in context.pages])

    # Cookies are shared inside a context:
    tab_a.evaluate("document.cookie = 'theme=dark; path=/'")
    print(tab_b.evaluate("document.cookie"))      # theme=dark
```

- `context.new_page()` opens a new blank tab in the same context.
- `bring_to_front()` activates the tab (visible when running headed).
- `[pg.url for pg in context.pages]` lists URLs of all tabs; our earlier `page` plus the two new tabs make three.
- `tab_a.evaluate(...)` runs JavaScript in the page. We set a cookie in tab A and read it in tab B, demonstrating that tabs in one context share cookies. (Cookies need an http(s) URL; our routed pages qualify.)

### Example 6: Two contexts, two users

```python
    ctx_a = browser.new_context()
    ctx_b = browser.new_context()
    for c in (ctx_a, ctx_b):
        c.route("http://test.local/**", serve)

    a = ctx_a.new_page(); a.goto("http://test.local/terms")
    b = ctx_b.new_page(); b.goto("http://test.local/terms")

    a.evaluate("document.cookie = 'user=alice; path=/'")
    print(b.evaluate("document.cookie") or "(empty)")      # (empty): isolated
```

- A separate context means separate cookies. User B does not see User A's cookie, which is the right model for testing multi-user systems.
- `for c in (ctx_a, ctx_b): c.route(...)` applies the same routing to both contexts.
- `... or "(empty)"` uses Python's `or` to display a placeholder when the string is empty.

### Example 7: Defensive capture (assert exactly one new page)

```python
def click_and_capture(context, page, locator):
    before = len(context.pages)
    with context.expect_page() as info:
        locator.click()
    new = info.value
    new.wait_for_load_state("domcontentloaded")
    assert len(context.pages) == before + 1, "expected exactly one new tab"
    return new

terms = click_and_capture(context, page, page.get_by_role("link", name="Terms"))
```

A tiny helper like this standardises the pattern for your suite and documents intent. It is a good candidate for a utility module, or later a page-object method (covered in depth on Wednesday).

---

## Real-World Scenarios

### Scenario 1: "Terms and Conditions" at checkout

Product management wants to ensure the Terms link in the checkout footer opens the correct document in a new tab, and that the user's cart is untouched.

```python
def test_terms_opens_in_new_tab(page, context):
    page.goto("/checkout")
    with page.expect_popup() as info:
        page.get_by_role("link", name="Terms and Conditions").click()
    terms = info.value
    expect(terms).to_have_url(re.compile(r"/legal/terms"))
    terms.close()
    expect(page.get_by_test_id("cart-count")).to_have_text("3")
```

### Scenario 2: Report preview in a separate window

A BI tool opens a report in a new tab. The tab is slow to render charts. Use assertions with generous but bounded timeouts rather than sleeps:

```python
with page.expect_popup() as info:
    page.get_by_role("button", name="Open report").click()
report = info.value
expect(report.locator("canvas.chart")).to_be_visible(timeout=15_000)
```

`15_000` is a Python numeric literal with an underscore for readability (15,000 ms = 15 seconds).

### Scenario 3: Cross-user notification

A support tool lets agents assign tickets to teammates. The assignee should see a notification immediately. Two contexts (two users) in one test verify this, as in Example 6, without logging in and out repeatedly.

### Scenario 4: Pop-ups blocked or unexpected

Sometimes pop-ups are intentionally unwanted: a marketing pop-up that should *not* appear. You can assert the absence:

```python
popups = []
page.on("popup", lambda p: popups.append(p))
page.get_by_role("button", name="Pay").click()
page.wait_for_timeout(500)       # last resort: brief wait to let any popup surface
assert not popups
```

A short fixed wait is one of the very few times `wait_for_timeout` is acceptable: when proving a negative (that something does *not* happen), no condition exists to wait for. Keep it small and comment why.

---

## Common Pitfalls and Best Practices

1. **Clicking before listening.** Writing `click()` then `expect_popup()` misses the event. Always wrap the click inside the `with` block.
2. **Using `expect_popup` for same-tab navigation.** It times out. Check for `target="_blank"` or `window.open`; otherwise use `wait_for_url`.
3. **Registering routes/listeners only on the first page.** Use `context.route`, `context.add_init_script`, and similar so new tabs inherit them.
4. **Reading `popup.url` immediately.** A new tab may still be at `about:blank`. Wait for load state or assert the URL.
5. **Forgetting `.value`.** `popup_info` is an event-info object; the page is `popup_info.value`.
6. **Expecting a global "current tab."** There is none. Always use the specific `Page` object you mean.
7. **Leaking tabs.** Close tabs you open, or rely on test isolation (each test gets a fresh context in pytest-playwright, which is covered in depth on Wednesday). Too many tabs slow down CI.
8. **Assuming two tabs equal two users.** Tabs share cookies in a context. Use separate contexts for separate users.
9. **Fighting third-party login pop-ups.** Real providers block bots. Use test accounts, stubs, or saved authentication state.
10. **Waiting with `time.sleep`.** Use `expect_popup`, `wait_for_event`, and assertions.
11. **Not distinguishing dialogs from windows.** Dialogs use `page.on("dialog")`; windows use popup/page events.
12. **Catching the wrong page in `context.expect_page()`.** If multiple pages might open at once, filter by URL after capture or use `page.expect_popup()` for a tighter scope.

**Best practices:** wrap capture logic in small helpers; assert on title/URL/heading to confirm you got the intended page; close what you open; use contexts for separation; keep browser state assumptions explicit.

---

## Mini Practice Exercises

### Exercise 1: First popup

Using the setup from this lesson, click "Terms" and assert the new tab's heading. Then close it. *Hint:* `expect_popup`.

### Exercise 2: Count the tabs

Write a test that asserts `len(context.pages)` is 1 at the start, 2 after clicking Terms, and 1 after closing the popup.

<details>
<summary>Solution</summary>

```python
assert len(context.pages) == 1
with page.expect_popup() as info:
    page.get_by_role("link", name="Terms").click()
assert len(context.pages) == 2
info.value.close()
assert len(context.pages) == 1
```
</details>

### Exercise 3: Attribute check versus click

Write two tests for the Terms link: (a) assert `target="_blank"` and the `href` ends with `/terms`; (b) click it and assert the new tab's title. Discuss when (a) is enough.

### Exercise 4: Same-tab or new tab?

For the About link, write a test using `wait_for_url`. Then deliberately wrap it in `expect_popup(timeout=2000)` and observe the timeout error. Why does it happen? *Answer:* no popup is ever created.

### Exercise 5: Two users

Using `set_content` pages (or the routed pages), create two contexts and prove cookies are isolated. Then put both pages in the *same* context and prove they share cookies.

### Exercise 6: Practice site

On `https://the-internet.herokuapp.com/windows`, click "Click Here". Capture the new window, assert its heading is "New Window", close it, and verify the original page heading is "Opening a new window".

<details>
<summary>Solution</summary>

```python
page.goto("https://the-internet.herokuapp.com/windows")
with page.expect_popup() as info:
    page.get_by_role("link", name="Click Here").click()
new = info.value
expect(new.get_by_role("heading", name="New Window")).to_be_visible()
new.close()
expect(page.get_by_role("heading", name="Opening a new window")).to_be_visible()
```
</details>

### Exercise 7 (stretch): Login pop-up

Extend the pop-up login example so the login pop-up has an email field and the opener displays "Welcome, <email>". Use `with login.expect_event("close"):` around the approve click.

---

## Summary / Key Takeaways

- A Playwright `Page` represents a tab *or* a window. A `BrowserContext` groups pages that share cookies and storage; separate contexts are isolated.
- There is no "switch window". Hold the `Page` object you need and use it directly.
- Capture new tabs with the **register-then-act** pattern: `with page.expect_popup() as info: ...click...; popup = info.value`. Use `context.expect_page()` when the opener relationship is unclear.
- Verify you have the right page with title, URL, or heading assertions; they also act as waits.
- Use `wait_for_url` for same-tab navigation, `wait_for_event("close")` for self-closing popups, `context.pages` for inspection.
- Use separate contexts to simulate multiple users; use shared context tabs to simulate one user.
- Attach routes and listeners on the context so every tab inherits them.
- Fixtures that give each test a fresh context and Page Objects that wrap multi-tab flows are covered in depth on Wednesday.

---

## External Resources

- Playwright Python docs, Pages (multiple pages, popups): https://playwright.dev/python/docs/pages
- Playwright Python docs, Browser contexts: https://playwright.dev/python/docs/browser-contexts
- Playwright Python API reference, Page (`expect_popup`): https://playwright.dev/python/docs/api/class-page#page-wait-for-event
- Playwright Python API reference, BrowserContext (`expect_page`): https://playwright.dev/python/docs/api/class-browsercontext
