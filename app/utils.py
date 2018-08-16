import functools
from .core.basehandler import LogicError, AuthError
from flask import request, session


def login_required(*args):
    role = args

    def func_wrapper(func):

        @functools.wraps(func)
        def _func_wrapper(cls, *args, **kwargs):
            session_id = request.cookies.get('session') or request.headers.get('X-Token-Id') or None

            if not session_id or not session.get('is_login'):
                raise AuthError('无效的认证')

            if not role or role in session.get('roles'):
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
