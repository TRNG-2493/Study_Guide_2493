"""Fixtures: configuration -> clients -> services -> data factories (all cleaned up)."""
import uuid

import pytest
import requests

from clients.api_client import ApiClient
from config import load_settings
from services.items_api import ItemsApi


@pytest.fixture(scope="session")
def settings():
    return load_settings()


@pytest.fixture(scope="session")
def api_available(settings):
    try:
        ok = requests.get(f"{settings.base_url}/health", timeout=2).status_code == 200
    except requests.RequestException:
        ok = False
    if not ok and settings.api_mode == "live" and settings.require_api:
        pytest.fail(f"API at {settings.base_url} is not reachable (REQUIRE_API=1)", pytrace=False)
    return ok


def pytest_collection_modifyitems(config, items):
    s = load_settings()
    skip_mode = pytest.mark.skip(reason="API_MODE=mock: live tests skipped")
    for item in items:
        if "live" in item.keywords and s.api_mode == "mock":
            item.add_marker(skip_mode)


@pytest.fixture(autouse=True)
def _live_guard(request):
    """Live tests are skipped with a clear reason (not 23 ugly errors) when the API is down."""
    if "live" in request.keywords:
        if not request.getfixturevalue("api_available"):
            pytest.skip("API unreachable (set REQUIRE_API=1 to make this a failure)")


def _logged_in_client(settings, user, password, api_available):
    if not api_available:
        pytest.skip("API unreachable (set REQUIRE_API=1 to make this a failure)")
    c = ApiClient(settings.base_url, timeout=settings.timeout)
    r = c.login(user, password)
    assert r.status_code == 200, f"login failed for {user}: {r.status_code}"
    return c


@pytest.fixture(scope="session")
def anon_client(settings):
    c = ApiClient(settings.base_url, timeout=settings.timeout)
    yield c
    c.close()


@pytest.fixture(scope="session")
def user_client(settings, api_available):
    c = _logged_in_client(settings, settings.user, settings.password, api_available)
    yield c
    c.close()


@pytest.fixture(scope="session")
def admin_client(settings, api_available):
    c = _logged_in_client(settings, settings.admin_user, settings.admin_password, api_available)
    yield c
    c.close()


@pytest.fixture
def anon_items(anon_client):
    return ItemsApi(anon_client)


@pytest.fixture
def items_api(user_client):
    return ItemsApi(user_client)


@pytest.fixture
def admin_items(admin_client):
    return ItemsApi(admin_client)


def unique_name(prefix="qa"):
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


@pytest.fixture
def make_item(items_api, admin_items):
    """Factory: creates items with unique names; deletes every one of them afterwards."""
    created = []

    def _make(**overrides):
        body = {"name": unique_name(), "price": 1.0, "category": "home", "stock": 1}
        body.update(overrides)
        item = items_api.create_ok(body)
        created.append(item.id)
        return item

    yield _make
    for item_id in created:
        admin_items.delete(item_id)   # 204 or 404 are both fine
