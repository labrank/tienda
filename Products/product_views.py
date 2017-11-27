from flask import jsonify, request, Blueprint
from pymongo import MongoClient
from Users.users_views import auth

client = MongoClient('localhost', 27017)
db = client.store
products = db.store.products

product = Blueprint('products', __name__)

@product.route('/products', methods=['GET'])
def get_products():
    output = []
    for product in products.find():
        output.append({"nombre": product["name"],"precio":product["price"]})
    return jsonify({"Products":output})

@product.route('/product/<string:name>', methods=['GET'])
def get_product(name):
    product = products.find_one({"name":name})
    if product:
        output = ({"nombre": product["name"],"precio":product["price"]})
    else:
        output = "No product find"
    return jsonify({"Products":output})

@product.route('/products', methods=['POST'])
@auth.login_required
def add_products():
    try:
        nombre = request.json["name"]
        precio = request.json["price"]
        product_id = products.insert_one({"name": nombre, "price": precio}).inserted_id
        producto_nuevo = products.find_one({"_id": (product_id)})
        output = {"name": producto_nuevo["name"], "price": producto_nuevo["price"]}
        return jsonify({"Product": output})
    except ValueError:
        return jsonify({"Hay un error en el ingreso de datos"})



@product.route('/products', methods=['DELETE'])
@auth.login_required
def remove_products():
    nombre = request.json["name"]
    precio = request.json["price"]
    products.remove({"name":nombre,"price":precio})
    return jsonify({"Product":"null"})

@product.route('/product/<string:name>', methods=['PUT'])
@auth.login_required
def update_products(name):
    try:
        product = products.find_one({"name":name})
        products.update_one({"_id":product["_id"]}, {"$set": request.json}, upsert=False)
        producto_nuevo = products.find_one({"name":request.json["name"]})
        output = {"name":producto_nuevo["name"], "price": producto_nuevo["price"]}
        return jsonify({"Product":output})
    except ValueError:
        return jsonify({"Hay un error en el ingreso de datos"})
