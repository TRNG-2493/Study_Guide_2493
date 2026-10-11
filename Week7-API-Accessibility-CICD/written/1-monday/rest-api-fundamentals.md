# REST API Fundamentals

## Learning Objectives

By the end of this lesson you will be able to:

- Define the terms **API**, **web API**, and **REST**, and explain them with everyday analogies.
- Describe the different types of APIs and explain where web APIs fit.
- Explain why APIs exist, how modern applications are layered, and why the test pyramid puts API tests in the middle.
- Explain who Roy Fielding is and why REST is an architectural style rather than a protocol.
- Explain each of the six REST constraints in plain language and state what each one means for a tester.
- Identify **resources**, **collections**, **sub-resources**, **endpoints**, and the **base URL** in any API address.
- Apply URL naming conventions and recognise poorly designed URLs.
- Compare the main API versioning strategies.
- Map HTTP methods to CRUD operations.
- Read and write JSON with every data type, including nested objects and arrays of objects, and fix common JSON syntax errors.
- Describe how status codes are used in a REST context.
- Recognise HATEOAS, the Richardson Maturity Model, pagination, filtering, and sorting at an awareness level.
- Read an OpenAPI (Swagger) specification excerpt line by line.
- Compare REST with SOAP, GraphQL, and gRPC.
- Explore every endpoint family of JSONPlaceholder with `curl` and predict the output.
- Apply a tester's checklist to any endpoint and work through realistic scenarios.

---

## Why This Matters

This week's epic is to add API testing, accessibility and MCP testing, and CI/CD to your Project 2 test automation framework. API testing is the foundation of everything else this week. On Tuesday you will automate API calls with Python. On Wednesday you will make those tests data-driven, mocked, and reusable. On Friday you will run them inside a GitLab pipeline. Every one of those steps depends on you understanding what a REST API is and how it is designed. Today is the vocabulary and mental-model day. If you leave today able to look at any URL and say "that is a collection, that is a sub-resource, that is the version, and these are the five tests I would write," the rest of the week will feel natural.

There is also a hard economic reason. Modern applications are built in layers. At the top is a user interface (a web page or mobile app) that people see. Underneath is an API that the screens call whenever they need data or want to change something. Underneath that are the business rules and the database. The user interface changes often, depends on browsers and devices, and is slow and fragile to automate. The API is stable, fast, and exercises the real business rules directly. Teams that test mainly through the UI end up with slow suites that fail for reasons unrelated to defects. Teams that test heavily at the API layer find defects earlier, run their suites in seconds, and can run them on every code change inside a CI/CD pipeline. When you are hired as a Test Automation Engineer, a large share of your daily work will be API tests, and your ability to design good API tests starts with understanding how REST APIs are designed.

You have already learned the basics of HTTP messages (requests, responses, methods, status codes, headers, and bodies) earlier today. This lesson builds on that by showing how REST uses those pieces to form a consistent style of API design. Later lessons today will go deep on each HTTP method, on Postman, on query parameters and path variables, on headers, and on Postman variables. Here we focus on the big picture.

---

## The Concept

### 1. What Is an API?

**API** stands for **Application Programming Interface**. Break the name into three parts. *Application* means any piece of software. *Programming* means the interaction is done by code, not by a person clicking buttons. *Interface* means a defined boundary, a place where two things meet and agree on how they will communicate. Put together, an API is a defined way for one piece of software to ask another piece of software to do something or to give it some data, without needing to know how the other software does it internally.

The most important word in that definition is **defined**. An API is a contract. It says: "If you send me a request that looks like this, I promise to respond with something that looks like that." Both sides can then be built and changed independently as long as they keep honouring the contract. As a tester, you are effectively a contract auditor. Your job is to check whether the promise is kept in every situation, including the unusual ones.

#### Several analogies

No single analogy covers everything, so here are four. Use whichever one clicks for you.

**The restaurant.** You sit at a table and read a menu. The menu lists what you can order and describes what you will get. You tell the waiter your order. The waiter takes it to a kitchen you never see, and returns with your food. You do not need to know the recipes, the brand of oven, or how many cooks there are. In this analogy, the menu is the API documentation, the waiter is the API itself (carrying requests in and responses out), and the kitchen is the server with its code and database. If you order something not on the menu, the waiter says "we do not have that," which is the equivalent of an error response. If the kitchen runs out of an ingredient, the waiter reports a different kind of problem, which is the equivalent of a server error.

**The electrical wall socket.** A socket is a standard interface. Any appliance with the right plug can draw power, and the appliance does not need to know whether the electricity came from coal, solar, or wind. If the socket changes its shape, every appliance stops working. That is why API contracts must not change carelessly, and why versioning (covered below) exists.

**The bank teller window.** You slide a withdrawal slip under the glass. You cannot walk into the vault yourself. The teller checks your identity, checks the balance, and returns cash or a refusal. The window is the only way in, and the rules are enforced on the other side of the glass. This analogy highlights that APIs also act as the gatekeeper for security and validation, which is exactly why testers care so much about them.

**The postal service.** You write an address on an envelope and drop it in a post box. The address format is standardised, and the postal system does not care what is inside. The reply comes back as another envelope. HTTP works much like this: each request and response is a self-contained message with a standard envelope (headers) and contents (body).

#### Types of APIs

The word API is broad, and you will meet several kinds in your career.

**Operating-system APIs** are the functions an operating system offers to programs, such as opening a file or drawing a window. **Library and framework APIs** are the functions and classes a code library exposes; when you call `len(my_list)` in Python or a method in a testing library, you are using a library API. **Database APIs** are the drivers and query interfaces programs use to talk to databases. **Hardware APIs** let software talk to devices such as cameras. And **web APIs** let programs on different computers talk over a network using HTTP.

You can also classify APIs by who may use them. A **private (internal) API** is used only inside one company, for example between the mobile app and the company's own servers. A **partner API** is shared with selected business partners under an agreement. A **public (open) API** is available to any developer, often with a free signup, such as weather, maps, or payment services. A **composite API** combines several calls into one, which saves round trips.

In this course, "API" means **web API**: an API reached over a network by sending HTTP requests and receiving HTTP responses. Almost all modern web, mobile, and cloud applications are built on them. When job descriptions say "API testing," they nearly always mean testing web APIs, and most of those are REST APIs.

### 2. Why APIs Exist: Layers, Reuse, and the Test Pyramid

Imagine an online bookshop. It has a website, an Android app, an iPhone app, and a partner site that resells its books. If each of these separately contained the code for "check stock," "calculate shipping," and "place an order," the company would maintain four copies of every business rule, and a bug fix in one would not fix the others. Instead, the company builds the business rules once, behind an API. Every client calls the same API. This gives several benefits.

First, **reuse**: one set of rules serves many clients. Second, **separation of concerns**: front-end developers work on how things look, back-end developers on how things work, and they agree on the API contract between them. Third, **independent change**: the company can redesign the website without touching the order logic. Fourth, **integration**: other companies can build on top of the service. Fifth, **testability**: since business rules are reachable through the API without any screen, they can be tested directly.

#### The layered architecture

A typical application has three or more layers:

```
+--------------------------------------------+
|  Presentation layer (UI)                   |   Web page, mobile app
+--------------------------------------------+
|  API / Service layer                       |   REST endpoints, validation, authentication
+--------------------------------------------+
|  Business logic layer                      |   Rules: discounts, stock, permissions
+--------------------------------------------+
|  Data layer                                |   Database, files, other services
+--------------------------------------------+
```

This diagram is a picture of how responsibility is divided. The top layer shows information to people and collects their input. The API layer exposes operations over HTTP and checks that incoming requests are well formed and authorised. The business layer decides what is allowed (for example, "a customer cannot order more items than are in stock"). The data layer stores the information. A click on a button in the UI triggers a request to the API layer, which passes through the lower layers and returns a response that the UI then renders.

#### The test pyramid

Because of this layering, tests can be written at different levels, and the **test pyramid** is a widely used guide for how many to write at each level.

```
            /\
           /UI\          Few: slow, fragile, expensive
          /----\
         / API  \        Some: fast, stable, business rules
        /--------\
       /   Unit   \      Many: very fast, small, developer-written
      /------------\
```

At the bottom are many **unit tests** that check small pieces of code in isolation. They are very fast, but they do not prove the pieces work together. At the top are a few **UI tests** that drive a real browser the way a user would. They prove the whole system works end to end, but they are slow, depend on page layout, and fail for incidental reasons. In the middle are **API tests**. They run the real business logic and real integrations but skip the screen, so they are fast enough to run on every commit and stable enough to trust. A healthy suite has lots of unit tests, a good number of API tests, and a carefully chosen few UI tests. As a Test Automation Engineer, the middle layer is where you will add the most value.

### 3. What Is REST and Where Did It Come From?

**REST** stands for **REpresentational State Transfer**. It is an **architectural style**: a set of design principles, not a product, a protocol, or a piece of software. Nobody can "install REST." Instead, a team designs its API to follow the principles, and an API that does is called **RESTful**.

