from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_elasticsearch import FlaskElasticsearch
from app.config import redis_client

db = SQLAlchemy()

mongo_client = PyMongo()

es_client = FlaskElasticsearch()

redis_client = redis_client
