"""
@Description：
@Author：tsir
@Time：2024/10/17 19:52
@Copyright：©2019-2030 成都俊云科技有限公司
"""
from common import db


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.String(32), nullable=False, unique=True, comment='比赛id')
    start_at = db.Column(db.DateTime, nullable=False, comment='比赛开始时间')
    match_time = db.Column(db.Integer, nullable=False, comment='比赛时长')
    state = db.Column(db.String(32), default='INIT', nullable=False, comment='数据状态')

    match_details = db.relationship('MatchDetail', backref='match')


class MatchBan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.String(32), nullable=False, unique=True, comment='比赛id')
    champion_id = db.Column(db.String(32), nullable=False, comment='英雄id')


class MatchDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.String(32), db.ForeignKey('match.match_id'), nullable=False, comment='比赛id')
    player_id = db.Column(db.String(32), nullable=False, comment='选手id')
    svp = db.Column(db.Integer, nullable=False, comment='是否为svp')
    mvp = db.Column(db.Integer, nullable=False, comment='是否为mvp')
    champion_id = db.Column(db.String(32), nullable=False, comment='英雄id')
    position = db.Column(db.String(32), nullable=False, comment='位置')
    score = db.Column(db.Integer, nullable=False, comment='得分')
    team_id = db.Column(db.String(32), nullable=False, comment='队伍id')
    win = db.Column(db.Integer, nullable=False, comment='是否胜利')
    kill = db.Column(db.Integer, nullable=False, comment='击杀数')
    death = db.Column(db.Integer, nullable=False, comment='死亡数')
    assist = db.Column(db.Integer, nullable=False, comment='助攻数')
    gold_earned = db.Column(db.Integer, nullable=False, comment='金币数')
    double_kills = db.Column(db.Integer, nullable=False, comment='连续击杀数')
    triple_kills = db.Column(db.Integer, nullable=False, comment='三杀数')
    quadra_kills = db.Column(db.Integer, nullable=False, comment='四杀数')
    penta_kills = db.Column(db.Integer, nullable=False, comment='五杀数')
    godlike = db.Column(db.Integer, nullable=False, comment='是否超神')
    champion_damage = db.Column(db.Integer, nullable=False, comment='英雄伤害')
    damage_taken = db.Column(db.Integer, nullable=False, comment='承受伤害')
    ward_placed = db.Column(db.Integer, nullable=False, comment='插眼数')
    gold_earned_percent = db.Column(db.Float, nullable=False, comment='金币占比')
    champion_damage_percent = db.Column(db.Float, nullable=False, comment='英雄伤害占比')


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(32), nullable=False, unique=True, comment='选手id')
    player_name = db.Column(db.String(32), nullable=False, comment='选手名称')
    player_real_name = db.Column(db.String(32), nullable=False, comment='选手真实姓名')
    player_grade = db.Column(db.String(32), nullable=False, comment='选手星级')


class Champion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    champion_id = db.Column(db.String(32), nullable=False, unique=True, comment='英雄id')
    champion_name = db.Column(db.String(32), nullable=False, comment='英雄名称')
    champion_icon = db.Column(db.String(32), nullable=False, comment='英雄图标')
