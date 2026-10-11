# Navigation Events

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a "navigation" is in a browser: full page loads, redirects, same-document changes (hash and History API), and reloads.
- Use `page.goto()` correctly, including the `wait_until` option, and read the returned `Response` (status, headers, `ok`).
- Describe the page lifecycle events (`domcontentloaded`, `load`, `networkidle`, `commit`) and explain which one to use and why `networkidle` is discouraged.
- Use `page.wait_for_url()` and `expect(page).to_have_url()` to wait for navigation to finish after a click, form submit, or redirect.
- Explain why `page.expect_navigation()` and `page.wait_for_navigation()` are discouraged (racy and legacy) and what to use instead; recognise the remaining valid uses.
- Navigate with `go_back()`, `go_forward()`, and `reload()`, and understand the browser history stack.
- Handle single-page applications (SPAs) where the URL changes without a page load.
- Listen to navigation-related events: `framenavigated`, `load`, `domcontentloaded`, `request`, `response`, `requestfinished`, `requestfailed`, `console`, and `pageerror`.
- Handle redirects, 4xx/5xx errors, failed navigations, and navigation timeouts.
- Assert URL and title with regular expressions and globs, and avoid common mistakes with query strings and trailing slashes.
- Wait for specific network requests and responses using `expect_request` and `expect_response`.

---

## Why This Matters

Every user journey is a sequence of navigations: open the home page, click Login, land on a dashboard, open an order, go back to the list. If your automation proceeds before the navigation completes, it will act on the *old* page (a click that does nothing), or on a half-loaded new page (a missing element), or it will assert on the wrong URL. These are the flakiest, hardest-to-diagnose failures in UI testing.

At the same time, modern applications blur the definition of "navigation". A single-page application (built with React, Angular, or Vue) changes the URL and the entire screen without ever reloading the browser page. A form submission may redirect three times before reaching its final address. A payment may bounce through an external provider and back. Today's earlier lessons (frames, tabs, dynamic elements) all touched on navigation indirectly; this lesson makes it explicit.

This is core to the Week 5 epic on *complex UI interactions* and to **Project 1 - QE Foundations**: the checks you write for your project flows (login redirect, "back button returns to the list", "unauthenticated users are redirected to sign-in") are navigation assertions. Understanding how Playwright thinks about navigation also means you will quickly recognise why the older "wait for navigation" idiom from other tools is not needed.

---

## The Concept

### 1. What counts as a navigation?

| Type | What happens | Example |
| --- | --- | --- |
| **Full page navigation** | Browser requests a new document; the old document is unloaded; a new one loads | Clicking a normal link, `page.goto()` |
| **Redirect** | Server responds with 301/302/303/307/308 and a `Location`; browser follows automatically | `/login` to `/login/` or to `/dashboard` |
| **Reload** | Same URL, new document | `page.reload()`, F5 |
| **History traversal** | Moves back/forward in the session history | `go_back()`, `go_forward()` |
| **Same-document navigation** | URL changes but the document stays: fragment (`#section`) or History API (`history.pushState`) | SPA route changes, anchors |
| **Client-side redirect** | JavaScript sets `location.href` or `location.replace()`, or `<meta http-equiv="refresh">` | "Redirecting you in 3 seconds..." |

A key distinction: **cross-document** navigations destroy the old page's JavaScript state and load a fresh one; **same-document** navigations keep the page alive. Playwright waits appropriately for both when you use its recommended tools.

### 2. `page.goto()`

```python
response = page.goto("https://example.com/products")
```

`goto` navigates, then waits until the navigation reaches a given **lifecycle stage** (by default, the `load` event). It returns a `Response` object for the main resource, or `None` for navigations that produce no network response (for example `about:blank` or same-document hash changes).

Parameters you should know:

| Parameter | Meaning |
| --- | --- |
| `url` | Absolute URL; or relative if the context has a `base_url` |
| `wait_until` | When to consider navigation finished: `"load"` (default), `"domcontentloaded"`, `"networkidle"`, or `"commit"` |
| `timeout` | Maximum time in ms (default 30,000; `0` disables) |
| `referer` | Sets the `Referer` header |

Reading the response:

```python
response = page.goto("https://example.com/products")
print(response.status)        # 200
print(response.ok)            # True for 200-299
print(response.url)           # final URL after redirects
print(response.headers)       # dict of response headers (lower-cased names)
```

