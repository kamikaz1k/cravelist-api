from flask import request
from flask_restful import abort, Resource

from app.helpers.auth import extract_token_from_request
from app.models.user import User
from app.models.token import Token


class LoginResource(Resource):
    def post(self):
        params = request.get_json()

        if 'email' not in params or 'password' not in params:
            abort(400, message="missing email and password")

        existing_user = User.find_by_credentials(
            email=params['email'],
            password=params['password']
        )

        if existing_user is None:
            abort(401, message="username and password do not match")

        token = Token.create(existing_user)

        return {'token': token.jwt_token}


class LogoutResource(Resource):
    def post(self):
        jwt_token = extract_token_from_request(request)

        token = Token.query.filter(
            Token.jwt_token == jwt_token,
            Token.revoked_on.is_(None)
        ).one_or_none()

        if token:
            token.revoke()

        return {}
