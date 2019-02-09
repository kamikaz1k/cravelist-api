from flask import current_app
import jwt


def encode_jwt(jwt_dict):
    return jwt.encode(jwt_dict, current_app.config['JWT_SECRET'])


def decode_jwt(jwt_string):
    return jwt.decode(jwt_string, current_app.config['JWT_SECRET'])
