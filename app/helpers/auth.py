from functools import wraps

from flask import g, request
from flask_restful import abort

from app.models.token import Token


def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = extract_token_from_request(request)
        user = _get_user_from_token(token)

        if user is None:
            abort(401)

        g.user = user
        return func(*args, **kwargs)
    return wrapper


def authorize_if_token_available(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = extract_token_from_request(request)
        g.user = _get_user_from_token(token)

        return func(*args, **kwargs)
    return wrapper


def extract_token_from_request(request):
    auth_header = request.headers.get('Authorization', "")
    return auth_header.replace('Bearer ', "")


def _get_user_from_token(jwt_token):
    if jwt_token:
        token = Token.find_by_token(jwt_token)
        if token is not None:
            return token.user
