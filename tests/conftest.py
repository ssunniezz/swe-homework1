import pytest
from flask import Flask
from flask.testing import FlaskClient

from vending_machine.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True, "WTF_CSRF_ENABLED": False})

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()
