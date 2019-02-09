from flask import request
from flask_restful import abort, Resource
from marshmallow.exceptions import ValidationError

from .schema import UserSchema
from app.models.user import User


class UsersResource(Resource):

    schema = UserSchema

    def post(self):
        try:
            self.schema().validate(request.get_json())
        except ValidationError:
            raise

        props = request.get_json()['data']['attributes']

        existing = User.query.filter(User.email == props['email']).count()

        if existing > 0:
            abort(409, message="{} exists already".format(props['email']))

        if 'password' not in props:
            abort(400, message="no password provided")

        user = User.create(**props)

        return self.schema().dump(user)

    def get(self, user_id=None):
        if user_id is not None:
            return self._get_single(user_id)
        else:
            return self._get_list()

    def _get_single(self, user_id):
        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        return self.schema().dump(user)

    def _get_list(self):

        page = int(request.args.get('p', 1))

        query = User.create_active_users_query()

        result = query.paginate(page, per_page=10, error_out=False)

        return self.schema().dump(result.items, many=True)

    def put(self, user_id):
        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        try:
            self.schema().validate(request.get_json())
        except ValidationError:
            raise

        props = request.get_json()['data']['attributes']

        user.update(**props)
        user.save()

        return self.schema().dump(user)

    def delete(self, user_id):
        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        user.delete()
        user.save()

        return {}
