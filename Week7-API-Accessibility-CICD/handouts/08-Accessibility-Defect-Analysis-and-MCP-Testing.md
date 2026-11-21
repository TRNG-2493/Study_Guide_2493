# Handout 08 – Accessibility Defect Analysis & MCP Testing


**Before class**

- Activate your `week7-demos` virtual environment and run: `pip install pytest pytest-playwright "mcp[cli]>=1.9,<2" pytest-asyncio`
- Node.js (only needed for the MCP Inspector, which runs with `npx`).

> The course notes use version 1 of the MCP Python SDK (`FastMCP`). Version 2 renames some classes, so pin `<2` for class.

> **How to use this handout:** each topic is a small, self-contained example in its own folder inside `week7-demos/`. Nothing carries over from one topic to the next. You will combine everything in **Handout 11 (Week 7 Mini-Project)**.

---

## Topic 4 – Accessibility Defect Analysis

### Definition

A raw scanner finding or a note from manual testing is **not yet a defect**. It first has to be confirmed, de-duplicated and classified. **Accessibility defect analysis** turns findings into actionable tickets by recording, for each one, the **WCAG success criterion** and level, the **POUR** principle, the **affected user group**, the **severity**, and the **root cause**. Severity measures the impact on users. Priority, which is decided separately with the product owner, measures when the defect will be fixed. A good bug report gives a developer everything needed to reproduce, fix and verify the problem.

### Key ideas

