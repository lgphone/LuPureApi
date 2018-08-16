import os
from redis import StrictRedis
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


SQLITE_PATH = os.path.join(BASE_DIR, 'sqlite3.db')
SESSION_KEY_PREFIX = 'session:'
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0

redis_client = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Flsdi12$ldsf1'


    @staticmethod
    def init_app(app):
        pass


class DevConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ssdi12$ldsf1'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLITE_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    MONGO_URI = 'mongodb://127.0.0.1:27017/test'
    ELASTICSEARCH_HOST = '127.0.0.1:9200'
    SESSION_TYPE = 'redis'  # session类型为redis
    SESSION_PERMANENT = False  # 如果设置为True，则关闭浏览器session就失效。
    SESSION_USE_SIGNER = False  # 是否对发送到浏览器上session的cookie值进行加密
    SESSION_KEY_PREFIX = SESSION_KEY_PREFIX  # 保存到session中的值的前缀
    SESSION_REDIS = redis_client  # 用于连接redis的配置


config = {
    'dev': DevConfig
}