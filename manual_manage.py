from app.interface import DatabaseInterface
from utils.utils import check_password, get_hashed_password
from datetime import datetime, timedelta


# DB interface
dbi = DatabaseInterface()


def add_user(name, password):
    print('adding user')
    print(dbi.add_user(name, get_hashed_password(password)))


def add_moist_data(id, value, a):
    print('adding moist')
    timestamp = datetime.utcnow()-timedelta(hours=a)+timedelta(hours=2)
    print(dbi.add_moist(id, value, timestamp))


# add_user('Admin', '321TimenBram@@')
# add_user('Tim', 'Qwerty-8-8')
# id = 1
values = [45, 35, 42, 54, 64, 42, 43, 36, 42, 35, 43, 26, 25, 32, 52, 43]

for id, value in enumerate(values):
    add_moist_data(1, value, id)
