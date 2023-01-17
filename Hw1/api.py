from collections import OrderedDict

from flask import Blueprint, request, jsonify

import app
import table

api_blueprint = Blueprint('api', __name__)

'''
API for listing stocks on every vending machine
'''


@api_blueprint.route('/api/stocks', methods=['GET'])
def stock_list():
    lst = []

    vendings = table.Vending.query.all()
    for vending in vendings:
        d = vending.json()

        stocks = sorted(table.Stock.query.filter_by(vending_id=vending.id).all(), key=lambda s: s.name)
        stock = {s.name: s.amount for s in stocks}

        d['stock'] = stock
        lst.append(d)

    return jsonify(lst)


'''
API for adding new vending machine, data were received through form-data
'''


@api_blueprint.route('/api/addVending', methods=['POST'])
def add_vending():
    cols = table.Vending.__table__.columns
    data = {c.name: request.form.get(c.name) for c in cols}

    if not data['name']:
        return {'success': False}

    new_vending = table.Vending()
    for d in data:
        setattr(new_vending, d, data[d])

    db = app.db
    db.session.add(new_vending)
    db.session.commit()

    return {'success': True}


'''
API for deleting vending machine by id, id were received through form-data
'''


@api_blueprint.route('/api/deleteVending', methods=['POST'])
def delete_vending():
    id = request.form.get('id')
    to_delete = table.Vending.query.filter_by(id=id).first()

    if not to_delete:
        return {'success': False}

    db = app.db
    db.session.delete(to_delete)
    db.session.commit()

    return {'success': True}


'''
API for editing vending machine by id, id and data were received through form-data
'''


@api_blueprint.route('/api/editVending', methods=['POST'])
def edit_vending():
    id = request.form.get('id')
    to_edit = table.Vending.query.filter_by(id=id).first()

    if not to_edit:
        return {'success': False}

    cols = table.Vending.__table__.columns
    data = {c.name: request.form.get(c.name) for c in cols}
    data.pop('id')

    for d in data:
        if data[d]:
            setattr(to_edit, d, data[d])

    db = app.db
    db.session.commit()

    return {'success': True}


'''
API for adding stock, data were received through form-data
'''


@api_blueprint.route('/api/addStock', methods=['POST'])
def add_stock():
    vending_id = request.form.get('vending_id')
    name = request.form.get('name').lower()
    amount = request.form.get('amount')

    product = table.Stock(vending_id=vending_id, name=name, amount=amount)

    db = app.db
    db.session.add(product)
    db.session.commit()

    return {'success': True}


'''
API for deleting stock, vending and product name were received through form-data
'''


@api_blueprint.route('/api/deleteStock', methods=['POST'])
def delete_stock():
    vending_id = request.form.get('vending_id')
    name = request.form.get('name').lower()

    to_delete = table.Stock.query.filter_by(vending_id=vending_id, name=name).first()

    if not to_delete:
        return {'success': False}

    db = app.db
    db.session.delete(to_delete)
    db.session.commit()

    return {'success': True}


'''
API for editing stock, data were received through form-data
'''


@api_blueprint.route('/api/editStock', methods=['POST'])
def edit_stock():
    vending_id = request.form.get('vending_id')
    name = request.form.get('name').lower()
    amount = request.form.get('amount')

    to_edit = table.Stock.query.filter_by(vending_id=vending_id, name=name).first()

    if not to_edit:
        return {'success': False}

    to_edit.amount = amount

    db = app.db
    db.session.commit()

    return {'success': True}
