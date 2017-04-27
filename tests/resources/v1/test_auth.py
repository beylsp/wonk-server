import base64
import json
import tests
import flask_bcrypt as bcrypt
from wonk.models.users import db
from wonk.models.users import User


class AuthenticationTest(tests.NeuralTestCase):
    def populate_db(self):
        with tests.app.app_context():
            user = User(username='john')
            user.password = bcrypt.generate_password_hash(password='doe')
            db.session.add(user)
            db.session.commit()

    def del_user_from_db(self, id):
        with tests.app.app_context():
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()

    def login(self, **kwargs):
        d = dict()
        method = kwargs.get('method', 'POST')
        d['method'] = method

        headers = kwargs.get('headers', {})
        auth = kwargs.get('auth')
        if auth:
            headers['Authorization'] = 'Basic ' + base64.b64encode('%s:%s' % auth)
        d['headers'] = headers

        return self.test_client.open('/rest/auth/v1/login/', **d)


class TestLogin(AuthenticationTest):
    def test_login_method_not_allowed(self):
        response = self.login(method='GET')
        self.assertEquals(response.status_code, 405)

    def test_login_without_header(self):
        response = self.login(method='POST')
        self.assertEquals(response.status_code, 401)

    def test_login_with_header_but_missing_credentials(self):
        headers = {'Authorization': 'Basic '}
        response = self.login(headers=headers)
        self.assertEquals(response.status_code, 401)

    def test_login_with_digest_auth_header(self):
        headers = {'Authorization': 'Digest ' + base64.b64encode('john:doe')}
        response = self.login(headers=headers)
        self.assertEquals(response.status_code, 401)

    def test_login_with_invalid_auth_header(self):
        headers = {'Authorization': 'Invalid ' + base64.b64encode('john:doe')}
        response = self.login(headers=headers)
        self.assertEquals(response.status_code, 401)

    def test_login_with_incomplete_auth_header(self):
        headers = {'Authorization': base64.b64encode('john:doe')}
        response = self.login(headers=headers)
        self.assertEquals(response.status_code, 401)

    def test_login_with_invalid_user(self):
        response = self.login(auth=('joe', 'doe'))
        self.assertEquals(response.status_code, 401)

    def test_login_with_invalid_password(self):
        response = self.login(auth=('john', 'bloggs'))
        self.assertEquals(response.status_code, 401)

    def test_login_with_invalid_user_and_no_password(self):
        response = self.login(auth=('joe', ''))
        self.assertEquals(response.status_code, 401)

    def test_login_with_valid_user_and_no_password(self):
        response = self.login(auth=('john', ''))
        self.assertEquals(response.status_code, 401)

    def test_login_with_no_user_and_invalid_password(self):
        response = self.login(auth=('', 'bloggs'))
        self.assertEquals(response.status_code, 401)

    def test_login_with_no_user_and_valid_password(self):
        response = self.login(auth=('', 'doe'))
        self.assertEquals(response.status_code, 401)

    def test_login_with_no_user_and_no_password(self):
        response = self.login(auth=('', ''))
        self.assertEquals(response.status_code, 401)

    def test_login_with_credentials(self):
        response = self.login(auth=('john', 'doe'))
        self.assertEquals(response.status_code, 200)
        self.assertIn('access_token', json.loads(response.data))

    def test_login_with_user_removed(self):
        self.del_user_from_db(id=1)
        response = self.login(auth=('john', 'doe'))
        self.assertEquals(response.status_code, 401)


class TestLogout(AuthenticationTest):
    ENDPOINT = '/rest/auth/v1/logout/'
