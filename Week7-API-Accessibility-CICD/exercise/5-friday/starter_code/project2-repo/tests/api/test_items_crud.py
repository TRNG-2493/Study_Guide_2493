import pytest

from conftest import unique_name
from models.item import ItemOut

pytestmark = [pytest.mark.live, pytest.mark.regression]


@pytest.mark.smoke
def test_health(anon_client):
    r = anon_client.get("/health")
    assert r.status_code == 200 and r.json() == {"status": "ok"}


def test_create_then_read_back(items_api, make_item):
    item = make_item(name=unique_name(), price=12.5, category="office", stock=3)
    r = items_api.get(item.id)
    assert r.status_code == 200
    assert ItemOut.model_validate(r.json()) == item


def test_put_replaces_item(items_api, make_item):
    item = make_item()
    new = {"name": item.name + "-v2", "price": 99.0, "category": "home", "stock": 7}
    r = items_api.replace(item.id, new)
    assert r.status_code == 200
    assert r.json() == {"id": item.id, **new}


def test_patch_changes_only_sent_fields(items_api, make_item):
    item = make_item()
    r = items_api.patch(item.id, {"price": 1.25})
    assert r.status_code == 200
    assert r.json()["price"] == 1.25 and r.json()["name"] == item.name


def test_delete_then_get_is_404(items_api, admin_items, make_item):
    item = make_item()
    d = admin_items.delete(item.id)
    assert d.status_code == 204 and d.content == b""
    assert items_api.get(item.id).status_code == 404


def test_duplicate_name_is_409(items_api, make_item):
    item = make_item()
    assert items_api.create({"name": item.name.upper(), "price": 1, "category": "home"}).status_code == 409
