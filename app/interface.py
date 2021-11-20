from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, exc, MetaData
from sqlalchemy.orm import sessionmaker
import os
from functools import wraps
from datetime import datetime, timedelta

from app.models import Users, Plots, Sensors, SensorData, Base
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

    def get_sensor_by_api_key(self, _api_key, _sensor_type):
        try:
            sensor_type_id = self.get_sensor_type(_sensor_type)
            plot = self.session.query(Plots).filter_by(
                api_key=_api_key).first()
            sensor = self.session.query(Sensors).filter_by(
                plots_id=plot.id, sensor_type=sensor_type_id).first()
            return sensor
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

    def add_sensor_value(self, sensor_id, _value, _timestamp):
        try:
            new_value = SensorData(
                sensors_id=sensor_id, value=_value, timestamp=_timestamp)
            self.session.add(new_value)
            self.session.commit()
            return new_value.id
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def get_latest_cell_data(self, sensor_id):
        try:
            last_cell = self.session.query(SensorData).order_by(
                SensorData.timestamp.desc()).filter(SensorData.sensors_id == sensor_id).first()
            return last_cell.value
        except exc.SQLAlchemyError as ex:
            logging.error(ex)
            return False

    def get_moist_on_hour(self, user_id, hour):
        try:
            plot_id = self.get_plot(user_id)
            sensor = self.get_sensor(plot_id, 1)
            target_hour_max = datetime.utcnow()+timedelta(hours=2)
            target_hour_min = datetime.utcnow()+timedelta(hours=2) - timedelta(hours=hour)
            moist = self.session.query(SensorData).filter(SensorData.sensors_id == sensor.id,
                                                          SensorData.timestamp >= target_hour_min,
                                                          SensorData.timestamp <= target_hour_max).all()
            for moists in moist:
                print(moists.value)
            return moist
        except exc.SQLAlchemyError as ex:
            logging.error(ex)
            return False
