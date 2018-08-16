from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.dbhandler import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(64), nullable=True)
    mobile = db.Column(db.String(32), nullable=True)
    sex = db.Column(db.Integer, default=0)
    avatar_url = db.Column(db.String(32), nullable=True)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
    time_modify = db.Column(db.String(32), onupdate=datetime.now)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
