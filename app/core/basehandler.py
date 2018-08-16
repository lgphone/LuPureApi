import datetime
import time
import uuid
import json
import hashlib
import base64
import copy


class BaseHandler(object):

    @classmethod
    def generate_hash_uuid(cls, limit=None):
        u = uuid.uuid4().hex
        if limit:
            u = u[:limit]
        return u

    @classmethod
    def get_datetime_now(cls):
        return datetime.datetime.now()

    @classmethod
    def get_timestamp(cls):
        return time.time()

    @classmethod
    def time_create(cls, t):
        return t.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def strptime(cls, t, f='%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.strptime(t, f)

    @classmethod
    def get_datetime_utcnow(cls):
        return datetime.datetime.utcnow()

    @classmethod
    def from_timestamp(cls, timestamp):
        return datetime.datetime.fromtimestamp(timestamp)

    @classmethod
    def to_timestamp(cls, t):
        return time.mktime(t.timetuple())

    @classmethod
    def sha1(cls, string):
        return hashlib.sha1(string.encode('UTF-8') if isinstance(string, str) else string).hexdigest()

    @classmethod
    def b64encode(cls, bytestring):
        return base64.b64encode(bytestring.encode('UTF-8') if isinstance(bytestring, str) else bytestring)

    @classmethod
    def b64decode(cls, bytestring):
        return base64.b64decode(bytestring.encode('UTF-8') if isinstance(bytestring, str) else bytestring)

    @classmethod
    def dumps(cls, obj, ensure_ascii=False):
        return json.dumps(obj, ensure_ascii=ensure_ascii)

    @classmethod
    def loads(cls, string, default=None):
        return json.loads(string) if string else default

    @classmethod
    def timedelta(cls, **kwargs):
        return datetime.timedelta(**kwargs)

    @classmethod
    def to_dict(cls, obj):
        data = copy.deepcopy(obj.__dict__)
        if data.get('_sa_instance_state'):
            data.pop('_sa_instance_state')
        if data.get('available'):
            data.pop('available')
        if data.get('id'):
            data.pop('id')
        for k, v in data.items():
            if isinstance(v, datetime.datetime):
                data[k] = cls.time_create(v)

        return data


class BaseError(Exception):
    def __init__(self, msg):
        self.code = 1001
        self.msg = msg

    def __str__(self):
        return self.msg


class AuthError(BaseError):
    def __init__(self, msg):
        self.code = 1002
        self.msg = msg


class VerifyError(BaseError):
    def __init__(self, msg):
        super(VerifyError, self).__init__(msg)
        self.code = 1003


class LogicError(BaseError):
    def __init__(self, msg):
        self.code = 1004
        self.msg = msg


class ParamsError(BaseError):
    def __init__(self, msg):
        self.code = 1005
        self.msg = msg


class Dict(dict):
    def __getattr__(self, item):
        resp = self.get(item, None)
        if isinstance(resp, dict):
            resp = Dict(resp)
        return resp

    def __setattr__(self, key, value):
        self[key] = value
