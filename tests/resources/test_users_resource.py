from nose.tools import eq_

from app.models.user import User
from tests.resources import BaseResourceTest


class TestUserResource(BaseResourceTest):

    def _create_user_payload(self, properties):
        user_id = properties.pop('id', None)
        payload = {
            "data": {
                "type": "users",
                "attributes": properties
            }
        }

        if user_id:
            payload['data']['id'] = user_id

        return payload

    def test_create_user(self):
        user_email = "regularuser@regularuser.com"
        response = self.test_client.post(
            '/api/users',
            json=self._create_user_payload({
                'email': user_email,
                'password': "123123",
                'name': "regularuser"
            })
        )

        eq_(response.status_code, 200)

        user = User.query.filter(User.email == user_email).first()
        self.assert_json(
            response.json,
            {
                "data": {
                    "type": "users",
                    "attributes": {
                        'email': 'regularuser@regularuser.com',
                        'name': 'regularuser',
                        'active': True
                    },
                    "id": user.id,
                    "links": {
                        "self": "/users/{}".format(user.id)
                    }
                },
                "links": {
                    "self": "/users/{}".format(user.id)
                }
            }
        )
