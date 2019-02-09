from tests import BaseDatabaseTestCase


class BaseResourceTest(BaseDatabaseTestCase):

    def __init__(self):
        super(BaseResourceTest, self).__init__()
        self.test_client = self.app.test_client()

    def setup(self):
        super(BaseResourceTest, self).setup()
