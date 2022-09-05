from statistics import median

import click
import requests
from flask import Flask
from flask_crontab import Crontab

from app.config import BaseConfig, BasicConfig, TestConfig
from app.models import SKUModel, db
from app.routes import routes_blueprint
from app.core import get_lowest, get_highest, get_median

SQLALCHEMY_PATH = "/tmp/databasehelloprint.db"
SQLALCHEMY_DATABASE_URI = "sqlite:///" + SQLALCHEMY_PATH

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    db.create_all()
    app.register_blueprint(routes_blueprint)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "any secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = BaseConfig.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(routes_blueprint)
    crontab.init_app(app)
    return app


def create_app_test():
    # TODO Duplicate code with create_app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "any secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = TestConfig.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(routes_blueprint)
    return app


def setup_database(app):
    with app.app_context():
        db.create_all()
        app.logger.info("DB init!")


crontab = Crontab(app)

if __name__ == "__main__":
    app = create_app()
    setup_database(app)
    app.run()


@crontab.job(minute="*/1", day_of_week="1-5")
def scheduled_highest_price():
    print(get_highest().to_json())


# add crontab job to run */3 8-10 * * *
@crontab.job(minute="*/3", hour="8-10")
def scheduled_lowest_price():
    print(get_lowest().to_json())


# add crontab job to run */5 11-12 * * 1,3,5


@crontab.job(minute="*/5", hour="11-12", day_of_week="1,3,5")
def scheduled_median_price():
    print(get_median())
