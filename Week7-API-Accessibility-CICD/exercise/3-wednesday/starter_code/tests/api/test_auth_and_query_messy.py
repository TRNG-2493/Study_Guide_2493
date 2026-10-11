import requests


def test_login_tester():
    r = requests.post("http://127.0.0.1:8000/auth/login", json={"username": "tester", "password": "tester123"})
    assert r.status_code == 200 and r.json()["role"] == "user"


def test_login_admin():
    r = requests.post("http://127.0.0.1:8000/auth/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 200 and r.json()["role"] == "admin"


def test_login_bad_password():
    r = requests.post("http://127.0.0.1:8000/auth/login", json={"username": "tester", "password": "nope"})
    assert r.status_code == 401


def test_user_cannot_delete():
    token = requests.post("http://127.0.0.1:8000/auth/login",
                          json={"username": "tester", "password": "tester123"}).json()["token"]
    r = requests.delete("http://127.0.0.1:8000/items/1", headers={"Authorization": "Bearer " + token})
    assert r.status_code == 403


def test_filter_office():
    r = requests.get("http://127.0.0.1:8000/items?category=office")
    assert r.json()["total"] == 2           # hard-coded, shared-state sensitive


def test_filter_home():
    r = requests.get("http://127.0.0.1:8000/items?category=home")
    assert r.json()["total"] == 1


def test_filter_electronics():
    r = requests.get("http://127.0.0.1:8000/items?category=electronics")
    assert r.json()["total"] == 2


def test_search_lamp():
    r = requests.get("http://127.0.0.1:8000/items?q=lamp")
    assert [i["name"] for i in r.json()["items"]] == ["Desk Lamp"]


def test_page_size_two():
    r = requests.get("http://127.0.0.1:8000/items?page=1&limit=2")
    assert len(r.json()["items"]) == 2


def test_bad_page_is_400():
    r = requests.get("http://127.0.0.1:8000/items?page=0")
    assert r.status_code == 400
