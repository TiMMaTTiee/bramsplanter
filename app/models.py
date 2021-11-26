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
    soil_moist1 = Column(Integer)
    soil_moist2 = Column(Integer)
    soil_temp1 = Column(Integer)
    soil_temp2 = Column(Integer)
    cell1 = Column(Integer)
    cell2 = Column(Integer)
    cell3 = Column(Integer)
    air_moist1 = Column(Integer)
    air_temp1 = Column(Integer)
    solar_bool = Column(Integer)
    air_moist2 = Column(Integer)
    air_temp2 = Column(Integer)
    lux = Column(Integer)
    flow_rate = Column(Integer)
    timestamp = Column(DateTime)
    plots_id = Column(Integer)

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'timestamp': self.timestamp,
           'soil_moist1': self.soil_moist1,
           'soil_moist2': self.soil_moist2,
           'soil_temp1': self.soil_temp1,
           'soil_temp2': self.soil_temp2,
           'cell1': self.cell1,
           'cell2': self.cell2,
           'cell3': self.cell3,
           'air_moist1': self.air_moist1,
           'air_temp1': self.air_temp1,
           'solar_bool': self.solar_bool,
           'air_moist2': self.air_moist2,
           'air_temp2': self.air_temp2,
           'lux': self.lux,
           'flow_rate': self.flow_rate
       }


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
5=cell1
6=cell2
7=cell3
8=air_moist1
9=air_temp1
10=solar_bool
11=air_moist2
12=air_temp2
13=lux
14=flow_rate
'''
