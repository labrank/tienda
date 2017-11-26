from flask import jsonify, request, Blueprint
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.store
users = db.users

user = Blueprint('user', __name__)
auth = HTTPBasicAuth()

@user.route('/users', methods=['GET'])
@auth.login_required
def get_products():
    output = []
    for user in users.find():
        output.append({"nombre": user["name"], "password":user["pwd"]})
    return jsonify({"users":output})

@auth.verify_password
def verify_password(username, password):
    user = users.find_one({"name":username, "pwd":password})
    if not user:
        return False
    return True