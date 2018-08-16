import functools
import json
from flask import request
from .core.basehandler import LogicError, AuthError
from .core.dbhandler import redis_client
from app.config import SESSION_KEY_PREFIX, SESSION_COOKIE_NAME, HEADER_TOKEN_NAME


def login_required(*args):
    role = args

    def func_wrapper(func):

        @functools.wraps(func)
        def _func_wrapper(cls, *args, **kwargs):

            t_id = request.cookies.get(SESSION_COOKIE_NAME) or request.headers.get(HEADER_TOKEN_NAME) or None
            if not t_id:
                raise AuthError('无效的认证')

            session_data = json.loads(redis_client.get(SESSION_KEY_PREFIX + t_id)) \
                if redis_client.get(SESSION_KEY_PREFIX + t_id) else None

            if not session_data or not session_data.get('is_login'):
                raise AuthError('无效的认证')

            if not role or role in session_data.get('roles'):
                return func(cls, *args, **kwargs)
            else:
                raise AuthError('没有权限')

        return _func_wrapper

    return func_wrapper


def need_params(*params, **type_params):

    def dec(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            for arg in params:
                if getattr(self.input, arg) is None:
                    raise LogicError('需要:%s 参数' % arg)
            for k, _type in type_params.items():
                if getattr(self.input, k) is None:
                    raise LogicError('需要:%s 参数' % k)
                if not isinstance(getattr(self.input, k), _type):
                    raise LogicError('参数 "%s" 类型应该是: %s' % (k, _type))

            return func(self, *args, **kwargs)

        return wrapper

    return dec
