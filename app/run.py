import os

from flask import Flask, g
from flask_restful import Resource, Api

from .database import db


api = Api()


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL')

    db.init_app(app)
    api.init_app(app)

    return app