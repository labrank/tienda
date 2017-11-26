from flask import Flask, jsonify, request
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.store
products = db.store.products

@app.route('/products', methods=['GET'])
def get_products():
    output = []
    for product in products.find():
        output.append({"nombre": product["name"],"precio":product["price"]})
    return jsonify({"Products":output})

@app.route('/product/<string:name>', methods=['GET'])
def get_product(name):
    product = products.find_one({"name":name})
    if product:
        output = ({"nombre": product["name"],"precio":product["price"]})
    else:
        output = "No product find"
    return jsonify({"Products":output})

@app.route('/products', methods=['POST'])
def add_products():
    nombre = request.json["name"]
    precio = request.json["price"]
    product_id = products.insert_one({"name":nombre,"price":precio}).inserted_id
    producto_nuevo = products.find_one({"_id": (product_id)})
    output = {"name":producto_nuevo["name"], "price": producto_nuevo["price"]}
    return jsonify({"Product":output})

@app.route('/products', methods=['DELETE'])
def remove_products():
    nombre = request.json["name"]
    precio = request.json["price"]
    products.remove({"name":nombre,"price":precio})
    return jsonify({"Product":"null"})

@app.route('/product/<string:name>', methods=['PUT'])
def update_products(name):
    product = products.find_one({"name":name})
    products.update_one({"_id":product["_id"]}, {"$set": request.json}, upsert=False)
    producto_nuevo = products.find_one({"name":request.json["name"]})
    output = {"name":producto_nuevo["name"], "price": producto_nuevo["price"]}
    return jsonify({"Product":output})