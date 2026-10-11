# Query Parameters and Path Variables

## Learning Objectives

By the end of this lesson you will be able to:

- Define **path variables** and **query parameters**, say exactly where each one sits inside a URL, and explain how a server reads them.
- Break any URL into scheme, host, path, query string and fragment, and say which parts the server actually receives.
- Build requests that use single, multiple and repeated query parameters, and recognise the three common ways of sending a list of values.
- Use query parameters for filtering, searching, sorting, field selection and pagination, and calculate offsets, page counts and last-page sizes by hand.
- Percent-encode special characters and Unicode correctly, and know which characters are reserved and why.
- Explain the difference between an empty parameter and a missing one, why a filter with no matches returns `200` with `[]`, and why a missing resource returns `404`.
- Decide between a path variable and a query parameter for any piece of information, and justify the choice.
- Read API documentation and extract the exact parameter rules (name, type, required or optional, default, allowed values, limits).
- Send both kinds of parameter with `curl` (in bash, PowerShell and cmd) and in Postman, including `:pathVariable` syntax, disabling rows and Bulk Edit.
- Write Postman test scripts that prove filters, limits, sorting and pagination really worked.
- Design a thorough set of positive and negative tests for parameters, and recognise the security risks that parameters create.

---

## Why This Matters

This week's epic is to build a pipeline-ready test automation framework for an API. Every automated API test you will ever write is, at its core, a request plus a set of expectations. The "plus" part, the part that makes one request different from another, is almost always a parameter. "Give me user 42." "List the open orders from last week, newest first, twenty at a time." "Search for products containing the word laptop." All of that information travels in the URL as **path variables** and **query parameters**.

For a tester these two mechanisms matter for three reasons.

First, they are **inputs**, and inputs are where defects live. A developer who writes `GET /users/{id}` has to decide what happens when the id is missing, negative, enormous, text, empty, or full of symbols. A developer who writes a `limit` parameter has to decide what `limit=0`, `limit=-5` and `limit=1000000` mean. Every one of those decisions is a place where the developer might have forgotten something, and every one is a test you can write.

Second, they are **everywhere**. You cannot use a real API without them, so you cannot test a real API without understanding them precisely. Many beginners lose hours to bugs that turn out to be a forgotten `&`, an unencoded space, or a path variable left as the literal text `:id`.

Third, they are the **foundation for what comes next**. Later today you will meet headers, and Postman variables and environments, which let you put values like `{{baseUrl}}` and `{{userId}}` into your requests. On Tuesday you will send the same parameters from Python code. On Wednesday you will run one test against many sets of parameter values (data-driven testing). All of that builds on the vocabulary and instincts you develop in this lesson, so we will take our time.

We will use two free practice services throughout. **JSONPlaceholder** (`https://jsonplaceholder.typicode.com`) is a fake REST API with posts, comments, users, todos, albums and photos. **httpbin** (`https://httpbin.org`) is a service that echoes back exactly what it received, which makes it perfect for seeing how a server interprets your parameters. You will also see a made-up shop API (`https://api.example.com`) where we need an example that the practice services cannot give us; those examples are illustrations, not live endpoints.

---

## The Concept

### Part 1: The Anatomy of a URL

Before we can talk about parameters we need to be precise about where they live. A URL (Uniform Resource Locator) is the address of something on a network. Consider this full example:

```
https://api.example.com:8443/v1/users/42/orders?status=open&sort=date#details
\___/   \_____________/\___/\___________________/ \______________/ \_____/
scheme      host       port        path               query        fragment
```

Here is what each part means, and how it relates to what we study today.

The **scheme** (`https`) says which protocol to use. For our purposes it is almost always `http` or `https`.

The **host** (`api.example.com`) says which server to contact. The optional **port** (`8443`) says which door on that server to knock on; if you leave it out, `http` uses 80 and `https` uses 443.

The **path** (`/v1/users/42/orders`) says which resource on that server you want. The path is split into **segments** by slashes: `v1`, `users`, `42` and `orders`. This is where **path variables** live. In the example, `42` is the path variable: it is the one segment whose value changes from request to request, while `v1`, `users` and `orders` are fixed.

The **query string** is everything after the first `?` and before any `#`. It is a list of `name=value` pairs joined by `&`. In the example it is `status=open&sort=date`. Each pair is a **query parameter**.

The **fragment** (`#details`) points at a place inside the document, such as a heading on a web page. This is the part beginners most often forget: **the fragment is never sent to the server**. The browser or HTTP client keeps it for itself. If you accidentally type `#` inside a parameter value without encoding it, everything after the `#` silently disappears from the request. We will return to this trap in the encoding section.

When your client actually sends the request over HTTP, it does not send the whole URL as one piece. The first line of the HTTP request (the request line, which you met in the HTTP messages lesson) contains the method and the **request target**, which is the path plus the query string:

```
GET /v1/users/42/orders?status=open&sort=date HTTP/1.1
Host: api.example.com:8443
Accept: application/json
```

The explanation: the scheme and port are used to open the connection, the host goes into the `Host` header, and the path and query string go in the request line. The fragment is dropped. The server therefore receives exactly two kinds of URL-based input from you: the path (including path variables) and the query string (including query parameters). Everything else in this lesson is about those two.

---

### Part 2: Path Variables

#### What a path variable is

A **path variable** (also called a **path parameter**) is a value that appears as one segment of the URL path and identifies **which specific resource** you are talking about.

Think of a path as the address of a flat in a building: `/building/12/floor/3/flat/7`. The numbers 12, 3 and 7 are not options; they are part of the address. If you drop one, you are no longer asking about the same place.

In a REST API the path is built from **nouns** (resources) and **identifiers**. Here are JSONPlaceholder examples you can run right now:

```bash
curl https://jsonplaceholder.typicode.com/users/3
curl https://jsonplaceholder.typicode.com/posts/10/comments
```

The explanation: `curl` sends a `GET` request by default. The first command asks for the single user whose id is `3`. The second asks for the comments that belong to the post whose id is `10`; here the path variable `10` is followed by a fixed segment `comments`, which names a sub-collection.

#### How documentation writes path variables

API documentation cannot print every possible id, so it writes a **placeholder** where the variable goes. The most common notations are curly braces and colons:

```
GET /users/{userId}
GET /users/{userId}/orders/{orderId}
GET /users/:userId/orders/:orderId
```

You replace the placeholder with a real value when you send the request. In the first line, `{userId}` becomes `42`, giving `/users/42`. Do not include the braces or the colon in the real request. A frequent beginner error is sending `/users/{userId}` literally; the server then looks for a user whose id is the text `{userId}` and answers `404` or `400`.

The name inside the braces (`userId`) is only a label for humans and tools. The server does not see the name in the request, only the value. That is an important difference from query parameters, where the name travels with the value.

#### How a server reads a path variable

On the server side, the web framework has a **route** defined with a pattern, something like `/users/{userId}`. When a request arrives for `/users/42`, the framework matches the pattern, takes the segment in the variable position, and hands the string `"42"` to the application code. The code then usually converts it to a number and looks the user up in a database. Two things follow from this.

First, the value always arrives as **text**. Whether it is valid as a number is the application's job to check. This is why testing `/users/abc` is worthwhile: if the developer forgot to validate, converting `"abc"` to a number may crash and produce a `500 Internal Server Error` instead of a clean `400 Bad Request` or `404 Not Found`.

Second, **position matters**. The framework decides what a segment means by where it is. `/users/42/orders` and `/orders/42/users` are different routes, even though the same words are present.

#### Characteristics of path variables

A path variable is usually **required**. If you leave it out, you do not get a "default" result; you reach a different endpoint. `/users/` (or `/users`) is the collection of all users, while `/users/42` is one user. A path variable identifies one specific thing, so it makes no sense to treat it as optional.

A path variable normally contains an **identifier** such as a number (`42`), a UUID (`3f2b8c1e-9d4a-4e6b-8a57-0c1d2e3f4a5b`), or a human-readable slug (`blue-running-shoes`). It should not contain slashes, because the slash is the character that separates segments. If an identifier could contain a slash, it must be encoded as `%2F`, and many servers handle that badly, which is itself a good test case.

#### Nested path variables

Resources often belong to other resources, and REST APIs express that by **nesting** path segments:

```
GET /users/42/orders             -> all orders of user 42
GET /users/42/orders/7           -> order 7 of user 42
GET /users/42/orders/7/items/2   -> item 2 within order 7 of user 42
```

Each variable narrows the scope. Reading left to right: "In the collection of users, take user 42; within that user's orders, take order 7; within that order's items, take item 2."

JSONPlaceholder supports one level of nesting:

```bash
curl https://jsonplaceholder.typicode.com/posts/1/comments
curl https://jsonplaceholder.typicode.com/users/1/todos
curl https://jsonplaceholder.typicode.com/albums/1/photos
```

The explanation: each command asks for the child collection of one parent. The first returns the comments of post 1, the second the todos of user 1, and the third the photos of album 1.

Nesting raises an important testing question, the **ownership check**. If order 7 belongs to user 42, then `/users/99/orders/7` should *not* return it; it should answer `404` (or `403`). A server that checks only the order id and ignores the user id has a serious defect. We will come back to this in the security section. Notice also that very deep nesting is generally considered poor design; most API designers stop at two or three levels.

