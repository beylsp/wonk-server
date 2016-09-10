"""Blueprint module associated with authentication view functions."""
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask_login import current_user

from app.oauth import OAuthSignIn

auth = Blueprint('auth', __name__)


@auth.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@auth.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        print('Authentication failed.')
        return redirect(url_for('index'))