| Severity | Rule of thumb |
|----------|---------------|
| **Blocker** | A user group cannot complete a key task at all (for example, the Submit button can't be reached by keyboard) |
| **Critical** | A key task is very hard and has no reasonable workaround |
| **Major** | There is a workaround, but it is painful, or the problem affects many pages |
| **Minor** | An annoyance with little effect on completing the task |

- **Root-cause categories:** missing semantics · naming/labels · contrast/design · focus management · ARIA misuse · dynamic content · content authoring.
- **De-duplicate:** one root cause (for example, a shared button component) can produce 40 axe nodes, but it is **one** ticket.
- **Close the loop:** verify the fix both manually and with a scan, add a regression test, and track the violation count over time.

### Worked example – Triaging the findings for a broken sign-up page

📁 Folder: `08-4-defects/`

The findings below come from an axe scan and a keyboard pass of this small, broken sign-up page:

```html
<html>
  <div class="title">Sign up</div>
  <img src="logo.png">
  <input type="email" name="email">
  <div class="btn" onclick="alert('sent')">Submit</div>
  <p style="color:#aaaaaa">Terms apply</p>
</html>
```

**Step 1 – List the raw findings.**

| # | Source | Finding |
|---|--------|---------|
| F1 | axe | `html-has-lang` |
| F2 | axe | `image-alt` on `img` |
| F3 | axe | `label` on `input[type=email]` |
| F4 | axe | `color-contrast` on `p` (2.3:1) |
| F5 | keyboard | Submit cannot be reached or activated with the keyboard |

**Step 2 – Classify each one.** Add the columns.

| # | WCAG SC (level) | POUR | Users affected |
|---|-----------------|------|----------------|
| F1 | 3.1.1 Language of Page (A) | U | Screen-reader users (wrong pronunciation) |
| F2 | 1.1.1 Non-text Content (A) | P | Blind users |
| F3 | 4.1.2 Name, Role, Value / 3.3.2 Labels (A) | R / U | Screen-reader and voice-control users |
| F4 | 1.4.3 Contrast (Minimum) (AA) | P | Low-vision users |
| F5 | 2.1.1 Keyboard (A) · 4.1.2 (A) | O / R | Keyboard, switch and screen-reader users |

**Step 3 – Rate severity and assign a root cause.**

| # | Severity | Root cause |
|---|----------|------------|
| F5 | **Blocker** – no keyboard user can sign up | Missing semantics (`div` used as a button) |
| F3 | **Critical** – the field has no name | Naming/labels |
| F2 | Minor – the logo carries no essential content | Content authoring |
| F4 | Minor – legal text is hard to read | Contrast/design |
| F1 | Minor | Missing semantics |

**Step 4 – Write the bug report for the top finding.**

```markdown
**Title:** [A11y][Blocker] Sign-up "Submit" not operable by keyboard – WCAG 2.1.1
**Environment:** Chrome 131 / Windows 11 / NVDA 2024.4, page /bad.html
**Steps:** 1. Load /bad.html  2. Press Tab from the address bar  3. Try to reach Submit
**Expected:** Submit receives visible focus; Enter or Space submits; NVDA says "Submit, button"
**Actual:** Focus skips Submit and leaves the page; NVDA does not announce a button
**Users affected:** keyboard-only, switch, screen-reader users – cannot complete sign-up
**WCAG:** 2.1.1 Keyboard (A), 4.1.2 Name, Role, Value (A)
**Root cause:** <div class="btn" onclick> instead of a native button
**Suggested fix:** <button type="submit">Submit</button>
**Evidence:** keyboard-pass table, screen recording
```

**Step 5 – Add a regression test** (`test_regression.py`) so the defect stays fixed. It uses `page.set_content`, so no web server is needed.

```python
FIXED = """
<html lang="en"><body><main>
  <h1>Sign up</h1>
  <label for="email">Email</label><input id="email" type="email">
  <button type="submit">Submit</button>
</main></body></html>
"""


def test_submit_is_keyboard_operable(page):
    page.set_content(FIXED)
    page.keyboard.press("Tab")      # email
    page.keyboard.press("Tab")      # submit
    focused = page.evaluate("document.activeElement.tagName + ':' + document.activeElement.textContent")
    assert focused == "BUTTON:Submit"
```

### Final code

The only code in this topic is `test_regression.py` from Step 5, which is already complete. Your folder contains just that file.

### How to run

```bash
cd week7-demos/08-4-defects
playwright install chromium      # once, if you have not already
pytest -v test_regression.py
```

### Checkpoint

- You have a triage table with **5 findings**, each with a WCAG criterion, severity and root cause, sorted with the blocker first.
- The test run gives `1 passed`. Replace the `<button>` with `<div class="btn">Submit</div>` and it fails, which proves the test can catch the bug.

### Your turn

1. An axe report shows `color-contrast` on **37 nodes**, all `.btn-secondary` elements across 12 pages. How many tickets do you open, and what is the root cause?
2. Write the full bug report for **F3** (the unlabeled email field).
3. A minor-severity defect is on the checkout page, which every customer uses, the week before a legal audit. Explain how severity and priority can differ here.
4. Name two metrics you would track on a team dashboard to show accessibility improving over time.

### Common errors

- **One ticket per axe node.** That creates noise. Group the nodes by root cause.
- **"Fails accessibility" as a title.** Name the control, the criterion and the impact.
- **Closing the ticket after a green scan only.** Verify with the keyboard and a screen reader too.

---

## Topic 5 – Introduction to MCP (Model Context Protocol) Testing

### Definition

The **Model Context Protocol (MCP)** is an open standard that lets AI applications connect to external tools and data in a consistent way. A **host** (an AI app) runs a **client**, which connects to a **server** that exposes **tools** (functions the model can call), **resources** (readable data) and **prompts** (reusable templates). Messages are **JSON-RPC 2.0** and travel over **stdio** or **streamable HTTP**. Testing an MCP server is a form of API testing: you check the handshake, the tool list and schemas, the results, and the error behaviour.

### Key ideas

| JSON-RPC shape | Has `id`? | Example |
|----------------|-----------|---------|
| Request | Yes | `{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{...}}` |
| Response | Yes | `{"jsonrpc":"2.0","id":1,"result":{...}}` |
| Error | Yes | `{"jsonrpc":"2.0","id":1,"error":{"code":-32601,"message":"Method not found"}}` |
| Notification | **No** | `{"jsonrpc":"2.0","method":"notifications/initialized"}` |

- **Lifecycle:** `initialize` → capability negotiation → `notifications/initialized` → normal calls → shutdown.
- **Testing layers:** (1) tool logic unit tests → (2) contract/schema (`tools/list`) → (3) protocol and errors → (4) resources and prompts → (5) end-to-end over stdio or HTTP. Most tests should sit in layers 1–4.
- A tool that raises an exception returns `isError: true`. **The server must stay alive** afterwards.

### Worked example – Building and testing a calculator server

📁 Folder: `08-5-mcp/`, files `calc_server.py`, `test_mcp_logic.py` and `test_mcp_protocol.py`

**Step 1 – Build a minimal server** (`calc_server.py`).

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calc")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("b must not be zero")
    return a / b


if __name__ == "__main__":
    mcp.run()
```

**Step 2 – Explore it manually with the MCP Inspector.**

```bash
npx @modelcontextprotocol/inspector python calc_server.py
```

In the browser, click **Connect → Tools → List Tools**, run `add` with `a=2, b=3`, then run `divide` with `b=0`.

**Step 3 – Layer 1: unit-test the tool logic** (`test_mcp_logic.py`). No MCP is involved yet.

```python
import pytest
from calc_server import add, divide


def test_add():
    assert add(2, 3) == 5


def test_divide_by_zero():
    with pytest.raises(ValueError, match="zero"):
        divide(1, 0)
```

**Step 4 – Layer 2: test the contract with an in-memory client** (`test_mcp_protocol.py`).

```python
import pytest
from mcp.shared.memory import create_connected_server_and_client_session as connect
from calc_server import mcp


@pytest.fixture
def server():
    return mcp._mcp_server          # low-level server behind FastMCP


@pytest.mark.asyncio
async def test_tools_list_contract(server):
    async with connect(server) as session:
        result = await session.list_tools()
    tools = {t.name: t for t in result.tools}
    assert set(tools) == {"add", "divide"}
    assert tools["add"].description == "Add two integers."
    assert set(tools["add"].inputSchema["required"]) == {"a", "b"}
```

**Step 5 – Layer 3: test the calls and the error behaviour.**

```python
@pytest.mark.asyncio
async def test_call_add(server):
    async with connect(server) as session:
        result = await session.call_tool("add", {"a": 1, "b": 1})
    assert result.isError is False
    assert result.content[0].text == "2"


@pytest.mark.asyncio
async def test_divide_error_keeps_server_alive(server):
    async with connect(server) as session:
        bad = await session.call_tool("divide", {"a": 1, "b": 0})
        assert bad.isError is True
        good = await session.call_tool("add", {"a": 2, "b": 2})
        assert good.content[0].text == "4"
```

### Final code

`calc_server.py` (Step 1) and `test_mcp_logic.py` (Step 3) are already complete. This is the finished protocol test file, combining Steps 4 and 5:

**`test_mcp_protocol.py`**

```python
import pytest
from mcp.shared.memory import create_connected_server_and_client_session as connect
from calc_server import mcp


@pytest.fixture
def server():
    return mcp._mcp_server          # low-level server behind FastMCP


@pytest.mark.asyncio
async def test_tools_list_contract(server):
    async with connect(server) as session:
        result = await session.list_tools()
    tools = {t.name: t for t in result.tools}
    assert set(tools) == {"add", "divide"}
    assert tools["add"].description == "Add two integers."
    assert set(tools["add"].inputSchema["required"]) == {"a", "b"}


@pytest.mark.asyncio
async def test_call_add(server):
    async with connect(server) as session:
        result = await session.call_tool("add", {"a": 1, "b": 1})
    assert result.isError is False
    assert result.content[0].text == "2"


@pytest.mark.asyncio
async def test_divide_error_keeps_server_alive(server):
    async with connect(server) as session:
        bad = await session.call_tool("divide", {"a": 1, "b": 0})
        assert bad.isError is True
        good = await session.call_tool("add", {"a": 2, "b": 2})
        assert good.content[0].text == "4"
```

### How to run

```bash
cd week7-demos/08-5-mcp

# manual exploration (needs Node.js)
npx @modelcontextprotocol/inspector python calc_server.py

# automated tests
pytest -v test_mcp_logic.py test_mcp_protocol.py
```

### Checkpoint

- In the Inspector (Step 2), `add` returns **5**, and `divide` with `b=0` shows an error result containing *"b must not be zero"*.
- The test run shows:

```
test_add PASSED
test_divide_by_zero PASSED
test_tools_list_contract PASSED
test_call_add PASSED
test_divide_error_keeps_server_alive PASSED
============ 5 passed ============
```

### Your turn

1. Add a `multiply` tool. Which existing test fails first, and why is that a **good** thing?
2. Write a test that calls a tool that does not exist (`"subtract"`) and asserts the result is an error, not a crash.
3. Add a resource `@mcp.resource("greeting://{name}")` that returns `f"Hello, {name}!"` and test it with `session.read_resource("greeting://Ana")`.
4. Write a layer-5 test that starts the server as a real subprocess using `stdio_client` and `StdioServerParameters(command=sys.executable, args=["calc_server.py"])`.

### Common errors

- **Calling `mcp.run()` without the `if __name__ == "__main__"` guard.** Importing the file in a test then hangs.
- **Printing to stdout in a stdio server.** stdout carries the protocol messages, so stray prints corrupt the stream. Log to stderr instead.
- **Yielding an open session from a fixture.** This causes an *"exit cancel scope in a different task"* error, so open the session inside each test.
- **Missing `@pytest.mark.asyncio`.** The test is skipped or warns *"coroutine was never awaited"*.

---

## Answers

<details>
<summary><strong>Topic 4 – Accessibility Defect Analysis</strong></summary>

1. Open **one** ticket. The root cause is contrast/design in the shared `.btn-secondary` style. List the affected pages and node count as evidence.
2. ```markdown
   **Title:** [A11y][Critical] Sign-up email field has no accessible name – WCAG 4.1.2 / 3.3.2
   **Environment:** Chrome 131 / Windows 11 / NVDA 2024.4, /bad.html
   **Steps:** 1. Load /bad.html  2. Tab to the email field with NVDA on
   **Expected:** NVDA announces "Email, edit"; a visible label is present
   **Actual:** NVDA announces "edit text" with no name; there is no visible label
   **Users affected:** screen-reader and voice-control users cannot identify the field
   **WCAG:** 4.1.2 Name, Role, Value (A); 3.3.2 Labels or Instructions (A)
   **Root cause:** input has no <label> or aria-label
   **Suggested fix:** <label for="email">Email</label><input id="email" ...>
   **Evidence:** axe rule `label`, NVDA speech viewer screenshot
   ```
3. Severity stays **minor** because the impact on a user is small. Priority becomes **high** because of the page's traffic and the legal deadline. Severity describes the impact, and priority describes when it gets fixed.
4. Examples: open accessibility defects by severity, axe violations per page over time, issue density (violations per 1,000 nodes), and the percentage of key user journeys that pass the manual checklist.

</details>

<details>
<summary><strong>Topic 5 – MCP Testing</strong></summary>

1. `test_tools_list_contract` fails because the set of tool names changed. This is good, because a contract change should be deliberate and visible. Update the test when the change is intended.
2. ```python
   @pytest.mark.asyncio
   async def test_unknown_tool(server):
       async with connect(server) as session:
           result = await session.call_tool("subtract", {"a": 1, "b": 1})
       assert result.isError is True
   ```
   (Depending on the SDK version, an unknown tool may instead raise an `McpError`. In that case, wrap the call in `pytest.raises(Exception)`.)
3. ```python
   @mcp.resource("greeting://{name}")
   def greeting(name: str) -> str:
       """A personalised greeting."""
       return f"Hello, {name}!"

   @pytest.mark.asyncio
   async def test_greeting(server):
       async with connect(server) as session:
           res = await session.read_resource("greeting://Ana")
       assert res.contents[0].text == "Hello, Ana!"
   ```
4. ```python
   import sys
   from mcp import ClientSession, StdioServerParameters
   from mcp.client.stdio import stdio_client

   PARAMS = StdioServerParameters(command=sys.executable, args=["calc_server.py"])

   @pytest.mark.asyncio
   async def test_stdio_end_to_end():
       async with stdio_client(PARAMS) as (read, write):
           async with ClientSession(read, write) as session:
               init = await session.initialize()
               assert init.capabilities.tools is not None
               result = await session.call_tool("add", {"a": 1, "b": 1})
               assert result.content[0].text == "2"
   ```

</details>
