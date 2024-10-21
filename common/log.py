import codecs
import os
import time
from logging import FileHandler


def config_logger(log_level, log_path, logger_module_list):
    base_config = {
        'version': 1,
        'formatters': {
            'application': {
                'format': '%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s'},
            'default': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}
        },
        'handlers': {
            'console': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'application_file': {
                'level': log_level,
                # 'class': 'logging.handlers.TimedRotatingFileHandler',
                'class': 'common.log.SafeFileHandler',
                'formatter': 'application',
                'filename': log_path,
                # 'when': 'D',
                'when': 'midnight',
                # 'when': 'M',
                'backupCount': 0,
                'encoding': 'UTF-8',
                'delay': 1  # 表示当第一次产生数据的时候才创建文件
            }
        },
        'loggers': {
        },
        'root': {
            'level': log_level,
            'handlers': ['application_file', 'console'],
            'propagate': False
        },
        'disable_existing_loggers': False
    }
    if isinstance(logger_module_list, str):
        base_config['loggers'][logger_module_list] = {
            'level': log_level,
            'handlers': ['application_file', 'console']
        }
    if isinstance(logger_module_list, (list, tuple)):
        for module_name in logger_module_list:
            if module_name in __name__:
                base_config['loggers'][module_name] = {'level': log_level,
                                                       'handlers': ['application_file', 'console'],
                                                       'propagate': False}
            else:
                base_config['loggers'][module_name] = {'level': log_level,
                                                       'handlers': ['application_file', 'console'],
                                                       'propagate': False}
    return base_config


class SafeFileHandler(FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=0, **kwargs):
        """
        Use the specified filename for streamed logging
        """
        if codecs is None:
            encoding = None
        FileHandler.__init__(self, filename, mode, encoding, delay)
        self.mode = mode
        self.encoding = encoding
        if kwargs.get('when') == 'S':
            # one second
            self.suffix = "%Y-%m-%d-%H-%M-%S"
        elif kwargs.get('when') == 'M':
            # one minute
            self.suffix = "%Y-%m-%d-%H-%M"
        elif kwargs.get('when') == 'H':
            # one hour
            self.suffix = "%Y-%m-%d-%H"
        elif kwargs.get('when') == 'D' or kwargs.get('when') in ['midnight', 'MIDNIGHT']:
            # one day
            self.suffix = "%Y-%m-%d"
        elif kwargs.get('when').startswith('W'):
            # one week
            self.suffix = "%Y-%W"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % kwargs.get('when'))
        self.suffix_time = ""

    def emit(self, record):
        """
        Emit a record.

        Always check time
        """
        try:
            if self.check_baseFilename(record):
                self.build_baseFilename()
            FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def check_baseFilename(self, record):
        """
        Determine if builder should occur.

        record is not used, as we are just comparing times,
        but it is needed so the method signatures are the same
        """
        timeTuple = time.localtime()

        if self.suffix_time != time.strftime(self.suffix, timeTuple) or not os.path.exists(
                self.baseFilename + '.' + self.suffix_time):
            return 1
        else:
            return 0

    def build_baseFilename(self):
        """
        do builder; in this case,
        old time stamp is removed from filename and
        a new time stamp is append to the filename
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # remove old suffix
        if self.suffix_time != "":
            index = self.baseFilename.find("." + self.suffix_time)
            if index == -1:
                index = self.baseFilename.rfind(".")
            self.baseFilename = self.baseFilename[:index]

        # add new suffix
        currentTimeTuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, currentTimeTuple)
        self.baseFilename = self.baseFilename + "." + self.suffix_time

        self.mode = 'a'
        if not self.delay:
            self.stream = self._open()
