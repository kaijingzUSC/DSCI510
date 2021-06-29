import sys
import time
import requests
import json
from bs4 import BeautifulSoup
from utils import load_json, save_json


class RiotDataManager(object):
    """ Data Manager for Riot Games API. 
        Note that since the data from Riot Games are huge and need API KEY,
        besides, the research is highly summoner-related, so it is hard to 
        decide what kind of data to retrieve without provided information, so
        these data are not stored locally. But there are some fixed data every
        game patch, and all of them are already downloaded from the developers'
        site of Riot Games for reference.
    """
    
    def __init__(self):
        """ Initiate attributes. """
        # load all configuration files (paths, headers, etc.)
        self.configs = load_json('../data/constants/config.json')
        # api key is a must for access to riot games api
        self.headers = {'X-Riot-Token': self.configs['API_KEY']}
        # test connection
        # self.connection_test()

    def connection_test(self):
        """ Connection test. 
            Check whether Riot API Key is valid by requesting.
        """
        host = self.get_host('NA1')
        ep = self.get_eps()['rotations']
        try:  # catch exceptions while requesting
            res = requests.get('https://'+host+ep, headers=self.headers)
            time.sleep(1)
        except Exception as e:
            print(f"Something wrong happened: {e} ")
            sys.exit()
        wrong_msgs = [
            {'status': {'message': 'Unauthorized', 'status_code': 401}},
            {'status': {'message': 'Forbidden', 'status_code': 403}}
        ]
        if json.loads(res.text) in wrong_msgs:
            print("Invalid API Key, please contact the author. ")
            return False
        print("Connection test passed. ")
        return True

    def set_api_key(self, api_key):
        """ Update API key for Riot Games API and test connection. 
        Params: api_key: str, Riot Games API Key.
        """
        if type(api_key) is not str:
            print("API Key must be string. Exiting... ")
            sys.exit()
        self.headers = {'X-Riot-Token': api_key}
        if not self.connection_test():
            self.headers = {'X-Riot-Token': self.configs['API_KEY']}
            print("New API Key aborted, old verison resumed.")
        else:
            self.configs['API_KEY'] = api_key
            save_json(self.configs, '../data/constants/config.json')
            print("API Key updated. ")

    def get_platforms(self):
        """ Get all available platforms from local. 
        Returns: platforms dictionary.
        """
        return load_json(self.configs['platforms_path'])

    def show_platforms(self):
        """ Print all available platforms and their hosts. """
        print("Available platforms and hosts: ")
        for plat_host in self.get_platforms():
            print(plat_host['platform'], "--", plat_host['host'])

    def get_host(self, platform):
        """ Get host name according to platform name. 
        Params: platform: str, platform name.
        Returns: str, host name.
        """
        for plat_host in self.get_platforms():
            if plat_host['platform'] == platform:
                return plat_host['host']
        print("Wrong shortcut for the platform. ")
        sys.exit()

    def get_eps(self):
        """ Get available endpoints from local. 
        Returns: endpoints dictionary.
        """
        return load_json(self.configs['endpoints_path'])

    def show_endpoints(self):
        """ Print all available endpoints. """
        print("Available endpoints: ")
        for k, v in self.get_eps().items():
            print(k, "--", v)

    def get_summoner(self, platform=None, sname=None):
        """ Get summoner basic information. 
        Params:
            platform: str, platform name.
            sname: str, summoner name.
        Returns: dictionary (usually).
        """
        if not (platform and sname):
            print("Platform and summoner name are needed. ")
            sys.exit()
        host = self.get_host(platform)
        ep = self.get_eps()['sname'].format(summonerName=sname)
        try:  # catch exceptions while requesting
            res = requests.get(url='https://'+host+ep, headers=self.headers)
            time.sleep(1)
        except Exception as e:
            print(f"Something wrong happened: {e} ")
            sys.exit()
        return res.json()

    def get_mastery(self, platform=None, sid=None, cid=None):
        """ Get summoner's champion mastery. 
        Params:
            platform: str, platform name.
            sid: str, encrypted summoner id by riot games.
            cid: str, champion id.
        Returns: dictionary (usually).
        """
        if not platform:
            print("Platform name are needed. ")
            sys.exit()
        host = self.get_host(platform)
        if cid and sid:
            ep = self.get_eps()['mastery_sid_cid'].format(
                encryptedSummonerId=sid, championId=cid)
        elif sid:
            ep = self.get_eps()['mastery_sid'].format(encryptedSummonerId=sid)
        else:
            print("Please provide sid+cid or sid. ")
            sys.exit()
        try:  # catch exceptions while requesting
            res = requests.get(url='https://'+host+ep, headers=self.headers)
            time.sleep(1)
        except Exception as e:
            print(f"Something wrong happened: {e} ")
            sys.exit()
        return res.json()

    def get_leagues(
        self, platform=None, sid=None, lid=None,
        queue=None, tier=None, div=None):
        """ Get league information of a summoner. 
        Params:
            platform: str, platform name.
            sid: str, encrypted summoner id by riot games.
            lid: str, encrypted league id by riot games.
            queue: str, queue type.
            tier: str, tier name.
            div: str, division name / rank name.
        Returns: dictionary (usually).
        """
        if not platform:
            print("Platform name are needed. ")
            sys.exit()
        host = self.get_host(platform)
        if sid:
            ep = self.get_eps()['league_sid'].format(encryptedSummonerId=sid)
        elif lid:
            ep = self.get_eps()['league_lid'].format(leagueId=lid)
        elif queue and tier and div:
            ep = self.get_eps()['league'].format(
                queue=queue, tier=tier, division=div)
        else:
            print('Wrong argument format. ')
            sys.exit()
        try:  # catch exceptions while requesting
            res = requests.get(url='https://'+host+ep, headers=self.headers)
            time.sleep(1)
        except Exception as e:
            print(f"Something wrong happened: {e} ")
            sys.exit()
        return res.json()

    def get_matches(self, platform=None, aid=None, mid=None, timeline=False):
        """ Get match information. 
        Params:
            platform: str, platform name.
            aid: str, encrypted account id by riot games.
            mid: str, match id.
            timeline: boolean, wheter get match timeline.
        Returns: dictionary (usually).
        """
        if not platform:
            print("Platform name are needed. ")
            sys.exit()
        host = self.get_host(platform)
        if aid:
            ep = self.get_eps()['matches_aid'].format(encryptedAccountId=aid)
        elif mid and timeline:
            ep = self.get_eps()['timeline_mid'].format(matchId=mid)
        elif mid:
            ep = self.get_eps()['match_mid'].format(matchId=mid)
        else:
            print('Wrong argument format. ')
            sys.exit()
        try:  # catch exceptions while requesting
            res = requests.get(url='https://'+host+ep, headers=self.headers)
            time.sleep(1)
        except Exception as e:
            print(f"Something wrong happened: {e} ")
            sys.exit()
        return res.json()


if __name__ == '__main__':
    riot = RiotDataManager()
    # riot.set_api_key('RGAPI-6cc01f9e-fae0-46ec-905b-74e7dffaaeee')
    # riot.set_api_key('1222')
    riot.connection_test()
    # summoner = riot.get_summoner('NA1', 'ReWr1Teee2333')
    # league = riot.get_leagues('NA1', summoner['id'])
    # mastery = riot.get_mastery('NA1', summoner['id'])
    # matches = riot.get_matches('NA1', summoner['accountId'])
    # print(league)
    # print(mastery)
    # print(matches)
