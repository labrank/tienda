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

sale  = Blueprint('sales', __name__)

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

@auth.verify_password
def verify_password(username, password):
    #cualquier usuario puede hacer compras
    user = users.find_one({"name":username, "pwd":password})
    if not user:
        return False
    return True