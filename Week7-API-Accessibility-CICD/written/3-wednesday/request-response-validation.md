# Request and Response Validation

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the idea of **contract testing** and why validating requests and responses protects you from API drift.
- Write JSON Schemas using types, `required`, `properties`, `additionalProperties`, `enum`, `pattern`, `minimum`/`maximum`, `minLength`, `items`/`minItems`, nullable type arrays, `oneOf`/`anyOf`, `$ref`/`$defs` and `format`.
- Validate a **request** payload before sending it and a **response** after receiving it.
- Use `Draft202012Validator`, `iter_errors` and `best_match` to produce readable error reports.
- Model responses as typed Python objects with **Pydantic** (`BaseModel`, `Field`, validators, `model_validate`, `ValidationError`, `model_dump`).
- Choose between a schema and a model, and describe the basics of an **OpenAPI** document.
- Write **negative validation** tests (400/422), keep schemas in a shared `schemas/` folder, and reason about schema versioning and backward compatibility.
- Recognise the common pitfalls: over-strict schemas and brittle tests.

---

## Why This Matters

This week's epic is to build an API test suite that a whole team can trust, run automatically, and keep healthy as the product changes. On Monday you explored APIs and sent requests; on Tuesday you checked status codes, used the basic `jsonschema` `validate()` call and wrote field-by-field assertions. Earlier today you organised that work into reusable pieces. Now we make validation **systematic**.

Picture this real scenario. A backend developer renames `userName` to `username` in a release. The mobile app, which reads `userName`, shows blank profiles. Your test suite was green, because your tests only asserted `status_code == 200` and one or two fields. A schema check on every response would have failed on the first run, with a message pointing at the exact field.

The reverse problem exists too. You write a test that posts a user, but you mistype `emial` in the payload. The server returns 400 and the test fails. Is the server broken, or is your test? If you validate your own request first, you know immediately: your test has a bug, not the API.

Validation gives you **early detection** of breaking changes, **clear failure messages**, and a **shared definition** of "correct". Later this week these checks will run unattended in a pipeline; for now, we build them.

---

## The Concept

### 1. The Contract Testing Idea

**What it is.** An API **contract** is the written agreement between the provider (the service) and its consumers (apps, other services, your tests). It says which endpoints exist, what you may send, and what you will get back, including error shapes.

**Why it matters.** Without a contract, "correct" lives in people's heads. With one, anyone can check a response mechanically.

**How it works.** A *contract test* takes a response and asks: "does this honour the agreement?" It does not care about business behaviour in depth (that is what your functional tests do). It only checks the **shape and rules of the data**: field names, types, which are required, allowed values, and ranges.

**When to use it.** On every response your suite receives, ideally automatically inside your API client helper. Because the check is cheap, you get free coverage: even a test written to check pagination will notice a broken `user` shape.

Two directions exist:

| Direction | You validate | Purpose |
|-----------|--------------|---------|
| **Request validation** | What you send | Positive tests: prove your test built a valid request. Negative tests: you *skip* this on purpose |
| **Response validation** | What you receive | Prove the server honoured the contract, success or error |

The subtle point: in a positive test, validate the request **before** sending, so a failure is unambiguous. In a negative test, deliberately send the invalid data, and then validate that the **error response** is itself well-formed.

### 2. JSON Schema in Depth

**JSON Schema** is a language-neutral way to describe JSON data, written as JSON. You saw a basic version on Tuesday. Here is the full toolkit, introduced one keyword at a time. We use **Draft 2020-12**, the current version, and Python's `jsonschema` library.

#### 2.1 Types

```python
{"type": "string"}      # "hello"
{"type": "integer"}     # 5   (not 5.5)
{"type": "number"}      # 5 or 5.5
{"type": "boolean"}     # true / false
{"type": "array"}       # [1, 2]
{"type": "object"}      # {"a": 1}
{"type": "null"}        # null
```

JSON Schema `integer` and `number` are about JSON values. In Python, note that `True` is technically an `int`, but `jsonschema` correctly treats booleans as **not** integers, so `{"type": "integer"}` rejects `true`.

#### 2.2 Objects: `properties`, `required`, `additionalProperties`

```python
USER_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["id", "name", "email"],
    "properties": {
        "id":    {"type": "integer", "minimum": 1},
        "name":  {"type": "string", "minLength": 1, "maxLength": 100},
        "email": {"type": "string", "format": "email"},
        "age":   {"type": ["integer", "null"], "minimum": 0, "maximum": 120},
        "role":  {"enum": ["admin", "member", "guest"]},
        "phone": {"type": "string", "pattern": "^\\+?[0-9]{7,15}$"},
        "tags":  {"type": "array", "items": {"type": "string"}, "uniqueItems": True}
    },
    "additionalProperties": False
}
```