REST was described by **Roy Fielding** in his 2000 doctoral dissertation at the University of California, Irvine. Fielding was one of the principal authors of the HTTP specification, and he wrote about the architecture that made the World Wide Web scale so successfully. He asked: why did the web, with millions of independent servers and clients built by different people, work so well? His answer was a set of constraints that, if followed, give a system desirable properties such as scalability, simplicity, and the ability to evolve. He named that set of constraints REST.

The central idea is that everything of interest is a **resource**: a thing with an identity, such as a customer, an order, a product, or a booking. Each resource is identified by a **URL**. A client never touches the resource directly. Instead, the client asks the server for a **representation** of it, typically a JSON document describing its current **state**, and the client may send a representation back to ask the server to change that state. That is where the name comes from: representations of state are transferred between client and server.

Because REST is a style and not a standard, there is no certification and no official checker. APIs can be more or less RESTful, and teams often disagree about how strictly to follow the rules. For a tester, this means you cannot assume every "REST API" behaves consistently. You must learn each API's conventions and verify them.

### 4. The Six REST Constraints, Each With a Testing Implication

Fielding defined six constraints. You do not need to memorise academic wording, but you should understand each idea, because they explain why APIs behave the way they do and each one has a direct consequence for how you test.

#### Constraint 1: Client-server separation

The client (the thing that asks) and the server (the thing that answers) are separate and communicate only through the API. The client does not know how data is stored, and the server does not know how data is displayed. Because of this, the web app, the mobile app, and your automated test script can all be clients of the same server.

*Testing implication:* Your test script is simply another client. You can test the server's behaviour without any user interface at all, which is exactly what API testing is. It also means that a defect in server logic will show up the same way no matter which client triggers it, so a single API test can protect all the clients.

#### Constraint 2: Stateless

Every request must contain all the information the server needs to understand and process it. The server does not remember anything about the client between requests. If a request needs authentication, the credentials or token travel with every request. If a request needs to say "I am on page 3 of the results," it says so in the request itself.

*Testing implication:* Statelessness is what makes API tests independent. Each test can send its own complete request and does not need to rely on an earlier call having "set up a session." If you find an API where the second call only works because of the first call, that is a design smell, and tests become order-dependent and flaky. You should also test that missing authentication on any single request is rejected, because the server is not supposed to "remember" that you logged in a moment ago.

Do not confuse *statelessness of the communication* with *absence of stored data*. A stateless API can absolutely store and change data in a database. What is stateless is the conversation: no hidden memory of previous requests.

#### Constraint 3: Cacheable

Responses must indicate whether they can be stored and reused (cached) by the client or by intermediaries such as content delivery networks. A response to "get the list of countries" can safely be reused for an hour, while a response to "get my account balance" generally should not be. Servers signal this with headers, which you will study in the headers lesson.

*Testing implication:* Caching bugs are subtle. A tester should check that data that changes frequently is not marked as cacheable for long periods, that private data is not cached in shared caches, and that a change made through `PUT` or `DELETE` is visible on the next `GET`. A stale response after an update is a classic defect.

#### Constraint 4: Uniform interface

All resources are accessed in a consistent, predictable way. This is the heart of REST and has four parts. Resources are **identified by URLs**. Resources are manipulated through **representations** (for example, JSON). Messages are **self-descriptive**, meaning each message carries enough information to describe how to process it (the `Content-Type` header says the body is JSON). And **hypermedia** can guide the client to what it can do next (this last part is called HATEOAS and is covered later).

*Testing implication:* Consistency itself is testable. If `GET /users/5` returns a field called `email` but `GET /orders/9` returns `emailAddress` for the same concept, or if one endpoint reports errors as `{"error": "..."}` and another as `{"message": "..."}`, that inconsistency is a defect or at least a design flaw. A good tester writes a few cross-cutting tests, such as "every error response has the same structure."

#### Constraint 5: Layered system

Between the client and the final server there may be several intermediate layers: load balancers, API gateways, proxies, firewalls, and caches. The client cannot tell, and does not need to know, whether it is talking to the end server or to an intermediary.

*Testing implication:* The status code you receive may have been produced by a layer in the middle rather than by the application. A `502 Bad Gateway` or `504 Gateway Timeout` usually signals a problem between layers, not a bug in your business logic. Also, a test environment may include a gateway that adds rules such as rate limits. When a test fails, you must ask which layer produced the response.

#### Constraint 6: Code on demand (optional)

A server may send executable code, such as JavaScript, to the client to extend its functionality. This is the only optional constraint, and it is rarely relevant to JSON APIs.

*Testing implication:* Almost none for API testing. It is worth knowing the term so you can recognise it in a textbook or interview, and remember that a design can be called RESTful without it.

#### Quick reference table

| Constraint | Plain meaning | What a tester does with it |
|------------|---------------|----------------------------|
| Client-server | Client and server are independent | Test the server directly without a UI |
| Stateless | Every request is complete on its own | Keep tests independent; check auth on each request |
| Cacheable | Responses say if they can be reused | Check freshness after updates and caching headers |
| Uniform interface | Same style everywhere | Check consistency of structure, naming, and errors |
| Layered system | Intermediaries may exist | Identify which layer produced an error |
| Code on demand | Server may send code (optional) | Rarely relevant |

### 5. Resources, Collections, Sub-resources, Endpoints, and the Base URL

Now let us give names to the pieces of an API address. We will use **JSONPlaceholder**, a free public fake API designed for practice.

A **resource** is a single "thing": one post, one user, one order. A **collection** is a group of resources of the same kind: all posts, all users. A **sub-resource** (or **nested resource**) is a resource that belongs to another resource, such as the comments that belong to one specific post. An **endpoint** is a specific URL, combined with an HTTP method, where the API can be reached. Strictly speaking, `GET /posts` and `POST /posts` are two different endpoints (or operations) at the same URL, but people often use "endpoint" to mean just the URL.

| URL | What it represents |
|-----|--------------------|
| `https://jsonplaceholder.typicode.com/posts` | The **collection** of all posts |
| `https://jsonplaceholder.typicode.com/posts/1` | A **single resource**: the post with ID 1 |
| `https://jsonplaceholder.typicode.com/posts/1/comments` | A **sub-collection**: the comments belonging to post 1 |
| `https://jsonplaceholder.typicode.com/comments/1` | A single comment resource, reached directly |
| `https://jsonplaceholder.typicode.com/users` | The collection of all users |

#### Anatomy of a URL

Take a longer address and label each piece:

```
https://api.shop.example.com:443/v1/customers/42/orders/7?expand=items#top
\___/   \__________________/ \_/ \_______________________/ \________/ \_/
scheme        host          port           path              query    fragment
```

The **scheme** (`https`) is the protocol. The **host** (`api.shop.example.com`) is the server's name. The **port** (`443`) is the door on that server; HTTPS uses 443 by default and is usually omitted. The **path** (`/v1/customers/42/orders/7`) identifies the resource. The **query string** (`?expand=items`) carries optional modifiers. The **fragment** (`#top`) is only used by browsers and is never sent to the server.

The **base URL** is the common prefix shared by every endpoint of the API. Here it would be `https://api.shop.example.com/v1`. Everything after the base URL is the endpoint path: `/customers/42/orders/7`. Defining the base URL once is important for testing. In Postman and in automated scripts you store the base URL in a variable so that the same tests can run against development, staging, and production by changing one value. You will do exactly this in the Postman variables lesson later today.

Reading `/customers/42/orders/7` from left to right gives a sentence: "in the customers collection, the customer with ID 42; within that customer's orders collection, the order with ID 7." The alternating pattern of collection name followed by identifier is the signature of REST URLs.

### 6. URL Naming Conventions

REST URLs are meant to be predictable. If you know there is a `/customers` collection, you should be able to guess that `/customers/42` is one customer and `/customers/42/orders` is that customer's orders. Consistent naming helps developers, helps documentation, and helps you write tests that generalise.

| Guideline | Good | Poor | Why it matters |
|-----------|------|------|----------------|
| Use **nouns** for resources; the HTTP method is the verb | `POST /orders` | `POST /createOrder` | The method already says "create." Verbs in URLs duplicate it and lead to endless variants (`/deleteOrder`, `/removeOrder`). |
| Use **plural** nouns for collections | `/users`, `/users/42` | `/user`, `/user/42` | One rule for both the collection and the item, so `/users/42` reads as "item 42 of users." |
| Identify items by **path ID** | `/users/42` | `/getUser?id=42` | The resource has its own address that can be bookmarked, cached, and linked. |
| **Nest** to show ownership | `/users/42/orders` | `/ordersOfUser42` | The structure of the URL mirrors the structure of the data. |
| Use **lowercase** letters | `/order-items` | `/OrderItems` | Paths can be case-sensitive; mixed case causes accidental 404 errors. |
| Use **hyphens** to separate words | `/order-items` | `/order_items`, `/orderItems` | Hyphens are the common convention and read clearly in links. |
| No **trailing slash** or file extension | `/users/42` | `/users/42/`, `/users/42.json` | Two addresses for one resource cause confusion and duplicate caching. |
| Do not expose **implementation details** | `/users` | `/getUsersFromMySql.php` | The URL is a public contract and should survive a change of technology. |
| Keep nesting **shallow** (about two levels) | `/orders/7/items` | `/customers/1/orders/7/items/3/options/2` | Deep paths are hard to read; refer to deep items directly by their own ID. |
| Use **query parameters** for filtering, not new paths | `/orders?status=shipped` | `/shippedOrders` | New filters should not create new endpoints. (Query parameters get their own lesson today.) |

