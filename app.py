
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from daosnapshot import DAO

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(DAO, "/dao/<string:n>")

if __name__ == "__main__":
  app.run()