Note `status`, `ok`, `url`, and `headers` are **properties** in the Python API, while `body()`, `text()`, and `json()` are methods.

**Important:** `goto` does *not* raise an exception for HTTP error statuses like 404 or 500. The navigation technically succeeded in loading *a* page. If you care, check `response.status` or `response.ok`. `goto` raises an error only for problems like DNS failure, connection refused, certificate errors, or timeouts (a `playwright.sync_api.Error` or `TimeoutError`).

With a `base_url` on the context, you can write relative URLs:

```python
context = browser.new_context(base_url="https://example.com")
page = context.new_page()
page.goto("/products")           # https://example.com/products
```

Using a base URL means switching environments (dev, staging, production) takes one configuration change instead of editing every test.

### 3. Lifecycle events and `wait_until`

A page load progresses through stages:

1. **commit**: the server has responded and the browser has started to receive the new document (the navigation is "committed"). The earliest point.
2. **domcontentloaded**: the HTML has been fully parsed and the DOM is built (but stylesheets, images, and some scripts may still be loading). Equivalent to the browser `DOMContentLoaded` event.
3. **load**: the page and all its dependent resources (images, stylesheets, scripts) have finished loading. Equivalent to the `load` event.
4. **networkidle**: no network connections for at least 500 ms. **Discouraged.**

What to use:

- **`"load"` (default)**: appropriate for most tests.
- **`"domcontentloaded"`**: good when you want to move quickly and rely on auto-waiting for specific elements.
- **`"commit"`**: when you only need the navigation to start (e.g. testing a redirect chain or slow pages) and will wait on something specific yourself.
- **`"networkidle"`**: avoid. Many modern sites never become network-idle (analytics beacons, polling, websockets, chat widgets). The Playwright docs explicitly recommend not relying on it for testing. Instead, assert on the content you need: the UI is ready when the *element you will use next* is ready, and Playwright's auto-waiting handles that.

You can also wait for a lifecycle state at any time:

```python
page.wait_for_load_state()                      # "load" by default
page.wait_for_load_state("domcontentloaded")
```

If the state has already been reached, it returns immediately.

### 4. Waiting for navigation after an action

After an action that triggers navigation (click a link, submit a form), you need to know when the new page has arrived. The modern, recommended approaches, in order:

**Approach A: Do nothing special; use auto-waiting and assertions.**

```python
page.get_by_role("link", name="Dashboard").click()
expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()
```

Playwright's click waits for any navigation *initiated by the click* to start before returning ("scheduled navigations" are tracked), and the following assertion retries until the new page shows the heading. This is usually the best and cleanest style: you wait for what you need, not for an abstract event.

**Approach B: Assert the URL.**

```python
page.get_by_role("link", name="Dashboard").click()
expect(page).to_have_url(re.compile(r".*/dashboard"))
```

`expect(page).to_have_url(...)` retries until the URL matches. In the Python API it accepts a string (an exact match against the full URL; if the context has a `base_url`, a relative path is resolved against it) or a compiled regular expression. Glob patterns are supported by `wait_for_url` and by route and response matchers, not by `to_have_url`. For anything partial, use a regular expression.

**Approach C: `page.wait_for_url()`.**

```python
page.get_by_role("button", name="Log in").click()
page.wait_for_url("**/dashboard")
```

`wait_for_url(url, wait_until="load", timeout=...)` waits for the page URL to match (glob, regular expression, or a predicate function), *and* for the page to reach the `wait_until` state. It is ideal for multi-step redirects: it simply waits until the *final* URL you expect is reached, whatever happens in between. Glob patterns: `*` matches anything except `/`, `**` matches anything including `/`, `?` matches one char, `{a,b}` alternatives.

```python
page.wait_for_url(re.compile(r"/orders/\d+$"))
page.wait_for_url(lambda url: "/orders/" in url and url.endswith("/confirmation"))
```

(The predicate form receives the URL string.)

**Approach D: `expect_navigation` (legacy; caveats).**

```python
with page.expect_navigation():
    page.get_by_role("link", name="Dashboard").click()
```

Playwright's docs mark `page.expect_navigation()` (and `wait_for_navigation`) as **deprecated/inherently racy** and recommend `page.wait_for_url()` instead. Why racy?

