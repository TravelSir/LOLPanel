"""
@Description：
@Author：tsir
@Time：2024/10/17 19:52
@Copyright：©2019-2030 成都俊云科技有限公司
"""
from flasgger_marshmallow import swagger_decorator
from flask import request

from apps.crawler.serializer import CrawlerMatchDataJsonSchema, CommonResponseSchema
from apps.crawler.service import CrawlerService
from apps.crawler.service import CrawlerScriptService
from common.codes import request_finish, Codes
from common.utils import BaseView


class CrawlerMatchDataView(BaseView):
    @swagger_decorator(
        json_schema=CrawlerMatchDataJsonSchema,
        response_schema={200: CommonResponseSchema},
        tags=['比赛数据抓取']
    )
    def post(self):
        cookies = request.json_schema.get("cookies")
        open_id = request.json_schema.get("open_id")
        cs = CrawlerService(cookies, open_id)
        cs.crawl_match_data()
        return request_finish(code=Codes.OK, data={"code": "0", "msg": "success"})


class CrawlerMatchScriptView(BaseView):
    """一些自定义脚本执行"""

    def post(self):
        css = CrawlerScriptService()
        css.run_script()
        return request_finish(code=Codes.OK, data={"code": "0", "msg": "success"})