Line by line:

- `"$schema"` declares the draft, so tools know which rules apply.
- `"type": "object"` says the root must be a JSON object.
- `"required"` lists keys that **must be present**. This is the most commonly misunderstood keyword: `properties` alone does **not** make a field required. A schema with properties but no `required` accepts `{}`.
- `"properties"` describes each known key. If a key is present, it must match its sub-schema.
- `"id"`: an integer, minimum 1. `minimum` and `maximum` are inclusive; `exclusiveMinimum` and `exclusiveMaximum` are strict.
- `"name"`: a string of 1 to 100 characters (`minLength`, `maxLength` count characters).
- `"email"`: `format` is an annotation for common patterns. See section 2.6 for an important caveat.
- `"age"`: `"type": ["integer", "null"]` is how you express a **nullable** field in modern JSON Schema: the value may be an integer or `null`. (Older OpenAPI 3.0 used `nullable: true`; do not use that in a 2020-12 schema.)
- `"role"`: `enum` lists the only allowed values, ideal for status fields.
- `"phone"`: `pattern` is a regular expression, matched anywhere in the string unless you anchor it with `^` and `$`, which you almost always should.
- `"tags"`: an array whose elements are strings (`items`), with no duplicates (`uniqueItems`).
- `"additionalProperties": False` rejects any key not listed in `properties`. Powerful, but see the pitfalls section before using it everywhere.

#### 2.3 Arrays: `items`, `minItems`, `maxItems`

```python
USERS_LIST_SCHEMA = {
    "type": "array",
    "minItems": 1,
    "maxItems": 100,
    "items": USER_SCHEMA
}
```

`items` is the schema **every element** must satisfy. `minItems` and `maxItems` bound the length. Use `minItems: 1` only when the contract promises a non-empty list; an empty search result is usually valid.

#### 2.4 Choices: `oneOf`, `anyOf`, `allOf`

```python
PAYMENT_SCHEMA = {
    "type": "object",
    "required": ["method"],
    "oneOf": [
        {"properties": {"method": {"const": "card"}},
         "required": ["method", "cardLast4"]},
        {"properties": {"method": {"const": "bank"}},
         "required": ["method", "iban"]}
    ]
}
```

- `oneOf`: the data must match **exactly one** sub-schema. Matching two is a failure, which surprises beginners.
- `anyOf`: at least one must match. This is the safer choice when the options can overlap.
- `allOf`: **all** must match, used for combining a base schema with extras.

Here a card payment must carry `cardLast4` and a bank payment must carry `iban`. `const` means "exactly this value".

#### 2.5 Reuse: `$defs` and `$ref`

Repeating the same address shape in five places invites drift. Define it once and reference it.

```python
ORDER_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["id", "shipping", "billing"],
    "properties": {
        "id": {"type": "integer"},
        "shipping": {"$ref": "#/$defs/address"},
        "billing":  {"$ref": "#/$defs/address"}
    },
    "$defs": {
        "address": {
            "type": "object",
            "required": ["street", "city"],
            "properties": {
                "street": {"type": "string"},
                "city":   {"type": "string"}
            }
        }
    }
}
```

`$defs` is a holding area for named sub-schemas. `{"$ref": "#/$defs/address"}` means "use the schema found at this path inside the current document" (`#` is the document root). If the address rules change, you edit one place. Across files you can also reference another file, for example `"$ref": "address.json"`, though that needs a resolver (the `referencing` library) and is easier to start without.

#### 2.6 Formats

`format` describes common string shapes: `email`, `uuid`, `date`, `date-time`, `uri`, `ipv4`. A critical beginner trap: in `jsonschema`, **formats are not checked unless you ask**. By default `format` is only an annotation.

```python
from jsonschema import Draft202012Validator

validator = Draft202012Validator(
    USER_SCHEMA,
    format_checker=Draft202012Validator.FORMAT_CHECKER,
)
```

Even then, some formats (such as `date-time` and `uri`) need optional extra packages installed to be enforced. A format that silently is not enforced gives false confidence, so test your schema with a deliberately bad value to confirm it really fails. When it matters and a format is unreliable, add an explicit `pattern`.

#### 2.7 Validating with `Draft202012Validator`

On Tuesday you used the one-shot `validate()` function. It stops at the **first** error. For testing, you usually want **all** of them.

