from typing import Dict, Set

from flask import Response, jsonify
from sqlalchemy import exc

from vending_machine import app, table
from vending_machine.table import StockTimeline


def add_vending(request_data: Dict[str, str]) -> Dict[str, bool]:
    """Add new vending machine.

    :param request_data: vending_info from the request
    :return: vending_info with success as boolean
    """
    if not request_data.__contains__("name"):
        return {"success": False}

    new_vending = table.Vending()
    for d in request_data:
        setattr(new_vending, d, request_data[d])

    db = app.db
    db.session.add(new_vending)
    db.session.commit()

    new_vending_info = new_vending.json()
    new_vending_info.update({"success": True})
    return new_vending_info


def edit_vending(request_data: Dict[str, str]) -> Dict[str, bool]:
    """Edit existing vending machine.

    :param request_data: vending_info from request
    :return: success as boolean
    """
    # rename to a more meaningful name
    vending_id = request_data.pop("id")
    to_edit = table.Vending.query.filter_by(id=vending_id).first()

    if not to_edit:
        return {"success": False}

    vending_data = request_data

    for d in vending_data:  # pragma :no cover
        if vending_data[d]:  # pragma :no cover
            setattr(to_edit, d, vending_data[d])  # pragma :no cover

    db = app.db
    db.session.commit()

    return {"success": True}


def delete_vending(request_data: Dict[str, str]) -> Dict[str, bool]:
    """Delete existing vending_machine by id.

    :param request_data: vending_id from request
    :return: success as boolean
    """
    # rename to a more meaningful name
    vending_id = request_data["id"]
    to_delete = table.Vending.query.filter_by(id=vending_id).first()

    if not to_delete:
        return {"success": False}

    db = app.db
    db.session.delete(to_delete)
    db.session.commit()

    return {"success": True}


def add_stock(request_data: Dict[str, str]) -> Dict[str, bool]:
    """Add new stock.

    :param request_data: vending_id, name, and amount from request
    :return: stock_info with success as boolean
    """
    if not request_data.__contains__("vending_id") or not request_data.__contains__("name"):
        return {"success": False}

    vending_id = request_data.get("vending_id")
    name = request_data.get("name").lower()
    amount = request_data.get("amount")

    db = app.db
    # add try-catch for invalid vending_id
    try:
        product = table.Stock(vending_id=vending_id, name=name, amount=amount)
        timeline = StockTimeline(vending_id=vending_id, product=name, amount=amount)
        db.session.add(product)
        db.session.add(timeline)
        db.session.commit()
    except exc.DatabaseError:
        db.session.rollback()
        return {"success": False}

    product_info = product.json()
    product_info.update({"success": True})

    return product_info


def edit_stock(request_data: Dict[str, str]) -> Dict[str, bool]:
    """Edit existing stock.

    :param request_data: vending_id, name, and amount from request
    :return: success as boolean
    """
    if not request_data.__contains__("vending_id") or not request_data.__contains__("name"):
        return {"success": False}

    vending_id = request_data.get("vending_id")
    name = request_data.get("name").lower()
    amount = request_data.get("amount")

    to_edit = table.Stock.query.filter_by(vending_id=vending_id, name=name).first()

    # return false if the stock does not exist
    if not to_edit:
        return {"success": False}

    to_edit.amount = amount
    timeline = StockTimeline(vending_id=vending_id, product=name, amount=amount)

    db = app.db
    db.session.add(timeline)
    db.session.commit()

    return {"success": True}


def delete_stock(request_data: Dict[str, str]) -> Dict[str, bool]:
    """Delete existing stock.

    :param request_data: vending_id, name from request
    :return: success as boolean
    """
    if not request_data.__contains__("vending_id") or not request_data.__contains__("name"):
        return {"success": False}

    vending_id = request_data.get("vending_id")
    name = request_data.get("name").lower()

    to_delete = table.Stock.query.filter_by(vending_id=vending_id, name=name).first()

    if not to_delete:
        return {"success": False}

    timeline = StockTimeline(vending_id=vending_id, product=name, amount=0)

    db = app.db
    db.session.delete(to_delete)
    db.session.add(timeline)
    db.session.commit()

    return {"success": True}


def stock_list() -> Response:
    """Get all stocks.

    :return: Json response including all vending_info with all stocks init.
    """
    # rename to a more meaningful name
    stock_lst = []

    vendings = table.Vending.query.all()
    for vending in vendings:
        # rename to a more meaningful name
        vending_info = vending.json()

        stocks = sorted(table.Stock.query.filter_by(vending_id=vending.id).all(), key=lambda s: s.name)
        stock = {s.name: s.amount for s in stocks}

        vending_info["stock"] = stock
        stock_lst.append(vending_info)

    return jsonify(stock_lst)


def stock_timeline_by_product(request_data: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    """List stock timeline of the product in each vending machine.

    :param request_data: product name
    :return: stock timeline of the product in each vending machine
    """
    product = request_data.get("product")
    timelines = StockTimeline.query.filter_by(product=product).all()

    to_return = {}

    for timeline in timelines:
        vending_id = timeline.vending_id
        time = timeline.time.strftime("%Y-%m-%d, %H:%M:%S GMT")

        if to_return.__contains__(vending_id):
            to_return[vending_id].update({time: timeline.amount})
        else:
            to_return[vending_id] = {time: timeline.amount}

    to_return["success"] = True

    return to_return


def stock_timeline_by_vending(request_data: Dict[str, str]) -> Dict[str, Set[str]]:
    """List all products in current vending machine at each time.

    :param request_data:
    :return: products in current vending machine at each time
    """
    vending_id = request_data.get("vending_id")
    timelines = StockTimeline.query.filter_by(vending_id=vending_id).all()

    to_return = {}
    current_products = set()

    for timeline in timelines:
        time = timeline.time.strftime("%Y-%m-%d, %H:00 GMT")

        current_products.add(timeline.product)
        if timeline.amount == 0:
            current_products.remove(timeline.product)

        to_return[time] = current_products.copy()

    to_return = dict(map(lambda item: (item[0], list(item[1])), to_return.items()))

    to_return["success"] = True

    return to_return
