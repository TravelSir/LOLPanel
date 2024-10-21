
class ProductionConfig:
    DEBUG = False
    LOG_LEVEL = 'INFO'
    LOG_PATH = '/var/log/lol_panel.log'
    LOGGER_MODULE_LIST = ['apps', 'sqlalchemy.engine']
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://SA:Pwd123456@localhost:1433/test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SALT = 'FT6N|Rj["fE!d]kq'

    # rabmq配置
    RABMQ_RABBITMQ_URL = "amqp://guest:guest@127.0.0.1:5672/lolvhost"
    RABMQ_SEND_EXCHANGE_NAME = "lol_panel"
    RABMQ_SEND_EXCHANGE_TYPE = "topic"