```python
from jsonschema import Draft202012Validator

validator = Draft202012Validator(USER_SCHEMA)

bad_user = {"id": 0, "name": "", "email": "ana@example.com", "age": 200, "nickname": "A"}

for error in validator.iter_errors(bad_user):
    print(list(error.absolute_path), "->", error.message)
```

Representative output (order can vary):

```text
['id'] -> 0 is less than the minimum of 1
['name'] -> '' should be non-empty
['age'] -> 200 is greater than the maximum of 120
[] -> Additional properties are not allowed ('nickname' was unexpected)
```

What each part does:

- `Draft202012Validator(schema)` builds a reusable validator object bound to one schema.
- `iter_errors(instance)` yields a `ValidationError` for **every** violation found.
- `error.absolute_path` is the route to the bad value (an empty path means the root object itself).
- `error.message` is a human-readable sentence. Exact wording varies between `jsonschema` versions, so never assert on message text in your tests.

Add `Draft202012Validator.check_schema(schema)` once when loading a schema file. It raises `SchemaError` if **the schema itself** is malformed, so a typo like `"typ": "string"` or `"minimum": "5"` is caught at load time rather than silently ignored.

#### 2.8 Readable Error Reports and `best_match`

For `oneOf` and `anyOf`, `iter_errors` can produce a confusing top-level error ("is not valid under any of the given schemas") and bury the useful detail in `error.context`. The helper `best_match` picks the most relevant error.

```python
from jsonschema import Draft202012Validator
from jsonschema.exceptions import best_match


def format_errors(instance, schema):
    """Return a list of readable lines, one per violation."""
    validator = Draft202012Validator(
        schema, format_checker=Draft202012Validator.FORMAT_CHECKER
    )
    errors = sorted(validator.iter_errors(instance),
                    key=lambda e: [str(p) for p in e.absolute_path])
    return [
        f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
        for e in errors
    ]


def assert_matches_schema(instance, schema, name="schema"):
    problems = format_errors(instance, schema)
    if problems:
        detail = "\n".join(f"  - {p}" for p in problems)
        raise AssertionError(f"Does not match {name}:\n{detail}")


def first_clue(instance, schema):
    """One 'most relevant' error, handy for oneOf/anyOf schemas."""
    err = best_match(Draft202012Validator(schema).iter_errors(instance))
    return None if err is None else err.message
```

Line by line:

- `format_errors` builds a validator **with** format checking turned on, then collects all errors.
- `sorted(..., key=...)` makes output stable. The `str(p)` conversion matters because a path can mix integers (array positions) and strings (keys), and Python cannot compare `1 < "name"`.
- The f-string joins the path parts with `/`, and uses `<root>` for a problem at the top level.
- `assert_matches_schema` raises a single `AssertionError` listing every problem. A test report then shows the whole picture in one run instead of one defect per run.
- `best_match(errors)` takes the iterator of errors and returns the single one a human would find most helpful, or `None` when there are none.

Representative failure message:

```text
AssertionError: Does not match user:
  - age: 200 is greater than the maximum of 120
  - name: '' should be non-empty
```

### 3. Validating the Request Before Sending

**What.** Check your own outgoing payload against the *request* schema before calling the API.

**Why.** If a positive test fails with a 400, you want to know whether the API is wrong or your test data is. Validating first turns "mystery 400" into an obvious test bug.

**How.** Use a **payload builder** that validates by default.

```python
# api/payloads.py
import uuid
from api.validators import assert_matches_schema, load_schema


def new_user(**overrides):
    """A VALID create-user payload. Fails fast if the test itself is wrong."""
    payload = {
        "name": "QA User",
        "email": f"qa+{uuid.uuid4().hex[:8]}@example.com",
        "age": 30,
    }
    payload.update(overrides)
    assert_matches_schema(payload, load_schema("new_user"), "new_user (request)")
    return payload


def raw_user(**fields):
    """An UNVALIDATED payload, for deliberately invalid requests."""
    return dict(fields)
```

Explanation:

- `new_user()` starts from a known-good payload, applies the caller's overrides, then validates the result. A typo such as `new_user(emial="x")` produces `additionalProperties` or `required` failures immediately, before any network call.
- The `uuid` suffix keeps emails unique so tests do not collide with each other (you built data helpers like this earlier).
- `raw_user()` does no checking. Two builders make intent obvious to readers: `new_user()` means "valid by construction", `raw_user()` means "anything goes".

Usage:

