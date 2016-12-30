"""Blueprint module associated with facts REST resources."""
from flask import Blueprint
from flask import jsonify
from flask import request
from flask_restful import Resource
from wonk.db import db
from wonk import decorators
from wonk import err

facts_bp = Blueprint('facts', __name__)


class FactResource(Resource):
    method_decorators = [decorators.token_required]


class Fact(FactResource):
    def get(self, id):
        return jsonify({'key': db.get('mykey')})


class FactList(FactResource):
    def get(self):
        modified = request.headers.get('If-Modified-Since')
        if not modified:
            raise err.NotModifiedError
        return jsonify({'hello': 'list'})
