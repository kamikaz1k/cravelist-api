from datetime import datetime
import bcrypt

from sqlalchemy import func

from app.database import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    updated_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        default=func.now(),
        onupdate=func.now()
    )
    created_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    @staticmethod
    def hash_password(password):
        if isinstance(password, str):
            password = bytes(password, 'utf-8')
        return bcrypt.hashpw(password, bcrypt.gensalt())

    @classmethod
    def create(cls, **props):
        user = cls()
        user.password = cls.hash_password(props.pop('password'))
        user.update(**props)

        user.save()
        return user

    def update(self, **props):
        self.email = props.pop('email', self.email)
        self.name = props.pop('name', self.name)

    @classmethod
    def find_by_credentials(cls, email, password):
        user = cls.query.filter(
            cls.email == email,
            cls.deleted_at.is_(None)
        ).one_or_none()

        if user and cls.verify_password(password, user.password):
            return user

    @staticmethod
    def verify_password(password, hashed_password):
        if isinstance(password, str):
            password = bytes(password, 'utf-8')

        if isinstance(hashed_password, str):
            hashed_password = bytes(hashed_password, 'utf-8')

        return bcrypt.checkpw(password, hashed_password)

    @classmethod
    def create_active_users_query(cls):
        return cls.query.filter(cls.deleted_at.is_(None))

    def delete(self):
        if self.deleted_at is None:
            self.deleted_at = datetime.now()

    def reactivate(self):
        self.deleted_at = None

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def active(self):
        return self.deleted_at is None

    @property
    def deleted(self):
        return self.deleted_at is not None
