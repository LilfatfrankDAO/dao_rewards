from flask import Flask
from flask_restful import Api

from daosnapshot import DAO

app = Flask(__name__)
api = Api(app)

api.add_resource(DAO, "/dao/<string:n>")

if __name__ == "__main__":
  app.run()