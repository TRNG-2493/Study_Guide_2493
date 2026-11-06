# Lecture 9: Homework

**Time:** 30–45 minutes
**Goal:** practise data-driven tests, `pytest.ini`, HTML reports and retries, all of which you'll reuse in the final project.

> This is a short warm-up. Do it **before** starting the final project: the JSON loader, `pytest.ini` and reporting hook carry straight over.

## Setup

1. Create a folder `homework_09/`.
2. Copy into it from `lecture_09/`:
   - `site/`, `pages/`, `utils/` and `conftest.py`
   - `tests/test_03_retries.py` (for Part 4)
3. Create the empty folders `test_data/` and the file `tests/test_lecture09_homework.py`.

```
homework_09/
├── conftest.py
├── pytest.ini                       ← you'll create this in Part 3
├── site/
├── pages/
├── utils/
├── test_data/
│   └── checkout_errors.json         ← you'll create this in Part 1
└── tests/
    ├── test_03_retries.py
    └── test_lecture09_homework.py
```

Run your homework on its own: `pytest homework_09`

## Starter code

`tests/test_lecture09_homework.py`:

```python
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.products_page import ProductsPage
from utils.data_loader import load_json


@pytest.fixture
def checkout_with_onesie(products_page: ProductsPage, cart_page: CartPage,
                         checkout_page: CheckoutPage) -> CheckoutPage:
    """Onesie in the cart, and the checkout form open."""
    products_page.add_to_cart("Onesie")
    products_page.go_to_cart()
    cart_page.checkout()
    return checkout_page


# ================= PART 1: Data-driven from JSON =================

# TODO: load checkout_errors.json into ERROR_CASES


# TODO: test_checkout_errors
#   - parametrized with ERROR_CASES, using each case's "id" as the test name
#   - enters the case's first name, last name and postcode
#   - checks the error message matches the case's "error"
#   - checks the "Place order" button is NOT shown (we didn't get past step 1)


# ================= PART 2: parametrize without a file =================

# TODO: test_price_sorting
#   - parametrized with 2 cases: ("Price (low to high)", False) and ("Price (high to low)", True)
#   - ids: "cheapest first" and "most expensive first"
#   - sorts, waits for the order to change, then checks get_prices() is sorted
#     (use sorted(prices, reverse=...))


# TODO: test_name_sorting
#   - same idea for "Name (A to Z)" and "Name (Z to A)", checking get_product_names()
#   - hint: the page starts sorted A to Z, so sort by price first,
#     or "A to Z" won't change anything and you can't tell it worked
```

---

## Part 1: Data-driven from JSON (required)

Create `test_data/checkout_errors.json` with **at least 5 cases**. Each case has: `id`, `first_name`, `last_name`, `postcode`, `error`.

Include:

| Case | Expected error |
|---|---|
| Missing first name | "First name is required" |
| Missing last name | "Last name is required" |
| Missing postcode | "Postcode is required" |
| Everything missing | *Try it on the site; which error appears first?* |
| First name is only spaces `"   "` | *Try it on the site* |

Then write `test_checkout_errors` in the starter file.

```bash
pytest homework_09 -v -k checkout_errors
```

You should see 5 tests with readable names, like `test_checkout_errors[chromium-missing postcode]`.

---

## Part 2: `parametrize` without a file (required)

Write `test_price_sorting` and `test_name_sorting` as described in the starter file.

```bash
pytest homework_09 -v -k sorting
```

4 tests should pass.

---

## Part 3: `pytest.ini` and the HTML report (required)

**1.** Create `homework_09/pytest.ini`:

```ini
[pytest]
testpaths = tests
addopts =
    --browser chromium
    --reruns 1
    --screenshot only-on-failure
    --tracing retain-on-failure
    --html=reports/report.html
    --self-contained-html
```

> No `base_url` is needed: `conftest.py` points tests at the local server.

**2.** Make **one** test fail on purpose. In `checkout_errors.json`, change the "missing postcode" case's error to `"Postal code is required"`.

**3.** Run just `pytest homework_09` (no other options). Then open `reports/report.html` (it's created in the folder you ran pytest from).

**4.** Answer as comments at the bottom of your test file:

1. Which test failed, and what did the report say the **actual** text was?
2. What does the screenshot in the report show?
3. The test failed twice before being reported. Why? (Look in `pytest.ini`.)
4. Where was the **trace** for the failing test saved? Open it with `playwright show-trace`. What's the last action before the failure?

**5.** Put the JSON back to `"Postcode is required"` and run again. Everything should pass.

---

## Part 4: Retries (required)

**1.** Run the flaky banner test **5 times without retries**. Note how many passed and failed.

```bash
pytest homework_09/tests/test_03_retries.py -k deal_banner_flaky --reruns 0 -v
```

> `--reruns 0` on the command line overrides `--reruns 1` in `pytest.ini`.

**2.** Run it **5 times with 2 retries**, and look for `RERUN` in the output:

```bash
pytest homework_09/tests/test_03_retries.py -k deal_banner_flaky --reruns 2 -v
```

**3.** Answer as comments:

5. How many of your 5 runs failed **without** retries? How many failed **with** them?
6. `test_deal_banner_fixed` uses `timeout=10_000` instead of retries. Give **two** reasons why that's a better fix.

---

## Submission checklist

- [ ] `test_data/checkout_errors.json` with at least 5 cases
- [ ] `test_lecture09_homework.py`: 9 passing tests (5 + 4)
- [ ] `pytest.ini`
- [ ] 6 answers as comments
