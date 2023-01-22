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
    # rename to a more meaningful name
    stock_list = []

    vendings = table.Vending.query.all()
    for vending in vendings:
        # rename to a more meaningful name
        vending_info = vending.json()

        stocks = sorted(table.Stock.query.filter_by(vending_id=vending.id).all(), key=lambda s: s.name)
        stock = {s.name: s.amount for s in stocks}

        vending_info['stock'] = stock
        stock_list.append(vending_info)

    return jsonify(stock_list)


'''
API for adding new vending machine, data were received through form-data
'''


@api_blueprint.route('/api/addVending', methods=['POST'])
def add_vending():
    cols = table.Vending.__table__.columns
    # rename to a more meaningful name
    request_data = {c.name: request.form.get(c.name) for c in cols}

    if not request_data['name']:
        return {'success': False}

    new_vending = table.Vending()
    for d in request_data:
        setattr(new_vending, d, request_data[d])

    db = app.db
    db.session.add(new_vending)
    db.session.commit()

    return {'success': True}


'''
API for deleting vending machine by id, id were received through form-data
'''


@api_blueprint.route('/api/deleteVending', methods=['POST'])
def delete_vending():
    # rename to a more meaningful name
    vending_id = request.form.get('id')
    to_delete = table.Vending.query.filter_by(id=vending_id).first()

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
    # rename to a more meaningful name
    vending_id = request.form.get('id')
    to_edit = table.Vending.query.filter_by(id=vending_id).first()

    if not to_edit:
        return {'success': False}

    # rename to a more meaningful name
    cols = table.Vending.__table__.columns
    vending_data = {c.name: request.form.get(c.name) for c in cols}
    vending_data.pop('id')

    for d in vending_data:
        if vending_data[d]:
            setattr(to_edit, d, vending_data[d])

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

    # add try-catch for invalid vending_id
    try:
        product = table.Stock(vending_id=vending_id, name=name, amount=amount)
    except:
        return {'success': False}

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

    # return false in case that amount is not parsed
    if not to_edit or not amount:
        return {'success': False}

    to_edit.amount = amount

    db = app.db
    db.session.commit()

    return {'success': True}
