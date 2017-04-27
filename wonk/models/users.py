"""Users database model and schema."""
from marshmallow import Schema
from marshmallow import fields
from . import db
import datetime as dt


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(28), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    created_at = dt.datetime.now()

    def __repr__(self):
        return '<id %r, user %r, password %r>' % (
            self.id, self.username, self.password)


class UserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
