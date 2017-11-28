import datetime
from flask import jsonify, request, Blueprint
from Users.users_views import auth
import controller

sale = Blueprint('sales', __name__)

@sale.route('/sales', methods=['POST'])
@auth.login_required
def add_sales():
    try:
        total = 0
        user = controller.users.find_one({"name":auth.username()})
        sale_id = controller.sales.insert_one({"user":user["_id"],"date":datetime.datetime.now(), "total":total}).inserted_id
        venta_nueva = controller.sales.find_one({"_id": (sale_id)})

        for prod in request.json["products"]:
            product = controller.products.find_one({"name": prod})
            total += product["price"]
            controller.sales_products.insert_one({"product":product["_id"], "sale":sale_id})
            controller.sales.update_one({"_id": sale_id}, {"$set": {"total": total}}, upsert=False)
        output = {"user": user["name"], "date": venta_nueva["date"], "total": total}
        return jsonify({"Sale":output})
    except ValueError:
        return jsonify({"Error"})

@sale.route('/sales/<string:user>', methods=['GET'])
@auth.login_required
def get_total_sales(user):
    total = 0
    user = controller.users.find_one({"name":user})
    user_consultant = controller.users.find_one({"name":auth.username()})
    if user_consultant["admin"]:
        sales_user = controller.sales.find({"user":user["_id"]})
        for subtotal in sales_user:
            total += subtotal["total"]
        return jsonify({"User": user["name"], "total":total})
    return jsonify({"error":"not allowed"}), 401

@sale.route('/sales/<string:user>/<string:product>', methods=['GET'])
@auth.login_required
def get_total_product(user, product):
    user_id = controller.users.find_one({"name":user})
    sale = controller.sales.find_one({"user":user_id["_id"]})
    user_product = controller.products.find_one({"name":product})
    sale_products = controller.sales_products.find({"sale":sale["_id"], "product":user_product["_id"]})
    buyed = sale_products.count()
    total = user_product["price"] * buyed
    output = {"User":user, "product": user_product["name"], "buyed":buyed, "total": total }
    return jsonify({"expended": output})

@auth.verify_password
def verify_password(username, password):
    #cualquier usuario puede hacer compras
    user = controller.users.find_one({"name":username, "pwd":password})
    if not user:
        return False
    return True