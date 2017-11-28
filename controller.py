from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.store
products = db.store.products
users = db.users
sales = db.sales
sales_products = db.sales_products