Some operations do not fit neatly into "create, read, update, delete." Examples are "cancel an order" or "send a password reset email." Mature APIs usually still model these in a noun-style: `POST /orders/7/cancellation`, or they update a status field with `PATCH /orders/7`. A few APIs use an action-style path such as `POST /orders/7/cancel`. Real-world APIs bend the rules, so as a tester you should evaluate each API against its own documentation, while noting inconsistencies in your findings.

**Tester's note on case and slashes:** Try variants of a valid URL. Does `/Users/1` work the same as `/users/1`? Does `/users/1/` behave the same as `/users/1`? Some servers redirect, some return 404, and some return the data. Whatever the behaviour, it should match what the documentation says.

### 7. API Versioning

APIs change over time. New fields are added, old fields are renamed, rules are tightened. But other developers (and your own mobile apps in the field) rely on the current contract, and breaking it causes real harm. **Versioning** is the practice of labelling the contract so that old clients keep working while new clients use the improved version. A **breaking change** is any change that can make existing clients fail, such as removing a field, renaming a field, changing a data type, or making a previously optional field required. A **non-breaking change** is typically adding a new optional field or a new endpoint.

The main strategies are:

| Strategy | Example | Advantages | Drawbacks |
|----------|---------|------------|-----------|
| **URL path versioning** | `GET /v1/users/42` and `GET /v2/users/42` | Very visible, easy to test and cache, easy to route | URL changes with each version; some argue a resource's address should not change |
| **Query parameter versioning** | `GET /users/42?version=2` | Easy to add, simple default | Easy to forget, can interfere with caching, less clear |
| **Header versioning** | `X-API-Version: 2` | Clean URLs | Invisible in browser address bar, harder to test casually |
| **Media type (content negotiation) versioning** | `Accept: application/vnd.shop.v2+json` | Purist approach; versions the representation, not the resource | More complex for clients and for testers |

URL path versioning is by far the most common, and it is what you will see in most real-world APIs and in this course.

*Testing implications:* Versioning gives you a regression-test mandate. When `v2` is released, `v1` must still behave exactly as documented until its published retirement date, so a good suite keeps tests for both. Check what happens when a client asks for a version that does not exist (`/v99/users`); it should produce a clear error, not a server crash. Check what happens when no version is given if the API says a default exists. And watch for **deprecation notices**, which APIs often announce in documentation or in response headers.

### 8. HTTP Methods Map to CRUD

Most operations on data fall into four categories, abbreviated **CRUD**: Create, Read, Update, Delete. REST maps these onto HTTP methods.

| CRUD | Meaning | HTTP method | Example | Typical success code |
|------|---------|-------------|---------|----------------------|
| **C**reate | Add something new | `POST` | `POST /users` | `201 Created` |
| **R**ead | Retrieve | `GET` | `GET /users/42` | `200 OK` |
| **U**pdate (replace) | Replace the whole resource | `PUT` | `PUT /users/42` | `200 OK` |
| **U**pdate (partial) | Change only some fields | `PATCH` | `PATCH /users/42` | `200 OK` |
| **D**elete | Remove | `DELETE` | `DELETE /users/42` | `200 OK` or `204 No Content` |

The same URL can do different things depending on the method. `/users/42` with `GET` reads that user, with `PUT` replaces it, and with `DELETE` removes it. That is what the earlier naming rule means by "the method is the verb."

Two properties matter greatly to testers. A method is **safe** if it does not change server data (`GET` should be safe). A method is **idempotent** if repeating the same request produces the same server state as sending it once (`GET`, `PUT`, and `DELETE` should be idempotent; `POST` normally is not, because sending it twice usually creates two records). The next lesson, **GET, POST, PUT and DELETE**, explores each method in depth, so we will not go further here.

### 9. Representations and JSON in Depth

When a client asks for a resource, the server does not send the "real" thing (which is a row in a database or an object in memory). It sends a **representation**: a snapshot of the resource's state in an agreed format. The most common format for REST APIs is **JSON** (JavaScript Object Notation). Others include XML, CSV, and plain text. The `Content-Type` header on a message says which format the body uses, and the `Accept` header on a request says which formats the client prefers. Today we focus on JSON because it dominates.

JSON is a lightweight text format for structured data. It is easy for people to read and for programs to parse. It is built from just two structures: **objects** (collections of named values) and **arrays** (ordered lists), which hold values of six kinds.

#### The data types

| JSON type | What it is | Example |
|-----------|------------|---------|
| **Object** | Unordered key/value pairs inside `{}` | `{"id": 1, "name": "Leanne"}` |
| **Array** | Ordered list of values inside `[]` | `[1, 2, 3]` |
| **String** | Text in double quotes | `"hello"` |
| **Number** | Integer or decimal, no quotes | `42`, `-7`, `3.14`, `1.5e3` |
| **Boolean** | Exactly `true` or `false`, no quotes | `true` |
| **Null** | The deliberate absence of a value | `null` |

Here is a realistic document that uses every type:

```json
{
  "id": 1,
  "name": "Leanne Graham",
  "email": "Sincere@april.biz",
  "isActive": true,
  "balance": 1520.75,
  "address": {
    "street": "Kulas Light",
    "city": "Gwenborough",
    "geo": { "lat": "-37.3159", "lng": "81.1496" }
  },
  "phones": ["1-770-736-8031", "010-692-6593"],
  "manager": null
}
```

Explanation line by line. The opening `{` begins an object, and the final `}` ends it. `"id": 1` is a key (always a string in double quotes), a colon, and a value that is a **number**. `"name"` and `"email"` have **string** values. `"isActive": true` is a **boolean**; note there are no quotes, so it is not the text "true." `"balance": 1520.75` is a **number** with a decimal part. `"address"` holds a **nested object** inside curly braces, and inside it `"geo"` holds yet another object, so objects can be nested as deeply as needed. `"phones"` is an **array** containing two strings, written in square brackets and separated by commas. Finally, `"manager": null` means "this field exists but has no value," which is different from leaving the field out entirely.

**Reading nested data.** To describe the path to a value, testers use a dotted style: the city is at `address.city`, the latitude is at `address.geo.lat`, and the first phone number is at `phones[0]` (arrays count from zero). Next week and on Tuesday you will use exactly this kind of path to assert on responses in code.

#### Arrays of objects

The most common shape in an API response is a **list of objects**, which is how collections are returned:

```json
[
  { "id": 1, "title": "First post", "userId": 1 },
  { "id": 2, "title": "Second post", "userId": 1 },
  { "id": 3, "title": "Third post", "userId": 2 }
]
```

The outer `[` `]` makes this an array. Each element is an object with the same keys, separated by commas. There is no comma after the last element. When you test a collection endpoint, you check things about the whole array (how many items? is it empty when it should be?) and things about every element (does every item have an `id`? is every `id` unique? does every `userId` refer to a real user?).

#### Empty values: be precise

An empty collection is `[]`. An empty object is `{}`. An empty string is `""`. A missing value is `null`. A field that is absent is absent. These five are all different, and tests should distinguish them. For example, `{"middleName": ""}`, `{"middleName": null}`, and `{}` all say different things about a user who has no middle name, and an API should be consistent about which it uses.

#### Numbers versus strings

`"id": 1` and `"id": "1"` are different in JSON: the first is a number, the second is text. Mixing them is a frequent source of defects, particularly when one endpoint returns IDs as numbers and another returns them as strings. Notice in the example above that `lat` and `lng` are strings even though they look numeric; that is the API's choice, and a test should assert the type that the documentation promises.

#### Common JSON syntax errors and how to fix them

Malformed JSON is the number one cause of `400 Bad Request` in beginner tests. A parser is unforgiving: one wrong character invalidates the entire document. Here are the usual culprits.

**Error 1: single quotes instead of double quotes.**

```json
{ 'name': 'Anna' }
```

JSON requires double quotes around keys and strings. Fix: `{ "name": "Anna" }`.

**Error 2: trailing comma.**

```json
{ "name": "Anna", "age": 30, }
```

The comma after `30` expects another pair that never comes. Fix: remove it, giving `{ "name": "Anna", "age": 30 }`.

**Error 3: missing comma between pairs.**

```json
{ "name": "Anna" "age": 30 }
```

Two pairs must be separated by a comma. Fix: `{ "name": "Anna", "age": 30 }`.

**Error 4: unquoted key.**

