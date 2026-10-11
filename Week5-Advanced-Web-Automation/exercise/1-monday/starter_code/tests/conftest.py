"""PROVIDED INFRASTRUCTURE - you do not need to edit this file.

It starts the local exercise web app on a free port for the whole test run and tells
pytest-playwright to use it as `base_url`, so in your tests `page.goto("/")` opens the form.
(Fixtures are Wednesday's topic. For today just treat this as "the app is already running".)
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from serve import start_in_thread  # noqa: E402


@pytest.fixture(scope="session")
def base_url():
    server, url = start_in_thread()
    yield url
    server.shutdown()
