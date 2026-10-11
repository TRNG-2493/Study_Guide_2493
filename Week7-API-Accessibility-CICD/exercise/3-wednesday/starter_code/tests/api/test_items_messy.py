import requests

# NOTE: this file "works" when run top to bottom against a freshly started server.
# It is deliberately messy. Do not fix it in place; refactor it (see the brief).

STATE = {}


def test_01_create_item():
    login = requests.post("http://127.0.0.1:8000/auth/login", json={"username": "tester", "password": "tester123"})
    token = login.json()["token"]
    r = requests.post("http://127.0.0.1:8000/items",
                      json={"name": "Order Widget", "price": 12.5, "category": "office", "stock": 3},
                      headers={"Authorization": "Bearer " + token})
    assert r.status_code == 201
    STATE["id"] = r.json()["id"]          # planted: later tests depend on this
    STATE["token"] = token


def test_02_get_created_item():
    r = requests.get("http://127.0.0.1:8000/items/" + str(STATE["id"]))
    assert r.status_code == 200
    assert r.json()["name"] == "Order Widget"


def test_03_update_created_item():
    r = requests.put("http://127.0.0.1:8000/items/" + str(STATE["id"]),
                     json={"name": "Order Widget", "price": 20.0, "category": "office", "stock": 3},
                     headers={"Authorization": "Bearer " + STATE["token"]})
    assert r.status_code == 200
    assert r.json()["price"] == 20.0


def test_04_delete_created_item():
    login = requests.post("http://127.0.0.1:8000/auth/login", json={"username": "admin", "password": "admin123"})
    r = requests.delete("http://127.0.0.1:8000/items/" + str(STATE["id"]),
                        headers={"Authorization": "Bearer " + login.json()["token"]})
    assert r.status_code == 204


def test_05_deleted_item_is_gone():
    r = requests.get("http://127.0.0.1:8000/items/" + str(STATE["id"]))
    assert r.status_code == 404


def test_list_has_five_items():
    r = requests.get("http://127.0.0.1:8000/items")
    assert r.json()["total"] == 5          # planted: breaks while test_01..04 are "in flight"


def test_get_item_1():
    r = requests.get("http://127.0.0.1:8000/items/1")
    assert r.json()["name"] == "Notebook"
    assert r.json()["price"] == 4.5


def test_get_item_2():
    r = requests.get("http://127.0.0.1:8000/items/2")
    assert r.json()["name"] == "Desk Lamp"
    assert r.json()["price"] == 24.99


def test_get_item_3():
    r = requests.get("http://127.0.0.1:8000/items/3")
    assert r.json()["name"] == "USB Cable"
    assert r.json()["price"] == 7.0


def test_create_duplicate_notebook_is_409():
    login = requests.post("http://127.0.0.1:8000/auth/login", json={"username": "tester", "password": "tester123"})
    r = requests.post("http://127.0.0.1:8000/items", json={"name": "Notebook", "price": 1, "category": "office"},
                      headers={"Authorization": "Bearer " + login.json()["token"]})
    assert r.status_code == 409


def test_create_negative_price_is_422():
    login = requests.post("http://127.0.0.1:8000/auth/login", json={"username": "tester", "password": "tester123"})
    r = requests.post("http://127.0.0.1:8000/items", json={"name": "Bad1", "price": -1, "category": "office"},
                      headers={"Authorization": "Bearer " + login.json()["token"]})
    assert r.status_code == 422


def test_create_bad_category_is_422():
    login = requests.post("http://127.0.0.1:8000/auth/login", json={"username": "tester", "password": "tester123"})
    r = requests.post("http://127.0.0.1:8000/items", json={"name": "Bad2", "price": 1, "category": "toys"},
                      headers={"Authorization": "Bearer " + login.json()["token"]})
    assert r.status_code == 422


def test_create_missing_name_is_422():
    login = requests.post("http://127.0.0.1:8000/auth/login", json={"username": "tester", "password": "tester123"})
    r = requests.post("http://127.0.0.1:8000/items", json={"price": 1, "category": "office"},
                      headers={"Authorization": "Bearer " + login.json()["token"]})
    assert r.status_code == 422