```json
{ name: "Anna" }
```

This is valid JavaScript, but not valid JSON. Fix: `{ "name": "Anna" }`.

**Error 5: comments.**

```json
{ "name": "Anna" // the customer
}
```

JSON has no comment syntax. Fix: remove the comment.

**Error 6: wrong literals.**

```json
{ "active": True, "manager": None, "score": NaN }
```

`True` and `None` are Python spellings, and `NaN` is not valid JSON. Fix: `{ "active": true, "manager": null, "score": null }`.

**Error 7: unescaped special characters inside strings.**

```json
{ "quote": "She said "hello"" }
```

The inner double quotes end the string early. Fix by escaping them with a backslash: `{ "quote": "She said \"hello\"" }`. Likewise, a literal line break inside a string must be written as `\n`.

**Error 8: unbalanced brackets.**

```json
{ "items": [1, 2, 3 }
```

The array was opened with `[` but never closed with `]`. Fix: `{ "items": [1, 2, 3] }`.

**Error 9: leading zeros and hex numbers.**

```json
{ "zip": 02134 }
```

JSON numbers cannot have leading zeros. If a value such as a ZIP code must keep its zero, it is really a string: `{ "zip": "02134" }`.

Explanation of the whole block of errors: each snippet is a small, wrong document followed by its fix. Practise spotting these by eye, and when in doubt, paste your JSON into a free validator such as jsonlint.com or use your editor's JSON mode. Remember, too, that an API may legitimately be *tested* with broken JSON on purpose. Sending malformed JSON to a `POST` endpoint is a valid negative test, and the API should respond with `400 Bad Request` and a helpful message instead of crashing with `500`.

### 10. Status Codes in a REST Context

You studied status codes in the HTTP messages lesson. In REST design they carry the outcome of the operation, so choosing the right code is part of the API's contract. Here is how they usually appear for REST operations.

| Operation | Success | Typical failures |
|-----------|---------|------------------|
| `GET /items` | `200 OK` (even if the list is empty) | `401` not authenticated, `403` not allowed |
| `GET /items/9` | `200 OK` | `404 Not Found` if no such item |
| `POST /items` | `201 Created`, often with a `Location` header pointing to the new item | `400` malformed body, `422` valid format but invalid content, `409` conflict (duplicate) |
| `PUT /items/9` | `200 OK` (or `204 No Content`) | `404`, `400`, `422`, `409` |
| `PATCH /items/9` | `200 OK` | `404`, `400`, `422` |
| `DELETE /items/9` | `200 OK` or `204 No Content` | `404` if already gone (documentation should say), `403` |
| Any | | `429 Too Many Requests` (rate limited), `500` server bug, `503` unavailable |

A few details matter for testers. `400` generally means the request itself is unreadable or malformed. `422 Unprocessable Content` means the request is well formed but its content breaks a rule (for example, an email without an `@`). Not every API distinguishes them, so follow the documentation. `401` means "I do not know who you are" (missing or bad credentials), whereas `403` means "I know who you are, but you are not allowed." `404` is returned for a missing resource, and a well-designed API also does not leak whether a forbidden resource exists. A response of `200` with an error message in the body (`{"success": false}`) is a design flaw, because it hides the failure from every tool that reads the status code. We will practise validating status codes in code on Tuesday.

### 11. HATEOAS and the Richardson Maturity Model (Awareness)

Two terms you will meet in interviews and documentation deserve a short introduction. You do not need to master them this week.

**HATEOAS** stands for *Hypermedia As The Engine Of Application State*. It is the part of the uniform interface constraint that says responses should include links telling the client what it can do next, much like a web page contains links. For example:

```json
{
  "id": 7,
  "status": "pending",
  "_links": {
    "self":   { "href": "/orders/7" },
    "cancel": { "href": "/orders/7/cancellation" },
    "items":  { "href": "/orders/7/items" }
  }
}
```

The `_links` object lists the related actions and where to find them. A client following HATEOAS does not need to build URLs by itself; it follows links. In practice, many "REST" APIs do not implement HATEOAS, and it is perfectly normal to encounter APIs that skip it. If an API does include links, a tester should verify that every link actually works and that links change appropriately with state (a shipped order should not offer a `cancel` link).

The **Richardson Maturity Model** grades how fully an API uses REST ideas, in four levels:

| Level | Description | Example |
|-------|-------------|---------|
| 0 | One URL, one method; everything is tunnelled through it (like a remote procedure call) | `POST /api` with an action name in the body |
| 1 | Separate **resources**, each with its own URL | `/orders`, `/customers` |
| 2 | Resources plus proper **HTTP methods and status codes** | `GET /orders/7`, `DELETE /orders/7` returning `204` |
| 3 | Level 2 plus **hypermedia controls** (HATEOAS) | Responses include `_links` |

Most real-world APIs that people call RESTful sit at Level 2, and that is the level you will test most. The model is useful as vocabulary: it helps you describe how an API deviates from REST and what you should expect from it.

### 12. Pagination, Filtering, and Sorting (Awareness)

A collection can be huge. A real shop could have ten million orders, and no server wants to send all of them in one response. REST APIs therefore provide ways to ask for part of a collection. At this stage you only need to recognise the three ideas. Query parameters, which carry them, get a full lesson later today (**Query parameters and path variables**).

**Pagination** means asking for the collection one page at a time. Typical forms are `GET /orders?page=2&limit=20` (page-based) or `GET /orders?offset=40&limit=20` (offset-based) or a cursor token (`?after=abc123`). The response may also tell you the total number of items or provide a link to the next page.

**Filtering** means asking only for items that match a condition, such as `GET /orders?status=shipped`. **Sorting** means ordering results, such as `GET /orders?sort=createdAt&order=desc`.

*Testing implications at a glance:* the first page, the last page, a page beyond the end, a page size of zero, a negative page number, and a huge page size are all classic boundary tests. Also test that sorting is stable and that filters can combine. We will explore these in detail in the query parameters lesson, so for now, simply be able to recognise them in a URL.

### 13. API Documentation and OpenAPI / Swagger

For other people (and test tools) to use an API, it must be described somewhere. This description is the **API documentation**. The most widely used standard format is the **OpenAPI Specification** (OAS), formerly known as **Swagger**. An OpenAPI document is a machine-readable file, written in YAML or JSON, that lists every path, every method, the parameters each accepts, the shape of request bodies, and the possible responses. Tools read these files to generate interactive documentation pages (often called Swagger UI), to generate client code, and to generate test cases or mock servers. Postman can import an OpenAPI file and build a collection of requests from it.

For a tester the specification is a primary source of **expected behaviour**. When the real API disagrees with its documentation, you have found a bug in the API or a defect in the documentation, and either deserves a report.

Here is a small excerpt, written in YAML, describing one endpoint of an imaginary bookshop API:

```yaml
openapi: 3.0.3
info:
  title: Bookshop API
  version: 1.0.0
servers:
  - url: https://api.bookshop.example.com/v1
paths:
  /books/{bookId}:
    get:
      summary: Get one book
      parameters:
        - name: bookId
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: The book was found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Book'
        '404':
          description: No book with that ID
components:
  schemas:
    Book:
      type: object
      required: [id, title]
      properties:
        id:
          type: integer
        title:
          type: string
        year:
          type: integer
        inStock:
          type: boolean
```

Here is what each part means. `openapi: 3.0.3` states which version of the specification this file follows. The `info` block gives the API's human-readable title and its own version number, `1.0.0`. The `servers` list contains the **base URL**; each path in the document is appended to it. The `paths` section is the heart of the file. The entry `/books/{bookId}` describes a URL in which `{bookId}` is a placeholder, a **path variable**. Beneath it, `get:` tells us this documents the `GET` method for that path, and `summary` is a short human description. The `parameters` list describes inputs: this one is called `bookId`, it is located `in: path` (it is part of the URL, as opposed to the query string or a header), it is `required: true` (a request without it is invalid), and its `schema` says its `type` must be an `integer`. The `responses` section lists outcomes by status code. Code `'200'` has a description and a `content` block saying the body is `application/json` and that its schema is found by following the reference (`$ref`) to `#/components/schemas/Book`, which is defined lower in the file. Code `'404'` says what happens when no such book exists. In the `components` section, the `Book` schema defines an object with four properties, each with a type, and says that `id` and `title` are `required`, while `year` and `inStock` are optional.

Now read it like a tester. From this excerpt alone you can derive at least these tests: a valid ID returns `200` and a body that matches the `Book` schema; an unknown ID such as `999999` returns `404`; a text ID such as `abc` should not be accepted (the schema says integer), and the documentation does not say what code to expect, which is itself a question to raise with the team; a negative or zero ID is a boundary; `id` and `title` must always be present; `year`, if present, must be an integer; and `inStock` must be a real boolean, not the string `"true"`. A well-read specification turns directly into a test list, and later this week you will write code that checks responses against a schema.

### 14. REST Versus SOAP, GraphQL, and gRPC

