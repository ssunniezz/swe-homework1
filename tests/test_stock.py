from flask.testing import FlaskClient

vending_info = {}
product_info = {}

add_stock_url = "/api/addStock"
edit_stock_url = "/api/editStock"
delete_stock_url = "/api/deleteStock"


def test_add_stock(client: FlaskClient):
    # add vending for testing
    data = {"name": "one", "location": "mahidol university"}

    r = client.post("/api/addVending", data=data).json

    global vending_info
    vending_info = r

    # ---------- #
    # adding stock
    data = {"vending_id": vending_info["id"], "name": "banana", "amount": "1"}

    r = client.post(add_stock_url, data=data).json

    global product_info
    product_info = r

    assert r["success"]


def test_stock_list(client: FlaskClient):
    guess_stocks = vending_info
    guess_stocks.pop("success")

    stock_info = {product_info["name"]: product_info["amount"]}
    guess_stocks["stock"] = stock_info

    stocks = client.get("/api/stocks").json

    assert stocks == [guess_stocks]


def test_add_stock_invalid(client: FlaskClient):
    global vending_info
    data = {"name": "banana", "amount": "1"}

    r = client.post(add_stock_url, data=data).json

    global product_info
    product_info = r

    assert not r["success"]


def test_add_stock_invalid_id(client: FlaskClient):
    global vending_info
    data = {"vending_id": "-1", "name": "oreo", "amount": "1"}

    r = client.post(add_stock_url, data=data).json

    global product_info
    product_info = r

    assert not r["success"]


def test_edit_stock(client: FlaskClient):
    global vending_info
    data = {"vending_id": vending_info["id"], "name": "banana", "amount": "1"}

    r = client.post(edit_stock_url, data=data).json

    global product_info
    product_info = r

    assert r["success"]


def test_edit_stock_invalid(client: FlaskClient):
    global vending_info
    invalid_data = {"vending_id": vending_info["id"], "amount": "1"}

    r = client.post(edit_stock_url, data=invalid_data).json

    global product_info
    product_info = r

    assert not r["success"]


def test_edit_stock_invalid_id(client: FlaskClient):
    global vending_info
    invalid_data = {"vending_id": "-1", "name": "banana", "amount": "2"}

    r = client.post(edit_stock_url, data=invalid_data).json

    global product_info
    product_info = r

    assert not r["success"]


def test_delete_stock(client: FlaskClient):
    global vending_info
    data = {
        "vending_id": vending_info["id"],
        "name": "banana",
    }

    r = client.post(delete_stock_url, data=data).json

    global product_info
    product_info = r

    assert r["success"]


def test_delete_stock_invalid(client: FlaskClient):
    global vending_info
    invalid_data = {
        "name": "banana",
    }

    r = client.post(delete_stock_url, data=invalid_data).json

    global product_info
    product_info = r

    assert not r["success"]


def test_delete_stock_invalid_id(client: FlaskClient):
    global vending_info
    invalid_data = {
        "vending_id": "-1",
        "name": "banana",
    }

    r = client.post(delete_stock_url, data=invalid_data).json

    global product_info
    product_info = r

    # delete vending after testing
    client.post("/api/deleteVending", data={"id": vending_info["id"]})

    assert not r["success"]
