from flask import Flask

from vending_machine import api
from vending_machine.db import db


def create_app() -> Flask:
    """Create flask app.

    :return: Flask app
    """
    app = Flask(__name__)
    app.register_blueprint(api.api_blueprint)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mariadb+mariadbconnector://sun:sun@127.0.0.1:3306/vending_machine"
    app.config["JSON_SORT_KEYS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app = create_app()
    app.run(host="localhost", port=8081, debug=True)
