from typing import Dict

from flask import jsonify
from sqlalchemy import exc

from vending_machine import table, app


def add_vending(request_data: Dict[str, str]):
    if not request_data.__contains__('name'):
        return {'success': False}

    new_vending = table.Vending()
    for d in request_data:
        setattr(new_vending, d, request_data[d])

    db = app.db
    db.session.add(new_vending)
    db.session.commit()

    new_vending_info = new_vending.json()
    new_vending_info.update({'success': True})
    return new_vending_info


def edit_vending(request_data: Dict[str, str]):
    # rename to a more meaningful name
    vending_id = request_data.pop('id')
    to_edit = table.Vending.query.filter_by(id=vending_id).first()

    if not to_edit:
        return {'success': False}

    vending_data = request_data

    for d in vending_data:
        if vending_data[d]:
            setattr(to_edit, d, vending_data[d])

    db = app.db
    db.session.commit()

    return {'success': True}


def delete_vending(request_data: Dict[str, str]):
    # rename to a more meaningful name
    vending_id = request_data['id']
    to_delete = table.Vending.query.filter_by(id=vending_id).first()

    if not to_delete:
        return {'success': False}

    db = app.db
    db.session.delete(to_delete)
    db.session.commit()

    return {'success': True}


def add_stock(request_data: Dict[str, str]):
    if not request_data.__contains__('vending_id') or not request_data.__contains__('name'):
        return {'success': False}

    vending_id = request_data.get('vending_id')
    name = request_data.get('name').lower()
    amount = request_data.get('amount')

    db = app.db
    # add try-catch for invalid vending_id
    try:
        product = table.Stock(vending_id=vending_id, name=name, amount=amount)
        db.session.add(product)
        db.session.commit()
    except exc.DatabaseError:
        db.session.rollback()
        return {'success': False}

    product_info = product.json()
    product_info.update({'success': True})

    return product_info


def edit_stock(request_data: Dict[str, str]):
    if not request_data.__contains__('vending_id') or not request_data.__contains__('name'):
        return {'success': False}

    vending_id = request_data.get('vending_id')
    name = request_data.get('name').lower()
    amount = request_data.get('amount')

    to_edit = table.Stock.query.filter_by(vending_id=vending_id, name=name).first()

    # return false if the stock does not exist
    if not to_edit:
        return {'success': False}

    to_edit.amount = amount

    db = app.db
    db.session.commit()

    return {'success': True}


def delete_stock(request_data: Dict[str, str]):
    if not request_data.__contains__('vending_id') or not request_data.__contains__('name'):
        return {'success': False}

    vending_id = request_data.get('vending_id')
    name = request_data.get('name').lower()

    to_delete = table.Stock.query.filter_by(vending_id=vending_id, name=name).first()

    if not to_delete:
        return {'success': False}

    db = app.db
    db.session.delete(to_delete)
    db.session.commit()

    return {'success': True}


def stock_list():
    # rename to a more meaningful name
    stock_lst = []

    vendings = table.Vending.query.all()
    for vending in vendings:
        # rename to a more meaningful name
        vending_info = vending.json()

        stocks = sorted(table.Stock.query.filter_by(vending_id=vending.id).all(), key=lambda s: s.name)
        stock = {s.name: s.amount for s in stocks}

        vending_info['stock'] = stock
        stock_lst.append(vending_info)

    return jsonify(stock_lst)
