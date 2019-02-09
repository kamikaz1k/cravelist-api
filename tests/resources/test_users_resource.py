from nose.tools import eq_, ok_

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
                        'email': "regularuser@regularuser.com",
                        'name': "regularuser",
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

    def test_update_user(self):
        user_email = "regularuser@regularuser.com"
        response = self.test_client.post(
            '/api/users',
            json=self._create_user_payload({
                'email': user_email,
                'password': "123123",
                'name': "regularuser"
            })
        )

        user_id = response.json['data']['id']
        payload = response.json
        payload['data']['attributes']['name'] = "MY NAME IS SLIMM"

        response = self.test_client.put(
            '/api/users/{}'.format(user_id),
            json=payload
        )

        eq_(response.status_code, 200)

        self.assert_json(
            response.json,
            {
                "data": {
                    "type": "users",
                    "attributes": {
                        'email': "regularuser@regularuser.com",
                        'name': "MY NAME IS SLIMM",
                        'active': True
                    },
                    "id": user_id,
                    "links": {
                        "self": "/users/{}".format(user_id)
                    }
                },
                "links": {
                    "self": "/users/{}".format(user_id)
                }
            }
        )

    def test_delete_user(self):
        user_email = "regularuser@regularuser.com"
        response = self.test_client.post(
            '/api/users',
            json=self._create_user_payload({
                'email': user_email,
                'password': "123123",
                'name': "regularuser"
            })
        )

        user_id = response.json['data']['id']

        user = User.query.filter(User.id == user_id).first()
        ok_(user)

        response = self.test_client.delete('/api/users/{}'.format(user_id))
        eq_(response.status_code, 200)
        ok_(User.query.filter(User.id == user_id).first().deleted)

    def test_get_user(self):
        user = self._create_user()

        response = self.test_client.get('/api/users/{}'.format(user.id))

        self.assert_json(
            response.json,
            {
                "data": {
                    "type": "users",
                    "attributes": {
                        'email': user.email,
                        'name': user.name,
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
