# Postman Collections

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what Postman is, what problems it solves, and why Quality Engineering (QE) teams use it.
- Install Postman, create an account, and understand the difference between the desktop app, the web app, and workspaces.
- Navigate every major area of the interface: sidebar, tabs, request builder tabs, response viewer, and Console.
- Send GET, POST, PUT, and DELETE requests step by step and read each part of the response.
- Create a **collection**, organise it with folders and sub-folders, apply a naming convention, and control request order.
- Document requests and collections using Markdown descriptions.
- Configure collection-level authorization and scripts, and explain how inheritance works.
- Write automated checks in JavaScript using `pm.test`, `pm.expect`, and `pm.response`, and explain every line.
- Save examples, run collections with the Collection Runner, and read the run results.
- Export and import a Collection v2.1 JSON file and read its structure.
- Use workspaces, forking, sharing, History, and the Console to collaborate and debug.
- Build a complete "Project 2 API" collection and avoid the most common beginner mistakes.

---

## Why This Matters

This week's epic is to add API testing, accessibility testing, and CI/CD to your Project 2 test automation framework. Everything in that epic starts with a single skill: being able to talk to an API and judge whether it answered correctly. Before you write a line of Python, you need to understand what the API offers, how its requests are shaped, and what a healthy response looks like. Postman is where most professional testers do exactly that.

In the previous lessons today you learned about HTTP messages, REST principles, and the four core methods. You may have tried them with a command-line tool such as `curl`. That works, but it has real limits. Long commands are easy to mistype, there is no built-in place to organise fifty requests, sharing means pasting text into chat messages, and there is no quick way to see whether twenty checks all passed. Postman gives you the same power with a graphical interface plus organisation, documentation, scripting, and sharing.

Imagine you join a team on your first day and are told, "Here is the new Orders API; test it by Friday." Without a tool you would be reading specifications and guessing. With Postman you can send a first request in two minutes, see real data, and begin building a reusable suite. That suite, a **collection**, becomes four different assets at once:

- **Living documentation.** Anyone can open it and see exactly how to call each endpoint.
- **A regression pack.** You can re-run every check with one click after each deployment.
- **A blueprint for automation.** Tomorrow you will translate what you discover here into Python code, and the request order, URLs, bodies, and expected results you record today become the specification for that code.
- **A shareable file.** The collection exports as JSON, which means it can live in Git beside your code. On Friday you will see how a pipeline can run it automatically; for now, simply know that your collection is designed to leave your laptop.

Your Monday exercise is to build a Postman collection for the Project 2 API as a project milestone. Mastering collections today is therefore not an academic exercise; it is the first deliverable of the week.

---

## The Concept

### 1. What Is Postman?

**Postman** is an API platform: a single product where you can design, send, test, document, mock, monitor, and share API requests. At its heart is a request builder. You choose an HTTP method, type a URL, optionally add headers, parameters, and a body, press **Send**, and inspect the response. Around that core, Postman adds organisation (collections), reuse (variables and environments), automation (scripts and the Collection Runner), and collaboration (workspaces and sharing).

**Why QE teams use it.** There are several reasons it became the default tool:

1. **Speed of exploration.** You can understand an unfamiliar API in minutes, before any code exists.
2. **Low barrier to entry.** Manual testers, developers, and analysts can all use it without programming knowledge, so it becomes a common language between roles.
3. **Visible results.** Status code, time, size, headers, and body are all shown in one place, which makes bugs easy to demonstrate and report.
4. **Built-in checks.** Short JavaScript snippets can turn an exploratory request into a repeatable test.
5. **Sharing.** A collection is a single artifact that can be handed to a developer with a bug report: "run this and you will see the failure."

**What Postman is not.** Postman is not a replacement for a coded automation framework. It is excellent for exploration, quick feedback, smoke checks, and documentation. A full framework, with complex data setup, reusable libraries, fixtures, parallel execution, and reporting integrated into your repository, is written in code. You will build that in Python starting tomorrow. A useful rule of thumb is: **explore and prototype in Postman, then industrialise in code.** Many teams keep both: the Postman collection as a quick, human-friendly check and the Python suite as the deep regression layer.

### 2. Installing Postman and Signing Up

Postman is available in two forms.

**The desktop app** runs on Windows, macOS, and Linux. You download it from the official Postman website, run the installer, and open the app. Its main advantage is that it can reach APIs running on your own machine (for example `http://localhost:3000`) and gives you full access to the Console and file features. For this course, the desktop app is recommended.

**The web app** runs in your browser at the Postman website after you sign in. It needs no installation, which is convenient on a locked-down computer. However, a browser cannot talk to a service on your local machine without extra setup (a small helper called the Postman Agent), and some features behave slightly differently.

**Signing up.** Postman works best with a free account. Create one with your email or a Google account. The free tier is sufficient for everything in this course. The account matters because it syncs your collections to the cloud, so the work you do on one computer appears on another, and it is required to join shared workspaces. Some versions of the app offer a lightweight "scratch pad" mode with no account, but that mode stores data only locally, has fewer collaboration features, and is not what we use here.

**Workspaces.** The first thing you see after signing in is a **workspace**. A workspace is a container that holds collections, environments, and other resources for a particular purpose. There are different kinds:

- **Personal workspace:** visible only to you. Use it for learning and experiments.
- **Team workspace:** visible to members of your team, so everyone sees the same collections and changes are synced. Use it for real project work.
- **Public workspace:** visible to anyone on the internet. Do not put work or secrets here by accident.
- **Partner workspace:** shared with external collaborators.

The workspace switcher is in the top bar. Before you create anything, always glance at the workspace name so you know who can see your work. In this course, create a personal workspace named something like `QE Training - Week 7`, and later your instructor may invite you to a team workspace for Project 2.

### 3. A Screen-by-Screen Tour of the Interface

Postman's layout changes slightly between versions, but the concepts are stable. We walk through it from outside to inside.

#### 3.1 The top bar

The top bar contains the **workspace switcher**, a **search** box (to find collections, requests, and more), the **Import** button, and account and settings icons. The settings (gear) icon opens options such as theme, request timeout, SSL certificate verification defaults, and proxy configuration.

#### 3.2 The sidebar (left)

The sidebar is your filing cabinet. Its main sections are:

- **Collections:** every collection in the workspace, expandable into folders and requests.
- **Environments:** named sets of variables (for example "Development" and "Staging"). You will learn them in the last lesson today.
- **History:** a chronological list of requests you have sent, even if you never saved them.
- Depending on the version you may also see **Flows**, **Mock Servers**, and **APIs**. You can ignore these for now.

A small **+** button creates a new collection, and a menu (three dots) next to each collection offers options such as Add request, Add folder, Rename, Duplicate, Export, and Run.

#### 3.3 Tabs

The central area uses **tabs**, like a web browser. Each open request lives in its own tab. A tab title shows the method (coloured: GET is green, POST is orange, PUT is blue, DELETE is red) and the request name. If a tab title is in italics, or has a dot, the request has unsaved changes. You open a new tab with the **+** icon, and you can drag tabs to reorder them. An unsaved request that was never placed into a collection appears as "Untitled Request".

#### 3.4 The request builder

Inside a tab, the top row contains three things from left to right: the **method dropdown** (GET, POST, PUT, PATCH, DELETE, and more), the **URL bar**, and the **Send** button, next to a **Save** button. Beneath that is a row of tabs that configure the request. Each one matters, so we take them one at a time.

