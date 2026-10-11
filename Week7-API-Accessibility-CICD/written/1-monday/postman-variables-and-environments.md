# Postman Variables and Environments

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the hard-coding problem and show, with a before-and-after example, how variables solve it.
- Write the `{{variableName}}` syntax correctly and list every place in a Postman request where it can be used.
- Describe, step by step, what Postman does with a variable between the moment you press **Send** and the moment the request leaves your machine.
- Define all five variable scopes (global, collection, environment, data, local), create each one, see each one, and choose the right one for a given value.
- Predict which value wins when the same name exists in several scopes, and prove it with an experiment.
- Create and switch between Dev, Test, and Staging environments.
- Explain the difference between initial and current values, and describe what is shared with teammates and what stays on your machine.
- Mark values as secret, understand that Postman has a vault, and export an environment without leaking credentials.
- Read, write, check, and delete variables from scripts with `pm.environment`, `pm.collectionVariables`, `pm.globals`, `pm.variables`, and `pm.iterationData`.
- Chain requests by capturing ids and tokens in post-response scripts, and compute values in pre-request scripts.
- Use dynamic variables such as `{{$guid}}` and `{{$randomEmail}}` to generate unique test data.
- Debug variable problems using the eye icon, hover cards, the Postman Console, and `console.log`.
- Build a portable Project 2 API collection that runs unchanged against any environment.

---

## Why This Matters

This week's epic is to grow from clicking around in Postman to building a pipeline-ready Project 2 test automation framework. Look at the week as a ladder. Today you build a Postman collection for the Project 2 API. Tomorrow you rebuild the same checks in Python. On Wednesday you make them data-driven and isolated, and on Friday a GitLab pipeline runs them with no human present. Every rung of that ladder depends on one design idea: **a test must not contain values that belong to a place, a person, or a moment.** The address of the server, the password, the id of the record that was just created, and the email address used in this run are all things that change. If they are written directly into your requests, your tests only work on your laptop, today, for you.

Variables are how Postman separates the **what** of a test (which endpoint, which checks) from the **where and who** (which server, which credentials, which data). A collection written this way can be handed to a teammate, pointed at a different server by changing one dropdown, and run by a machine that has never seen it before. That is exactly what a pipeline-ready framework requires. Employers who hire automation engineers look for this skill in the first five minutes of reviewing a candidate's collection: they open it, look at a URL, and see either `https://dev.api.company.com/users/42` (a throw-away experiment) or `{{baseUrl}}/users/{{userId}}` (a professional asset).

Variables also matter for safety. Test collections routinely contain tokens and passwords. Collections get shared, exported, committed to repositories, and screenshotted into tickets. Understanding exactly which parts of a variable are shared and which stay private is the difference between a safe habit and a security incident.

---

## The Concept

### 1. The hard-coding problem

**Hard-coding** means typing a specific value directly into the place where it is used, instead of storing it once under a name and referring to the name. Here is what a small, real collection looks like when it is hard-coded. Imagine four requests that test a user service.

**Before (hard-coded):**

```
GET    https://dev.api.example.com/api/v1/users/42
        Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.abc123
POST   https://dev.api.example.com/api/v1/users
        Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.abc123
        Body:   {"email": "qa.tester@example.com", "name": "QA Tester"}
PUT    https://dev.api.example.com/api/v1/users/42
        Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.abc123
DELETE https://dev.api.example.com/api/v1/users/42
        Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.abc123
```

This block is not code you would run; it is a picture of four requests as they would appear in the Postman builder. Read it carefully and count the repeated values: the host `dev.api.example.com` appears four times, the version path `/api/v1` four times, the token four times, and the user id `42` three times. Now list what goes wrong.

First, when the team wants the same tests to run against staging, you must edit every URL by hand. With four requests that is annoying; with fifty it is a day of work, and you will miss one, so one request will quietly keep testing dev while you believe you tested staging. That is a worse outcome than a failure, because it produces false confidence.

Second, the token expires. Every request must be edited again, and one stale token produces a baffling `401 Unauthorized` on a single request while the others pass.

Third, the id `42` was the record that existed when you wrote the test. Tomorrow someone deletes it, and every test that mentions it fails for a reason that has nothing to do with the software quality you are testing.

Fourth, the email `qa.tester@example.com` is fixed. The second time the POST runs, the server answers `409 Conflict` because that email is already registered.

Fifth, the token is now embedded in every request. When you export or share the collection, the token travels with it.

**After (using variables):**

```
GET    {{baseUrl}}/users/{{userId}}
POST   {{baseUrl}}/users
        Body: {"email": "{{userEmail}}", "name": "QA Tester"}
PUT    {{baseUrl}}/users/{{userId}}
DELETE {{baseUrl}}/users/{{userId}}
        Auth (set once on the collection): Bearer {{authToken}}
```

Each double-curly-brace name is a placeholder. The host and version path live in one variable, `baseUrl`, whose value is `https://dev.api.example.com/api/v1` in the Dev environment and a different address in Staging. The token lives in one variable, `authToken`, filled in by a login request. The user id is captured from the POST response, so it always refers to a record that really exists. The email is generated fresh each run. The authorization header is configured once, on the collection, instead of four times. Every one of the five problems above disappears, and you did not add any complexity to the requests themselves; you replaced literal values with names. The rest of this lesson explains exactly how that replacement works and how to control it.

### 2. What a variable is, the syntax, and where it can be used

A **variable** is a name that stands for a value. In Postman, you refer to a variable by wrapping its name in two pairs of curly braces: `{{name}}`. The name is case-sensitive, so `baseUrl`, `baseURL`, and `BaseUrl` are three different variables. Names may contain letters, digits, underscores, hyphens, and dots, but you should stick to **camelCase** (`baseUrl`, `authToken`, `createdItemId`) or **snake_case** (`base_url`) and be consistent across the whole team. Avoid spaces; they technically work in some places but break readability and some scripts.

If `baseUrl` holds `https://jsonplaceholder.typicode.com` and `userId` holds `3`, then this text:

```
{{baseUrl}}/users/{{userId}}
```

becomes this when the request is sent:

```
https://jsonplaceholder.typicode.com/users/3
```

The braces and the name vanish; only the stored value remains. The analogy is a mail-merge letter. The template says "Dear `{{firstName}}`", and the word processor swaps in a real first name for each recipient. The template stays the same; the data changes.

Where can you use `{{...}}`? Almost anywhere you can type text into a request:

| Place in the request | Example | Notes |
|---|---|---|
| URL (host, path) | `{{baseUrl}}/orders/{{orderId}}` | The most common use |
| Query parameter value (and key) | `?page={{pageNumber}}` | Edit in the Params table or the URL bar |
| Path variable value | `:id` set to `{{userId}}` in the Path Variables table | Covered in the query parameters lesson |
| Header key or value | `Authorization: Bearer {{authToken}}` | Also works for custom headers like `X-Api-Key` |
| Body: raw JSON, form-data, x-www-form-urlencoded, GraphQL | `{"email": "{{userEmail}}"}` | Mind the quoting rules in section 18 |
| Authorization tab fields | Token box set to `{{authToken}}` | Username, password, API key fields as well |
| Scripts | `pm.variables.replaceIn("{{baseUrl}}/ping")` | In scripts you usually use the `pm` functions instead; see section 11 |
| Collection, folder, and request names/descriptions | Documentation text | Variables in docs resolve when published |

Where do variables **not** resolve by themselves? Inside the JavaScript of a script, a bare `{{baseUrl}}` is not valid code and will not be replaced (the editor would treat it as a broken object literal). In scripts, you read variables with `pm.environment.get("baseUrl")` and friends. This distinction between the text-substitution world (request fields) and the JavaScript world (scripts) trips up almost every beginner, so keep it in mind.

### 3. How Postman resolves variables: what happens before a request is sent

It helps to picture what Postman does when you click **Send**, in order. Knowing the order explains many puzzling behaviours.

1. Postman gathers every variable that is currently available: global, collection, the selected environment, data (if running with a data file), and local.
2. Any **pre-request scripts** run, in this order: collection first, then folder, then request. These scripts can create or change variables.
3. Postman scans every part of the request (URL, params, headers, body, auth) for `{{name}}` patterns.
4. For each name it finds, Postman looks through the scopes from narrowest to widest and takes the first match (the exact order is the precedence list in section 5). The matching text is replaced by the stored value.
5. Dynamic variables beginning with `$` (like `{{$guid}}`) are generated at this moment.
6. If a name matches nothing, it is **left as literal text**. Postman does not stop you. You will see something like `https://{{baseUrl}}/users`, sent as-is, and the server or DNS will fail. This is why red variable names in the editor matter.
7. The finished request is sent over the network.
8. The response arrives, and **post-response scripts (the Tests tab)** run, in the order request, folder, collection. These scripts typically read the response and store values for the next request.

