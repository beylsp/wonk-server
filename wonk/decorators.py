from flask_restful import reqparse
from functools import wraps
from wonk import err
from wonk import jws


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        parser = reqparse.RequestParser(bundle_errors=True)
	parser.add_argument(
            'Authentication-Token', location='headers',
	    required=True, dest='token',
	)
        parser.add_argument(
	    'User-Id', location='headers',
	    required=True, dest='user',
        )
        _args = parser.parse_args()
        data = jws.verify_token(_args.token)
        if not data or 'user' not in data:
            raise err.NotAuthorizedError
        if data.get('user') != _args.user:
            raise err.NotAuthorizedError
        return func(**kwargs)
    return wrapper