- **It can hang when no navigation happens.** If the click does not trigger a navigation (e.g. it becomes a same-document change, or the app uses a client-side route), the `with` block waits until timeout.
- **It can mis-fire.** If multiple navigations occur (a redirect chain, or a navigation plus an iframe navigation), it resolves on the *first* matching one, which may not be the final page.
- **It couples the test to *how* the page navigates** (full load vs. SPA), while you really care *where* the user ends up.

You will still see `expect_navigation` in tutorials and legacy code, so you must be able to read it. The pattern is the same "register first, then act" idea you used for popups: the `with` block listens before the click. It supports `url=` (glob/regex/predicate) and `wait_until=`. In new code, prefer `click()` followed by `wait_for_url()` or an assertion.

> **Historical note.** In older Playwright versions and in tools like Selenium or Puppeteer, you often had to wait explicitly after a click. Since Playwright's actions already wait for initiated navigations to commit, and web-first assertions retry, explicit navigation waits are now rarely needed.

### 5. Same-document navigation and SPAs

In a single-page application, clicking "Orders" changes the address bar to `/orders` using `history.pushState`, and JavaScript swaps the visible content. No new document loads, so the browser `load` event does **not** fire again. This breaks any approach that waits for a "page load":

- `page.wait_for_load_state()` returns immediately (the page *is* already loaded).
- `expect_navigation` may time out, or may resolve on the History API change depending on version; do not depend on it.

What *does* work:

```python
page.get_by_role("link", name="Orders").click()
page.wait_for_url("**/orders")                       # URL changed via pushState: supported
expect(page.get_by_role("heading", name="Orders")).to_be_visible()   # content rendered
```

`wait_for_url` recognises History API and hash navigations. The heading assertion confirms the *content* has rendered, which is what matters to a user. Always check for content in SPAs; the URL changes first and the data may arrive later.

### 6. History: back, forward, reload

```python
page.go_back()        # like the Back button; returns Response or None
page.go_forward()
page.reload()         # returns Response
```

Each returns a `Response` when the navigation involves a network response, or `None` otherwise (e.g. going back within SPA history). They wait for the `load` state by default (parameter `wait_until`).

Testing back-button behaviour is valuable: after a successful form submission and redirect, going back should not resubmit or show stale pages; after login, going back should not return to the login form (or if it does, it should be handled gracefully). Browsers may serve pages from the **back/forward cache (bfcache)**, in which case the page is restored with its state rather than reloaded; scripts that expect to run on load may not run again. The `pageshow` event with `persisted=True` indicates bfcache restoration. Testers sometimes meet this as "the page shows old data after Back".

### 7. Redirects

A server redirect is followed automatically by the browser. `goto` returns the response for the **final** document, and `page.url` is the final URL. To inspect the chain:

```python
response = page.goto("/old")
print(response.url)                       # /new (after redirect)
print(response.request.redirected_from)    # Request for /old, or None
```

`Request.redirected_from` links back through the chain. To see each hop, listen to `page.on("response", ...)` and print `r.status` and `r.url`; hops show 301/302 statuses, then a 200.

To test that a protected page redirects unauthenticated users:

```python
page.goto("/account")
expect(page).to_have_url(re.compile(r"/login\?next=%2Faccount"))
```

Mind query strings: `to_have_url("https://x.com/login")` does **not** match `https://x.com/login?next=...`. Use a regular expression, or check parts with `urllib.parse`:

```python
from urllib.parse import urlparse, parse_qs
u = urlparse(page.url)
assert u.path == "/login"
assert parse_qs(u.query)["next"] == ["/account"]
```

Python's `urlparse` splits scheme, host, path, query, and fragment; `parse_qs` turns the query string into a dictionary of lists. This is more robust than string matching when parameter order may vary.

### 8. Navigation events

You can observe events that occur during navigation:

| Event | Fires when | Argument |
| --- | --- | --- |
| `page.on("domcontentloaded")` | DOM ready | Page |
| `page.on("load")` | Load event | Page |
| `page.on("framenavigated")` | A frame (including main frame) committed a navigation | Frame |
| `page.on("request")` | A request is issued | Request |
| `page.on("response")` | A response is received | Response |
| `page.on("requestfinished")` | A request finished successfully | Request |
| `page.on("requestfailed")` | A request failed (DNS, connection, aborted) | Request |
| `page.on("console")` | `console.log` etc. | ConsoleMessage |
| `page.on("pageerror")` | Uncaught exception in page JS | Error |
| `page.on("close")` | Page closed | Page |
| `page.on("crash")` | Page crashed | Page |

