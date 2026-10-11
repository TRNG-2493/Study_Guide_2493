import pytest
import requests
import responses

from app.price_service import PriceService, PriceServiceError, PriceServiceTimeout, RateLimitError

pytestmark = pytest.mark.mock
BASE = "https://prices.example.test"


@pytest.fixture
def sleeps():
    return []


@pytest.fixture
def svc(sleeps):
    return PriceService(BASE, max_retries=2, sleep=sleeps.append)   # no real waiting


@responses.activate
def test_tax_rate_success(svc):
    responses.get(f"{BASE}/tax/DE", json={"country": "DE", "rate": 0.19})
    assert svc.get_tax_rate("de") == 0.19


@responses.activate
@pytest.mark.parametrize("net, rate, expected", [(100, 0.19, 119.0), (9.99, 0.2, 11.99), (0, 0.5, 0.0)],
                         ids=["round", "rounding", "zero"])
def test_price_with_tax(svc, net, rate, expected):
    responses.get(f"{BASE}/tax/FR", json={"rate": rate})
    assert svc.price_with_tax(net, "FR") == expected


def test_negative_price_rejected_without_http_call(svc):
    with responses.RequestsMock() as rsps:      # no registered URLs: any call would fail the test
        with pytest.raises(ValueError):
            svc.price_with_tax(-1, "DE")
        assert len(rsps.calls) == 0


@responses.activate
def test_convert_sends_query_and_rounds(svc):
    responses.get(f"{BASE}/rates", json={"base": "USD", "rates": {"EUR": 0.923}},
                  match=[responses.matchers.query_param_matcher({"base": "USD", "symbols": "EUR"})])
    assert svc.convert(10, "usd", "eur") == 9.23


@responses.activate
def test_convert_missing_rate(svc):
    responses.get(f"{BASE}/rates", json={"base": "USD", "rates": {}})
    with pytest.raises(PriceServiceError):
        svc.convert(10, "USD", "EUR")


@responses.activate
def test_server_error_is_not_retried(svc, sleeps):
    responses.get(f"{BASE}/tax/DE", status=500)
    with pytest.raises(PriceServiceError, match="500"):
        svc.get_tax_rate("DE")
    assert len(responses.calls) == 1 and sleeps == []


@responses.activate
def test_timeout_maps_to_domain_error(svc):
    responses.get(f"{BASE}/tax/DE", body=requests.exceptions.ReadTimeout())
    with pytest.raises(PriceServiceTimeout):
        svc.get_tax_rate("DE")


@responses.activate
def test_429_then_success_honours_retry_after(svc, sleeps):
    responses.get(f"{BASE}/tax/DE", status=429, headers={"Retry-After": "3"})
    responses.get(f"{BASE}/tax/DE", json={"rate": 0.19})
    assert svc.get_tax_rate("DE") == 0.19
    assert len(responses.calls) == 2 and sleeps == [3.0]


@responses.activate
def test_429_forever_raises_after_retries(svc, sleeps):
    responses.get(f"{BASE}/tax/DE", status=429)
    with pytest.raises(RateLimitError):
        svc.get_tax_rate("DE")
    assert len(responses.calls) == 3 and sleeps == [1.0, 1.0]     # 1 try + 2 retries


@responses.activate
def test_non_json_body_is_domain_error(svc):
    responses.get(f"{BASE}/tax/DE", body="<html>oops</html>")
    with pytest.raises(PriceServiceError):
        svc.get_tax_rate("DE")