#### Case sensitivity, trailing slashes and other path details

The **path is case-sensitive** according to the URL standard: `/Users/42` and `/users/42` are technically different paths. Many frameworks are strict and answer `404` for `/Users/42`; a few are lenient. The **host** part is not case-sensitive. When you test, do not assume; try it and compare with the documentation.

**Trailing slashes** are another source of inconsistency. Are `/users/42` and `/users/42/` the same? Some servers treat them identically, some redirect one to the other with a `301` or `308` status, and some return `404` for the unexpected form. Neither answer is wrong by itself, but the behaviour should be consistent and documented. If your test client does not follow redirects, an unexpected `301` will surprise you. When writing automated tests, always copy the exact form from the documentation.

#### Path variables versus path text

Not every changing part of a path is a "variable" in the sense of an input. In `/v1/users`, the `v1` is an API version. It changes rarely, and it is part of the fixed route. When we say "path variable" we mean a segment whose value changes with the specific resource you want.

---

### Part 3: Query Parameters

#### What a query parameter is

A **query parameter** (also called a **query string parameter** or **URL parameter**) is a `name=value` pair placed after the `?` that **modifies, filters or shapes** what the server returns from a resource or collection.

Where a path variable is part of the address, a query parameter is more like an instruction attached to the request: "go to this address, but only bring back the open ones, sorted by date, twenty at a time."

```
GET /posts?userId=1
GET /posts?userId=1&_limit=5
```

The explanation: the first `?` marks the end of the path and the start of the query string. Each pair has the shape `name=value`. Multiple pairs are separated by `&`. Neither the `?` nor the `&` is part of any name or value; they are punctuation that the server uses to split the string.

Try it:

```bash
# Only posts written by user 1
curl "https://jsonplaceholder.typicode.com/posts?userId=1"

# Only the first 3 posts
curl "https://jsonplaceholder.typicode.com/posts?_limit=3"

# Combine both conditions
curl "https://jsonplaceholder.typicode.com/posts?userId=2&_limit=3"
```

The explanation: all three are `GET` requests to the same path, `/posts`, which is the collection of posts. Without a query string you would get all 100 posts. The first adds a filter; the second adds a limit; the third combines them, and the server applies both, giving up to three posts that belong to user 2. The quotes around each URL are essential; the section on `curl` explains why.

#### How a server parses a query string

The server (or the framework in front of the application) performs these steps on the query string `userId=2&_limit=3`:

1. Split the string on `&` into pieces: `userId=2` and `_limit=3`.
2. Split each piece on the first `=` into a name and a value: (`userId`, `2`) and (`_limit`, `3`).
3. **Percent-decode** the names and values (turn `%20` back into a space, and so on).
4. Store the result in a map or list that the application can query, for example `params["userId"]`.

Everything is text at this stage. The application must convert `"3"` to the number 3 and decide what to do if the text was `"three"`.

httpbin is the best tool for watching this in action, because its `/get` endpoint returns the parsed parameters in an `args` field:

```bash
curl "https://httpbin.org/get?name=Ada&role=admin&role=tester"
```

A trimmed version of the response looks like this:

```json
{
  "args": {
    "name": "Ada",
    "role": ["admin", "tester"]
  },
  "url": "https://httpbin.org/get?name=Ada&role=admin&role=tester"
}
```

The explanation: `args` is the server's own interpretation of your query string. `name` has one value, so it is a plain string. `role` appeared twice, and httpbin (like many servers) collected both values into a list. The `url` field shows the exact URL the server received. Whenever you are unsure how a client is encoding your parameters, an httpbin request is an excellent way to find out.

#### Required versus optional

Query parameters are usually **optional**. A request without a query string normally still works and returns default behaviour, for example the first page of all items in default order.

Some query parameters are **required**. A search endpoint such as `GET /search?q=laptop` makes no sense without `q`, so the server should answer `400 Bad Request` with a message saying which parameter is missing. Documentation tells you which is which, and your tests should check both directions: that a required parameter really is enforced, and that omitting an optional one gives the documented default.

#### Single, multiple and repeated parameters

A **single** parameter is one pair: `?status=open`.

**Multiple** parameters with different names are joined with `&`: `?status=open&sort=date`. Servers normally combine different filters with logical **AND**: the result must match all of them. The order of different names does not normally matter, so `?a=1&b=2` and `?b=2&a=1` give the same result. Testing that claim is a good check.

A **repeated** parameter is the same name used more than once. The URL standard allows it, but there is no single rule for what it means, and this is a major source of surprises. Here are the three common conventions for sending a list of values.

| Style | Example | Who uses it |
|-------|---------|-------------|
| Repeated name | `?id=1&id=2&id=3` | JSONPlaceholder, many Java and Node frameworks, httpbin |
| Bracket suffix | `?id[]=1&id[]=2&id[]=3` | PHP and Ruby on Rails style frameworks |
| Comma-separated | `?id=1,2,3` | Many public APIs, for compactness |

Each convention requires the server to be built for it. If you send `?id=1,2,3` to a server that expects repeated names, it will treat `"1,2,3"` as a single value and probably find nothing or return an error. The documentation is the only authority.

JSONPlaceholder uses the repeated-name style. Try:

```bash
curl "https://jsonplaceholder.typicode.com/posts?id=1&id=2&id=3"
```

The explanation: this asks for the posts whose id is 1, **or** 2, **or** 3. Notice that for repeated values of the same field the logic is OR (any of them), whereas for different fields it is AND. You should get exactly three posts back.

What if a server does not support repeats and you send one anyway? Different servers react differently. Some use the **first** value, some use the **last**, some join them, some return an error. This variation is exactly why "repeated parameter" appears in our test design tables later. Your test should discover what the API does and compare it with the documentation.

There is a second, less obvious subtlety: names are also case-sensitive on most servers. `?userId=1` and `?userid=1` are different parameters. If you misspell a name, a lenient server will simply **ignore** it and return everything, and a careless test that checks only for a `200` status will pass even though the filter was never applied. Always verify the content of the response, not just the status code.

#### Empty versus missing parameters

There are three different situations that look similar but are not the same:

```
GET /posts                 -> the parameter is missing (not sent at all)
GET /posts?userId=         -> the parameter is present but empty
GET /posts?userId          -> the name only, with no equals sign
```

A **missing** parameter means "use the default." An **empty** one (`userId=`) means "the client explicitly said the value is the empty string." Depending on the server, that could mean "no filter" (same as missing), "match nothing", or "invalid, return `400`." The name-only form (`?userId`) is parsed by different servers as an empty value or as a flag with no value.

None of these is universally correct. The point for a tester is to **know the three cases exist, probe each one, and compare the behaviour with the documentation**. A common real bug is a server that crashes with a `500` on the empty case because the developer tried to convert `""` to a number.

#### Typical uses of query parameters

Names vary between APIs, so always read the documentation, but the jobs are common.

| Job | Typical names | Example |
|-----|--------------|---------|
| Filtering | `status`, `userId`, `category` | `/products?category=books` |
| Searching | `q`, `search`, `query` | `/products?q=laptop` |
| Sorting | `sort`, `order`, `sortBy`, `_sort` | `/products?sort=price&order=desc` |
| Pagination | `page`, `limit`, `offset`, `size`, `cursor` | `/products?page=3&limit=20` |
| Field selection | `fields`, `select` | `/users?fields=id,name` |
| Extra detail | `expand`, `include`, `verbose` | `/orders?include=items` |

Let us look at each in more depth.

**Filtering** narrows a collection to items matching a condition on a field. `GET /todos?userId=1&completed=true` should return only todos belonging to user 1 and marked completed. Filtering is the single most important query parameter job for testers, because it is easy to write a filter that appears to work for the developer's single test case and breaks for others.

**Searching** is different from filtering. A filter normally requires **exact** equality on a field (`status=open`). A search usually looks for a word or fragment across one or several fields and may be case-insensitive, partial, or ranked by relevance. When you test search, check the exact semantics: does `q=lap` find "laptop"? Does `q=LAPTOP`? Does `q=lap top`?

**Sorting** controls the order of results. Two designs are common: a field name plus a direction (`sort=price&order=desc`), or a single parameter with a sign prefix (`sort=-price`, where the minus means descending). JSONPlaceholder uses `_sort` and `_order`:

```bash
curl "https://jsonplaceholder.typicode.com/posts?_sort=title&_order=desc&_limit=5"
```

The explanation: the server sorts all posts by their `title` in descending order, then keeps the first five. The order of operations matters. The server should sort first and limit afterwards; if it limited first and sorted afterwards, you would get the wrong five. That is a classic bug you can check for.

**Field selection** (sometimes called "sparse fieldsets") lets the client ask for only the fields it needs, reducing the size of the response: `/users?fields=id,name`. Here the comma-separated style is used. A test should check that the returned objects contain exactly the requested fields and nothing else.

**Extra detail** parameters such as `expand` or `include` ask for related data to be embedded in the response, saving a second request.

#### Pagination in depth

If a collection holds 10,000 items, the server should not send them all at once; that would be slow, expensive and might crash the client. Instead it splits the collection into **pages** and returns one at a time. There are three common styles, and each has different arithmetic you must understand to test it.

