"""Blueprint module associated with authentication REST resources."""
import flask
import flask_login as login
import flask_restful as rest
import wonk.oauth as oauth

auth_bp = flask.Blueprint('auth', __name__)


class AuthProvider(rest.Resource):
    def get(self, provider):
        if not login.current_user.is_anonymous:
            print('Already signed in.')
        si = oauth.OAuthSignIn.get_provider(provider)
        return si.authorize()


class AuthCallback(rest.Resource):
    def get(self, provider):
        if not login.current_user.is_anonymous:
            print('Already signed in.')
        si = oauth.OAuthSignIn.get_provider(provider)
        social_id, username, email = si.callback()
        if social_id is None:
            print('Authentication failed.')
