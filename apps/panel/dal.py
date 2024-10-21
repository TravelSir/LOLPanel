"""
@Description：
@Author：tsir
@Time：2024/10/19 15:59
@Copyright：©2019-2030 成都俊云科技有限公司
"""
from sqlalchemy import func, distinct

from common import db
from models.lol import Player, MatchDetail, Match


def find_player(player_name):
    return Player.query.filter(
        Player.player_name.ilike(f'%{player_name}%')
    ).first()


def find_player_by_id(player_id):
    return Player.query.filter(
        Player.player_id == player_id
    ).first()


def query_match_details(player_id=None, match_ids=None):
    query = MatchDetail.query
    if player_id:
        query = query.filter(MatchDetail.player_id == player_id)
    if match_ids:
        query = query.filter(
            MatchDetail.match_id.in_(match_ids)
        )
    return query.all() or []


def query_matches_by_players(player_ids):
    matches_with_players = (
        db.session.query(Match)
        .join(MatchDetail)
        .filter(MatchDetail.player_id.in_(player_ids))
        .group_by(Match.match_id)
        .having(func.count(distinct(MatchDetail.player_id)) == len(player_ids))  # 确保每个比赛都包含所有player_ids
        .all()
    )

    return matches_with_players


