from flask import Flask
from flask_cors import CORS
from flask_restplus import Api, Namespace

cors = CORS()

api = Api(version='1.0', title='WebRTC API',
          description='WebRTC API', doc='/docs')

ns = Namespace('webrtc', description='WebRTC operations')
api.add_namespace(ns)


def create_app():
    app = Flask(__name__)
    api.init_app(app)
    cors.init_app(app)
    return app
