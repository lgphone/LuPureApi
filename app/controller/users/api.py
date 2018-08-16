from sqlalchemy.exc import IntegrityError
from app.core.apihandler import ApiHandler
from app.core.basehandler import AuthError, LogicError
from app.model.users import Users
from app.utils import need_params, login_required
from .wrapper import check_login


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
        self.db.session.add(user)
        self.db.session.commit()


class Login(ApiHandler):
    @need_params(*['username', 'password'])
    def post(self):
        user_obj = check_login(username=self.input.username, password=self.input.password)
        if user_obj:
            user_info = self.to_dict(user_obj)
            user_info.pop('password')
            # 设置session Header
            self.set_header['X-Token-Id'] = self.session_id
            # 登陆tags
            self.session['is_login'] = True
            # 添加user信息，方便下次调用
            self.session['user'] = user_info
            # 返回用户信息
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
            self.db.session.add(user_obj)
            self.db.session.commit()
        except IntegrityError:
            raise LogicError("用户名重复")


class Profile(ApiHandler):
    @login_required()
    def post(self):
        user_info = self.session.get('user')
        user_obj = Users.query.filter_by(uid=user_info['uid']).first()

        if self.input.email:
            user_info['email'] = user_obj.email = self.input.email
        if self.input.sex:
            user_info['sex'] = user_obj.email = self.input.sex
        if self.input.avatar_url:
            user_info['avatar_url'] = user_obj.email = self.input.avatar_url

        self.session['user'] = user_info
        self.db.session.add(user_obj)
        self.db.session.commit()

    @login_required()
    def get(self):
        user_info = self.session.get('user')
        return user_info
