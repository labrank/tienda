from flask import jsonify, request, Blueprint
from flask_httpauth import HTTPBasicAuth
from controller import users

user = Blueprint('user', __name__)
auth = HTTPBasicAuth()

@user.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    output = []
    for user in users.find():
        output.append({"nombre": user["name"]})
    return jsonify({"users":output})

@user.route('/users', methods=['POST'])
@auth.login_required
def add_users():
    try:
        nombre = request.json["name"]
        pwd = request.json["pwd"]
        admin = request.json["admin"]
        user_id = users.insert_one({"name":nombre, "pwd":pwd, "admin":admin}).inserted_id
        nuevo_usuario = users.find_one({"_id":user_id})
        output = {"name":nuevo_usuario["name"], "password":nuevo_usuario["pwd"]}
        return jsonify({"users":output})
    except ValueError:
        return jsonify({"Hay un error en el ingreso de datos"})

@auth.verify_password
def verify_admin_password(username, password):
    user = users.find_one({"name":username, "pwd":password, "admin":bool(1)})
    if not user:
        return False
    return True