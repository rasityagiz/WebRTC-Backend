from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "<h1>It's working!</h1>"


@app.route("/get", methods=["GET"])
def get():
    return {'Deneme': 'Başarılı'}


if __name__ == "__main__":
    app.run()
