"""
@Description：
@Author：tsir
@Time：2024/10/17 19:51
@Copyright：©2019-2030 成都俊云科技有限公司
"""
from flask import Blueprint
from flask_restful import Api

from apps.crawler.view import CrawlerMatchDataView
from apps.crawler.view import CrawlerMatchScriptView

crawler_bp = Blueprint('crawler', __name__)
api = Api(crawler_bp)

api.add_resource(CrawlerMatchDataView, '/v1/crawler/match_data')
api.add_resource(CrawlerMatchScriptView, '/v1/crawler/script')
