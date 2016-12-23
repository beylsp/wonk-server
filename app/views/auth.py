"""Blueprint module associated with authentication view functions."""
import flask
import flask_login as login

from app.oauth import OAuthSignIn

auth = flask.Blueprint('auth', __name__)


@auth.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@auth.route('/callback/<provider>')
def oauth_callback(provider):
    if not login.current_user.is_anonymous:
        return flask.redirect(flask.url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        print('Authentication failed.')
        return flask.redirect(flask.url_for('index'))
