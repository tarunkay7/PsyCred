from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/home',methods=["GET"])
def hello():
    return jsonify("hello")


if __name__ == '__main__':
    app.run(debug=True)