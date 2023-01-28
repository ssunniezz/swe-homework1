from vending_machine.app import app
from vending_machine.service import add_vending, edit_vending, delete_vending

vending_info = {}


def test_add_vending():
    data = {
        "name": "one",
        "location": "mahidol university"
    }

    with app.app_context():
        r = add_vending(data)

    global vending_info
    vending_info = r

    assert r['success']


def test_add_vending_invalid():
    data = {
        "location": "mahidol university"
    }

    with app.app_context():
        r = add_vending(data)
    assert not r['success']


def test_edit_vending():
    global vending_info
    data = {
        "id": vending_info['id'],
        "name": "two",
        "location": "thammasat university"
    }

    with app.app_context():
        r = edit_vending(data)
    assert r['success']


def test_edit_vending_invalid():
    global vending_info
    data = {
        "id": -1,
        "name": "two",
        "location": "thammasat university"
    }
    with app.app_context():
        r = edit_vending(data)

    assert not r['success']


def test_delete_vending():
    global vending_info
    data = {
        "id": vending_info['id'],
    }

    with app.app_context():
        r = delete_vending(data)

    assert r['success']


def test_delete_vending_invalid():
    global vending_info
    data = {
        "id": '-1',
    }

    with app.app_context():
        r = delete_vending(data)

    assert not r['success']
