from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

from app.database import db
from app.helpers.jwt import encode_jwt


EXPIRY_PERIOD = timedelta(days=30)


class Token(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="user")
    jwt_token = db.Column(
        db.String(300),
        nullable=False,
        index=True,
        unique=True
    )

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

    expires_on = db.Column(db.TIMESTAMP, nullable=False)
    revoked_on = db.Column(db.TIMESTAMP, nullable=True)

    def revoke(self):
        self.revoked_on = datetime.now()
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter(
            cls.jwt_token == token,
            cls.revoked_on.is_(None),
            cls.expires_on > datetime.now()
        ).one_or_none()

    @staticmethod
    def generate_jwt_params(user, expires_on):
        return {
            'user_id': user.id,
            'email': user.email,
            'exp': round(expires_on.timestamp())
        }

    @classmethod
    def create(cls, user):
        expires_on = datetime.now() + EXPIRY_PERIOD
        jwt_token = encode_jwt(cls.generate_jwt_params(user, expires_on))

        token = cls(
            user_id=user.id,
            jwt_token=jwt_token,
            expires_on=expires_on
        )
        token.save()

        return token
