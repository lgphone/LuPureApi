from app.core.apihandler import ApiHandler
from app.model.users import Users


class Index(ApiHandler):
    def get(self):
        import time
        time.sleep(10)
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
        self.db_session.add(user)
        self.db_session.commit()

