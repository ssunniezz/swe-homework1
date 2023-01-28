from vending_machine.app import app
from vending_machine.service import add_vending, add_stock, delete_stock, edit_stock, delete_vending, stock_list

vending_info = {}
product_info = {}


def test_add_stock():
    # add vending for testing
    data = {
        "name": "one",
        "location": "mahidol university"
    }

    with app.app_context():
        r = add_vending(data)

    global vending_info
    vending_info = r

    # ---------- #
    # adding stock
    data = {
        "vending_id": vending_info['id'],
        "name": "banana",
        "amount": "1"
    }

    with app.app_context():
        r = add_stock(data)

    global product_info
    product_info = r

    assert r['success']


def test_stock_list():
    guess_stocks = vending_info
    guess_stocks.pop('success')

    stock_info = {product_info['name']: product_info['amount']}
    guess_stocks['stock'] = stock_info

    with app.app_context():
        stocks = stock_list()

    assert stocks.json == [guess_stocks]


def test_add_stock_invalid():
    global vending_info
    data = {
        "name": "banana",
        "amount": "1"
    }

    with app.app_context():
        r = add_stock(data)

    global product_info
    product_info = r

    assert not r['success']


def test_add_stock_invalid_id():
    global vending_info
    data = {
        "vending_id": "-1",
        "name": "oreo",
        "amount": "1"
    }

    with app.app_context():
        r = add_stock(data)

    global product_info
    product_info = r

    assert not r['success']


def test_edit_stock():
    global vending_info
    data = {
        "vending_id": vending_info['id'],
        "name": "banana",
        "amount": "1"
    }

    with app.app_context():
        r = edit_stock(data)

    global product_info
    product_info = r

    assert r['success']


def test_edit_stock_invalid():
    global vending_info
    data = {
        "vending_id": vending_info['id'],
        "amount": "1"
    }

    with app.app_context():
        r = edit_stock(data)

    global product_info
    product_info = r

    assert not r['success']


def test_edit_stock_invalid_id():
    global vending_info
    data = {
        "vending_id": "-1",
        "name": "banana",
        "amount": "2"
    }

    with app.app_context():
        r = edit_stock(data)

    global product_info
    product_info = r

    assert not r['success']


def test_delete_stock():
    global vending_info
    data = {
        "vending_id": vending_info['id'],
        "name": "banana",
    }

    with app.app_context():
        r = delete_stock(data)

    global product_info
    product_info = r

    assert r['success']


def test_delete_stock_invalid():
    global vending_info
    data = {
        "name": "banana",
    }

    with app.app_context():
        r = delete_stock(data)

    global product_info
    product_info = r

    assert not r['success']


def test_delete_stock_invalid_id():
    global vending_info
    data = {
        "vending_id": "-1",
        "name": "banana",
    }

    with app.app_context():
        r = delete_stock(data)

    global product_info
    product_info = r

    # delete vending after testing
    with app.app_context():
        delete_vending({'id': vending_info['id']})

    assert not r['success']
