from flask import Flask, jsonify, request
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.store
products = db.store.products

@app.route('/products', methods=['GET'])
def get_products():
    output = []
    for product in products.find():
        output.append({"nombre": product["name"],"precio":product["price"]})
    return jsonify({"Products":output})

@app.route('/products', methods=['POST'])
def add_products():
    nombre = request.json["name"]
    precio = request.json["price"]
    product_id = products.insert({"name":nombre,"price":precio})
    producto_nuevo = products.find_one({"_id": product_id})
    return jsonify({"Product":producto_nuevo})


if __name__ == '__main__':
    app.run(debug=True)