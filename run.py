from flask import Flask
from flask_restplus import Api, Resource, fields
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='WebRTC API',
          description='WebRTC API', doc='/docs')

ns = api.namespace('webrtc', description='WebRTC operations')


@ns.route("/get")
class Get(Resource):
    def get(self):
        return {'Deneme': 'Başarılı'}


@app.route("/", methods=["GET"])
def home():
    return "<h1>It's working!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
