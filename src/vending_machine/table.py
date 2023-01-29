from typing import Dict

from sqlalchemy.orm import backref

from vending_machine.db import db


class Vending(db.Model):
    """Vending machine object.

    id: Primary key
    name: Vending machine name
    location: Location of vending machine
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    location = db.Column(db.String(50), default="")

    def json(self) -> Dict[str, str]:
        """Turn vending_info into a dictionary.

        :return: vending_info as a dictionary
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Stock(db.Model):
    """Stock object.

    id: Primary key
    vending_id: Foreign key with Vending.id
    name: Product name
    amount: Amount of product
    """

    __table_args__ = (db.UniqueConstraint("name", "vending_id", name="uid"),)
    id = db.Column(db.Integer, primary_key=True)
    vending_id = db.Column(db.Integer, db.ForeignKey("vending.id"), nullable=False)
    vending = db.relationship("Vending", backref=backref("stock", cascade="all,delete"))
    name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, default=0)

    def json(self) -> Dict[str, str]:
        """Turn stock_info into a dictionary.

        :return: stock_info as a dictionary
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
