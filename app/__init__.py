from gevent import monkey
monkey.patch_all()

from flask import Flask
from app.router import router_init
from app.middleware import middleware_init
from app.core.dbhandler import db, mongo_client, es_client


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    db.init_app(app)
    mongo_client.init_app(app)
    es_client.init_app(app)
    router_init(app)
    middleware_init(app)
    return app
