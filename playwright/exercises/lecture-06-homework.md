# Lecture 6: Homework

**Time:** 60 minutes
**Goal:** practise dialogs, frames, Shadow DOM, navigation, new tabs and pop-ups, and file upload and download.

## Setup

1. Copy all three practice pages from the Lecture 6 demo into your `homework/` folder:
   - `events_practice.html`
   - `frame_profile.html`
   - `help.html`
2. Create `homework/test_lecture06_homework.py` with the starter code below.
3. Open `events_practice.html` in your browser and try each section by hand first.

**Rules:** no `sleep`; create upload files with `tmp_path` (no hard-coded paths like `C:\Users\...`).

## Starter code

```python
import csv
import re
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Dialog, Page, expect

PRACTICE_PAGE = Path(__file__).parent / "events_practice.html"


@pytest.fixture
def store(page: Page) -> Page:
    page.goto(PRACTICE_PAGE.as_uri())
    return page


# ================= PART 1: Dialogs =================

def test_01_alert_message(store: Page):
    # TODO: click "Show alert" and accept the alert
    # TODO: the alert's message was "Your order has been placed!"
    # TODO: #dialog-result says "Alert closed"
    pass


def test_02_accept_confirm(store: Page):
    # TODO: click "Delete account" and accept
    # TODO: the dialog's type was "confirm"
    # TODO: #dialog-result says "Account deleted"
    pass


def test_03_prompt_with_text(store: Page):
    # TODO: click "Enter coupon" and enter "FREESHIP"
    # TODO: #dialog-result says "Coupon applied: FREESHIP"
    pass


def test_04_cancel_prompt(store: Page):
    # TODO: click "Enter coupon" and press Cancel
    # TODO: #dialog-result says ... (try it in the browser to find out)
    pass


# ================= PART 2: Frames and Shadow DOM =================

def test_05_profile_frame(store: Page):
    # TODO: inside the Profile form frame, enter "Ben Carter" and click Save
    # TODO: the frame shows "Saved: Ben Carter"
    pass


def test_06_nested_newsletter_frame(store: Page):
    # TODO: subscribe "ben@example.com" in the Newsletter frame
    # TODO: it shows "Subscribed: ben@example.com"
    pass


def test_07_shadow_dom_follow(store: Page):
    # TODO: the user card (#open-card) shows the name "Asha Patel"
    # TODO: click Follow; the status says "Following"
    pass


# ================= PART 3: Navigation, tabs and pop-ups =================

def test_08_navigate_and_go_back(store: Page):
    # TODO: click "Help page"; the title is "Help Centre"
    # TODO: click "Back to the store"; the title is "Practice Store - Events"
    # TODO: use the browser's back button; the title is "Help Centre" again
    pass


def test_09_new_tab_then_close(store: Page, context: BrowserContext):
    # TODO: click "Open help in a new tab"
    # TODO: the NEW tab's main heading is "Help Centre"
    # TODO: close the new tab; only 1 page is left in the context
    pass


def test_10_chat_popup(store: Page):
    # TODO: click "Open chat window"
    # TODO: the pop-up's URL contains "from=chat" and its title is "Help Centre"
    pass


def test_11_delayed_redirect(store: Page):
    # TODO: click "Go to help in 1 second"
    # TODO: wait for the URL to contain "from=redirect"
    # TODO: the title is "Help Centre"
    pass


# ================= PART 4: Upload and download =================

def test_12_upload_resume(store: Page, tmp_path: Path):
    # TODO: create a file "cv.pdf" of exactly 1024 bytes in tmp_path
    # TODO: upload it as the Resume
    # TODO: #resume-result says "Uploaded: cv.pdf (1024 bytes)"
    pass


def test_13_upload_photos_from_memory(store: Page):
    # TODO: upload TWO photos created in memory: "cat.png" and "dog.png"
    #       (no files on disk!)
    # TODO: #photos-result says "2 photos: cat.png, dog.png"
    pass


def test_14_avatar_file_chooser(store: Page, tmp_path: Path):
    # TODO: create "profile.jpg" in tmp_path
    # TODO: click "Choose avatar" and choose the file
    # TODO: #avatar-result says "Avatar: profile.jpg"
    pass


def test_15_download_and_read_csv(store: Page, tmp_path: Path):
    # TODO: click "Export orders as CSV" and save the download in tmp_path
    # TODO: read it with the csv module
    # TODO: the customers are ["Asha", "Ben"]
    # TODO: the totals add up to 27.5
    pass
```

---

## Parts 1–4 (required)

Complete all 15 tests, then run:

```bash
pytest homework -v
```

All 15 should pass.

**Hints:**

- Test 01: you need to save the message somewhere, so use a function with a list, not just a `lambda`.
- Test 07: the card's name and status are inside Shadow DOM. Which kinds of locator can see inside?
- Test 09: which fixture gives you the browser context?
- Test 12: `b"x" * 1024` is 1024 bytes.
- Test 13: `set_input_files` accepts a list of `{"name": ..., "mimeType": ..., "buffer": ...}` dictionaries.

---

## Part 5: Bonus (optional) — a live website

Create `homework/test_lecture06_bonus.py` for **https://the-internet.herokuapp.com**:

| Page | Task |
|---|---|
| `/javascript_alerts` | Click **Click for JS Prompt**, enter "hello"; `#result` says "You entered: hello" |
| `/nested_frames` | The middle frame (inside the top frame) says "MIDDLE". *Hint:* these use `<frame>` with `name` attributes |
| `/windows` | Click **Click Here**; the new window's heading is "New Window" |
| `/upload` | Upload a file and submit; the page says "File Uploaded!" and shows the file name |

---

## Submission checklist

- [ ] `test_lecture06_homework.py`: 15 passing tests
- [ ] Every dialog handler is registered before the click
- [ ] Upload files created with `tmp_path` or in memory
- [ ] (Optional) Part 5 bonus tests