The key insight is the ordering between steps 2 and 3. Because pre-request scripts run *before* substitution, a pre-request script can calculate a value, store it, and have the very same request use it. Conversely, a post-response script runs *after* the request is already sent, so a variable it sets can only affect the **next** request, never the current one. Many beginners write a login test that sets the token in the Tests tab and wonder why the login request itself did not use it. It cannot; the substitution already happened.

### 4. The five scopes

A **scope** defines where a variable lives and where it can be seen. Postman has five. We cover each in the same shape: definition, how to create, how to see, when to use, lifecycle, and an example.

#### 4.1 Global scope

**Definition.** A global variable is visible to every request in every collection in the whole workspace. It is the widest scope.

**How to create.** Open **Environments** in the left sidebar, choose **Globals** at the top, and add a row with a name and value, then **Save**. In a script: `pm.globals.set("name", "value")`.

**How to see.** The **Globals** tab in the sidebar lists them. The eye icon (top right) shows them in a section called Globals. Hovering a `{{name}}` in a request shows the scope as Global.

**When to use.** Rarely. Good uses are throwaway experiments, or a value genuinely shared by unrelated collections in a personal workspace (for example, your own name used in sample bodies). Because every collection can see a global, any collection can also accidentally collide with it. Professional collections avoid globals.

**Lifecycle.** A global persists until you delete it. It survives closing Postman and survives collection runs. If a script changes it, the new value stays.

**Example.** A global `learnerName` = `Alex` used while following tutorials.

#### 4.2 Collection scope

**Definition.** A collection variable is visible only to requests, folders, and scripts inside one collection. It travels with the collection.

**How to create.** Click the collection name, open the **Variables** tab, add a row with name, initial value, and current value, then **Save**. In a script: `pm.collectionVariables.set("name", "value")`.

**How to see.** The **Variables** tab of the collection, or the Collection section in the eye icon quick-look.

**When to use.** For values that stay the same across all environments: the API version segment (`apiVersion = v1`), a default page size, a default timeout, or a placeholder such as `createdItemId` that the collection's own scripts fill in. A collection variable is also an excellent *default* that an environment can override.

**Lifecycle.** Persists with the collection until you change or delete it. Scripts can overwrite it, and the changed value stays as the **current value**. Because it travels with the collection (via the initial value), a teammate who forks or imports the collection receives it.

**Example.** `pageSize` = `20` defined on the Project 2 collection and used as `?limit={{pageSize}}` in every list request.

#### 4.3 Environment scope

**Definition.** An environment variable belongs to a named environment (Dev, Test, Staging) and is visible to any request that runs while that environment is the one selected in the top-right dropdown. Only one environment can be active at a time.

**How to create.** Sidebar, **Environments**, **+** (create environment), name it, add variables, **Save**. In a script: `pm.environment.set("name", "value")`.

**How to see.** Click the environment in the sidebar, or use the eye icon, which shows the Environment section for the active one.

**When to use.** For values that differ by target: `baseUrl`, test-user credentials, tokens, tenant ids, feature-flag settings, timeouts. This is the scope you will use most.

**Lifecycle.** Persists until you change or delete it. If you switch environments, the previous one's variables disappear from view (they are not deleted) and the new one's appear. If **no environment is selected**, environment variables do not exist for the request.

**Example.** `baseUrl` = `https://dev.api.example.com/api/v1` in Dev and `https://staging.api.example.com/api/v1` in Staging.

#### 4.4 Data scope

**Definition.** A data variable comes from a CSV or JSON file you attach when running a collection with the Collection Runner (or from Newman, the command-line runner). Each row of the file is one **iteration**, and the columns of that row become data variables for that iteration only.

**How to create.** You do not type them into Postman. In the Runner, choose **Select File** under Data, upload `users.csv`, and each column header becomes a variable name. Details of file formats and design come on Wednesday ("Data-driven API testing"); here you only need to know the scope exists and where it sits in precedence.

**How to see.** The Runner shows a data preview before the run. In a script, `pm.iterationData.toObject()` prints the current row.

**When to use.** To run the same requests many times with different inputs, such as ten different login attempts.

**Lifecycle.** Exists only for the duration of one iteration of one run. When the run ends, they are gone, and you cannot overwrite them permanently.

**Example.** A CSV with columns `username,password,expectedStatus` produces `{{username}}`, `{{password}}`, and `{{expectedStatus}}` that change with every row.

#### 4.5 Local scope

**Definition.** A local variable exists only while a single request is running (or while a single collection run is executing). It is created in scripts and is not saved anywhere. It is the narrowest scope.

**How to create.** Only from a script: `pm.variables.set("name", "value")`.

**How to see.** It will not show in any table, because it is not stored. Use `console.log(pm.variables.get("name"))` or the eye icon during a run to observe it.

**When to use.** For temporary calculated values that should never leak into an environment or collection: a timestamp used for one request, a signature computed from the body, an intermediate number. Because it is local, it cannot pollute anything.

**Lifecycle.** Created when the script runs, gone when the request (or run) ends. It does not persist between separate manual sends.

**Example.** A pre-request script computes `requestTime` and the header `X-Request-Time: {{requestTime}}` uses it for this one send.

A quick summary table:

| Scope | Created by | Stored? | Lives as long as | Best for |
|---|---|---|---|---|
| Global | Globals tab or `pm.globals.set` | Yes | Until deleted | Experiments only |
| Collection | Collection Variables tab or `pm.collectionVariables.set` | Yes | Until deleted | Constants shared across environments, defaults |
| Environment | Environment tab or `pm.environment.set` | Yes | Until deleted | Per-target values, tokens, credentials |
| Data | Data file in Runner | No (file) | One iteration | Many inputs through the same requests |
| Local | `pm.variables.set` | No | One request or run | Temporary calculations |

### 5. Precedence: which value wins, and a worked experiment

Postman allows the same name to exist in several scopes at once. When a request uses `{{team}}`, Postman must pick one. The rule is that the **narrowest scope wins**:

```
Local  >  Data  >  Environment  >  Collection  >  Global
(highest priority)                              (lowest priority)
```

This is a deliberate design. Wide scopes provide defaults and narrow scopes provide overrides. A collection might say `timeoutMs = 3000`; the Staging environment says `timeoutMs = 1000`; a data row might say `timeoutMs = 50`; and a script might override everything for one call. Each narrower scope wins over the wider one.

Reading a rule is one thing; seeing it happen locks it in. Here is an experiment you can run in ten minutes. It uses `postman-echo.com`, a free public service run by Postman that simply echoes back whatever you send.

**Setup.** Create a new collection named `Scope Lab`. Create an environment named `Lab Env`, and select it. Create the same variable name, `team`, in four places:

| Scope | Where you create it | Value |
|---|---|---|
| Global | Globals tab | `global-value` |
| Collection | Scope Lab, Variables tab | `collection-value` |
| Environment | Lab Env | `environment-value` |
| Local | (script, later) | `local-value` |

Remember to click **Save** on each. Add a request to the collection named `Echo team`:

```
GET https://postman-echo.com/get?team={{team}}
```

Give the request this **Tests** (post-response) script:

```javascript
console.log("pm.variables.get       :", pm.variables.get("team"));
console.log("pm.environment.get     :", pm.environment.get("team"));
console.log("pm.collectionVariables :", pm.collectionVariables.get("team"));
console.log("pm.globals.get         :", pm.globals.get("team"));
```

Explanation of the script, line by line. `console.log(...)` prints values to the Postman Console, which is the debugging window described in section 17. Each line has two arguments separated by a comma: a text label so you can tell the lines apart, and a value. The first call, `pm.variables.get("team")`, asks Postman to resolve `team` using the full precedence rule, so it tells you what the request actually used. The next three calls look only into one specific scope, and so tell you what that individual scope holds. Printing all four side by side makes the difference between "what each scope holds" and "what wins" visible.

**Run 1: global, collection, and environment defined.** Open the Console (View menu, Show Postman Console, or the keyboard shortcut Ctrl+Alt+C on Windows and Linux, Cmd+Option+C on Mac), then click Send. The response JSON from postman-echo will contain `"args": { "team": "environment-value" }`. The console prints `environment-value` for `pm.variables.get`, and the three scope-specific lines print their own values. **Result: environment wins.**

**Run 2: delete the environment variable.** In Lab Env remove the `team` row and Save. Send again. The echo now shows `collection-value`. The `pm.environment.get` line prints `undefined`. **Result: collection wins over global.**

**Run 3: delete the collection variable.** Send again. The echo shows `global-value`. **Result: with nothing narrower, the global is used.**

**Run 4: put the variables back, then add a local override.** Restore `team` in the environment and collection. Add this **Pre-request Script** to the `Echo team` request:

```javascript
pm.variables.set("team", "local-value");
```

This single line creates a local variable named `team`. The string on the left is the name, and the string on the right is the value. Send again. The echo shows `local-value`, and the console shows `pm.variables.get` giving `local-value` while `pm.environment.get` still gives `environment-value`. **Result: local beats environment, collection, and global, and it did not change any of them.** After the request finishes, open Lab Env: the `team` value is unchanged, because the local variable was never saved.

