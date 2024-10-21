"""
@Description：
@Author：tsir
@Time：2024/10/18 10:44
@Copyright：©2019-2030 成都俊云科技有限公司
"""
import uuid

from apps.crawler.dal import get_match_details, update_match_detail
from common.const import RabbitmqRoutingKey
from common import rabmq


class CrawlerService:
    def __init__(self, cookies, open_id):
        self.cookies = cookies
        self.open_id = open_id

    def crawl_match_data(self):
        """
        抓取比赛数据, 仅触发，抛出消息去执行

        """
        rabmq.send(
            routing_key=RabbitmqRoutingKey.CRAWL_MATCH_DATA_TASK,
            body={
                "message_id": str(uuid.uuid4()).replace('-', ''),
                "cookies": self.cookies,
                "open_id": self.open_id,
            }
        )


class CrawlerScriptService:

    def run_script(self):
        self.init_damage_trans()

    def init_damage_trans(self):
        match_details = get_match_details()
        # 按比赛+队伍分组统计总伤害和总经济
        match_dict = dict()

        for md in match_details:
            if md.match_id not in match_dict:
                match_dict[md.match_id] = dict(
                    total_damage=0,
                    total_gold=0,
                )
            match_dict[md.match_id]["total_damage"] += md.champion_damage
            match_dict[md.match_id]["total_gold"] += md.gold_earned

        # 保存到数据库
        for md in match_details:
            # 计算伤转
            total_damage = match_dict.get(md.match_id).get("total_damage")
            total_gold = match_dict.get(md.match_id).get("total_gold")
            update_match_detail(md.match_id, {
                'champion_damage_percent': round(md.champion_damage * 100 / total_damage, 2),
                'gold_earned_percent': round(md.gold_earned * 100 / total_gold, 2),
            })

