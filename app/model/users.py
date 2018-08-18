from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.dbhandler import db


class Users(db.Model):
    """
    用户表
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(256))
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


class Roles(db.Model):
    """
    角色
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)


class Permissions(db.Model):
    """
    权限表
    """
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(64), nullable=True)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)


class UserToRole(db.Model):
    """
    用户角色对应表，
    有过期时间,unix格式 0为永不过期
    """
    __tablename__ = 'users_to_roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    available = db.Column(db.Boolean, default=1)
    time_expire = db.Column(db.Integer)
    time_create = db.Column(db.DateTime, default=datetime.now)


class RoleToPermission(db.Model):
    """
    角色权限对应表
    """
    __tablename__ = 'role_to_permission'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    perm_id = db.Column(db.Integer)
    available = db.Column(db.Boolean, default=1)
    time_create = db.Column(db.DateTime, default=datetime.now)