```python
page.on("framenavigated", lambda frame: print("navigated:", frame.url))
page.on("response", lambda r: print(r.status, r.url))
page.on("requestfailed", lambda r: print("FAILED:", r.url, r.failure))
page.on("pageerror", lambda e: print("JS error:", e))
```

These are excellent **diagnostic** tools: when a test fails, the log of navigations and failed requests often explains why. They can also be used in assertions, for example failing a test if the page logs an uncaught JavaScript error:

```python
errors = []
page.on("pageerror", lambda e: errors.append(str(e)))
# ... run the test ...
assert not errors, f"JavaScript errors: {errors}"
```

`framenavigated` fires for *every* frame, including iframes (recall the Frames lesson); filter with `frame == page.main_frame` if you only want top-level navigations.

Use `page.remove_listener("event", handler)` or `page.once("event", handler)` to unregister or run once.

### 9. Waiting for specific requests and responses

When a navigation or action triggers an API call you must wait for, register first, then act:

```python
with page.expect_response("**/api/orders*") as response_info:
    page.get_by_role("link", name="Orders").click()
response = response_info.value
assert response.status == 200
orders = response.json()
```

`expect_request` is the same for requests. The matcher can be a glob, a regular expression, or a predicate: `lambda r: r.url.endswith("/orders") and r.request.method == "GET"`. This ties your test to the real network behaviour and also lets you inspect the payload. But: assert on the **UI** as well (the user sees the DOM, not the JSON).

### 10. Errors and timeouts

| Situation | What Playwright does |
| --- | --- |
| HTTP 404/500 | `goto` succeeds; `response.status` tells you. |
| DNS failure / refused connection | Raises `playwright.sync_api.Error`, e.g. `net::ERR_NAME_NOT_RESOLVED`. |
| Certificate problem | Raises `net::ERR_CERT_*` unless `ignore_https_errors=True` on the context. |
| Page never reaches `load` | Raises `TimeoutError` (default 30 s). |
| Aborted navigation (another navigation started) | Raises an error such as `net::ERR_ABORTED` or "Navigation interrupted". |

A classic gotcha: `goto` followed immediately by another `goto` before the first has finished produces "navigation interrupted by another navigation". Allow each navigation to complete or accept it deliberately.

Example of a robust check:

```python
response = page.goto("/does-not-exist")
assert response is not None and response.status == 404
expect(page.get_by_role("heading", name="Page not found")).to_be_visible()
```

To test a failing server, you can *mock* the response using routing (later topic), or point at a test endpoint that returns 500.

### 11. Navigation and authentication state

After login, the session cookie lives in the browser context, so every following `goto` is authenticated. Between tests, new contexts start empty. Re-using logged-in state across tests (saving `storage_state`) saves time; fixtures to share it are covered in depth on Wednesday.

### 12. Navigating inside frames and popups

Frames navigate independently of the main page. To wait for a frame's navigation, use the `Frame` object (`frame.wait_for_url()`, `frame.wait_for_load_state()`), or assert on the content inside it with `frame_locator`. New tabs (see Multiple Tabs and Windows) have their own navigation lifecycle: after capturing a popup, call `popup.wait_for_load_state()` or assert on its URL.

---

## Code Examples

Redirects are produced by a real server, and Playwright's `route.fulfill()` does not re-route a redirect it fulfills itself, so for this lesson we start a tiny local web server using only Python's standard library. It runs in a background thread for the duration of the script, needs no installation, and gives us redirects, a 404 page, a form POST, and an SPA page.

### The local test server

