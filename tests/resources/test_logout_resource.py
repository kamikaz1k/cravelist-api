from datetime import datetime, timedelta

from nose.tools import eq_, ok_

from app.models.token import Token
from tests.resources import BaseResourceTest


class TestLogoutResource(BaseResourceTest):

    def setup(self):
        super(TestLogoutResource, self).setup()

        self.user = self._create_user()
        self.user_token = self._create_token_for_user(self.user)

    def test_logout_success(self):
        response = self.test_client.post(
            '/api/auth/logout',
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            }
        )

        token = Token.query.filter(
            Token.jwt_token == self.user_token.jwt_token
        ).first()

        eq_(response.status_code, 200)
        ok_(token.revoked_on is not None)

    def test_logout_failure__no_token(self):
        response = self.test_client.post('/api/auth/logout')
        eq_(response.status_code, 200)

    def test_logout_failure__invalid_token(self):
        response = self.test_client.post(
            '/api/auth/logout',
            headers={
                'Authorization': 'Bearer invalidtoken'
            }
        )
        eq_(response.status_code, 200)

    def test_logout_failure__expired_token(self):
        self.user_token.expires_on = datetime.now() - timedelta(days=1)
        self.user_token.save()

        response = self.test_client.post(
            '/api/auth/logout',
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            }
        )
        eq_(response.status_code, 200)

    def test_logout_failure__revoked_token(self):
        self.user_token.revoke()
        response = self.test_client.post(
            '/api/auth/logout',
            headers={
                'Authorization': 'Bearer ' + self.user_token.jwt_token
            }
        )
        eq_(response.status_code, 200)