**Style 1: page and limit.** The client says which page number it wants and how many items per page.

```
GET /posts?_page=3&_limit=10
```

Pages normally start at 1. The first item on a page is calculated as:

```
offset = (page - 1) * limit
```

With `page=3` and `limit=10`, `offset = (3 - 1) * 10 = 20`, so the page contains the items at positions 21 to 30 (counting from 1). JSONPlaceholder has 100 posts with ids 1 to 100 in order, so you should see ids 21 to 30.

To know how many pages exist:

```
totalPages = ceil(totalItems / limit)
```

**Worked example.** There are 95 items and `limit=20`. Then `totalPages = ceil(95 / 20) = ceil(4.75) = 5`. Pages 1 to 4 each contain 20 items (80 items in total), and page 5 contains the remaining `95 - 80 = 15`. Page 6 is beyond the end, so it should contain 0 items. Whether the server answers `200` with `[]` or `404` or `400` for page 6 is a design decision that must be documented; most APIs choose `200` with an empty list.

Now a quirk of dividing evenly: with 100 items and `limit=20`, `ceil(100 / 20) = 5` pages, and page 5 holds exactly 20 items, not 0. A buggy server that computes `totalPages = floor(totalItems / limit) + 1` would report 6 pages and return an empty final page. That is a typical off-by-one defect, and the case "item count is an exact multiple of the page size" is a boundary you should always test.

**Style 2: offset and limit** (sometimes `skip` and `take`). The client says how many items to skip and how many to return.

```
GET /products?offset=40&limit=20
```

Here you supply the offset directly, so the arithmetic is simpler: skip 40 items, return the next 20, which are items 41 to 60 counting from 1. The relation to the page style is `page = offset / limit + 1` when the offset is a multiple of the limit. Offset pagination is more flexible (you can start at any item, such as offset 5) but it is easier to produce inconsistent results, as we describe below.

**Style 3: cursor-based pagination.** Instead of a page number, the server gives you an opaque token (the **cursor**) that marks where the previous page ended, and you send it back to get the next page.

```
GET /events?limit=20
-> { "data": [ ...20 events... ], "nextCursor": "eyJpZCI6MjB9" }

GET /events?limit=20&cursor=eyJpZCI6MjB9
-> { "data": [ ...next 20 events... ], "nextCursor": "eyJpZCI6NDB9" }
```

The explanation: the first call returns the first 20 events plus a `nextCursor` value. That value looks like gibberish deliberately: it is **opaque**, meaning the client must not interpret or build it, only copy it into the next request. (In this example it is a Base64 encoding of internal data, but you should never rely on that.) When `nextCursor` is `null` or absent, there are no more pages. You cannot jump straight to "page 7" with cursors; you move forward one page at a time. Cursors are popular for large or fast-changing data (timelines, event logs) because they stay consistent when items are added or deleted during paging.

To see why, imagine offset-based paging while data changes. You fetch `offset=0&limit=10` and receive items 1-10. Before you fetch the next page, someone deletes item 3. Now what was item 11 has moved to position 10, so `offset=10&limit=10` starts at what was originally item 12, and **you never see item 11**. Cursor-based paging says "continue after the item I last saw", which is immune to that shift. Your tests can reveal such weaknesses by modifying data between page requests (in a safe test environment).

JSONPlaceholder reports the total count in a response **header** called `X-Total-Count`. You can see headers with `curl -i`:

```bash
curl -i "https://jsonplaceholder.typicode.com/posts?_page=2&_limit=10"
```

The explanation: `-i` tells curl to print the response headers before the body. Look for `X-Total-Count: 100`. That header lets a client work out the number of pages without downloading everything. We cover headers fully in the next lesson; for now just note that pagination metadata may arrive in headers or in the JSON body (fields like `total`, `page`, `hasMore`), depending on the API.

Pagination is a rich source of defects. In the test design section we will list the edge cases: page 0, negative page, page beyond the end, limit 0, limit enormous, last page, and an item count that divides evenly.

---

### Part 4: Percent-Encoding in Depth

#### Why encoding exists

A URL is a string that uses a deliberately small set of characters so that it can pass safely through every kind of computer, network and program. Some characters in that string have **structural meaning**: they separate parts of the URL. The question is how to include one of those characters as ordinary *data* inside a value. The answer is **percent-encoding** (also called URL encoding): write the byte value of the character in hexadecimal, with a `%` in front.

#### Reserved and unreserved characters

The URL standard divides characters into groups.

**Unreserved characters** are always safe and never need encoding: the letters `A-Z` and `a-z`, the digits `0-9`, and the four symbols `-`, `.`, `_` and `~`.

**Reserved characters** have special roles in a URL. They are `: / ? # [ ] @ ! $ & ' ( ) * + , ; =`. When one of these appears in a position where it would be misread as structure, it must be encoded. Whether a particular reserved character matters depends on where it appears. For instance, `/` is structural in the path (it separates segments), while inside a query value it is usually harmless, though encoding it is always safe.

Everything else (spaces, quotes, `<`, `>`, `%` itself, non-English letters, emoji) is **unsafe** and must be encoded.

#### The reference table

| Character | Meaning in a URL | Encoded form |
|-----------|------------------|--------------|
| space | Not allowed | `%20` (or `+` in query strings) |
| `!` | Sub-delimiter | `%21` |
| `"` | Not allowed | `%22` |
| `#` | Starts the fragment | `%23` |
| `$` | Sub-delimiter | `%24` |
| `%` | Starts an escape | `%25` |
| `&` | Separates query pairs | `%26` |
| `'` | Sub-delimiter | `%27` |
| `+` | Space in query strings | `%2B` |
| `,` | Sub-delimiter (list separator) | `%2C` |
| `/` | Separates path segments | `%2F` |
| `:` | Separates scheme, port | `%3A` |
| `;` | Sub-delimiter | `%3B` |
| `<` | Not allowed | `%3C` |
| `=` | Separates name from value | `%3D` |
| `>` | Not allowed | `%3E` |
| `?` | Starts the query string | `%3F` |
| `@` | Separates user info from host | `%40` |
| `[` | Reserved | `%5B` |
| `]` | Reserved | `%5D` |

A very important point is the character **`%` itself**. Because `%` introduces an escape sequence, a literal percent sign in your data must become `%25`. If you do not encode it, the server tries to read the next two characters as hexadecimal and may fail or misinterpret them. For example, a search for `50%` must be sent as `50%25`; a raw `?discount=50%` produces a malformed escape.

#### The space: `%20` versus `+`

In a query string, a space can be written as either `%20` or `+`. The `+` convention comes from the HTML form encoding (`application/x-www-form-urlencoded`) and is understood by nearly every server for query strings. In the **path**, however, `+` means a literal plus sign, so a space in a path must always be `%20`. The safest habit is to use `%20` everywhere. This also means that if you want a literal plus sign in a query value, such as in the phone number `+44 20 7946 0000`, you must write `%2B`; a bare `+` will arrive as a space.

#### Unicode

URLs can only carry ASCII characters, so non-English letters and symbols are first converted to bytes using **UTF-8** and then each byte is percent-encoded. A character can take one to four bytes.

| Character | UTF-8 bytes (hex) | Encoded |
|-----------|-------------------|---------|
| `é` | C3 A9 | `%C3%A9` |
| `è` | C3 A8 | `%C3%A8` |
| `€` | E2 82 AC | `%E2%82%AC` |
| `日` | E6 97 A5 | `%E6%97%A5` |
| `😀` | F0 9F 98 80 | `%F0%9F%98%80` |

#### Worked examples

**Example 1.** Encode the search value `rock & roll`. The space becomes `%20` and the ampersand `%26`, giving `rock%20%26%20roll`, so the request is:

```
GET /songs?q=rock%20%26%20roll
```

If you forgot to encode the `&`, the server would see `q=rock%20` followed by a separate parameter named ` roll` with no value. The search would silently become "rock" and an extra junk parameter would appear. This is the same kind of error as a broken filter, and it is very hard to spot without checking the response data.

**Example 2.** Encode `café & crème`. The word `café` has an `é` (`%C3%A9`), and `crème` has an `è` (`%C3%A8`). Replacing each space with `%20` and the ampersand with `%26`, we get `caf%C3%A9%20%26%20cr%C3%A8me`.

**Example 3.** Encode `black & white #1`. The space characters become `%20`, `&` becomes `%26`, and `#` becomes `%23`, giving `black%20%26%20white%20%231`. Without encoding `#`, everything from the `#` onwards would be treated as a fragment and **never leave your machine**; the server would search for `black & white` and nothing more.

**Example 4.** Decode `price%3E100%26sort%3Dasc`. Reading each escape: `%3E` is `>`, `%26` is `&`, `%3D` is `=`. The decoded text is `price>100&sort=asc`. Notice that after decoding, this text contains an `&` and an `=`. If it had been sent *unencoded* these would have been seen as structure; because they were encoded, the server received them as part of a single value.

