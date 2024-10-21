"""
@Description：
@Author：tsir
@Time：2024/10/18 10:40
@Copyright：©2019-2030 成都俊云科技有限公司
"""
from marshmallow import fields

from common.utils import BaseSchema


class CommonResponseSchema(BaseSchema):
    code = fields.String(required=True, doc='状态码')
    msg = fields.String(required=True, doc='状态描述')


class CrawlerMatchDataJsonSchema(BaseSchema):
    cookies = fields.String(required=True, description='cookies, 抓取战绩需要登录，所以这里需要cookies')
    open_id = fields.String(required=True, description='open_id, 用于标识用户')
