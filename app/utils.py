import functools
import json
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import request
from .core.basehandler import LogicError, AuthError
from .core.dbhandler import redis_client
from app.config import SESSION_KEY_PREFIX, SESSION_COOKIE_NAME, HEADER_TOKEN_NAME, BASE_DIR


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


def generate_check_code(width=120, height=30, char_length=5, font_name='Rocko.ttf', font_size=28):
    font_file = os.path.join(BASE_DIR, 'fonts', font_name)

    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))

    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)