**Params.** This tab lists the **query parameters**, the key-value pairs after the `?` in a URL. If you type `https://jsonplaceholder.typicode.com/posts?userId=1` into the URL bar, Postman automatically shows a row with key `userId` and value `1` in this table. It works the other way too: typing in the table updates the URL. Each row has a checkbox, so you can temporarily switch a parameter off without deleting it. Query parameters and path variables get their own full lesson later today, so here it is enough to know where they live.

**Authorization.** Many APIs need to know who is calling. This tab lets you choose a type from a dropdown, such as *No Auth*, *API Key*, *Bearer Token*, *Basic Auth*, and *OAuth 2.0*. Postman then adds the right header for you. For example, choosing **Bearer Token** and pasting a token makes Postman send `Authorization: Bearer <token>`. There is also a very important option called **Inherit auth from parent**, which means "use whatever the folder or collection says". We return to this in the inheritance section.

**Headers.** This tab lists the HTTP request headers you studied in the HTTP messages lesson. You can add your own, such as `Accept: application/json`. Postman also sends some headers automatically (such as `Content-Type`, `Content-Length`, `User-Agent`, and `Host`). Clicking the **hidden** link shows these auto-generated headers. A header you add manually with the same name overrides the automatic one. There is a dedicated Headers lesson later today.

**Body.** For methods that send data (POST, PUT, PATCH), the body is the payload. A row of radio buttons selects its type:

- **none:** no body. This is the default and what you use for GET and DELETE in most cases.
- **form-data:** key-value pairs sent as `multipart/form-data`. This is the type used for file uploads, because a row can be changed from *Text* to *File*.
- **x-www-form-urlencoded:** key-value pairs encoded like a query string (`name=Asha&role=tester`) and sent with `Content-Type: application/x-www-form-urlencoded`. This is the format traditional HTML forms use.
- **raw:** free text that you type yourself. A dropdown on the right chooses the language: Text, JavaScript, **JSON**, HTML, or XML. Choosing JSON sets `Content-Type: application/json` automatically and enables syntax colouring and error highlighting. Most modern REST APIs expect raw JSON.
- **binary:** a single file as the entire body, such as an image or a PDF, with no wrapper around it.
- **GraphQL:** a special editor for GraphQL APIs, where you write a query and optional variables. REST testing is our focus this week, so just recognise it.

**Scripts.** This tab holds JavaScript that Postman runs automatically. It has two sub-tabs. **Pre-request** code runs *before* the request is sent (for example, to generate a random value or set a variable). **Post-response** code runs *after* the response arrives (for example, to check the status code). In older versions of Postman the post-response area was called **Tests**, so you may see that name in tutorials. The scripting language is JavaScript, and you will see it in detail soon.

**Settings.** Per-request behaviour switches. Typical items include whether to **follow redirects**, whether to **enable SSL certificate verification**, whether to send the **cookie header automatically**, and a request-specific timeout. Beginners rarely need to change these. One worth remembering is SSL verification: if a test server uses a self-signed certificate and Postman refuses to connect, this setting is where you can relax it for that request. Never turn it off for production systems.

**Documentation icon.** At the right edge of the builder there are shortcut icons, including one for **Documentation**, where you write the description for that request.

#### 3.5 The response viewer

When you press Send, the lower half of the tab shows the response. At its right edge you see three vital statistics: **Status** (for example `200 OK`), **Time** (how long the round trip took, in milliseconds), and **Size** (how large the response was). Hovering over each reveals more detail. For instance, hovering over Time shows a breakdown into DNS lookup, connection, TLS handshake, and transfer, and hovering over Status explains the meaning of the code.

The response viewer has its own tabs:

- **Body** shows the payload and has three view modes. **Pretty** formats JSON or XML with indentation and colouring, making it easy to read, and lets you collapse sections. **Raw** shows exactly the text that arrived, with no formatting, which is useful when you suspect the formatting hides something such as stray whitespace. **Preview** renders the response as a web page, useful when the API returns HTML. For JSON APIs you will use Pretty almost all the time.
- **Cookies** lists the cookies the server asked the client to store, with their domain, path, and expiry.
- **Headers** lists every response header, for example `Content-Type`, `Cache-Control`, and `Server`.
- **Test Results** lists each `pm.test` check as PASS or FAIL, along with an error message for failures. A count such as `3/4` appears in the tab title.

If a request fails before any response arrives (for example, the server is unreachable or the name does not resolve), Postman shows an error message such as "Could not get response" instead of a status code. That is a *connection* problem, not an HTTP status, and it is worth learning to tell the two apart.

#### 3.6 The Console

At the bottom-left of the window is a **Console** button (or choose *View > Show Postman Console* in some versions). The Console records everything Postman does: every request line, the headers that were actually sent, the response, and any message printed by `console.log` in your scripts. It is the equivalent of a flight recorder and your best debugging tool. We use it in a dedicated section later.

### 4. Sending Requests Step by Step

We use **JSONPlaceholder**, a free public fake REST API at `https://jsonplaceholder.typicode.com`. It accepts writes but does not actually store them, which makes it safe for practice: a POST returns a realistic success response, but the data is not permanently saved.

#### 4.1 GET: reading data

1. Click **+** to open a new tab.
2. Leave the method as **GET**.
3. Type `https://jsonplaceholder.typicode.com/posts/1` in the URL bar.
4. Click **Send**.

You should see `200 OK`, a time of roughly 100 to 400 milliseconds, and a JSON body like this:

```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur..."
}
```

This is one *post resource*: an object with four fields. Notice what we did not need: no body and no special header. GET is a read, so the URL alone identifies what we want. Try changing the URL to `/posts` (without the 1) and you will receive an array of one hundred posts, and the Size will grow accordingly. Then try `/posts/9999`. The status becomes `404 Not Found` and the body is an empty object `{}`. That is your first look at a negative scenario: asking for something that does not exist.

#### 4.2 POST: creating data

1. Open a new tab and change the method to **POST**.
2. URL: `https://jsonplaceholder.typicode.com/posts`.
3. Open the **Body** tab, select **raw**, and select **JSON** from the dropdown on the right.
4. Type this JSON in the editor:

```json
{
  "title": "Created from Postman",
  "body": "Hello API",
  "userId": 1
}
```

5. Click **Send**.

The expected result is `201 Created` and a response containing your data plus a new `id` (JSONPlaceholder always answers `101`). The code `201`, rather than `200`, is the REST convention for "a new resource was created". Open the request's **Headers** tab and click the hidden headers link: you will see that Postman added `Content-Type: application/json` because you picked JSON in the raw dropdown. If you had left the dropdown on Text, the server might not understand the body, which is a classic source of confusing `400` or `415` errors.

#### 4.3 PUT: replacing data

1. New tab, method **PUT**.
2. URL: `https://jsonplaceholder.typicode.com/posts/1`. Note that PUT targets an *existing* resource, so the id is in the URL.
3. Body: raw JSON with the *complete* replacement:

```json
{
  "id": 1,
  "title": "Updated title",
  "body": "Updated body",
  "userId": 1
}
```

4. Click **Send**. Expect `200 OK` and the updated object echoed back.

PUT means "replace the whole resource with what I send". If a real API followed this strictly and you omitted a field, that field might be cleared. (PATCH is the method for partial updates; the next lesson covers the distinction.)

#### 4.4 DELETE: removing data

1. New tab, method **DELETE**.
2. URL: `https://jsonplaceholder.typicode.com/posts/1`.
3. Leave Body as **none**.
4. Click **Send**. Expect `200 OK` with an empty JSON object.

