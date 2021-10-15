from app.interface import DatabaseInterface
from utils.utils import check_password, get_hashed_password

# DB interface
dbi = DatabaseInterface()

def add_user(name, password):
    print('adding user')
    print(dbi.add_user(name, get_hashed_password(password)))

add_user('Tim', 'Qwerty-8-8')