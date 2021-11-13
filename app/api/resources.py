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
from collections import Counter

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


@api_rest.route('/sensor-update')
class SensorUpdate(Resource):
    def post(self):
        api_key = request.args.get('api_key')
        sensor_type = request.args.get('type')
        sensor = dbi.get_sensor_by_api_key(api_key, sensor_type)
        sensor_value = request.args.get('value')

        dbi.add_sensor_value(sensor.id, sensor_value, datetime.utcnow())

        return '', 200


@api_rest.route('/get-settings')
class SetSettings(Resource):
    def get(self):
        print(request.args.get('api_key'))
        print(request.args.get('type'))
        print(request.args.get('value'))
        print(request.args.get('bullshit'))
        return '', 200


@api_rest.route('/verify_user/<string:username>/<string:password>')
class VerifyUser(Resource):
    def get(self, username, password):
        user = dbi.get_user(username)
        if check_password(password, user.password):
            return jsonify({'data': 'approved'})
        else:
            print('Wrong password')
            return {'data': 'invalid password'}, 400


@api_rest.route('/moist_data/<int:user_id>/<string:time_type>/<int:time_count>')
class MoistData(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, user_id, time_type, time_count):
        try:
            moist_data = []
            moist_return_data = []

            if time_type == 'hour':
                moist_data = dbi.get_moist_on_hour(user_id, time_count)

            elif time_type == 'day':
                moist_data = dbi.get_moist_on_day(user_id, time_count)
            elif time_type == 'week':
                moist_data = dbi.get_moist_on_week(user_id, time_count)
            else:
                raise Exception("Invalid time type: %s", time_type)
            for moist in moist_data:
                moist_dict = {'timestamp': moist.timestamp,
                              'value': moist.value}
                moist_return_data.append(moist_dict)
            moist_return_dict = {'data': moist_return_data}
            return jsonify(moist_return_dict)
        except Exception as e:
            print(e)


@api_rest.route('/cell_data/<int:user_id>')
class CellData(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, user_id):
        try:
            print(user_id)
            plot_id = dbi.get_plot(user_id)
            sensor1 = dbi.get_sensor(plot_id, 5)
            sensor2 = dbi.get_sensor(plot_id, 6)
            sensor3 = dbi.get_sensor(plot_id, 7)
            moist_return_data = []

            moist_dict = {'cell1': dbi.get_latest_cell_data(sensor1.id)}
            moist_return_data.append(moist_dict)

            moist_dict = {'cell2': dbi.get_latest_cell_data(sensor2.id)}
            moist_return_data.append(moist_dict)

            moist_dict = {'cell3': dbi.get_latest_cell_data(sensor3.id)}
            moist_return_data.append(moist_dict)

            moist_return_dict = {'data': moist_return_data}
            return jsonify(moist_return_dict)
        except Exception as e:
            print(e)


@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}
