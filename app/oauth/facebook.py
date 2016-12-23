"""A facebook authentication service provider that implements OAuth2."""
import flask
import rauth

from app.oauth import OAuthSignIn


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = rauth.service.OAuth2Service(
            name='facebook',
            base_url='http://graph.facebook.com',
            access_token_url='http://graph.facebook.com/oauth/access_token',
            authorize_url='https://www.facebook.com/dialog/oauth',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
        )

    def authorize(self):
        return flask.redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in flask.request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': flask.request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()}
        )
        me = oauth_session.get('me').json()
        return (
            'facebook$' + me['id'],
            me.get('email').split('@')[0],  # Facebook  does not provide
                                            # username, so the email's user
                                            # is used instead
            me.get('email')
        )
