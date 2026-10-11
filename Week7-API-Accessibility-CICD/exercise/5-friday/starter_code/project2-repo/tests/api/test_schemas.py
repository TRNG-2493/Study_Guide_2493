import pytest
from jsonschema import ValidationError, validate
from pydantic import ValidationError as PydanticError

from models.item import ItemList, ItemOut
from schemas import ITEM_LIST_SCHEMA, ITEM_SCHEMA

pytestmark = pytest.mark.regression


@pytest.mark.live
def test_list_matches_jsonschema_and_model(anon_items):
    body = anon_items.list().json()
    validate(body, ITEM_LIST_SCHEMA)
    assert ItemList.model_validate(body).total == body["total"]


@pytest.mark.live
def test_created_item_matches_both(make_item, items_api):
    item = make_item()
    validate(items_api.get(item.id).json(), ITEM_SCHEMA)


@pytest.mark.parametrize("bad", [
    {"id": 1, "name": "x", "price": -1, "category": "home", "stock": 0},
    {"id": 1, "name": "x", "price": 1, "category": "toys", "stock": 0},
    {"id": 1, "name": "x", "price": 1, "category": "home", "stock": 0, "extra": 1},
], ids=["negative-price", "bad-category", "extra-field"])
def test_both_validators_reject_bad_items(bad):
    with pytest.raises(ValidationError):
        validate(bad, ITEM_SCHEMA)
    with pytest.raises(PydanticError):
        ItemOut.model_validate(bad)