Real APIs often respond `204 No Content` (success, deliberately nothing in the body) or `200`. The specification of *your* API decides, and the tests you write must match that specification.

#### 4.5 Saving a request

Until you press **Save** (or `Ctrl+S` / `Cmd+S`), a request is only a draft and appears in History. Pressing Save opens a dialog where you choose a name and the collection or folder where it should live. Always save with a meaningful name; the dialog is also where you can create a new collection on the fly.

### 5. What Is a Collection?

A **collection** is a saved, named group of requests, together with everything that belongs to them: folders, descriptions, authorization settings, scripts, variables, and examples. A helpful analogy is a **recipe binder**. A single request is one recipe card. The collection is the binder, with dividers (folders) for starters, mains, and desserts, a cover page explaining the binder (the description), and a note at the front that applies to every recipe, such as "always preheat the oven" (collection-level settings).

A collection can contain:

- **Requests:** individual saved API calls.
- **Folders and sub-folders:** groups of related requests, which can be nested.
- **Variables:** reusable values (the final lesson today covers these).
- **Authorization:** one setting that all requests can inherit.
- **Scripts:** pre-request and post-response code that runs for every request inside.
- **Documentation:** Markdown text that describes the collection and each request.
- **Examples:** saved sample responses.

In the interface, a collection has its own page (click its name) with tabs for Overview, Authorization, Scripts, Variables, and Runs. Folders have a similar, smaller page. This arrangement matters because settings placed higher in the tree flow downward.

### 6. Creating a Collection, Folders, and Naming Conventions

#### 6.1 Creating a collection

1. In the sidebar, click **+** next to Collections (or choose *New > Collection*).
2. Choose a blank collection and name it, for example `Project2-API-Tests`.
3. On the collection's **Overview** tab, write a description (we cover Markdown shortly).
4. Click the three dots next to the collection and choose **Add folder**. Name it.
5. To create a folder inside a folder (a **sub-folder**), use the three dots on the folder and choose Add folder again.
6. To add a request, choose **Add request** from the three-dots menu of the collection or a folder. Alternatively, build a request in a tab and use Save to choose a destination.

#### 6.2 A folder structure that scales

Folders should mirror how the team thinks about the API. A common and effective pattern is one folder per *resource* (users, posts, orders), then separate folders for *scenarios* such as negative tests. For example:

```
Project2-API-Tests
 ├── 00 - Smoke
 ├── 01 - Users
 │    ├── Happy path
 │    │    ├── GET - List users
 │    │    ├── GET - Get user by ID
 │    │    ├── POST - Create user
 │    │    ├── PUT - Update user
 │    │    └── DELETE - Delete user
 │    └── Negative
 │         ├── GET - User not found returns 404
 │         └── POST - Missing required field returns 400
 ├── 02 - Posts
 └── 99 - Cleanup
```

The tree above uses a sub-folder pair (Happy path and Negative) inside Users. This separation means you can run only the negative tests when needed, and a teammate scanning the tree sees at once which scenarios are covered.

#### 6.3 A naming convention

Names are the table of contents of your suite. Choose a pattern and apply it everywhere. A reliable one is:

`METHOD - Action or scenario [expected result]`

Examples: `POST - Create user with valid data`, `GET - Get user by ID`, `GET - User not found returns 404`. The method is first so the list sorts and scans well; the scenario is in plain language so a person reading a failed run immediately knows what broke without opening the request. Avoid vague names such as `Request 1`, `test`, or `new request copy`. Use numeric prefixes (`01 -`, `02 -`) on *folders* when their order matters, because Postman sorts siblings by position, and prefixes make the intent explicit in exports and reports.

#### 6.4 Request ordering

Inside a collection or folder, requests appear in a specific order, and the Collection Runner executes them from top to bottom by default. You change the order by **dragging and dropping** requests or folders. Order matters because tests are often dependent: a request that creates a record should come before the one that reads it, and a cleanup request that deletes it should come last. Good practice is to make each request as independent as possible, but when order does matter, make it deliberate and mention it in the folder description.

### 7. Documenting Collections and Requests with Markdown

Both collections, folders, and individual requests have a description area. It accepts **Markdown**, a lightweight way to format text using plain characters. The basics:

```markdown
# Project 2 API Tests

Regression suite for the **Project 2** REST API.

## How to run
1. Select the *Project 2 - Dev* environment.
2. Run the folder `00 - Smoke` first.

## Notes
- Requests in `01 - Users` depend on each other and must run in order.
- `99 - Cleanup` removes test data.

| Folder | Purpose |
|--------|---------|
| 00 - Smoke | Fast health checks |
| 01 - Users | CRUD for users |
```

In Markdown, lines starting with `#` become headings (more `#` characters mean a smaller heading), text wrapped in double asterisks becomes bold, single asterisks become italic, lines beginning with `1.` form a numbered list, lines beginning with `-` form a bullet list, and the pipe-and-dash syntax makes a table. Backticks mark code.

For a single request, a good description answers three questions: *What does this request do? Which inputs are required or optional? What do we expect back (status code and key fields)?* For example, "Creates a new user. Requires `name` and `email`. Expect `201` and a response containing the new `id`." Postman can turn these descriptions into browsable web documentation (a published docs page) automatically, but even if you never publish them, they make the collection understandable to a teammate and to your future self six months later.

### 8. Collection-Level Authorization, Scripts, and Inheritance

Imagine fifty requests that all need the same bearer token. Entering it fifty times would be tedious and, if the token changed, a nightmare to fix. Postman solves this with **inheritance**: settings made at a higher level automatically apply to everything below, unless something lower overrides them.

The tree has three levels: **collection**, then **folder**, then **request**.

#### 8.1 Inheriting authorization

Open the collection page and click the **Authorization** tab. Choose a type, for example *Bearer Token*, and enter the token (ideally as a variable such as `{{token}}`, which you will learn soon). Now open any request inside the collection and look at its Authorization tab. By default it shows **Inherit auth from parent**, with a note that it uses the collection's setting. The request sends the token without you setting anything on it.

Folders can override. If the folder `Public endpoints` should not send a token, set that folder's Authorization to **No Auth**. Requests inside inherit from the folder, not the collection. A single request can also override everything by choosing its own type. The rule is simple: **the nearest explicit setting wins; "Inherit" means look one level up.**

#### 8.2 Collection-level and folder-level scripts

The **Scripts** tab on the collection and on a folder works the same way as on a request, but the code runs for *every* request beneath it. The order of execution is:

1. Collection script.
2. Folder script (each folder level from outer to inner).
3. Request script.

This ordering applies to the pre-request stage and to the post-response stage alike. In practice you use collection-level scripts for things that every request needs: a pre-request script that prints the request name to the Console, or a post-response script that checks that *no* request returns a server error (`5xx`) or takes more than a few seconds. You write it once and it protects the whole collection. Request-level scripts remain for checks that are specific to one request.

A caution that trips up beginners: if a collection-level post-response script contains a check that fails for one special request (for example, one that deliberately expects a 404), that failure will show for that request too. Design shared checks to be general ("response time is under 3000 ms"), and keep specific expectations at the request level.

### 9. Writing Tests in Postman

Postman's scripting language is **JavaScript**. This is simply the language the tool understands; the Python equivalents arrive tomorrow. You do not need to be a JavaScript developer. A handful of ideas cover nearly everything you will write. This section starts with the syntax and then builds up the checks.

#### 9.1 JavaScript syntax you need

Before reading the code, here are the building blocks, since you may be meeting them for the first time.

