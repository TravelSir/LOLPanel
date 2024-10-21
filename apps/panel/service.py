"""
@Description：
@Author：tsir
@Time：2024/10/19 15:58
@Copyright：©2019-2030 成都俊云科技有限公司
"""
from apps.panel.dal import find_player, query_match_details, query_matches_by_players, find_player_by_id


class PlayerDataService:

    def query_by_name(self, player_name):
        player = find_player(player_name)
        if not player:
            return False, "未找到该选手"

        ret = {"player_name": player.player_name}
        # 内战胜率
        match_details = query_match_details(player.player_id)
        if not match_details:
            return False, "无内战信息"

        ret['match_count'] = len(match_details)
        ret['win_percent'] = round(len([m for m in match_details if m.win]) * 100 / len(match_details), 2)
        ret['mvp_count'] = len([m for m in match_details if m.mvp])
        ret['svp_count'] = len([m for m in match_details if m.svp])
        ret['kda'] = self.calculate_kda(match_details)
        ret['damage_trans'] = self.calculate_damage_trans(match_details)
        return True, ret
    #
    # def calculate_kda(self, match_details):
    #     total_kda = 0
    #     for m in match_details:
    #         total_kda += (m.kill + m.assist) / (m.death or 1)
    #     return round(total_kda / len(match_details), 2)

    def calculate_kda(self, match_details):
        total_kill = total_assist = total_death = 0
        for m in match_details:
            total_kill += m.kill
            total_assist += m.assist
            total_death += m.death
        return round((total_kill + total_assist) / (total_death or 0), 2)

    def calculate_damage_trans(self, match_details):
        total_percent = 0
        for m in match_details:
            total_percent += m.champion_damage_percent / m.gold_earned_percent
        return round(total_percent * 100 / len(match_details), 2)


class PartnerWinService:
    def __init__(self, base_player_name, partner_player_name):
        self.base_player_name = base_player_name
        self.partner_player_name = partner_player_name

    def win_info(self):
        base_player = find_player(self.base_player_name)
        if not base_player:
            return False, "未找到该选手"
        partner_player = find_player(self.partner_player_name)
        if not partner_player:
            return False, "未找合作选手"

        matches = query_matches_by_players(player_ids=[base_player.player_id, partner_player.player_id])
        if not matches:
            return False, "未找到合作信息"

        base_match_details = query_match_details(player_id=base_player.player_id, match_ids=[m.match_id for m in matches])
        if not base_match_details:
            return False, "未找到合作信息"

        partner_match_details = query_match_details(player_id=partner_player.player_id, match_ids=[m.match_id for m in matches])
        if not partner_match_details:
            return False, "未找到合作信息"

        # 筛选出队友的数据
        partner_match_dict = {m.match_id: m.team_id for m in partner_match_details}

        match_details = [m for m in base_match_details if partner_match_dict.get(m.match_id) == m.team_id]
        win_count = len([m for m in match_details if m.win])
        win_percent = int(round(win_count * 100 / len(match_details), 2))
        return True, {"win_count": win_count, "match_count": len(match_details), "win_percent": win_percent}


class PlayerRankService:
    def rank_list(self):
        match_details = query_match_details()
        player_match_dict = dict()
        for md in match_details:
            player_match_dict.setdefault(md.player_id, []).append(md)

        ret = []
        for k, v in player_match_dict.items():
            total_count = len(v)
            # if total_count < 10:
            #     continue
            win_count = len([m for m in v if m.win])
            win_percent = round(win_count * 100 / total_count, 2)
            ret.append(
                {"player_name": find_player_by_id(k).player_name, "total_count": total_count, "win_count": win_count, "win_percent": win_percent})
        ret = sorted(ret, key=lambda x: x['win_percent'], reverse=True)
        return True, {"rank_list": ret}
