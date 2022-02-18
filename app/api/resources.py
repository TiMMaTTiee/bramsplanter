"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime, timedelta
from flask import jsonify, request, abort
from flask_restx import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from utils.utils import check_password, get_hashed_password
from collections import Counter
from werkzeug.datastructures import ImmutableMultiDict

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
        try:
            api_key = request.args.get('api_key')
            plot = dbi.get_plot_by_api_key(api_key)
            sensor_values = {
                'soil_moist1': request.args.get('soil_moist1'),
                'soil_moist2': request.args.get('soil_moist2'),
                'soil_temp1': request.args.get('soil_temp1'),
                'soil_temp2': request.args.get('soil_temp2'),
                'cell1': request.args.get('cell1'),
                'cell2': request.args.get('cell2'),
                'cell3': request.args.get('cell3'),
                'air_moist1': request.args.get('air_moist1'),
                'air_temp1': request.args.get('air_temp1'),
                'solar_bool': request.args.get('solar_bool'),
                'air_moist2': request.args.get('air_moist2'),
                'air_temp2': request.args.get('air_temp2'),
                'lux': request.args.get('lux'),
                'flow_rate': request.args.get('flow_rate')
            }

            latest_sensor_data = dbi.get_latest_sensor_data(plot.id)

            if (datetime.utcnow() - timedelta(hours=1)) > latest_sensor_data.timestamp:
                dbi.add_sensor_value(plot.id, sensor_values, datetime.utcnow())
            else:
                dbi.update_sensor_value(
                    latest_sensor_data.id, sensor_values, datetime.utcnow())

            # Check if it has been more than a day since latest water
            if (datetime.utcnow() - timedelta(hours=12)) > plot.latest_water:
                # Check if soil moist is below limit
                esp_settings = dbi.get_esp_settings(plot.id)
                if int(sensor_values['soil_moist1']) < esp_settings.reserved_1:
                    # Trigger pump 1 on next data request
                    dbi.trigger_pump_1(plot.id)
                if int(sensor_values['soil_moist2']) < esp_settings.reserved_2:
                    # Trigger pump 2 on next data request
                    dbi.trigger_pump_2(plot.id)
                dbi.update_latest_water(plot.id, datetime.utcnow())

            return 'Bedankt voor je data, slet', 200
        except Exception as e:
            print(e)
            return {'Error: ': e}, 400


@api_rest.route('/get-esp-settings')
class GetEspSettings(Resource):
    def get(self):
        try:
            api_key = request.args.get('api_key')
            plot = dbi.get_plot_by_api_key(api_key)

            esp_settings = dbi.get_esp_settings(plot.id)
            esp_return_data = {
                'manual_trigger': esp_settings.manual_trigger, 'manual_trigger_2': esp_settings.manual_trigger_2,
                'manual_amount': esp_settings.manual_amount, 'manual_amount_2': esp_settings.manual_amount_2,
                'update_interval': esp_settings.update_interval, 'reserved_1': esp_settings.reserved_1, 'reserved_2': esp_settings.reserved_2}

            sensor_return_dict = {'data': esp_return_data}
            dbi.reset_esp_settings(plot.id)
            return jsonify(sensor_return_dict)
        except Exception as e:
            print(e)
            return {'Error: ': e}, 400


@api_rest.route('/get_esp_settings_uuid/<string:api_key>')
class GetEspSettingsUuid(Resource):
    def get(self, api_key):
        try:
            plot = dbi.get_plot_by_api_key(api_key)

            esp_settings = dbi.get_esp_settings(plot.id)
            esp_return_data = {
                'manual_trigger': esp_settings.manual_trigger, 'manual_trigger_2': esp_settings.manual_trigger_2,
                'manual_amount': esp_settings.manual_amount, 'manual_amount_2': esp_settings.manual_amount_2,
                'update_interval': esp_settings.update_interval, 'limit_1': esp_settings.reserved_1, 'limit_2': esp_settings.reserved_2}

            sensor_return_dict = {'data': esp_return_data}
            return jsonify(sensor_return_dict)
        except Exception as e:
            print(e)
            return {'data': e}, 400


@api_rest.route('/set_esp_settings/<string:api_key>/<int:manual_trigger>/<int:manual_trigger_2>/<int:manual_amount>/<int:manual_amount_2>/<int:update_interval>/<int:limit_1>/<int:limit_2>')
class SetEspSettingsUuid(Resource):
    def get(self, api_key, manual_trigger, manual_trigger_2, manual_amount, manual_amount_2, update_interval, limit_1, limit_2):
        try:
            plot = dbi.get_plot_by_api_key(api_key)
            settings = {
                'manual_trigger': manual_trigger, 'manual_trigger_2': manual_trigger_2,
                'manual_amount': manual_amount, 'manual_amount_2': manual_amount_2,
                'update_interval': update_interval, 'reserved_1': limit_1, 'reserved_2': limit_2}
            result = dbi.update_esp_settings(plot.id, settings)
            return_dict = {'data': result}
            return jsonify(return_dict)
        except Exception as e:
            print(e)
            return {'data': e}, 400


