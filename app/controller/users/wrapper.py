from app.core.dbhandler import db
from app.model.users import Users, UserToRole, Roles, Permissions, RoleToPermission


def check_login(username, password):
    user_obj = Users.query.filter_by(username=username, available=1).first()
    if user_obj:
        check_status = user_obj.check_password(password)
        if check_status:
            return user_obj

    return False


def get_roles(user_id):
    roles_data = []
    role_ids = [_i[0] for _i in db.session.query(UserToRole.id).filter_by(id=user_id, available=1)]

    for _i in Roles.query.filter(Roles.id.in_(role_ids), Roles.available == 1).all():
        roles_data.append(_i.name)

    return roles_data


def get_permissions(user_id):
    permissions_data = []
    role_ids = [_i[0] for _i in db.session.query(UserToRole.id).filter_by(id=user_id, available=1)]

    permission_ids = [_i[0] for _i in db.session.query(RoleToPermission.perm_id).filter(
        RoleToPermission.perm_id.in_(role_ids),
        RoleToPermission.available == 1
    ).all()]

    for _i in Permissions.query.filter(Permissions.id.in_(permission_ids), Permissions.available == 1).all():
        permissions_data.append({
            'name': _i.name,
            'url': _i.url
        })

    return permissions_data
