import math
import time

import requests


class LolQueryAcl(object):
    def __init__(self, cookies):
        self.url_map = {
            # 玩家搜索数据
            "search_player": "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/SearchPlayer",
            # 游戏模式数据
            "battle_report": "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetBattleReport",
            # 获取对局列表数据
            "battle_list": "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetBattleList",
            # 获取对局详情数据
            "battle_detail": "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetBattleDetail",
        }
        self.cookies = cookies

    def get_headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Referer": "https://www.wegame.com.cn/helper/lol/v2/index.html",
            "Cookie": self.cookies,
        }

    @staticmethod
    def get_area_data():
        return {1: {'id': '1', 'strid': 'HN1', 'isp': '电信一', 'name': '艾欧尼亚', 'idc': '东莞东城', 'tcls': '257',
                    'ob': '1'},
                3: {'id': '3', 'strid': 'HN2', 'isp': '电信二', 'name': '祖安', 'idc': '杭州东冠', 'tcls': '513',
                    'ob': '1'},
                4: {'id': '4', 'strid': 'HN3', 'isp': '电信三', 'name': '诺克萨斯', 'idc': '东莞大朗', 'tcls': '769',
                    'ob': '1'},
                2: {'id': '2', 'strid': 'WT1', 'isp': '网通一', 'name': '比尔吉沃特', 'idc': '济南担山屯',
                    'tcls': '258',
                    'ob': '1'},
                6: {'id': '6', 'strid': 'WT2', 'isp': '网通二', 'name': '德玛西亚', 'idc': '济南担山屯', 'tcls': '514',
                    'ob': '1'},
                9: {'id': '9', 'strid': 'WT3', 'isp': '网通三', 'name': '弗雷尔卓德', 'idc': '天津数据中心',
                    'tcls': '770',
                    'ob': '1'},
                5: {'id': '5', 'strid': 'HN4', 'isp': '电信四', 'name': '班德尔城', 'idc': '成都光华', 'tcls': '1025',
                    'ob': '0'},
                7: {'id': '7', 'strid': 'HN5', 'isp': '电信五', 'name': '皮尔特沃夫', 'idc': '杭州东冠', 'tcls': '1281',
                    'ob': '0'},
                8: {'id': '8', 'strid': 'HN6', 'isp': '电信六', 'name': '战争学院', 'idc': '东莞大朗', 'tcls': '1537',
                    'ob': '0'},
                10: {'id': '10', 'strid': 'HN7', 'isp': '电信七', 'name': '巨神峰', 'idc': '杭州东冠', 'tcls': '1793',
                     'ob': '0'},
                11: {'id': '11', 'strid': 'HN8', 'isp': '电信八', 'name': '雷瑟守备', 'idc': '东莞大朗', 'tcls': '2049',
                     'ob': '0'},
                12: {'id': '12', 'strid': 'WT4', 'isp': '网通四', 'name': '无畏先锋', 'idc': '济南担山屯',
                     'tcls': '1026',
                     'ob': '0'},
                17: {'id': '17', 'strid': 'HN12', 'isp': '电信十二', 'name': '钢铁烈阳', 'idc': '成都高新',
                     'tcls': '3073',
                     'ob': '0'},
                13: {'id': '13', 'strid': 'HN9', 'isp': '电信九', 'name': '裁决之地', 'idc': '成都高新', 'tcls': '2305',
                     'ob': '0'},
                14: {'id': '14', 'strid': 'HN10', 'isp': '电信十', 'name': '黑色玫瑰', 'idc': '东莞大朗',
                     'tcls': '2561',
                     'ob': '0'},
                15: {'id': '15', 'strid': 'HN11', 'isp': '电信十一', 'name': '暗影岛', 'idc': '东莞大朗',
                     'tcls': '2817',
                     'ob': '0'},
                16: {'id': '16', 'strid': 'WT5', 'isp': '网通五', 'name': '恕瑞玛', 'idc': '天津数据中心',
                     'tcls': '1282',
                     'ob': '0'},
                19: {'id': '19', 'strid': 'HN14', 'isp': '电信十四', 'name': '均衡教派', 'idc': '南京二长',
                     'tcls': '3585',
                     'ob': '0'},
                18: {'id': '18', 'strid': 'HN13', 'isp': '电信十三', 'name': '水晶之痕', 'idc': '杭州东冠',
                     'tcls': '3329',
                     'ob': '0'},
                20: {'id': '20', 'strid': 'WT6', 'isp': '网通六', 'name': '扭曲丛林', 'idc': '天津数据中心',
                     'tcls': '1538',
                     'ob': '0'},
                21: {'id': '21', 'strid': 'EDU1', 'isp': '教育网', 'name': '教育网专区', 'idc': '上海南汇',
                     'tcls': '65539',
                     'ob': '0'},
                22: {'id': '22', 'strid': 'HN15', 'isp': '电信十五', 'name': '影流', 'idc': '南京二长', 'tcls': '3841',
                     'ob': '0'},
                23: {'id': '23', 'strid': 'HN16', 'isp': '电信十六', 'name': '守望之海', 'idc': '南京二长',
                     'tcls': '4097',
                     'ob': '0'},
                24: {'id': '24', 'strid': 'HN17', 'isp': '电信十七', 'name': '征服之海', 'idc': '东莞大朗',
                     'tcls': '4353',
                     'ob': '0'},
                25: {'id': '25', 'strid': 'HN18', 'isp': '电信十八', 'name': '卡拉曼达', 'idc': '深圳蛇口',
                     'tcls': '4609',
                     'ob': '0'},
                26: {'id': '26', 'strid': 'WT7', 'isp': '网通七', 'name': '巨龙之巢', 'idc': '天津数据中心',
                     'tcls': '1794',
                     'ob': '0'},
                27: {'id': '27', 'strid': 'HN19', 'isp': '电信十九', 'name': '皮城警备', 'idc': '成都高新',
                     'tcls': '4865',
                     'ob': '0'},
                30: {'id': '30', 'strid': 'BGP1', 'isp': '全网络大区一', 'name': '男爵领域', 'idc': '上海腾讯宝信DC',
                     'tcls': '261', 'ob': '0'},
                31: {'id': '31', 'strid': 'BGP2', 'isp': '全网络大区二', 'name': '峡谷之巅', 'idc': '上海腾讯宝信DC',
                     'tcls': '517', 'ob': '0'}}

    @staticmethod
    def get_icon_full_path(icon_id):
        return f"https://wegame.gtimg.com/g.26-r.c2d3c/helper/lol/assis/images/resources/usericon/{icon_id}.png"

    @staticmethod
    def base_req_acl(resp):
        if resp.status_code != 200:
            return False, resp.text
        result = resp.json()
        if result['result']['error_code'] != 0:
            return False, result['result']['error_message']
        return True, result

    def get_player(self, nickname):
        data = {"nickname": nickname, "tag": 0, "page_size": 20, "from_src": "lol_helper"}
        resp = requests.post(headers=self.get_headers(), data=data, url=self.url_map['search_player'])
        success, result = self.base_req_acl(resp)
        if not success:
            return False, result
        return True, result['players']

    def combination_player_search_data(self, player_data, nickname):
        result = []
        for pd in player_data:
            result.append({
                "openid": pd["openid"],
                "area": self.get_area_data().get(pd['area'])['name'],
                "area_id": pd['area'],
                "icon": self.get_icon_full_path(pd['icon_id']),
                "level": pd['level'],
                "full_nickname": f"{nickname}#{pd['tag_num']}"
            })
        return result

    def get_battle_report(self, openid, area):
        data = {"account_type": 2, "area": area, "id": openid, "sids": [255], "from_src": "lol_helper"}
        resp = requests.post(headers=self.get_headers(), json=data, url=self.url_map['battle_report'])
        success, result = self.base_req_acl(resp)
        if not success:
            return False, result
        arm_data = {
            "total": result['battle_count']['total_arm_games'],
            "win": result['battle_count']['total_arm_wins'],
            "lost": result['battle_count']['total_arm_losts'],
            "win_rate": math.ceil(
                round(result['battle_count']['total_arm_wins'] / result['battle_count']['total_arm_games'] * 100, 1))
        }
        return True, arm_data

    def get_battle_list(self, openid, area, select_filter="aram", offset=0, count=5):
        """
        获取对局列表数据

        :param openid: 用户唯一id
        :param area: 大区  例如：艾欧里亚 1
        :param select_filter: 选择对局类型 aram-> 大乱斗
        :param offset: 偏移量 默认为0
        :param count: 查询对局数 默认 5
        """
        data = {
            "account_type": 2,
            "area": area,
            "id": openid,
            "count": count,
            "filter": select_filter,
            "offset": offset,
            "from_src": "lol_helper"
        }
        resp = requests.post(headers=self.get_headers(), json=data, url=self.url_map['battle_list'])
        success, result = self.base_req_acl(resp)
        if not success:
            return False, result
        if not result['battles']:
            return False, "暂无对局数据"
        # 只有自定义对局数据
        battle_list = [i for i in result['battles'] if i["game_queue_id"] == 0]
        return True, battle_list

    def get_battle_detail(self, openid, area, game_id):
        """
        获取对局列表数据

        :param openid: 用户唯一id
        :param area: 大区  例如：艾欧里亚 1
        :param game_id: 对局id
        """
        data = {
            "account_type": 2,
            "area": area,
            "id": openid,
            "game_id": game_id,
            "from_src": "lol_helper"
        }
        resp = requests.post(headers=self.get_headers(), json=data, url=self.url_map['battle_detail'])
        success, result = self.base_req_acl(resp)
        if not success:
            return False, result
        return True, result


if __name__ == '__main__':
    lol_client = LolQueryAcl()
    nn = "鹤林村丶村霸"
    success, my_data = lol_client.get_player(nn)
    print(success, my_data)
    # com_data = lol_client.combination_player_search_data(my_data, nn)
    # print(com_data)

    # 获取赛季数据
    # print(lol_client.get_battle_report("22ZF6+w2Pnz+xWtt8n2osA==", 1))
    # offset = 0
    # ret_list = []
    # range = 50
    # while True:
    #     ok, data = lol_client.get_battle_list(my_data[0]['openid'], 5, select_filter="", count=8, offset=offset)
    #     if not ok or len(ret_list) >= range:
    #         break
    #     ret_list.extend(data)
    #     offset += 8
    #     time.sleep(1)
    # ret_list = ret_list[:range]
    # print(len(ret_list),len([r for r in ret_list if r == 'Win']) / len(ret_list))
    print(lol_client.get_battle_detail("3blpHotwkRX4iqxMOBVPog==", 5, "500230925022"))
