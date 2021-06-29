import sys
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from utils import *


class WanplusDataManager(object):
    """ Data Manager for wanplus.com. 
        Data from this site mainly focus on pro matches / tournaments.
    """
    
    def __init__(self):
        """ Initiate attributes. """
        # load all configuration files (paths, headers, etc.)
        self.configs = load_json('../data/constants/config.json')
        self.columns_ref = load_json(self.configs['wanplus_df_path'])

    def get_data(self, eid='870', mode='player', source='remote'):
        """ Get data from wanplus.com. 
        Params:
            eid: str, event id.
            mode: str, 'team', 'player', or 'hero'.
            source: str, 'remote' or 'local'.
        Returns: a Python dict, res['data'] is data.
        """
        data_path = f'../data/tournaments/{mode}/{eid}.json'
        if source == 'remote':
            # load request parameters for posting
            ajax_params = load_json(self.configs[f'wanplus_{mode}_path'])
            url = ajax_params['url']
            headers = ajax_params['headers']
            data = ajax_params['data']
            data['eid'] = eid
            try:  # catch exceptions while requesting
                res = requests.post(url=url, data=data, headers=headers).json()
                time.sleep(1)
            except Exception as e:
                print(f"Something wrong happened: {e} ")
                sys.exit()
            if mode == 'hero':  # data structure is different
                data = res['data']['stateList']
                event_list = res['data']['eventList']
            else:
                data, event_list = res['data'], res['eventList']
            save_json(data, data_path)  # update local data
            print(f"Remote data loaded and saved to {data_path} ")
            return data, event_list
        elif source == 'local':
            print("Local data loaded. ")
            return load_json(data_path)
        else:
            print("Wrong source type. Exiting... ")
            sys.exit()

    def get_team_data(self, eid='870', source='remote'):
        """ Get Pandas DataFrame data of teams from wanplus.com. 
        Params:
            eid: str, event id.
            source: str, 'remote' or 'local'.
        Returns: pre_team_df: a preprocessed Pandas DataFrame object.
        """
        res = self.get_data(eid=eid, mode='team', source=source)
        data = res[0] if source == 'remote' else res
        data_dic = {team['teamname']: team for team in data}
        # convert to Pandas DataFrame
        team_df = pd.DataFrame.from_dict(data_dic, orient='index')
        # choose cols and set new col names
        team_cols = self.columns_ref['team_cols']
        team_new_cols = self.columns_ref['team_new_cols']
        team_df = team_df[team_cols]
        team_df.columns = team_new_cols
        # convert to float
        pre_team_df = team_df.applymap(lambda x: get_float(x))
        return pre_team_df

    def get_player_data(self, eid='870', pos='TOP', source='remote'):
        """ Get Pandas DataFrame data of players from wanplus.com. 
        Params:
            eid: str, event id.
            pos: str, player position
            source: str, 'remote' or 'local'.
        Returns: pre_player_df: a preprocessed Pandas DataFrame object.
        """
        res = self.get_data(eid=eid, mode='player', source=source)
        data = res[0] if source == 'remote' else res
        data_dic = {player['playername']: player for player in data}
        # convert to Pandas DataFrame
        player_df = pd.DataFrame.from_dict(data_dic, orient='index')
        # choose cols and set new col names
        player_cols = self.columns_ref['player_cols']
        player_new_cols = self.columns_ref['player_new_cols']
        player_df = player_df[player_cols]
        player_df.columns = player_new_cols
        # convert position names from Chinese to English
        player_df['pos'] = player_df['pos'].map(lambda x: convert_pos(x))
        # get corresponding team win rate
        team_df = self.get_team_data(eid=eid, source=source)
        player_df['teamname'] = player_df['teamname'].map(
            lambda x: team_df.loc[x, 'win_rate'])
        player_df.rename(columns={'teamname': 'win_rate'}, inplace=True)
        # choose postition and then drop that column
        player_df = player_df[player_df['pos']==pos].drop(columns=['pos'])
        # convert to float
        pre_player_df = player_df.applymap(lambda x: get_float(x))
        return pre_player_df

    def get_hero_data(self, eid='870', pos='TOP', source='remote'):
        """ Get Pandas DataFrame data of heroes from wanplus.com. 
        Params:
            eid: str, event id.
            pos: str, player position
            source: str, 'remote' or 'local'.
        Returns: hero_df: a preprocessed Pandas DataFrame object.
        """
        res = self.get_data(eid=eid, mode='hero', source=source)
        data = res[0] if source == 'remote' else res
        data_dic = {hero['cpherokey']: hero for hero in data}
        # convert to DataFrame
        hero_df = pd.DataFrame.from_dict(data_dic, orient='index')
        # choose and set new cols
        hero_cols = self.columns_ref['hero_cols']
        hero_new_cols = self.columns_ref['hero_new_cols']
        hero_df = hero_df[hero_cols]
        hero_df.columns = hero_new_cols
        return hero_df

    def update_all(self):
        """ Update events to local for analysis. """
        event_path = self.configs['wanplus_event_path']
        save_json(self.get_data()[1], event_path)  # update events
        event_data = load_json(event_path)
        # for k, v in list(event_data.items()):  # update all events
        for k, v in list(event_data.items())[:5]:  # update recent events
            self.get_data(eid=v['eid'], mode='team', source='remote')
            self.get_data(eid=v['eid'], mode='player', source='remote')
            self.get_data(eid=v['eid'], mode='hero', source='remote')
        print("Local data updated. ")


if __name__ == '__main__':
    wanplus = WanplusDataManager()
    # wanplus.update_all()
    # pre_df = wanplus.get_team_data(eid='870', source='local')
    pre_df = wanplus.get_player_data(eid='870', pos='MID', source='local')
    std_df = get_std_df(pre_df)
    print(get_key_factors(df=std_df, measure='win_rate'))
    # pre_df = wanplus.get_hero_data(source='local')
    # print(pre_df)
