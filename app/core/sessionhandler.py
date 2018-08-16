import uuid
import json
from flask.sessions import SessionInterface
from flask.sessions import SessionMixin
from app.core.dbhandler import redis_client
from app.config import HEADER_TOKEN_NAME, SESSION_KEY_PREFIX


class LuSession(dict, SessionMixin):
    def __init__(self, initial=None, sid=None):
        self.sid = sid
        self.initial = initial
        super(LuSession, self).__init__(initial or ())

    def __setitem__(self, key, value):
        super(LuSession, self).__setitem__(key, value)

    def __getitem__(self, item):
        return super(LuSession, self).__getitem__(item)

    def __delitem__(self, key):
        super(LuSession, self).__delitem__(key)


class LuSessionInterface(SessionInterface):
    session_class = LuSession
    container = {}

    def __init__(self):
        self.redis = redis_client

    def _generate_sid(self):
        return str(uuid.uuid4())

    def open_session(self, app, request):
        """
        程序刚启动时执行，需要返回一个session对象
        """
        # 从cookie 或者header 中获取sid
        sid = request.cookies.get(app.session_cookie_name) or request.headers.get(HEADER_TOKEN_NAME)
        if not sid:
            sid = self._generate_sid()
            return self.session_class(sid=sid)

        # session保存在redis中
        val = self.redis.get(SESSION_KEY_PREFIX + sid)

        # session保存在内存中
        # val = self.container.get(sid)

        if val is not None:
            try:
                data = json.loads(val)
                return self.session_class(data, sid=sid)
            except Exception as e:
                print(e)
                return self.session_class(sid=sid)
        return self.session_class(sid=sid)

    def save_session(self, app, session, response):
        """
        程序结束前执行，可以保存session中所有的值
        如：
            保存到resit
            写入到用户cookie
        """
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)

        # 只有在设置了才存数据库，不然不存
        if dict(session):
            val = json.dumps(dict(session))
            # session保存在redis中
            self.redis.setex(name=SESSION_KEY_PREFIX + session.sid, time=app.permanent_session_lifetime, value=val)
            # session保存在内存中
            # self.container.setdefault(session.sid, val)

        # 设置cookie
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=expires, httponly=httponly,
                            domain=domain, path=path, secure=secure)
        # 设置header
        if not response.headers.get(HEADER_TOKEN_NAME):
            response.headers[HEADER_TOKEN_NAME] = session.sid
