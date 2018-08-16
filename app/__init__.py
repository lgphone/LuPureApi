import os
from gevent import monkey
monkey.patch_all()


from flask import Flask
from flask_session import Session
from .config import config
from .routers import router_init
from .middleware import middleware_init
from .core.dbhandler import db, mongo_client, es_client


# 获取配置信息
config_obj = config[os.getenv('FLASK_CONFIG') or 'dev']

# 生成app对象，并初始化
app = Flask(__name__)
app.config.from_object(config_obj)
Session(app)
db.init_app(app)
mongo_client.init_app(app)
es_client.init_app(app)
router_init(app)
middleware_init(app)
