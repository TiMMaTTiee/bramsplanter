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

    def get_plot(self, _user_id):
        try:
            plot = self.session.query(Plots).filter_by(
                users_id=_user_id).first()
            return plot
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def get_sensor(self, _plot_id, _type):
        try:
            sensor = self.session.query(Sensors).filter_by(
                plots_id=_plot_id, sensor_type=_type).first()
            return sensor
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def add_moist(self, id, _value, _timestamp):
        try:
            new_moist = SensorData(
                sensors_id=id, value=_value, timestamp=_timestamp)
            self.session.add(new_moist)
            self.session.commit()
            return new_moist.id
        except exc.SQLAlchemyError as ex:
            self.session.rollback()
            logger.error(ex)
            return False

    def get_moist_on_hour(self, user_id, hour):
        try:
            plot = self.get_plot(user_id)
            sensor = self.get_sensor(plot.id, 1)
            target_hour_max = datetime.utcnow()+timedelta(hours=2)
            target_hour_min = datetime.utcnow()+timedelta(hours=2) - timedelta(hours=hour)
            moist = self.session.query(SensorData).filter(SensorData.sensors_id == sensor.id,
                                                          SensorData.timestamp >= target_hour_min,
                                                          SensorData.timestamp <= target_hour_max).all()
            for moists in moist:
                print(moists.timestamp)
                print(moists.value)
            return moist
        except exc.SQLAlchemyError as ex:
            logging.error(ex)
            return False
