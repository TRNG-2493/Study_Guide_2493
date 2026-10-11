import pytest
import requests
import responses

from clients.api_client import ApiClient
from services.items_api import ItemsApi

pytestmark = pytest.mark.mock
BASE = "http://api.test"


@responses.activate
def test_login_stores_token_and_sends_bearer():
    responses.post(f"{BASE}/auth/login", json={"token": "t0k", "token_type": "Bearer", "role": "user"})
    responses.get(f"{BASE}/items/1", json={"id": 1})
    c = ApiClient(BASE)
    c.login("u", "p")
    ItemsApi(c).get(1)
    assert responses.calls[1].request.headers["Authorization"] == "Bearer t0k"


@responses.activate
def test_default_timeout_is_applied():
    responses.get(f"{BASE}/health", json={"status": "ok"})
    ApiClient(BASE, timeout=3).get("/health")
    assert responses.calls[0].request.req_kwargs["timeout"] == 3


@responses.activate
def test_timeout_propagates():
    responses.get(f"{BASE}/health", body=requests.exceptions.ConnectTimeout())
    with pytest.raises(requests.exceptions.Timeout):
        ApiClient(BASE).get("/health")