**Run 5: data scope.** Remove the pre-request script. Create a file `team.csv` containing two lines:

```
team
data-value
```

Open the collection's **Run** option (the Collection Runner), select only `Echo team`, upload `team.csv` as the data file, and run. The echo shows `data-value`, even though environment, collection, and global all still define `team`. **Result: data beats environment.** With the pre-request script restored, local would beat data too, completing the full ladder.

The summary of the experiment:

| What was defined | What the request resolved |
|---|---|
| Global, collection, environment | `environment-value` |
| Global, collection | `collection-value` |
| Global only | `global-value` |
| Global, collection, environment, local | `local-value` |
| Global, collection, environment, data (run with CSV) | `data-value` |
| Global, collection, environment, data, local | `local-value` |

A second lesson hides in this experiment. `pm.variables.get` follows precedence, while `pm.environment.get` reads only the environment. If a bug exists where "the request uses the wrong value," always print `pm.variables.get` first, because it tells you what Postman actually resolved.

### 6. Creating and switching environments, step by step

An **environment** is a named set of variables that represents a place your tests run. The most common set in industry is Local (your own machine), Dev (shared development server), Test or QA (stable testing server), and Staging (a near copy of production). Here is how to build three of them.

1. In the left sidebar, click **Environments**.
2. Click the **+** (Create Environment) button. A new tab opens with a default name such as "New Environment".
3. Rename it by clicking the name: type `Project2 - Dev`. A clear prefix with the project name helps when you own many environments.
4. In the table, type `baseUrl` in the **Variable** column. In the **Initial value** and **Current value** columns, type `https://dev.api.example.com/api/v1`. (Initial versus current is the next section.)
5. Add a second row: `username` = `qa_dev_user`. Add a third: `password` with type set to **secret** (section 8), and value `dev-password-placeholder`. Add a fourth: `authToken` with empty values. It will be filled by the login request.
6. Click **Save** (Ctrl+S). Unsaved environments show a dot on the tab.
7. Create the next one quickly by using the **three dots** menu beside your environment, choosing **Duplicate**, renaming the copy to `Project2 - Test`, and editing only the values that differ (`baseUrl`, `username`, `password`).
8. Duplicate once more for `Project2 - Staging`.
9. Use the **environment dropdown** in the top-right corner of the Postman window (it initially says "No Environment"). Pick `Project2 - Dev`. The name shows in the dropdown, and the eye icon beside it now lists Dev's variables.
10. To switch, simply pick a different environment from the same dropdown. The requests do not change; only the values substituted into them do.

Here is how the three might differ:

| Variable | Dev | Test | Staging |
|---|---|---|---|
| `baseUrl` | `https://dev.api.example.com/api/v1` | `https://test.api.example.com/api/v1` | `https://staging.api.example.com/api/v1` |
| `username` | `qa_dev_user` | `qa_test_user` | `qa_stg_user` |
| `password` | (secret) | (secret) | (secret) |
| `timeoutMs` | `3000` | `2000` | `1000` |
| `authToken` | (set by login) | (set by login) | (set by login) |

Keep the **same variable names** across all environments. The entire trick depends on the requests using `{{baseUrl}}` and every environment providing a `baseUrl`. If Staging calls it `base_url` instead, requests will show a red variable when you switch to it.

Two safety practices. First, never point an automation suite that creates and deletes data at production. Use sandbox or test environments, and give production (if you ever include it) a name like `PROD - READ ONLY` to make the danger obvious. Second, glance at the dropdown before you send anything destructive. A DELETE sent while the wrong environment is selected is a classic, painful mistake.

### 7. Initial value versus current value, in depth

Every variable in a global, collection, or environment table has **two** value columns. This design confuses beginners, but it exists for a good reason: it allows a team to share a collection's *structure* without sharing everyone's *secrets*.

| Column | Where it is stored | Synced to the Postman cloud and teammates? | Included when you export? |
|---|---|---|---|
| **Initial value** | Postman cloud, once you are signed in and the workspace is shared | Yes | Yes |
| **Current value** | Only on your local Postman app | No | See the export warning in section 19 |

When Postman sends a request, it uses the **current value**. If the current value is empty, it falls back to the initial value. When you type a value into the table, the two start identical, but you can edit them independently.

**A sync and sharing scenario.** Priya and Marcus both work in a shared team workspace on the Project 2 collection and the `Project2 - Dev` environment. Priya creates the `password` variable. She types `Pa55-real!` into **both** columns by mistake, and saves. Postman syncs the initial value to the cloud. Marcus opens the workspace and sees `Pa55-real!` in his Initial value column. Every teammate, every future member of the workspace, and any forked copy of the collection now has a real password. That is a leak.

Now watch the right way. Priya types the placeholder `<set-your-own>` into **Initial value** and her real password into **Current value**. She saves. The cloud only receives `<set-your-own>`. Marcus sees the placeholder, and types his own test-user password into **his** Current value. His Postman stores it locally. Each person's requests send their own password; no password was shared. Marcus's collection run works, Priya's works, and nothing sensitive is stored in the cloud.

Further consequences worth remembering:

- A script that calls `pm.environment.set("authToken", "...")` changes the **current** value only, which is desirable: a freshly obtained token must never be synced to teammates.
- When a teammate says "it works on my machine," compare current values. They may have a stale token or have forgotten to fill in their credentials.
- If you reset a current value to the initial value (Postman offers a "Reset all" option in the quick-look), you lose whatever your scripts captured. Do this deliberately.
- Run results in CI (Friday) have no personal Postman app at all, so initial values (or injected values) are all the runner sees. We will meet that case on Friday.

### 8. Secret-type variables and the vault (awareness)

In the variable table, each row has a **Type** column that defaults to **default** and can be changed to **secret**. A secret variable behaves exactly like any other variable when requests are sent, but its value is **masked** with dots on screen, with a show/hide toggle. This protects you from shoulder-surfing, screen sharing during a demo, and accidental screenshots. Use the secret type for passwords, API keys, tokens, and client secrets.

Be honest about what the secret type is and is not. It is a **display protection** and a reminder. It does not by itself stop the initial value from syncing. The real protection comes from the habit in section 7: placeholders in initial value, real value in current value, type set to secret. Do both.

Postman also offers a **vault**: a local, encrypted storage area in the Postman desktop app for sensitive values such as API keys. Vault secrets are referenced with a special syntax like `{{vault:my-secret-name}}`, never synced to the cloud, and available across workspaces on your machine. You do not need the vault for this course, but you should know it exists, because it is the stronger option for long-lived credentials and because many companies mandate it. The Postman documentation linked at the end of the lesson describes setup.

### 9. Using variables in each part of a request

Here is each place with a realistic example. We assume the Project 2 environment above.

**URL.** `{{baseUrl}}/items/{{itemId}}` resolves to `https://dev.api.example.com/api/v1/items/17`. Note that the variable `baseUrl` already contains `https://`, so you do not type it again. Typing `https://{{baseUrl}}` produces `https://https://...`, which is one of the most common mistakes.

**Query parameters.** In the Params tab, key `limit`, value `{{pageSize}}`. The URL bar shows `?limit={{pageSize}}`. You can also use a variable for the key, though that is rare.

**Headers.** Key `X-Tenant-Id`, value `{{tenantId}}`. Key `Authorization`, value `Bearer {{authToken}}`. The word `Bearer` and the space are literal text; only the token is a variable.

**Body.** Select **Body**, **raw**, **JSON**:

```json
{
  "name": "{{itemName}}",
  "quantity": {{quantity}},
  "ownerEmail": "{{userEmail}}"
}
```

Look at the quoting. `name` and `ownerEmail` are strings, so their variables are inside quotation marks. `quantity` is a number, so its variable is **not** quoted; after substitution the JSON reads `"quantity": 5`. Section 18 explains this rule fully.

**Authorization tab.** Choose type **Bearer Token** and type `{{authToken}}` into the Token box. Postman adds the header for you when sending. Section 16 shows how to set this once for the entire collection.

**Scripts.** Scripts do not substitute text. They call functions, covered next.

### 10. A beginner's guide to the JavaScript used in Postman scripts

Postman scripts are written in **JavaScript**. If you have not written JavaScript before, here are the six pieces of syntax you need. Everything else in this lesson uses only these.

```javascript
// This is a comment: Postman ignores everything after the two slashes.

const name = "Alex";            // const creates a named value that cannot be reassigned
let count = 1;                  // let creates a named value that can change later
count = count + 1;              // now count is 2

const user = { id: 7, email: "a@b.com" };   // an object: named fields in curly braces
console.log(user.id);                       // dot notation reads a field: prints 7

const text = '{"id": 7}';                   // a string that looks like JSON
const parsed = JSON.parse(text);            // JSON.parse converts JSON text into an object
console.log(parsed.id);                     // prints 7

function double(n) { return n * 2; }        // a function: reusable named steps
const triple = (n) => n * 3;                // an arrow function: shorter way to write one
console.log(double(4), triple(4));          // prints 8 12
```

