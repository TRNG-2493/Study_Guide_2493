"""Settings read from environment variables (provided; you may extend).

    SITE=local   (default) offline copy: site/practice_page.html  -> works with no network
    SITE=live              the real https://www.saucedemo.com
    HEADLESS=0             show the browser window (default 1 = no window)
    SLOW_MO=300            milliseconds pause between actions (handy when watching)

PowerShell:  $env:SITE="live"      bash:  SITE=live python -m pytest
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SITE = os.environ.get("SITE", "local").lower()
if SITE not in {"local", "live"}:
    raise ValueError(f"SITE must be 'local' or 'live', got {SITE!r}")

HEADLESS = os.environ.get("HEADLESS", "1") == "1"
SLOW_MO = int(os.environ.get("SLOW_MO", "0"))

USERNAME, PASSWORD = "standard_user", "secret_sauce"   # published on the practice site itself
BAD_PASSWORD = "definitely_wrong"

if SITE == "local":
    LOGIN_URL = (ROOT / "site" / "practice_page.html").as_uri()
    INVENTORY_URL = LOGIN_URL                # single page; localStorage decides what shows
else:
    LOGIN_URL = "https://www.saucedemo.com/"
    INVENTORY_URL = "https://www.saucedemo.com/inventory.html"
