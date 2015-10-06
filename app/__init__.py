from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

import os
from config import config

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

with app.app_context():
    config_name = os.getenv('CONFIG') or 'default'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(userid):
        return User.query.filter_by(user_id=userid).first()

from .views import *
from .models import User