Line by line. The first line is a comment. `const name = "Alex";` declares a variable called `name` that holds text; the semicolon ends the statement. `const` means the name cannot later be pointed at something else, and it is the safest default. `let count = 1;` declares a changeable variable, and the next line reassigns it. The object `user` bundles related values under field names; `user.id` reads one field. `JSON.parse(text)` is essential for API work: a response body arrives as text, and parsing it produces an object whose fields you can read. The `function double(n)` line defines a function, which takes an input `n` and `return`s a result. The arrow function `(n) => n * 3` does the same job in a compact form; you will see arrow functions inside `pm.test`. Finally, `console.log` prints any number of values separated by commas.

Note that JavaScript variables (`const x`) are different from Postman variables (`{{x}}`). A JavaScript `const` exists only during that script run, like a scratch pad. A Postman variable is stored in a scope. You move values between the two worlds with `pm.environment.set(...)` and `pm.environment.get(...)`.

### 11. The `pm` variable functions in detail

Postman gives every script an object called `pm`. Its variable helpers are grouped by scope.

| Object | Scope it touches | Notes |
|---|---|---|
| `pm.globals` | Global | Wide and risky; avoid |
| `pm.collectionVariables` | Collection | Good for defaults and collection-specific state |
| `pm.environment` | Environment | Most used; also has `pm.environment.name` |
| `pm.variables` | Reads all scopes by precedence; writes to **local** | The "what will actually be used" view |
| `pm.iterationData` | Data (current row) | Read-only in practice |

The common methods on these objects are `get`, `set`, `unset`, `has`, and `toObject`. Here they all appear together, using the environment object:

```javascript
// SET: store a value under a name
pm.environment.set("itemId", 17);

// GET: read a value; returns undefined if the name does not exist
const id = pm.environment.get("itemId");
console.log("id is", id);

// HAS: ask whether a name exists; returns true or false
if (pm.environment.has("authToken")) {
    console.log("a token is stored");
} else {
    console.log("no token stored yet");
}

// TOOBJECT: get all variables of this scope as a plain object
const all = pm.environment.toObject();
console.log(all);

// UNSET: remove one variable
pm.environment.unset("itemId");

// CLEAR: remove all variables in this scope (use with care)
// pm.environment.clear();
```

Explanation line by line. `pm.environment.set("itemId", 17)` creates (or overwrites) an environment variable named `itemId`. The first argument is the name as a string; the second is the value. Postman stores variable values as text, so `17` is stored as `"17"` and comes back as the string `"17"`, not the number. That is fine when substituting into URLs, but it matters when you compare: `pm.expect(id).to.eql("17")` compares text. `pm.environment.get("itemId")` returns the stored value, or `undefined` if the name is not there. The line `const id = ...` saves the answer in a JavaScript constant so the script can reuse it. `pm.environment.has("authToken")` returns `true` or `false`. It is the safe way to test existence, and it is used inside an `if (...) { ... } else { ... }` statement: the first block runs when the answer is true, the second otherwise. `pm.environment.toObject()` returns every variable of the scope as one JavaScript object such as `{ baseUrl: "...", itemId: "17" }`, which is useful for a quick dump while debugging. `pm.environment.unset("itemId")` deletes that one variable, a good cleanup step at the end of a chain. `clear()` deletes everything in the scope; it is commented out with `//` here because it is dangerous, and you should almost never call it.

Setting objects or arrays: because values are stored as text, wrap them in `JSON.stringify` when saving and `JSON.parse` when reading.

```javascript
pm.collectionVariables.set("ids", JSON.stringify([1, 2, 3]));
const ids = JSON.parse(pm.collectionVariables.get("ids"));
console.log(ids.length);   // 3
```

The first line converts the array into the text `[1,2,3]` before storing it. The second reads that text and converts it back into a real array so you can use `.length` or loop over it.

The same methods exist on the other objects with these notes:

```javascript
// Collection scope
pm.collectionVariables.set("apiVersion", "v1");
console.log(pm.collectionVariables.get("apiVersion"));

// Global scope
pm.globals.set("learnerName", "Alex");
console.log(pm.globals.has("learnerName"));       // true

// Precedence-aware reading, and local writing
pm.variables.set("requestTime", Date.now());      // creates a LOCAL variable
console.log(pm.variables.get("requestTime"));     // reads whichever scope wins
console.log(pm.variables.has("baseUrl"));         // true if defined anywhere
console.log(pm.variables.toObject());             // every visible variable, merged
console.log(pm.variables.replaceIn("{{baseUrl}}/ping"));   // substitute inside a string

// Data scope: the current row of the data file (empty when no file is used)
console.log(pm.iterationData.get("username"));
console.log(pm.iterationData.has("username"));
console.log(pm.iterationData.toObject());
```

Walk through the notable lines. `pm.variables.set(...)` writes a **local** variable, as proven in the experiment. `pm.variables.get(...)` reads using precedence, so it is the most reliable "what will the request see" check. `pm.variables.toObject()` returns the merged view of everything visible. `pm.variables.replaceIn("{{baseUrl}}/ping")` takes a string that contains `{{...}}` markers and returns it with values substituted, including dynamic variables like `{{$guid}}`; this is the way to use the `{{ }}` syntax from inside a script. The `pm.iterationData` lines read the current data row; they return `undefined` or an empty object when you ran the request manually without a data file. `pm.iterationData` also offers `unset`, but you normally treat it as read-only, and you use `pm.variables.set` for anything you need to change in a script. Wednesday's lesson returns to it.