```python
import re
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright, expect

PAGES = {
    "/": """<title>Home</title><h1>Home</h1>
        <a href="/products">Products</a>
        <a href="/old">Old link (redirects)</a>
        <a href="/missing">Missing page</a>
        <a href="/spa">SPA</a>
        <form action="/submit" method="post">
          <input name="who" value="student"><button>Send</button>
        </form>""",
    "/products": "<title>Products</title><h1>Products</h1><a href='/'>Home</a>",
    "/thanks": "<title>Thanks</title><h1>Thank you</h1>",
    "/spa": """<title>SPA</title><h1 id="view">Home view</h1>
        <button id="go-orders">Orders</button>
        <script>
          document.getElementById('go-orders').onclick = () => {
            history.pushState({}, '', '/spa/orders');
            setTimeout(() => { document.getElementById('view').textContent = 'Orders view'; }, 400);
          };
        </script>""",
    "/spa/orders": "<title>Orders</title><h1>Orders (direct load)</h1>",
}

# path -> (status code, Location header)
REDIRECTS = {
    "/old": (301, "/products"),
    "/submit": (303, "/thanks"),                                   # Post/Redirect/Get
    "/protected": (302, "/login?next=%2Fprotected&ref=email"),
}


class Handler(BaseHTTPRequestHandler):
    def handle_any(self):
        length = int(self.headers.get("Content-Length", 0))
        if length:
            self.rfile.read(length)                  # read and ignore a POST body
        path = self.path.split("?")[0]

        if path in REDIRECTS:
            status, location = REDIRECTS[path]
            self.send_response(status)
            self.send_header("Location", location)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        body = PAGES.get(path)
        status = 200 if body is not None else 404
        if body is None:
            body = "<title>404</title><h1>Page not found</h1>"
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    do_GET = handle_any
    do_POST = handle_any

    def log_message(self, *args):                    # keep the console quiet
        pass


server = HTTPServer(("127.0.0.1", 0), Handler)        # port 0 = let the OS choose a free port
BASE = f"http://127.0.0.1:{server.server_address[1]}"
threading.Thread(target=server.serve_forever, daemon=True).start()
```

**Explanation**

- `PAGES` holds the HTML for each path: a home page with several links and a form, a products page, a thank-you page, an SPA page that uses `history.pushState`, and a direct-load orders page.
- `REDIRECTS` maps paths to a status code and a `Location` header: a permanent redirect (301), a *Post/Redirect/Get* redirect (303), and a temporary redirect (302) that carries a query string.
- `class Handler(BaseHTTPRequestHandler)`: Python's standard-library request handler. `handle_any` runs for both GET and POST (`do_GET = handle_any` and `do_POST = handle_any` assign the same method to both names). It reads and discards any POST body, sends a redirect if the path is in `REDIRECTS`, otherwise sends the page or a 404.
- `send_response(status)`, `send_header(...)`, `end_headers()`, and `wfile.write(...)` are the standard-library calls to build an HTTP response by hand. Redirect `Location` values are relative; the browser resolves them against the current origin.
- `HTTPServer(("127.0.0.1", 0), Handler)`: binds to the local machine on any free port. `server.server_address[1]` is the chosen port, which we place into `BASE`.
- `threading.Thread(target=server.serve_forever, daemon=True).start()` serves requests in the background; `daemon=True` means the thread will not keep the script alive when it finishes.
- The SPA button changes the URL immediately but updates the content 400 ms later, which is exactly the situation that tricks beginners: the URL is "ready" before the UI.
- All following examples assume this setup code has run and are written inside `with sync_playwright() as p:` with `browser = p.chromium.launch()`.

### Example 1: `goto`, `wait_until`, and the Response

```python
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(base_url=BASE)
    page = context.new_page()

    response = page.goto("/products", wait_until="domcontentloaded")
    print(response.status, response.ok, response.url)   # 200 True http://127.0.0.1:<port>/products
    print(response.headers.get("content-type"))         # text/html; charset=utf-8

    missing = page.goto("/missing")
    print(missing.status, missing.ok)                    # 404 False
    expect(page.get_by_role("heading", name="Page not found")).to_be_visible()
    browser.close()
```

**Line-by-line**

- `browser.new_context(base_url=BASE)`: lets us write `page.goto("/products")`; `BASE` is the address of our local server.
- `page.goto("/products", wait_until="domcontentloaded")`: navigates and waits only until the HTML is parsed.
- `response.status` (200), `response.ok` (True), `response.url` (absolute final URL).
- `response.headers.get("content-type")`: dictionary lookup; header names are lower-case.
- `page.goto("/missing")` does **not** raise even though it is a 404; we inspect `status`. We also assert on the visible "Page not found" heading, which is what a user would see.

### Example 2: Click then assert (the recommended style)

```python
    page.goto("/")
    page.get_by_role("link", name="Products").click()
    expect(page).to_have_url(f"{BASE}/products")
    expect(page).to_have_title("Products")
    expect(page.get_by_role("heading", name="Products")).to_be_visible()
```

- No explicit navigation wait: `click()` handles the start of navigation; each `expect(...)` retries until satisfied.
- `to_have_url` with a string requires an exact match (including origin). With `base_url` set on the context, you can pass a relative-looking path in some versions; to be safe use the full URL, a regex, or `wait_for_url`.
- `to_have_title` checks the `<title>`.