**Example 5 (the double-encoding trap).** Suppose a tool encodes `rock & roll` correctly to `rock%20%26%20roll`, and then a second layer encodes it again. The `%` becomes `%25`, producing `rock%2520%2526%2520roll`. The server decodes once and sees the literal text `rock%20%26%20roll` instead of `rock & roll`. This is a very common defect when one part of a framework encodes and another does too. It is also a good negative test: send double-encoded input on purpose and see what the server does.

#### Where encoding applies

Encode **each value separately**, never the whole URL. If you encode the entire URL, you would also encode the `?`, `&`, `=` and `/` that you need as structure. The correct procedure is to encode each name and each value and then assemble the URL with the unencoded punctuation. Tools such as Postman's Params table and `curl --data-urlencode` do this for you, which is why you should use them rather than building strings by hand.

---

### Part 5: Path Variables Versus Query Parameters

#### The core idea

The two mechanisms answer different questions.

| | Path variable | Query parameter |
|---|---------------|-----------------|
| Location | In the path (`/users/42`) | After `?` (`?role=admin`) |
| Purpose | **Identify** one specific resource | **Filter, sort, page or shape** a result |
| Required? | Typically yes | Typically optional |
| If omitted | You reach a different endpoint | Default behaviour applies |
| Name sent? | No, only the value | Yes, name and value |
| Order | Position matters | Order of different names rarely matters |
| Missing target | `404 Not Found` | `200` with an empty list |

Remember it this way: **path answers "which one?"; query answers "how would you like it?"**.

```
GET /users/42             -> "Give me user 42."                 (identify)
GET /users?role=admin     -> "Give me users, only the admins."  (filter)
```

#### Decision guide with ten examples

Ask yourself: *Would the request be a different resource without this value, or just a different view of the same resource?* If the former, it is a path variable. If the latter, a query parameter.

| # | Information | Better as | Reason |
|---|-------------|-----------|--------|
| 1 | The id of a user: `/users/42` | Path | Names one specific resource |
| 2 | Only the active users: `/users?status=active` | Query | A filter on a collection |
| 3 | Comments of post 7: `/posts/7/comments` | Path | Posts own comments; the parent is part of the address |
| 4 | The same comments as a filter: `/comments?postId=7` | Query | Also valid; filters the whole comments collection (JSONPlaceholder supports both) |
| 5 | Page number: `/products?page=3` | Query | Changes the view, not the resource |
| 6 | Sort order: `/products?sort=price` | Query | Presentation of the same collection |
| 7 | Search text: `/products?q=laptop` | Query | A search is a filter with free text |
| 8 | Which version of the API: `/v2/users` | Path (fixed segment) | Selects a different contract, not a filter |
| 9 | The id of an order to cancel: `DELETE /orders/9001` | Path | The target of the action |
| 10 | Which fields to return: `/users/42?fields=id,name` | Query | Shapes the representation of user 42 |
| 11 | Language of a message: `/messages/5?lang=fr` | Query | Same resource, different presentation |
| 12 | A file name: `/files/report.pdf` | Path | Identifies the file |

Examples 3 and 4 show that the line can blur: the same result can sometimes be reached either way. A good API is consistent, and as a tester your job is not to decide which design is prettier but to check that the actual behaviour matches the documentation.

One more useful rule: **never use a query parameter to identify the primary resource of a `GET`, `PUT` or `DELETE` of one item** if the API's design uses a path variable. `DELETE /orders?id=9001` could be acceptable in a poorly designed API but is not typical REST, and a documented `DELETE /orders/9001` must not accidentally work both ways.

#### Combining both

Real requests mix them freely. Reading this example left to right:

```
GET /stores/12/products?inStock=true&sort=price&page=2&limit=5
```

`/stores/12` is a path variable identifying the store, and `/products` is the sub-collection. Then `inStock=true` filters, `sort=price` orders, and `page=2&limit=5` pages the result. The sentence in plain English: "In store 12, show products that are in stock, sorted by price, page two of five per page." The path chose the *scope*; the query shaped the *view*.

---

### Part 6: Reading API Documentation for Parameters

Good documentation lists every parameter in a table. Here is a realistic extract for our invented shop API:

```
GET /stores/{storeId}/products

Path parameters
  storeId   integer   required   The id of the store. Must be >= 1.

Query parameters
  category  string    optional   Filter by category. One of: books, music, games.
  minPrice  number    optional   Minimum price, inclusive. Default: none.
  maxPrice  number    optional   Maximum price, inclusive. Default: none.
  sort      string    optional   Field to sort by: price, name. Default: name.
  order     string    optional   asc or desc. Default: asc.
  page      integer   optional   Page number, starting at 1. Default: 1.
  limit     integer   optional   Items per page, 1 to 50. Default: 20.

Responses
  200  A page of products (possibly empty).
  400  An invalid parameter value.
  404  The store does not exist.
```

Read it in this order, and turn each piece of information into a test.

First, note the **location**: `storeId` is a path parameter, the others are query parameters. Second, note **required or optional**: only `storeId` is required, so omitting it is a different endpoint, and omitting the others must apply the defaults. Third, the **type**: `storeId` is an integer, so `abc` and `1.5` are type-confusion tests. Fourth, the **allowed values**: `category` has a closed list, so `category=food` should give `400`, and `category=BOOKS` tests case sensitivity. Fifth, the **ranges**: `limit` is 1 to 50, so the boundary tests are 0, 1, 50 and 51. Sixth, the **defaults**: `page` defaults to 1, so a request with no `page` should equal a request with `page=1`. Seventh, the **responses table**: a nonexistent store is `404`, and an invalid value is `400`; notice it says a page may be empty, which confirms `200` with `[]` for a filter with no matches.

Documents that are machine-readable (OpenAPI/Swagger specifications) express the same facts in a formal way, often with `in: path` or `in: query` labels. You will meet that format in the context of tooling later in the week; the information is the same.

Whenever documentation is missing or unclear about a parameter's behaviour, treat that as a finding. Write it down as a question for the developer or product owner. Testing against an unstated rule is guessing.

---

### Part 7: Hands-On with curl

`curl` is a command-line tool for sending HTTP requests. It is available on Linux, macOS and modern Windows. It is excellent for quick experiments and for reproducing bugs in a way that you can paste into a ticket.

#### The basic form and the quoting problem

```bash
curl "https://jsonplaceholder.typicode.com/posts?userId=1&_limit=3"
```

The explanation: the URL is wrapped in double quotes. Without them, the shell would interpret `&` as "run the previous command in the background and then start a new command", and `?` as a wildcard character. The command would then send only `https://jsonplaceholder.typicode.com/posts?userId=1` and try to run a command named `_limit=3`. Always quote URLs that contain a query string.

Quoting rules differ between shells, and this is a classic stumbling block on a team where people use different operating systems.

**bash and zsh (Linux, macOS, Git Bash).** Prefer **single quotes** because nothing inside them is interpreted: `curl 'https://httpbin.org/get?a=1&b=2'`. Double quotes work but the shell still expands `$` (variables) and `!` (history) inside them, so a value such as `price$` or `hello!` can be altered before curl sees it.

**PowerShell (Windows).** In Windows PowerShell 5.1 the word `curl` is an **alias** for a different command, `Invoke-WebRequest`, which has different options. To run the real curl, type `curl.exe`. PowerShell treats `&` as a reserved operator, so quote URLs. Single quotes are literal; double quotes expand `$variables` and the backtick is the escape character: `curl.exe 'https://httpbin.org/get?a=1&b=2'`.

**cmd.exe (Windows Command Prompt).** Only **double quotes** are recognised for grouping; single quotes are passed through literally and would become part of the URL. The ampersand separates commands unless it is inside double quotes: `curl "https://httpbin.org/get?a=1&b=2"`. Also, `%` is special inside `.bat` files (write `%%`), though not when typing at the prompt.

Here is a compact summary.

| Shell | Safe quoting | Notes |
|-------|--------------|-------|
| bash/zsh | Single quotes | Double quotes expand `$` and `!` |
| PowerShell | Single quotes, and use `curl.exe` | `curl` alone is an alias for something else |
| cmd.exe | Double quotes only | `&` outside quotes splits the command |

#### Letting curl do the encoding: `-G` and `--data-urlencode`

Hand-encoding values is error-prone. Let curl do it:

```bash
curl -G "https://httpbin.org/get" --data-urlencode "q=rock & roll"
```

The explanation, option by option: `-G` (long form `--get`) tells curl to take any data options and append them to the URL as a **query string** with the method `GET`, instead of putting them in a request body. `--data-urlencode "q=rock & roll"` supplies a `name=value` pair and tells curl to percent-encode the **value** part (not the name, and not the `=`). The result is `GET /get?q=rock%20%26%20roll`. In httpbin's response the `args` field will show `"q": "rock & roll"`, proving the server decoded it properly.

You can repeat the options to add more parameters:

```bash
curl -G "https://httpbin.org/get" \
  --data-urlencode "q=café & crème" \
  --data-urlencode "category=books" \
  -d "page=2" \
  -d "limit=5"
```

The explanation: each `--data-urlencode` adds an encoded pair. `-d` (long form `--data`) adds a pair **without** encoding, which is fine for values that you know are safe such as numbers. The backslash at the end of a line continues the command on the next line in bash; in PowerShell the continuation character is a backtick, and in cmd it is a caret `^`. Together with `-G`, all four pairs go into the query string and httpbin shows them in `args`.

