from __future__ import absolute_import
import fakedata
import mock

from . import app
from flask_testing import TestCase
from werkzeug.exceptions import BadRequest
from werkzeug.datastructures import Headers
from wonk import decorators
from wonk import err


class TestDecorators(TestCase):
    def create_app(self):
        return app

    def test_parse_req_args_raises_bad_request_if_missing_headers(self):
        with app.test_request_context():
            self.assertRaises(BadRequest, decorators._parse_req_args)

    def test_parse_req_args_raises_bad_request_if_missing_user_id(self):
        hdr = Headers()
        hdr.add('Authentication-Token', fakedata.randstr())
        with app.test_request_context(headers=hdr):
            self.assertRaises(BadRequest, decorators._parse_req_args)

    def test_parse_req_args_raises_bad_request_if_missing_auth_token(self):
        hdr = Headers()
        hdr.add('User-Id', fakedata.randstr())
        with app.test_request_context(headers=hdr):
            self.assertRaises(BadRequest, decorators._parse_req_args)

    def test_parse_req_args_does_not_raise_bad_request_if_too_many_headers(self):
        hdr = Headers()
        hdr.add('Authentication-Token', fakedata.randstr())
        hdr.add('User-Id', fakedata.randstr())
        hdr.add('Foo', fakedata.randstr())
        with app.test_request_context(headers=hdr):
            try:
                decorators._parse_req_args()
            except BadRequest:
                self.fail('_parse_req_args() raised unexpected BadRequest')

    def test_parse_req_args_returns_user(self):
        user = fakedata.randstr()
        hdr = Headers()
        hdr.add('Authentication-Token', fakedata.randstr())
        hdr.add('User-Id', user)
        with app.test_request_context(headers=hdr):
            d = decorators._parse_req_args()
            self.assertEquals(d.user, user)

    def test_parse_req_args_returns_user(self):
        token = fakedata.randstr()
        hdr = Headers()
        hdr.add('Authentication-Token', token)
        hdr.add('User-Id', fakedata.randstr())
        with app.test_request_context(headers=hdr):
            d = decorators._parse_req_args()
            self.assertEquals(d.token, token)

    @mock.patch('wonk.jws.is_valid_token')
    def test_raise_if_invalid_token(self, func_mock):
        func_mock.return_value = False
        with app.app_context():
            self.assertRaises(err.NotAuthorizedError, 
                decorators._raise_if_invalid_token, fakedata.randstr(),
                fakedata.randstr())

    @mock.patch('wonk.jws.is_valid_token')
    def test_not_raise_if_invalid_token(self, func_mock):
        func_mock.return_value = True
        with app.app_context():
            try:
                decorators._raise_if_invalid_token(
                    fakedata.randstr(), fakedata.randstr())
            except err.NotAuthorizedError:
                self.fail('_raise_if_invalid_token() raised unexpected NotAuthorizedError')