### Example 3: `wait_for_url` with redirect

```python
    page.goto("/")
    page.get_by_role("link", name="Old link").click()
    page.wait_for_url("**/products")
    print(page.url)                       # http://127.0.0.1:<port>/products
    print(len(page.context.pages))        # 1  (same tab)
```

- The link points to `/old`, which answers 301 and sends the browser to `/products`. The final URL is `/products`.
- `wait_for_url("**/products")`: the glob means "any scheme/host/path prefix, ending with /products".
- You do not care how many hops happened; you wait for the destination.

### Example 4: Observing every hop

```python
    hops = []

    def log_response(r):
        if r.request.is_navigation_request():
            hops.append((r.status, r.url))

    page.on("response", log_response)
    page.goto("/old")
    page.remove_listener("response", log_response)    # stop listening
    print(hops)
    # [(301, '<BASE>/old'), (200, '<BASE>/products')]
```

- `r.request.is_navigation_request()` is True for document navigations (not images or scripts).
- Defining a *named* function lets us unregister it later with `remove_listener`. An anonymous `lambda` cannot be removed unless you keep a reference to it.
- `def log_response(r):` is a nested function; `hops` is captured from the enclosing scope, so appending to it works without any `global` statement.
- `hops` lists status and URL for each step of the chain. Observing hops is great for verifying that old URLs redirect permanently (301) rather than temporarily (302), an SEO-related requirement.
- `response.request.redirected_from` gives another way to walk the chain after the fact.

### Example 5: Form submit with Post/Redirect/Get

```python
    page.goto("/")
    page.get_by_role("button", name="Send").click()
    page.wait_for_url("**/thanks")
    expect(page.get_by_role("heading", name="Thank you")).to_be_visible()

    page.go_back()
    expect(page).to_have_url(f"{BASE}/")
```

- The form POSTs to `/submit`, which answers `303 See Other` with `Location: /thanks`; the browser then GETs `/thanks`. This pattern prevents duplicate form submission on refresh.
- `wait_for_url("**/thanks")` waits for the final page after the redirect.
- `page.go_back()` goes to `/` (the form), *skipping* the `/submit` step because redirects replace history entries. A well-built app behaves this way; verifying it is a good functional test.

### Example 6: SPA navigation

```python
    page.goto("/spa")
    page.get_by_role("button", name="Orders").click()

    page.wait_for_url("**/spa/orders")                     # URL changes at once (pushState)
    print(page.get_by_role("heading").inner_text())         # may still say 'Home view' !

    expect(page.get_by_role("heading", name="Orders view")).to_be_visible()   # wait for content
```

- This is the trap: the URL has already changed, but the content updates 400 ms later. Reading the heading right after `wait_for_url` shows the old content.
- The robust test always finishes by asserting on **content**, not only on the URL.
- Notice no `load` event: `page.wait_for_load_state()` would return instantly and prove nothing.

### Example 7: Legacy `expect_navigation` (read, but avoid writing)

```python
    page.goto("/")
    with page.expect_navigation(url="**/products"):
        page.get_by_role("link", name="Products").click()
    expect(page.get_by_role("heading", name="Products")).to_be_visible()
```

- `expect_navigation` starts listening, then the click triggers the navigation, and the `with` block waits until a navigation matching the URL pattern commits.
- It works here because the link triggers a real cross-document navigation. For the SPA button in Example 6 it would behave unpredictably.
- Equivalent modern code: click, then `page.wait_for_url("**/products")`.

### Example 8: Waiting for an API call triggered by navigation

```python
def api(route):
    route.fulfill(status=200, content_type="application/json", body='{"orders": [1, 2, 3]}')

context.route("**/api/orders", api)

page.goto("/")
with page.expect_response("**/api/orders") as r:
    page.evaluate("fetch('/api/orders')")       # stands in for what an SPA route does
print(r.value.status, r.value.json())            # 200 {'orders': [1, 2, 3]}
```

- `page.evaluate("fetch(...)")` simulates the application calling its API; in a real test the trigger would be a click.
- `r.value.json()` parses the body into a Python dict.

### Example 9: A failing navigation

```python
import playwright.sync_api as pw

try:
    page.goto("http://does-not-exist.invalid/", timeout=5000)
except pw.Error as e:
    print("Navigation failed:", str(e).splitlines()[0])
```