To send a repeated parameter, repeat the pair:

```bash
curl -G "https://httpbin.org/get" -d "id=1" -d "id=2" -d "id=3"
```

The explanation: httpbin will respond with `"id": ["1", "2", "3"]`. For the bracket style, use `--data-urlencode "id[]=1"`; but note that curl treats square brackets in the **URL** as a globbing feature (a range syntax), so if you type brackets directly in the URL you need the `-g` (`--globoff`) option: `curl -g "https://httpbin.org/get?id[]=1&id[]=2"`.

Useful extras while experimenting: `-i` shows response headers, `-v` shows the full request and response (including the exact request line, so you can check the encoding), and `-s` hides the progress meter.

Path variables in curl need no special option, because they are simply part of the URL: `curl https://jsonplaceholder.typicode.com/users/3`. If you build the URL from a shell variable, remember to quote it: `curl "https://jsonplaceholder.typicode.com/users/$USER_ID"`.

---

### Part 8: Hands-On in Postman

#### Query parameters, step by step

1. Create a new request (the **+** button, or **New > HTTP**). Set the method to `GET`.
2. Type the base URL only: `https://jsonplaceholder.typicode.com/posts`.
3. Open the **Params** tab under the URL bar. You see a table called **Query Params** with columns **Key**, **Value** and **Description**.
4. In the first empty row type `userId` as the key and `1` as the value.
5. In the next row type `_limit` as the key and `3` as the value.
6. Look at the URL bar. Postman has built `https://jsonplaceholder.typicode.com/posts?userId=1&_limit=3` for you. The table and the URL stay in sync: editing either updates the other.
7. Click **Send**. Check the status and the body.

Each row has a **checkbox** on the left. **Unticking** a row disables the parameter without deleting it, and Postman removes it from the URL. This is a fast way to test "what if this parameter is absent?" and to switch between scenarios without retyping. Re-ticking it restores the parameter.

Use the **Description** column to record what each parameter does; descriptions are saved with the request and become documentation for the team.

To see the exact request Postman sent, open the **Postman Console** (View > Show Postman Console). It prints the final URL after encoding. Always check it when something behaves strangely.

#### Bulk Edit

For many parameters, typing in a grid is slow. Click **Bulk Edit** at the right of the Params header. The table turns into a text box with one `key:value` per line:

```
userId:1
_limit:3
```

The explanation: you can paste a whole list of parameters from documentation or a ticket and Postman parses it into rows. A line that begins with `//` becomes a disabled row. Click **Key-Value Edit** to switch back to the grid.

#### Path variables, step by step

In Postman, a path variable is written with a **colon** before the name:

1. Type the URL `https://jsonplaceholder.typicode.com/users/:userId`.
2. A new table titled **Path Variables** appears under the Query Params table in the Params tab, with the key `userId` already listed.
3. Type `3` in the **Value** column.
4. Click **Send**. Postman replaces `:userId` with `3` and requests `/users/3`.

This keeps the URL readable and lets you change the value without editing the URL text. You can combine both kinds in one request: `https://jsonplaceholder.typicode.com/users/:userId/posts` with `userId` set to `1` and, in Query Params, `_limit` set to `2`.

Two warnings. First, if you **leave the Value empty**, Postman sends the literal text `:userId` in the URL and the server returns an error; if you see `404` for a path-variable request, check this first. Second, the colon syntax only applies in the path. A port number such as `localhost:3000` is recognised as a port, not a variable, but a colon in a place you did not intend can confuse the parser.

Later today, in the lesson on Postman variables and environments, you will learn how to replace fixed values like `3` with variables such as `{{userId}}` that come from an environment. Do not worry about that yet.

#### Encoding in Postman

When you type values in the **Params table**, Postman percent-encodes them automatically when it builds the request. For example, entering the value `rock & roll` produces `rock%20%26%20roll` in the request that is actually sent. If you instead type the characters directly into the URL bar, Postman may leave some characters unencoded. When in doubt, use the table and confirm in the Console.

---

### Part 9: Verifying Parameters with Postman Test Scripts

A status code of `200` proves only that the server did not complain. It does not prove that the parameter had any effect. A misspelled filter name is commonly ignored and returns everything with a `200`. Tests for parameters must therefore inspect the **data**.

Postman test scripts are JavaScript placed in the **Scripts** tab (or **Tests** in older versions), which run after the response arrives. The core pieces are `pm.test(name, function)`, which defines a named check; `pm.response`, which represents the response; and `pm.expect(value)`, which builds an assertion.

#### Script 1: a filter works

Request: `GET https://jsonplaceholder.typicode.com/posts?userId=1`

```javascript
pm.test("Status is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Every returned post belongs to user 1", function () {
    const posts = pm.response.json();
    pm.expect(posts).to.be.an("array").that.is.not.empty;
    posts.forEach(function (post) {
        pm.expect(post.userId).to.eql(1);
    });
});
```

Line by line: `pm.test("Status is 200", function () {...})` defines a test with a readable name; if anything inside the function throws, the test is marked failed. `pm.response.to.have.status(200)` asserts the status code. In the second test, `pm.response.json()` parses the response body as JSON and returns a JavaScript value; for this endpoint it is an array of post objects, which we store in `posts`. `pm.expect(posts).to.be.an("array").that.is.not.empty` checks that the value is an array and that it has at least one element. This guard matters: if the array were empty, the `forEach` loop would run zero times and the test would **pass vacuously**, proving nothing. `posts.forEach(function (post) {...})` runs the inner function once per element. `pm.expect(post.userId).to.eql(1)` asserts that this post's `userId` is deeply equal to 1; `eql` compares by value, and note that it checks the number 1, so a response with the string `"1"` would fail, which is what we want.

#### Script 2: a limit is respected

Request: `GET https://jsonplaceholder.typicode.com/posts?_limit=3`

```javascript
pm.test("No more than 3 posts are returned", function () {
    const posts = pm.response.json();
    pm.expect(posts.length).to.be.at.most(3);
});

pm.test("Exactly 3 posts are returned because more than 3 exist", function () {
    pm.expect(pm.response.json()).to.have.lengthOf(3);
});
```

Line by line: `posts.length` is the number of elements. `.to.be.at.most(3)` asserts that it is less than or equal to 3; this is the minimum a limit must guarantee. The second test is stricter. `.to.have.lengthOf(3)` asserts exactly 3. We know JSONPlaceholder holds 100 posts, so a correct limit of 3 must return exactly 3. The "at most" check passes even if the server returns 0 items by mistake, which is why you should also check "exactly" whenever you know the data supports it.

#### Script 3: sorting works

Request: `GET https://jsonplaceholder.typicode.com/posts?_sort=id&_order=desc&_limit=10`

```javascript
pm.test("Posts are sorted by id in descending order", function () {
    const ids = pm.response.json().map(function (post) {
        return post.id;
    });
    const sortedCopy = ids.slice().sort(function (a, b) {
        return b - a;
    });
    pm.expect(ids).to.eql(sortedCopy);
    pm.expect(ids[0]).to.eql(100);
});
```

Line by line: `.map(function (post) { return post.id; })` transforms the array of posts into an array containing only the ids. `ids.slice()` makes a **copy** of the array, because `sort` changes the array it is called on, and we want to keep the original for comparison. `.sort(function (a, b) { return b - a; })` sorts numerically in descending order: when the function returns a positive number, `b` is placed before `a`. Without the comparison function JavaScript would sort numbers as text (so 100 would come before 9), which is a famous trap. `pm.expect(ids).to.eql(sortedCopy)` asserts that the server's order equals our own independent sorted version. The final line makes a stronger claim: the first id must be 100, since the highest id overall must come first once we sort descending and take 10.

#### Script 4: pages do not overlap

This one uses the **collection of two requests**, the second saving what the first one saw, but we can keep it within one request by making a second call from the script:

```javascript
const baseUrl = "https://jsonplaceholder.typicode.com/posts";

pm.test("Page 1 and page 2 contain different posts", function (done) {
    pm.sendRequest(baseUrl + "?_page=1&_limit=10", function (err, res1) {
        pm.sendRequest(baseUrl + "?_page=2&_limit=10", function (err2, res2) {
            const ids1 = res1.json().map(function (p) { return p.id; });
            const ids2 = res2.json().map(function (p) { return p.id; });
            const overlap = ids1.filter(function (id) { return ids2.includes(id); });
            pm.expect(overlap).to.eql([]);
            done();
        });
    });
});
```

Line by line: `pm.sendRequest(url, callback)` sends an additional HTTP request from inside the script, and the callback runs when the response arrives. We nest two calls to fetch page 1 and then page 2. The `done` argument tells Postman that this test is asynchronous: it must wait until we call `done()`; without it the test would finish before the responses arrive. Inside, we extract the ids from each page with `map`. `ids1.filter(...)` keeps the ids from page 1 that also appear in page 2 (`includes` checks membership), giving us the **overlap**. We assert that the overlap equals an empty array. Do not worry about the callback style; it is how Postman handles waiting for the network.

#### Script 5: an empty filter result versus a missing resource

Request A: `GET https://jsonplaceholder.typicode.com/posts?userId=999`

