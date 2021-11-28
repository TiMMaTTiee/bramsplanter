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
            dbi.update_sensor_value(latest_sensor_data.id, sensor_values, datetime.utcnow())

        return 'Bedankt voor je data, slet', 200


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
            return {'data': e}, 400

@api_rest.route('/get_esp_settings_uuid/<string:user_uuid>')
class GetEspSettingsUuid(Resource):
    def get(self, user_uuid):
        try:
            plot = dbi.get_plot_uuid(user_uuid)

            esp_settings = dbi.get_esp_settings(plot)
            esp_return_data = {
                'manual_trigger': esp_settings.manual_trigger, 'manual_trigger_2': esp_settings.manual_trigger_2, 
                'manual_amount': esp_settings.manual_amount, 'manual_amount_2': esp_settings.manual_amount_2,
                'update_interval': esp_settings.update_interval, 'reserved_1': esp_settings.reserved_1, 'reserved_2': esp_settings.reserved_2}

            sensor_return_dict = {'data': esp_return_data}
            return jsonify(sensor_return_dict)
        except Exception as e:
            print(e)
            return {'data': e}, 400


@api_rest.route('/set_esp_settings/<string:user_uuid>/<int:manual_trigger>/<int:manual_trigger_2>/<int:manual_amount>/<int:manual_amount_2>/<int:update_interval>')
class SetEspSettingsUuid(Resource):
    def get(self, user_uuid, manual_trigger, manual_trigger_2, manual_amount, manual_amount_2, update_interval):
        try:
            plot = dbi.get_plot_uuid(user_uuid)
            print(manual_trigger)
            print(manual_trigger_2)
            settings = {
                'manual_trigger': manual_trigger, 'manual_trigger_2': manual_trigger_2, 
                'manual_amount': manual_amount, 'manual_amount_2': manual_amount_2,
                'update_interval': update_interval, 'reserved_1': 0, 'reserved_2': 0}
            result = dbi.update_esp_settings(plot, settings)
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


@api_rest.route('/recent_data/<string:user_uuid>')
class RecentData(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, user_uuid):
        try:
            plot_id = dbi.get_plot_uuid(user_uuid)
            sensor_return_data = dbi.get_latest_sensor_data(plot_id)
            
            sensor_return_dict = {'data': sensor_return_data.serialize}
            return jsonify(sensor_return_dict)
        except Exception as e:
            print(e)
            return {'data': e}, 400


@api_rest.route('/all_data/<string:user_uuid>/<string:time_type>/<int:time_count>')
class AllData(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, user_uuid, time_type, time_count):
        try:
            plot_id = dbi.get_plot_uuid(user_uuid)
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
                        cell_1.insert(0, int(entry.cell1 * 0.1875 * 0.001 * 100) / 100)
                        cell_2.insert(0, int(entry.cell2 * 0.1875 * 0.001 * 100) / 100)
                        cell_3.insert(0, int(entry.cell3 * 0.1875 * 0.001 * 100) / 100)
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


@api_rest.route('/recent_image/<string:user_uuid>')
class RecentImage(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, user_uuid):
        try:
            return_data = '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1pVu3p1S082rUbp/7UrHD9z17u5mI2fW1O+40tmm/Zba7Xe67UeF9kRWVsftyY633PTWyB630O3h61zG2GlkF17Og0bCx9nI9of8WTsu0FX3GMna+ER2Po+MP8HqtLXmhprqjmZVVrbdMKv3u9HTSzt72d3damTsDrY01ddWzex6htl2t+fWxyey9f9i119nVXbOXPeN7GULfT6PbH2dTkdVM61+NBI+nkbOar1GFvea1Z7fadD6CN/S3NwSX7W+XY/cft1s52txKqtrYi/I/OjXI/u2u53etlm186JjL43sdEv8J7VHsrk57st22nT8He6hkb1soU/XI9sv5O58irmqpkYh0Uj4+M4j215rGXupZOcXW3Z3JtnxxK+H17XWbn9Gsf2mWbG3WrS9fHX7jW2X97q+rnX1Ll7X2qfdbWtt7BWn2z+mD42MBbuluXFebU1dfVOHT9pRrfjytm+kvq6mdt72jfTeyF620MfXtbYd4/h739I0b1bstUvNK5obXJlEI6F/G9npPXs9XY/cEckOz43u1vsjYyGt6uaGPr4/si+72+HtmPUNfboe2frGy5Yd+1/X0Okja7v8TqGZtfHvZ5zXuOPUr6eTx5630OX9kTvf+tjj+yNjSa2pjD9z9hJXNBIANBIANBIANBIANBIANBIANBIA0EgA0EgA0EgA0EgA0EgA0EgA0EgA0EgA0EgA0EgA0EgAQCMBQCMBQCMBQCMBQCMBQCMBQCMBQCMBQCMBQCMBQCMBQCMBAI0EAI0EAI0EAI0EAI0EAI0EAI0EAI0EAI0EAI0EAI0EAI0EADQSADQSADQSADQSADQSADQSADQSADQSADQSADQSADQSANBIANBIANBIANBIANBIANBIANBIANBIANBIANBIANBIANBIAEAjAUAjAUAjAUAjAUAjAUAjAUAjAUAjAUAjAUAjAUAjAUAjAQCNBACNBACNBACNBACNBACNBACNBACNBACNBACNBACNBACNBAA0EgD66v8BElu3/PVnx0cAAAAASUVORK5CYII='
            return_data_dict = {'data': return_data}
            return jsonify(return_data_dict)
        except Exception as e:
            print(e)
            return {'data': e}, 400


@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}