```python
def test_create_user(client):
    response = client.post("/users", json=new_user(name="Ana"))
    assert response.status_code == 201
```

**When not to.** Never route negative tests through `new_user()`; the validator would stop you from sending the bad data you intend to send.

### 4. Validating the Response After Receiving

**What.** Run the response body through the *response* schema.

**How.** Combine protocol checks (status code, `Content-Type`) with the schema check. Check the cheap things first, so the first failure explains the most.

```python
# api/validators.py
import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"


def load_schema(name):
    with open(SCHEMA_DIR / f"{name}.json", encoding="utf-8") as f:
        schema = json.load(f)
    Draft202012Validator.check_schema(schema)       # catch typos in the schema itself
    return schema
```

(`assert_matches_schema` from section 2.8 lives in the same module.)

```python
def test_get_user_matches_contract(client):
    response = client.get("/users/1")

    assert response.status_code == 200, response.text
    assert "application/json" in response.headers["Content-Type"]
    assert_matches_schema(response.json(), load_schema("user"), "user (response)")
```

Note `response.text` as the assertion message: when the status is wrong, you see the server's own explanation in the report.

**Real-world scenario.** An `/orders` endpoint started returning `total` as the string `"10.00"` instead of a number. A single schema line, `"total": {"type": "number"}`, flagged it the same day.

### 5. Pydantic Models as Typed Response Models

**What.** **Pydantic** lets you describe data as a Python class with type hints. It validates and **converts** data when you create an object from it.

**Why.** Once parsed, you work with `user.email` instead of `body["email"]`, you get editor autocomplete, and a typo in an attribute name becomes an immediate error instead of a `KeyError` later. Many Python teams find this more natural than raw JSON Schema.

**How.** Install it with `pip install pydantic` (version 2 syntax is used here).

```python
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class User(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    age: Optional[int] = Field(default=None, ge=0, le=120)
    role: str = "member"

    @field_validator("role")
    @classmethod
    def role_must_be_known(cls, value):
        if value not in {"admin", "member", "guest"}:
            raise ValueError(f"unknown role {value!r}")
        return value
```

Line by line:

- `class User(BaseModel)`: inherit from `BaseModel` to get validation.
- `model_config = ConfigDict(extra="forbid")`: reject unknown fields, like `additionalProperties: false`. The default is `"ignore"`, which silently drops extras.
- `id: int = Field(ge=1)`: type `int`, greater than or equal to 1. Other constraints: `gt`, `lt`, `le`, `min_length`, `max_length`, `pattern`.
- `Optional[int] = Field(default=None, ...)`: the field may be `None` and may be omitted. Note a difference from JSON Schema: in Pydantic, a field with a **default** is not required; a field with no default is required.
- `role: str = "member"`: optional with a default.
- `@field_validator("role")`: a custom rule run after the type check. It must **return** the value, or raise `ValueError` (Pydantic turns that into a validation error).

Using it:

```python
payload = {"id": 7, "name": "Ana", "email": "ana@example.com", "age": None}

user = User.model_validate(payload)        # build and validate
print(user.name)                           # attribute access
print(user.model_dump())                   # back to a plain dict
print(user.model_dump(exclude_none=True))  # drop None values
```

Representative output:

```text
Ana
{'id': 7, 'name': 'Ana', 'email': 'ana@example.com', 'age': None, 'role': 'member'}
{'id': 7, 'name': 'Ana', 'email': 'ana@example.com', 'role': 'member'}
```

Handling failure, and cross-field rules:

```python
try:
    User.model_validate({"id": 0, "name": "", "email": "nope", "extra": 1})
except ValidationError as err:
    for item in err.errors():
        print(item["loc"], item["type"])
```

Representative output:

```text
('id',) greater_than_equal
('name',) string_too_short
('email',) string_pattern_mismatch
('extra',) extra_forbidden
```

`err.errors()` returns a list of dictionaries, one per problem, with `loc` (where), `type` (a stable code, safer to assert on than the message) and `msg`. `str(err)` gives a readable multi-line report that is ideal for an assertion message.

For a rule involving several fields, use `@model_validator(mode="after")`, which receives the finished model:

```python
from pydantic import model_validator


class Booking(BaseModel):
    start: int
    end: int

    @model_validator(mode="after")
    def end_after_start(self):
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self
```

**Coercion warning.** By default Pydantic is "lax": the string `"5"` becomes the integer `5`. That is friendly in application code but **hides contract violations** in tests. If the API should return a number and returns a string, you want to know. Use strict mode for contract checks:

