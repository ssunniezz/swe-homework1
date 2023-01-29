import os

from dotenv import load_dotenv
from flask import Flask

from vending_machine import api
from vending_machine.db import db


def create_app() -> Flask:
    """Create flask app.

    :return: Flask app
    """
    app = Flask(__name__)
    app.register_blueprint(api.api_blueprint)

    load_dotenv()
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{user}:{password}@{host}:{port}/vending_machine"
    app.config["JSON_SORT_KEYS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app = create_app()
    app.run(host="localhost", port=8081, debug=True)
