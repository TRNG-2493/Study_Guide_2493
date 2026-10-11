# Starter structure

```
starter_code/
  project2_api_server.py   stand-in API (python project2_api_server.py [port])
  requirements.txt         requests, pytest, jsonschema
  pytest.ini               markers smoke / regression, --strict-markers
  conftest.py              fixtures with TODOs (base_url, session, tokens, created_item ...)
  schemas.py               JSON schemas (TODO)
  tests/api/               skeleton tests, each reports SKIPPED (TODO) until you implement it
```
Run: `BASE_URL=http://127.0.0.1:8000 pytest -m smoke` or just `pytest`.
Add more tests and parametrized cases as the brief asks; delete the skips as you go.