REST is the most common style, but not the only one. Knowing the alternatives helps you recognise them on the job and answer interview questions. The skills you learn this week (HTTP, JSON, status codes, headers, authentication) transfer to all of them.

| Aspect | REST | SOAP | GraphQL | gRPC |
|--------|------|------|---------|------|
| **What it is** | Architectural style over HTTP | Protocol with strict standards | Query language and runtime for APIs | High-performance remote procedure call framework |
| **Data format** | Mostly JSON (also XML, others) | XML only (the "envelope") | JSON | Binary (Protocol Buffers) |
| **Endpoints** | Many URLs, one per resource | Usually a single URL | Usually a single URL | Service methods defined in a `.proto` file |
| **Methods used** | GET, POST, PUT, PATCH, DELETE | Almost always POST | POST (queries and mutations in the body) | HTTP/2 streaming calls |
| **Contract** | Optional (OpenAPI) | Required (WSDL) | Required (schema) | Required (`.proto`) |
| **Caching** | Easy, uses HTTP caching | Difficult | Harder, needs extra tooling | Not HTTP-cache based |
| **Typical use** | Public and mobile-facing web APIs | Banking, telecom, legacy enterprise systems | Front-ends that need flexible data shapes | Fast internal service-to-service calls |
| **Main strength** | Simple, widely understood | Strong standards, built-in security features | Client chooses exact fields, fewer round trips | Speed, strict typing, streaming |
| **Main weakness** | Over-fetching and under-fetching | Verbose and heavy | Complex caching and error handling | Not human-readable, limited browser support |

Briefly, **SOAP** (Simple Object Access Protocol) wraps every message in an XML envelope and is defined by a rigid contract called WSDL. You will meet it in older banking and enterprise systems. **GraphQL**, created at Facebook, exposes one endpoint where the client describes exactly the fields it wants, which avoids sending too much (over-fetching) or too little (under-fetching) data. **gRPC**, created at Google, is used for fast communication between internal services using a compact binary format. For a tester, SOAP means building XML requests, GraphQL means writing queries and watching for a `200` that still contains an `errors` array, and gRPC needs special tools. We focus on REST in this course because it is the most common in the industry, and because the HTTP skills carry over.

### 15. Guided Exploration of JSONPlaceholder with curl

Now let us treat **JSONPlaceholder** (`https://jsonplaceholder.typicode.com`) as if it were the system under test. It is a free, public, fake REST API. "Fake" means that it accepts write requests and replies as though they worked, but it does not actually save anything. That is ideal for learning because nothing you do can break it, and everyone sees the same data.

**What is curl?** `curl` is a command-line program that sends HTTP requests and shows the responses. It is available on most operating systems (macOS, Linux, and recent Windows). Today you will use it to see the raw mechanics before Postman gives you a friendlier interface. The flags we use are:

| Flag | Meaning |
|------|---------|
| `-i` | Include the response status line and headers in the output |
| `-X METHOD` | Choose the HTTP method (default is GET) |
| `-H "Name: value"` | Add a request header |
| `-d 'data'` | Send a request body (this also makes the default method POST) |
| `-s` | Silent mode; hides the progress meter |

**A note on output.** Responses below are shortened where they are long, and the exact whitespace may differ. On Windows Command Prompt, single quotes do not work for the JSON body; use double quotes and escape inner ones, or use PowerShell or Git Bash.

#### The six resource families

JSONPlaceholder exposes six resources, and knowing their sizes lets you predict what you will see:

| Resource | Count | Describes | Key fields |
|----------|-------|-----------|------------|
| `/posts` | 100 | Blog posts | `userId`, `id`, `title`, `body` |
| `/comments` | 500 | Comments on posts | `postId`, `id`, `name`, `email`, `body` |
| `/albums` | 100 | Photo albums | `userId`, `id`, `title` |
| `/photos` | 5000 | Photos in albums | `albumId`, `id`, `title`, `url`, `thumbnailUrl` |
| `/todos` | 200 | To-do items | `userId`, `id`, `title`, `completed` |
| `/users` | 10 | Users | `id`, `name`, `username`, `email`, `address`, `phone`, `website`, `company` |

The relationships are: a user has many posts, albums, and todos; a post has many comments; an album has many photos. These relationships explain the nested routes.

#### Step 1: Read a collection

```bash
curl -s https://jsonplaceholder.typicode.com/posts
```

This asks for the `posts` collection. Expected output is a JSON **array** of 100 objects, which begins like this:

```json
[
  {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur ..."
  },
  {
    "userId": 1,
    "id": 2,
    "title": "qui est esse",
    "body": "est rerum tempore vitae\nsequi sint nihil ..."
  }
]
```

