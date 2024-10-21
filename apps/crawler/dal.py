"""
@Description：
@Author：tsir
@Time：2024/10/18 10:50
@Copyright：©2019-2030 成都俊云科技有限公司
"""
from common import db
from models.lol import Match, Player, MatchBan, MatchDetail


def find_latest_match_id():
    return Match.query.order_by(Match.start_at.desc()).first()


def save_match(match_id,start_at,match_time):
    record = Match(
        match_id=match_id,
        start_at=start_at,
        match_time=match_time
    )
    db.session.add(record)
    db.session.flush()
    return record


def query_init_matches():
    return Match.query.filter(Match.state == 'INIT').all() or []


def query_players():
    return Player.query.all() or []


def add_player(player_id, player_name):
    record = Player(
        player_id=player_id,
        player_name=player_name,
        player_real_name="",
        player_grade=""
    )
    db.session.add(record)
    db.session.flush()
    return record


def add_match_ban_info(match_id, champion_id):
    record = MatchBan(
        match_id=match_id,
        champion_id=champion_id
    )
    db.session.add(record)
    db.session.flush()
    return record


def add_match_detail(match_id, player_id, svp, mvp, champion_id, position, score, team_id, win, kill, death, assist, gold_earned, double_kills, triple_kills, quadra_kills, penta_kills, godlike, champion_damage, damage_taken, ward_placed):
    record = MatchDetail(
        match_id=match_id,
        player_id=player_id,
        svp=svp,
        mvp=mvp,
        champion_id=champion_id,
        position=position,
        score=score,
        team_id=team_id,
        win=win,
        kill=kill,
        death=death,
        assist=assist,
        gold_earned=gold_earned,
        double_kills=double_kills,
        triple_kills=triple_kills,
        quadra_kills=quadra_kills,
        penta_kills=penta_kills,
        godlike=godlike,
        champion_damage=champion_damage,
        damage_taken=damage_taken,
        ward_placed=ward_placed,
    )
    db.session.add(record)
    db.session.flush()
    return record


def finish_match_crawl(match_id, state='FINISH'):
    Match.query.filter(Match.match_id == match_id).update({'state': state})


def get_match_details():
    return MatchDetail.query.all()


def update_match_detail(match_id, update_kwargs):
    MatchDetail.query.filter(MatchDetail.match_id == match_id).update(update_kwargs)
