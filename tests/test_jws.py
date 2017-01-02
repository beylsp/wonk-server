import fakedata
import mock
import time
import sys
import unittest

from . import app
from flask_testing import TestCase
from wonk import jws


class TestJWS(TestCase):
    def create_app(self):
        return app

    def test_verify_valid_token_returns_data(self):
        data = fakedata.randstr()
        with app.app_context():
            token = jws.generate_token(data=data)
            res = jws.verify_token(token)
        self.assertEquals(data, res)

    def test_verify_bad_token_returns_none(self):
        data = fakedata.randstr()
        with app.app_context():
            token = jws.generate_token(data=data)
            res = jws.verify_token(token[::-1])
        self.assertIsNone(res)

    def test_verify_expired_token_returns_none(self):
        def time_mock(*args, **kwargs):
            return sys.maxint
        data = fakedata.randstr()
        with app.app_context():
            token = jws.generate_token(data=data, expires_in=5)
            with mock.patch('time.time', time_mock):
                res = jws.verify_token(token)
        self.assertIsNone(res)

    def test_is_valid_token_no_data_returns_false(self):
        token = fakedata.randstr()
        user = fakedata.randstr()
        def verify_token_mock(*args, **kwargs):
            return None
        with app.app_context():
            with mock.patch('wonk.jws.verify_token', verify_token_mock):
                self.assertFalse(jws.is_valid_token(token, user))

    def test_is_valid_token_no_user_returns_false(self):
        token = fakedata.randstr()
        user = fakedata.randstr()
        def verify_token_mock(*args, **kwargs):
            return {'notuser': user}
        with app.app_context():
            with mock.patch('wonk.jws.verify_token', verify_token_mock):
                self.assertFalse(jws.is_valid_token(token, user))

    def test_is_valid_token_no_user_match_returns_false(self):
        token = fakedata.randstr()
        user = fakedata.randstr()
        user_no_match = fakedata.randstr()
        def verify_token_mock(*args, **kwargs):
            return {'user': user_no_match}
        with app.app_context():
            with mock.patch('wonk.jws.verify_token', verify_token_mock):
                self.assertFalse(jws.is_valid_token(token, user))

    def test_is_valid_token_user_match_returns_true(self):
        token = fakedata.randstr()
        user = fakedata.randstr()
        def verify_token_mock(*args, **kwargs):
            return {'user': user}
        with app.app_context():
            with mock.patch('wonk.jws.verify_token', verify_token_mock):
                self.assertTrue(jws.is_valid_token(token, user))