```javascript
pm.test("A filter with no matches returns 200 and an empty array", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json()).to.eql([]);
});
```

Request B: `GET https://jsonplaceholder.typicode.com/posts/9999`

```javascript
pm.test("A missing single resource returns 404", function () {
    pm.response.to.have.status(404);
});
```

Line by line: in test A we assert both the status and that the body is exactly an empty array, using deep equality `eql([])`. In test B we assert `404`. Together they demonstrate the key distinction explained in the next section.

---

### Part 10: Designing Tests for Parameters

#### The 404 versus empty-list distinction

This is a rule worth memorising. `GET /posts?userId=999` asks the **collection** `/posts` to filter itself. The collection exists; it simply contains no matches, so the right answer is `200 OK` with an empty list `[]`. `GET /posts/9999` asks for **one specific resource** that does not exist, so the right answer is `404 Not Found`. A server that returns `404` for an empty filter result misleads clients into thinking the endpoint itself is broken, and a server that returns `200` with an empty body for a missing single resource hides the error. The nesting case follows the same logic: `GET /users/1/posts` where user 1 has no posts is `200` with `[]`, but `GET /users/999/posts` where user 999 does not exist is `404`.

#### Path variable tests

| Test | Example | Expected outcome |
|------|---------|------------------|
| Valid id | `/users/3` | `200` and user 3 |
| Non-existent id | `/users/99999` | `404` |
| Wrong type | `/users/abc` | `400` or `404`, never `500` |
| Decimal | `/users/1.5` | `400` or `404` |
| Zero | `/users/0` | `404` or `400` |
| Negative | `/users/-1` | `400` or `404` |
| Boundary (last valid) | `/users/10` on a 10-user system | `200` |
| Boundary (one past) | `/users/11` | `404` |
| Very large | `/users/99999999999999999999` | Clean `4xx` (watch for integer overflow `500`) |
| Leading zeros | `/users/003` | Documented behaviour; same as `/users/3`, or `400` |
| Whitespace | `/users/%20` | Clean `4xx` |
| Special characters | `/users/1;DROP` | Clean `4xx`, no stack trace |
| Encoded slash | `/users/1%2F2` | Clean `4xx`, not a server error |
| Wrong case | `/Users/3` | Per documentation (commonly `404`) |
| Trailing slash | `/users/3/` | Consistent with documentation |
| Wrong owner | `/users/1/orders/7` where order 7 belongs to user 2 | `404` or `403`, never the order |

#### Query parameter tests

| Test | Example | Expected outcome |
|------|---------|------------------|
| Valid filter | `?userId=1` | Only user 1's items |
| Filter, no matches | `?userId=999` | `200` and `[]` |
| Misspelled name | `?userld=1` (lowercase L) | Documented: ignored or `400`; make sure your test notices |
| Unknown parameter | `?foo=bar` | Ignored or `400`, per documentation |
| Multiple filters | `?userId=1&completed=true` | Both applied (AND) |
| Order independence | `?a=1&b=2` vs `?b=2&a=1` | Same result |
| Invalid type | `?_limit=abc` | `400` |
| Empty value | `?userId=` | Documented behaviour |
| Name only | `?userId` | Documented behaviour |
| Duplicate | `?userId=1&userId=2` | Documented behaviour; varies |
| Case of name | `?USERID=1` | Usually not matched |
| Case of value | `?status=OPEN` | Documented behaviour |
| Huge value | `?q=` followed by 10,000 characters | `414 URI Too Long` or `400`, not a crash |
| Special characters | `?q=%00`, `?q=%27`, `?q=%3Cscript%3E` | Handled safely |
| Unicode | `?q=caf%C3%A9` | Returns "café" matches |
| Double encoding | `?q=%2520` | Treated as the literal text `%20` |

The `414 URI Too Long` status is a real response code that servers use when the URL exceeds a limit (often around 8 KB, though this varies); long search strings are a legitimate test.

#### Boundary values

A **boundary value** is a value at, just below and just above a limit. If `limit` is documented as 1 to 50, then the interesting values are 0 (just below), 1 (lowest valid), 2, 49, 50 (highest valid) and 51 (just above). Developers make off-by-one errors with `<` versus `<=`, so the edges are where bugs hide. Pick the boundary values from the documentation, then add the unexpected ones: `-1`, a decimal such as `10.5`, and a huge number.

#### Type confusion

Because everything arrives as text, try sending the wrong type: a word where a number is expected, a decimal where an integer is expected, a number where a word is expected, the literal text `null`, `true`, `undefined`, and `NaN`. The aim is to see a clean `400` with a clear message rather than `500`, an empty result, or silent acceptance.

#### Pagination edge cases

| Case | Example | What to check |
|------|---------|---------------|
| First page | `page=1` | Equals default (no page parameter) |
| Page zero | `page=0` | `400`, or treated as 1; documented |
| Negative page | `page=-1` | `400`; never a negative offset error |
| Last page | `page=5` with 95 items, limit 20 | 15 items |
| Exact multiple | 100 items, limit 20, `page=5` | 20 items, and `page=6` is empty |
| Beyond the end | `page=6` | Empty list, `200` (usually) |
| Limit zero | `limit=0` | `400`, or empty, but not "return everything" |
| Limit negative | `limit=-1` | `400` |
| Limit above maximum | `limit=51` when max is 50 | `400` or capped to 50; documented |
| Huge limit | `limit=1000000` | Not a crash or a slow dump of the database |
| No overlap | Pages 1 and 2 | No item appears twice |
| No gaps | Pages 1 to N joined | Together equal the full collection |
| Default limit | No `limit` | Documented default |
| Metadata | Total count or next cursor | Matches reality |

#### Ordering stability

If you sort by a field where many items share a value (for example sorting products by `category`), the order **within** each group may be unspecified. A server that does not use a secondary sort key may return the same item on page 1 and again on page 2, or skip another, because the tie order changes between requests. To test it, sort by a non-unique field, fetch all pages, and check that you receive each item exactly once. Also check that repeating the *same* request gives the *same* order.

#### Order of operations

Verify that filtering, sorting and paging are applied in the right sequence: filter first, then sort, then page. If paging happened before filtering, page 1 might contain only two matches and a mostly empty list while page 2 held more. Combine all three in one request and check each property.

#### Unknown parameters and strictness

Some servers silently ignore unknown parameters (lenient), and some reject them with `400` (strict). Neither is inherently wrong, but silent ignoring has a testing consequence: a typo in your own test (`?usrId=1`) will pass the status check and return everything. This is why your tests must assert on content, not just status.

---

### Part 11: Security Awareness

Parameters come from outside the system, so they are **untrusted input**. You are not expected to become a security specialist this week, but a competent tester recognises these risks and includes a few safe probes in their suites.

**Injection.** If a server builds a database query by gluing the parameter value into a string, an attacker can change the meaning of the query. The classic probe is `' OR '1'='1`, which in a vulnerable system turns a search into "match everything". Encoded in a URL it looks like `?q=%27%20OR%20%271%27%3D%271`. A secure server returns a normal result (probably nothing found) or a `400`, and never a database error message, a stack trace, or a surprising flood of data. Similar probes use `<script>alert(1)</script>` to check whether the value is reflected back unescaped in a page (cross-site scripting), and `../../etc/passwd` in a path variable to check for path traversal. Only run such probes against systems you are authorised to test, and never against someone else's production service.

**Insecure Direct Object Reference (IDOR).** If an API lets you read `/orders/9001` and the server never checks that order 9001 belongs to *you*, you can simply try `/orders/9002`, `/orders/9003` and read other customers' data. Sequential, guessable ids make this trivial. Test it by authenticating as one user and requesting resources owned by another; the correct answer is `403` or `404`. This is a path-variable problem and one of the most common serious API vulnerabilities. (Authentication itself is covered later in the week.)

**Sensitive data in URLs.** URLs are not private. They appear in browser history, server access logs, proxy logs, analytics tools and the `Referer` header sent to other sites. Therefore never put passwords, API keys, session tokens or personal data such as national ID numbers in a path or query string. `GET /login?user=ada&password=secret` is a defect even if it works, because that password is now written in every log along the route. Secrets belong in headers or request bodies, which you will study in the next lesson. As a tester, when you see a token in a URL, raise it.

**Information leakage in errors.** A malformed parameter should produce a short, generic message. A response containing a file path, SQL fragment or class name tells an attacker about the system and is itself a defect.

---

### Part 12: Realistic Scenarios

**Scenario 1: The silently ignored filter.** A tester writes `GET /orders?statuss=shipped` (a typo) and checks only that the status is `200`. The test passes forever, and the filter was never applied. When the real application sends the correct name, the API had a genuine bug in filtering, but nobody noticed because the test was meaningless. *Lesson:* assert on content. After requesting `status=shipped`, loop through the results and check every `status` is `shipped`, and also assert the array is not empty.

**Scenario 2: The ampersand in a company name.** A customer search for `AT&T` returns thousands of unrelated customers. The front-end developer built the URL by string concatenation: `/customers?name=AT&T`. The server read `name=AT` and a separate parameter `T`. The fix was to encode the value as `AT%26T`. *Lesson:* always encode values; as a tester include `&`, `=`, `#`, `+` and `%` in search tests.

