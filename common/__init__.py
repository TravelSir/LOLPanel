import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS
from flask_rabmq import RabbitMQ

from common.log import config_logger
from config import Config
import logging.config

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(session_options={'autocommit': True})

# 初始化环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 初始化日志
logging.config.dictConfig(config_logger(Config.LOG_LEVEL, Config.LOG_PATH, Config.LOGGER_MODULE_LIST))
logger = logging.getLogger(__name__)

CORS(app, supports_credentials=True, expose_headers=['Set-Cookie'])

# 初始化DB
db.init_app(app)

# 初始化rabmq
rabmq = RabbitMQ()
rabmq.init_app(app)
