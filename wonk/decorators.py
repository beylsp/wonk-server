from flask_restful import reqparse
from functools import wraps
from wonk import err
from wonk import jws


def _parse_args():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument(
        'Authentication-Token', location='headers',
        required=True, dest='token',
    )
    parser.add_argument(
        'User-Id', location='headers',
        required=True, dest='user',
    )
    return parser.parse_args()


def _raise_if_invalid_token(args):
    data = jws.verify_token(args.token)
    if not data or 'user' not in data:
        raise err.NotAuthorizedError
    if data.get('user') != args.user:
        raise err.NotAuthorizedError


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _raise_if_invalid_token(_parse_args())
        return func(**kwargs)
    return wrapper
