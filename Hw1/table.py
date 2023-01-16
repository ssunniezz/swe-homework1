from sqlalchemy.orm import backref

from db import db


class Vending(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    location = db.Column(db.String(50), default='')

    def json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vending_id = db.Column(db.Integer, db.ForeignKey('vending.id'), unique=True)
    vending = db.relationship('Vending', backref=backref('product', cascade='all,delete'))
    coke = db.Column(db.Integer, default=0)
    taro = db.Column(db.Integer, default=0)
    lays = db.Column(db.Integer, default=0)

    def json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

