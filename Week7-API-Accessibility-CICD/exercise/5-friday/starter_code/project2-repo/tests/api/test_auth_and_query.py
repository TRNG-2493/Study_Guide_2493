import pytest

from conftest import unique_name

pytestmark = [pytest.mark.live, pytest.mark.regression]


@pytest.mark.parametrize("who, role", [("user", "user"), ("admin", "admin")])
def test_login_roles(settings, anon_client, who, role):
    from clients.api_client import ApiClient
    c = ApiClient(settings.base_url)
    creds = {"user": (settings.user, settings.password), "admin": (settings.admin_user, settings.admin_password)}[who]
    r = c.login(*creds)
    assert r.status_code == 200 and r.json()["role"] == role


@pytest.mark.parametrize("user, pw", [("tester", "nope"), ("nobody", "x"), ("", "")],
                         ids=["bad-password", "unknown-user", "empty"])
def test_login_bad_credentials(anon_client, user, pw):
    assert anon_client.post("/auth/login", json={"username": user, "password": pw}).status_code == 401


def test_write_without_token_is_401(anon_items):
    assert anon_items.create({"name": unique_name(), "price": 1, "category": "home"}).status_code == 401


def test_user_cannot_delete_is_403(items_api, make_item):
    assert items_api.delete(make_item().id).status_code == 403


def test_search_finds_only_my_item(items_api, make_item):
    item = make_item()
    body = items_api.list(q=item.name).json()
    assert [i["id"] for i in body["items"]] == [item.id]      # unique name => isolated from other tests


@pytest.mark.parametrize("params", [{"page": 0}, {"limit": 51}, {"limit": "abc"}],
                         ids=["page-0", "limit-51", "limit-text"])
def test_bad_paging_is_400(anon_items, params):
    assert anon_items.list(**params).status_code == 400
