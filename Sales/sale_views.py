import datetime
from flask import jsonify, request, Blueprint
from Users.users_views import auth
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.store
products = db.store.products
users = db.users
sales = db.sales
sales_products = db.sales_products

sale = Blueprint('sales', __name__)

@sale.route('/sales', methods=['POST'])
@auth.login_required
def add_sales():
    total = 0
    user = users.find_one({"name":auth.username()})
    sale_id = sales.insert_one({"user":user["_id"],"date":datetime.datetime.now(), "total":total}).inserted_id
    venta_nueva = sales.find_one({"_id": (sale_id)})

    for prod in request.json["products"]:
        product = products.find_one({"name": prod})
        total += product["price"]
        sales_products.insert_one({"product":product["_id"], "sale":sale_id})
    sales.update_one({"_id": sale_id}, {"$set": {"total": total}}, upsert=False)
    output = {"user": user["name"], "date": venta_nueva["date"], "total": total}
    return jsonify({"Sale":output})

@sale.route('/sales/<string:user>', methods=['GET'])
@auth.login_required
def get_total_sales(user):
    total = 0
    user = users.find_one({"name":user})
    user_consultant = users.find_one({"name":auth.username()})
    if user_consultant["admin"]:
        sales_user = sales.find({"user":user["_id"]})
        for subtotal in sales_user:
            total += subtotal["total"]
        return jsonify({"User": user["name"], "total":total})
    return jsonify({"error":"not allowed"}), 401

@sale.route('/sales/<string:user>/<string:product>', methods=['GET'])
@auth.login_required
def get_total_product(user, product):
    #TODO: Encontrar producto del usuario y mostrar total de su compra por ese producto
    total = 0
    user = users.find_one({"name":user})
    sale = sales.find_one({"name":user["_id"]})
    return jsonify({"error":"not allowed"}), 401

@auth.verify_password
def verify_password(username, password):
    #cualquier usuario puede hacer compras
    user = users.find_one({"name":username, "pwd":password})
    if not user:
        return False
    return True