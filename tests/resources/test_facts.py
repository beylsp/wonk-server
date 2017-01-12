import json
import mock
import time
import sys
import unittest

from .. import app
from .. import fakedata
from flask import jsonify
from flask_testing import TestCase
from werkzeug.exceptions import BadRequest
from wonk import jws


class TestFacts(TestCase):
    def create_app(self):
        return app

    def test_get_fact_raises_400_if_no_headers(self):
        response = self.client.get('/r/%d/' % fakedata.randint(), headers={})
        self.assertEquals(response.status_code, 400)

    @mock.patch('wonk.jws.is_valid_token')
    def test_get_fact_raises_401_if_invalid_token(self, func_mock):
        func_mock.return_value = False
        response = self.client.get('/r/%d/' % fakedata.randint(),
            headers={'Authentication-Token': fakedata.randstr(),
                     'User-Id': fakedata.randstr()}
        )
        self.assertEquals(response.status_code, 401)

    @mock.patch('wonk.jws.is_valid_token')
    def test_get_fact(self, func_mock):
        func_mock.return_value = True
        # mock redis db values
        v = fakedata.randstr()
        db = self.app.extensions['redis']
        db.redis['mykey'] = v

        response = self.client.get('/r/%d/' % fakedata.randint(),
            headers={'Authentication-Token': fakedata.randstr(),
                     'User-Id': fakedata.randstr()}
        )
        data = json.loads(response.get_data())
        self.assertEquals(data['key'], v)

    @mock.patch('wonk.jws.is_valid_token')
    def test_get_fact_list_raises_304_if_missing_if_modified_since_header(self, func_mock):
        func_mock.return_value = True
        response = self.client.get('/r/',
            headers={'Authentication-Token': fakedata.randstr(),
                     'User-Id': fakedata.randstr()}
        )
        self.assertEquals(response.status_code, 304)

    @mock.patch('wonk.jws.is_valid_token')
    def test_get_fact_list(self, func_mock):
        func_mock.return_value = True
        response = self.client.get('/r/',
            headers={'Authentication-Token': fakedata.randstr(),
                     'User-Id': fakedata.randstr(),
                     'If-Modified-Since': 'Thu, 12 Jan 2017 20:00:00 GMT'}
        )
        data = json.loads(response.get_data())
        self.assertEquals(data['hello'], 'list')

