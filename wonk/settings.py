import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    OAUTH_CREDENTIALS = {
        'google': {
            'id': os.getenv('OAUTH_GOOGLE_ID'),
            'secret': os.getenv('OAUTH_GOOGLE_SECRET')
        },
        'facebook': {
            'id': os.getenv('OAUTH_FACEBOOK_ID'),
            'secret': os.getenv('OAUTH_FACEBOOK_SECRET')
        },
        'twitter': {
            'id': os.getenv('OAUTH_TWITTER_ID'),
            'secret': os.getenv('OAUTH_TWITTER_SECRET')
        },
    }
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(64))


class ProductionConfig(Config):
    REDIS_URL = 'redis://localhost:6379/0'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': ProductionConfig,
}
