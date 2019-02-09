from nose.tools import eq_

from app.models.token import Token
from tests.resources import BaseResourceTest


class TestLoginResource(BaseResourceTest):

    def test_login_success(self):
        PASSWORD = "secretpass"
        user = self._create_user(password=PASSWORD)

        response = self.test_client.post(
            '/api/auth/login',
            json={
                'email': user.email,
                'password': PASSWORD
            }
        )

        token_record = Token.query.filter(Token.user_id == user.id).first()

        eq_(response.status_code, 200)
        eq_(response.json, {'token': token_record.jwt_token})

    def test_login_failure(self):
        user = self._create_user()

        response = self.test_client.post(
            '/api/auth/login',
            json={
                'email': user.email,
                'password': "IamAHackerman"
            }
        )

        eq_(response.status_code, 401)
        eq_(response.json, {'message': "username and password do not match"})

    def test_login_malformed(self):
        user = self._create_user()

        response = self.test_client.post(
            '/api/auth/login',
            json={
                'email': user.email
            }
        )
        eq_(response.status_code, 400)
        eq_(response.json, {'message': "missing email and password"})

        response = self.test_client.post(
            '/api/auth/login',
            json={
                'password': "IamAHackerman"
            }
        )
        eq_(response.status_code, 400)
        eq_(response.json, {'message': "missing email and password"})
