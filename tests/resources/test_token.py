from __future__ import absolute_import
import json
import mock
import time
import sys
import unittest

from .. import app
from .. import fakedata
from flask import jsonify
from flask.testing import FlaskClient
from flask_testing import TestCase
from werkzeug.exceptions import BadRequest
from wonk import jws


class TestToken(TestCase):
    def create_app(self):
        return app

    def test_get_token_raises_400_if_missing_headers(self):
        response = self.client.get('/token/', headers={})
        self.assertEquals(response.status_code, 400)

    def test_get_token_raises_400_if_missing_access_token(self):
        response = self.client.get('/token/',
            headers={'User-Id': fakedata.randstr(),
                     'Token-Provider': fakedata.randstr()}
        )
        self.assertEquals(response.status_code, 400)

    def test_get_token_raises_400_if_missing_user_id(self):
        response = self.client.get('/token/',
            headers={'Access-Token': fakedata.randstr(),
                     'Token-Provider': fakedata.randstr()}
        )
        self.assertEquals(response.status_code, 400)

    def test_get_token_raises_400_if_missing_token_provider(self):
        response = self.client.get('/token/',
            headers={'Access-Token': fakedata.randstr(),
                     'User-Id': fakedata.randstr()}
        )
        self.assertEquals(response.status_code, 400)

    @mock.patch('wonk.oauth.OAuthSignIn.authorized')
    def test_get_token_raises_401_if_invalid_headers(self, authorize_mock):
        authorize_mock.return_value = False
        response = self.client.get('/token/',
            headers={'Access-Token': fakedata.randstr(),
                     'User-Id': fakedata.randstr(),
                     'Token-Provider': fakedata.randstr()}
        )
        self.assertEquals(response.status_code, 401)

    @mock.patch('wonk.jws.generate_token')
    @mock.patch('wonk.oauth.OAuthSignIn.authorized')
    def test_get_token_raises_401_if_no_token_generated(self, authorize_mock, generate_token_mock):
        authorize_mock.return_value = True
        generate_token_mock.return_value = False
        response = self.client.get('/token/',
            headers={'Access-Token': fakedata.randstr(),
                     'User-Id': fakedata.randstr(),
                     'Token-Provider': fakedata.randstr()}
        )
        self.assertEquals(response.status_code, 401)

    @mock.patch('wonk.jws.generate_token')
    @mock.patch('wonk.oauth.OAuthSignIn.authorized')
    def test_get_token_returns_auth_token(self, authorize_mock, generate_token_mock):
        token = fakedata.randstr()
        authorize_mock.return_value = True
        generate_token_mock.return_value = token
        response = self.client.get('/token/',
            headers={'Access-Token': fakedata.randstr(),
                     'User-Id': fakedata.randstr(),
                     'Token-Provider': fakedata.randprovider()}
        )
        data = json.loads(response.get_data())
        self.assertEquals(data['token'], token)