**Which scope should a script write to?** Use `pm.environment.set` for values that belong to the target (tokens, ids tied to that server's data). Use `pm.collectionVariables.set` for values tied to the collection and independent of environment (for example a counter). Use `pm.variables.set` for temporary calculations. Avoid `pm.globals.set`. A frequent bug: you `set` in one scope and `get` from another, so the value appears missing. Choose one scope for each variable and use the same object for writing and reading.

An important operational note: `pm.environment.set` needs an environment to write into. If no environment is selected, the write will not be saved and later requests will not see the value. If chains mysteriously fail from the very first run, check that the dropdown is not on "No Environment".

### 12. Post-response scripts: capturing ids and tokens to chain requests

APIs rarely work in isolation. You create a resource, the server returns its new id, and the next requests need that id. A **post-response script** (the **Tests** tab in older versions, or **Post-response** in the newest versions) runs after the response arrives. It can read the response, store pieces in variables, and make assertions. A **chain** is a sequence of requests where each uses values captured by earlier ones.

The response helpers you need are these:

| Expression | Meaning |
|---|---|
| `pm.response.json()` | The response body parsed into a JavaScript object (fails if the body is not valid JSON) |
| `pm.response.text()` | The raw body text |
| `pm.response.code` | The numeric status code, e.g. `201` |
| `pm.response.headers.get("Location")` | One response header's value |
| `pm.test("name", function () { ... })` | A named check; shows pass or fail in the Test Results tab |
| `pm.expect(value).to...` | An assertion inside a test |

#### Full worked build: a CRUD chain for the Project 2 API

For this walkthrough we assume the Project 2 API has the following shape. This is the pattern; adjust the paths and field names to the real API you are given.

| Operation | Request | Success response |
|---|---|---|
| Login | `POST /auth/login` with `{"username": "...", "password": "..."}` | `200` and `{"token": "abc..."}` |
| Create | `POST /items` with `{"name": "...", "quantity": 5}` | `201` and `{"id": 17, "name": "...", "quantity": 5}` |
| Read | `GET /items/17` | `200` and the item |
| Update | `PUT /items/17` with the full item | `200` and the updated item |
| Delete | `DELETE /items/17` | `200` or `204` |
| Verify deleted | `GET /items/17` | `404` |

Start with the environment `Project2 - Dev` created in section 6 containing `baseUrl`, `username`, `password`, and an empty `authToken`. Create a collection named `Project 2 API` and a request in it for each row above. We will fill each in order.

**Request 1: Login.** Method POST, URL `{{baseUrl}}/auth/login`. Body (raw, JSON):

```json
{
  "username": "{{username}}",
  "password": "{{password}}"
}
```

The credentials come from the environment, so no password sits inside the request. In the **Post-response** (Tests) tab add:

```javascript
pm.test("Login returns 200", function () {
    pm.response.to.have.status(200);
});

const body = pm.response.json();
pm.environment.set("authToken", body.token);

pm.test("Token captured", function () {
    pm.expect(pm.environment.get("authToken")).to.be.a("string").and.not.empty;
});
```

Explanation. The first `pm.test` block passes only if the status is 200. `pm.test` takes a name and a function; inside, `pm.response.to.have.status(200)` is the assertion. `const body = pm.response.json();` parses the response text into an object called `body`. If the server returned `{"token": "abc123"}`, then `body.token` is `"abc123"`. `pm.environment.set("authToken", body.token);` stores it, so every later request that uses `{{authToken}}` now has a valid token. The last test confirms the capture worked: `.to.be.a("string")` checks the type and `.and.not.empty` checks it is not an empty string. If your API names the field `access_token` or nests it as `data.token`, change `body.token` accordingly; reading the real response body first is always step one.

**Collection-level authorization (do this now, once).** Click the collection, open **Authorization**, set type **Bearer Token**, and enter `{{authToken}}`. Every request in the collection whose own Authorization tab says **Inherit auth from parent** will now send the header automatically. Set the Login request's Authorization to **No Auth**, since it is how you obtain the token. Section 16 expands on this.

**Request 2: Create item.** POST `{{baseUrl}}/items`. In the **Pre-request Script** tab, generate a unique name:

```javascript
const unique = "item-" + Date.now();
pm.variables.set("itemName", unique);
```

`Date.now()` returns the number of milliseconds since the start of 1970, which differs on every run. The `+` joins text and number into one string such as `item-1760184000123`. `pm.variables.set` stores it as a local variable available to this request's body, since pre-request scripts run before substitution. Body:

```json
{
  "name": "{{itemName}}",
  "quantity": 5
}
```

Post-response script:

```javascript
pm.test("Create returns 201", function () {
    pm.response.to.have.status(201);
});

const created = pm.response.json();
pm.environment.set("itemId", created.id);
pm.environment.set("itemName", created.name);

pm.test("Response echoes the name we sent", function () {
    pm.expect(created.name).to.eql(pm.variables.get("itemName"));
});
```

Explanation. The status check is the same pattern as before. `created` holds the parsed body. We store the server-assigned `id` as `itemId`, which the rest of the chain needs; the server, not us, decides the id, which is exactly why we must capture it. We also store the name in the environment. Note the subtle order: after `pm.environment.set("itemName", ...)` there are now both a local and an environment `itemName`; the local one has precedence during this request and disappears afterward, and the environment copy remains for later requests. The final test compares what the server echoed against the value we sent. `eql` means deep equality. Here it passes because both are the same string.

**Request 3: Read item.** GET `{{baseUrl}}/items/{{itemId}}`. Post-response:

```javascript
pm.test("Read returns 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Read returns the item we created", function () {
    const item = pm.response.json();
    pm.expect(item.id).to.eql(Number(pm.environment.get("itemId")));
    pm.expect(item.name).to.eql(pm.environment.get("itemName"));
});
```

Explanation. `item.id` from JSON is a number, but environment values are text. `Number(...)` converts the text `"17"` back to the number `17` so `eql` compares like with like. Forgetting this conversion produces an assertion error that reads like `expected 17 to deeply equal '17'`, a classic confusion.

**Request 4: Update item.** PUT `{{baseUrl}}/items/{{itemId}}` with body:

```json
{
  "name": "{{itemName}}-updated",
  "quantity": 10
}
```

Post-response:

```javascript
pm.test("Update returns 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Quantity was updated", function () {
    pm.expect(pm.response.json().quantity).to.eql(10);
});
```

Here `pm.response.json().quantity` chains the parse and field access in one expression, a compact style you will see often.

**Request 5: Delete item.** DELETE `{{baseUrl}}/items/{{itemId}}`. Post-response:

```javascript
pm.test("Delete succeeds", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 204]);
});
```

`oneOf([200, 204])` passes if the code is either value, since APIs differ in what a successful delete returns. Confirm which one your API uses and tighten the test accordingly.

**Request 6: Verify deleted.** GET `{{baseUrl}}/items/{{itemId}}` again. Post-response:

```javascript
pm.test("Item no longer exists (404)", function () {
    pm.response.to.have.status(404);
});

// Clean up chain state so the next run starts fresh
pm.environment.unset("itemId");
pm.environment.unset("itemName");
```

This test passes when the item is gone. The two `unset` lines delete the chain's variables, so a later run cannot accidentally reuse a stale id. Note that the request used `{{itemId}}` *before* the script unset it, because substitution happens before the response scripts run.

**Run it.** Order the requests as listed (drag them in the sidebar), select the **Project 2 API** collection, click **Run**, confirm the environment is `Project2 - Dev`, and run. All six requests should execute in sequence. The Runner's results show each request with its tests. You have just built a fully automated CRUD lifecycle with no hard-coded host, credentials, or ids.

A caution about public sandbox APIs. If you rehearse this chain against JSONPlaceholder (`https://jsonplaceholder.typicode.com`), remember that it *pretends* to save: a POST to `/posts` returns the id `101`, but a later GET of `/posts/101` returns `404` because nothing was stored. The capture and substitution mechanics still work exactly as shown, but the "read what I created" step will fail on that site. That is a property of the sandbox, not a bug in your script.

### 13. Pre-request scripts: computing values before sending

A **pre-request script** runs before the variables are substituted, so it is the correct place to calculate anything the request needs. Three common patterns follow.

**A timestamp and a unique email.**

```javascript
const stamp = Date.now();
pm.variables.set("requestTime", new Date().toISOString());
pm.variables.set("userEmail", "qa+" + stamp + "@example.com");
```

`Date.now()` gives a number of milliseconds. `new Date().toISOString()` creates a date object for right now and formats it as text like `2026-10-11T09:30:00.000Z`, a widely used timestamp format. Both go into local variables, so they exist only for this request. The email combines a fixed prefix, the number, and a domain. The `+` signs inside the quotation marks mean "join the pieces". Because the number changes every millisecond, the address is unique, preventing "email already exists" collisions.

**A base64 string.** Some APIs want `username:password` base64-encoded (HTTP Basic authentication).

```javascript
const raw = pm.environment.get("username") + ":" + pm.environment.get("password");
const encoded = CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(raw));
pm.variables.set("basicToken", encoded);
```

Explanation. We build the combined text, then use **CryptoJS**, a cryptography library that Postman includes in its script sandbox, so you do not need to import anything. `CryptoJS.enc.Utf8.parse(raw)` turns the text into CryptoJS's internal byte format, and `CryptoJS.enc.Base64.stringify(...)` turns that into base64 text. We store the result so the header `Authorization: Basic {{basicToken}}` can use it. (Postman's Basic Auth type does this for you automatically; the manual way is shown so you understand what happens.)

**A hash (awareness level).** Some APIs require a signature, such as a SHA-256 hash of the body plus a secret.

```javascript
const payload = pm.request.body.raw;
const secret = pm.environment.get("signingSecret");
const signature = CryptoJS.HmacSHA256(payload, secret).toString();
pm.variables.set("signature", signature);
```

`pm.request.body.raw` reads the body text that is about to be sent. `CryptoJS.HmacSHA256(payload, secret)` computes a keyed hash, and `.toString()` converts it to a hexadecimal string. The header `X-Signature: {{signature}}` then carries it. You will not need this for the Project 2 API unless the API specification says so; the point is to know that Postman scripts can compute such values, so you never have to give up and hard-code them.

### 14. Dynamic variables

**Dynamic variables** are built-in generators. You write them like other variables but with a leading `$`, and Postman produces a fresh value every time the request is sent. You cannot edit, store, or see them in any table; they just work.

| Dynamic variable | Produces | Example output |
|---|---|---|
| `{{$guid}}` | A UUID | `a3f1c1e2-5b0a-4c53-9a3a-2f6d3a1b9c11` |
| `{{$randomUUID}}` | Another UUID generator | similar |
| `{{$timestamp}}` | Current Unix time in seconds | `1760184000` |
| `{{$isoTimestamp}}` | Current time, ISO format | `2026-10-11T09:30:00.000Z` |
| `{{$randomInt}}` | Integer from 0 to 1000 | `482` |
| `{{$randomEmail}}` | A fake email address | `Kaitlyn_Ritchie@example.net` |
| `{{$randomFirstName}}` | A first name | `Maria` |
| `{{$randomLastName}}` | A last name | `Okafor` |
| `{{$randomFullName}}` | A full name | `Maria Okafor` |
| `{{$randomCity}}` | A city | `Lake Meadow` |
| `{{$randomPhoneNumber}}` | A phone number | `912-555-0187` |
| `{{$randomBoolean}}` | `true` or `false` | `true` |
| `{{$randomPassword}}` | A random password string | `n3Xt_P4ss` |

The exact outputs differ every time, and the full list is in Postman's documentation (linked below).

A body that uses several of them:

```json
{
  "name": "{{$randomFullName}}",
  "email": "{{$randomEmail}}",
  "externalRef": "{{$guid}}",
  "age": {{$randomInt}}
}
```