- The `.invalid` top-level domain is reserved and never resolves, so this produces a `net::ERR_NAME_NOT_RESOLVED` error.
- `pw.Error` is the base class for Playwright errors; `pw.TimeoutError` is a subclass for timeouts. Catching these lets you assert on failure modes, or print helpful diagnostics.
- `str(e).splitlines()[0]` shows just the first line of the long message.

### Example 10: Diagnostic logging helper

```python
def attach_diagnostics(page):
    page.on("framenavigated", lambda f: print("[nav]", f.url) if f == page.main_frame else None)
    page.on("requestfailed", lambda r: print("[failed]", r.method, r.url, r.failure))
    page.on("pageerror", lambda e: print("[js-error]", e))
    page.on("console", lambda m: print(f"[console.{m.type}]", m.text))
```

- Attach this once per page (a fixture will do it automatically on Wednesday), and your failing tests will show a timeline of navigations, failed requests, console output, and uncaught JavaScript errors.
- `f == page.main_frame` filters out iframe navigations.
- `m.type` is "log", "error", "warning", and so on.

---

## Real-World Scenarios

### Scenario 1: Login redirect and deep-link return

Unauthenticated user opens `/account/orders`; the app redirects to `/login?returnTo=/account/orders`; after login the user lands back on `/account/orders`.

```python
page.goto("/account/orders")
expect(page).to_have_url(re.compile(r"/login\?returnTo=%2Faccount%2Forders"))
page.get_by_label("Email").fill("student@example.com")
page.get_by_label("Password").fill("secret")
page.get_by_role("button", name="Sign in").click()
page.wait_for_url("**/account/orders")
expect(page.get_by_role("heading", name="Your orders")).to_be_visible()
```

Note the URL-encoded characters (`%2F` for `/`). Parse with `urlparse`/`parse_qs` for clarity if the encoding varies.

### Scenario 2: Checkout via an external payment provider

User clicks Pay; the browser goes to `https://pay.example.com/...`; after approval it returns to `/order/confirmation?id=...`.

```python
page.get_by_role("button", name="Pay").click()
page.wait_for_url(re.compile(r"pay\.example\.com"))
# test-mode provider page: approve
page.get_by_role("button", name="Approve test payment").click()
page.wait_for_url(re.compile(r"/order/confirmation\?id=\d+"), timeout=60_000)
```

A generous timeout is appropriate for a multi-hop journey including a third party. Use a test-mode provider or a stub; real providers block automation.

### Scenario 3: Broken links crawl

Quality teams often check that top-level navigation links return 200:

```python
links = page.locator("nav a").evaluate_all("els => els.map(e => e.href)")
for href in links:
    r = page.request.get(href)       # a lightweight API request, not a page load
    assert r.ok, f"{href} returned {r.status}"
```

`page.request` is Playwright's API-request client (sharing the page's cookies) and is faster than navigating to each link. Use real navigation when you also need to check rendered content.

### Scenario 4: Back-button and stale data

After editing a record and saving, pressing Back should not show an editable form with old values. Test: submit the form, `go_back()`, assert expected state (either the form is disabled, or a "this page has expired" message, or the edit page shows the new values).

### Scenario 5: Slow redirects and meta refresh

A maintenance page says "You will be redirected in 5 seconds" and then goes to `/status`. `page.wait_for_url("**/status", timeout=10_000)` is the right tool: explicit destination, explicit upper bound.

---

## Common Pitfalls and Best Practices

1. **Using `networkidle` as a readiness signal.** Slow and unreliable. Wait for the element or content you need.
2. **Thinking `goto` raises on 404/500.** It does not. Check `response.status` and the page content.
3. **Asserting on the URL only in SPAs.** The URL can change before content renders. Add a content assertion.
4. **Using `expect_navigation` when no navigation happens.** It hangs until timeout. Prefer `wait_for_url` / assertions.
5. **Exact URL comparisons with query strings, trailing slashes, or fragments.** Use regexes or `urlparse`.
6. **Hard-coding environment URLs.** Use `base_url` (and environment variables) so tests run anywhere.
7. **Starting a second navigation before the first finishes.** Leads to "navigation interrupted" errors. Wait between them.
8. **Reading `page.url` immediately after click.** It may still be the old URL. Use `wait_for_url` or `expect(page).to_have_url`.
9. **Ignoring console and page errors.** A JavaScript exception may be the true cause of "the page did not navigate". Log them.
10. **Not testing negative paths.** Add tests for 404 pages, unauthorized access redirects, and server errors.
11. **Anonymous listener lambdas you cannot remove.** Use named functions if you need `remove_listener`.
12. **Forgetting frames and popups navigate separately.** Wait on the right object (`frame`, `popup`).

