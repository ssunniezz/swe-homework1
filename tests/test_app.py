from flask import Flask

from vending_machine.app import create_app


def test_create_app():
    app = create_app()
    assert type(app) == Flask
