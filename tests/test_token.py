import fakedata
import mock
import time
import sys
import unittest

from wonk import create_app
from wonk import jws


class TestToken(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')

    def test_verify_valid_token_returns_data(self):
        data = fakedata.randstr()
        with self.app.app_context():
            token = jws.generate_token(data=data)
            res = jws.verify_token(token)
        self.assertEquals(data, res)

    def test_verify_bad_token_returns_none(self):
        data = fakedata.randstr()
        with self.app.app_context():
            token = jws.generate_token(data=data)
            res = jws.verify_token(token[::-1])
        self.assertIsNone(res)

    def test_verify_expired_token_returns_none(self):
        def time_mock(*args, **kwargs):
            return sys.maxint
        data = fakedata.randstr()
        with self.app.app_context():
            token = jws.generate_token(data=data, expires_in=5)
            with mock.patch('time.time', time_mock):
                res = jws.verify_token(token)
        self.assertIsNone(res)
