# Handout 02 – Request Details & Postman

> **How to use this handout:** each topic is a small, self-contained example. Start each one fresh (a new Postman collection, or a new terminal command), and don't reuse anything from another topic. You will combine everything in **Handout 11 (Week 7 Mini-Project)**.

**Before class**

- Postman desktop app installed and signed in.
- A terminal with `curl` (Git Bash on Windows, or `curl.exe` in PowerShell) and HTTPie.
- **curl** is already installed on Windows 10/11 (`curl.exe`), macOS and most Linux systems. **HTTPie** installs with `pip install httpie` (or `brew install httpie` on macOS). Check both with `curl --version` and `http --version`. If Windows says `http` is not recognized, use `python -m httpie` instead.
- Every curl command below also has an HTTPie version, so you can try both. In HTTPie, `name=value` is a JSON string field, `name:=1` is a JSON number, `name==value` is a query parameter, and `Name:value` is a header.
- Practice APIs: `https://jsonplaceholder.typicode.com` and `https://httpbin.org` (httpbin echoes back whatever you send).

---

## Topic 4 – Query Parameters and Path Variables

### Definition

A **path variable** is part of the URL path that identifies **which** resource you want, for example the `7` in `/posts/7`. A **query parameter** is a `key=value` pair after the `?` that changes **how** you get it, for example filtering, sorting or paging (`/posts?userId=1`). Multiple query parameters are joined with `&`. Special characters such as spaces must be **percent-encoded** (a space becomes `%20`).

### Key ideas

| | Path variable | Query parameter |
|---|---|---|
| Where | Inside the path: `/users/{id}` | After `?`: `?key=value&key2=value2` |
| Used for | Identity (which one) | Filter, search, sort, page, select fields |
| Missing value | Usually `404 Not Found` | Usually ignored or a default is used |
| Postman syntax | `/posts/:id` → fill in the **Path Variables** table | **Params** tab |

- A filter that matches nothing returns `200` with an empty list `[]`, **not** `404`.
- Pagination maths: page `p` with size `n` starts at offset `(p − 1) × n`.

### Worked example – Filtering and paging

**Step 1 – Use a path variable to get one post.**

```bash
curl -s https://jsonplaceholder.typicode.com/posts/7 | python -m json.tool
```

*HTTPie version:*

```bash
http -b https://jsonplaceholder.typicode.com/posts/7
```

**Step 2 – Use a query parameter to filter posts by user.**

```bash
curl -s "https://jsonplaceholder.typicode.com/posts?userId=2" \
  | python -c "import sys, json; d = json.load(sys.stdin); print(len(d), {p['userId'] for p in d})"
```

*HTTPie version:*

```bash
http -b https://jsonplaceholder.typicode.com/posts userId==2 \
  | python -c "import sys, json; d = json.load(sys.stdin); print(len(d), {p['userId'] for p in d})"
```

In HTTPie, `name==value` adds a query parameter, so you never have to type `?` and `&` yourself.

**Step 3 – Combine parameters to filter and limit.**

```bash
curl -s "https://jsonplaceholder.typicode.com/comments?postId=1&_limit=2" | python -m json.tool
```

*HTTPie version:*

```bash
http -b https://jsonplaceholder.typicode.com/comments postId==1 _limit==2
```

**Step 4 – Encode a space and confirm what the server received.**

```bash
curl -s "https://httpbin.org/get?q=hello%20world&tag=qa&tag=api"
```

*HTTPie version:*

```bash
http -b https://httpbin.org/get q=="hello world" tag==qa tag==api
```

HTTPie encodes the space for you (as `+`), and httpbin decodes it back to `hello world`.

**Step 5 – Do the same in Postman.** Create a request `GET https://jsonplaceholder.typicode.com/posts/:id`, set `id` = `7` in **Path Variables**, then add `userId` in the **Params** tab and watch the URL update.

### Checkpoint

- Step 2 prints `10 {2}`: ten posts, all from user 2.
- Step 3 shows exactly **2** comment objects.
- Step 4 echoes `"args": {"q": "hello world", "tag": ["qa", "api"]}`. The space was decoded, and the repeated key became a list.

### Your turn

1. Get all comments for post 3 using a **query parameter**, then using a **sub-resource path**. Do both return the same number of items?
2. Request `/posts?userId=999`. What status code and body do you get? Explain why it is not `404`.
3. An API has 95 items with a page size of 10. How many pages are there, how many items are on the last page, and what is the offset of page 4?
4. Decide whether each piece of information should be a path variable or a query parameter: order id, sort direction, search text, customer id that owns the orders.

---

## Topic 5 – Headers

### Definition

