"""Blueprint module associated with facts REST resources."""
import wonk.err as err
import flask
import flask_restful as rest
import functools
import wonk.oauth as oauth


from flask_restful import reqparse

facts_bp = flask.Blueprint('facts', __name__)

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'Access-Token', location='headers',
    required=True, dest='token',
)
parser.add_argument(
    'User-Id', location='headers',
    required=True, dest='user'
)


def authorize(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        qs = parser.parse_args()
        if not oauth.OAuthSignIn.authorized(qs.token, qs.user):
            raise err.NotAuthorizedError
        return func(**kwargs)
    return wrapper


class FactResource(rest.Resource):
    method_decorators = [authorize]


class Fact(FactResource):
    def get(self, id):
        return {'hello': 'fact no.%d' % id}


class FactList(FactResource):
    def get(self):
        modified = flask.request.headers.get('If-Modified-Since')
        if not modified:
            raise err.NotModifiedError
        return {'hello': 'list'}
