from __future__ import absolute_import
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
        with app.app_context():
            token = jws.generate_token(data=fakedata.randstr())
            res = jws.verify_token(token[::-1])
        self.assertIsNone(res)

    @mock.patch('time.time')
    def test_verify_expired_token_returns_none(self, func_mock):
        with app.app_context():
            token = jws.generate_token(data=fakedata.randstr(), expires_in=5)
            # make sure token is expired
            func_mock.return_value = sys.maxint
            res = jws.verify_token(token)
        self.assertIsNone(res)

    @mock.patch('wonk.jws.verify_token')
    def test_is_valid_token_no_data_returns_false(self, func_mock):
        func_mock.return_value = None
        with app.app_context():
            self.assertFalse(jws.is_valid_token(
                token=fakedata.randstr(), for_user=fakedata.randstr()))

    @mock.patch('wonk.jws.verify_token')
    def test_is_valid_token_no_user_returns_false(self, func_mock):
        user = fakedata.randstr()
        func_mock.return_value = {'notuser': user}
        with app.app_context():
            self.assertFalse(jws.is_valid_token(
                token=fakedata.randstr(), for_user=user))

    @mock.patch('wonk.jws.verify_token')
    def test_is_valid_token_no_user_match_returns_false(self, func_mock):
        user_no_match = fakedata.randstr()
        func_mock.return_value = {'user': user_no_match}
        with app.app_context():
            self.assertFalse(jws.is_valid_token(
                token=fakedata.randstr(), for_user=fakedata.randstr()))

    @mock.patch('wonk.jws.verify_token')
    def test_is_valid_token_user_match_returns_true(self, func_mock):
        user = fakedata.randstr()
        func_mock.return_value = {'user': user}
        with app.app_context():
            self.assertTrue(jws.is_valid_token(
                token=fakedata.randstr(), for_user=user))