```python
class StrictUser(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    id: int
    name: str
```

With this, `StrictUser.model_validate({"id": "7", "name": "Ana"})` raises a `ValidationError`. You can also export the JSON Schema of a model with `User.model_json_schema()`.

In a test:

```python
def test_get_user_parses(client):
    response = client.get("/users/7")
    assert response.status_code == 200
    try:
        user = User.model_validate(response.json())
    except ValidationError as err:
        raise AssertionError(f"Invalid user response:\n{err}") from err
    assert user.id == 7
```

### 6. Schema Versus Model: Trade-Offs

| Question | JSON Schema | Pydantic model |
|----------|-------------|----------------|
| Language-neutral, shareable with front-end and other teams | Yes | No (Python only) |
| Can be generated from or checked against OpenAPI | Directly | With extra tooling |
| Reads like normal Python, gives attribute access | No | Yes |
| Reports **all** errors | `iter_errors` | `ValidationError.errors()` |
| Default behaviour | Strict on types | Lax coercion unless strict |
| Custom logic (cross-field rules) | Awkward | Easy with validators |

**When to choose which.** Use JSON Schema when the contract is shared across teams or languages, or comes from an OpenAPI file. Use Pydantic when you want typed objects to work with, or complex rules. Many teams combine them: schema files for the contract check, Pydantic for convenient access in readable tests. Consistency within one framework matters more than the choice itself. Do not validate every response twice "just in case".

### 7. OpenAPI / Swagger Basics

**What.** **OpenAPI** (formerly Swagger) is the standard format for writing an API contract as YAML or JSON. **Swagger UI** renders it as a clickable web page.

```yaml
openapi: 3.1.0
info:
  title: Demo API
  version: 1.0.0
paths:
  /users:
    post:
      summary: Create a user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewUser'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '422':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
components:
  schemas:
    NewUser:
      type: object
      required: [name, email]
      properties:
        name:  {type: string, minLength: 1}
        email: {type: string}
    User:
      type: object
      required: [id, name, email]
      properties:
        id:    {type: integer}
        name:  {type: string}
        email: {type: string}
    Error:
      type: object
      required: [message]
      properties:
        message: {type: string}
```

How to read it:

- `openapi` and `info` identify the spec version and the API.
- `paths` lists each URL; under each URL, each HTTP method; under each method, the `requestBody` and the `responses` keyed by **status code**.
- `components/schemas` holds reusable definitions, referenced with `$ref`, exactly like `$defs` in plain JSON Schema.
- OpenAPI 3.1 uses full JSON Schema 2020-12 for its schemas, which means everything in section 2 applies. OpenAPI 3.0 used a slightly different dialect (with `nullable: true`), so check which version your team's spec uses.

**Why it matters to a tester.** Each documented status code and schema is a **test candidate**. Postman can import a spec to build a collection (you saw this on Monday).

**Validating responses against a spec.** The idea: instead of copying schemas by hand, load the spec, find the schema for this path, method and status, and validate the response against it. Libraries exist for this: **openapi-core** validates requests and responses against a spec, and **Schemathesis** reads a spec and generates many test requests automatically. They are worth knowing about; for this course we validate with hand-managed schema files, which teaches the same ideas.

A tiny hand-rolled version, so the concept is concrete (this works for a 3.1 spec whose schema uses only local `$ref`s):

```python
def schema_for(spec, path, method, status):
    node = spec["paths"][path][method]["responses"][str(status)]
    schema = node["content"]["application/json"]["schema"]
    # attach components so "#/components/schemas/..." references resolve
    return {**schema, "components": spec["components"]}
```

Because `$ref: '#/components/schemas/User'` points inside the same document, embedding `components` next to the schema lets the reference resolve. For anything beyond a demo, use `openapi-core`.

### 8. Negative Validation: Rejecting Bad Requests

**What.** Prove the API **refuses** invalid input, and refuses it properly.

**Why.** An API that accepts `age: -5` stores bad data forever. Rejection behaviour is part of the contract.

**Which status code.** Both `400 Bad Request` and `422 Unprocessable Content` are common for validation failures, depending on the framework (many Python frameworks use 422). Check your API's documentation and assert the exact code it promises; if it is genuinely undocumented, accept `in (400, 422)` temporarily and raise the ambiguity with the team.

**How.** Use `pytest.mark.parametrize` to try many bad inputs with one test body (a pattern from earlier in the course), and use `raw_user()`.

