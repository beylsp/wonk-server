"""Blueprint module associated with facts REST resources."""
from flask import Blueprint
from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from functools import wraps
from wonk import err
from wonk import token

facts_bp = Blueprint('facts', __name__)

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'Authentication-Token', location='headers',
    required=True, dest='token',
)
parser.add_argument(
    'User-Id', location='headers',
    required=True, dest='user',
)


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _args = parser.parse_args()
        data = token.verify(_args.token)
        if not data or 'user' not in data:
            raise err.NotAuthorizedError
        if data.get('user') != _args.user:
            raise err.NotAuthorizedError
        return func(**kwargs)
    return wrapper


class FactResource(Resource):
    method_decorators = [token_required]


class Fact(FactResource):
    def get(self, id):
        return {'hello': 'fact no.%d' % id}


class FactList(FactResource):
    def get(self):
        modified = request.headers.get('If-Modified-Since')
        if not modified:
            raise err.NotModifiedError
        return {'hello': 'list'}
