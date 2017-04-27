"""Blueprint module associated with REST authentication endpoints."""
import flask
import flask_restful as rest
import flask_bcrypt as bcrypt
from flask import g
from flask import request
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from wonk import err
from wonk.models.users import User


class RestHTTPBasicAuth(HTTPBasicAuth):
    def _verify_password(self, pwd_hash, password):
        return bcrypt.check_password_hash(pwd_hash, password)

    def _verify_http_auth(self):
        auth = request.authorization
        if auth:
            user = User.query.filter_by(username=auth.username).first()
        else:
            return False
        if user and self._verify_password(user.password, auth.password):
            g.user = user
            return True
        return False

    def http_auth_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if self._verify_http_auth():
                return f(*args, **kwargs)
            raise err.NotAuthorizedError
        return decorated


blueprint = flask.Blueprint('auth', __name__)
auth = RestHTTPBasicAuth()


class Login(rest.Resource):
    @auth.http_auth_required
    def post(self):
        return {'access_token': 'hello world'}


class Logout(rest.Resource):
    def post(self):
        return {'access_token': 'hello world'}
