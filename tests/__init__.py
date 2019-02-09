from email.utils import format_datetime
from os import environ

from json_delta import udiff
from nose.tools import eq_
from sqlalchemy import event

from app import create_app, db
from app.models.token import Token
from app.models.user import User


DB_NAME = 'test'
LOCAL_DB_TEST_URL = "mysql+mysqldb://root@localhost/{}?charset=utf8".format(
    DB_NAME
)


class BaseDatabaseTestCase(object):
    # Having a global app saves on test cleanup and instantiation
    # Also, since connection pools are bound to engines
    # this allows connections to be pooled correctly
    # instead of having idle connections
    app = None

    def __init__(self):
        super(BaseDatabaseTestCase, self).__init__()
        test_config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': environ.get(
                'TEST_DATABASE_URL',
                LOCAL_DB_TEST_URL
            )
        }

        if BaseDatabaseTestCase.app is None:
            BaseDatabaseTestCase.app = create_app(test_config)
            self._setup_database()

    def _setup_database(self):
        with self.app.app_context():
            # Create DB if it doesn't exist
            db.engine.execute(
                'CREATE DATABASE IF NOT EXISTS {};'.format(DB_NAME)
            )

            # Create tables if they dont exist
            db.create_all()
            db.engine.execute('SET FOREIGN_KEY_CHECKS = 0;')
            for table in db.metadata.sorted_tables:
                db.engine.execute('TRUNCATE TABLE {};'.format(table.name))
            db.engine.execute('SET FOREIGN_KEY_CHECKS = 1;')

    def setup(self):
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        self._setup_nested_txn()

    def _setup_nested_txn(self):
        # connect to the database
        self.connection = db.engine.connect()

        # begin a non-ORM transaction
        self.transaction = self.connection.begin()

        options = dict(bind=self.connection, binds={})
        self.session = db.create_scoped_session(options=options)

        db.session = self.session

        # then each time that SAVEPOINT ends, reopen it
        @event.listens_for(self.session, "after_transaction_end")
        def restart_savepoint(session, transaction):
            if transaction.nested and not transaction._parent.nested:
                session.expire_all()

                session.begin_nested()

    def _teardown_nested_txn(self):
        self.session.close()
        self.transaction.rollback()
        self.connection.close()

    def teardown(self):
        self._teardown_nested_txn()
        self._ctx.pop()

    def assert_json(self, expected, actual):
        diff = "\n".join(udiff(expected, actual))
        eq_(diff, ' {...}', diff)

    def assert_datetime(self, expected, actual):
        if not isinstance(expected, str):
            expected = format_datetime(expected)

        if not isinstance(actual, str):
            actual = format_datetime(actual)

        return eq_(actual, expected)

    def _create_user(self, **overrides):
        options = {
            'email': "regularuser@regularuser.com",
            'name': "regularuser",
            'password': "123123123"
        }
        options.update(overrides)
        return User.create(**options)

    # def _create_admin_user(self, **overrides):
    #     options = {
    #         'email': "adminuser@adminuser.com",
    #         'name': "adminuser",
    #         'password': "123123123",
    #         'is_admin': True,
    #         'is_user_manager': False
    #     }
    #     options.update(overrides)
    #     return self._create_user(**options)

    def _create_token_for_user(self, user):
        return Token.create(user)
