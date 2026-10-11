# Frames and Nested Frames

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an `<iframe>` is, why websites use them, and why they behave like "a page inside a page" for automation.
- Describe why a locator on the main page cannot "see" elements inside a frame, and recognise the symptoms of that mistake.
- Use `page.frame_locator()` to interact with elements inside a frame, and understand why this is the recommended approach.
- Chain `frame_locator()` calls to reach elements inside nested frames (a frame inside a frame inside a page).
- Use the lower-level `page.frame()`, `page.frames`, and `locator.content_frame` APIs when you need a `Frame` object, and know when each tool is appropriate.
- Combine frame handling with the auto-waiting and assertion features you already know (`expect`).
- Debug the most common frame-related failures: wrong selector for the frame, strict-mode violations, frames that load late, and cross-origin frames.
- Write small, readable helper functions so frame logic does not clutter your tests.

---

## Why This Matters

This week's epic is to master *complex UI interactions* in Playwright. On Monday you learned to handle individual controls: dialogs, checkboxes, radio buttons, dropdowns, keyboard and mouse actions, and auto-suggestions. Those skills assume the control lives in the page you are driving. Real applications are rarely that tidy.

Frames are everywhere in production software:

- **Payment forms.** Card number fields from providers such as Stripe or PayPal are served inside an iframe so that the merchant's site never touches raw card data.
- **Rich text editors.** Many WYSIWYG editors (for example TinyMCE in its classic mode) render the editable area inside an iframe.
- **Embedded widgets.** Maps, video players, chat widgets, CAPTCHA boxes, ads, and consent banners are frequently iframes.
- **Legacy applications.** Older enterprise portals are often built from `<frameset>` or nested iframes: a navigation frame, a content frame, and a header frame.

For your **Project 1 - QE Foundations** deliverable, you will automate UI flows that look much like real products. If your tests cannot enter a frame, a whole category of user journeys (checkout, editing, embedded forms) is simply untestable. Knowing how to reach inside a frame, and how to do it in a way that is stable rather than flaky, is a core skill for a Quality Engineer.

---

## The Concept

### 1. What is a frame?

An **iframe** (inline frame) is an HTML element that embeds another complete HTML document inside the current one.

```html
<h1>My Shop</h1>
<iframe id="payment" src="https://payments.example.com/card-form"></iframe>
```

The embedded document has its own:

- DOM tree (its own `<html>`, `<head>`, `<body>`),
- JavaScript global scope (its own `window`),
- CSS (styles from the outer page do not leak in),
- URL and navigation history.