- **Comments.** Text after `//` on a line is ignored by the computer and is there for humans.
- **Variables.** `const body = ...;` creates a named container whose contents will not be reassigned. `let` creates one that can be reassigned. A semicolon `;` ends a statement.
- **Strings.** Text in quotes, such as `"Status code is 200"`.
- **Functions.** A function is a reusable block of code. `function () { ... }` defines one without a name (an *anonymous* function). The newer *arrow function* style `() => { ... }` means the same thing. You will see both; they are interchangeable for our purposes.
- **Objects and dot access.** A JSON response becomes a JavaScript object. `body.title` means "the value stored under the key `title`". `body.address.city` goes one level deeper.
- **Arrays.** A list in square brackets. `items[0]` is the first element (counting starts at zero), and `items.length` is how many there are.
- **Method chaining.** `pm.expect(x).to.be.a("string")` reads almost like English. The words `to`, `be`, `an`, and `have` are placeholders that make the sentence readable and change nothing.

#### 9.2 The `pm` object

`pm` is a ready-made object that Postman supplies inside every script. It is your doorway to everything: `pm.response` is the response you just received, `pm.request` is the request that was sent, `pm.test` defines a check, and `pm.expect` makes a comparison. You never create `pm`; it is simply there.

#### 9.3 The anatomy of a test

Here is the smallest complete test:

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

Explained line by line:

- Line 1: `pm.test(` starts a test. It takes two arguments. The first, `"Status code is 200"`, is the **test name**; it appears in Test Results, so write it as a readable sentence. The second argument, `function () {`, is the **body of the test**, the code to run.
- Line 2: `pm.response.to.have.status(200);` is an **assertion**: a statement that must be true. `pm.response` is the response object, `.to.have.status(200)` asserts that its status code is 200. If it is, nothing happens and the test passes. If not, Postman raises an error, and the test is reported as failed with a message like "expected response to have status code 200 but got 404".
- Line 3: `});` closes the function and the `pm.test(` call.

The rule to remember: **a test passes if its function finishes without an error and fails if an assertion throws one.** One test can contain several assertions, but the first failing one stops that test, so keep tests small and focused so a failure points to one cause.

#### 9.4 Status code tests

```javascript
pm.test("Status code is 201 Created", function () {
    pm.response.to.have.status(201);
});

pm.test("Status code is a success code", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 201, 204]);
});

pm.test("Status text is OK", function () {
    pm.response.to.have.status("OK");
});
```

Explanation: The first test is the standard exact check. The second reads the number directly using `pm.response.code` and uses `.to.be.oneOf([...])`, which passes if the value appears in the given array; the square brackets create an array of acceptable codes. This is useful when the specification allows several answers. The third checks the status *text* instead of the number; passing a string to `status(...)` compares against the reason phrase. In general prefer the number, since numbers are what specifications define.

#### 9.5 Header tests

```javascript
pm.test("Content-Type header is JSON", function () {
    pm.response.to.have.header("Content-Type");
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});
```

Explanation: The first assertion checks that a header named `Content-Type` exists. The second uses `pm.response.headers.get("Content-Type")` to read the header's *value*, then `.to.include("application/json")` checks that the text contains that fragment. We use `include` rather than an exact match because servers commonly send `application/json; charset=utf-8`, and an exact comparison would fail because of the extra `charset` part. Header names are case-insensitive in HTTP, and Postman honours that.

#### 9.6 Body field tests

```javascript
pm.test("Post 1 has the expected id and user", function () {
    const body = pm.response.json();
    pm.expect(body.id).to.eql(1);
    pm.expect(body.userId).to.equal(1);
});
```

Explanation: `pm.response.json()` takes the response text and **parses** it, converting JSON text into a JavaScript object that you can navigate with dots. We store it in a constant called `body` (you may name it anything). `pm.expect(body.id)` wraps the value we want to inspect, and `.to.eql(1)` asserts it equals 1. `eql` performs a deep comparison and `equal` performs a strict comparison; for numbers and strings they behave identically, and the difference only appears with objects and arrays, where `eql` compares their contents.

If the response is *not* valid JSON (for example, an HTML error page), `pm.response.json()` itself throws a parse error, and the test fails with a message about unexpected tokens. This is a common source of confusing failures, and the Raw view of the body is how you diagnose it.

#### 9.7 Type tests

```javascript
pm.test("Field types are correct", function () {
    const body = pm.response.json();
    pm.expect(body.title).to.be.a("string");
    pm.expect(body.id).to.be.a("number");
    pm.expect(body.title).to.not.be.empty;
    pm.expect(body).to.have.property("userId");
});
```

Explanation: `.to.be.a("string")` asserts the type; other useful type names are `"number"`, `"boolean"`, `"object"`, and `"array"`. `.to.not.be.empty` combines negation (`not`) with the `empty` check, so it fails for an empty string, an empty array, or an empty object. Note that `empty` is written without parentheses because it is a property, not a function call. `.to.have.property("userId")` asserts that the key exists on the object, regardless of its value. Type checks are powerful: a bug where a number arrives as a string (`"1"` instead of `1`) is the kind of defect that breaks other systems yet is invisible to the eye in the Pretty view.

#### 9.8 Array tests

```javascript
pm.test("List returns 100 posts", function () {
    const posts = pm.response.json();
    pm.expect(posts).to.be.an("array");
    pm.expect(posts).to.have.lengthOf(100);
});

pm.test("Every post has id, title and userId", function () {
    const posts = pm.response.json();
    posts.forEach(function (post) {
        pm.expect(post).to.have.all.keys("userId", "id", "title", "body");
    });
});

pm.test("The first post belongs to user 1", function () {
    const posts = pm.response.json();
    pm.expect(posts[0].userId).to.eql(1);
});
```

Explanation: In the first test, `an("array")` confirms the top-level value is a list (note that `an` and `a` are interchangeable aliases), and `lengthOf(100)` checks how many elements it holds. In the second, `posts.forEach(function (post) { ... })` is a **loop**: it runs the inner function once for each element, naming the current element `post`. Inside, `to.have.all.keys(...)` asserts that the object has exactly those keys and no others. Looping over every element is how you verify that *all* items, not only the first, follow the contract. In the third, `posts[0]` selects the first element by index. Be careful: asserting on a fixed position makes a test fragile if the data order can change.

#### 9.9 Response time tests

```javascript
pm.test("Response time is under 1000 ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(1000);
});
```

Explanation: `pm.response.responseTime` is the number of milliseconds the call took, and `.to.be.below(1000)` asserts that it is less than one second. Choose the threshold from the team's agreed performance expectation rather than from what you happened to observe, and be aware that response time in a single run is noisy because of network conditions. Treat this as a coarse safety net, not a performance test.

#### 9.10 JSON schema validation (awareness level)

A **JSON schema** is a document that describes the *shape* of valid JSON: which fields must exist, and what type each has. Instead of writing many individual assertions, you write the schema once and ask Postman to check the entire response against it.

```javascript
const schema = {
    type: "object",
    required: ["userId", "id", "title", "body"],
    properties: {
        userId: { type: "integer" },
        id: { type: "integer" },
        title: { type: "string" },
        body: { type: "string" }
    }
};

pm.test("Response matches the post schema", function () {
    pm.response.to.have.jsonSchema(schema);
});
```

