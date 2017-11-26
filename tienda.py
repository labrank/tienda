from flask import Flask, jsonify
from pymongo import MongoClient


app = Flask(__name__)

@app.route('/hello', methods=['GET'])
@app.route('/', methods=['GET'])
def get_tasks():
    return jsonify("hello, world")

if __name__ == '__main__':
    app.run(debug=True)