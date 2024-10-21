import datetime
import logging
import re
import time
import traceback
from functools import wraps

from flask import request
from flask_restful import Resource
from marshmallow import Schema

logger = logging.getLogger(__name__)


def except_middleware(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = None
        try:
            logger.info(
                '[%s]: request url %s',
                re.sub(r"\s.*", "", re.sub(r'.*method\s', "", func.__str__().replace("<function ", ""))),
                request.url
            )
            result = func(*args, **kwargs)
        except Exception as E:
            logger.error(traceback.format_exc())
            result = {"error_code": 500, "error_msg": "服务错误，请重试！"}, 500
        finally:
            end_time = time.time()
            logger.info(
                '[%s]: request response %s %s',
                re.sub(r"\s.*", "", re.sub(r'.*method\s', "", func.__str__().replace("<function ", ""))),
                str(result)[:500] + '......' + str(result)[-500:] if len(str(result)) > 1000 else result,
                end_time - start_time
            )
            return result

    return wrapper


class BaseView(Resource):
    method_decorators = [except_middleware]


class BaseSchema(Schema):

    class Meta:
        strict = True  # 通过抛异常的方式提示错误


def datetime_to_time_str(date_time):
    if type(date_time) == str:
        return date_time
    try:
        time_str = date_time.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        time_str = ''
    return time_str


class TimeUtil:
    @classmethod
    def timestamp_to_datetime(cls, timestamp):
        return datetime.datetime.fromtimestamp(timestamp)