**Headers** are `Name: value` lines that carry extra information about a request or response, such as the format of the body, the format the client accepts, or who the caller is. Header names are case-insensitive. Request headers describe the request (`Accept`, `Authorization`), and response headers describe the reply (`Content-Type`, `Cache-Control`). Many API failures, such as `401`, `406` and `415`, can be diagnosed by reading the headers.

### Key ideas

| Header | Sent by | Example | Typical failure if wrong |
|--------|---------|---------|--------------------------|
| `Content-Type` | Whoever sends a body | `application/json` | `415 Unsupported Media Type` |
| `Accept` | Client | `application/json` | `406 Not Acceptable` |
| `Authorization` | Client | `Bearer eyJ...` / `Basic dXNlcjpwYXNzd2Q=` | `401 Unauthorized` |
| `Retry-After` | Server | `30` | Seen with `429 Too Many Requests` |

- **Basic auth** is `username:password` in Base64. That is **encoding, not encryption**, so always use HTTPS.
- Never paste real tokens into screenshots, chat, or files you commit.

### Worked example – Sending and checking headers

**Step 1 – See the headers curl sends by default.**

```bash
curl -s https://httpbin.org/headers
```

*HTTPie version:*

```bash
http -b https://httpbin.org/headers
```

Compare the two outputs: the `User-Agent` is `curl/8.x` in one and `HTTPie/3.x` in the other.

**Step 2 – Add your own headers.**

```bash
curl -s https://httpbin.org/headers \
  -H "Accept: application/json" \
  -H "X-Request-Id: qe-week7-001"
```

*HTTPie version:*

```bash
http -b https://httpbin.org/headers Accept:application/json X-Request-Id:qe-week7-001
```

In HTTPie, `Name:value` (with a colon and no space) adds a header.

**Step 3 – Call a protected endpoint without and then with Basic auth.**

```bash
curl -i https://httpbin.org/basic-auth/user/passwd
curl -i -u user:passwd https://httpbin.org/basic-auth/user/passwd
```

*HTTPie version:*

```bash
http https://httpbin.org/basic-auth/user/passwd
http -a user:passwd https://httpbin.org/basic-auth/user/passwd
```

**Step 4 – Decode the Basic header by hand.**

```bash
echo "dXNlcjpwYXNzd2Q=" | base64 -d
```

**Step 5 – Check a header in Postman.** Send `GET https://jsonplaceholder.typicode.com/posts/1` and add this on the **Scripts → Post-response** tab:

```javascript
pm.test("Response is JSON", function () {
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});
```

### Checkpoint

- Step 2 shows `"X-Request-Id": "qe-week7-001"` echoed back.
- Step 3 returns `401` first, then `200` with `{"authenticated": true, "user": "user"}`.
- Step 4 prints `user:passwd`.
- Step 5 shows **Test Results (1/1)** with a green PASS.

### Your turn

1. Call `https://httpbin.org/bearer` with no header, then with `-H "Authorization: Bearer abc123"` (HTTPie: `http https://httpbin.org/bearer "Authorization:Bearer abc123"`). Record both status codes and bodies.
2. Base64-encode `tester:Secret1` (`echo -n "tester:Secret1" | base64`) and write the full `Authorization` header.
3. In Postman, add a test that checks the response from Step 5 has a `Cache-Control` header.
4. Match each code to the header most likely at fault: `401`, `406`, `415`.

### Common errors

- **`echo` without `-n`.** It adds a newline, so the Base64 value changes. Use `echo -n` when you encode.
- **Writing `Bearer` without a space, or adding quotes around the token.** The format must be exactly `Bearer <token>`.
- **Setting `Content-Type` on a GET with no body.** It is harmless but meaningless. It is `Accept` that controls the response format.

---

## Topic 6 – Postman Collections

### Definition

**Postman** is a desktop tool for building, sending and testing API requests without writing a full program. A **collection** is a saved, ordered group of requests, organized into folders, that you can document, share, export as JSON and run all at once. Each request can include **tests** written in JavaScript with `pm.test` and `pm.expect`. The **Collection Runner** runs every request in order and reports the pass/fail results.

### Key ideas

- **Structure:** Collection → Folders (e.g. `Posts`, `Users`) → Requests named clearly, such as `GET single post`.
- **A test passes** if its function finishes without throwing. An assertion that fails throws an error and marks the test as failed.
- **Inheritance:** authorization and scripts set at collection level apply to every request unless a request overrides them.
- **Export** gives you a Collection v2.1 JSON file that you can version in Git and share with your team.

### Worked example – Building a small collection

**Step 1 – Create the collection.** Click **+ → Collection**, name it `Collections Demo`, and add a folder named `Posts`.

**Step 2 – Add a request.** In `Posts`, add `GET single post`: `GET https://jsonplaceholder.typicode.com/posts/1`. Click **Send**, then **Save**.

**Step 3 – Add a status test** on **Scripts → Post-response**:

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

