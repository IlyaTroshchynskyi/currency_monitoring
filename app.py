import logging
from logging.config import dictConfig
from flask.logging import default_handler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import LOGGING


dictConfig(LOGGING)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///golden-eye.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.logger = logging.getLogger('GoldenEye')
app.logger.removeHandler(default_handler)


import views
