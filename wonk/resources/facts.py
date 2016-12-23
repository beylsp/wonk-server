"""Blueprint module associated with facts REST resources."""
import flask
import flask_login as login
import flask_restful as rest

facts_bp = flask.Blueprint('facts', __name__)


class Fact(rest.Resource):
    def get(self, id):
        if login.current_user.is_anonymous:
            return {'message': 'Unauthorized'}
        return {'hello': 'world'}
