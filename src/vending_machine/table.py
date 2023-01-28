from sqlalchemy.orm import backref

from vending_machine.db import db


class Vending(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    location = db.Column(db.String(50), default='')

    def json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Stock(db.Model):
    __table_args__ = (
        db.UniqueConstraint('name', 'vending_id', name='uid'),
    )
    id = db.Column(db.Integer, primary_key=True)
    vending_id = db.Column(db.Integer, db.ForeignKey('vending.id'), nullable=False)
    vending = db.relationship('Vending', backref=backref('stock', cascade='all,delete'))
    name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, default=0)

    def json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

