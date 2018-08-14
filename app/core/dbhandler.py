from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_elasticsearch import FlaskElasticsearch

db = SQLAlchemy()

mongo_client = PyMongo()

es_client = FlaskElasticsearch()
