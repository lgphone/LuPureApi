# from flask import request


def middleware_init(app):
    @app.before_request
    def count_ip():
        # print('count_ip middleware')
        pass

    return app


