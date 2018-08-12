import os
from gevent.pywsgi import WSGIServer
from config import config
from app import create_app


if __name__ == '__main__':
    app = create_app(config[os.getenv('FLASK_CONFIG') or 'dev'])
    # app.run(host='0.0.0.0')
    app = WSGIServer(('0.0.0.0', 5000), app)
    app.serve_forever()