Each of the four placeholders is replaced independently, so the name and email will not belong to the same fake person; they are separate random draws. The `age` placeholder has no quotes because it produces a number (and a random integer up to 1000 may not be a sensible age; validate against your API's rules or compute your own with a script).

Three important behaviours. First, each **occurrence** of a dynamic variable generates a new value, so using `{{$guid}}` twice in one request produces two different ids. If you need the same generated value in two places, create it in a pre-request script (`pm.variables.set("ref", pm.variables.replaceIn("{{$guid}}"))`) and use `{{ref}}` in both places. Second, in scripts you reach dynamic variables through `pm.variables.replaceIn("{{$randomEmail}}")`, since `{{$...}}` is not valid JavaScript by itself. Third, random data is a double-edged tool. It prevents collisions, but a failing test may be hard to reproduce, because the data that caused the failure is gone. Good practice is to log the generated values with `console.log` or store them in a variable so you can see them in the Console afterwards.

### 15. `pm.sendRequest` and the login-token flow (awareness)

Normally one request sends one HTTP message. `pm.sendRequest` lets a **script** send an additional request. This is useful when a collection should fetch a token automatically before any request, without requiring you to run the Login request manually. Here is the pattern, which you may place in the **collection-level** Pre-request script:

```javascript
const hasToken = pm.environment.get("authToken");

if (!hasToken) {
    pm.sendRequest({
        url: pm.environment.get("baseUrl") + "/auth/login",
        method: "POST",
        header: { "Content-Type": "application/json" },
        body: {
            mode: "raw",
            raw: JSON.stringify({
                username: pm.environment.get("username"),
                password: pm.environment.get("password")
            })
        }
    }, function (err, res) {
        if (err) {
            console.log("Login failed:", err);
        } else {
            pm.environment.set("authToken", res.json().token);
        }
    });
}
```

Explanation. The first line reads the current token. `if (!hasToken)` means "if there is no token (undefined or empty)", where `!` means "not". Inside, `pm.sendRequest(options, callback)` takes two arguments. The first is an object describing the request: `url`, `method`, a `header` object, and a `body` object where `mode: "raw"` and `raw` hold the JSON text. `JSON.stringify` converts a JavaScript object into JSON text, the reverse of `JSON.parse`. The second argument is a **callback function** that Postman calls when the response comes back. It receives `err` (set if the network call failed) and `res` (the response). If there is no error, `res.json().token` extracts the token and stores it in the environment. This is awareness-level material: it works, but it hides a request inside a script where it is harder to see and debug, and it does not handle token expiry. For the exercises today, a visible Login request at the start of the collection is clearer. Tomorrow you will build the same "log in once, reuse the token" flow in Python with fixtures.

### 16. Collection-level authorization inheriting a token variable

Pasting a token into every request is the hard-coding problem again. Postman's **authorization inheritance** solves it. Auth can be set at three levels: collection, folder, and request. A request whose Authorization type is **Inherit auth from parent** uses the closest parent that defines auth.

To set it up:

1. Click the collection name in the sidebar and open the **Authorization** tab.
2. Choose **Bearer Token** from the Type dropdown.
3. In the **Token** box type `{{authToken}}`. Postman adds the header `Authorization: Bearer <value>` at send time.
4. Save the collection.
5. For each request, make sure its Authorization type is **Inherit auth from parent** (the default for new requests).
6. For public endpoints such as Login, set the request to **No Auth**.

Now token handling is a three-part system: the login request captures `authToken`, the collection auth reads `{{authToken}}`, and every other request inherits it. When the token expires, you rerun Login, and nothing else changes. Use the Postman Console or the Headers tab's **hidden** auto-generated headers (the "6 hidden" link) to confirm the header was added.

### 17. Debugging variables

When something is wrong, work through these tools in order.

**Colour in the editor.** A variable shown in **orange/red** has no value anywhere in the current scopes; a variable shown in **blue** was resolved. Red means: no environment selected, a typo, or a variable that has not been created yet.

**Hover.** Hover the mouse over `{{baseUrl}}` in the URL. A card shows the **scope**, the **initial value**, and the **current value**. This answers "where is this coming from, and what is it?" in two seconds.

**The eye icon.** The eye in the top right opens a quick-look panel listing the globals and the active environment's variables (and collection variables when a request is open). You can edit current values there in a hurry.

**The Postman Console.** Open it from the **View** menu or with Ctrl+Alt+C (Cmd+Option+C on Mac). It lists every request that was sent, with the **final URL**, headers, and body after substitution, plus everything you printed. If the final URL contains `{{baseUrl}}` still, the variable was undefined.

**`console.log` in scripts.** The simplest and most powerful tool:

```javascript
console.log("itemId before send:", pm.variables.get("itemId"));
console.log("whole environment:", pm.environment.toObject());
console.log("status:", pm.response.code);
```

Each call prints a label and a value; objects are expandable in the Console. Put a log at the start of a script to see what the script saw, and another at the end to see what it produced.

A table of common symptoms:

| Symptom | Likely cause | Fix |
|---|---|---|
| `{{baseUrl}}` shows red | No environment selected, or the name is misspelled or differently cased | Pick the environment, compare names exactly |
| The Console shows a request to `https://{{baseUrl}}/...` or a DNS error | Variable undefined, or you typed `https://` before a variable that already contains it | Define the variable; remove the extra scheme |
| Old value is still used | The script wrote to one scope but you read another, or a higher-precedence scope has the same name | Print `pm.variables.get`, then each scope's value |
| Chain works on the second run but not the first | The variable existed from a previous run | Check initial state; use `unset` at the end of chains |
| The value works for you, not a teammate | Real value is only in your **current** value | Agree on setup instructions and placeholder initial values |
| `Cannot read properties of undefined (reading 'id')` | The response was not what you expected (error body, HTML), so `body.id` is missing | `console.log(pm.response.text())` first |
| `Unexpected token < in JSON` | `pm.response.json()` was called on an HTML error page | Check the status code before parsing |
| Variable set by script is gone | No environment selected, or the script ran after the request that needed it | Select an environment; move the script to pre-request |

### 18. Variable types and JSON quoting rules

All Postman variables are stored as **text**, but when they land inside a JSON body, JSON's own rules apply. The simple rule is: **Postman substitutes the text exactly; it does not add or remove quotation marks.** So you, the author, must put the quotation marks where JSON requires them.

| JSON type | Correct template | After substitution | Common mistake |
|---|---|---|---|
| String | `"name": "{{itemName}}"` | `"name": "Widget"` | `"name": {{itemName}}` produces `"name": Widget`, invalid JSON |
| Number | `"quantity": {{quantity}}` | `"quantity": 5` | `"quantity": "{{quantity}}"` sends the string `"5"`; some APIs reject it |
| Boolean | `"active": {{isActive}}` | `"active": true` | Quoting it sends the string `"true"` |
| Null | `"note": null` | unchanged | Using an empty variable gives `"note": ` (invalid) |
| Object or array | `"tags": {{tagsJson}}` where `tagsJson` is `["a","b"]` | `"tags": ["a","b"]` | Forgetting that a stored array must be valid JSON text |

Two related traps. First, a value containing a double quote or a backslash (for example a name like `O"Brien`) will break the JSON when placed inside a quoted string. Either avoid such values or build the body in a pre-request script with `JSON.stringify`. Second, the strictest tests deliberately compare types. If your API expects the number `5` and your body sends the string `"5"`, a good API returns `400 Bad Request`, which might be exactly the validation behaviour you want to test next week; but accidentally sending the wrong type makes a correct API look broken.

### 19. Exporting environments safely

You will export for backups, for committing to a repository, and for sharing with a teammate who is not in your workspace. In the sidebar, hover the environment, open the three-dots menu, and choose **Export**; Postman saves a `.json` file. Collections export the same way, from the collection's menu.

The danger is that an exported file might contain real secrets. Do not assume Postman will exclude current values; Postman versions differ in what they export, so **always open the file in a text editor and read it before sharing**. Follow this routine:

1. Before exporting, set every sensitive variable's initial value to a placeholder such as `<set-me>`, and clear its current value if you will export current values.
2. Export the environment to a file named `project2-dev.postman_environment.json`.
3. Open the file in a text editor and search for words such as `password`, `token`, `key`, `secret`, and long random-looking strings.
4. Replace any real value you find with a placeholder, and save.
5. Commit only the scrubbed file. Add a note in the project README that says which variables each person must fill in.
6. If a real secret ever reached a repository, treat it as compromised: rotate (replace) the credential immediately. Deleting the file in a later commit does not remove it from history.

A cleaned fragment looks like this:

```json
{
  "name": "Project2 - Dev",
  "values": [
    { "key": "baseUrl",   "value": "https://dev.api.example.com/api/v1", "type": "default", "enabled": true },
    { "key": "username",  "value": "qa_dev_user",   "type": "default", "enabled": true },
    { "key": "password",  "value": "<set-me>",      "type": "secret",  "enabled": true },
    { "key": "authToken", "value": "",              "type": "secret",  "enabled": true }
  ]
}
```

The file is JSON. The `values` array has one object per variable, each with a `key` (the name), a `value`, a `type` (`default` or `secret`), and an `enabled` flag. The `password` value is a placeholder, and `authToken` is empty because the login request fills it in. Anyone importing this file gets the structure and fills in their own secrets.

### 20. Full worked build: a portable `Project 2 API` collection

This section puts everything together into the deliverable for today's exercise. Treat it as a checklist you can follow while building.

**Step 1. Environments.** Create `Project2 - Local` (or Dev) and a second one, `Project2 - Test`. In each define `baseUrl`, `username`, `password` (secret type), `authToken` (secret type, empty), and `timeoutMs`. Fill real secrets only in current values and put placeholders in initial values.

**Step 2. Collection variables.** On the `Project 2 API` collection, open Variables and add `apiVersion` = `v1` (if your API paths include it) and `pageSize` = `20`. Keep per-target values out of here.

**Step 3. Collection authorization.** Bearer Token, `{{authToken}}`, as in section 16.

**Step 4. Folder structure.** Create folders `Auth`, `Items CRUD`, and `Negative Tests`. Place Login in `Auth`, the six requests of section 12 in `Items CRUD`, and requests such as "Get item with unknown id" and "Create item without name" in `Negative Tests`.

**Step 5. Replace every hard-coded value.** In every request the URL must begin with `{{baseUrl}}`. Search the collection (Ctrl+F in the sidebar) for `http://` and `https://`, and for any long token string; none should remain except inside variable values.

**Step 6. Capture and chain.** Login stores `authToken`; Create stores `itemId`; later requests use it; the last request unsets it.

**Step 7. Collection-level checks.** At collection level, add a Pre-request script that checks that the environment is selected and the base URL exists:

```javascript
if (!pm.variables.get("baseUrl")) {
    throw new Error("baseUrl is not defined. Select a Project2 environment (top right).");
}
```

Explanation. `pm.variables.get("baseUrl")` reads the resolved value. `!` flips true and false, so the condition means "baseUrl is missing". `throw new Error("...")` stops the script with a readable message, which Postman shows as a script error before the request runs. This gives teammates a clear instruction instead of a mysterious DNS failure.

**Step 8. Run the whole collection with the Runner under both environments.** Run it with `Project2 - Local`, then switch the dropdown to `Project2 - Test` and run again. The same collection must pass against both without a single edit. If it does, it is portable.

**Step 9. Export and scrub.** Export the collection and the environments, scrub them using section 19, and place them in your project folder, for example `postman/Project2.postman_collection.json` and `postman/project2-dev.postman_environment.json`. These files can also be run outside the Postman app with Newman, Postman's command-line runner, which is outside this week's lessons.

**Step 10. Document.** Add a short README section: how to import, which environment to select, which variables to fill in, and in what order to run the requests.

Forward pointer: this same separation of configuration from tests returns in Python configuration on Tuesday and in pipeline variables and secrets on Friday.

### 21. Realistic scenarios

**Scenario 1: Moving from Dev to Staging before a release.** The release manager asks for a regression run on Staging by 3 p.m. A tester with a hard-coded collection must edit dozens of URLs. A tester using `{{baseUrl}}` switches the dropdown to `Project2 - Staging`, clicks Run, and has results in minutes. The test content did not change; only the target did.

**Scenario 2: Two testers, one shared password policy.** The team shares a workspace. The lead stores a placeholder in the initial value for each test user's password. Each tester types their own sandbox password into their current value. Nobody sees anyone else's credentials; the lead can audit the workspace and find only placeholders.

**Scenario 3: The token that expires every 15 minutes.** A long regression run keeps failing with `401` halfway through. The team places the Login request first and uses collection-level inheritance with `{{authToken}}`. For long runs, they add a collection pre-request that checks a stored expiry time (a variable `tokenExpiresAt`) and logs in again when needed. They solve the problem in one place rather than in a hundred requests.

**Scenario 4: "Email already exists."** A test that registers a user passes the first time and fails forever afterwards. The tester replaces the fixed email with `qa+{{$timestamp}}@example.com` (or a pre-request script with `Date.now()`). The test now passes on every run, and they log the email so any failing record can be traced.

**Scenario 5: The mysterious wrong environment.** A tester runs the "delete all my test orders" request. Nothing happens, and then the dev team reports their data was wiped. The dropdown had silently stayed on Staging. The fix is cultural and technical: environment names that make the target obvious, a collection pre-request that logs `pm.environment.name` at the start of every run, and no destructive requests allowed in production-like environments.

**Scenario 6: A colleague's run fails, yours passes.** Their Console shows `Bearer ` followed by nothing. Their `authToken` current value is empty because they never ran Login. The checklist in the README, plus a test at the start of the collection that fails loudly when the token is missing, fixes it.

### 22. Common mistakes and why they happen

**Typing `https://` before a base URL variable that already contains it.** This yields `https://https://host`. The cause is that a variable is replaced as plain text with no understanding of URLs. Decide once what the variable includes, and write it in the README.

**Mixing up `{{name}}` and `pm.environment.get("name")`.** The braces are for request fields. In scripts, use the `pm` functions. The braces are not JavaScript.

**Setting in one scope and reading from another.** A script that does `pm.globals.set("token", t)` and a request that uses an environment variable of the same name look correct but disagree. Settle one scope per variable.

**Expecting a post-response script to change the current request.** The request has already been sent, so the new value affects the next request. Move the calculation to a pre-request script when the current request needs it.

**Forgetting to save.** Environment edits show an unsaved dot, and unsaved values are ignored by some paths such as Runner runs. Save with Ctrl+S.

**Leaving real secrets in the initial value.** Initial values sync and export. Use placeholders there.

**Comparing a number with text.** Stored values are text. Convert with `Number(...)` before comparing with JSON numbers.

**Using globals for everything.** Names collide across collections; a global with the same name as a collection variable is silently overridden, or silently overrides a missing one. Prefer environment and collection scopes.

**Ignoring red variables.** A red name means Postman will send literal braces. Fix it before pressing Send.

**Not cleaning up chain state.** Leftover `itemId` values let a later run appear to succeed using stale data. Unset at the end of the chain.

**Forgetting quoting rules in JSON.** Strings need quotes, numbers and booleans do not. A small slip yields `400 Bad Request` and a confused tester.

### 23. Practice exercises with worked solutions

**Exercise 1. Two environments.** Create environments `Dev` and `Alt` that both define `baseUrl` as `https://jsonplaceholder.typicode.com`, with `userId` set to `1` in Dev and `2` in Alt. Run `GET {{baseUrl}}/users/{{userId}}` in each and confirm the responses differ.

*Solution.* In the sidebar, create `Dev` with rows `baseUrl` and `userId = 1`; create `Alt` with the same names and `userId = 2`; Save both. Create a request named `Get user`, set the URL to `{{baseUrl}}/users/{{userId}}`. Select `Dev` in the dropdown and Send; the response body has `"id": 1` and `"name": "Leanne Graham"`. Switch the dropdown to `Alt` and Send; the body has `"id": 2` and `"name": "Ervin Howell"`. The request was never edited, which shows that environments change the values behind the names.

**Exercise 2. Scope clash.** Define `userId` at collection scope as `5` and at environment scope as `1`. Which user is returned, and why? Then delete the environment value and predict what happens.

*Solution.* User 1 is returned, because the environment scope is narrower than the collection scope, and the narrower scope wins (Local > Data > Environment > Collection > Global). After deleting the environment's `userId`, no narrower scope defines it, so the collection value applies and user 5 is returned. Verify with `console.log(pm.variables.get("userId"))`.

**Exercise 3. Capture an id.** Write a post-response script on `POST {{baseUrl}}/posts` that saves the returned `id` to an environment variable `postId`, and verify the capture with a test. Then add `GET {{baseUrl}}/posts/{{postId}}` after it.

*Solution.* Body for the POST (raw JSON): `{"title": "foo", "body": "bar", "userId": 1}`. Post-response script:

```javascript
const created = pm.response.json();
pm.environment.set("postId", created.id);

pm.test("postId captured", function () {
    pm.expect(pm.environment.get("postId")).to.exist;
});
```

The first line parses the response, the second stores the id (JSONPlaceholder returns `101`), and the test confirms the variable exists. The follow-up GET resolves to `/posts/101`. Because JSONPlaceholder does not really store the new post, that GET returns `404`. That is expected; the point of the exercise is the capture and substitution, which you can confirm in the Console by checking that the URL ended in `101`.

**Exercise 4. A unique title.** Add a pre-request script that generates a unique `title` using `Date.now()` and use it in the body.

*Solution.* Pre-request script:

```javascript
pm.variables.set("title", "Post " + Date.now());
```

Body: `{"title": "{{title}}", "body": "bar", "userId": 1}`. The string is quoted in the body because the title is a string. Send twice and compare in the Console: the title differs each time. The variable is local, so it appears in no environment table.

**Exercise 5. Initial versus current.** Explain the difference between initial and current values, and say where you would store an API key and why.

*Solution.* The initial value is synced to the Postman cloud, visible to teammates, and may be included in exports. The current value stays on your own machine and is what requests actually use. An API key belongs in a variable of type **secret**, with a placeholder in the initial value and the real key only in the current value, so it is masked on screen and never synced. For maximum protection the Postman vault can hold it.

**Exercise 6. Prove a precedence rule yourself.** Using `postman-echo`, show that a data-file value beats an environment value, but a local value beats the data value.

*Solution.* Define `team = environment-value` in the active environment. Create `team.csv` with header `team` and one row `data-value`. Request: `GET https://postman-echo.com/get?team={{team}}`. Run through the Collection Runner with the file: the echoed `args.team` is `data-value`. Then add the pre-request script `pm.variables.set("team", "local-value");` and run again: the echo is `local-value`. The two runs prove Data > Environment and Local > Data.

**Exercise 7. A defensive collection check.** Write a collection-level pre-request script that stops the run with a clear message if `authToken` is empty for any request except the login request.

*Solution.*

```javascript
const isLogin = pm.info.requestName === "Login";
const token = pm.environment.get("authToken");

if (!isLogin && !token) {
    throw new Error("authToken is empty. Run the Login request first.");
}
```

`pm.info.requestName` is the name of the request now running. The first line produces `true` when the current request is called `Login`. The second reads the token. The `if` checks "not login AND no token"; `&&` means "and". If both are true, `throw new Error(...)` aborts with a readable message. Requests named differently from `Login` will trigger the error when no token is stored, and the login request itself is allowed through.

**Exercise 8. Same generated value twice.** A body needs the same random GUID in `orderRef` and in `trackingRef`. Writing `{{$guid}}` twice gives different values. Fix it.

*Solution.* Pre-request script:

```javascript
const ref = pm.variables.replaceIn("{{$guid}}");
pm.variables.set("sharedRef", ref);
console.log("sharedRef =", ref);
```

Body: `{"orderRef": "{{sharedRef}}", "trackingRef": "{{sharedRef}}"}`. `replaceIn` generates one GUID and returns it as text, `set` saves it locally, and the body uses the stored name twice, so both fields match. The log line records the value for reproducibility.

**Exercise 9. Convert a hard-coded request.** Rewrite `GET https://dev.api.example.com/api/v1/items?limit=20` with header `Authorization: Bearer eyJ...abc` into a portable form.

*Solution.* Environment `Dev`: `baseUrl = https://dev.api.example.com/api/v1`, `authToken` (secret). Collection variable `pageSize = 20`. Collection authorization: Bearer Token `{{authToken}}`. The request becomes `GET {{baseUrl}}/items?limit={{pageSize}}` with Authorization set to *Inherit auth from parent* and no manual header. Host and token moved to the environment, the page size to a collection default, and the header disappeared in favour of inheritance.

**Exercise 10. Scrub an export.** You exported an environment and found the line `{ "key": "authToken", "value": "eyJhbGciOi...", "type": "secret" }`. What do you do before committing?

*Solution.* Replace the value with an empty string or a placeholder, check the rest of the file for other secrets, and commit only the scrubbed file. If the unscrubbed file was already committed or shared, assume the token is compromised, revoke or rotate it, and understand that a later deleting commit does not erase history.

### 24. Self-check quiz

1. What does Postman do with a `{{name}}` that matches no variable in any scope?
2. List the five scopes from highest to lowest precedence.
3. A script in the Tests tab sets `authToken`. Can the same request use it? Why or why not?
4. Which column of a variable is synced to teammates, and which is used by default when sending?
5. Which `pm` function reads a value using precedence, and which function writes a local variable?
6. Why is `"quantity": "{{quantity}}"` risky in a JSON body?
7. What does `{{$guid}}` produce, and why does using it twice in a body give two different values?
8. Why should you open an exported environment file before sharing it?
9. Why must you convert `pm.environment.get("itemId")` with `Number(...)` before comparing it with a JSON number?
10. Name two benefits of setting Bearer authorization on the collection rather than on each request.

**Answers.**

1. It leaves the text `{{name}}` unchanged and sends it literally, which usually causes a failure; the variable shows red in the editor.
2. Local, data, environment, collection, global.
3. No. The request has already been sent when post-response scripts run, so the variable can only affect later requests. Set it in a pre-request script if the same request needs it.
4. The initial value is synced; the current value is used when sending and stays local.
5. `pm.variables.get` reads with precedence; `pm.variables.set` writes a local variable.
6. The quotes turn the number into a string (`"5"`), and some APIs reject or mishandle strings where numbers are expected.
7. It generates a UUID. Each occurrence is generated independently, so two uses give two values.
8. Because the export may contain real secrets in values, and once shared or committed they can leak.
9. Variable values are stored as text, while JSON numbers are numeric; strict equality between `"17"` and `17` fails.
10. The token is defined in one place, so renewing it needs no per-request edits, and no request carries a hard-coded token that could leak or go stale.

### 25. Glossary

**Variable.** A named placeholder whose value is substituted into a request or read by a script.

**`{{ }}` syntax.** The double-curly-brace notation that marks a Postman variable in request fields.

**Scope.** The place where a variable lives and is visible: global, collection, environment, data, or local.

**Precedence.** The rule that decides which value wins when the same name exists in several scopes; the narrowest scope wins.

**Environment.** A named set of variables representing a target such as Dev or Staging, selected from the top-right dropdown.

**Initial value.** The synced, shareable value of a variable.

**Current value.** The local value of a variable actually used when sending; not synced.

**Secret type.** A variable type that masks its value on screen.

**Vault.** Postman's local encrypted storage for sensitive values, referenced as `{{vault:name}}`.

**Data variable.** A variable that comes from a row of a CSV or JSON data file during a runner iteration.

**Local variable.** A temporary variable created with `pm.variables.set` that exists only for one request or run.

**Dynamic variable.** A built-in generator such as `{{$guid}}`, producing a new value each time.

**Pre-request script.** JavaScript that runs before the request is sent and before variable substitution.

**Post-response script.** JavaScript (the Tests tab) that runs after the response arrives.

**Chaining.** Capturing values from one response and using them in later requests.

**`pm` object.** The object Postman gives to every script, exposing variables, the request, the response, and testing helpers.

**CryptoJS.** A cryptography library included in Postman's script sandbox, used for hashes and encoding.

**Collection Runner.** The tool that runs the requests of a collection in sequence, optionally with a data file.

**Newman.** Postman's command-line collection runner.

**Hard-coding.** Writing a specific value directly into a request instead of referring to it by name.

---

## Summary

- Hard-coded hosts, tokens, ids, and emails make tests fragile, non-portable, and unsafe to share. Variables (`{{name}}`) replace each with a named placeholder, resolved just before the request is sent.
- Postman has five scopes: global, collection, environment, data, and local. The narrower scope wins: Local > Data > Environment > Collection > Global. The experiment in section 5 proves it, and `pm.variables.get` shows what actually resolves.
- Environments (Dev, Test, Staging) hold per-target values. Keep the same variable names in every environment and switch with the dropdown, not by editing requests.
- Initial values sync and may be exported; current values stay local. Put placeholders in initial values and real secrets in current values, set the type to secret, and consider the vault for long-lived credentials.
- In scripts, use `pm.environment`, `pm.collectionVariables`, `pm.globals`, `pm.variables`, and `pm.iterationData` with `get`, `set`, `unset`, `has`, and `toObject`. Stored values are text, so convert and quote carefully.
- Post-response scripts capture ids and tokens to chain requests; pre-request scripts compute timestamps, unique emails, base64 strings, and signatures; dynamic variables generate fresh data.
- Collection-level authorization with `{{authToken}}` removes repeated headers; `pm.sendRequest` can automate login at awareness level.
- Debug with the red/blue colouring, hover cards, the eye icon, the Postman Console, and `console.log`. Always scrub exports before sharing.
- A portable Project 2 API collection uses `{{baseUrl}}`, captured ids, an inherited token, and placeholders in every shared file. Data-driven runs come on Wednesday, and the same ideas return in Python configuration on Tuesday and CI variables on Friday.

## Additional Resources

- Postman Docs, *Variables*: https://learning.postman.com/docs/sending-requests/variables/variables/
- Postman Docs, *Create and manage environments*: https://learning.postman.com/docs/sending-requests/variables/managing-environments/
- Postman Docs, *Dynamic variables*: https://learning.postman.com/docs/tests-and-scripts/write-scripts/variables-list/
- Postman Docs, *Script reference (the `pm` object)*: https://learning.postman.com/docs/tests-and-scripts/write-scripts/postman-sandbox-api-reference/
- Postman Docs, *Postman Vault*: https://learning.postman.com/docs/sending-requests/postman-vault/postman-vault-secrets/
