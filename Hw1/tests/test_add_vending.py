import requests


def test_add_vending():
    url = "http://127.0.0.1:5000/api/addVending"

    data = {
        "name": "one",
        "location": "mahidol university"
    }

    r = requests.post(url, data=data)

    assert r.json() == {'success': True}


def test_add_vending_invalid():
    url = "http://127.0.0.1:5000/api/addVending"

    data = {
        "location": "mahidol university"
    }

    r = requests.post(url, data=data)

    assert r.json() == {'success': False}


if __name__ == '__main__':
    test_add_vending()
    test_add_vending_invalid()
