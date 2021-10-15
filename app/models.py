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
    user_id = Column(ForeignKey('users.id'), index=True)
    name = Column(String(45))
    user = relationship('Users')
    