**Step 4 – Add body checks to the same script.**

```javascript
const post = pm.response.json();

pm.test("Post has the requested id", function () {
    pm.expect(post.id).to.eql(1);
});

pm.test("Title is a non-empty string", function () {
    pm.expect(post.title).to.be.a("string").and.not.be.empty;
});
```

**Step 5 – Add a second request** `POST create post` with a raw JSON body (`{"title": "x", "body": "y", "userId": 1}`) and this test:

```javascript
pm.test("Created returns 201", function () {
    pm.response.to.have.status(201);
});
```

**Step 6 – Run it.** Right-click the collection, choose **Run collection**, then click **Run Collections Demo**.

### Final code

Your `Collections Demo` collection should now contain these two requests and scripts.

**`Posts` → `GET single post` → `GET https://jsonplaceholder.typicode.com/posts/1` → **Scripts → Post-response****

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

const post = pm.response.json();

pm.test("Post has the requested id", function () {
    pm.expect(post.id).to.eql(1);
});

pm.test("Title is a non-empty string", function () {
    pm.expect(post.title).to.be.a("string").and.not.be.empty;
});
```

**`Posts` → `POST create post` → `POST https://jsonplaceholder.typicode.com/posts` → **Body → raw → JSON****

```json
{"title": "x", "body": "y", "userId": 1}
```

**`POST create post` → **Scripts → Post-response****

```javascript
pm.test("Created returns 201", function () {
    pm.response.to.have.status(201);
});
```

### How to run

1. Click **Save** on both requests.
2. Right-click `Collections Demo` and choose **Run collection**.
3. Leave both requests ticked and click **Run Collections Demo**.

### Checkpoint

The Runner summary shows **2 requests, 4 tests, 4 passed, 0 failed**, with every row green.

### Your turn

1. Add a `Users` folder with `GET all users` and a test that the response is an array of length 10 (`pm.expect(pm.response.json()).to.have.lengthOf(10)`).
2. Add `GET missing post` (`/posts/9999`) with a test that expects `404`.
3. Add a Markdown description to the collection that explains what it tests.
4. Export the collection (v2.1), open the JSON file, and find where your test scripts are stored.

### Common errors

- **Forgetting to Save.** Unsaved changes are not included in a Runner run.
- **A body set to "Text" instead of "JSON".** Postman then sends the wrong `Content-Type`. In the Body tab, choose **raw → JSON**.
- **Calling `pm.response.json()` on a non-JSON response.** It throws an error and the whole script stops.

---

## Topic 7 – Postman Variables and Environments

### Definition

A **variable** is a named placeholder written as `{{name}}` that Postman replaces with a value just before sending a request. Variables remove hard-coded values such as base URLs, ids and tokens, so one collection can run against different servers. An **environment** is a named set of variables, such as `Dev`, `Test` or `Staging`, that you switch with a dropdown. Scripts can read and write variables, which lets you **chain** requests by passing data from one response to the next request.

### Key ideas

| Scope (narrowest wins) | Set with | Typical use |
|------------------------|----------|-------------|
| Local | `pm.variables.set` | A temporary value inside one run |
| Data | CSV/JSON file in the Runner | Data-driven runs |
| Environment | Environments panel / `pm.environment.set` | `baseUrl`, credentials for each server |
| Collection | Collection → Variables / `pm.collectionVariables.set` | Values shared by every environment |
| Global | `pm.globals.set` | Rarely needed; avoid |

- **Initial vs current value:** the initial value is shared with your team, while the current value stays on your machine. Put secrets only in the current value, or mark them as **secret**.
- **Dynamic variables** such as `{{$guid}}`, `{{$randomEmail}}` and `{{$timestamp}}` generate fresh data on every send.

### Worked example – One collection, any environment

**Step 1 – Create an environment.** Click **Environments → +** and name it `JSONPlaceholder`. Add the variable `baseUrl` = `https://jsonplaceholder.typicode.com`, save it, and select it in the top-right dropdown.

**Step 2 – Create a new collection** named `Variables Demo` with one request, `GET post`, that uses the variable instead of a hard-coded URL:

```
{{baseUrl}}/posts/1
```

Hover over `{{baseUrl}}`. If the environment is selected, the value shows in a tooltip.

**Step 3 – Capture a value from the response** on the `GET post` post-response script:

```javascript
const post = pm.response.json();
pm.environment.set("userId", post.userId);
```

**Step 4 – Chain it into the next request.** Add `GET author of post` to the same collection:

```
{{baseUrl}}/users/{{userId}}
```

**Step 5 – Use a dynamic variable.** Add `POST create post` (`{{baseUrl}}/posts`, body **raw → JSON**):

```json
{ "title": "Run {{$guid}}", "body": "by {{$randomEmail}}", "userId": 1 }
```

