"""
@Description：
@Author：tsir
@Time：2024/10/19 15:58
@Copyright：©2019-2030 成都俊云科技有限公司
"""
from flasgger_marshmallow import swagger_decorator
from flask import request

from apps.panel.serializer import PlayerDataQuerySchema, CommonErrorResponseSchema, PartnerWinQuerySchema
from apps.panel.serializer import PlayerDataResponseSchema
from apps.panel.serializer import PartnerWinResponseSchema
from apps.panel.serializer import PlayerWinRankResponseSchema
from apps.panel.service import PlayerDataService
from apps.panel.service import PartnerWinService
from apps.panel.service import PlayerRankService
from common.codes import request_finish, Codes
from common.utils import BaseView


class PlayerDataView(BaseView):
    @swagger_decorator(
        query_schema=PlayerDataQuerySchema,
        response_schema={
            200: PlayerDataResponseSchema,
            400: CommonErrorResponseSchema
        },
        tags=['召唤师数据查询']
    )
    def get(self):
        player_name = request.query_schema.get("player_name")
        pd_s = PlayerDataService()
        ok, ret = pd_s.query_by_name(player_name)
        if not ok:
            return request_finish(code=Codes.BAD_REQUEST, data=ret)
        return request_finish(code=Codes.OK, data=ret)


class PartnerWinView(BaseView):
    @swagger_decorator(
        query_schema=PartnerWinQuerySchema,
        response_schema={
            200: PartnerWinResponseSchema,
            400: CommonErrorResponseSchema
        },
        tags=['合作伙伴胜率查询']
    )
    def get(self):
        base_player_name = request.query_schema.get("base_player_name")
        partner_player_name = request.query_schema.get("partner_player_name")
        pw_s = PartnerWinService(base_player_name, partner_player_name)
        ok, ret = pw_s.win_info()
        if not ok:
            return request_finish(code=Codes.BAD_REQUEST, data=ret)
        return request_finish(code=Codes.OK, data=ret)


class PlayerWinRankView(BaseView):
    @swagger_decorator(
        response_schema={200: PlayerWinRankResponseSchema},
        tags=['玩家胜率排行']
    )
    def get(self):
        pw_s = PlayerRankService()
        ok, ret = pw_s.rank_list()
        if not ok:
            return request_finish(code=Codes.BAD_REQUEST, data=ret)
        return request_finish(code=Codes.OK, data=ret)
