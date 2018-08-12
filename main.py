import os
from gevent.pywsgi import WSGIServer
from config import config
from app import create_app


if __name__ == '__main__':
    run_env = os.getenv('FLASK_CONFIG') or 'dev'
    app = create_app(config[run_env])
    if run_env != 'prod':
        app.run(host='0.0.0.0')
    else:
        app = WSGIServer(('0.0.0.0', 5000), app)
        app.serve_forever()
