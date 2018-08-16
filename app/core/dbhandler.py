from redis import ConnectionPool, StrictRedis
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_elasticsearch import FlaskElasticsearch
from app.config import REDIS_HOST, REDIS_DB, REDIS_PORT

db = SQLAlchemy()

mongo_client = PyMongo()

es_client = FlaskElasticsearch()

r_conn_pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

redis_client = StrictRedis(connection_pool=r_conn_pool)
