# Starter code - QE Summit registration form

Everything runs offline; no internet needed after `pip install` and `playwright install chromium`.

```
starter_code/
  app/index.html        the web app under test (single static page) - read it, do not edit it
  serve.py              tiny http.server helper for exploring the app by hand
  tests/conftest.py     PROVIDED: starts the app for pytest and sets base_url - do not edit
  tests/test_form_flow.py   18 core TODO tests (stages 1-6)  <- your main work
  tests/test_stretch.py     6 optional stretch tests (skipped until you remove the skip line)
  project1_milestone/   app-neutral template for your Project 1 repo (see main README)
  requirements.txt, pytest.ini
```

## Run it
```bash
python -m venv .venv && . .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                                   # whole suite, headless (expect TODO failures at the start)
pytest -k test_01 --headed --slowmo 400  # one test, watch it
python serve.py                          # explore the app: http://127.0.0.1:8765/
```

Expected at the start: `1 passed, 18 failed, 6 skipped` (every failure says `TODO: implement ...`).
