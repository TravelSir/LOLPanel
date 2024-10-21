"""
@Description：
@Author：tsir
@Time：2024/10/19 15:59
@Copyright：©2019-2030 成都俊云科技有限公司
"""
from marshmallow import fields

from common.utils import BaseSchema


class CommonErrorResponseSchema(BaseSchema):
    error_code = fields.Integer(required=True, doc='状态码')
    error_msg = fields.String(required=True, doc='状态描述')


class PlayerDataQuerySchema(BaseSchema):
    player_name = fields.String(required=True, doc='玩家昵称')


class PlayerDataResponseSchema(BaseSchema):
    player_name = fields.String(required=True, doc='玩家昵称')
    match_count = fields.Integer(required=True, doc='比赛场次')
    win_percent = fields.Float(required=True, doc='胜率')
    mvp_count = fields.Integer(required=True, doc='MVP次数')
    svp_count = fields.Integer(required=True, doc='SVP次数')
    kda = fields.Float(required=True, doc='KDA')
    damage_trans = fields.Float(required=True, doc='伤害转化率')


class PartnerWinQuerySchema(BaseSchema):
    base_player_name = fields.String(required=True, doc='基础玩家昵称')
    partner_player_name = fields.String(required=True, doc='合作玩家昵称')


class PartnerWinResponseSchema(BaseSchema):
    match_count = fields.Integer(required=True, doc='合作场次')
    win_count = fields.Integer(required=True, doc='胜利场次')
    win_percent = fields.Integer(required=True, doc='胜率')


class PlayerWinRankItemSchema(BaseSchema):
    rank = fields.Integer(required=True, doc='排名')
    player_name = fields.String(required=True, doc='玩家昵称')

    win_percent = fields.Integer(required=True, doc='胜率')


class PlayerWinRankItemSchema(BaseSchema):
    # rank = fields.Integer(required=True, doc='排名')
    player_name = fields.String(required=True, doc='玩家昵称')
    total_count = fields.Integer(required=True, doc='总场次')
    win_count = fields.Integer(required=True, doc='胜利场次')
    win_percent = fields.Float(required=True, doc='胜率')


class PlayerWinRankResponseSchema(BaseSchema):
    rank_list = fields.Nested(PlayerWinRankItemSchema, many=True, doc="排行榜")