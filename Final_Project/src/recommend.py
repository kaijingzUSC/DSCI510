import sys
import time
import argparse
import numpy as np
from utils import *
from riot import RiotDataManager
from wanplus import WanplusDataManager
from opgg import OPGGDataManager


class Recommendation(object):
    """ Recommendation System for Skill Improvements. 
        Recommendation for players is completed, since recommendation for
        teams requires the data from wanplus.com and the composition is quite
        hard, still developing...
    """
    def __init__(self):
        self.riot = RiotDataManager()
        self.opgg = OPGGDataManager()
        self.wanplus = WanplusDataManager()

    def recommend_for_ranks(
            self, platform=None, sname=None,
            data_save_path='../data/champion-ranks', 
            in_detail=True, source='remote'):
        if not (platform and sname):
            print("Platform and summoner name must be given. Exiting... ")
            sys.exit()
        # print("Processing... ")
        # use riot data manager to parse summoner information
        self.riot.connection_test()
        summoner_info = self.riot.get_summoner(platform, sname)
        sid = summoner_info['id']
        # use encrypted summoner id to retrieve top 5 champions played
        top_champions = self.riot.get_mastery(platform, sid)[:5]
        # load local champion basic information for reference
        champion_ref = load_json(self.riot.configs['champion_search_path'])
        top_cnames = []
        # get names from reference (id --> name)
        for t_champion in top_champions:
            for champion in champion_ref['data'].values():
                if champion['key'] == str(t_champion['championId']):
                    top_cnames.append(champion['name'])
        league = self.riot.get_leagues(platform, sid)[0]
        tier, rank = league['tier'], league['rank']
        # use opgg data manager to retrieve champion ranking data
        champion_ranks = self.opgg.get_champion_ranks(
            data_save_path+f'/{tier.lower()}.json', tier.lower(), source)
        # get top 5 over-power champions in this tier
        op_champions = sorted(
            champion_ranks.items(), key=lambda x: int(x[1]['rank']))[:5]
        top_champions_dic = {i: {} for i in top_cnames}
        for c_name, c_body in champion_ranks.items():
            if c_name in top_cnames:
                top_champions_dic[c_name]['rank'] = c_body['rank']
                top_champions_dic[c_name]['win_ratio'] = c_body['win_ratio']
        # print(top_champions_dic)
        # get champion recommendation
        best_c = max(
            top_champions_dic.items(), key=lambda x: x[1]['rank'])[0]

        print(f"Summoner name: {sname}, Rank: {tier+' '+rank}")

        print(f"Most skillful champions: {top_cnames if in_detail else ''} ")
        img_dir = self.riot.configs['champion_img_path']
        top_ids = [get_champion(c_name=i)['id'] for i in top_cnames]
        show_img(img_dir, top_ids)

        print(f"Current patch best champion: {best_c if in_detail else ''} ")
        show_img(img_dir, get_champion(c_name=best_c)['id'])

        print(f"{best_c}'s current average winning ratio in {tier}: ")
        print(f"{top_champions_dic[best_c]['win_ratio']}. ")

        print("For different positions: ")
        counters_data = self.opgg.get_champion_counters(best_c, source)
        for pos in counters_data:
            print(f"[Position {pos}]: ")
            print(f"{best_c} is countered by: ")
            strongs = counters_data[pos]['strong']
            print(strongs if in_detail else '')
            strongs = [
                get_champion(c_name=i)['id'] for i in list(strongs.keys())]
            show_img(img_dir, strongs)

            print(f"Besides, {best_c} performs well against: ")
            weaks = counters_data[pos]['weak'] 
            print(weaks if in_detail else '')
            weaks = [
                get_champion(c_name=i)['id'] for i in list(weaks.keys())]
            show_img(img_dir, weaks)

        print(f"Also, {sname} can try champions with high winning ratios: ")
        print(op_champions if in_detail else '')
        show_img(
            img_dir,
            [get_champion(c_name=cp)['id'] for cp, data in op_champions])

    def recommend_for_teams(self, eid='870', source='remote'):
        """ Developing... """
        print(f"The winning factors will be listed according to event {eid}. ")
        pre_team_df = self.wanplus.get_team_data(eid=eid, source=source)
        std_team_df = get_std_df(pre_team_df)
        team_key_factors = get_key_factors(std_team_df, 'win_rate')
        print("The weights of team factors related to winning: ")
        print(team_key_factors.to_frame())
        pie_factors(team_key_factors, 'Team Winning Keys')

        for pos in ['TOP', 'JUG', 'MID', 'BOT', 'SUP']:
            pre_player_df = self.wanplus.get_player_data('870', pos, source)
            std_player_df = get_std_df(pre_player_df)
            player_key_factors = get_key_factors(std_player_df, 'win_rate')
            print(f"The weights of position {pos} factors related to winning: ")
            print(player_key_factors.to_frame())
            pie_factors(player_key_factors, f'{pos} Winning Keys')

        print("The factors above are important and worth paying attention.")
        

# completed, milestone 3
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-source", "--source", type=str,
        help="data source, remote or local", default='remote')
    parser.add_argument(
        "-inter", "--interactive", type=str,
        help="enable interactive mode, yes or no", default='no')
    args = parser.parse_args()
    if args.source not in ('remote', 'local', 'test'):
        print("Invalid arguments for 'source'. Exiting... ")
        sys.exit()
    if args.interactive not in ('yes', 'no'):
        print("Invalid arguments for 'interactive'. Exiting... ")
        sys.exit()
    if args.source == 'test':
        args.source = 'remote'

    func_dic = {'0': 'For Ranks', '1': 'For Teams'}
    func_n = '1'
    if args.interactive == 'yes':
        while True:
            print(f"Current functions: {func_dic}. ")
            func_n = input("Input what you want to do (0 or 1): ")
            if func_n in ('0', '1'):
                print(f"Your choice: {func_dic[func_n]}. ")
                break

    rec = Recommendation()
    if func_n == '0':
        pf = 'KR'
        sname = 'The shy'
        if args.interactive == 'yes':
            rec.riot.show_platforms()
            pf = input("Input platform: ")
            sname = input("Input summoner name: ")
        rec.recommend_for_ranks(platform=pf, sname=sname, source=args.source)
        # rec.recommend_for_ranks(platform=pf, sname=sname, source='local')
    else:
        rec.recommend_for_teams(eid='870', source=args.source)
        # rec.recommend_for_teams(eid='870', source='local')
