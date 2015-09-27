from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin

import os
from config import config

app = Flask(__name__)
db = SQLAlchemy()
admin = Admin()

with app.app_context():
    config_name = os.getenv('CONFIG') or 'default'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    admin.init_app(app)

from .views import index