Explanation: The `const schema = { ... };` defines an object that describes the expected shape. `type: "object"` says the response must be an object. `required` lists the keys that must be present. `properties` states the allowed type for each key. The test then calls `pm.response.to.have.jsonSchema(schema)`, which validates the response and fails with a list of violations if it does not match. Postman's sandbox also bundles two JavaScript validation libraries, **tv4** (older, used as `tv4.validate(data, schema)`) and **Ajv** (more modern and the one behind `jsonSchema`). You will encounter both in older tutorials. At this stage, just remember the idea: *a schema is a reusable description of a valid response*. Tuesday and Wednesday revisit validation in Python, where the same concept returns in a more powerful form.

#### 9.11 Reading what you wrote: where results appear

After clicking Send, open the **Test Results** tab in the response viewer. Each `pm.test` appears as one line, with PASS in green or FAIL in red. A failed line shows an assertion message. For example, `AssertionError: expected 404 to equal 200` means "the actual value (404) was not what you asserted (200)". Learn to read these messages carefully; the actual value is always the first number or text, and the expected value is second.

### 10. Saving Examples with Requests

An **example** is a saved request-and-response pair attached to a request, showing what a typical interaction looks like. In the response viewer, there is a **Save Response** option with **Save as example**. Give it a descriptive name such as `201 - Created successfully` or `404 - User not found`.

Why save examples?

1. **Documentation.** The examples appear under the request in the sidebar and in published docs, so a reader sees real sample data without sending anything.
2. **Evidence.** You can save the response that proved a bug, and attach it to your defect report.
3. **Mocking (awareness).** Postman can use examples to build a mock server that imitates the API before it exists. Wednesday's HTTP mocking lesson explores mocking concepts in code.

A good practice is to save one example per important outcome: success, validation error, not found, unauthorised.

### 11. The Collection Runner in Detail

The **Collection Runner** executes many requests automatically, in sequence, and reports the combined results. It converts a collection of exploratory requests into a regression pack.

#### 11.1 Starting a run

Hover over the collection (or a folder) in the sidebar, click the three dots, and choose **Run collection** (or **Run folder**). Alternatively, open the collection's page and use its **Run** tab. A configuration screen appears.

#### 11.2 The settings, one by one

- **Requests list:** every request is shown with a checkbox. Untick any you want to skip, and drag to reorder. The order set here applies to this run only.
- **Iterations:** how many times the entire selection is repeated. With `1`, each request runs once. With `3`, the whole sequence runs three times. Iterations are useful for repeated stability checks or, together with a data file, for running the same requests with different inputs.
- **Delay:** a pause in milliseconds between requests. Use it when the API enforces rate limits (a cap on requests per minute) or when a server needs time to process a change. Without a delay, Postman fires requests as quickly as it can.
- **Data file (awareness):** you may upload a CSV or JSON file in which each row (or object) represents one iteration. Postman substitutes the row's values into variables of the same name. This is the beginning of *data-driven testing*, which Wednesday covers in depth. For today, recognise that the feature exists and the number of rows decides the number of iterations.
- **Persist responses for a session and keep variable values:** options that control whether responses are stored for later viewing and whether variable changes made during a run are kept afterwards. Leave the defaults unless you have a reason.
- **Other run modes:** Postman can also schedule runs in the cloud or run a collection from the command line. The command-line route (a tool called **Newman**) is outside this week's lessons, and we do not need it today.

Click **Run** to begin.

#### 11.3 Reading the results

The results page lists requests as they complete. For each you see the method, the name, the status code, the time, and the response size. Beneath each are the tests, shown as passed or failed. At the top there is a summary of total requests, passed tests, failed tests, and total duration. Click a request in the results to see exactly what was sent and received, which is how you diagnose a failure: find the red line, open it, read the assertion message, and then compare the request and response with your expectation.

Two cautions. First, a request can return `200` and still show failures if a test inside it failed; "failed" refers to *tests*, not only HTTP status. Second, a request with **no tests** is reported as having nothing to check, so it can never fail on content. This is why the best practices below insist that every request has at least one test.

Finally, the results can be exported as a JSON file, useful for attaching a record of a run to a ticket.

### 12. Exporting and Importing Collections (Collection v2.1)

Everything in a collection can be exported to a single JSON file. The format has a version number; **Collection v2.1** is the current commonly used one.

**Export:** click the three dots on the collection, choose **Export**, pick **Collection v2.1**, and save the file, for example `Project2-API-Tests.postman_collection.json`.

**Import:** click **Import** in the top bar or sidebar and drag the file in, or paste a link or raw JSON text. The collection reappears fully intact.

#### 12.1 Reading the structure line by line

Here is a small but realistic export, trimmed for readability:

```json
{
  "info": {
    "_postman_id": "8f3c2d1e-0000-0000-0000-000000000001",
    "name": "Project2-API-Tests",
    "description": "Regression collection for the Project 2 API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "01 - Users",
      "item": [
        {
          "name": "POST - Create user",
          "event": [
            {
              "listen": "test",
              "script": {
                "type": "text/javascript",
                "exec": [
                  "pm.test(\"Status code is 201\", function () {",
                  "    pm.response.to.have.status(201);",
                  "});"
                ]
              }
            }
          ],
          "request": {
            "method": "POST",
            "header": [
              { "key": "Content-Type", "value": "application/json" }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"name\": \"Asha\",\n  \"email\": \"asha@example.com\"\n}",
              "options": { "raw": { "language": "json" } }
            },
            "url": {
              "raw": "https://jsonplaceholder.typicode.com/users",
              "protocol": "https",
              "host": ["jsonplaceholder", "typicode", "com"],
              "path": ["users"]
            }
          },
          "response": []
        }
      ]
    }
  ],
  "auth": {
    "type": "bearer",
    "bearer": [{ "key": "token", "value": "{{token}}", "type": "string" }]
  },
  "variable": []
}
```

Reading from the top:

- The whole file is a single JSON object with these main keys: `info`, `item`, `auth`, and `variable`. Postman can also store collection-level `event` entries (scripts) at the same level.
- `info` is the collection's identity. `_postman_id` is a unique identifier generated by Postman. `name` and `description` are what you typed. `schema` is a URL that declares which format version the file follows (here v2.1.0), which tells tools how to read it.
- `item` is an array holding everything inside the collection. An entry that itself contains an `item` array is a **folder** (here `01 - Users`); an entry that has a `request` is a **request**. Sub-folders are simply folders nested inside `item` arrays, and the array order *is* the request order.
- Inside the request entry, `name` is the display name. `event` is an array of scripts. `listen` is either `"test"` (the post-response script) or `"prerequest"`. `script.exec` is an array of strings, one per line of your JavaScript, with quotes escaped as `\"` because JSON strings use double quotes.
- `request` describes the call. `method` is the HTTP verb. `header` is an array of key-value objects. `body.mode` records which Body radio button was selected (`raw`, `formdata`, `urlencoded`, and so on), and `raw` holds the text; the `\n` sequences are line breaks. `options.raw.language` stores the JSON dropdown choice.
- `url` stores the address both as a single string (`raw`) and split into `protocol`, `host` (split at the dots), and `path` (split at the slashes).
- `response` is an array that holds the saved **examples**. It is empty here.
- The top-level `auth` block is the collection-level authorization. Here it states bearer type and a token taken from the variable `{{token}}`. Requests that "inherit auth" read this.
- `variable` holds collection variables.

You rarely edit this by hand, but recognising the structure helps in three situations: reviewing a collection in a merge request (you can see exactly which lines changed), diagnosing an import problem, and understanding what tools read when they run your collection.

**Why export matters for QE.** A JSON file can be committed to Git beside your code, reviewed by colleagues, and tracked over time. A command-line runner called Newman can execute it outside the Postman app. That is outside this week's lessons (on Friday you will run the Python suite in a pipeline instead); for now, note that a collection is portable.

