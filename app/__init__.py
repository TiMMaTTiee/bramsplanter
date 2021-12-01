import os
from flask import Flask, current_app, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from dotenv import load_dotenv

from .api import api_bp
from .client import client_bp

load_dotenv()  # take environment variables from .env.

app = Flask(__name__, static_folder='../dist/static')
app.register_blueprint(api_bp)
# app.register_blueprint(client_bp)

from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))
uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
Config.SQLALCHEMY_DATABASE_URI=uri
db = SQLAlchemy()
migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db)
app.logger.info('>>> {}'.format(Config.SQLALCHEMY_DATABASE_URI))

from .models import Users


# enable CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)


