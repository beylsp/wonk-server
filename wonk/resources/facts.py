"""Blueprint module associated with facts REST resources."""
import flask
import flask_login as login
import flask_restful as rest

facts_bp = flask.Blueprint('facts', __name__)


class Fact(rest.Resource):
    def get(self, id):
        access_token = flask.session.get('access_token')
        if access_token is None:
            return{'message': 'Not authorized'}
        return {'hello': 'world'}
