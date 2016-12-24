"""A google authentication service provider that implements OAuth2."""
import flask
import json
import rauth
import requests

from rauth.compat import urljoin
from wonk.oauth import OAuthSignIn


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.service = rauth.service.OAuth2Service(
            name='google',
            base_url='https://www.googleapis.com/oauth2/v1/',
            access_token_url='https://www.googleapis.com/oauth2/v4/token',
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

    def authorized(self, access_token, user):
        session = self.service.session_obj(access_token=access_token)
        url = urljoin(self.service.base_url, 'userinfo')
        r = session.get(url, params={'access_token': access_token})
        if not r.status_code == requests.codes.ok:
            return False
        return r.json().get('id') == user

    def callback(self):
        if 'code' not in flask.request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
                decoder=self._parse,
                data={'code': flask.request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()}
        )
        userinfo = oauth_session.get('userinfo').json()
        social_id = 'google$' + str(userinfo.get('id'))
        username = userinfo.get('name')
        return social_id, username, None  # Google does not provide email

    def _parse(self, s):
        d = dict(json.loads(s))

        for k, v in d.items():
            if not isinstance(k, bytes) and not isinstance(v, bytes):
                # skip this iteration if we have no keys or values to update
                continue
            d.pop(k)
            if isinstance(k, bytes):
                k = k.decode('utf-8')
            if isinstance(v, bytes):
                v = v.decode('utf-8')
            d[k] = v
        return d
