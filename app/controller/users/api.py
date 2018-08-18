from io import BytesIO
from sqlalchemy.exc import IntegrityError
from app.core.dbhandler import db
from app.core.apihandler import ApiHandler
from app.core.basehandler import AuthError, LogicError, VerifyError
from app.model.users import Users
from app.utils import need_params, login_required, generate_check_code
from .wrapper import check_login, get_roles


class Index(ApiHandler):
    def get(self):
        data = [
            {'id': _i.id,
             'username': _i.username,
             'sex': _i.sex,
             'time_create': self.time_create(_i.time_create),
             'time_modify': self.time_create(_i.time_modify) if _i.time_modify else None
             }
            for _i in Users.query.all()]

        self.set_cookie.update({'name': 'yang'})
        return data

    def post(self):
        user = Users(username=self.input.username, password=self.input.password)
        db.session.add(user)
        db.session.commit()


class Login(ApiHandler):
    @need_params(*['username', 'password'])
    def post(self):
        user_obj = check_login(username=self.input.username, password=self.input.password)
        if user_obj:
            self.session['is_login'] = True

            roles = get_roles(user_obj.id)
            self.session['roles'] = roles

            user_info = self.to_dict(user_obj)
            user_info.pop('password')
            # 登陆 Flag
            self.session['user'] = user_info

            return user_info
        else:
            raise AuthError('账号或密码不正确')


class LoginOut(ApiHandler):
    @login_required()
    def get(self):
        self.session.clear()

    @login_required()
    def post(self):
        self.session.clear()


class Register(ApiHandler):
    @need_params(*['username', 'password'])
    def post(self):
        try:
            user_obj = Users(username=self.input.username, uid=self.generate_hash_uuid(12))
            user_obj.set_password(password=self.input.password)
            db.session.add(user_obj)
            db.session.commit()
        except IntegrityError:
            raise LogicError("用户名重复")


class Profile(ApiHandler):
    @login_required()
    def post(self):
        user_info = self.session.get('user')
        user_obj = Users.query.filter_by(uid=user_info['uid'], available=1).first()

        if self.input.email:
            user_info['email'] = user_obj.email = self.input.email
        if self.input.sex:
            user_info['sex'] = user_obj.email = self.input.sex
        if self.input.avatar_url:
            user_info['avatar_url'] = user_obj.email = self.input.avatar_url

        self.session['user'] = user_info
        db.session.add(user_obj)
        db.session.commit()

    @login_required()
    def get(self):
        user_info = self.session.get('user')
        return user_info


class Captcha(ApiHandler):
    def get(self):
        stream = BytesIO()
        img, code = generate_check_code()
        img.save(stream, 'png')
        self.session['code'] = code
        # base64  byte 转 str
        captcha = self.b64encode(stream.getvalue()).decode('utf-8')
        # 生成图片数据
        captcha = 'data:image/png;base64,' + captcha

        return captcha

    @need_params('code')
    def post(self):
        code = self.input.code
        if code.upper() != self.session.get('code'):
            raise VerifyError('验证码错误')

        # 设置session为验证通过，这样比如收集验证码就可以根据此字段判断用户是否已经输入验证码并正确的
        self.session['code_pass'] = True
