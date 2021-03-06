# -*- coding:utf-8 -*-
import os
import sys

import logging

import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

reload(sys)

if sys.getdefaultencoding() != 'utf8':
    sys.setdefaultencoding('utf8')

app = Flask(__name__, static_folder= os.path.join(os.path.dirname(__file__), "..", "static"))
# app.config.from_pyfile('flaskapp.cfg')

log_file_name = os.path.join(
    os.environ.get('OPENSHIFT_PYTHON_LOG_DIR', '.'),
    'app.log')

handler = logging.FileHandler(log_file_name, mode='a')
handler.setLevel(logging.INFO)
fmt = "%(asctime)s\t%(message)s"
# 实例化formatter
formatter = logging.Formatter(fmt)
# 为handler添加formatter
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

pool = redis.ConnectionPool(host=os.environ.get('OPENSHIFT_REDIS_HOST', 'localhost'),
                            port=int(os.environ.get('OPENSHIFT_REDIS_PORT', '16379')),
                            password=os.environ.get('REDIS_PASSWORD', None))

app.redis = redis.StrictRedis(connection_pool=pool)

# 定义常量
APP_ID = os.environ.get('BAIB_ID', None)
API_KEY = os.environ.get('BAIB_KEY', None)
SECRET_KEY = os.environ.get('BAIB_SECRET', None)

# # 初始化AipNlp对象
# if APP_ID and API_KEY and SECRET_KEY:
#     app.aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)
# else:
#     app.aipNlp = None

from models import *
from views import *
from naodong import recite_word_page
from talkerchu import talkerchu_page

app.register_blueprint(talkerchu_page, url_prefix="/talkerchu")
app.register_blueprint(recite_word_page, url_prefix="/reciteword")