The outer brackets show it is an array. Each element is a post object with `userId` (the author), `id` (the post's own ID), `title`, and `body`. The text is meaningless "lorem ipsum"-style filler, which is deliberate. Note the `\n` inside the body: that is how JSON writes a line break inside a string.

#### Step 2: Read one resource

```bash
curl -s https://jsonplaceholder.typicode.com/posts/1
```

Adding `/1` selects the post whose `id` is 1. The output is a single JSON **object**, not an array:

```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur ..."
}
```

Compare this with Step 1: the same fields, but without the outer array. A test must know which of the two shapes to expect.

#### Step 3: Read a resource that does not exist

```bash
curl -i https://jsonplaceholder.typicode.com/posts/99999
```

The `-i` flag shows the status line and headers. The first line of the output is `HTTP/2 404` (or `HTTP/1.1 404 Not Found`), followed by headers, and the body is an empty object `{}`. This is how this API tells you that no such resource exists. In a real application, a more informative error message in the body would be better, and you would note this as an observation.

#### Step 4: Read a sub-collection (nested route)

```bash
curl -s https://jsonplaceholder.typicode.com/posts/1/comments
```

This reads the comments that belong to post 1. Expected output is an array of 5 comment objects, each with `postId` equal to `1`:

```json
[
  {
    "postId": 1,
    "id": 1,
    "name": "id labore ex et quam laborum",
    "email": "Eliseo@gardner.biz",
    "body": "laudantium enim quasi est quidem magnam voluptate ..."
  }
]
```

The shortened sample shows only the first element. Every comment's `postId` should be `1`, which is a good property to assert in a test.

#### Step 5: Compare nested and direct access

```bash
curl -s https://jsonplaceholder.typicode.com/comments/1
curl -s "https://jsonplaceholder.typicode.com/comments?postId=1"
```

The first call reads a single comment directly by its own ID. The second uses a **query parameter** to filter the whole comments collection and returns the same five comments as Step 4. (Quote the URL when it contains `?` so the shell does not misinterpret the character.) This shows that there is often more than one way to reach the same data: a nested path or a filter. A tester should confirm both give consistent results.

#### Step 6: The other families

```bash
curl -s https://jsonplaceholder.typicode.com/users/1
curl -s https://jsonplaceholder.typicode.com/todos/1
curl -s https://jsonplaceholder.typicode.com/albums/1
curl -s https://jsonplaceholder.typicode.com/albums/1/photos
curl -s https://jsonplaceholder.typicode.com/users/1/todos
```

The first returns user 1, an object with nested data. Expected output begins:

```json
{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "address": {
    "street": "Kulas Light",
    "suite": "Apt. 556",
    "city": "Gwenborough",
    "zipcode": "92998-3874",
    "geo": { "lat": "-37.3159", "lng": "81.1496" }
  },
  "phone": "1-770-736-8031 x56442",
  "website": "hildegard.org",
  "company": { "name": "Romaguera-Crona", "catchPhrase": "...", "bs": "..." }
}
```

This is the best example of a rich object, with nested `address`, `geo`, and `company` objects. The second call returns a todo, expected to look like `{"userId": 1, "id": 1, "title": "delectus aut autem", "completed": false}`; note the **boolean** `completed`. The third returns an album with `userId`, `id`, and `title`. The fourth returns the photos of album 1, an array of 50 objects with `albumId`, `id`, `title`, `url`, and `thumbnailUrl`. The fifth returns the todos belonging to user 1, an array of 20 objects. Photo URLs and image hosts used by the service can change over time, so assert on structure and types rather than exact image URLs.

#### Step 7: Filtering and counting

```bash
curl -s "https://jsonplaceholder.typicode.com/posts?userId=1"
curl -s "https://jsonplaceholder.typicode.com/todos?completed=true"
```

The first returns only the 10 posts written by user 1. The second returns only the completed todos. These are examples of **filtering** with query parameters, which you will study in detail later today. Note that the filter is a request for part of a collection, and the response is still an array.

#### Step 8: Create a resource

```bash
curl -i -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"QEA training","body":"Learning REST","userId":1}'
```

Explanation of each part: `-i` shows the status line and headers; `-X POST` selects the POST method; the URL is the collection to add to; the backslash at the end of a line simply continues the command on the next line; `-H` sets the `Content-Type` header to tell the server that the body is JSON; and `-d` supplies the body. The expected response begins with `HTTP/2 201` (Created) and a body such as:

```json
{
  "title": "QEA training",
  "body": "Learning REST",
  "userId": 1,
  "id": 101
}
```

The server echoes what you sent and adds a new `id`, `101`, because the collection already holds 100 posts. **Important:** because this is a fake API, if you now request `GET /posts/101` you will receive `404`. The record was never actually stored. This is a useful reminder that in a real system you must always verify a create by reading the resource back, which is how you detect an API that claims success without saving.

#### Step 9: Replace and update a resource

```bash
curl -i -X PUT https://jsonplaceholder.typicode.com/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"id":1,"title":"Updated title","body":"Updated body","userId":1}'

curl -i -X PATCH https://jsonplaceholder.typicode.com/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Only the title changes"}'
```

The first command replaces post 1 entirely with the body provided, and the second changes only the `title` field. Both return `200 OK` and echo the resulting object. For `PATCH`, the response shows the full post with the new title merged in; for `PUT`, you get back exactly what you sent. Again, nothing is really stored.

#### Step 10: Delete a resource

```bash
curl -i -X DELETE https://jsonplaceholder.typicode.com/posts/1
```

Expected output is `HTTP/2 200` and a body of `{}`. A real API might return `204 No Content` with no body at all. Neither is wrong by itself, as long as it matches the documentation. The post will still exist if you read it again, because the API is fake.

#### What you should observe overall

By now you should have noticed the patterns: collections return arrays and single resources return objects; the same URL does different things with different methods; nested routes show relationships; query parameters filter; `404` is returned for a non-existent ID; and `201` is returned on creation. These patterns are what REST predicts, and the remainder of the week builds on them.

### 16. Thinking Like a Tester About a REST API

For any endpoint, ask questions in several categories. Keep this checklist; you will use it every day this week. It is organised by the kind of endpoint, because different operations call for different ideas.

#### A. Reading a single resource: `GET /resources/{id}`

The functional checks are: a valid ID returns `200` and the correct record; the fields match the documentation in name, type, and format; the ID in the body equals the ID in the URL; nested objects have their expected structure. The negative and boundary checks are: a non-existent ID returns `404`; an ID of `0`, a negative number, a very large number, a decimal, text, and special characters in the ID each return a controlled `4xx` response and never a `500`; a deleted resource returns `404`. The security checks are: no credentials returns `401`; another user's resource returns `403` or `404`; sensitive fields such as passwords or internal flags never appear. The non-functional checks are: the response time is acceptable and the `Content-Type` is `application/json`.

#### B. Reading a collection: `GET /resources`

Check that the response is an array; that it is an empty array (not an error, not `null`) when there are no items; that the count matches the expected data; that every element has the same structure; that IDs are unique; that default ordering is documented and stable; that pagination works and the last page behaves; that filters and sorting return exactly the right subset; that very large collections do not exhaust the server (a limit is enforced); and that unauthorised callers are refused.

#### C. Creating: `POST /resources`

Check that a valid body returns `201` with the new resource, and a `Location` header if documented; that a follow-up `GET` returns the same data (a read-back proof); that the server generates the `id` and ignores or rejects a client-supplied one; that required fields missing one at a time each cause a `4xx` with a clear message; that wrong data types, empty strings, `null`, overly long values, special characters, Unicode, and HTML or SQL-like text are handled safely; that malformed JSON returns `400`; that a wrong `Content-Type` is rejected (typically `415`); that duplicates are handled (`409` or documented behaviour); that sending the same request twice behaves as documented; and that no credentials means `401`.

#### D. Replacing and updating: `PUT` and `PATCH /resources/{id}`

Check that the changes persist and a `GET` confirms them; that unchanged fields remain unchanged after a `PATCH`; that a `PUT` that omits a field behaves as documented (reset to default or rejected); that read-only fields such as `id` and `createdAt` cannot be changed; that updating a non-existent ID gives `404`; that the same `PUT` repeated yields the same state (idempotency); that invalid values are rejected without changing the stored data; and that a user cannot update another user's resource.

#### E. Deleting: `DELETE /resources/{id}`

Check that the correct success code is returned; that a follow-up `GET` returns `404`; that deleting again returns the documented result (`404` or `204`); that related data is handled properly (deleting a customer with orders is either blocked or cascaded, as documented); that only authorised callers may delete; and that the collection count decreases by exactly one.

#### F. Cross-cutting checks (every endpoint)

Check consistency of error format; correct `Content-Type`; no stack traces or server details in errors; rate limiting behaviour; HTTPS enforcement; behaviour with extra unexpected fields; behaviour with very large bodies; and that responses conform to the documented schema.

The golden rule is that a `500 Internal Server Error` in response to *any* client input is a defect. Bad input is the client's mistake and should be answered with a `4xx`; only the server's own failure should produce a `5xx`.

### 17. Worked Real-World Scenarios

The best way to learn is to apply the ideas to realistic systems. Each scenario below describes an API, then walks through the resources, URLs, and the tests you would think of.

#### Scenario 1: Online shop

*The system.* A shop exposes `/products`, `/customers`, `/orders`, and `/orders/{id}/items`.

*Resource thinking.* `products` and `customers` are top-level collections. An order belongs to a customer and has line items, so `/orders/7/items` is a sub-collection of order 7. Creating an order is `POST /orders` with a body such as:

```json
{
  "customerId": 42,
  "items": [
    { "productId": 5, "quantity": 2 },
    { "productId": 9, "quantity": 1 }
  ]
}
```

This body is an object containing a number (`customerId`) and an array of objects (`items`), where each element has a product reference and a quantity. Explanation: the server should respond `201`, create an order ID, calculate prices on its own, and set the status to `pending`.

*Test ideas.* Quantity `0`, negative, or huge; a non-existent `productId` (expect a `4xx`, not `500`); an out-of-stock product (expect a clear business-rule error); an empty `items` array; the server must calculate the total itself and ignore any `total` sent by the client; two identical `POST` requests should not accidentally charge twice if the documentation promises protection (idempotency keys); a customer must not be able to read another customer's `/orders/{id}`; the order's total must equal the sum of its item prices.

#### Scenario 2: Library system

*The system.* Resources are `/books`, `/members`, and `/loans`. Borrowing a book is modelled as creating a loan: `POST /loans` with `{"memberId": 3, "bookId": 12}`. Returning it is `PATCH /loans/55` with `{"status": "returned"}`.

*Resource thinking.* Notice that "borrow" is not a verb in the URL; it is the creation of a *loan* resource. This noun-first thinking is a core REST skill.

*Test ideas.* Borrowing a book that is already on loan should be refused (`409 Conflict`); a member with overdue books or at their loan limit should be refused; returning a book twice; borrowing with a non-existent member; a loan's due date must be after its start date; the book's availability shown in `GET /books/12` must change after the loan and change back after return (this is state consistency across resources).

#### Scenario 3: Banking

*The system.* Resources are `/accounts`, `/accounts/{id}/transactions`, and `/transfers`. A transfer is `POST /transfers` with `{"fromAccount": "A1", "toAccount": "B2", "amount": 100.00}`.

*Resource thinking.* Money requires stricter rules than most domains. Transfers are created, not edited; transactions are an append-only history.

*Test ideas.* Amounts of `0`, negative, `0.001` (too many decimals), and huge values; a transfer exceeding the balance (expect a refusal and *no* change to either account); sending to the same account; a transfer between non-existent accounts; the two balances after a transfer must differ by exactly the amount, and their sum must be unchanged; sending the same transfer twice quickly must not move money twice; the account must not be readable by other users; there should be no `PUT` or `DELETE` on a completed transaction (expect `405 Method Not Allowed`); a decimal amount should be a number, never a floating-point string that rounds unexpectedly.

#### Scenario 4: Ride-sharing

*The system.* Resources are `/riders`, `/drivers`, `/rides`, and `/rides/{id}/location`. A ride moves through states: `requested`, `accepted`, `in-progress`, `completed`, `cancelled`.

*Resource thinking.* A ride is a resource with a **state machine**. REST handles this by updating a `status` field or by creating sub-resources, for example `POST /rides/88/cancellation`.

*Test ideas.* Valid transitions succeed (`requested` to `accepted`); invalid transitions are refused (`completed` back to `requested`; cancelling a completed ride); a driver cannot accept a ride that another driver already accepted; coordinates have boundaries (latitude between -90 and 90, longitude between -180 and 180); a rider cannot request two simultaneous rides if the rules forbid it; the fare must be calculated server-side; the location sub-resource should update quickly and reject stale data; and a rider should see only their own rides.

#### Scenario 5: Social media posts

*The system.* This is the world that JSONPlaceholder imitates: `/users`, `/posts`, `/posts/{id}/comments`.

*Test ideas.* Every comment's `postId` must match the post it is listed under (this is exactly Step 4 above); the `userId` of a new post must refer to a real user; a post with an empty `title` should be rejected; very long bodies and emoji must be handled; deleting a post should handle its comments (removed or orphaned, as documented); and an edit should not change the author.

#### Scenario 6: Hotel booking (shows date logic)

*The system.* `/rooms`, `/bookings`. `POST /bookings` takes `{"roomId": 4, "checkIn": "2026-12-01", "checkOut": "2026-12-05"}`.

*Test ideas.* Check-out before check-in; same-day stay; a date in the past; an invalid date such as `2026-02-30`; wrong date format; overlapping bookings for the same room (expect `409`); and a booking made at the same instant by two clients. Dates are a rich source of defects, and an API test is the fastest way to find them.

### 18. Common Mistakes

Learners and teams frequently make the following mistakes when starting with REST APIs.

**Treating REST as a standard rather than a style.** There is no single "REST rulebook," and different teams make different choices. Always read the documentation and observe the API's actual behaviour before assuming.

**Using verbs in URLs and the wrong methods.** Designs such as `GET /deleteUser?id=5` are dangerous: web crawlers and caches treat `GET` as safe, so a crawler might delete data. Testers should flag any state change performed through `GET`.

**Testing only the happy path.** A suite that only checks `200 OK` on valid input catches very few real bugs. The valuable defects hide in validation, state, security, and boundaries.

**Checking only the status code.** A `200` with the wrong body is still a bug. Verify the body, headers, and the effect on stored data as well.

**Not reading back after a write.** Always follow a `POST`, `PUT`, `PATCH`, or `DELETE` with a `GET` to prove the change really happened.

**Confusing 401 and 403, or 400 and 422.** Know what each means, and check what the documentation promises.

**Assuming order of fields or order of array items.** JSON objects are unordered, so a test must not depend on field order. Array order may matter only if the API documents an ordering.

**Hard-coding the base URL and IDs everywhere.** This makes tests impossible to move between environments. Use variables (the Postman variables lesson will teach this today).

**Believing the fake API is real.** JSONPlaceholder does not persist data. If you expect your created post to appear later, you will wrongly conclude the API is broken.

**Sending malformed JSON by accident.** Single quotes, trailing commas, and unescaped quotes are the usual causes; validate your body first.

**Ignoring `Content-Type`.** Without `Content-Type: application/json`, many servers will not parse your body, and you will see confusing errors.

### 19. Practice Exercises With Worked Solutions

Try each exercise yourself before reading the solution. Exercises 6 and 8 use a terminal with `curl`; the others can be done on paper.

#### Exercise 1: Identify the parts of a URL

*Task.* In `https://api.shop.example.com/v2/orders/17/items?sort=price&order=desc`, identify the scheme, host, base URL (assume it includes the version), the collection, the resource ID, the sub-collection, and the query string.

*Solution.* The scheme is `https`. The host is `api.shop.example.com`. The base URL is `https://api.shop.example.com/v2`, because the version is part of the shared prefix. The first collection is `orders`; `17` is the ID of one order, so `/orders/17` is a single resource. `items` is a sub-collection belonging to order 17. The query string is `sort=price&order=desc`, which sorts the items by price in descending order. Reading it as a sentence: "give me the items of order 17, sorted by price, highest first."

#### Exercise 2: Fix the URL design

*Task.* Rewrite each of these in a RESTful style: (a) `POST /createNewCustomer`, (b) `GET /getOrderById?id=9`, (c) `POST /deleteProduct/5`, (d) `GET /Customer_Orders/42`, (e) `GET /shippedOrders`.

*Solution.* (a) `POST /customers`: a noun, plural, and the method supplies "create." (b) `GET /orders/9`: the ID goes in the path. (c) `DELETE /products/5`: use the `DELETE` method rather than a verb on a `POST`. (d) `GET /customers/42/orders`: lowercase, plural, and nested to show ownership. (e) `GET /orders?status=shipped`: a filter belongs in a query parameter, not a new collection.

#### Exercise 3: Map operations to methods

*Task.* For a library API, write the method and URL for: list all books; get book 8; add a new book; change only the title of book 8; replace book 8 completely; remove book 8; list the loans of member 3.

*Solution.* `GET /books`; `GET /books/8`; `POST /books` with a JSON body; `PATCH /books/8` with `{"title": "New title"}`; `PUT /books/8` with a complete book body; `DELETE /books/8`; `GET /members/3/loans`. Note that `PATCH` changes part of the resource and `PUT` supplies a complete replacement.

#### Exercise 4: Write JSON

*Task.* Write one JSON document describing a book with: a title (string), a year (number), whether it is available (boolean), a list of authors (array of strings), a publisher with a name and a city (nested object), and a series that is not applicable (null).

*Solution.*

```json
{
  "title": "Clean Code",
  "year": 2008,
  "available": true,
  "authors": ["Robert C. Martin"],
  "publisher": { "name": "Prentice Hall", "city": "Upper Saddle River" },
  "series": null
}
```

Explanation: the root is an object. The `title` is a string in double quotes, `year` is a bare number, `available` is the boolean `true` (no quotes), `authors` is an array even though there is only one author (the shape stays consistent if more are added), `publisher` is a nested object, and `series` is `null`, indicating the field exists but has no value. There is no trailing comma after the last pair.

#### Exercise 5: Debug the JSON

*Task.* Find and fix all the errors:

```json
{
  'id': 7,
  title: "REST in Practice",
  "price": 29.99,
  "tags": ["api", "rest",],
  "inStock": True,
  "notes": "Called "essential" by readers"
}
```

*Solution.* There are five errors. The key `'id'` uses single quotes; it must be `"id"`. The key `title` has no quotes; it must be `"title"`. The array has a trailing comma after `"rest"`; remove it. The value `True` is Python style; JSON requires lowercase `true`. The inner quotes in `"essential"` terminate the string early; they must be escaped as `\"essential\"`. The corrected document is:

```json
{
  "id": 7,
  "title": "REST in Practice",
  "price": 29.99,
  "tags": ["api", "rest"],
  "inStock": true,
  "notes": "Called \"essential\" by readers"
}
```

#### Exercise 6: Explore with curl

*Task.* Using `curl`, find out: (a) how many todos belong to user 3; (b) the title of post 5; (c) the email of the first comment of post 7; (d) the status code returned for `/users/11`.

*Solution.* (a) Run `curl -s "https://jsonplaceholder.typicode.com/todos?userId=3"` or `curl -s https://jsonplaceholder.typicode.com/users/3/todos` and count the objects; there are 20. (b) Run `curl -s https://jsonplaceholder.typicode.com/posts/5` and read the `title` field. (c) Run `curl -s https://jsonplaceholder.typicode.com/posts/7/comments` and read the `email` of the first array element. (d) Run `curl -i https://jsonplaceholder.typicode.com/users/11`; there are only 10 users, so the status line shows `404`. If you have the `jq` tool installed you can count with `curl -s ... | jq length`, but counting by eye or in an editor works as well.

#### Exercise 7: Derive tests from an OpenAPI excerpt

*Task.* Given this excerpt, list at least eight tests.

```yaml
/products/{id}:
  delete:
    parameters:
      - name: id
        in: path
        required: true
        schema: { type: integer, minimum: 1 }
    responses:
      '204': { description: Deleted }
      '404': { description: Not found }
      '403': { description: Not allowed }
```

*Solution.* The excerpt documents a `DELETE` on a product with an integer path variable that must be at least 1, and three outcomes. Possible tests: (1) delete an existing product as an authorised user and expect `204`; (2) read the product afterwards and expect `404`; (3) delete the same product again and expect `404`; (4) delete a non-existent ID such as `999999` and expect `404`; (5) delete as an unauthorised user and expect `403` and confirm the product still exists; (6) send `id` as `0` (below the minimum) and expect a `4xx`; (7) send a negative ID; (8) send a text ID such as `abc` and expect a `4xx`, not `500`; (9) send a decimal such as `1.5`; (10) delete a product that is part of an existing order and verify the documented behaviour, noting that the excerpt does not define it, so raise a question; (11) check that the collection count decreases by exactly one. The last two show how a tester also finds gaps in the specification.

#### Exercise 8: Predict, then verify

*Task.* Before running the command, predict the status code and the shape of the body (object, array, or empty), then run it and compare: (a) `GET /posts/1/comments`, (b) `GET /posts/0`, (c) `POST /todos` with `{"title":"test","completed":false,"userId":1}`, (d) `DELETE /comments/3`, (e) `GET /photos?albumId=2`.

*Solution.* (a) `200`, an array of 5 comment objects. (b) `404`, an empty object `{}`, since there is no post with ID 0. (c) `201`, an object echoing your data with `id` 201, because there are 200 todos. (d) `200`, an empty object `{}`. (e) `200`, an array of 50 photo objects, all with `albumId` equal to 2. Run them with `curl -i` for the first lines of output. If any result surprised you, write down why; the difference between your prediction and reality is where learning happens.

#### Exercise 9: Design the resources

*Task.* A gym wants an API for classes, trainers, and member bookings. Propose resources, URLs, methods, and the JSON for booking a class. Then list six tests.

*Solution.* Resources: `/classes`, `/trainers`, `/members`, and `/bookings`. Methods: `GET /classes` lists classes; `GET /classes/5` reads one; `GET /trainers/2/classes` lists the classes a trainer teaches; `POST /bookings` books a place; `DELETE /bookings/31` cancels a booking; `GET /members/8/bookings` lists a member's bookings. The booking body might be `{"memberId": 8, "classId": 5}`. Six tests: a valid booking returns `201`; booking a full class returns `409`; booking the same class twice for the same member returns `409`; a non-existent class returns `404` or `422` as documented; cancelling returns success and frees a place (check the class's remaining capacity increases by one); and one member cannot cancel another member's booking (`403`).

