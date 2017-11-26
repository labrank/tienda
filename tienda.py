from flask import Flask

app = Flask(__name__)

from Products.product_views import product
app.register_blueprint(product)

if __name__ == '__main__':
    app.run(debug=True)