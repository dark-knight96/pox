from flask import Flask
from flask import jsonify, make_response

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    print("Request to index received")
    result = {"data": "Hello world!!"}
    response = make_response(jsonify(result))
    return response


if __name__ == "__main__":
    localhost = "127.0.0.1"
    port = "2000"
    print("Flask app running on " + localhost + " " + port)
    app.run(host=localhost, port=port, debug=True)