**Scenario 3: The disappearing last item.** A mobile app downloads a catalogue with `limit=20` and pages until it receives an empty page. A catalogue of exactly 100 items shows only 80. The server computes `totalPages = floor(100 / 20) = 5`, but its page indexing starts from 0, so page 5 does not exist and the last 20 items are never delivered. *Lesson:* test the exact-multiple boundary and the last page, and compare the union of all pages against the full collection.

**Scenario 4: Someone else's invoice.** A customer notices that their invoice URL ends in `/invoices/1043`. Changing the number to `1044` shows a stranger's invoice with an address and amount. The server checked that the user was logged in, but never that invoice 1044 belonged to them. *Lesson:* for every path variable that identifies a user-owned resource, test with a valid id belonging to a different user. This is IDOR, and it is a high-severity defect.

**Scenario 5: Sorting before limiting.** A leaderboard endpoint `GET /scores?sort=points&order=desc&limit=10` should return the top ten. A tester notices a player with 9,500 points missing. The server fetched the first ten rows from the database in id order, then sorted those ten. *Lesson:* check that the top-N result really holds the extreme values: compare against a request with a large limit sorted by the same field and confirm the first ten match.

**Scenario 6: The case-sensitive category.** The documentation lists `category=books`. The mobile app sends `category=Books` and receives `200` with `[]`, so the "Books" tab appears empty. The server compares strings case-sensitively. Nobody wrote a test for case. *Lesson:* test mixed case for string filters and agree on the rule with the team (normalise to lower case on the server, or document it).

**Scenario 7: The page parameter that vanished.** After a refactoring, `page` was renamed to `pageNumber` on the server, but the client still sends `page=2`. The server ignores unknown parameters, so every request returns page 1 and the app loops forever. *Lesson:* a pagination test should confirm page 2 differs from page 1, and the "no overlap" test would have caught this in seconds.

---

### Part 13: Common Mistakes and Why They Happen

**Forgetting to quote a URL in the shell.** The `&` is interpreted as a command separator, so only the first parameter is sent and a mysterious "command not found" message appears. *Why:* the shell parses the line before curl runs. *Fix:* quote the URL (single quotes in bash, double in cmd).

**Using `curl` in Windows PowerShell and getting strange output.** *Why:* `curl` is an alias for `Invoke-WebRequest`. *Fix:* use `curl.exe`.

**Typing `#` in a value.** Everything after it vanishes. *Why:* the fragment is never sent. *Fix:* encode as `%23`.

**Typing a literal `+` and expecting a plus sign.** It arrives as a space. *Why:* `+` means space in query strings. *Fix:* encode as `%2B`.

**Encoding the whole URL.** The request breaks because `?`, `=`, `&` and `/` are encoded too. *Why:* only values (and names) should be encoded, not the structural characters. *Fix:* use the Params table or `--data-urlencode`.

**Double encoding.** A value contains `%2520` and the server sees `%20`. *Why:* two layers each encoded the text. *Fix:* encode exactly once; inspect the request in the Postman Console or with `curl -v`.

**Leaving a Postman path variable empty.** The request goes to `/users/:userId`. *Why:* Postman sends the text literally when no value is supplied. *Fix:* fill the Value column.

**Asserting only the status code.** A broken filter passes. *Why:* `200` means only that the request was accepted. *Fix:* assert on the response data, and guard against vacuous passes with a non-empty check.

**Confusing `404` with "no results".** *Why:* both feel like "nothing found". *Fix:* remember the collection-versus-single-resource rule.

**Assuming parameter order matters (or does not).** Test it instead of guessing.

**Assuming repeated parameters work the same everywhere.** *Why:* the standard does not define their meaning. *Fix:* read the documentation and test it for your API.

**Trusting default limits.** A test that omits `limit` gets the default page size, which may change. *Fix:* set `limit` explicitly in tests that count items.

**Putting secrets in the URL.** *Why:* it is convenient. *Fix:* use headers or the body; URLs are logged.

---

### Part 14: Where This Connects

You have now met the two URL inputs that appear in nearly every request. In the lessons that follow today you will see **headers**, which carry metadata such as content type and credentials, and **Postman variables and environments**, which let you replace fixed values like `3` or the base URL with `{{userId}}` and `{{baseUrl}}`. On Tuesday you will send the same parameters from Python code using the Requests library (it accepts a dictionary of parameters and does the encoding for you), and on Wednesday you will run one test against many parameter combinations read from files. For now, practise with Postman and curl so the ideas are solid.

---

## Practice Exercises

Try each exercise yourself before reading the solution. Use a terminal and Postman.

### Exercise 1: Classify the parts

Given `https://api.example.com/v1/stores/12/products?inStock=true&sort=price#top`, identify the scheme, host, path, path variable, query string, each query parameter, and the fragment. State which parts the server receives.

**Solution.** The scheme is `https` and the host is `api.example.com`. The path is `/v1/stores/12/products`. The path variable is `12` (the store id); `v1`, `stores` and `products` are fixed segments. The query string is `inStock=true&sort=price`, made of two parameters: `inStock` with value `true`, and `sort` with value `price`. The fragment is `top`. The server receives the request target `/v1/stores/12/products?inStock=true&sort=price` plus the host in the `Host` header. It does **not** receive `#top`.

### Exercise 2: Nested path versus filter

Fetch comments for post 7 on JSONPlaceholder in two ways: using the nested path and using a filter on the `comments` collection. Compare the results.

**Solution.**

```bash
curl "https://jsonplaceholder.typicode.com/posts/7/comments"
curl "https://jsonplaceholder.typicode.com/comments?postId=7"
```

Both return the same five comments, each with `postId` equal to 7. The first is a path-based address (the parent is part of the path); the second is a filter on the whole `comments` collection. You can verify equality in Postman by saving both bodies and comparing the ids. The exercise shows that two designs can expose the same data, and your tests should check each one the documentation promises.

### Exercise 3: Verify a combined filter

Request `https://jsonplaceholder.typicode.com/todos?userId=1&completed=true`. Write a Postman test that proves every item has `userId` equal to 1 **and** `completed` equal to `true`, and that the result is not empty.

**Solution.**

```javascript
pm.test("Every todo is user 1 and completed", function () {
    const todos = pm.response.json();
    pm.expect(todos).to.be.an("array").that.is.not.empty;
    todos.forEach(function (todo) {
        pm.expect(todo.userId).to.eql(1);
        pm.expect(todo.completed).to.eql(true);
    });
});
```

The first expectation guards against a vacuous pass. Inside the loop, `eql(1)` checks the number and `eql(true)` checks the boolean, not the string `"true"`. If any single todo fails either assertion, the test fails and Postman reports which one.

### Exercise 4: Probe unusual limits

Request `/posts?_limit=0`, `/posts?_limit=-1` and `/posts?_limit=abc` on JSONPlaceholder, and record the status code and the number of items returned for each. Decide whether each behaviour is acceptable.

**Solution.** Run each request in Postman and note the status and `length` of the body (you can see the array length with `pm.response.json().length` in the Console). JSONPlaceholder is a lenient fake API and its handling of these values may differ from what a strict production API would do; record what you observe rather than assuming. A well-designed real API should return `400` for `-1` and `abc`, and should either return `400` or an empty list for `0`; it should never treat `0` as "no limit" and return everything. The exercise teaches you to write down the *actual* behaviour and compare it against the documented rule. For a public practice API with no stated rule, your finding is "undocumented; lenient".

### Exercise 5: Encode and decode

(a) Encode `black & white #1`. (b) Encode `100% café`. (c) Decode `a%2Bb%3Dc`.

**Solution.** (a) `black%20%26%20white%20%231`. (b) The `%` becomes `%25`, the space becomes `%20`, and `é` becomes `%C3%A9`: `100%25%20caf%C3%A9`. (c) `%2B` is `+`, `%3D` is `=`, so the result is `a+b=c`. You can check your answers by sending them to httpbin: `curl -G https://httpbin.org/get --data-urlencode "q=100% café"` and reading `args` and `url` in the response.

### Exercise 6: See how repeated parameters are parsed

Send `https://httpbin.org/get?tag=a&tag=b&tag[]=c&list=1,2` and describe how httpbin interprets each.

**Solution.**

```bash
curl "https://httpbin.org/get?tag=a&tag=b&tag[]=c&list=1,2"
```

If curl complains about brackets, add `-g`: `curl -g "..."`. In `args` you should see `tag` as a list `["a", "b"]`, a separate key named `tag[]` with value `"c"`, and `list` as the single string `"1,2"`. This shows that httpbin understands the repeated-name style, treats `tag[]` as just another name (it has no special bracket handling), and does **not** split on commas. If your API expected bracket or comma style, you would have to rely on its documentation. The lesson: the parsing convention belongs to the server, not to HTTP.

### Exercise 7: Pagination arithmetic

A collection has 237 items. (a) With `limit=25`, how many pages exist and how many items are on the last page? (b) With offset pagination and `limit=25`, which `offset` returns the last page? (c) Which items (by position) does `page=4&limit=25` return? (d) What should `page=11` return?

