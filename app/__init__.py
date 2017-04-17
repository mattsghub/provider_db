# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# local imports
from config import app_config
from instance import config as iconfig

# db variable initialization
db = SQLAlchemy()

login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username="mattspython",
        password="password123",
        hostname="mattspython.mysql.pythonanywhere-services.com",
        databasename="mattspython$provider_db",
        )#iconfig.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)
    from app import models

    #@app.route('/')
    #def hello_world():
    #    return 'Hello, World!'

    return app
