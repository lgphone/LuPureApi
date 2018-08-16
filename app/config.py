import os
from datetime import timedelta
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


SQLITE_PATH = os.path.join(BASE_DIR, 'sqlite3.db')
SESSION_KEY_PREFIX = 'session:'
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
HEADER_TOKEN_NAME = 'X-Token'
SESSION_COOKIE_NAME = 'token'


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'Flsdi12$ldsf1'


    @staticmethod
    def init_app(app):
        pass


class DevConfig(BaseConfig):
    DEBUG = True
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'ssdi12$ldsf1'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLITE_PATH
    SESSION_COOKIE_NAME = SESSION_COOKIE_NAME
    REMEMBER_COOKIE_DURATION = timedelta(days=3)
    SQLALCHEMY_DATABASE_URI = 'mysql://flask:123456@192.168.1.30:3306/flask?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    SQLALCHEMY_POOL_SIZE = 10
    MONGO_URI = 'mongodb://127.0.0.1:27017/test'
    ELASTICSEARCH_HOST = '127.0.0.1:9200'


config = {
    'dev': DevConfig
}