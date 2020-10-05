from flask import Flask,jsonify
app = Flask(__name__)


@app.route('/')
def hello():
    return jsonify(message = 'Hello world!'),200