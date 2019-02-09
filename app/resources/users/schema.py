from marshmallow_jsonapi import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    email = fields.Str()
    name = fields.Str()
    active = fields.Bool()

    class Meta:
        type_ = 'users'
        self_url = '/users/{id}'
        self_url_kwargs = {'id': '<id>'}
        self_url_many = '/users'
        strict = True
