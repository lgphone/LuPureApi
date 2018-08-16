from app.core.dbhandler import db
from app.model.users import Users, UserToRole, Roles, Permissions, RoleToPermission


def check_login(username, password):
    user_obj = Users.query.filter_by(username=username).first()
    if user_obj:
        check_status = user_obj.check_password(password)
        if check_status:
            return user_obj

    return False


def get_roles(user_id):
    role_ids = [_i[0] for _i in db.session.query(UserToRole.id).filter_by(id=user_id)]
    print(role_ids)

