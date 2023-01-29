from flask.testing import FlaskClient

vending_info = {}


def test_add_vending(client: FlaskClient):
    data = {"name": "one", "location": "mahidol university"}

    r = client.post("/api/addVending", data=data).json

    global vending_info
    vending_info = r

    assert r["success"]


def test_add_vending_invalid(client: FlaskClient):
    data = {"location": "mahidol university"}

    r = client.post("/api/addVending", data=data).json

    assert not r["success"]


def test_edit_vending(client: FlaskClient):
    global vending_info
    data = {"id": vending_info["id"], "name": "two", "location": "thammasat university"}

    r = client.post("/api/editVending", data=data).json

    assert r["success"]


def test_edit_vending_invalid(client: FlaskClient):
    global vending_info
    data = {"id": -1, "name": "two", "location": "thammasat university"}

    r = client.post("/api/editVending", data=data).json

    assert not r["success"]


def test_delete_vending(client: FlaskClient):
    global vending_info
    data = {
        "id": vending_info["id"],
    }

    r = client.post("/api/deleteVending", data=data).json

    assert r["success"]


def test_delete_vending_invalid(client: FlaskClient):
    global vending_info
    data = {
        "id": "-1",
    }

    r = client.post("/api/deleteVending", data=data).json

    assert not r["success"]
