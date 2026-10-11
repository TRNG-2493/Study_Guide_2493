import pytest

from conftest import unique_name
from utils.data_loader import json_params, read_csv

pytestmark = [pytest.mark.live, pytest.mark.regression]

SEED_ROWS = read_csv("items.csv")


@pytest.mark.parametrize("row", SEED_ROWS, ids=[r["name"] for r in SEED_ROWS])
def test_seed_items_by_id(anon_items, row):
    body = anon_items.get(row["item_id"]).json()
    assert body["name"] == row["name"]
    assert body["price"] == float(row["price"])
    assert body["category"] == row["category"]
    assert body["stock"] == int(row["stock"])


FILTERS = read_csv("filters.csv")


@pytest.mark.parametrize("row", FILTERS, ids=[r["case_id"] for r in FILTERS])
def test_category_filter(anon_items, row):
    body = anon_items.list(category=row["category"], limit=50).json()
    assert body["total"] >= int(row["min_expected_seed_count"])   # others may add items: never ==
    assert all(i["category"] == row["category"] for i in body["items"])


@pytest.mark.parametrize("case", json_params("payloads.json", "valid"))
def test_valid_payloads_create(items_api, admin_items, case):
    body = {**case["body"], "name": unique_name()}
    r = items_api.create(body)
    try:
        assert r.status_code == 201
        assert all(r.json()[k] == v for k, v in body.items())
    finally:
        if r.status_code == 201:
            admin_items.delete(r.json()["id"])


@pytest.mark.parametrize("case", json_params("payloads.json", "invalid"))
def test_invalid_payloads_are_422(items_api, case):
    body = dict(case["body"])
    r = items_api.create(body)
    assert r.status_code == 422
    assert case["bad_field"] in r.json()["details"]


def test_invalid_json_is_400(items_api):
    r = items_api.create_raw("{oops", headers={"Content-Type": "application/json"})
    assert r.status_code == 400