**Solution.** (a) `totalPages = ceil(237 / 25) = ceil(9.48) = 10`. Nine full pages hold `9 * 25 = 225` items, so the last page holds `237 - 225 = 12`. (b) The last page starts after 225 items, so `offset = 225`; it matches `(10 - 1) * 25 = 225`. (c) `offset = (4 - 1) * 25 = 75`, so positions 76 to 100. (d) Page 11 is beyond the end, so it should return an empty list (`200` with `[]` in most APIs) or a documented `4xx`; it must not return the last page again or a server error.

### Exercise 8: Test the pagination of JSONPlaceholder

Using `_page` and `_limit`, prove in Postman that fetching pages 1 to 10 of size 10 reproduces all 100 posts exactly once.

**Solution.** One approach uses a collection runner or a single script that sends ten requests:

```javascript
const base = "https://jsonplaceholder.typicode.com/posts?_limit=10&_page=";
let allIds = [];
let finished = 0;

pm.test("Ten pages of 10 contain 100 unique posts", function (done) {
    for (let page = 1; page <= 10; page++) {
        pm.sendRequest(base + page, function (err, res) {
            allIds = allIds.concat(res.json().map(function (p) { return p.id; }));
            finished++;
            if (finished === 10) {
                pm.expect(allIds).to.have.lengthOf(100);
                pm.expect(new Set(allIds).size).to.eql(100);
                done();
            }
        });
    }
});
```

The explanation: we start with an empty list `allIds` and a counter `finished`. The loop fires ten asynchronous requests (one per page). In each callback we append that page's ids and increase the counter. When the counter reaches 10 (all responses received), we assert two things: the total number of ids is 100 (no gaps), and the number of **unique** ids is also 100 (no duplicates), because `new Set(allIds).size` counts distinct values. Then `done()` ends the test. Because the responses may arrive in any order, we do not rely on order here.

### Exercise 9: Missing versus empty

Request `/posts?userId=999`, `/posts/999`, `/users/999/posts` and `/users/1/posts` on JSONPlaceholder. Predict, then verify, the status code and body of each.

**Solution.** `/posts?userId=999` is a filter with no matches, so `200` and `[]`. `/posts/999` asks for a single resource that does not exist, so `404` (with `{}` as the body on this service). `/users/1/posts` returns user 1's posts, `200` with a list of ten. `/users/999/posts` is a nested route under a user that does not exist; on JSONPlaceholder this returns an empty list `200 []`, which is more lenient than a strict REST design (strictly, a missing parent should be `404`). Note this as a real-world inconsistency that you would log in a production API: the rule is "missing parent resource is `404`", and the fake API does not follow it. If your observed result differs, record exactly what you saw.

### Exercise 10: Build a Postman request with both kinds

In Postman, create a request to `https://jsonplaceholder.typicode.com/users/:userId/todos` with `userId` = 2, query parameters `completed=false` and `_limit=5`. Use Bulk Edit to enter the query parameters, then disable `completed` and compare.

**Solution.** Type the URL with `:userId`; fill the Path Variables table with `userId` = `2`. Open Bulk Edit and paste `completed:false` and `_limit:5` on separate lines; Key-Value Edit shows two rows. The final URL is `.../users/2/todos?completed=false&_limit=5`. Send it and confirm up to 5 todos, all with `completed` equal to `false`. Untick the `completed` row, and Send again: now todos with both values appear (up to 5). The URL bar loses `completed=false`. This confirms the checkbox removes the parameter from the request, which is exactly how you test "parameter absent".

---

## Self-Check Quiz

Answer each question before looking at the answers.

1. In `/orders/9001/items?sort=price`, which part is the path variable and which is a query parameter?
2. Which part of a URL is never sent to the server?
3. What is the percent-encoded form of `&`, and why does it matter inside a value?
4. A request `GET /products?category=books` finds no matches. What status and body should the server return? What about `GET /products/99999` for a missing product?
5. With 95 items and `limit=20`, how many items are on the last page?
6. Name three common ways to send multiple values for one parameter.
7. Why should a test for a filter check the response body and not only the status code?
8. In Windows PowerShell, why might `curl` not behave like the curl in the lesson?
9. Why is `GET /login?user=ada&password=secret` a defect?
10. What does `-G` do in `curl -G --data-urlencode "q=a b"`?
11. In Postman, what happens if you use `:userId` in a URL but leave the value blank?
12. What is an IDOR, and which kind of URL input does it usually involve?

### Answers

1. `9001` is the path variable (an order id); `items` is a fixed segment. `sort=price` is the query parameter.
2. The fragment (everything after `#`). The client keeps it.
3. `%26`. An unencoded `&` is read as the separator between parameters, so the value would be cut off and the remainder would be parsed as a new, unintended parameter.
4. `200` with an empty list `[]`, because the collection exists. `GET /products/99999` for a missing product returns `404`.
5. `95 - (4 * 20) = 15` items; there are `ceil(95 / 20) = 5` pages.
6. Repeated names (`id=1&id=2`), bracket suffix (`id[]=1&id[]=2`) and comma-separated (`id=1,2`).
7. Because `200` only shows the request was accepted. A misspelled or ignored filter still returns `200` with unfiltered data. Checking the content proves the filter was applied.
8. Because `curl` is an alias for `Invoke-WebRequest`; use `curl.exe`.
9. Credentials in a URL are recorded in history, logs and referrer headers, so they leak. Secrets belong in headers or bodies.
10. `-G` appends the data to the URL as a query string (and uses `GET`) instead of sending it as a body; `--data-urlencode` percent-encodes the value, so the request is `?q=a%20b`.
11. Postman sends the literal text `:userId` in the path, and the server typically returns an error such as `404` or `400`.
12. Insecure Direct Object Reference: an authenticated user reads or changes another user's data by changing an identifier. It usually involves path variables (ids).

---

## Summary

A **path variable** is a segment of the URL path that identifies a specific resource (`/users/42`); it is normally required, only its value is sent, and its position gives it meaning. A **query parameter** is a `name=value` pair after `?`, joined with `&`, that filters, searches, sorts, pages or shapes a result, and is normally optional. The fragment after `#` never reaches the server.

Servers split the query string on `&` and `=`, percent-decode it, and treat everything as text, so validation of type and range is the application's responsibility, and the best place for a tester to look for bugs. Repeated parameters have no single standard meaning; the three common conventions are repeated names, bracket suffix and comma-separated lists. Missing, empty and name-only parameters are three distinct cases.

Pagination comes in page/limit, offset/limit and cursor styles, with arithmetic you must be able to do by hand (`offset = (page - 1) * limit`, `totalPages = ceil(total / limit)`). Special characters in values must be percent-encoded exactly once; reserved characters such as `& = # + % /` and all non-ASCII text need particular care.

A filter with no matches returns `200` and `[]`, while a missing single resource returns `404`. Choose a path variable when the value identifies the resource and a query parameter when it changes the view of it. Use `-G --data-urlencode` in curl and the Params table in Postman to let the tools do the encoding, quote URLs correctly for your shell, and write tests that check the response data, not just the status code. Test boundaries, wrong types, empty and duplicate values, unknown parameters, huge values, injection strings and pagination edge cases, and watch for security problems such as IDOR and secrets in URLs.

---

## Glossary

**Base URL**: the constant front part of an API address, such as `https://api.example.com/v1`.

**Boundary value**: a value at or next to a documented limit, such as 0, 1, 50 and 51 for a limit of 1 to 50.

**Cursor**: an opaque token returned by the server that marks the position from which the next page should start.

**Encoding (percent-encoding)**: writing a character as `%` followed by two hexadecimal digits, so that it can travel safely in a URL.

**Fragment**: the part of a URL after `#`, used by clients only and never sent to the server.

**IDOR (Insecure Direct Object Reference)**: a flaw where changing an identifier lets a user reach data that belongs to someone else.

**Offset**: the number of items to skip before returning results.

**Opaque**: a value the client must not interpret or construct, only pass back unchanged.

**Pagination**: splitting a large collection into smaller pages returned one at a time.

**Path**: the part of a URL after the host and before `?`, identifying a resource.

**Path variable (path parameter)**: a segment of the path whose value identifies a specific resource.

**Query parameter**: a `name=value` pair in the query string that filters, sorts, pages or shapes a response.

**Query string**: everything after the first `?` and before any `#`.

**Request target**: the path plus query string, as written in the first line of an HTTP request.

**Reserved character**: a character such as `? & = # /` that has structural meaning in a URL.

**Segment**: one piece of a path between slashes.

**Unreserved character**: a letter, digit, or one of `- . _ ~`, which never needs encoding.

**UTF-8**: the standard way of turning any character into one to four bytes, used before percent-encoding non-ASCII text.

---

## Additional Resources

- MDN Web Docs, *What is a URL?*: https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/What_is_a_URL
- Postman Docs, *Send parameters with API requests*: https://learning.postman.com/docs/sending-requests/create-requests/parameters/
- JSONPlaceholder guide (filtering, nested resources, paging and sorting): https://jsonplaceholder.typicode.com/guide/
- curl documentation, *Everything curl* (the `-G` and `--data-urlencode` options): https://everything.curl.dev/
- httpbin, a service that echoes requests, for experiments: https://httpbin.org/
