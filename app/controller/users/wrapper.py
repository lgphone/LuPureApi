from flask import session
from app.model.users import Users


def check_login(username, password):
    user_obj = Users.query.filter_by(username=username).first()
    if user_obj:
        check_status = user_obj.check_password(password)
        if check_status:
            session['is_login'] = True
            session['user'] = user_obj
            user_info = {
                'id': user_obj.id,
                'username': user_obj.username,
                'email': user_obj.email,
                'sex': user_obj.sex,
                'time_create': user_obj.time_create
            }
            return user_info

    return False
