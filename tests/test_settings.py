import os
import unittest
from flask import current_app
from wonk import settings
from tests import app


class TestProductionConfig(unittest.TestCase):
    def setUp(self):
        app.config.from_object(settings.config['production'])

    def test_app_config_is_not_debug(self):
        self.assertFalse(app.config['DEBUG'])

    def test_app_config_is_not_testing(self):
        self.assertFalse(app.config['TESTING'])

    def test_app_config_is_not_tracking_sqlalchemy_modifications(self):
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])

    def test_current_app(self):
        self.assertFalse(current_app is None)


class TestDevelopmentConfig(unittest.TestCase):
    def setUp(self):
        app.config.from_object(settings.config['development'])

    def test_app_config_is_debug(self):
        self.assertTrue(app.config['DEBUG'])

    def test_app_config_is_not_testing(self):
        self.assertFalse(app.config['TESTING'])

    def test_app_config_is_not_tracking_sqlalchemy_modifications(self):
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])

    def test_app_config_database_uri(self):
        db_uri = 'sqlite:///%s' % (os.path.join(settings.basedir, '.neural.db'))
        self.assertEquals(app.config['SQLALCHEMY_DATABASE_URI'], db_uri)

    def test_current_app(self):
        self.assertFalse(current_app is None)


class TestTestingConfig(unittest.TestCase):
    def setUp(self):
        app.config.from_object(settings.config['testing'])

    def test_app_config_is_not_debug(self):
        self.assertFalse(app.config['DEBUG'])

    def test_app_config_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    def test_app_config_is_not_tracking_sqlalchemy_modifications(self):
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])

    def test_app_config_database_uri(self):
        db_uri = 'sqlite:///%s' % (os.path.join(settings.basedir, '.neural_test.db'))
        self.assertEquals(app.config['SQLALCHEMY_DATABASE_URI'], db_uri)

    def test_current_app(self):
        self.assertFalse(current_app is None)


class TestDefaultConfig(unittest.TestCase):
    def setUp(self):
        app.config.from_object(settings.config['default'])

    def test_app_config_is_debug(self):
        self.assertTrue(app.config['DEBUG'])

    def test_app_config_is_not_testing(self):
        self.assertFalse(app.config['TESTING'])

    def test_app_config_is_not_tracking_sqlalchemy_modifications(self):
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])

    def test_app_config_database_uri(self):
        db_uri = 'sqlite:///%s' % (os.path.join(settings.basedir, '.neural.db'))
        self.assertEquals(app.config['SQLALCHEMY_DATABASE_URI'], db_uri)

    def test_current_app(self):
        self.assertFalse(current_app is None)
