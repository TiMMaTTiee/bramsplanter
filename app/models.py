from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
# from app import db

Base = declarative_base()
metadata = Base.metadata

# Super hacky, but for db migrations, uncomment the db import and change Base per class to db.Model. Also comment the model imports in the db interface


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(45))
    name = Column(String(45))
    password = Column(String(1000))


class Plots(Base):
    __tablename__ = 'plots'

    id = Column(Integer, primary_key=True)
    users_id = Column(Integer)
    name = Column(String(45))
    api_key = Column(String(255))


class Sensors(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)
    sensor_type = Column(Integer)
    plots_id = Column(Integer)
    name = Column(String(45))


class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    timestamp = Column(DateTime)
    sensors_id = Column(Integer)


class EspSettings(Base):
    __tablename__ = 'esp_settings'

    id = Column(Integer, primary_key=True)
    plots_id = Column(Integer)
    manual_trigger = Column(Integer)
    manual_amount = Column(Integer)
    manual_trigger_2 = Column(Integer)
    manual_amount_2 = Column(Integer)


'''
1=soil_moist1
2=soil_moist2
3=soil_temp1
4=soil_temp2
5=Cell1
6=Cell2
7=Cell3
8=air_moist1
9=air_temp1
10=SOLAR_bool
11=air_moist2
12=air_temp2
13=lux
14=flow_rate
15=Cell_total
'''
