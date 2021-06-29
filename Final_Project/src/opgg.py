import sys
import time
import requests
from bs4 import BeautifulSoup
from utils import load_json, save_json, get_champion


class OPGGDataManager(object):
    """ Data Manager for op.gg.com. """

    def __init__(self):
        """ Initiate attributes. """
        self.configs = load_json('../data/constants/config.json')
        self.ajax_params = load_json(self.configs['opgg_c_rank_path'])

    def get_summoner(self, platform=None, sname=None):
        """ Get summoner information from op.gg.com. 
        Params:
            platform: str, platform name.
            sname: str, summoner name.
        Returns:
            soup: BeautifulSoup object, containing summoner's information.
        """
        if platform not in ('NA', 'KR'):
            print("Platform must be NA or KR. Exiting ... ")
            sys.exit()
        if not sname:
            print('Null summoner name. Exiting ... ')
            sys.exit()
        host = 'na.op.gg' if platform == 'NA' else 'www.op.gg'
        ep = f'/summoner/userName={sname}'
        try:  # catch exceptions while requesting
            res = requests.get(url='https://'+host+ep)
            time.sleep(1)
        except Exception as e:
            print(f"Something wrong happened: {e} ")
            sys.exit()
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def get_champion_positions(self, c_id=None):
        """ Get champion positions. 
        Params: c_id: str, champion id (simplified name). 
        Returns: list, champion positions.
        """
        if not c_id:
            print("Champion id is needed. ")
            sys.exit()
        url = 'https://na.op.gg/champion/statistics'
        try:  # catch exceptions while requesting
            res = requests.get(url=url)
            time.sleep(1)
        except Exception as e:
            print(f"Something wrong happened: {e} ")
            sys.exit()
        soup = BeautifulSoup(res.text, 'lxml')
        champion = soup.find('div', {'data-champion-key': c_id})
        pos_class = 'champion-index__champion-item__positions'
        positions = champion.find('div', {'class': pos_class})
        return [pos.text.lower() for pos in positions.findAll('div')]

    def get_champion_counters(self, c_name=None, source='remote'):
        """ Get the counters of a certain champion. 
        Params:
            c_name: str, champion name.
            source: str, data location, remote or local.
        Returns: list, counters of the champion.
        """
        if not c_name:
            print("Champion name is needed. ")
            sys.exit()
        if source == 'remote':
            c_id = get_champion(c_name=c_name)['id'].lower()
            counters_data = {}
            for pos in self.get_champion_positions(c_id):
                # c_id = c_id.lower()
                try:  # catch exceptions while requesting
                    res = requests.get(
                        f'https://na.op.gg/champion/{c_id}/statistics/{pos}')
                    time.sleep(1)
                except Exception as e:
                    print(f"Something wrong happened: {e} ")
                    sys.exit()
                soup = BeautifulSoup(res.text, 'lxml')
                # parse html to get champion counters
                strong_class = 'champion-stats-header-matchup__table ' + \
                    'champion-stats-header-matchup__table--strong tabItem'
                weak_class = 'champion-stats-header-matchup__table ' + \
                    'champion-stats-header-matchup__table--weak tabItem'
                strong_soup = soup.find('table', {'class': strong_class})
                strong_champions = {}
                for champion_soup in strong_soup.tbody.findAll('tr'):
                    tds = champion_soup.findAll('td')
                    c_id = tds[0].text.strip()
                    win_ratio = tds[1].find('b').text.strip()
                    strong_champions[c_id] = win_ratio
                weak_soup = soup.find('table', {'class': weak_class})
                weak_champions = {}
                for champion_soup in weak_soup.tbody.findAll('tr'):
                    tds = champion_soup.findAll('td')
                    c_id = tds[0].text.strip()
                    win_ratio = tds[1].find('b').text.strip()
                    weak_champions[c_id] = win_ratio
                counters_data[pos] = {}
                counters_data[pos]['strong'] = strong_champions
                counters_data[pos]['weak'] = weak_champions
            print("Remote data loaded. ")
            return counters_data
        elif source == 'local':
            data = load_json(self.configs['champion_counters_path'])[c_name]
            print("Local data loaded. ")
            return data
        else:
            print(f"Wrong source type: {source} ")
            sys.exit()

    def get_champion_ranks(self, data_save_path, tier='gold', source='remote'):
        """ Get recent (weekly) champion ranks according to tiers. 
        Params:
            data_save_path: str, the path to save retrieved data.
            tier: str, also called 'league', current stage for ranking.
            source: str, remote or local, where to retrieve data.
        Returns: dictionary of champions.
        """
        if not data_save_path:
            print("The path of data must be given. ")
            sys.exit()
        if source == 'remote':
            self.ajax_params = load_json(self.configs['opgg_c_rank_path'])
            url = 'https://na.op.gg/statistics/ajax2/champion/'
            headers = self.ajax_params['headers']
            data = self.ajax_params['data']
            data['league'] = tier
            try:  # catch exceptions while requesting
                res = requests.post(url=url, data=data, headers=headers)
                time.sleep(1)
            except Exception as e:
                print(f"Something wrong happened: {e} ")
                sys.exit()
            c_soup = BeautifulSoup(res.text, 'lxml')
            c_dic = {}
            for tr in c_soup.tbody.findAll('tr'):
                c_name = tr.find('td', {'class': 'Cell ChampionName'}).text
                c_rank = tr.find('td', {'class': 'Cell Rank'}).text
                w_ratio = tr.find('span', {'class': 'Value'}).text
                c_dic[c_name.strip()] = {'rank': c_rank, 'win_ratio': w_ratio}
            save_json(c_dic, data_save_path)
            print(f"Remote data loaded and saved to {data_save_path} ")
            return c_dic
        elif source == 'local':
            data = load_json(data_save_path)
            print("Local data loaded. ")
            return data
        else:
            print(f"Wrong source type: {source} ")
            sys.exit()

    def update_champion_ranks(self, data_save_path='../data/champion-ranks'):
        """ Update all recent champion ranks for each tier. 
        Params: data_save_path: str, path to save data.
        """  
        for tier in (
            'iron', 'bronze', 'silver', 'gold', 'platium', 'diamond',
            'master', 'grandmaster', 'challenger'
        ):
            self.get_champion_ranks(data_save_path+f'/{tier}.json', tier)

    def update_champion_counters(
            self, data_save_path='../data/championCounters.json'):
        """ Update all recent champion counters of all champions. 
        Params: data_save_path: str, path to save data.
        """
        data = {}
        c_path = '../data/dragontail-9.24.2/9.24.2/data/en_US/champion.json'
        champion_ref = load_json(c_path)
        for champion in champion_ref['data'].values():
            c_name = champion['name']
            data[c_name] = self.get_champion_counters(c_name)
        save_json(data, data_save_path)
        print(f"Remote data saved to {data_save_path} ")


if __name__ == '__main__':
    opgg = OPGGDataManager()
    opgg.update_champion_ranks()
    opgg.update_champion_counters()
