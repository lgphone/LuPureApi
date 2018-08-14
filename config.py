import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123sdf9sdjkksdr'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tmp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    MONGO_URI = 'mongodb://127.0.0.1:27017/test'
    ELASTICSEARCH_HOST = '127.0.0.1:9200'


config = {
    'dev': DevConfig
}