"""
@Description：
@Author：tsir
@Time：2024/10/19 15:58
@Copyright：©2019-2030 成都俊云科技有限公司
"""
from flask import Blueprint
from flask_restful import Api

from apps.panel.view import PlayerDataView, PartnerWinView, PlayerWinRankView

panel_bp = Blueprint('panel', __name__)
api = Api(panel_bp)

api.add_resource(PlayerDataView, '/v1/panel/player_detail')
api.add_resource(PartnerWinView, '/v1/panel/partner_win')
api.add_resource(PlayerWinRankView, '/v1/panel/player_rank')