"""A google authentication service provider that implements OAuth2."""
import flask
import rauth

from wonk.oauth import OAuthSignIn


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.service = rauth.service.OAuth2Service(
            name='google',
            base_url='https://www.googleapis.com/oauth2/v1/',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
        )

    def authorize(self):
        return flask.redirect(self.service.get_authorize_url(
            scope='https://www.googleapis.com/auth/userinfo.profile',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in flask.request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': flask.request.args['code'],
                      'grant_type': 'authorization code',
                      'redirect_url': self.get_callback_url()}
        )
        me = oauth_session.get('me').json()
        return (
            'google$' + me['id'],
            me.get('username'),
            me.get('email')
        )