```python
import pytest

BAD_USERS = [
    pytest.param({"email": "a@example.com"},                      id="missing-name"),
    pytest.param({"name": "Ana"},                                 id="missing-email"),
    pytest.param({"name": "Ana", "email": "not-an-email"},        id="bad-email"),
    pytest.param({"name": "Ana", "email": "a@example.com", "age": -5},  id="negative-age"),
    pytest.param({"name": "", "email": "a@example.com"},          id="empty-name"),
    pytest.param({"name": "Ana", "email": "a@example.com", "age": "x"}, id="age-wrong-type"),
]


@pytest.mark.parametrize("payload", BAD_USERS)
def test_invalid_user_is_rejected(client, payload):
    response = client.post("/users", json=raw_user(**payload))

    assert response.status_code in (400, 422), response.text
    assert "application/json" in response.headers.get("Content-Type", "")
    assert_matches_schema(response.json(), load_schema("error"), "error")
    assert "Traceback" not in response.text
```

What it proves: the status is a client error (not 500, which would mean the server crashed on bad input), the error has the documented shape, and no stack trace leaks. The `id=` labels make failing cases readable: `test_invalid_user_is_rejected[negative-age]`.

Also verify nothing was created: after a rejected POST, a follow-up `GET`/list should not contain the bad record.

### 9. Shared Schema Files in `schemas/`

Keep schemas as `.json` files in version control:

```text
schemas/
├── new_user.json     # request schema
├── user.json         # response schema
├── users_list.json
├── order.json
└── error.json
```

Benefits: one source of truth for every test; schema changes show up in code review; non-Python teammates can read them. The `load_schema` function from section 4 is the single entry point, so tests never embed schema dictionaries inline.

Example `schemas/error.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["message"],
  "properties": {
    "message": {"type": "string", "minLength": 1},
    "details": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["field"],
        "properties": {"field": {"type": "string"}, "issue": {"type": "string"}}
      }
    }
  }
}
```

Notice the error schema does **not** set `additionalProperties: false`. Error bodies often grow extra helpful fields (`code`, `traceId`), and forbidding them would break tests for no benefit.

### 10. Schema Versioning and Backward Compatibility

APIs evolve; your schemas must evolve with them without breaking everyone.

**Backward-compatible (safe) changes**, which old consumers survive:

- Adding a new **optional** field to a response.
- Adding a new value to an input `enum`.
- Loosening a limit (`maxLength` 50 to 100) on a request.

**Breaking changes**, which need a new API version:

- Removing or renaming a response field.
- Changing a field's type (`integer` to `string`).
- Making an optional request field **required**.
- Removing an `enum` value from a response, or tightening a request rule.

**How to manage it.**

1. Change the schema file in the **same merge request** as the API change, so the diff shows exactly what moved.
2. When the API has versions (`/v1/users`, `/v2/users`), keep matching schema files (`user_v1.json`, `user_v2.json`) and keep running the old one while v1 is supported.
3. Use a tolerant schema for fields you do not own, and a strict one for fields you do.

**Contract drift** is when the real API changes and tests, docs or mocks do not. A schema check on every response is your main defence. Later this week, the CI/CD lessons show how to run these checks on every change automatically.

### 11. Common Pitfalls

**Over-strict schemas.** Setting `additionalProperties: false` everywhere means that when the backend adds a harmless new field, every test fails. Reserve it for cases where leaking an extra field would be a real problem (for example, a response that must never include `passwordHash`). A middle path is to assert that specific forbidden fields are absent rather than banning all extras.

**Pinning values that should vary.** `{"const": "2025-01-01T10:00:00Z"}` on a timestamp, or `enum` listing today's ten cities. Describe the *rule* (`format`, `pattern`, `type`), not today's data.

**Asserting on error message text.** `"is a required property"` changes between library versions. Assert on `error.validator` (such as `"required"`) or Pydantic's `type` code, or on paths.

**Trusting `format` blindly.** As shown in section 2.6, unchecked formats pass silently.

**Forgetting `required`.** A schema with only `properties` accepts `{}`. Always test your schema against an empty object and a clearly wrong one.

**Schemas that only test the happy path.** A schema that can never fail is useless. For each schema, keep a couple of known-bad samples and confirm they are rejected (see exercise 1).

**Duplicating rules.** If the schema says `status` is an enum, do not assert it again. Use the schema for shape, and assertions for business meaning ("total equals the sum of items").

**Brittle ordering.** If ordering is not guaranteed, check membership or sort first.

### Glossary

### Contract
The agreement between provider and consumer about endpoints, data shapes and errors.

