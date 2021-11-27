from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, exc, MetaData
from sqlalchemy.orm import sessionmaker
import os
from functools import wraps
from datetime import datetime, timedelta

from app.models import Users, Plots, Sensors, SensorData, EspSettings, Base
from datetime import datetime
import logging
import uuid
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()  # take environment variables from .env.


class DatabaseInterface():
    def __init__(self, initialize_database=False, test_db=False):
        self.test_db = test_db
        if test_db:
            self.engine = create_engine('sqlite:///:memory:', echo=True)
        else:
            logger.info('Connecting to database at %s',
                        os.environ.get("DATABASE_URL"))
            print('Connecting to database at %s',
                  os.environ.get("DATABASE_URL"))
            self.engine = create_engine(os.environ.get(
                "DATABASE_URL"), echo=False, isolation_level='READ COMMITTED')
        if initialize_database:
            Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_user(self, _name, _password):
        try:
            new_user = Users(uuid=uuid.uuid4(), name=_name, password=_password)
            self.session.add(new_user)
            self.session.commit()
            return new_user.id
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def get_user(self, _name):
        try:
            user = self.session.query(Users).filter_by(name=_name).first()
            return user
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def get_user_uuid(self, _uuid):
        try:
            user = self.session.query(Users).filter_by(uuid=_uuid).first()
            return user
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def get_plot(self, _user_id):
        try:
            plot = self.session.query(Plots).filter_by(
                users_id=_user_id).first()
            return plot.id
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def get_plot_uuid(self, _user_uuid):
        try:
            _user_id = self.get_user_uuid(_user_uuid).id
            plot = self.session.query(Plots).filter_by(
                users_id=_user_id).first()
            return plot.id
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            print(ex)
            return False

    def get_sensor(self, _plot_id, _type):
        try:
            sensor = self.session.query(Sensors).filter_by(
                sensor_type=_type).first()
            return sensor.id
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def get_sensor_plot(self, _plot_id):
        try:
            sensors = self.session.query(Sensors).filter_by(
                plots_id=_plot_id).all()
            return sensors
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def get_plot_by_api_key(self, _api_key):
        try:
            plot = self.session.query(Plots).filter_by(
                api_key=_api_key).first()
            return plot
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def get_sensor_type(self, x):
        return {
            'soil_moist1': 1,
            'soil_moist2': 2,
            'soil_temp1': 3,
            'soil_temp2': 4,
            'Cell1': 5,
            'Cell2': 6,
            'Cell3': 7,
            'air_moist1': 8,
            'air_temp1': 9,
            'SOLAR_bool': 10,
            'air_moist2': 11,
            'air_temp2': 12,
            'lux': 13,
            'flow_rate': 14
        }.get(x, 0)

    def add_sensor_value(self, plot_id, values, _timestamp):
        try:
            new_value = SensorData(
                plots_id=plot_id, 
                soil_moist1=values['soil_moist1'],
                soil_moist2=values['soil_moist2'],
                soil_temp1=values['soil_temp1'],
                soil_temp2=values['soil_temp2'],
                cell1=values['cell1'],
                cell2=values['cell2'],
                cell3=values['cell3'],
                air_moist1=values['air_moist1'],
                air_temp1=values['air_temp1'],
                solar_bool=values['solar_bool'],
                air_moist2=values['air_moist2'],
                air_temp2=values['air_temp2'],
                lux=values['lux'],
                flow_rate=values['flow_rate'],
                timestamp=_timestamp,
                latest_update=_timestamp)
            self.session.add(new_value)
            self.session.commit()
            return new_value.id
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def update_sensor_value(self, data_id, values, _timestamp):
        try:
            last_entry = self.session.query(SensorData).order_by(
                SensorData.timestamp.desc()).filter(SensorData.id == data_id).first()
            last_entry.soil_moist1=values['soil_moist1']
            last_entry.soil_moist2=values['soil_moist2']
            last_entry.soil_temp1=values['soil_temp1']
            last_entry.soil_temp2=values['soil_temp2']
            last_entry.cell1=values['cell1']
            last_entry.cell2=values['cell2']
            last_entry.cell3=values['cell3']
            last_entry.air_moist1=values['air_moist1']
            last_entry.air_temp1=values['air_temp1']
            last_entry.solar_bool=values['solar_bool']
            last_entry.air_moist2=values['air_moist2']
            last_entry.air_temp2=values['air_temp2']
            last_entry.lux=values['lux']
            last_entry.flow_rate=values['flow_rate']
            last_entry.latest_update = _timestamp
            self.session.commit()
            return last_entry.id
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def get_latest_sensor_data(self, plot_id):
        try:
            last_entry = self.session.query(SensorData).order_by(
                SensorData.timestamp.desc()).filter(SensorData.plots_id == plot_id).first()
            return last_entry
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logging.error(ex)
            return False

    def get_all_sensor_data(self, plot_id):
        try:
            all_entries = self.session.query(SensorData).order_by(
                SensorData.timestamp.desc()).filter(SensorData.plots_id == plot_id).all()
            return all_entries
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logging.error(ex)
            return False
    
    def get_esp_settings(self, plot_id):
        try:
            settings = self.session.query(EspSettings).filter(EspSettings.plots_id == plot_id).first()
            return settings
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logging.error(ex)
            return False
    
    def update_esp_settings(self, plot_id, values):
        try:
            settings = self.session.query(EspSettings).filter(EspSettings.plots_id == plot_id).first()
            settings.manual_trigger = values['manual_trigger']
            settings.manual_trigger_2 = values['manual_trigger_2']
            settings.manual_amount = values['manual_trigger_2']
            settings.manual_amount_2 = values['manual_trigger_2']
            settings.update_interval = values['manual_trigger_2']
            settings.reserved_1 = values['reserved_1']
            settings.reserved_2 = values['reserved_2']
            self.session.commit()
            return settings.id
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logging.error(ex)
            return False

    def reset_esp_settings(self, plot_id):
        try:
            settings = self.session.query(EspSettings).filter(EspSettings.plots_id == plot_id).first()
            settings.manual_trigger = 0
            settings.manual_trigger_2 = 0
            self.session.commit()
            return settings.id
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logging.error(ex)
            return False
