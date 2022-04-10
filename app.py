from flask import Flask
from flask.ext.cors import CORS, cross_origin
from flask_restful import Api

from daosnapshot import DAO
app = Flask(__name__)
api = Api(app)

api.add_resource(DAO, "/dao/<string:n>")

cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


if __name__ == "__main__":
  app.run()

@app.route('/foo', methods=['POST','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
