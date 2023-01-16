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
    sql = 'SELECT * FROM product'
    sql1 = 'SHOW COLUMNS FROM vending_machine.product'

    db = app.db
    stocks = db.engine.execute(sql)
    cols = db.engine.execute(sql1).all()

    lst = []

    for s in stocks:
        obj = OrderedDict()
        for i in range(len(cols)):
            if cols[i][0] == 'vending_id':
                vending = table.Vending.query.filter_by(id=s[i]).first()
                obj["vending"] = vending.json()
            else:
                obj[cols[i][0]] = s[i]
        lst.append(obj)

    print(lst)
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

    products = table.Product(vending=new_vending)

    db = app.db
    db.session.add(new_vending)
    db.session.add(products)
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
API for adding product, product name was received through form-data
'''


@api_blueprint.route('/api/addProduct', methods=['POST'])
def add_product():
    name = request.form.get('name')

    if not name:
        return {'success': False}

    sql = f'ALTER TABLE product ADD COLUMN {name} int DEFAULT (0)'

    db = app.db
    db.engine.execute(sql)
    setattr(table.Product, name, 0)
    print(getattr(table.Product, name))

    return {'success': True}

