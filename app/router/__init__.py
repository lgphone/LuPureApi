from app.controller.users.api import Index


routers = [
    ('/users/login', Index, 'users_login'),
]


def router_init(app):
    for _r in routers:
        app.add_url_rule(rule=_r[0], view_func=_r[1].as_view(name=_r[2]))
    return app