@api_rest.route('/verify_user/<string:username>/<string:password>')
class VerifyUser(Resource):
    def get(self, username, password):
        user = dbi.get_user(username)
        if check_password(password, user.password):
            return jsonify({'data': 'approved', 'uuid': user.uuid})
        else:
            print('Wrong password')
            return {'data': 'invalid password'}, 400


@api_rest.route('/recent_data/<string:api_key>')
class RecentData(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, api_key):
        try:
            plot_id = dbi.get_plot_by_api_key(api_key).id
            sensor_return_data = dbi.get_latest_sensor_data(plot_id)

            sensor_return_dict = {'data': sensor_return_data.serialize}
            return jsonify(sensor_return_dict)
        except Exception as e:
            print(e)
            return {'data': e}, 400


@api_rest.route('/all_data/<string:api_key>/<string:time_type>/<int:time_count>')
class AllData(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, api_key, time_type, time_count):
        try:
            plot_id = dbi.get_plot_by_api_key(api_key).id
            sensor_return_data = dbi.get_all_sensor_data(plot_id)

            air_moist_1 = []
            soil_moist_1 = []
            soil_moist_2 = []

            air_temp_1 = []
            soil_temp_1 = []

            cell_1 = []
            cell_2 = []
            cell_3 = []

            last_hour_value = datetime.today()

            if time_type == 'hour':
                delta_t = timedelta(hours=1)
            if time_type == 'day':
                delta_t = timedelta(days=1)
            if time_type == 'week':
                delta_t = timedelta(weeks=1)

            for i in range(time_count):
                entry_found = False
                for entry in sensor_return_data:
                    if (last_hour_value - delta_t) < entry.timestamp < last_hour_value:
                        air_temp_1.insert(0, entry.air_temp1)
                        soil_temp_1.insert(0, entry.soil_temp1)
                        air_moist_1.insert(0, entry.air_moist1)
                        soil_moist_1.insert(0, entry.soil_moist1)
                        soil_moist_2.insert(0, entry.soil_moist2)
                        cell_1.insert(
                            0, int(entry.cell1 * 0.1875 * 0.001 * 100) / 100)
                        cell_2.insert(
                            0, int(entry.cell2 * 0.1875 * 0.001 * 100) / 100)
                        cell_3.insert(
                            0, int(entry.cell3 * 0.1875 * 0.001 * 100) / 100)
                        last_hour_value = last_hour_value - delta_t
                        entry_found = True
                        break
                if not entry_found:
                    air_temp_1.insert(0, 0)
                    soil_temp_1.insert(0, 0)
                    air_moist_1.insert(0, 0)
                    soil_moist_1.insert(0, 0)
                    soil_moist_2.insert(0, 0)
                    cell_1.insert(0, 0)
                    cell_2.insert(0, 0)
                    cell_3.insert(0, 0)
                    last_hour_value = last_hour_value - delta_t

            sensor_return_dict = {
                'temp_data':
                    [
                        {'name': 'Air temperature 1', 'data': air_temp_1},
                        {'name': 'Soil temperature 1', 'data': soil_temp_1}
                    ],
                'perc_data':
                    [
                        {'name': 'Air moisture 1', 'data': air_moist_1},
                        {'name': 'Soil moisture 1', 'data': soil_moist_1},
                        {'name': 'Soil moisture 2', 'data': soil_moist_2},
                    ],
                'cell_data':
                    [
                        {'name': 'Cell 1', 'data': cell_1},
                        {'name': 'Cell 2', 'data': cell_2},
                        {'name': 'Cell 3', 'data': cell_3}
                    ]
            }
            return jsonify(sensor_return_dict)
        except Exception as e:
            print(e)
            return {'data': e}, 400


@api_rest.route('/recent_image/<string:api_key>')
class RecentImage(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, api_key):
        try:
            return_data = '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'
            return_data_dict = {'data': return_data}
            return jsonify(return_data_dict)
        except Exception as e:
            print(e)
            return {'data': e}, 400


@api_rest.route('/post_image')
class PostImage(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def post(self):
        try:
            data = request.args.get('image')
            print(data)
            return_data = 'ok'
            return_data_dict = {'data': return_data}
            return jsonify(return_data_dict)
        except Exception as e:
            print(e)
            return {'data': e}, 400


@api_rest.route('/plots_for_uuid/<string:user_uuid>')
class PlotsForUUID(Resource):
    def get(self, user_uuid):
        try:
            if (user_uuid == 'cc72d57b-a9d3-4c75-bd7f-61a92e950f89'):
                plots = dbi.get_all_plots()
            else:
                plots = dbi.get_plot_uuid(user_uuid)

            plots_data = []
            for plot in plots:
                plot_dict = {'id': plot.id, 'name': plot.name,
                             'api_key': plot.api_key}
                plots_data.append(plot_dict)

            plots_dict = {'data': plots_data}
            return jsonify(plots_dict)

        except Exception as e:
            print(e)
            return {'data': e}, 400


@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}
