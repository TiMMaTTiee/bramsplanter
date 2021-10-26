from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, exc, MetaData
from sqlalchemy.orm import sessionmaker
import os
from functools import wraps

from app.models import Users, Plots, Sensors, SensorData, Base
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


class DatabaseInterface():
    def __init__(self, initialize_database=False, test_db=False):
        self.test_db = test_db
        if test_db:
            self.engine = create_engine('sqlite:///:memory:', echo=True)
        else:
            logger.info('Connecting to database at %s', os.environ.get("DATABASE_URL"))
            print('Connecting to database at %s', os.environ.get("DATABASE_URL"))
            self.engine = create_engine(os.environ.get("DATABASE_URL"), echo=False, isolation_level='READ COMMITTED')
        if initialize_database:
            Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_user(self, _name, _password):
        try:
            new_user = Users(uuid=uuid.uuid4(), name = _name, password = _password)
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