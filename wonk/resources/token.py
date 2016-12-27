"""Blueprint module associated with token REST resources."""
from flask import Blueprint
from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from wonk import err
from wonk import token
from wonk.oauth import OAuthSignIn

token_bp = Blueprint('token', __name__)


class TokenProvider(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument(
            'Access-Token', location='headers',
            required=True, dest='token',
        )
        self.parser.add_argument(
            'User-Id', location='headers',
            required=True, dest='user',
        )
        self.parser.add_argument(
            'Token-Provider', location='headers',
            required=True, dest='provider',
        )

    def get(self):
        args = self.parser.parse_args()
        if not OAuthSignIn.authorized(args.provider, args.token, args.user):
            raise err.NotAuthorizedError

        _token = token.generate(data={'user': args.user})
        if not _token:
            raise err.NotAuthorizedError
        return jsonify({'token': _token.decode('ascii')})