#### Exercise 10: Spot the REST violations

*Task.* Identify what is wrong with each design: (a) `GET /api/deleteUser/5`, (b) an API that returns `200` with `{"success": false, "error": "not found"}`, (c) an API that works only if you first call `/login` and then call other endpoints from the same IP address without sending any token, (d) one endpoint returns `{"error": "bad"}` while another returns `{"message": "bad"}`.

*Solution.* (a) A verb in the URL and a state change through `GET`, which is supposed to be safe; it should be `DELETE /users/5`. (b) The status code hides the failure; it should be `404`. (c) It violates statelessness: the server is remembering the client between requests, which makes tests order-dependent. Credentials should travel with each request. (d) It violates the uniform-interface idea of consistency; errors should share one structure.

### 20. Self-Check Quiz

Answer these without looking back, then compare with the answers.

1. What does API stand for, and what does the word "interface" tell you?
2. Who defined REST, and in what kind of document?
3. Name the six REST constraints.
4. Which constraint explains why a token must be sent with every request?
5. In `/customers/42/orders/7`, which parts are collections and which are IDs?
6. Why is `POST /createOrder` considered poor design?
7. Which versioning strategy puts the version in the URL path? Give an example.
8. Which HTTP method normally maps to Create, and what is its usual success code?
9. Name the six JSON data types.
10. Why is `{ "active": True }` invalid JSON?
11. What is the difference between `401` and `403`?
12. Why is `200 OK` with `{"error": "not found"}` a design flaw?
13. In the Richardson Maturity Model, which level introduces proper HTTP methods and status codes?
14. What does HATEOAS add to a response?
15. In an OpenAPI file, what does `in: path` mean for a parameter?
16. Which API style uses a single endpoint and lets the client choose the fields it receives?
17. Why does a `POST` to JSONPlaceholder not appear when you `GET` it afterwards?
18. If a client sends malformed JSON and the server crashes with `500`, is that a defect? Why?

