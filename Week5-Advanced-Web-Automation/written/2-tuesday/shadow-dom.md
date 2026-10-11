# Shadow DOM

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what the Shadow DOM is, why browsers have it, and how it differs from the regular ("light") DOM and from iframes.
- Recognise a shadow host and shadow root in Chrome DevTools, and tell **open** from **closed** shadow roots.
- Explain how Playwright's locators automatically **pierce open shadow roots** so that CSS selectors, `get_by_role`, `get_by_text`, `get_by_label`, and similar locators work without any special syntax.
- Identify what does *not* pierce shadow DOM (XPath, `document.querySelector` inside `evaluate`) and how to work around it.
- Use `css:light` and other tools when you *want* to avoid piercing.
- Handle **slots** (light DOM content projected into a shadow tree) and nested shadow roots (a web component inside another).
- Use `evaluate` to inspect `shadowRoot`, and understand why closed roots are largely off-limits.
- Debug shadow-DOM-related failures and work with developers to make components testable (`data-testid`, accessible roles).

---

## Why This Matters

Modern front-end development increasingly relies on **web components**: reusable custom HTML elements such as `<date-picker>`, `<user-card>`, `<ui-button>`, or `<sl-dialog>`. Design systems from large companies (Salesforce Lightning Web Components, Shoelace, Material Web, Ionic, and many internal libraries) ship their widgets as web components using Shadow DOM so that styles and structure are protected from the rest of the page.

For a Quality Engineer the consequence is serious: **elements that are plainly on the screen may be hidden from naive tools.** In older frameworks (and in plain JavaScript using `document.querySelector`), the contents of a shadow root cannot be reached by ordinary selectors. A test that worked fine on a traditional site suddenly cannot find a button inside a web component. The tester sees the button, DevTools shows the button, but the script cannot find it.

The Week 5 epic is about mastering *complex UI interactions*. Shadow DOM is one of the "gotchas" that separates a beginner from a confident automation engineer, and it can appear in the UI you automate for **Project 1 - QE Foundations** if your practice application uses component libraries. The good news, which this lesson will make concrete, is that Playwright was designed to handle it: most of the time everything "just works". Your job is to understand *why* it works, so that on the day it does not, you know where to look.

---

## The Concept

### 1. The three DOMs: light, shadow, and iframe