### Contract test
A check that a request or response honours the contract's shape and rules.

### JSON Schema
A language-neutral vocabulary (written in JSON) for describing and validating JSON data.

### `required`
Lists the object keys that must be present; `properties` alone does not do this.

### `additionalProperties`
Controls whether keys not listed in `properties` are allowed.

### `$defs` / `$ref`
A place to define reusable sub-schemas, and the pointer that reuses one.

### `iter_errors` / `best_match`
`jsonschema` tools to list every violation, or to pick the single most useful one.

### Pydantic model
A Python class that validates and converts data from type hints; created with `model_validate`, exported with `model_dump`.

### Coercion
Automatic type conversion (`"5"` to `5`); helpful in apps, risky in contract tests.

### OpenAPI
The standard format for describing an API's paths, schemas and responses; rendered by Swagger UI.

### Negative validation
Deliberately sending invalid data to confirm the API rejects it (400/422) with a well-formed error.

### Contract drift
The real API changing while tests, docs or mocks stay the same.

---

## Practice Exercises

### Exercise 1: Prove your schema can fail

Write a schema for a `post` response (`userId`, `id`, `title`, `body`: all required; ids integers, `title` and `body` non-empty strings). Test it with one good sample and three bad ones (missing `title`, `id` as a string, empty `body`). Print all errors for each bad sample.

**Solution:**

```python
from jsonschema import Draft202012Validator

POST_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer"},
        "id":     {"type": "integer"},
        "title":  {"type": "string", "minLength": 1},
        "body":   {"type": "string", "minLength": 1},
    },
}

Draft202012Validator.check_schema(POST_SCHEMA)
validator = Draft202012Validator(POST_SCHEMA)

good = {"userId": 1, "id": 1, "title": "t", "body": "b"}
bad_samples = {
    "missing title": {"userId": 1, "id": 1, "body": "b"},
    "id as string":  {"userId": 1, "id": "1", "title": "t", "body": "b"},
    "empty body":    {"userId": 1, "id": 1, "title": "t", "body": ""},
}

assert list(validator.iter_errors(good)) == []
for label, sample in bad_samples.items():
    errors = list(validator.iter_errors(sample))
    assert errors, f"schema accepted a bad sample: {label}"
    print(label, "->", [e.message for e in errors])
```

The key habit: a schema that rejects nothing is worthless, so every schema gets at least one known-bad sample.

### Exercise 2: Request builders and a parametrized negative test

Write `new_post(**overrides)` that validates against a request schema (`title` and `body` required strings, `userId` integer, nothing else allowed), and `raw_post(**fields)` that does not. Show that `new_post(titel="x")` fails before any network call.

**Solution:**

```python
from jsonschema import Draft202012Validator

NEW_POST_SCHEMA = {
    "type": "object",
    "required": ["title", "body", "userId"],
    "properties": {
        "title":  {"type": "string", "minLength": 1},
        "body":   {"type": "string"},
        "userId": {"type": "integer"},
    },
    "additionalProperties": False,
}


def new_post(**overrides):
    payload = {"title": "Hello", "body": "World", "userId": 1}
    payload.update(overrides)
    errors = [e.message for e in Draft202012Validator(NEW_POST_SCHEMA).iter_errors(payload)]
    if errors:
        raise AssertionError(f"Invalid test payload: {errors}")
    return payload


def raw_post(**fields):
    return dict(fields)


try:
    new_post(titel="x")            # typo in the test
except AssertionError as err:
    print("caught test bug:", err)
```

`titel` is not in `properties` and `additionalProperties` is false, so the builder raises. Because the payload also keeps the valid `title`, the only complaint is the unexpected key.

### Exercise 3: A Pydantic model with a validator and strict mode

Model `Product` with `sku` (string, pattern `^[A-Z]{2}-\d{3}$`), `price` (number, greater than 0), `tags` (list of strings, default empty). Show that lax mode accepts `"price": "9.5"` but strict mode rejects it. Print `model_dump()`.

**Solution:**

```python
from typing import List
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class Product(BaseModel):
    sku: str = Field(pattern=r"^[A-Z]{2}-\d{3}$")
    price: float = Field(gt=0)
    tags: List[str] = Field(default_factory=list)


class StrictProduct(Product):
    model_config = ConfigDict(strict=True)


data = {"sku": "AB-123", "price": "9.5"}
print(Product.model_validate(data).model_dump())      # price coerced to 9.5

try:
    StrictProduct.model_validate(data)
except ValidationError as err:
    print(err.errors()[0]["type"])                    # float_type
```

