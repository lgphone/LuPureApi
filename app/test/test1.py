from gevent import monkey
monkey.patch_all()

from flask import Flask
from gevent import pywsgi

import time

app = Flask(__name__)
# app.debug = True

@app.route('/')
def index():
    time.sleep(10)
    return 'Hello World1'

@app.route('/1')
def index1():
    return 'Hello World111'


server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
server.serve_forever()