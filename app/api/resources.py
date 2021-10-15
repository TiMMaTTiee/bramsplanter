"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import jsonify, request, abort
from flask_restx import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from utils.utils import check_password, get_hashed_password

from app.interface import DatabaseInterface
from . import api_rest

# DB interface
dbi = DatabaseInterface()

# auth
auth = HTTPBasicAuth()

def require_auth(func):
    """ Secure method decorator """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verify if User is Authenticated
        # Authentication logic goes here
        user = dbi.get_user(kwargs["username"])
        if check_password(kwargs["password"], user.password):
            return func(*args, **kwargs)
        else:
            return abort(401)
    return wrapper

class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]

@api_rest.route('/verify_user/<string:username>/<string:password>')
class VerifyUser(Resource):
    def get(self, username, password):
        user = dbi.get_user(username)
        if check_password(password, user.password):
            return jsonify({'data':'approved'})
        else:
            print('Wrong password')
            return {'data': 'invalid password'}, 400

@api_rest.route('/resource/<string:resource_id>')
class ResourceOne(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}

    def post(self, resource_id):
        json_payload = request.json
        return {'timestamp': json_payload}, 201


@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}
