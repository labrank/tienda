from flask import Flask, jsonify

app = Flask(__name__)

from Products.product_views import product
from Users.users_views import user
from Sales.sale_views import sale

app.register_blueprint(product)
app.register_blueprint(user)
app.register_blueprint(sale)


@app.route('/', methods=['GET'])
def add_sales():
    return jsonify("Hello, store!")


if __name__ == '__main__':
    app.run(debug=True)