**Best practices:** express waits as the *destination or outcome*, not the mechanism; keep one place for environment URLs; centralise diagnostics; check status codes explicitly when they matter; combine URL and content assertions; keep `wait_until` at default unless you have a reason.

---

## Mini Practice Exercises

### Exercise 1: Response details

Write a test that calls `page.goto("/products")` and asserts `status == 200`, `ok`, the title, and the content-type header contains `text/html`.

<details>
<summary>Solution</summary>

```python
r = page.goto("/products")
assert r.status == 200 and r.ok
assert "text/html" in r.headers["content-type"]
expect(page).to_have_title("Products")
```
</details>

### Exercise 2: Redirect hops

Record the navigation hops for `/old` and assert the first status is 301 and the final URL ends with `/products`. *Hint:* Example 4.

### Exercise 3: Back and forward

From `/`, click Products, then `go_back()`, then `go_forward()`. After each step assert URL and heading. What does `go_back()` return? *Answer:* a `Response` for a full-document navigation, or `None` if the target was restored without a network response.

### Exercise 4: SPA trap

Write one test that fails because it reads the heading right after `wait_for_url` in the SPA example (use `assert page.get_by_role("heading").inner_text() == "Orders view"`), then fix it with `expect`. Explain why the first version is flaky.

<details>
<summary>Solution</summary>

`inner_text()` is an immediate read; the content updates 400 ms after the URL. The fix is `expect(page.get_by_role("heading", name="Orders view")).to_be_visible()` (or `to_have_text`), which retries.
</details>

### Exercise 5: Query strings

Create a route that redirects `/protected` to `/login?next=%2Fprotected&ref=email`. Assert the path is `/login`, `next` is `/protected`, and `ref` is `email` using `urlparse`/`parse_qs`.

### Exercise 6: Console and errors

Create a page whose script throws an uncaught `Error("boom")` and logs `console.error("bad")`. Capture both with `page.on("pageerror")` and `page.on("console")` and assert the messages.

### Exercise 7: Practice site (stretch)

On `https://the-internet.herokuapp.com/redirector`, click the "here" link and wait for the status-codes page using `wait_for_url`. Then visit `https://the-internet.herokuapp.com/status_codes/404` and assert `response.status == 404` without an exception being raised.

<details>
<summary>Hint</summary>

`page.get_by_role("link", name="here").click()` then `page.wait_for_url("**/status_codes")`. For the 404, `r = page.goto(".../status_codes/404")` then `assert r.status == 404`.
</details>

---

## Summary / Key Takeaways

- A navigation can be a full load, a redirect chain, a reload, history traversal, or a same-document change (hash/History API). SPAs rarely fire `load` again.
- `page.goto()` returns a `Response`; it raises for network-level failures but **not** for 404/500. Check `status`/`ok`.
- Lifecycle stages: `commit`, `domcontentloaded`, `load`, `networkidle`. Default `load` is fine; avoid `networkidle`.
- After an action, rely on auto-waiting plus **content assertions**; use `page.wait_for_url()` (glob, regex, or predicate) for destinations and redirects; use `expect(page).to_have_url()` for retrying URL checks.
- `expect_navigation`/`wait_for_navigation` are legacy and racy; recognise them, prefer `wait_for_url`.
- `go_back`, `go_forward`, `reload` test history behaviour; bfcache can restore pages without reloading them.
- Navigation and network events (`framenavigated`, `response`, `requestfailed`, `pageerror`, `console`) are superb diagnostics.
- Use `base_url`, parse query strings with `urlparse`, and always assert on what the user sees.
- Shared fixtures for diagnostics, base URLs, and authenticated state are covered in depth on Wednesday.

---

## External Resources

- Playwright Python docs, Navigations: https://playwright.dev/python/docs/navigations
- Playwright Python docs, Events: https://playwright.dev/python/docs/events
- Playwright Python API reference, `page.wait_for_url`: https://playwright.dev/python/docs/api/class-page#page-wait-for-url
- Playwright Python API reference, `page.goto`: https://playwright.dev/python/docs/api/class-page#page-goto
- MDN Web Docs, History API: https://developer.mozilla.org/en-US/docs/Web/API/History_API