**Security reminder.** An export may contain tokens or passwords typed into authorization or variable fields. Before committing a file to a repository, search it for secrets, and use variables to keep real values out of the collection itself.

### 13. Workspaces, Forking, Sharing, and History

**Sharing.** In a team workspace, everyone with access sees the collection and can run it. Changes by one person are synced to the cloud and visible to others. You can also share a single collection through a link, or export a file as described above.

**Roles.** Teams assign permissions such as viewer (can read and run) and editor (can change). Give people only what they need, particularly for shared collections that run against shared environments.

**Forking.** To **fork** a collection means to make your own linked copy of it. You modify your fork freely without disturbing the original. When your changes are ready, you can open a **pull request** that proposes merging them back, and a reviewer can compare differences and approve. This mirrors the Git workflow you already know from earlier weeks, applied to API collections. You can also **pull** upstream changes into your fork to stay current. Forking is the safe way to experiment in a shared collection.

**Watching and versions.** You can *watch* a collection to be notified of changes, and Postman keeps a version history so you can see who edited what and restore earlier states in supported plans.

**History.** The History tab in the sidebar lists every request you sent in chronological order, grouped by day. Clicking an entry reopens the request exactly as you sent it. History is a safety net for the common moment when you tweaked a request, got a great result, and forgot to save. History is personal and is not a substitute for saving, because it can be cleared and does not appear in shared collections.

### 14. Debugging with the Postman Console

When something does not behave as expected, the **Console** shows what really happened rather than what you assumed. Open it from the bottom-left **Console** button.

It displays:

- Each request as sent: the final URL (after variables were replaced), headers (including auto-generated ones), and body.
- Each response: status, headers, and body.
- Messages from your scripts, produced by `console.log`.
- Script errors, in red, with the line that caused them.

Printing from a script looks like this:

```javascript
const body = pm.response.json();
console.log("Status:", pm.response.code);
console.log("Full body:", body);
console.log("First title:", body.title);
```