You have already met one way of embedding content: an **iframe** is a *separate document* with its own `window`, loaded in its own browsing context (today's first lesson). Shadow DOM is different. It is a way of hiding part of the *same document's* tree behind a boundary.

| Feature | Regular (light) DOM | Shadow DOM | iframe |
| --- | --- | --- | --- |
| Same document and `window`? | Yes | Yes | No (separate document) |
| CSS from outer page applies inside? | Yes | **No** (encapsulated) | No |
| `document.querySelector` finds inside? | Yes | **No** (boundary) | No |
| Scripts share globals with outer page? | Yes | Yes | No |
| Playwright needs special handling? | No | **No** (open roots pierced automatically) | Yes (`frame_locator`) |

A helpful analogy: the light DOM is the open-plan office. An iframe is a different company in a separate building with its own entrance. Shadow DOM is a **glass-walled meeting room** inside your office: you can see in, you are in the same building, but your office-wide announcements (global CSS and global `querySelector` calls) do not reach inside.

### 2. Vocabulary

```html
<user-card name="Maria"></user-card>
```

- **Custom element**: an HTML tag defined by JavaScript (`customElements.define('user-card', ...)`). Custom element names must contain a hyphen.
- **Shadow host**: the element that *has* a shadow tree attached, here `<user-card>`.
- **Shadow root**: the root of the hidden tree, attached with `host.attachShadow({mode: 'open'})`.
- **Shadow tree**: the elements living in the shadow root: its own markup, `<style>`, and so on.
- **Light DOM**: the regular child nodes of the host, as written in the page's HTML.
- **Slot**: a placeholder `<slot></slot>` in the shadow tree where light DOM children are *projected* (displayed).

In DevTools you see this as:

```
<user-card name="Maria">
  #shadow-root (open)
     <style>...</style>
     <h2>Maria</h2>
     <button class="follow">Follow</button>
</user-card>
```

The `#shadow-root (open)` node is the giveaway.

### 3. Open versus closed

`attachShadow({mode: 'open'})` creates an **open** shadow root: JavaScript can reach it through `host.shadowRoot`. `attachShadow({mode: 'closed'})` creates a **closed** root: `host.shadowRoot` returns `null`, and external code cannot reach the tree through the standard API.

| Mode | `host.shadowRoot` | Playwright locators |
| --- | --- | --- |
| open | the root | Pierce automatically |
| closed | `null` | Generally cannot reach; see Section 9 |

The vast majority of component libraries (including Shoelace, Material Web, Ionic, and Lightning Web Components in most configurations) use **open** roots. You will rarely meet closed ones.

### 4. Why it "just works" in Playwright

Playwright's selector engines are designed to **pierce open shadow roots by default**. Concretely:

- **CSS locators** (`page.locator("css=...")` or just `page.locator("button.follow")`) look inside open shadow roots as well as the light DOM. This differs from the browser's own `querySelector`.
- **Text, role, label, placeholder, alt text, title, and test-id locators** (`get_by_text`, `get_by_role`, `get_by_label`, `get_by_placeholder`, `get_by_alt_text`, `get_by_title`, `get_by_test_id`) also pierce.
- **Chaining and filtering** work as normal: `page.locator("user-card").filter(has_text="Maria")`.

So for an open shadow root, you write exactly the code you would write if the shadow boundary did not exist:

```python
page.get_by_role("button", name="Follow").click()
page.locator("user-card button.follow").click()
page.locator("user-card").get_by_role("heading").inner_text()
```

That second selector, `user-card button.follow`, is worth studying. In plain CSS (as understood by the browser), a descendant combinator would *not* cross the shadow boundary. Playwright's CSS engine deliberately does. You can read it as "find a `button.follow` that is a descendant of a `user-card`, even if the path passes through a shadow root".

### 5. What does *not* pierce

1. **XPath.** `page.locator("//button")` does **not** pierce shadow roots. XPath works on the light DOM only. This is one of several reasons to avoid XPath in modern tests.
2. **Raw JavaScript** via `page.evaluate("document.querySelector('button')")`. The browser's `querySelector` does not cross shadow boundaries. You must walk through `host.shadowRoot` yourself (see Example 6).
3. **`css:light`**, which exists *to opt out* of piercing. When you write `page.locator("css:light=button")`, Playwright treats the selector like a plain browser `querySelector` and does not look into shadow roots. This is rarely required, but is useful if two identical elements exist and you intentionally want only the one in the light DOM.
4. **Closed shadow roots**, as discussed.

Also note: **`page.locator("css=my-element >> css=button")`** (the older `>>` chaining syntax) works with piercing too, but prefer the modern `.locator()` chaining or `.get_by_*` methods.

### 6. Slots: light DOM content displayed in the shadow tree

Web components often use slots so that the caller can pass content:

```html
<fancy-button>
  Save changes           <!-- light DOM child of the host -->
</fancy-button>
```

with a shadow tree such as:

```html
#shadow-root
  <button class="btn"><slot></slot></button>
```

The text "Save changes" is a *light DOM* node (a child of `<fancy-button>`), but it is *rendered* inside the `<button>`. For Playwright:

- `get_by_role("button", name="Save changes")` works: the accessibility tree computes the name from the slotted content.
- `get_by_text("Save changes")` works too.
- Clicking either one clicks the slot's rendered location (the button), because Playwright clicks at the element's visual centre.

You rarely need to think about slots when using Playwright, except when you assert on structure (`expect(host).to_contain_text("Save changes")` works as `to_contain_text` considers rendered/slotted text for the host element).

### 7. Nested shadow roots

Components contain components. A `<checkout-form>` may contain a `<payment-selector>` in its shadow tree, which contains a `<card-input>` in its own shadow tree. Piercing is recursive: a CSS selector reaches through *all* levels of open roots, so:

```python
page.locator("card-input input").fill("4242 4242 4242 4242")
```

works regardless of depth. If you want the path to be explicit (clearer to readers, and guards against duplicate matches), chain locators:

```python
page.locator("checkout-form").locator("payment-selector").locator("card-input").locator("input").fill("...")
```

### 8. Accessibility roles inside shadow DOM

`get_by_role` is built on the browser's accessibility tree, which composes the *flattened* tree (shadow DOM merged with light DOM and slots) the way assistive technology sees it. This is why role-based locators are the most robust choice for web components: they target what the *user* perceives, not how developers structured the tree. If a `<button>` inside a shadow root has no accessible name (an icon without a label), `get_by_role("button", name=...)` will not find it. That is also an accessibility bug worth reporting; as a stop-gap use `data-testid` or `aria-label`.

### 9. When piercing is not enough

- **Closed shadow root.** You cannot get inside using locators. Options, from best to worst:
  1. Ask developers to expose a stable interface: a `data-testid` on the *host*, ARIA attributes, public methods or properties.
  2. Test through the *host* element's public behaviour: click the host (`page.locator("my-widget").click()`), type with the keyboard after focusing the host, read host attributes, and assert on observable results elsewhere in the page.
  3. In a test build, configure the component to use open mode (some libraries have a flag).
  4. Use `add_init_script` to monkey-patch `Element.prototype.attachShadow` so every root is created open. This is a hack but has been used successfully:

```python
page.add_init_script("""
  const orig = Element.prototype.attachShadow;
  Element.prototype.attachShadow = function (init) {
    return orig.call(this, { ...init, mode: 'open' });
  };
""")
```

  It must be added **before** the page's scripts run (`add_init_script` runs at the start of every navigation). Use it sparingly, because a test that changes the component's mode no longer tests the exact production behaviour.

- **Performance with huge trees.** Piercing selectors search more nodes. Scope with a host locator (`page.locator("user-card")`) first for speed and clarity.

### 10. Debugging shadow DOM problems

1. Open DevTools and look for `#shadow-root (open)` or `(closed)` in the Elements panel.
2. In the console, check `document.querySelector('user-card').shadowRoot`. If it is `null` the root is closed (or the element has no shadow).
3. Use `playwright codegen`; it generates locators that account for shadow DOM.
4. Count matches: `print(page.locator("user-card button").count())`. Zero means a wrong selector; more than one means strictness errors on actions.
5. Use the Playwright Inspector's "Pick locator" feature, which works through shadow DOM.
6. Check whether the component is inside an **iframe** as well; shadow DOM and iframes can be combined (`frame_locator("iframe").locator("user-card button")`).

---

## Code Examples

All examples build a web component with `page.set_content()`. Scripts in `set_content` run, so the custom elements are defined for real.

### Example 1: A `user-card` component with an open shadow root

```python
from playwright.sync_api import sync_playwright, expect

HTML = """
<h1>Team</h1>
<user-card name="Maria Lopez"></user-card>
<user-card name="John Smith"></user-card>

<script>
  class UserCard extends HTMLElement {
    connectedCallback() {
      const root = this.attachShadow({ mode: 'open' });
      root.innerHTML = `
        <style>
          .card { border: 1px solid #999; padding: 8px; margin: 4px; }
        </style>
        <div class="card">
          <h2>${this.getAttribute('name')}</h2>
          <button class="follow">Follow</button>
          <span class="status" role="status"></span>
        </div>`;
      root.querySelector('.follow').addEventListener('click', () => {
        root.querySelector('.status').textContent = 'Following';
      });
    }
  }
  customElements.define('user-card', UserCard);
</script>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(HTML)

    # 1) Plain browser querySelector cannot see into the shadow tree:
    print(page.evaluate("document.querySelector('button.follow')"))   # None

    # 2) Playwright locators can:
    print(page.locator("button.follow").count())     # 2

    maria = page.locator("user-card").filter(has_text="Maria Lopez")
    maria.get_by_role("button", name="Follow").click()
    expect(maria.get_by_role("status")).to_have_text("Following")

    # The other card is unchanged
    john = page.locator("user-card").filter(has_text="John Smith")
    expect(john.get_by_role("status")).to_have_text("")

    browser.close()
```

**Line-by-line explanation**

- `class UserCard extends HTMLElement { ... }`: JavaScript that defines a new custom element class. Extending `HTMLElement` is how all custom elements start.
- `connectedCallback()`: a lifecycle method the browser calls when the element is inserted into the page. Here we set up the component.
- `this.attachShadow({ mode: 'open' })`: creates the open shadow root and returns it. If we used `'closed'`, Playwright (and any outside code) could not reach inside.
- `root.innerHTML = ...`: fills the shadow tree with a style, heading, button, and status area, using a JavaScript template literal (backticks) with `${...}` interpolation to insert the name attribute.
- The `<style>` inside the shadow root applies *only* inside it: this is the encapsulation that shadow DOM provides.
- `root.querySelector('.follow')`: note we use the **root's** `querySelector`, which is the only way for the component's own code to find elements inside its shadow tree.
- `customElements.define('user-card', UserCard)`: registers the tag name. Names must contain a hyphen.
- In Python: `page.evaluate("document.querySelector('button.follow')")` evaluates plain JavaScript in the page and returns the result to Python. It returns `None` because the browser's `querySelector` does not pierce shadow roots. This line exists purely to *demonstrate* the problem.
- `page.locator("button.follow").count()`: **2**, since Playwright's CSS engine pierces both cards' roots.
- `page.locator("user-card").filter(has_text="Maria Lopez")`: picks the host whose rendered text contains "Maria Lopez". `has_text` considers text inside shadow roots too, which is why the heading inside the shadow tree can be used as the filter.
- `maria.get_by_role("button", name="Follow").click()`: scoped to Maria's card; no strict mode violation, even though both cards have a Follow button.
- `maria.get_by_role("status")`: the `<span role="status">` is found by ARIA role. The assertion verifies the button's effect.
- `expect(john.get_by_role("status")).to_have_text("")`: confirms that John's card did not change; scoping prevented clicking the wrong button.

### Example 2: Two ways to locate (role-based vs CSS)

```python
# Role/text based: reads like a user's perspective
page.get_by_role("button", name="Follow").first.click()

# CSS based: reads like the DOM structure
page.locator("user-card:nth-of-type(2) .follow").click()

# Test id based (requires dev support):
# page.get_by_test_id("follow-john").click()
```

- `.first` picks the first match when multiple elements match; without it, the action would be a strict-mode violation.
- `user-card:nth-of-type(2)`: CSS positional pseudo-class; the second `user-card` among siblings of the same type. Positional selectors are fragile; use them only when nothing better exists.
- `get_by_test_id` uses the `data-testid` attribute by default (configurable). This is robust, but it needs support from developers: ask for test ids on the *interactive elements inside* the component, and make sure they are included in the shadow tree.

### Example 3: Nested components and slots

```python
HTML = """
<app-shell>
  <h1 slot="title">Dashboard</h1>
</app-shell>

<script>
  class FancyButton extends HTMLElement {
    constructor() {
      super();
      const r = this.attachShadow({ mode: 'open' });
      r.innerHTML = '<button class="btn"><slot></slot></button>';
      r.querySelector('button').addEventListener('click',
        () => this.dispatchEvent(new CustomEvent('pressed', { bubbles: true, composed: true })));
    }
  }
  customElements.define('fancy-button', FancyButton);

  class AppShell extends HTMLElement {
    constructor() {
      super();
      const r = this.attachShadow({ mode: 'open' });
      r.innerHTML = `
        <header><slot name="title"></slot></header>
        <fancy-button id="save">Save changes</fancy-button>
        <p id="msg"></p>`;
      r.getElementById('save').addEventListener('pressed',
        () => { r.getElementById('msg').textContent = 'Saved!'; });
    }
  }
  customElements.define('app-shell', AppShell);
</script>
"""
page.set_content(HTML)

# Nested open roots: <app-shell> root contains <fancy-button> whose root contains <button>
page.get_by_role("button", name="Save changes").click()
expect(page.locator("app-shell").locator("#msg")).to_have_text("Saved!")
expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()   # slotted light-DOM heading
```

**Explanation**

- `FancyButton` has a shadow root with `<button><slot></slot></button>`. The text "Save changes" is **slotted** content: it is a light DOM child of `<fancy-button>`, displayed inside the button.
- When clicked, the inner button dispatches a `CustomEvent` named `pressed` with `bubbles: true, composed: true`. `composed` lets the event cross the shadow boundary upward. This is how components talk to the world outside their shadow root.
- `AppShell` places a `<fancy-button>` inside its own shadow tree: **nested roots**. It also contains a named slot (`title`) that displays the `<h1 slot="title">` supplied by the page author.
- `get_by_role("button", name="Save changes")`: Playwright pierces two levels of shadow root and resolves the accessible name from the slotted text.
- `page.locator("app-shell").locator("#msg")`: chained locators; `#msg` lives in app-shell's shadow tree.
- `get_by_role("heading", name="Dashboard")`: the `<h1>` is in the *light DOM* but is displayed through the `title` slot. The role locator still finds it.

### Example 4: XPath does not pierce

```python
print(page.locator("xpath=//button").count())      # 0  (XPath cannot see inside shadow roots)
print(page.locator("css=button").count())          # 1  (CSS engine pierces)
print(page.locator("css:light=button").count())    # 0  (explicitly opts out of piercing)
```

- This is a quick experiment you can run to demonstrate the three behaviours, against Example 3's page.
- `xpath=` prefix selects the XPath engine, `css=` the CSS engine; `css:light=` is the non-piercing CSS variant. In day-to-day work you almost never need to type `css=`; Playwright detects CSS automatically, and XPath is detected when the selector starts with `//` or `..`.
- If you find yourself needing XPath on a modern component-based site, switch to role/text/CSS locators.

### Example 5: Assertions that work through the shadow boundary

```python
card = page.locator("user-card").first
expect(card).to_contain_text("Maria Lopez")
expect(card.get_by_role("button", name="Follow")).to_be_enabled()
expect(card.locator("h2")).to_have_text("Maria Lopez")
card.get_by_role("button", name="Follow").click()
expect(card.locator(".status")).to_have_text("Following")
expect(card.locator("button.follow")).to_have_count(1)
```

Every assertion you learned in earlier lessons behaves the same way; you do not use special API calls to assert on shadow content.

### Example 6: Inspecting a shadow root with `evaluate`

Sometimes you need to read something that locators cannot express. Use `evaluate` and walk the tree explicitly:

```python
host = page.locator("user-card").first

# Is the root open?
is_open = host.evaluate("el => el.shadowRoot !== null")
print("open root:", is_open)

# Read the heading text by explicitly using the shadowRoot
heading = host.evaluate("el => el.shadowRoot.querySelector('h2').textContent")
print(heading)

# Read computed style inside the shadow tree
color = host.evaluate("""el => {
    const btn = el.shadowRoot.querySelector('.follow');
    return getComputedStyle(btn).display;
}""")
print(color)
```

**Explanation**

- `locator.evaluate("el => ...")` runs the JavaScript function with the matched element as its argument and returns the (JSON-serialisable) result to Python.
- `el.shadowRoot` is `null` for closed roots, hence the first check.
- `el.shadowRoot.querySelector('h2')` is what the browser requires: *start from the root*. This is the hand-written equivalent of what Playwright's selector engine does for you.
- `getComputedStyle(...)` reads the final applied CSS, useful for checks that cannot be done through the accessibility tree.
- Use `evaluate` for diagnostics and unusual checks; for ordinary clicking and typing, locators are safer because they auto-wait and verify actionability, whereas `evaluate` runs immediately.

### Example 7: A closed shadow root, and a workaround

```python
HTML = """
<secret-box></secret-box>
<script>
  class SecretBox extends HTMLElement {
    connectedCallback() {
      const r = this.attachShadow({ mode: 'closed' });
      r.innerHTML = '<button>Reveal</button>';
    }
  }
  customElements.define('secret-box', SecretBox);
</script>
"""
page.set_content(HTML)
print(page.get_by_role("button", name="Reveal").count())   # 0 (hidden by closed root)
```

- Role/CSS locators find nothing, even though the user sees the button.
- Workaround for a **test-only** scenario: patch `attachShadow` *before* the page's scripts run:

```python
context = browser.new_context()
context.add_init_script("""
  const orig = Element.prototype.attachShadow;
  Element.prototype.attachShadow = function (init) {
    return orig.call(this, { ...init, mode: 'open' });
  };
""")
page = context.new_page()
page.set_content(HTML)
print(page.get_by_role("button", name="Reveal").count())   # 1
```

- `context.add_init_script(...)` registers a script that runs in every page of the context **before any page script**, on each navigation. The patched `attachShadow` always creates open roots.
- `{ ...init, mode: 'open' }` is JavaScript object-spread: copy all options from `init` and override `mode`.
- Consider this a diagnostic or last-resort tool; recommend to your team that components expose a testable surface instead.

### Example 8: Real-world pattern: a helper around a shadow-based component

```python
class UserCardComponent:
    """Small wrapper that hides locator details from tests."""
    def __init__(self, page, name: str):
        self.root = page.locator("user-card").filter(has_text=name)

    def follow(self):
        self.root.get_by_role("button", name="Follow").click()

    def status(self):
        return self.root.get_by_role("status")

# in a test:
card = UserCardComponent(page, "Maria Lopez")
card.follow()
expect(card.status()).to_have_text("Following")
```

- `class UserCardComponent:` is an ordinary Python class; `__init__` is the constructor that runs when you create an instance.
- `self.root` stores a *locator* (lazy), not an element, so it stays valid after re-renders.
- The test now reads like a business statement. If the component's markup changes, you update one class. This idea, the **Page Object Model**, is covered in depth on Wednesday.

---

## Real-World Scenarios

### Scenario 1: A design-system "date-picker" web component

The company's design system provides `<ds-date-picker>`. Its input and calendar are inside shadow roots. Because Playwright pierces, the helper from the *Date Pickers* lesson works almost unchanged: replace `page.get_by_label("Check-in")` with the equivalent locator against the web component. Role-based locators are best, as they continue to work whichever way the component is internally built.

### Scenario 2: Third-party cookie/consent banner

Consent management platforms often render the banner inside a shadow root. Test setups routinely need to dismiss it:

```python
page.get_by_role("button", name="Accept all").click()
```

If a naive CSS selector from a Selenium-era suite (`#accept-btn`) stops working after the vendor switched to web components, the fix is usually to use the role/text locator.

### Scenario 3: Component library regression testing

When a component library upgrades, QA wants to verify nothing broke. Tests locate each component by role and verify behaviour (open, close, keyboard navigation, disabled state), independent of internal structure. If tests were coupled to specific shadow-tree paths (`my-select >> .internal-wrapper > li:nth-child(3)`), every internal refactor would break them. Role-based locators survive.

### Scenario 4: Mixed iframe and shadow DOM

An embedded widget loads in an iframe and itself uses web components:

```python
widget = page.frame_locator("iframe[title='Support chat']")
widget.locator("chat-launcher").get_by_role("button", name="Open").click()
```

Frame handling (from earlier today) plus piercing (from this lesson) compose naturally.

---

## Common Pitfalls and Best Practices

1. **Reaching for XPath.** XPath will not pierce. Use CSS, role, text, label, or test-id locators.
2. **Using `document.querySelector` in `evaluate` to find shadow content.** It cannot cross the boundary. Walk `shadowRoot` explicitly, or better, use locators.
3. **Confusing shadow DOM with iframes.** Symptoms differ: shadow DOM works with ordinary locators; iframes require `frame_locator`. If locators fail, check DevTools to see which boundary you are facing.
4. **Overly deep CSS paths.** `user-card >> div > div > button:nth-child(2)` is brittle. Prefer `get_by_role`.
5. **Duplicate matches across components.** Repeated components lead to strict-mode violations. Scope with `filter(has_text=...)` on the host, as in Example 1.
6. **Assuming closed roots can be tested like open ones.** If an element is truly unreachable, escalate to developers (stable test interface) rather than layering hacks.
7. **Forgetting the accessibility angle.** A control without an accessible name is both an a11y defect and a locator problem. Raise it.
8. **Using `evaluate` for actions.** `el.click()` inside `evaluate` skips Playwright's actionability checks and auto-waiting. Use `locator.click()`.
9. **Timing.** Custom elements may upgrade a moment after page load (the element exists but its shadow tree is not rendered yet). Locators auto-wait for the inner element, but `count()` and `evaluate` do not.
10. **Assuming `css:light` is needed.** It almost never is; piercing is the right default.

**Best practices:** prefer role/label/text locators; scope by host element; use `data-testid` on interactive parts when roles are ambiguous; keep component wrappers in one place; ask developers to prefer open shadow roots and meaningful accessible names; avoid XPath in component-based apps.

---

## Mini Practice Exercises

### Exercise 1: Observe the boundary

Using Example 1, print `page.evaluate("document.querySelectorAll('h2').length")` and `page.locator("h2").count()`. Explain the difference.

<details>
<summary>Solution</summary>

The first prints `0` because the browser's `querySelectorAll` does not look inside shadow roots; the second prints `2` because Playwright's CSS engine pierces open roots. Both headings exist, which proves the boundary is a *query* boundary, not a "not rendered" situation.
</details>

### Exercise 2: Scoped interaction

Add a third `user-card` (Priya Nair). Follow Priya only and assert that Maria and John statuses are still empty.

*Hint:* `filter(has_text="Priya Nair")`.

### Exercise 3: Build your own component

Write a `toggle-switch` custom element with an open shadow root containing a `<button role="switch" aria-checked="false">`. Clicking it flips `aria-checked` between `true` and `false`. Write tests using `get_by_role("switch")` and `to_have_attribute("aria-checked", "true")`. (`to_be_checked()` also understands `aria-checked` on checkbox-like roles; check the assertions documentation to see which roles your Playwright version supports.)

<details>
<summary>Hint</summary>

Use `root.innerHTML = '<button role="switch" aria-checked="false">Dark mode</button>'` and toggle in a click listener using `btn.setAttribute('aria-checked', String(btn.getAttribute('aria-checked') !== 'true'))`. In tests, `page.get_by_role("switch", name="Dark mode")` finds it through the shadow root. `to_have_attribute` is the safest assertion.
</details>

### Exercise 4: XPath versus CSS

Write one test that proves XPath cannot see a shadow button while CSS can. Then rewrite your XPath to a role-based locator.

### Exercise 5: Evaluate walk

Write a function `shadow_text(host_locator, css)` that returns `textContent` of the first element matching `css` inside the host's shadow root, using `evaluate`. Return `None` if the root is closed.

<details>
<summary>Solution</summary>

```python
def shadow_text(host, css):
    return host.evaluate(
        """(el, css) => {
            if (!el.shadowRoot) return null;
            const t = el.shadowRoot.querySelector(css);
            return t ? t.textContent : null;
        }""",
        css,
    )
```

The second argument to `evaluate` is passed as the JavaScript function's second parameter.
</details>

### Exercise 6: A public example (stretch)

Visit a component-library demo that uses web components, such as the Shoelace documentation (`https://shoelace.style/`), find a `sl-button` or `sl-input`, and write a locator-only script that clicks or types into it. Record which locator style (role, label, CSS) was the most stable. Check whether the demo is still available when you run it; public sites change.

---

## Summary / Key Takeaways

- Shadow DOM is a boundary inside one document that hides a component's internal tree and styles. It is **not** an iframe.
- Playwright's CSS, text, role, label, placeholder, and test-id locators **pierce open shadow roots automatically**. You write ordinary locators.
- XPath and `document.querySelector` inside `evaluate` do **not** pierce; `css:light` opts out of piercing deliberately.
- Slots project light DOM content into a shadow tree; role locators see the *flattened* tree like a user does.
- Nested roots work the same; scope by host element to avoid duplicates.
- Closed roots cannot be reached by locators; negotiate a test interface or use a test-only patch like an init script.
- Use `evaluate` for diagnostics, not for clicking.
- Wrapping components in helper classes keeps tests readable; page objects and fixtures are covered in depth on Wednesday.

---

## External Resources

- Playwright Python docs, Other locators (CSS selectors, shadow DOM piercing, `css:light`): https://playwright.dev/python/docs/other-locators
- Playwright Python docs, Locators: https://playwright.dev/python/docs/locators
- MDN Web Docs, Using shadow DOM: https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM
- MDN Web Docs, Using custom elements: https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements
