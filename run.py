from flask_restplus import Resource, fields
from webrtc import ns, create_app

app = create_app()


@ns.route("/get")
class Get(Resource):
    def get(self):
        return {'Deneme': 'Başarılı'}


@app.route("/", methods=["GET"])
def home():
    return "<h1>It's working!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
