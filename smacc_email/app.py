import os

import flask

from werkzeug.local import LocalProxy

from common import swagger
from common.sentry import register_sentry

import smacc_email.api
from smacc_email import schemas
from smacc_email import settings


def create_app(config: dict):
    app = flask.Flask(__name__)
    app.config.update(**config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_sentry(app)
    schemas.manager.init_app(app)
    smacc_email.api.manager.init_app(app)
    app.register_blueprint(swagger.blueprint)
    return app


api = LocalProxy(lambda: create_app(settings.api_config(os.environ)))
