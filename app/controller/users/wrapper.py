from app.model.users import Users


def check_login(username, password):
    user_obj = Users.query.filter_by(username=username).first()
    if user_obj:
        check_status = user_obj.check_password(password)
        if check_status:
            return user_obj

    return False
