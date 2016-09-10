import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False

    OAUTH_CREDENTIALS = {
        'google': {
            'id': '12345',
            'secret': 'abcdef'
        },
        'facebook': {
            'id': '23456',
            'secret': 'bcdefg'
        },
        'twitter': {
            'id': '34567',
            'secret': 'cdefgh'
        },

    }


class ProductionConfig(Config):
    pass


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
