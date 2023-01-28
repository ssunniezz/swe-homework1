from flask import Blueprint, request
from vending_machine.service import add_vending, delete_vending, edit_vending, add_stock, delete_stock, edit_stock, \
    stock_list

api_blueprint = Blueprint('api', __name__)

'''
API for listing stocks on every vending machine
'''


@api_blueprint.route('/api/stocks', methods=['GET'])
def call_stock_list():
    return stock_list()


'''
API for adding new vending machine, data were received through form-data
'''


@api_blueprint.route('/api/addVending', methods=['POST'])
def call_add_vending():
    return add_vending(dict(request.form))


'''
API for deleting vending machine by id, id were received through form-data
'''


@api_blueprint.route('/api/deleteVending', methods=['POST'])
def call_delete_vending():
    return delete_vending(dict(request.form))


'''
API for editing vending machine by id, id and data were received through form-data
'''


@api_blueprint.route('/api/editVending', methods=['POST'])
def call_edit_vending():
    return edit_vending(dict(request.form))


'''
API for adding stock, data were received through form-data
'''


@api_blueprint.route('/api/addStock', methods=['POST'])
def call_add_stock():
    return add_stock(dict(request.form))


'''
API for deleting stock, vending and product name were received through form-data
'''


@api_blueprint.route('/api/deleteStock', methods=['POST'])
def call_delete_stock():
    return delete_stock(dict(request.form))


'''
API for editing stock, data were received through form-data
'''


@api_blueprint.route('/api/editStock', methods=['POST'])
def call_edit_stock():
    return edit_stock(dict(request.form))
