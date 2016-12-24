from flask import jsonify
from werkzeug.exceptions import HTTPException

class NotModifiedError(HTTPException):
    code = 304
    description = 'Not Modified'


class NotAuthorizedError(HTTPException):
    code = 401
    description = 'Not Authorized'
