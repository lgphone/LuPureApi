from datetime import datetime
from app.core.dbhandler import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(64), nullable=True)
    mobile = db.Column(db.String(32), nullable=True)
    sex = db.Column(db.Integer, default=0)
    avatar_url = db.Column(db.String(32), nullable=True)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.String(32), onupdate=datetime.now)