Think of it like a **picture-in-picture TV**. The big screen is the main page. The small window in the corner is a different channel with its own remote control. If you press buttons on the main remote (the main page's locators), the small channel does not respond; you need to point at the small screen explicitly.

Playwright's own vocabulary:

| Term | Meaning |
| --- | --- |
| **Page** | A browser tab. |
| **Frame** | A document inside a page. Every page has exactly one **main frame** (the top-level document) and zero or more **child frames** (iframes). |
| **FrameLocator** | A Playwright object that represents "the iframe element matched by this selector" and lets you build locators *inside* it. |
| **Nested frame** | A frame that is itself inside another frame. |

### 2. Why locators on `page` cannot see inside frames

When you write:

```python
page.get_by_role("button", name="Pay now").click()
```

Playwright searches the DOM of the **main frame**. An `<iframe>` element appears in that DOM as a single opaque element. Its *contents* belong to another document, so they are invisible to the main frame's query. The result is a timeout that looks like this:

```
playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded.
Call log:
  - waiting for get_by_role("button", name="Pay now")
```

This is the single most common beginner error with frames. If you see "waiting for ..." and the element is clearly on the screen, ask yourself: *"Is this inside an iframe?"* You can check in your browser's DevTools: if the Elements panel shows a `#document` node inside an `<iframe>` element, you are in a frame.

### 3. The modern solution: `frame_locator()`

`page.frame_locator(selector)` returns a **FrameLocator**. From it, you use the *same* locator methods you already know: `locator()`, `get_by_role()`, `get_by_label()`, `get_by_text()`, `get_by_placeholder()`, and so on.

```python
card = page.frame_locator("iframe#payment")
card.get_by_label("Card number").fill("4242 4242 4242 4242")
card.get_by_role("button", name="Pay now").click()
```

Why is this the recommended approach?

1. **It is lazy.** Like all Playwright locators, a `FrameLocator` does not look up the iframe when you create it. It resolves the iframe *each time* you use it. If the frame reloads or is re-created, your locator still works. (With old-style frame handles you could end up holding a reference to a detached frame.)
2. **It auto-waits.** Playwright waits for the iframe element to appear, then for the element inside it to satisfy the usual actionability checks (visible, stable, enabled, receives events).
3. **It composes.** You can chain `frame_locator()` for nested frames and use `filter`, `nth`, and the other locator features.
4. **It works with `expect`.** Assertions retry until they pass or time out.

### 4. Choosing the right selector for the iframe itself

The selector you pass to `frame_locator()` identifies the `<iframe>` *element* in the outer page. Good options, from most to least preferred:

| Selector | Example | Notes |
| --- | --- | --- |
| `title` attribute | `page.frame_locator('iframe[title="Secure card payment"]')` | Accessible iframes should have a title; this is stable and meaningful. |
| `data-testid` | `page.frame_locator('[data-testid="checkout-frame"]')` | Best if the dev team adds test ids. |
| `id` / `name` | `page.frame_locator("#payment")` or `'iframe[name="card"]'` | Fine if they are stable (not auto-generated). |
| `src` partial match | `page.frame_locator('iframe[src*="payments"]')` | Useful for third-party frames. |
| Position | `page.frame_locator("iframe").first` / `.nth(1)` | Fragile; use only as a last resort. |

Beware of auto-generated ids such as `iframe#frame-8f3a91c`; they change on every page load. Prefer anything meaningful and stable.

> **Strictness:** like normal locators, `frame_locator()` is strict. If your selector matches **two** iframes and you then perform an action, Playwright raises a strict mode violation. Make the selector more specific, or choose explicitly with `.first`, `.last`, or `.nth(n)`.

### 5. Nested frames

A nested frame is a frame inside a frame. You reach it by chaining:

```python
inner = page.frame_locator("#outer").frame_locator("#inner")
inner.get_by_text("Hello from the inside").click()
```

Read it from left to right: "on the page, go into the iframe `#outer`, then inside that document, go into the iframe `#inner`, then find this text."

The classic practice page `the-internet.herokuapp.com/nested_frames` uses a `<frameset>` (an older construct). There, the top frame contains three child frames (left, middle, right) and a separate bottom frame. Playwright handles these too, using `page.frame(name="frame-top")` and similar, which we will look at shortly.

### 6. The lower-level API: `Frame` objects

Sometimes you want a **Frame** object rather than a FrameLocator, for example to:

- read the frame's URL (`frame.url`),
- evaluate JavaScript in that frame's context,
- wait for the frame to finish loading (`frame.wait_for_load_state()`),
- enumerate every frame on the page for debugging.

The relevant APIs:

```python
page.main_frame              # the top-level Frame
page.frames                  # list of every Frame (main + all nested)
page.frame(name="card")      # find a frame by its name attribute
page.frame(url="**/card-form*")   # find a frame by URL (glob or regex)
frame.child_frames           # direct children of a frame
frame.parent_frame           # parent Frame (None for main frame)
frame.name                   # the name attribute of the frame
frame.url                    # the current URL
```

A `Frame` object has the same locator methods as `Page`: `frame.locator()`, `frame.get_by_role()`, and so on.

There is also a bridge between the two worlds:

- `frame_locator.owner` gives you a regular `Locator` pointing at the `<iframe>` element itself (useful for asserting on the iframe's visibility or attributes).
- `locator.content_frame` (available in current Playwright versions; check the docs for the version you installed) turns a Locator that points at an `<iframe>` into a `FrameLocator`.
- `element_handle.content_frame()` returns a `Frame` from an element handle (element handles are discouraged for most work, but this is a legitimate use).

**Rule of thumb:** use `frame_locator()` by default. Reach for `page.frame()` only when you truly need a `Frame` object, and remember that a Frame object is a *snapshot reference*. If the frame navigates or is replaced, you may need to fetch it again.

### 7. Frames and auto-waiting

Frame loading is asynchronous. The iframe element can exist in the page long before its content has loaded. Playwright's locators already handle this: the action waits (up to the timeout) for the element to appear *inside* the frame. You do **not** need `time.sleep()`.

What you should still verify is that you are asserting about the right thing. For example, to confirm the payment frame has rendered:

```python
expect(page.frame_locator("#payment").get_by_label("Card number")).to_be_visible()
```

### 8. Cross-origin frames

Browsers enforce the **same-origin policy**: JavaScript on `shop.example.com` cannot normally reach into an iframe served from `payments.example.com`. This is a security feature, and it is why your own page scripts cannot touch a third-party payment form.

Playwright is *not* subject to this restriction, because it controls the browser from the outside via its automation protocol. `frame_locator()` works the same on cross-origin frames as on same-origin ones. This is a key advantage over some older tools.

Limitations to be aware of:

- Third-party frames (CAPTCHAs, 3-D Secure bank pages) are often designed to detect and block automation. You may not be able to complete them in a test, and you generally should not try. In test environments, ask for a **test mode** or a stubbed provider (e.g., test card numbers, a CAPTCHA that always passes).
- Third-party frames can change their markup without warning. Keep selectors minimal and keep frame logic in one place (a helper or page object, which we will build on Wednesday).

---

## Code Examples

All examples in this lesson are **self-contained**: they build their own tiny pages with `page.set_content()` so you can run them without any external website. Use the same pattern for your own experiments.

> **Note on `set_content` and frames:** `set_content()` accepts an HTML string. An iframe can carry its own HTML via the `srcdoc` attribute. The browser treats `srcdoc` content as a separate document, so this faithfully reproduces the frame behaviour you will see in real applications.

### Example 1: The problem, and the fix

```python
from playwright.sync_api import sync_playwright, expect

HTML = """
<h1>My Shop</h1>
<button id="outer-btn">Outer button</button>
<iframe id="payment" title="Secure card payment" srcdoc="
  <label for='card'>Card number</label>
  <input id='card' type='text'>
  <button id='pay'>Pay now</button>
  <p id='msg'></p>
  <script>
    document.getElementById('pay').addEventListener('click', () => {
      document.getElementById('msg').textContent =
        'Paid with ' + document.getElementById('card').value;
    });
  </script>
"></iframe>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(HTML)

    # 1) A main-page locator cannot see inside the iframe.
    print(page.get_by_role("button", name="Pay now").count())   # 0

    # 2) frame_locator gets us inside.
    card = page.frame_locator('iframe[title="Secure card payment"]')
    card.get_by_label("Card number").fill("4242 4242 4242 4242")
    card.get_by_role("button", name="Pay now").click()
    expect(card.locator("#msg")).to_have_text("Paid with 4242 4242 4242 4242")

    browser.close()
```

**Line-by-line explanation**

- `from playwright.sync_api import sync_playwright, expect`: imports the synchronous API entry point and the `expect` assertion helper. "Sync" means each call blocks until it finishes, which is easiest for beginners to read.
- `HTML = """ ... """`: a triple-quoted Python string holding our test page. It contains an outer button and an iframe.
- `<iframe id="payment" title="Secure card payment" srcdoc="...">`: the iframe. `srcdoc` supplies the inner HTML inline. Inside it we have a labelled input, a button, a paragraph for output, and a small script that writes the card value into the paragraph when the button is clicked.
- `with sync_playwright() as p:`: starts Playwright and guarantees clean shutdown when the block ends.
- `browser = p.chromium.launch()`: launches headless Chromium. (Pass `headless=False` to watch it run.)
- `page = browser.new_page()`: opens a new tab in a fresh, isolated browser context.
- `page.set_content(HTML)`: loads our HTML string into the page.
- `page.get_by_role("button", name="Pay now").count()`: asks the **main frame** how many matching buttons exist. It prints `0`, proving the main page cannot see inside the iframe. Notice that `count()` does not wait, which is why it is useful for demonstrating "does this exist right now?".
- `card = page.frame_locator('iframe[title="Secure card payment"]')`: creates a FrameLocator for the iframe whose `title` attribute matches. Nothing is fetched yet; it is just a description.
- `card.get_by_label("Card number").fill(...)`: finds the input by its label text *inside the frame* and types the value. `fill` waits for the element to be visible, enabled, and editable.
- `card.get_by_role("button", name="Pay now").click()`: clicks the button inside the frame.
- `expect(card.locator("#msg")).to_have_text(...)`: a web-first assertion. It retries until the paragraph's text equals the expected string or the timeout (5 seconds by default for `expect`) expires.
- `browser.close()`: releases the browser.

### Example 2: Nested frames

Writing nested `srcdoc` strings by hand gets ugly because quotes must be escaped at each level. A cleaner approach for tests is to use `page.route()` to serve three tiny pages from memory (routing is revisited in later weeks; for now treat it as a convenient way to build test pages):

```python
from playwright.sync_api import sync_playwright, expect

PAGES = {
    "/outer": "<h1>Outer</h1><iframe id='outer-frame' src='/middle'></iframe>",
    "/middle": "<h2>Middle</h2><iframe id='inner-frame' src='/inner'></iframe>",
    "/inner": (
        "<button id='deep'>Deep button</button><p id='out'></p>"
        "<script>document.getElementById('deep').onclick = "
        "() => { document.getElementById('out').textContent = 'clicked deep'; }"
        "</script>"
    ),
}

def serve(route):
    path = route.request.url.replace("http://test.local", "")
    route.fulfill(status=200, content_type="text/html", body=PAGES[path])

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.route("http://test.local/**", serve)
    page.goto("http://test.local/outer")

    deep = (
        page.frame_locator("#outer-frame")   # step into the middle document
            .frame_locator("#inner-frame")   # step into the inner document
    )
    deep.get_by_role("button", name="Deep button").click()
    expect(deep.locator("#out")).to_have_text("clicked deep")

    print([f.url for f in page.frames])
    browser.close()
```

**Line-by-line explanation**

- `PAGES = {...}`: a dictionary mapping URL paths to HTML bodies. `/outer` embeds `/middle`; `/middle` embeds `/inner`. This creates a genuine two-level nesting.
- The inner page has a button whose `onclick` writes into a paragraph. Because we use `.onclick = () => {...}` there is no quote-escaping problem.
- `def serve(route):`: a **route handler**. Playwright calls it for each request that matches the route pattern.
- `route.request.url.replace("http://test.local", "")`: strips the fake host so we are left with `/outer`, `/middle`, or `/inner`.
- `route.fulfill(status=200, content_type="text/html", body=PAGES[path])`: answers the request with our own HTML, so no real network or server is needed.
- `page.route("http://test.local/**", serve)`: registers the handler for every URL under the fake host. The `**` glob matches any path.
- `page.goto("http://test.local/outer")`: navigates; the browser requests `/outer`, then discovers the iframes and requests `/middle` and `/inner`, all served by our handler.
- `page.frame_locator("#outer-frame").frame_locator("#inner-frame")`: the nested chain. The second `frame_locator` searches for `#inner-frame` *inside the outer iframe's document*, not the main page.
- `.get_by_role("button", name="Deep button").click()`: final target inside the innermost frame.
- `expect(deep.locator("#out")).to_have_text("clicked deep")`: confirms the click had an effect.
- `[f.url for f in page.frames]`: a list comprehension that prints the URL of every frame (main, middle, inner). This is a handy debugging trick when you are unsure how many frames exist.

You do not need to master `page.route` today; treat it as a convenient tool for building test pages. Focus on the `frame_locator` chain.

### Example 3: Using the `Frame` API (`page.frame`, `page.frames`)

```python
from playwright.sync_api import sync_playwright

HTML = """
<iframe name="left"  srcdoc="<p id='who'>I am LEFT</p>"></iframe>
<iframe name="right" srcdoc="<p id='who'>I am RIGHT</p>"></iframe>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(HTML)

    # Enumerate every frame for debugging
    for f in page.frames:
        print(repr(f.name), f.url)

    left = page.frame(name="left")
    right = page.frame(name="right")

    print(left.locator("#who").inner_text())    # I am LEFT
    print(right.locator("#who").inner_text())   # I am RIGHT

    # Navigation tree
    print(left.parent_frame == page.main_frame)  # True
    browser.close()
```

**Line-by-line explanation**

- `<iframe name="left" ...>`: the `name` attribute is what `page.frame(name=...)` matches. Note it is the **name** attribute, not the id.
- `for f in page.frames:`: iterates all frames. The main frame has an empty name (`''`) and URL `about:blank` (because we used `set_content`). The children show `about:srcdoc`.
- `page.frame(name="left")`: returns the `Frame` object, or `None` if no frame matches. Always remember that it can be `None`; if you call a method on `None` you get an `AttributeError`, which hides the real problem (the frame was not found). In real tests you might write `assert left is not None, "left frame not found"`.
- `left.locator("#who").inner_text()`: `Frame` supports `locator()` just like `Page`. `inner_text()` returns the visible text. Both frames use the same id `who`, but because each lives in its own document there is no clash.
- `left.parent_frame == page.main_frame`: demonstrates the tree relationship.

**Important caveat:** `page.frame(name="left")` is evaluated *immediately*. If the iframe has not been attached yet, it returns `None`. FrameLocator does not have this problem because it waits. That is another reason to prefer `frame_locator()`.

### Example 4: Bridging from a Locator to a frame

```python
iframe_element = page.locator("iframe[name='left']")
expect(iframe_element).to_be_visible()                # assert on the iframe element itself

frame_loc = page.frame_locator("iframe[name='left']")
expect(frame_loc.owner).to_have_attribute("name", "left")
```

- `page.locator("iframe[name='left']")` treats the `<iframe>` as a normal element in the outer page, which is useful for checks such as visibility, size, or attributes.
- `frame_loc.owner` is the reverse: given a FrameLocator, get the Locator for the iframe element itself.

### Example 5: A reusable helper

```python
from playwright.sync_api import Page, FrameLocator

def payment_frame(page: Page) -> FrameLocator:
    """Return the FrameLocator for the secure payment iframe."""
    return page.frame_locator('iframe[title="Secure card payment"]')

def pay(page: Page, card_number: str) -> None:
    frame = payment_frame(page)
    frame.get_by_label("Card number").fill(card_number)
    frame.get_by_role("button", name="Pay now").click()
```

- `Page` and `FrameLocator` are imported only for **type hints**. They tell readers (and your editor) what each function accepts and returns; Python itself ignores them at runtime.
- The selector for the iframe lives in *one* place. If a developer renames the title, you fix one line, not twenty tests. This is the seed of the Page Object Model, which is covered in depth on Wednesday.

### Example 6: Filtering and picking among several frames

```python
frames = page.locator("iframe")
print(frames.count())

# Choose the frame whose title contains "ad"
ad = page.frame_locator("iframe").nth(0)

# Or narrow it to a single iframe with a more specific CSS selector
chat = page.frame_locator("iframe[src*='chat']")
chat.get_by_placeholder("Type a message").fill("Hello")
```

`page.frame_locator("iframe")` matches *all* iframes; actions will raise a strict mode error unless you narrow it. `.nth(0)` is zero-based. `iframe[src*='chat']` is a CSS **attribute selector**: `*=` means "contains".

---

## Real-World Scenarios

### Scenario 1: Checkout with a hosted payment field

An e-commerce site shows a "Card number" box that is really an iframe hosted by the payment provider. Your test must:

1. Add a product to the cart (main page).
2. Fill shipping details (main page).
3. Enter card details (inside iframe).
4. Click "Place order" (main page) and assert the confirmation.

Notice that a single test switches **context** several times. With `frame_locator`, there is nothing to "switch back" from; you simply use `page` for the main page and `frame` for the iframe. This is a significant improvement over the older Selenium pattern (`switch_to.frame()` followed by `switch_to.default_content()`), where forgetting to switch back is a classic bug.

```python
def test_checkout(page):
    page.goto("/checkout")
    page.get_by_label("Email").fill("student@example.com")
    pay_frame = page.frame_locator("iframe[title='Secure card number']")
    pay_frame.get_by_placeholder("Card number").fill("4242424242424242")
    page.get_by_role("button", name="Place order").click()   # back on main page, no switching
    expect(page.get_by_role("heading", name="Thank you")).to_be_visible()
```

### Scenario 2: A rich text editor

An editor's content area is an iframe whose `<body>` is `contenteditable`. To type a blog post:

```python
editor = page.frame_locator("iframe.editor-area").locator("body")
editor.click()
editor.press_sequentially("Hello, world!")          # types character by character
expect(editor).to_contain_text("Hello, world!")
```

`press_sequentially` sends real key events one at a time (it replaced the older `type` method). Use `fill()` when you only need to set the value; use `press_sequentially()` when the application listens for individual key events.

### Scenario 3: Legacy portal with a frameset

Old admin portals use `<frameset>` with named frames such as `frame-top` and `frame-bottom`. The `page.frame(name="frame-bottom")` approach is convenient here because the names are stable and static.

```python
page.goto("https://the-internet.herokuapp.com/nested_frames")
top = page.frame(name="frame-top")
print([f.name for f in top.child_frames])             # ['frame-left', 'frame-middle', 'frame-right']
print(page.frame(name="frame-bottom").locator("body").inner_text())   # BOTTOM
print(page.frame(name="frame-middle").locator("#content").inner_text())  # MIDDLE
```

`child_frames` returns the direct children in document order. `page.frame(name=...)` searches *all* frames in the page, not only top-level ones, so you can fetch `frame-middle` directly without walking down from `frame-top`.

### Scenario 4: Dynamic iframes that appear after an action

A chat widget loads its iframe only after the user clicks a launcher button. `frame_locator` is lazy, so you can click and interact immediately:

```python
page.get_by_role("button", name="Chat with us").click()
chat = page.frame_locator("iframe[title='Chat']")
chat.get_by_role("textbox").fill("Where is my order?")
chat.get_by_role("button", name="Send").click()
expect(chat.get_by_text("Thanks for contacting us")).to_be_visible()
```

No explicit wait is needed; each step auto-waits for the frame and the element.

---

## Common Pitfalls and Best Practices

1. **Forgetting the frame entirely.** Symptom: timeouts on elements you can see. Fix: inspect the DOM for `<iframe>`/`#document`. In the Playwright **Inspector** or **codegen**, the generated code will include `frame_locator` automatically if the element is inside a frame (try `playwright codegen`).
2. **Matching more than one iframe.** Symptom: strict mode violation. Fix: narrow the selector, or pick `.first`/`.nth()` deliberately and leave a comment explaining why.
3. **Using auto-generated ids.** Prefer `title`, `name`, `data-testid`, or stable `src` fragments.
4. **Using `page.frame()` for something that loads late.** It returns `None` immediately if the frame is not attached yet. Use `frame_locator()` for anything dynamic. If you really need a `Frame`, wait for it first, for example with `page.wait_for_selector("iframe#x")` (or assert on `page.locator("iframe#x")`) and then call `page.frame(...)`, or use `page.wait_for_event("framenavigated")`.
5. **Holding on to stale Frame objects.** A `Frame` that was navigated away or removed can raise errors like "Frame was detached". Re-fetch it, or use `FrameLocator`.
6. **Expecting frame logic to persist.** Unlike Selenium, there is no "current frame" state in Playwright. Every locator is explicit about where it searches. This is a feature: you cannot accidentally be "stuck" in a frame.
7. **Asserting on the wrong thing.** `expect(page.get_by_text("Done")).to_be_visible()` fails if "Done" is inside the frame. Make sure the `expect` receives a locator from the right context.
8. **Fighting a protected third-party frame.** If it blocks automation (CAPTCHA, bank 3-D Secure), do not try to defeat it; use a test configuration or mock the provider.
9. **Overlong chains in tests.** Wrap frame chains in helpers or fixtures so the tests read like business steps, not DOM paths.
10. **Sleeping.** `time.sleep(3)` after opening a frame is both slow and unreliable. Rely on auto-waiting and `expect`.

### Debugging checklist

- Print `[f.url for f in page.frames]` to see what frames actually exist.
- Run with `PWDEBUG=1` (environment variable) or use `page.pause()` to open the Playwright Inspector and use "Pick locator"; it understands frames.
- Use `playwright codegen <url>` to see what Playwright generates for your clicks.
- Check the **trace viewer** (`context.tracing.start(...)` / `playwright show-trace`), which shows the DOM snapshot for each step, including frame contents.

---

## Mini Practice Exercises

Use `page.set_content()` or the practice site `https://the-internet.herokuapp.com/` for these.

### Exercise 1: First frame interaction (warm-up)

Create a page with an iframe (`title="Newsletter"`) containing an email input and a "Subscribe" button that writes "Subscribed: <email>" into a paragraph. Write a test that fills the email, clicks Subscribe, and asserts the paragraph text.

*Hint:* Copy Example 1 and change the labels. Use `get_by_label` for the input and `get_by_role("button", name="Subscribe")`.

<details>
<summary>Solution sketch</summary>

```python
HTML = """
<iframe title="Newsletter" srcdoc="
  <label>Email <input id='e' type='email'></label>
  <button onclick=&quot;document.getElementById('m').textContent='Subscribed: '+document.getElementById('e').value&quot;>Subscribe</button>
  <p id='m'></p>">
</iframe>
"""
page.set_content(HTML)
f = page.frame_locator("iframe[title='Newsletter']")
f.get_by_label("Email").fill("a@b.com")
f.get_by_role("button", name="Subscribe").click()
expect(f.locator("#m")).to_have_text("Subscribed: a@b.com")
```

`&quot;` is an HTML entity for a double quote; it is needed because the `srcdoc` attribute itself is wrapped in double quotes.
</details>

### Exercise 2: Two iframes, one test

Build a page with two iframes (`name="a"` and `name="b"`), each containing `<input id="x">`. Fill `a` with "one" and `b` with "two", then read both values back with `input_value()`.

*Hint:* Use two separate FrameLocators, or `page.frame(name="a")`. Remember both inputs share an id; the frame boundary keeps them apart.

<details>
<summary>Solution sketch</summary>

```python
page.set_content("""
<iframe name="a" srcdoc="<input id='x'>"></iframe>
<iframe name="b" srcdoc="<input id='x'>"></iframe>
""")
page.frame_locator("iframe[name='a']").locator("#x").fill("one")
page.frame_locator("iframe[name='b']").locator("#x").fill("two")
assert page.frame_locator("iframe[name='a']").locator("#x").input_value() == "one"
assert page.frame_locator("iframe[name='b']").locator("#x").input_value() == "two"
```
</details>

### Exercise 3: Nested frames on a real practice site

Visit `https://the-internet.herokuapp.com/nested_frames`. Print the text of the LEFT, MIDDLE, RIGHT, and BOTTOM frames.

*Hint:* This page uses a `<frameset>`, so use `page.frame(name="frame-left")` and similar names (`frame-middle`, `frame-right`, `frame-bottom`). Read `body` text with `.locator("body").inner_text()`.

### Exercise 4: Rich text editor

On `https://the-internet.herokuapp.com/iframe`, an editor sits inside an iframe with id `mce_0_ifr`. Clear the default text, type your own sentence, and assert it appears.

*Hint:* `page.frame_locator("#mce_0_ifr").locator("#tinymce")`. Use `.fill("...")` on that body element. Dismiss any banner the editor shows if it blocks the page (you learned about dialogs on Monday; this one is an on-page notice, not a browser dialog, so a normal `click()` will do).

### Exercise 5: Refactor

Take your solution to Exercise 4 and extract a function `editor(page)` that returns the Locator for the editor body, plus `write(page, text)` and `read(page)`. Add a test that uses only those helpers.

*Hint:* Compare to Example 5.

### Exercise 6 (stretch): Debug a broken test

The following code times out. Explain why and fix it.

```python
page.set_content("<iframe id='f' srcdoc=\"<button>Go</button>\"></iframe>")
page.get_by_role("button", name="Go").click(timeout=2000)
```

*Answer:* the button is inside an iframe, so a page-level locator cannot find it. Use `page.frame_locator("#f").get_by_role("button", name="Go").click()`.

---

## Summary / Key Takeaways

- An iframe is a separate document inside your page. Locators on `page` search only the main frame.
- `page.frame_locator(selector)` is the default, recommended tool. It is lazy, auto-waiting, and chainable.
- Chain `frame_locator().frame_locator()` for nested frames; read the chain left to right as "go into... then go into...".
- `page.frame(name=...)`, `page.frames`, `frame.child_frames`, `frame.parent_frame` give you `Frame` objects, which are useful for inspection, framesets, and evaluating JavaScript, but are evaluated immediately and can go stale.
- Playwright works across origins; there is no "switch to frame" state to manage or forget.
- Choose stable iframe selectors (`title`, `data-testid`, stable `name`/`id`, `src*=`), keep them in helpers, and avoid sleeps.
- Frame skills are directly applicable to your **Project 1 - QE Foundations** UI tests; you will build on them with Page Objects and fixtures, which are covered in depth on Wednesday.

---

## External Resources

- Playwright Python docs, Frames: https://playwright.dev/python/docs/frames
- Playwright Python API reference, FrameLocator: https://playwright.dev/python/docs/api/class-framelocator
- Playwright Python API reference, Frame: https://playwright.dev/python/docs/api/class-frame
- MDN Web Docs, the `<iframe>` element: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe
