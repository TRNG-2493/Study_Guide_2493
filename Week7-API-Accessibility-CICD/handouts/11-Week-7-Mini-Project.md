# Handout 11 – Week 7 Mini-Project: Blog API Quality Check

In Handouts 01–10 you practised each concept on its own. In this mini-project you put them **together** in one small, complete project. You will build a test suite for a blog API: explore it by hand, automate it in Python, validate its contract, mock its failures, check its status page for accessibility, expose it through an MCP tool (optional), and run everything in a GitLab pipeline.

The API is `https://jsonplaceholder.typicode.com` (free, no login, **fakes** writes).

When you finish, the project looks like this:

```
week7-mini-project/
├── config.py
├── blog_client.py
├── mcp_server.py          (optional, Part 6)
├── schemas/post.json
├── data/new_posts.csv
├── site/index.html
├── tests/
│   ├── conftest.py
│   ├── test_posts.py
│   ├── test_contract.py
│   ├── test_mocked.py
│   ├── test_a11y.py
│   └── test_mcp.py        (optional, Part 6)
├── pytest.ini
├── requirements.txt
├── .gitignore
└── .gitlab-ci.yml
```

---

## Part 0 – Setup (5 min)

**Step 1 – Create the folder and a virtual environment.**

```bash
mkdir week7-mini-project && cd week7-mini-project
mkdir tests schemas data site
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
```

**Step 2 – Create `requirements.txt` and install.**

```
requests
pytest
pytest-html
jsonschema
responses
playwright==1.49.0
pytest-playwright
axe-playwright-python
mcp[cli]>=1.9,<2
pytest-asyncio
httpie
```

```bash
pip install -r requirements.txt
playwright install chromium
```

**Step 2b – Check the command-line tools.** curl is already installed on Windows 10/11 (`curl.exe`), macOS and most Linux systems. HTTPie is in `requirements.txt` (or install it with `brew install httpie` on macOS). Check both with:

```bash
curl --version
http --version
```

If Windows says `http` is not recognized, use `python -m httpie` instead of `http`.

**Step 3 – Create `pytest.ini`.**

```ini
[pytest]
pythonpath = .
testpaths = tests
markers =
    smoke: quick checks for every merge request
    a11y: accessibility checks (need a browser)
    mcp: MCP server tests
addopts = -ra --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html
```

**Step 4 – Create `.gitignore`.**

```
.venv/
.env
reports/
__pycache__/
```

✅ **Checkpoint:** `pytest` runs and reports `no tests ran`.

---

## Part 1 – Explore the API by hand (10 min)

**Goal:** before you automate anything, see the real requests and responses.

**Step 1 – Read one post and one missing post with curl, then with HTTPie.**

```bash
curl -i https://jsonplaceholder.typicode.com/posts/1
curl -i https://jsonplaceholder.typicode.com/posts/9999
```

*HTTPie version:*

```bash
http https://jsonplaceholder.typicode.com/posts/1
http https://jsonplaceholder.typicode.com/posts/9999
```

**Step 2 – Filter with a query parameter and create a post.**

```bash
curl -s "https://jsonplaceholder.typicode.com/posts?userId=1" | python -m json.tool | head -8
curl -i -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "hello", "body": "b", "userId": 1}'
```

*HTTPie version:*

```bash
http -b --pretty=format https://jsonplaceholder.typicode.com/posts userId==1 | head -8
http POST https://jsonplaceholder.typicode.com/posts title=hello body=b userId:=1
```

**Step 3 – Build a small Postman collection.** Create an environment `Blog` with `baseUrl` = `https://jsonplaceholder.typicode.com`. Create a collection `Blog API` with `GET {{baseUrl}}/posts/1` and this post-response script:

```javascript
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("Body has id 1", () => pm.expect(pm.response.json().id).to.eql(1));
```

✅ **Checkpoint:** curl and HTTPie both show `200` then `404 {}`, the POST returns `201` with `"id": 101`, and the Postman Runner shows **2 passed**.

📝 **Try it (A):** add `GET {{baseUrl}}/posts/9999` to the collection with a test that expects `404`.

---

## Part 2 – A client and the first tests (15 min)

**Goal:** wrap the API in a small client with configuration from the environment, then write status and JSON tests that use fixtures.

**Step 1 – Read configuration from the environment** (`config.py`).

```python
import os

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
TIMEOUT = float(os.getenv("API_TIMEOUT", "5"))
API_TOKEN = os.getenv("API_TOKEN", "")
```

**Step 2 – Write the client** (`blog_client.py`). It sets a timeout on every call, sends the token if there is one, and never asserts.

```python
import requests
import config


class BlogClient:
    def __init__(self, base_url=config.BASE_URL, token=config.API_TOKEN, timeout=config.TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers["Accept"] = "application/json"
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def _request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, f"{self.base_url}{path}", **kwargs)

    def get_post(self, post_id):
        return self._request("GET", f"/posts/{post_id}")

    def posts_by_user(self, user_id):
        return self._request("GET", "/posts", params={"userId": user_id})

    def create_post(self, **fields):
        return self._request("POST", "/posts", json=fields)

    def delete_post(self, post_id):
        return self._request("DELETE", f"/posts/{post_id}")
```

**Step 3 – Add fixtures** (`tests/conftest.py`): one shared client, plus a self-cleaning post with a unique title.

```python
import uuid

import pytest
from blog_client import BlogClient


@pytest.fixture(scope="session")
def client():
    c = BlogClient()
    yield c
    c.session.close()


@pytest.fixture
def new_post(client):
    title = f"mini-{uuid.uuid4().hex[:8]}"          # unique per test
    post = client.create_post(title=title, body="b", userId=1).json()
    yield post
    client.delete_post(post["id"])                   # cleanup runs even if the test fails
```

**Step 4 – Write status and JSON tests** (`tests/test_posts.py`).

```python
import pytest


@pytest.mark.smoke
def test_get_post_ok(client):
    r = client.get_post(1)
    assert r.status_code == 200
    assert r.headers["Content-Type"].startswith("application/json")
    assert r.json()["id"] == 1


def test_missing_post_returns_404(client):
    r = client.get_post(9999)
    assert r.status_code == 404, f"got {r.status_code}: {r.text[:200]}"


def test_posts_by_user(client):
    posts = client.posts_by_user(1).json()
    assert len(posts) == 10
    assert all(p["userId"] == 1 for p in posts)


def test_new_post_echoes_fields(new_post):
    assert new_post["id"] == 101
    assert new_post["title"].startswith("mini-")
```

✅ **Checkpoint:** `pytest -v tests/test_posts.py` shows **4 passed**, and `pytest -m smoke` runs only 1 of them.

📝 **Try it (B):** add a parametrized test that checks `/posts/1`, `/posts/50` and `/posts/100` all return `200`.

---

## Part 3 – Contract and data-driven tests (15 min)

**Goal:** describe what a post must look like once (a schema), and drive creation tests from a CSV file.

**Step 1 – Save the contract** (`schemas/post.json`).

```json
{
  "type": "object",
  "required": ["id", "userId", "title", "body"],
  "properties": {
    "id":     { "type": "integer", "minimum": 1 },
    "userId": { "type": "integer", "minimum": 1 },
    "title":  { "type": "string",  "minLength": 1 },
    "body":   { "type": "string" }
  }
}
```

**Step 2 – Add the test data** (`data/new_posts.csv`).

```
case,title,user_id
simple,Hello,1
unicode,Café ✓,2
long,xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx,3
```

**Step 3 – Load both files and write the tests** (`tests/test_contract.py`).

```python
import csv
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schemas" / "post.json").read_text(encoding="utf-8"))
with (ROOT / "data" / "new_posts.csv").open(newline="", encoding="utf-8-sig") as f:
    ROWS = list(csv.DictReader(f))


def assert_matches_post_schema(body):
    errors = list(Draft202012Validator(SCHEMA).iter_errors(body))
    assert not errors, "; ".join(f"{list(e.path)}: {e.message}" for e in errors)


@pytest.mark.smoke
def test_get_post_matches_schema(client):
    assert_matches_post_schema(client.get_post(1).json())


@pytest.mark.parametrize("row", ROWS, ids=[r["case"] for r in ROWS])
def test_create_post_from_csv(client, row):
    r = client.create_post(title=row["title"], body="b", userId=int(row["user_id"]))
    assert r.status_code == 201
    assert_matches_post_schema(r.json())
    assert r.json()["title"] == row["title"]
```

✅ **Checkpoint:** `pytest -v tests/test_contract.py` shows **4 passed**, including `test_create_post_from_csv[unicode]`.

📝 **Try it (C):** change `"title"` in the schema to `{"type": "integer"}` and run again. What does the failure message say? (Change it back afterwards.)

---

## Part 4 – Mocked failure tests (10 min)

**Goal:** prove the client behaves well when the server breaks, without touching the network.

**Step 1 – Write the tests** (`tests/test_mocked.py`).

```python
import pytest
import requests
import responses
from blog_client import BlogClient

FAKE = "https://api.example.test"


@responses.activate
def test_server_error_is_reported():
    responses.add(responses.GET, f"{FAKE}/posts/1", status=500)
    r = BlogClient(base_url=FAKE).get_post(1)
    assert r.status_code == 500


@responses.activate
def test_network_failure_raises():
    responses.add(responses.GET, f"{FAKE}/posts/1", body=requests.ConnectionError("down"))
    with pytest.raises(requests.ConnectionError):
        BlogClient(base_url=FAKE).get_post(1)


@responses.activate
def test_token_is_sent():
    responses.add(responses.GET, f"{FAKE}/posts/1", json={"id": 1})
    BlogClient(base_url=FAKE, token="abc12345").get_post(1)
    assert responses.calls[0].request.headers["Authorization"] == "Bearer abc12345"
```

✅ **Checkpoint:** `pytest -v tests/test_mocked.py` shows **3 passed**, even with Wi-Fi turned off.

📝 **Try it (D):** add a test where the fake server returns `429` with a `Retry-After: 2` header, and assert that the client passes both the code and the header through unchanged.

---

## Part 5 – Accessibility checks (10 min)

**Goal:** the blog team has a small status page. Scan it with axe and check that it works with the keyboard.

**Step 1 – Create the page** (`site/index.html`).

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Blog API status</title></head>
<body>
  <main>
    <h1>Blog API status</h1>
    <p>All systems operational.</p>
    <label for="post-id">Post id</label>
    <input id="post-id" type="number" min="1">
    <button type="button">Check post</button>
  </main>
</body>
</html>
```

**Step 2 – Write the checks** (`tests/test_a11y.py`). The page is opened straight from disk, so no web server is needed.

```python
from pathlib import Path

import pytest
from axe_playwright_python.sync_playwright import Axe

PAGE = (Path(__file__).resolve().parent.parent / "site" / "index.html").as_uri()
OPTIONS = {"runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa"]}}


@pytest.mark.a11y
def test_status_page_has_no_violations(page):
    page.goto(PAGE)
    results = Axe().run(page, options=OPTIONS)
    assert results.violations_count == 0, results.generate_report()


@pytest.mark.a11y
def test_button_reachable_by_keyboard(page):
    page.goto(PAGE)
    page.keyboard.press("Tab")          # input
    page.keyboard.press("Tab")          # button
    assert page.evaluate("document.activeElement.textContent") == "Check post"
```

✅ **Checkpoint:** `pytest -v -m a11y` shows **2 passed**.

> ⚠️ Always run the `a11y` tests **on their own** (`-m a11y`). Playwright's sync API and the async MCP tests in Part 6 cannot share one PyTest run. If they do, you get `RuntimeError: Runner.run() cannot be called from a running event loop`.

📝 **Try it (E):** delete the `<label>` line, run the scan, and write a one-line bug report: title, WCAG criterion and severity. Then put the label back.

---

## Part 6 – *(Optional)* An MCP tool (10 min)

**Goal:** let an AI assistant use the blog API through an MCP tool, and test that tool without the network.

**Step 1 – Write the server** (`mcp_server.py`). The tool reuses `BlogClient`.

```python
from mcp.server.fastmcp import FastMCP
from blog_client import BlogClient

mcp = FastMCP("blog")


@mcp.tool()
def get_post_title(post_id: int) -> str:
    """Return the title of a blog post."""
    r = BlogClient().get_post(post_id)
    if r.status_code == 404:
        raise ValueError(f"post {post_id} not found")
    r.raise_for_status()
    return r.json()["title"]


if __name__ == "__main__":
    mcp.run()
```

**Step 2 – Test the contract and the behaviour, with the HTTP calls mocked** (`tests/test_mcp.py`).

```python
import pytest
import responses
from mcp.shared.memory import create_connected_server_and_client_session as connect

import config
from mcp_server import mcp


@pytest.mark.mcp
@pytest.mark.asyncio
async def test_tool_is_listed():
    async with connect(mcp._mcp_server) as session:
        tools = (await session.list_tools()).tools
    assert [t.name for t in tools] == ["get_post_title"]


@pytest.mark.mcp
@pytest.mark.asyncio
async def test_tool_returns_title_and_handles_404():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, f"{config.BASE_URL}/posts/1", json={"id": 1, "title": "hello"})
        rsps.add(responses.GET, f"{config.BASE_URL}/posts/999", status=404, json={})
        async with connect(mcp._mcp_server) as session:
            ok = await session.call_tool("get_post_title", {"post_id": 1})
            missing = await session.call_tool("get_post_title", {"post_id": 999})
    assert ok.content[0].text == "hello"
    assert missing.isError is True
```

✅ **Checkpoint:** `pytest -v -m mcp` shows **2 passed**.

---

## Part 7 – A GitLab pipeline with reports (15 min)

**Goal:** run everything automatically on every push, keep the reports, and keep the token secret.

**Step 1 – Create `.gitlab-ci.yml`.**

```yaml
stages: [test]

default:
  image: python:3.12-slim
  before_script:
    - pip install -r requirements.txt

smoke:
  stage: test
  script:
    - pytest -q --maxfail=3 -m smoke
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

api-and-mcp:
  stage: test
  script:
    - pytest -q -m "not a11y"
  artifacts:
    when: always
    expire_in: 1 week
    paths: [reports/]
    reports:
      junit: reports/junit.xml
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

a11y:
  stage: test
  image: mcr.microsoft.com/playwright/python:v1.49.0-jammy
  script:
    - pytest -q -m a11y
  artifacts:
    when: always
    expire_in: 1 week
    paths: [reports/]
    reports:
      junit: reports/junit.xml
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

**Step 2 – Add the token as a secret.** In GitLab, go to **Settings → CI/CD → Variables** and add `API_TOKEN` = `mini-project-token-01` with **Masked** and **Protected** ticked. `config.py` reads it automatically, and the client sends it as a Bearer header. JSONPlaceholder ignores the header, but a real API would need it.

**Step 3 – Push to `main`.**

```bash
git init -b main
git add .
git commit -m "Week 7 mini-project"
git remote add origin <your GitLab project URL>
git push -u origin main
```

✅ **Checkpoint:**

- The pipeline shows two green jobs: `api-and-mcp` and `a11y`.
- The pipeline's **Tests** tab lists every test (15 in total: 13 from `api-and-mcp` and 2 from `a11y`).
- Each job has **Job artifacts → Browse → reports/report.html**.

📝 **Try it (F):** create a branch, change a test so that it fails, and open a merge request. Which job runs, and where do you see the failure?

---

## Final checklist

- [ ] curl, HTTPie and Postman explored the API, and the collection has passing tests
- [ ] `BlogClient` reads its config from environment variables and always uses a timeout
- [ ] Status, JSON, fixture and cleanup tests pass (`tests/test_posts.py`)
- [ ] Schema and CSV-driven tests pass (`tests/test_contract.py`)
- [ ] Mocked failure tests pass offline (`tests/test_mocked.py`)
- [ ] The status page passes axe and the keyboard check (`-m a11y`)
- [ ] *(Optional)* The MCP tool is listed and tested (`-m mcp`)
- [ ] The pipeline is green, the reports are downloadable, and the token is masked

## Reflection questions

1. Which tests would you run on **every** merge request, and which only on `main`? Why?
2. Which of your tests would break if JSONPlaceholder really saved data? How would you change them?
3. What does the mocked suite prove that the live suite cannot, and the other way round?
4. Name one accessibility issue that axe cannot find on the status page, and how you would test for it.

---

## Answers

<details>
<summary><strong>Try it (A) – Postman 404 test</strong></summary>

```javascript
pm.test("Missing post returns 404", () => pm.response.to.have.status(404));
```

</details>

<details>
<summary><strong>Try it (B) – Parametrized status test</strong></summary>

```python
@pytest.mark.parametrize("post_id", [1, 50, 100])
def test_posts_exist(client, post_id):
    assert client.get_post(post_id).status_code == 200
```

</details>

<details>
<summary><strong>Try it (C) – Breaking the schema</strong></summary>

The tests fail with a message such as `['title']: 'sunt aut facere ...' is not of type 'integer'`. The path tells you exactly which field broke the contract.

</details>

<details>
<summary><strong>Try it (D) – 429 pass-through</strong></summary>

```python
@responses.activate
def test_rate_limit_is_passed_through():
    responses.add(responses.GET, f"{FAKE}/posts/1", status=429, headers={"Retry-After": "2"})
    r = BlogClient(base_url=FAKE).get_post(1)
    assert r.status_code == 429
    assert r.headers["Retry-After"] == "2"
```

</details>

<details>
<summary><strong>Try it (E) – Bug report for the missing label</strong></summary>

axe reports the rule `label`. Example report line: *"[A11y][Critical] Status page 'Post id' input has no accessible name – WCAG 4.1.2 / 3.3.2 (A). Screen-reader users hear only 'spin button' and cannot tell what to type."*

</details>

<details>
<summary><strong>Try it (F) – Failing merge request</strong></summary>

Only the `smoke` job runs on the merge request (`api-and-mcp` and `a11y` are main-only). If you broke a smoke test, the job is red, and the log shows the `FAILED` line and the assertion message. If you broke a non-smoke test, the merge request pipeline stays green. That failure only shows up after the merge to `main`, which is a good argument for choosing smoke tests carefully.

</details>

<details>
<summary><strong>Reflection – sample answers</strong></summary>

1. On every merge request, run fast, stable checks: smoke API tests, mocked tests and schema checks. Run the full live suite and accessibility scans on `main` (and nightly), because they are slower and depend on external systems.
2. `test_new_post_echoes_fields` (the id would not always be `101`) and `test_posts_by_user` (the count could change). Assert on the data the test created itself, and use ranges or `> 0` instead of exact counts.
3. Mocks prove error handling (500s, network failures, outbound headers) quickly and deterministically. Live tests prove the real API still matches your assumptions (the contract), which mocks cannot.
4. Examples: a logical focus order and visible focus, screen-reader announcements for status changes, and whether the text is understandable. Test these manually with the keyboard and NVDA or VoiceOver.

</details>
