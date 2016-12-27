"""Blueprint module associated with oauth REST resources."""
import flask
import flask_login as login
import flask_restful as rest
import wonk.oauth as oauth

oauth_bp = flask.Blueprint('oauth', __name__)


class OAuthProvider(rest.Resource):
    def get(self, provider):
        if not login.current_user.is_anonymous:
            print('Already signed in.')
        si = oauth.OAuthSignIn.get_provider(provider)
        return si.authorize()


class OAuthCallback(rest.Resource):
    def get(self, provider):
        if not login.current_user.is_anonymous:
            print('Already signed in.')
        si = oauth.OAuthSignIn.get_provider(provider)
        social_id, username, email = si.callback()
        if social_id is None:
            print('Authentication failed.')
