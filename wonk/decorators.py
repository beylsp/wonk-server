from flask_restful import reqparse
from functools import wraps
from wonk import err
from wonk import jws


def _parse_req_args():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument(
        'Authentication-Token', location='headers',
        required=True, dest='token',
    )
    parser.add_argument(
        'User-Id', location='headers',
        required=True, dest='user',
    )
    return parser.parse_args(strict=True)


def _raise_if_invalid_token(token, user):
    if not jws.is_valid_token(token, user):
        raise err.NotAuthorizedError


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        g = _parse_req_args()
        _raise_if_invalid_token(g.token, g.user)
        return func(**kwargs)
    return wrapper
