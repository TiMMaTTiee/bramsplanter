""" Security Related things """
from functools import wraps
from flask import request
from flask_restx import abort


def require_auth(func):
    """ Secure method decorator """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verify if User is Authenticated
        # Authentication logic goes here
        print('Add auth logix')
        print(request)
        if request.headers.get('auth'):
            return func(*args, **kwargs)
        else:
            return abort(401)
    return wrapper