### Final code

You should now have one environment and one collection set up like this.

**Environment `JSONPlaceholder` (selected in the top-right dropdown)**

```
Variable   Initial / current value
baseUrl    https://jsonplaceholder.typicode.com
userId     (set by the GET post script)
```

**Collection `Variables Demo` → `GET post` → URL `{{baseUrl}}/posts/1` → **Scripts → Post-response****

```javascript
const post = pm.response.json();
pm.environment.set("userId", post.userId);
```

**`GET author of post` → URL**

```
{{baseUrl}}/users/{{userId}}
```

**`POST create post` → URL `{{baseUrl}}/posts` → **Body → raw → JSON****

```json
{ "title": "Run {{$guid}}", "body": "by {{$randomEmail}}", "userId": 1 }
```

### How to run

1. Select the `JSONPlaceholder` environment in the top-right dropdown.
2. Right-click `Variables Demo`, choose **Run collection**, and keep the order: `GET post` → `GET author of post` → `POST create post`.
3. Click **Run Variables Demo**, then run it a second time.

### Checkpoint

- After Step 3, clicking the 👁 (eye) icon shows `userId` = `1` in the environment.
- Step 4 returns user 1 (`"name": "Leanne Graham"`).
- Running the collection twice shows a different `title` in the POST response each time.

### Your turn

1. Create a second environment, `Broken`, where `baseUrl` points to `https://jsonplaceholder.typicode.com/wrong`. Run the collection with it and describe what fails.
2. Add `baseUrl` as a **collection** variable of `Variables Demo` as well, give it a different value, and prove which one wins when both exist.
3. Add a pre-request script that sets `pm.variables.set("postId", 5)` and change a request to use `{{postId}}`.
4. Add `apiKey` to an environment and mark it **secret**. What do teammates see if you share the environment?

### Common errors

- **"No environment" is selected.** `{{baseUrl}}` then shows in red and the request fails with `Invalid URL`.
- **Typos in variable names.** `{{baseURL}}` and `{{baseUrl}}` are different names, because names are case-sensitive.
- **Putting secrets in the initial value.** That value syncs to your team workspace.

---

## Answers

<details>
<summary><strong>Topic 4 – Query Parameters and Path Variables</strong></summary>

1. `/comments?postId=3` and `/posts/3/comments` both return **5** comments.
2. `200 OK` with `[]`. The collection `/posts` exists, and the filter simply matched nothing. `404` would mean the resource itself does not exist.
3. There are 10 pages (95 ÷ 10 rounded up). The last page has 5 items. Page 4 starts at offset `(4 − 1) × 10 = 30`.
4. Order id → path (`/orders/{id}`). Sort direction → query (`?order=desc`). Search text → query (`?q=...`). Owning customer → either a path (`/customers/{id}/orders`) or a query (`/orders?customerId=...`). Both are defensible, so the API documentation decides.

</details>

<details>
<summary><strong>Topic 5 – Headers</strong></summary>

1. Without a header you get `401` with an empty body. With the header you get `200` and `{"authenticated": true, "token": "abc123"}`.
2. `dGVzdGVyOlNlY3JldDE=` → `Authorization: Basic dGVzdGVyOlNlY3JldDE=`.
3. ```javascript
   pm.test("Has Cache-Control header", function () {
       pm.response.to.have.header("Cache-Control");
   });
   ```
4. `401` → `Authorization`. `406` → `Accept`. `415` → `Content-Type`.

</details>

<details>
<summary><strong>Topic 6 – Postman Collections</strong></summary>

1. ```javascript
   pm.test("Returns 10 users", function () {
       pm.response.to.have.status(200);
       pm.expect(pm.response.json()).to.be.an("array").and.have.lengthOf(10);
   });
   ```
2. ```javascript
   pm.test("Missing post returns 404", function () {
       pm.response.to.have.status(404);
   });
   ```
3. Click the collection → **Overview** → edit the description field (Markdown is supported).
4. Each request has an `event` array. The `listen: "test"` entry holds `script.exec`, which is a list of your script's lines.

</details>

<details>
<summary><strong>Topic 7 – Postman Variables and Environments</strong></summary>

1. Every request returns `404`, so the status tests fail. In the chained request, `userId` is never set (the `404` body is `{}`), so `{{userId}}` stays unresolved.
2. The **environment** value wins over the collection value. You can prove it by hovering over `{{baseUrl}}` or by logging `pm.variables.get("baseUrl")` in the Console.
3. Pre-request script: `pm.variables.set("postId", 5);` and URL: `{{baseUrl}}/posts/{{postId}}`. This is a local variable, so it lasts for that run only.
4. Teammates see the variable name but a masked value. Only the initial value is shared, so leave the initial value empty for secrets.

</details>
