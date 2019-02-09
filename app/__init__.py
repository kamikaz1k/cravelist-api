import os

from flask import Flask
from flask_restful import Resource, Api

from .database import db
from .resources.users import UsersResource
from .resources.auth import LoginResource, LogoutResource


api = Api()


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

api.add_resource(
    UsersResource,
    '/api/users',
    '/api/users/<int:user_id>'
)

api.add_resource(LoginResource, '/api/auth/login')
api.add_resource(LogoutResource, '/api/auth/logout')


def create_app(config={}):

    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL')
    app.config['JWT_SECRET'] = os.environ.get('JWT_SECRET', 'super-secret')

    app.config.update(config)

    db.init_app(app)
    api.init_app(app)

    return app
