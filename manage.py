from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from gevent.pywsgi import WSGIServer
from app import app as main_app
from app.core.dbhandler import db

manager = Manager(main_app)
migrate = Migrate(main_app, db)


@manager.command
def hello():
    print('hello')


@manager.command
def create_all():
    print('starting migrate db...')
    db.create_all(app=main_app)
    print('migrate db over')


@manager.command
def drop_all():
    db.drop_all()


@manager.command
def run_prod():
    app = WSGIServer(('0.0.0.0', 5000), main_app)
    app.serve_forever()


manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
