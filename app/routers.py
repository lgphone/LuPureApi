from app.controller.users.api import Login, Register, LoginOut, Profile, Captcha


routers = [
    ('/users/_captcha', Captcha, 'users_captcha'),
    ('/users/login', Login, 'users_login'),
    ('/users/register', Register, 'users_register'),
    ('/users/logout', LoginOut, 'users_logout'),
    ('/users/profile', Profile, 'users_profile'),
]


def router_init(app):
    for _r in routers:
        app.add_url_rule(rule=_r[0], view_func=_r[1].as_view(name=_r[2]))
    return app
