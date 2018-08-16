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
        user_info = check_login(username=self.input.username, password=self.input.password)
        if user_info:
            return user_info
        else:
            raise AuthError('账号密码不正确')


class LoginOut(ApiHandler):
    @login_required()
    def get(self):
        return self.post

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
        user_obj = self.session.get('user')
        if self.input.email:
            user_obj.email = self.input.email
        if self.input.sex:
            user_obj.sex = self.input.sex
        if self.input.avatar_url:
            user_obj.avatar_url = self.input.avatar_url
        self.db.session.add(user_obj)
        self.db.session.commit()
        self.session['user'] = user_obj

    @login_required()
    def get(self):
        user_obj = self.session.get('user')
        data = self.to_dict(user_obj)
        data.pop('password')

        return data
