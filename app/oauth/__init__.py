"""Base class for OAuth service providers."""
import importlib
import os
import re

from flask import current_app
from flask import url_for


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def get_callback_url(self):
        return url_for('auth.oauth_callback', provider=self.provider_name,
                       _external=True)

    def authorize(self):
        raise NotImplementedError('Subclasses should implement this.')

    def callback(self):
        raise NotImplementedError('Subclasses should implement this.')

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


# now import all OAuth implementations
pysearchre = re.compile('.py$', re.IGNORECASE)
oauthfiles = filter(pysearchre.search, os.listdir(os.path.dirname(__file__)))
oauthmods = map(lambda f: '.' + os.path.splitext(f)[0], oauthfiles)
for mod in oauthmods:
    if not mod.startswith('__'):
        importlib.import_module(mod, package='app.oauth')
