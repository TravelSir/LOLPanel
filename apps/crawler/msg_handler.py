"""
@Description：
@Author：tsir
@Time：2024/10/18 11:05
@Copyright：©2019-2030 成都俊云科技有限公司
"""
import json
import logging
import time
import urllib.parse
import uuid

from apps.crawler.dal import find_latest_match_id, save_match, query_init_matches, query_players, add_player, \
    add_match_ban_info, add_match_detail, finish_match_crawl
from common import rabmq
from common.const import RabbitmqRoutingKey
from common.utils import TimeUtil
from components.wegame_spider import LolQueryAcl

logger = logging.getLogger(__name__)


@rabmq.queue(exchange_name="lol_panel", routing_key=RabbitmqRoutingKey.CRAWL_MATCH_DATA_TASK)
def crawl_match_data_task(message):
    logger.info(f"收到抓取比赛数据任务: {message}")
    message = json.loads(message)
    cookies = message.get("cookies")
    lol_client = LolQueryAcl(cookies)

    #
    base_open_id = message.get("open_id")

    match_list = []
    offset = 0
    latest_match = find_latest_match_id()
    # 拉取所有自定义对局
    while True:
        ok, data = lol_client.get_battle_list(base_open_id, 5, select_filter="", count=8, offset=offset)
        if not ok:
            break
        match_list.extend(data)
        # 只拉取新的对局
        latest_start_at = TimeUtil.timestamp_to_datetime(int(data[-1].get("game_start_time"))/1000)
        if latest_match and data and latest_match.start_at >= latest_start_at:
            break

        offset += 8
        time.sleep(0.5)

    # 存储对局数据
    for mc in match_list:
        match_id = mc.get("game_id")
        start_at = TimeUtil.timestamp_to_datetime(int(mc.get("game_start_time"))/1000)
        match_time = mc.get("game_time_played")
        if latest_match and latest_match.match_id == mc.get("game_id"):
            break
        # 保存对局数据
        save_match(
            match_id=match_id,
            start_at=start_at,
            match_time=match_time
        )

    # 触发抓取对局详情任务
    rabmq.send(
        routing_key=RabbitmqRoutingKey.CRAWL_MATCH_DETAIL_TASK,
        body={
            "message_id": str(uuid.uuid4()).replace('-', ''),
            "cookies": cookies,
            "base_open_id": base_open_id}
    )
    return True


@rabmq.queue(exchange_name="lol_panel", routing_key=RabbitmqRoutingKey.CRAWL_MATCH_DETAIL_TASK)
def crawl_match_detail(message):
    logger.info(f"收到抓取比赛详情任务: {message}")
    message = json.loads(message)
    cookies = message.get("cookies")
    base_open_id = message.get("base_open_id")
    lol_client = LolQueryAcl(cookies)

    # 仅触发，自动扫描未抓取的对局详情
    matches = query_init_matches()
    exist_players = [pl.player_id for pl in query_players()]
    for match in matches:
        logger.info(f"开始抓取对局详情: {match.match_id}")
        ok, detail = lol_client.get_battle_detail(base_open_id, 5, match.match_id)
        if not ok:
            logger.error(f"对局详情抓取失败: {match.match_id}")
            return True
        players = detail['battle_detail']['player_details']
        # 排除非内战自定义，两边的人都必须满足三人在群里
        team_dict = dict()
        for player in players:
            team_dict.setdefault(player['teamId'], []).append(player['openid'])

        need_filter = False
        for k, v in team_dict.items():
            cnt = 0
            for pid in v:
                if pid in exist_players:
                    cnt += 1
            if cnt < 3:
                need_filter = True
                break

        if need_filter:
            finish_match_crawl(match.match_id, 'FILTER')

        # 保存玩家信息
        for player in players:
            if player['openid'] not in exist_players:
                add_player(
                    player_id=player['openid'],
                    player_name=urllib.parse.unquote(player['name'])
                )
                exist_players.append(player['openid'])
            add_match_detail(
                match_id=match.match_id,
                player_id=player['openid'],
                svp=player['battleHonour']['isSvp'],
                mvp=player['battleHonour']['isMvp'],
                champion_id=player['championId'],
                position=player['position'],
                score=player['gameScore'],
                team_id=player['teamId'],
                win=1 if player['win'] == 'Win' else 0,
                kill=player['championsKilled'],
                death=player['numDeaths'],
                assist=player['assists'],
                gold_earned=player['goldEarned'],
                double_kills=player['battleHonour']['isDoubleKills'],
                triple_kills=player['battleHonour']['isTripleKills'],
                quadra_kills=player['battleHonour']['isQuadraKills'],
                penta_kills=player['battleHonour']['isPentaKills'],
                godlike=player['battleHonour']['isGodlike'],
                champion_damage=player['totalDamageToChampions'],
                damage_taken=player['totalDamageTaken'],
                ward_placed=player['wardPlaced']
            )

        # 更新ban信息
        ban_info = []
        team_details = detail['battle_detail']['team_details']
        [ban_info.extend(team['banInfoList']) for team in team_details]
        for bi in ban_info:
            add_match_ban_info(
                match_id=match.match_id,
                champion_id=bi['championId']
            )

        finish_match_crawl(match.match_id)
        logger.info(f"对局详情抓取完成: {match.match_id}")
    return True
