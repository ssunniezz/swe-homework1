from typing import Dict

from flask import Blueprint, Response, request

from vending_machine.service import (
    add_stock,
    add_vending,
    delete_stock,
    delete_vending,
    edit_stock,
    edit_vending,
    stock_list,
)

api_blueprint = Blueprint("api", __name__)

"""
API for listing stocks on every vending machine
"""


@api_blueprint.route("/api/stocks", methods=["GET"])
def call_stock_list() -> Response:
    """Call stock list service.

    :return: response as json
    """
    return stock_list()


"""
API for adding new vending machine, data were received through form-data
"""


@api_blueprint.route("/api/addVending", methods=["POST"])
def call_add_vending() -> Dict[str, bool]:
    """Call add vending service.

    :return: vending_info with success as boolean
    """
    return add_vending(dict(request.form))


"""
API for deleting vending machine by id, id were received through form-data
"""


@api_blueprint.route("/api/deleteVending", methods=["POST"])
def call_delete_vending() -> Dict[str, bool]:
    """Call delete vending service.

    :return: success as boolean
    """
    return delete_vending(dict(request.form))


"""
API for editing vending machine by id, id and data were received through form-data
"""


@api_blueprint.route("/api/editVending", methods=["POST"])
def call_edit_vending() -> Dict[str, bool]:
    """Call edit vending service.

    :return: success as boolean
    """
    return edit_vending(dict(request.form))


"""
API for adding stock, data were received through form-data
"""


@api_blueprint.route("/api/addStock", methods=["POST"])
def call_add_stock() -> Dict[str, bool]:
    """Call add stock service.

    :return: stock_info with success as boolean
    """
    return add_stock(dict(request.form))


"""
API for deleting stock, vending and product name were received through form-data
"""


@api_blueprint.route("/api/deleteStock", methods=["POST"])
def call_delete_stock() -> Dict[str, bool]:
    """Call delete stock service.

    :return: success as boolean
    """
    return delete_stock(dict(request.form))


"""
API for editing stock, data were received through form-data
"""


@api_blueprint.route("/api/editStock", methods=["POST"])
def call_edit_stock() -> Dict[str, bool]:
    """Call delete stock service.

    :return: success as boolean
    """
    return edit_stock(dict(request.form))
