import os
from flask_script import Manager
from gevent.pywsgi import WSGIServer
from config import config
from app import create_app
from app.core.dbhandler import db

run_env = os.getenv('FLASK_CONFIG') or 'dev'
app = create_app(config[run_env])

manager = Manager(app)


@manager.command
def hello():
    print('hello')


@manager.command
def migrate():
    print('starting migrate db...')
    db.create_all(app=app)
    print('migrate db over')


@manager.command
def run_prod():
    app = create_app(config[run_env])
    app = WSGIServer(('0.0.0.0', 5000), app)
    app.serve_forever()


if __name__ == "__main__":
    manager.run()
