"""JSON Web Signature functions."""
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature
from itsdangerous import SignatureExpired

DEFAULT_TOKEN_EXPIRY = 60 * 10  # defaults to 10 minutes


def generate_token(data, expires_in=DEFAULT_TOKEN_EXPIRY):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
    return s.dumps(data)


def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return None
    return data
