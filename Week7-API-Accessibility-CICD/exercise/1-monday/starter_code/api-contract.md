# Project 2 API contract (stand-in server, http://127.0.0.1:8000)

All bodies are JSON. Every response carries an `X-Request-Id` header. Errors look like `{"error": "<message>"}`; 422 adds `"details": {field: reason}`.
Auth: `Authorization: Bearer <token>` (token from `/auth/login`). Users: `tester/tester123` (role user), `admin/admin123` (role admin).

| Method | Path | Auth | Success | Error codes |
|---|---|---|---|---|
| GET | /health | none | 200 `{"status":"ok"}` | - |
| POST | /auth/login | none | 200 `{"token","token_type":"Bearer","role"}` | 401 bad credentials, 400 invalid JSON |
| GET | /items | none | 200 `{"total","page","limit","items":[...]}` | 400 bad paging |
| POST | /items | any user | 201 item + `Location: /items/{id}` | 401, 409 duplicate name, 422 validation, 400 invalid JSON |
| GET | /items/{id} | none | 200 item | 404 |
| PUT | /items/{id} | any user | 200 item | 401, 404, 422, 400 |
| PATCH | /items/{id} | any user | 200 item | 401, 404, 422, 400 |
| DELETE | /items/{id} | admin | 204 (no body) | 401, 403, 404 |
| POST | /admin/reset | admin | 200 `{"status":"reset"}` (restores seed data) | 401, 403 |

Unsupported method on a known path returns 405; unknown path returns 404.

## Query parameters for GET /items
`category` (office, home, electronics), `q` (name substring, case-insensitive), `page` (>=1, default 1), `limit` (1-50, default 10).

## Item shape
```json
{"id": 1, "name": "Notebook", "price": 4.5, "category": "office", "stock": 100}
```
Create/PUT rules: `name` non-empty string (unique, case-insensitive), `price` number >= 0, `category` one of office/home/electronics, `stock` optional integer >= 0 (default 0). PATCH accepts any subset.
Seed data: 5 items (ids 1-5); the next created id is 6.