`default_factory=list` gives each object its own fresh list.

### Exercise 4: Negative test with an error contract

For a `POST /users` endpoint, list five bad payloads, the expected status, and the checks you would run on the error response. Then implement `assert_error_response(response, field=None)` that checks the status is 400 or 422, the body matches `error.json`, and optionally that `field` appears in `details`.

**Solution:**

```python
def assert_error_response(response, field=None):
    assert response.status_code in (400, 422), response.text
    assert "application/json" in response.headers.get("Content-Type", "")
    body = response.json()
    assert_matches_schema(body, load_schema("error"), "error")
    if field is not None:
        fields = [d["field"] for d in body.get("details", [])]
        assert field in fields, f"expected an error for {field!r}, got {fields}"
    assert "Traceback" not in response.text
```

Five bad payloads: missing `name`, missing `email`, malformed `email`, negative `age`, `age` as a string. Expected status: 400 or 422 per the API docs. Checks: status is a client error and not 500, the error body matches the contract, the offending field is named, no stack trace leaks, and a follow-up list shows no new record.

---

## Quiz

**Q1.** A schema has `properties` for `id`, `name` and `email` but no `required` list, and no other rules. Which payload passes?
A) `{}`  B) `{"unknown": 1}` only if `additionalProperties` is false  C) Only `{"id": 1}`  D) None of them

**Q2.** How do you allow a field to be an integer or `null` in a 2020-12 schema?
A) `"nullable": true`  B) `"type": ["integer", "null"]`  C) `"optional": true`  D) `"type": "integer?"`

**Q3.** Why prefer `iter_errors` over `validate()` in tests?
A) It is faster  B) It reports every violation, not only the first  C) It checks formats automatically  D) It repairs the data

**Q4.** In a negative test, why do we use `raw_user()` instead of `new_user()`?
A) `new_user()` is slower  B) `new_user()` would validate and stop us sending the invalid data we intend to send  C) `raw_user()` sends valid data  D) There is no difference

**Q5.** Which is a backward-incompatible API change?
A) Adding an optional response field  B) Renaming a response field  C) Loosening a request `maxLength`  D) Adding a new documented endpoint

**Answers**

1. **A.** Without `required`, nothing is mandatory, so `{}` passes. `properties` does not mean required.
2. **B.** `nullable` is the older OpenAPI 3.0 spelling.
3. **B.** `iter_errors` yields all violations so one run shows the whole picture.
4. **B.** Negative tests must be able to send invalid data.
5. **B.** Removing or renaming a field breaks consumers that read it.

---

## Summary

- A **contract** defines what is correct; **contract tests** check requests and responses against it, catching drift early.
- JSON Schema gives you `type`, `required`, `properties`, `additionalProperties`, `enum`, `pattern`, `minimum`/`maximum`, `minLength`, `items`/`minItems`, nullable type arrays, `oneOf`/`anyOf`, `$defs`/`$ref` and `format` (which must be switched on).
- Use `Draft202012Validator` with `iter_errors` for complete reports and `best_match` for `oneOf`/`anyOf` clarity; call `check_schema` to catch broken schemas.
- Validate your **request** before sending in positive tests (`new_user`) and skip that on purpose in negative ones (`raw_user`); always validate the **response** and error bodies.
- Pydantic models give typed, attribute-style access with `Field` constraints, validators, `model_validate`, `ValidationError` and `model_dump`; use strict mode for contract checks.
- Choose JSON Schema for shareable, language-neutral contracts and Pydantic for convenient Python typing. Do not duplicate both without reason.
- OpenAPI describes `paths`, `components/schemas` and `responses`; tools like openapi-core and Schemathesis can validate or test against it.
- Keep schemas in `schemas/`, change them with the API, and respect backward-compatibility rules.
- Avoid over-strict schemas, pinned volatile values, assertions on message text, and schemas that never fail.

## Additional Resources

- JSON Schema, *Learn JSON Schema*: https://json-schema.org/learn/getting-started-step-by-step
- `jsonschema` (Python) documentation, *Validating with jsonschema and error handling*: https://python-jsonschema.readthedocs.io/en/stable/errors/
- Pydantic documentation, *Models*: https://docs.pydantic.dev/latest/concepts/models/
- Pydantic documentation, *Validators*: https://docs.pydantic.dev/latest/concepts/validators/
- OpenAPI Initiative, *OpenAPI Specification*: https://spec.openapis.org/oas/latest.html
- Schemathesis documentation: https://schemathesis.readthedocs.io/