**Answers.**

1. Application Programming Interface. "Interface" means a defined boundary and contract between two pieces of software, so the caller does not need to know the internals.
2. Roy Fielding, in his year 2000 doctoral dissertation.
3. Client-server, stateless, cacheable, uniform interface, layered system, code on demand (optional).
4. Statelessness: each request must carry everything the server needs, including authentication.
5. `customers` and `orders` are collections; `42` and `7` are IDs of single resources.
6. It puts a verb in the URL. The HTTP method already says "create," so the URL should be `POST /orders`.
7. URL path versioning, such as `/v1/users`.
8. `POST`, normally returning `201 Created`.
9. Object, array, string, number, boolean, null.
10. JSON literals are lowercase: `true`, `false`, `null`. `True` is Python syntax.
11. `401` means the caller is not authenticated (unknown identity); `403` means the caller is known but not permitted.
12. It hides failure from any tool or client that relies on status codes, and it breaks the principle that the status code carries the outcome.
13. Level 2.
14. Hypermedia links that tell the client what related actions and resources are available.
15. The parameter is part of the URL path, such as the `{bookId}` in `/books/{bookId}`.
16. GraphQL.
17. JSONPlaceholder is a fake API: it accepts and echoes writes but does not persist them.
18. Yes. Bad client input should produce a `4xx` (here, `400`). A `500` indicates the server failed to handle an expected kind of error, which is a robustness defect.

### 21. Glossary

**API (Application Programming Interface):** A defined contract that lets one piece of software use the services of another.

**Web API:** An API accessed over a network using HTTP.

**REST (REpresentational State Transfer):** An architectural style for designing web APIs around resources, standard methods, and stateless messages.

**RESTful:** Describes an API that follows REST principles.

**Resource:** A thing with an identity that the API exposes, such as a user or an order.

**Collection:** A group of resources of the same type, such as `/users`.

**Sub-resource (nested resource):** A resource that belongs to another resource, such as `/posts/1/comments`.

**Endpoint:** A specific URL (with its HTTP method) at which the API can be called.

**Base URL:** The common prefix shared by all endpoints of an API.

**Path variable:** A changing part of the URL path that identifies a resource, such as `42` in `/users/42`.

**Query string:** The part of a URL after `?` that carries optional parameters.

**Representation:** A snapshot of a resource's state in an agreed format such as JSON.

**CRUD:** Create, Read, Update, Delete; the four basic data operations.

**Safe method:** A method that does not change server data (for example, `GET`).

**Idempotent method:** A method where repeating the same request leaves the server in the same state as sending it once.

**JSON:** JavaScript Object Notation, a text format built from objects, arrays, strings, numbers, booleans, and null.

**Stateless:** Each request carries everything needed; the server keeps no memory of earlier requests.

**Cache:** A stored copy of a response that can be reused.

**HATEOAS:** Hypermedia As The Engine Of Application State; responses include links to related actions.

**Richardson Maturity Model:** A four-level scale (0 to 3) for how fully an API uses REST ideas.

**Pagination:** Retrieving a collection in pages.

**Filtering:** Requesting only the items that match a condition.

**Versioning:** Labelling the API contract so that old clients keep working as it evolves.

**Breaking change:** A change that can make existing clients fail.

**OpenAPI / Swagger:** A standard, machine-readable format for describing REST APIs.

**Schema:** A formal description of the structure and types of a JSON document.

**SOAP:** An XML-based protocol with strict contracts, common in older enterprise systems.

**GraphQL:** A query language where the client specifies exactly which fields it wants.

**gRPC:** A high-performance, binary remote procedure call framework.

**Test pyramid:** A guideline recommending many unit tests, fewer API tests, and few UI tests.

**curl:** A command-line tool for sending HTTP requests.

**Mock / fake API:** A service that imitates a real API for practice or testing, such as JSONPlaceholder.

---

## Summary

- An **API** is a defined contract that lets software talk to other software; a **web API** does so over HTTP, and it is the layer where most business rules can be tested quickly and reliably.
- The **test pyramid** recommends many unit tests, a solid layer of API tests, and a few UI tests. API testing is the sweet spot of speed, stability, and coverage.
- **REST** is an architectural style described by Roy Fielding in 2000. It is organised around **resources** identified by URLs and manipulated through **representations**.
- The six constraints (client-server, stateless, cacheable, uniform interface, layered system, optional code on demand) each have a direct testing implication, especially statelessness (independent tests) and uniformity (consistent structures).
- Good URLs use plural nouns, path IDs, shallow nesting, lowercase letters, and hyphens. The HTTP method supplies the verb. A base URL identifies the API root and should be stored in a variable.
- APIs are versioned to protect existing clients, most commonly through the URL path (`/v1/`). Old versions need regression tests.
- HTTP methods map to **CRUD**: `POST` creates, `GET` reads, `PUT` and `PATCH` update, `DELETE` removes. The next lesson covers them in depth.
- **JSON** consists of objects, arrays, strings, numbers, booleans, and null. Most beginner errors come from single quotes, trailing commas, missing commas, unescaped quotes, and Python-style literals.
- Status codes carry the outcome of an operation. `4xx` means the client erred; `5xx` means the server failed, and a `500` in response to bad input is a defect.
- **HATEOAS** and the **Richardson Maturity Model** describe how fully an API follows REST. Pagination, filtering, and sorting let clients request part of a collection and are explored in the query parameters lesson.
- **OpenAPI/Swagger** documents are specifications that testers can read line by line to derive tests.
- REST, SOAP, GraphQL, and gRPC are different styles; REST is the most common, and its HTTP skills transfer to the others.
- A tester examines every endpoint for happy path, validation, boundary, state, security, and non-functional behaviour, and always reads back after a write.

## Additional Resources

- Roy Fielding, *Architectural Styles and the Design of Network-based Software Architectures* (the original REST dissertation, Chapter 5): https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
- Red Hat, *What is a REST API?*: https://www.redhat.com/en/topics/api/what-is-a-rest-api
- MDN Web Docs, *Working with JSON*: https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON
- OpenAPI Initiative, *What is OpenAPI?*: https://www.openapis.org/what-is-openapi
- Swagger documentation, *OpenAPI 3.0 Guide*: https://swagger.io/docs/specification/about/
- JSONPlaceholder guide (free fake API for practice): https://jsonplaceholder.typicode.com/guide/
- Martin Fowler, *Richardson Maturity Model*: https://martinfowler.com/articles/richardsonMaturityModel.html
