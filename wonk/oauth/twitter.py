"""A twitter authentication service provider that implements OAuth 1.0a."""
import flask
import rauth

from wonk.oauth import OAuthSignIn


class TwitterSignIn(OAuthSignIn):
    def __init__(self):
        super(TwitterSignIn, self).__init__('twitter')
        self.service = rauth.service.OAuth1Service(
            name='twitter',
            base_url='https://api.twitter.com/1.1',
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
        )

    def authorize(self):
        request_token = self.service.get_request_token(
            params={'oauth_callback': self.get_callback_url()}
        )
        flask.session['request_token'] = request_token
        return flask.redirect(
            self.service.get_authorize_url(request_token[0]))

    def callback(self):
        request_token = flask.session.pop('request_token')
        if 'oauth_verifier' not in flask.request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            request_token[0], request_token[1],
            data={'oauth_verifier': flask.request.args['oauth_verifier']}
        )
        me = oauth_session.get('1.1/account/verify_credentials.json').json()
        social_id = 'twitter$' + str(me.get('id'))
        username = me.get('screen_name')
        return social_id, username, None  # Twitter does not provide email
