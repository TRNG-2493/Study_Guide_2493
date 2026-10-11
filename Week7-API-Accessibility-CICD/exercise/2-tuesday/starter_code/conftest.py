"""Shared fixtures for the Project 2 API suite.  Complete every TODO.

Read configuration from environment variables (BASE_URL, API_USER, API_PASSWORD,
API_ADMIN_USER, API_ADMIN_PASSWORD) with defaults for the stand-in server.
"""
import os

import pytest
import requests  # noqa: F401  (you will need it)


@pytest.fixture(scope="session")
def base_url():
    # TODO: return os.getenv("BASE_URL", <default>) without a trailing slash
    raise NotImplementedError("TODO: base_url")


@pytest.fixture(scope="session")
def session():
    # TODO: create a requests.Session, yield it, close it afterwards
    raise NotImplementedError("TODO: session")


@pytest.fixture(scope="session")
def user_token(session, base_url):
    # TODO: POST /auth/login as the normal user (credentials from env vars), return the token
    raise NotImplementedError("TODO: user_token")


@pytest.fixture(scope="session")
def admin_token(session, base_url):
    # TODO: same for the admin user
    raise NotImplementedError("TODO: admin_token")


@pytest.fixture
def auth_headers(user_token):
    # TODO: {"Authorization": "Bearer <token>"}
    raise NotImplementedError("TODO: auth_headers")


@pytest.fixture
def admin_headers(admin_token):
    # TODO
    raise NotImplementedError("TODO: admin_headers")


@pytest.fixture
def item_payload():
    # TODO: a valid item body with a UNIQUE name each time (hint: uuid4) - duplicates give 409
    raise NotImplementedError("TODO: item_payload")


@pytest.fixture
def created_item(session, base_url, auth_headers, admin_headers, item_payload):
    # TODO: POST the item, assert 201, `yield` the created item (JSON),
    # then delete it as admin. Tolerate 404 (the test may have deleted it already).
    raise NotImplementedError("TODO: created_item")


@pytest.fixture
def make_item(session, base_url, auth_headers, admin_headers):
    # TODO (stage 8/9): factory fixture - yield a function that creates items,
    # remember their ids, and delete them all after the test.
    raise NotImplementedError("TODO: make_item")
