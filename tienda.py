from flask import Flask

app = Flask(__name__)

from Products.product_views import product
from Users.users_views import user
app.register_blueprint(product)
app.register_blueprint(user)

if __name__ == '__main__':
    app.run(debug=True)