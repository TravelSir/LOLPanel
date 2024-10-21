
class TestConfig:
    DEBUG = True
    LOG_LEVEL = 'INFO'
    LOG_PATH = 'lol_panel.log'
    LOGGER_MODULE_LIST = ['apps', 'sqlalchemy.engine']
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/lol"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SALT = 'magicTsir'

    # rabmq配置
    RABMQ_RABBITMQ_URL = "amqp://guest:guest@127.0.0.1:5672/lolvhost"
    RABMQ_SEND_EXCHANGE_NAME = "lol_panel"
    RABMQ_SEND_EXCHANGE_TYPE = "topic"