Explanation: `console.log(...)` prints each argument to the Console, separated by spaces. The first call prints a label and the status code. The second prints the entire parsed object, which you can expand in the Console to explore its fields. The third prints one field. Logging is how you discover, for example, that `body.data.items` is the real location of the field you were looking for when `body.items` returned `undefined`. (`undefined` is JavaScript's word for "this does not exist".)

A typical debugging routine: (1) the test fails; (2) read the assertion message in Test Results; (3) open the Console to see the exact request that was sent, which often reveals a missing header, a wrongly typed URL, or an unreplaced variable showing as `{{name}}`; (4) add `console.log` lines; (5) fix and re-send. Remove noisy logging when you are finished so shared collections stay clean.

### 15. Best Practices for Collections

1. **One collection per system or API, one folder per resource.** A tidy tree is easier to maintain than a long flat list.
2. **Use a clear, consistent naming convention** (`METHOD - Scenario`) so failed runs are self-explanatory.
3. **Every request has at least one test**, and the status code is the minimum. A request with no tests can never tell you that something broke.
4. **Keep happy-path and negative tests separate**, so you can run them independently and see coverage at a glance.
5. **Make requests independent where you can.** If order is unavoidable, document it and keep dependent requests adjacent.
6. **Use inheritance** for shared authorization and general checks instead of copying them into every request.
7. **Never hard-code secrets or environment-specific URLs.** Use variables and environments (the last lesson today covers them).
8. **Write descriptions** with what, inputs, and expected results.
9. **Clean up the data you create**, with a final folder of deletion requests, so reruns do not collide.
10. **Export and commit** the collection regularly and review it as you would code.
11. **Keep tests focused:** one idea per `pm.test` so a failing name tells you the reason.

### 16. Worked Build: The "Project 2 API" Collection

Now we assemble everything into the Monday milestone. Your instructor will give you the actual Project 2 API base URL and its documentation. The structure below is the blueprint to follow; adjust resource names and fields to match the real API. We assume it manages **users** and **items**, with authentication by bearer token. The base address is written as `{{baseUrl}}`, a variable placeholder; the last lesson today explains how to define it, and until then you may type the full URL.

**Collection:** `Project2-API-Tests`

**Collection settings:**
- *Description:* purpose, how to run, folder order, contact person.
- *Authorization:* Bearer Token, value `{{token}}`, inherited by all folders.
- *Collection post-response script* (runs for every request):

```javascript
pm.test("No server error (status below 500)", function () {
    pm.expect(pm.response.code).to.be.below(500);
});

pm.test("Response time is under 3000 ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(3000);
});
```

This protects every request with two broad safety checks. `below(500)` passes for any success, redirect, or client error, and fails only for server errors, which are never acceptable. The response-time guard is intentionally generous, because it applies to everything.

**Folders and requests:**

*00 - Smoke*
- `GET - Health check` (no auth override if the endpoint is public; set folder auth to No Auth). Tests: status is 200; body has the expected `status` field value.

*01 - Users / Happy path*
- `GET - List users`. Tests: status 200; body is an array; every user has `id`, `name`, `email`; response time under 1000 ms.
- `GET - Get user by ID`. Tests: status 200; `id` equals the requested id; `email` is a string containing "@".
- `POST - Create user with valid data`. Body: raw JSON with name and email. Tests: status 201; response has an `id`; the echoed `name` equals what was sent; `Content-Type` is JSON.
- `PUT - Update user`. Tests: status 200; the changed field has its new value.
- `DELETE - Delete user`. Tests: status 200 or 204.

*01 - Users / Negative*
- `GET - User not found returns 404`. Tests: status 404.
- `POST - Missing required field returns 400`. Body lacks `email`. Tests: status 400; error message exists in the body.
- `GET - List users without token returns 401`. Authorization overridden to No Auth. Tests: status 401.

*02 - Items*
- `GET - List items`, `GET - Get item by ID`, `POST - Create item`, `PUT - Update item`, `DELETE - Delete item`, each with the same style of tests (status, shape, key fields).

*03 - Negative (items)*
- `GET - Item not found returns 404`, `POST - Invalid price type returns 400`.

*99 - Cleanup*
- Deletes any records created earlier, so reruns start clean.

**Finishing steps:** save an example for the success and main error responses of each request; add a description to every folder and request; drag requests into the intended order; run the whole collection with the Collection Runner and fix any failing checks (either the test or, if you have found a real defect, report it); export as Collection v2.1 and keep the JSON in your Project 2 repository.

Notice how the design supports the later work: tomorrow, each request in this collection becomes a Python test function, the folder names become test modules, and the checks you wrote become Python assertions.

### 17. Common Mistakes and Why They Happen

1. **Forgetting to press Save.** The request works, then disappears or reverts. Cause: tabs hold draft changes until saved. Look for the unsaved indicator, or use History to recover.
2. **Choosing raw but leaving it as Text.** The server returns `400` or `415` because the `Content-Type` is `text/plain`. Cause: the dropdown, not the radio button, sets the type. Always select JSON.
3. **Sending a body with GET or leaving a stale body on DELETE.** Many servers ignore or reject it. Cause: the Body tab keeps its content when you change the method. Set Body to none.
4. **Invalid JSON in the body** (trailing commas, single quotes, missing quotes on keys). Cause: JSON is stricter than JavaScript. The editor underlines errors, so look for red marks.
5. **Tests that cannot fail.** For example, asserting only that the response exists, or having no tests at all. Cause: confusing "I looked at it" with "I verified it". Every test should be able to fail for a real reason.
6. **Hard-coding values** such as full URLs, tokens, and ids. Cause: it is quick at first. Result: the collection breaks the moment the environment changes. Use variables.
7. **Asserting on volatile data**, such as exact timestamps, random ids, or array positions. Cause: the value looked constant during one run. Assert on type, format, or presence instead.
8. **Parsing a non-JSON response with `pm.response.json()`.** The script throws "Unexpected token". Cause: an HTML error page or empty body came back. Check the status first and view the Raw body.
9. **Shared tests that do not fit every request** at collection level. Cause: forgetting inheritance applies to all children. Keep shared checks generic.
10. **Order dependence by accident.** A run passes in the designed order but fails when only one request is run. Cause: a later request relies on data created by an earlier one. Document dependencies or make each request create its own data.
11. **Committing secrets.** Tokens and passwords end up in an exported JSON in a repository. Cause: typing real values into the collection. Use variables, and review exports.
12. **Ignoring the Console.** People stare at a failing test without checking what was truly sent. Cause: not knowing it exists. Open it first.
13. **Confusing connection errors with HTTP errors.** "Could not get response" is not a status code. Cause: they both look like failure. Check the URL, network, and server first.

### 18. Practice Exercises with Full Worked Solutions

All exercises use JSONPlaceholder, so they are safe to run. Try each one yourself before reading the solution.

#### Exercise 1: Send and inspect a GET request

*Task:* Send a GET request to `https://jsonplaceholder.typicode.com/users/1`. Record the status, the `name`, the `email`, and the city in the address.

*Solution:* Open a new tab, keep GET, enter the URL, and click Send. The status is `200 OK`. In the Pretty body, `name` is `"Leanne Graham"`, `email` is `"Sincere@april.biz"`, and the address object contains `city` with the value `"Gwenborough"`. The city is nested: you reach it by opening `address` and then reading `city`, which in JavaScript would be written `body.address.city`. Also note the response time and size shown above the body. Reading nested fields is the skill this exercise builds, since real API responses are rarely flat.

#### Exercise 2: Create a collection with folders

*Task:* Create a collection `JSONPlaceholder-Practice` with folders `Posts` and `Users`, and a description in Markdown.

*Solution:* In the sidebar, click **+** next to Collections, choose a blank collection, and name it. On the Overview tab, write:

```markdown
# JSONPlaceholder Practice
Practice collection for **Week 7, Monday**.

- `Posts`: CRUD requests for posts
- `Users`: read-only requests for users
```

Then use the three dots on the collection, choose Add folder twice, and name the folders `Posts` and `Users`. The Markdown renders with a heading, bold text, and a bullet list, confirming the description area accepts formatting.

#### Exercise 3: Add the five CRUD requests with good names

*Task:* In `Posts`, create `GET - List posts`, `GET - Get post by ID`, `POST - Create post`, `PUT - Update post`, and `DELETE - Delete post`.

*Solution:* Use three dots on the `Posts` folder and choose Add request for each. Configure them as follows. List: GET `https://jsonplaceholder.typicode.com/posts`. Get by ID: GET `.../posts/1`. Create: POST `.../posts` with Body raw JSON `{"title":"Practice","body":"Created in Postman","userId":1}`. Update: PUT `.../posts/1` with raw JSON `{"id":1,"title":"Updated","body":"Updated body","userId":1}`. Delete: DELETE `.../posts/1`, Body none. Send each once to confirm it works, and save. The names follow the `METHOD - Purpose` convention, so the folder reads as a table of contents.

#### Exercise 4: Status-code tests on every request

*Task:* Add a status-code test to each request: 200 for GET, PUT, and DELETE; 201 for POST.

*Solution:* Open each request, go to **Scripts**, then **Post-response**, and paste the appropriate code. For GET, PUT, and DELETE:

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

For the POST request, change the number and the name:

```javascript
pm.test("Status code is 201 Created", function () {
    pm.response.to.have.status(201);
});
```

Click Send, open Test Results, and confirm that each shows PASS. The test name should always state the same number that the assertion checks; a mismatch between name and number is a common copy-and-paste error that produces misleading reports.

#### Exercise 5: A body-field and type test

*Task:* On `GET - Get post by ID`, check that `id` is 1, `title` is a non-empty string, and `userId` is a number.

*Solution:*

```javascript
pm.test("Post body has expected id, title and userId", function () {
    const body = pm.response.json();
    pm.expect(body.id).to.eql(1);
    pm.expect(body.title).to.be.a("string").and.not.empty;
    pm.expect(body.userId).to.be.a("number");
});
```

Line by line: `pm.response.json()` converts the JSON text into an object stored in `body`. The first assertion compares `id` to 1. The second chains two checks with `.and`: the value must be a string and must not be empty. The third confirms the type of `userId`. If you wanted a failure to be traceable to one cause, you could split this into three separate tests; combining them is acceptable here because all three describe the same resource.

#### Exercise 6: Test an array and loop over it

*Task:* On `GET - List posts`, check that the response is an array of 100 elements, and that every element has a numeric `id` and a string `title`.

*Solution:*

```javascript
pm.test("List returns an array of 100 posts", function () {
    const posts = pm.response.json();
    pm.expect(posts).to.be.an("array");
    pm.expect(posts).to.have.lengthOf(100);
});

pm.test("Every post has a numeric id and a string title", function () {
    const posts = pm.response.json();
    posts.forEach(function (post) {
        pm.expect(post.id).to.be.a("number");
        pm.expect(post.title).to.be.a("string");
    });
});
```

The first test checks the container; the second checks the contents. `forEach` calls the inner function for each post in turn, so a single bad element anywhere in the list fails the test. The difference between testing "an array exists" and "everything inside it is right" is exactly the kind of depth that distinguishes a useful test from a decorative one.

#### Exercise 7: Header, time, and schema tests

*Task:* On `GET - Get post by ID`, add tests for the JSON content type, a response time under 2000 ms, and a schema.

*Solution:*

```javascript
pm.test("Content-Type is JSON", function () {
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});

pm.test("Response time is under 2000 ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

const postSchema = {
    type: "object",
    required: ["userId", "id", "title", "body"],
    properties: {
        userId: { type: "integer" },
        id: { type: "integer" },
        title: { type: "string" },
        body: { type: "string" }
    }
};

pm.test("Body matches the post schema", function () {
    pm.response.to.have.jsonSchema(postSchema);
});
```

The first test uses `include` because the actual header is `application/json; charset=utf-8`. The second checks the timing against a generous threshold. The third defines the schema as an ordinary constant and then validates the entire body against it in one assertion. To prove the schema test really works, temporarily change `type: "integer"` for `id` to `"string"` and re-send: the test should now fail with a message explaining that `id` should be a string. Always confirm that a test *can* fail.

#### Exercise 8: A negative test

*Task:* Create `GET - Post not found returns 404` in a new folder `Negative`, and test that the status is 404 and the body is an empty object.

*Solution:* Add a folder named `Negative` inside `Posts`, and add a GET request to `https://jsonplaceholder.typicode.com/posts/9999`. In Post-response scripts:

```javascript
pm.test("Status code is 404", function () {
    pm.response.to.have.status(404);
});

pm.test("Body is an empty object", function () {
    const body = pm.response.json();
    pm.expect(Object.keys(body)).to.have.lengthOf(0);
});
```

`Object.keys(body)` returns an array containing the names of all keys on the object. For an empty object, that array has length zero, so the assertion holds. Negative tests confirm that the API refuses or reports invalid situations correctly, which is as important as confirming success.

#### Exercise 9: A collection-level shared test and inheritance

*Task:* Add a collection-level script that checks every response has status below 500, then prove it runs for a request that has no script of its own.

*Solution:* Click the collection name, choose the **Scripts** tab, then **Post-response**, and enter:

```javascript
pm.test("No server error", function () {
    pm.expect(pm.response.code).to.be.below(500);
});
```

Now open a request that contains no script (create `GET - List users` in `Users` with URL `.../users` and no tests), click Send, and open Test Results. You will see "No server error" passing even though that request has no script, because the collection script runs for every child. This demonstrates inheritance: you wrote it once, and it applies everywhere.

#### Exercise 10: Run, read, export, and re-import

*Task:* Run the full collection with 1 iteration and a 200 ms delay, read the results, export it as v2.1, and import it back under a new name.

*Solution:* Open the three-dots menu of the collection and choose **Run collection**. Leave iterations at 1 and set Delay to `200`. Click Run. When it finishes, check the summary: every request should show its status and green tests. Click a request in the results to see the exact request and response. Then use the three dots on the collection, choose **Export**, select **Collection v2.1**, and save the file. Click **Import**, drop the file in, and confirm a second copy of the collection appears with all folders, requests, tests, and descriptions intact. Open the exported file in a text editor and locate the `info`, `item`, and `event` keys to connect what you see in the app to the structure described earlier.

### 19. Self-Check Quiz

Answer each question before reading the answer below it.

**Q1. What is the difference between the Pre-request and Post-response script tabs?**
*Answer:* Pre-request code runs before the request is sent (for preparing data or variables); Post-response code runs after the response arrives, and it is where tests are normally written. In older versions, the second tab is called Tests.

**Q2. You choose Body > raw but leave the language dropdown on Text. The API replies 415 Unsupported Media Type. Why?**
*Answer:* Postman sends `Content-Type: text/plain` instead of `application/json`. The server rejects the format. Choose JSON in the dropdown (or set the header manually).

**Q3. A request inside a collection has Authorization set to "Inherit auth from parent". Where does it get its credentials?**
*Answer:* From the nearest folder or collection above it that defines authorization. If a folder defines it, the folder wins over the collection.

**Q4. In what order do collection, folder, and request scripts run?**
*Answer:* Collection first, then folder, then request, for both pre-request and post-response scripts.

**Q5. What does a `pm.test` do if its function finishes without throwing an error?**
*Answer:* It is reported as passed. A failed assertion throws an error and makes the test fail.

**Q6. Why use `.to.include("application/json")` for a Content-Type check rather than an exact match?**
*Answer:* Servers often append extra text such as `; charset=utf-8`. An exact comparison would fail, but `include` still passes.

**Q7. What is the purpose of Iterations and Delay in the Collection Runner?**
*Answer:* Iterations repeat the whole run a set number of times (often with a data file for different inputs). Delay pauses between requests, helping with rate limits and slow servers.

**Q8. In the exported JSON, how can you tell a folder from a request?**
*Answer:* A folder is an object in `item` that contains its own `item` array. A request is an object that contains a `request` key.

**Q9. Name two reasons to save an example with a request.**
*Answer:* It documents sample data for readers without sending anything, and it preserves evidence (such as a failing response) for bug reports. It can also drive a mock server.

**Q10. Your test shows `AssertionError: expected 404 to equal 200`. Which number is the actual response and which is the expected?**
*Answer:* The first number (404) is the actual value received; the second (200) is what the test expected.

**Q11. Why can a request with no tests never reveal a bug in the response content?**
*Answer:* Because there is nothing to compare the response against. Even a `200` with wrong data would show as a clean run.

**Q12. Is Newman, the command-line runner for collections, taught in this week's lessons?**
*Answer:* No. It is outside this week's lessons; on Friday the pipeline runs the Python test suite instead.

### 20. Glossary

- **API:** an interface that lets programs communicate, usually over HTTP.
- **Assertion:** a statement in a test that must be true (for example "status is 200").
- **Authorization (inherit):** a setting that makes a request use the credentials defined higher in the tree.
- **Body:** the payload sent with a request or returned in a response.
- **Collection:** a saved group of requests with folders, scripts, auth, variables, and documentation.
- **Collection Runner:** the feature that executes a collection's requests in sequence and summarises test results.
- **Collection v2.1:** the JSON format version used to export and import collections.
- **Console:** Postman's log of every request, response, script message, and error.
- **Example:** a saved request-and-response pair attached to a request.
- **Folder:** a container inside a collection that groups requests; folders can be nested.
- **Fork:** a personal linked copy of a collection that can later be merged back via a pull request.
- **History:** a list of recently sent requests.
- **Iteration:** one complete pass through the selected requests in a run.
- **JSON schema:** a document that describes the valid shape and types of a JSON structure.
- **Markdown:** a plain-text formatting syntax used in descriptions.
- **Newman:** Postman's command-line runner (not covered this week).
- **`pm` object:** the built-in JavaScript object providing access to request, response, tests, and variables.
- **Pre-request script:** JavaScript that runs before a request is sent.
- **Post-response script:** JavaScript that runs after a response arrives (formerly "Tests").
- **Query parameters:** key-value pairs after the `?` in a URL.
- **Request:** a single saved API call with method, URL, headers, body, and scripts.
- **Response time:** how long the server took to answer, in milliseconds.
- **Workspace:** a container for collections and environments, either personal, team, or public.

---

## Summary

- Postman is a graphical API platform for exploring, documenting, testing, and sharing requests. QE teams use it for quick exploration and lightweight automation, then build deeper suites in code.
- Install the desktop app, sign in, and work inside a clearly chosen workspace (personal for learning, team for shared work).
- The interface has a sidebar, tabs, a request builder (Params, Authorization, Headers, Body, Scripts, Settings), a response viewer (Body in Pretty, Raw, and Preview; Cookies; Headers; Test Results; status, time, and size), and a Console.
- GET reads, POST creates (expect 201), PUT replaces, and DELETE removes. Choosing raw JSON for the body matters because it sets the right `Content-Type`.
- A collection is a saved binder of requests. Use folders, sub-folders, a `METHOD - Scenario` naming convention, deliberate ordering, and Markdown descriptions.
- Authorization and scripts defined at the collection or folder level are inherited by the requests below; the nearest explicit setting wins, and scripts run collection, then folder, then request.
- Tests are JavaScript using `pm.test`, `pm.expect`, and `pm.response`. Check status, headers, body fields, types, arrays, response time, and optionally a JSON schema. A test passes unless an assertion throws.
- Save examples to document outcomes and keep evidence.
- The Collection Runner repeats requests in order using iterations, delay, and optionally a data file, and shows per-request and per-test results.
- Collections export and import as v2.1 JSON, which can be reviewed and version-controlled; watch for secrets in exports.
- Forking, sharing, and History support collaboration and recovery; the Console is the main debugging tool.
- Follow best practices, avoid the common mistakes, and use the Project 2 blueprint as your Monday milestone. Python automation starts tomorrow, and on Friday a pipeline will run your Python suite automatically.

## Additional Resources

- Postman Docs, *Collections overview*: https://learning.postman.com/docs/collections/collections-overview/
- Postman Docs, *Write scripts to test API response data*: https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-scripts/
- Postman Docs, *Run collections with the Collection Runner*: https://learning.postman.com/docs/collections/running-collections/intro-to-collection-runs/
- Postman Docs, *Postman Collection format (v2.1) reference*: https://schema.postman.com/
- Postman Docs, *Authorization and inheritance*: https://learning.postman.com/docs/sending-requests/authorization/authorization-overview/
