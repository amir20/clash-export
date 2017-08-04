import concurrent.futures
from urllib.parse import quote

import os
import requests

token = os.getenv('API_TOKEN')
headers = {'authorization': 'Bearer ' + token}


def __get_with_threads(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        return list(executor.map(lambda url: requests.get(url, headers=headers), urls))


def find_clan_by_tag(tag):
    return requests.get('https://api.clashofclans.com/v1/clans/' + quote(tag), headers=headers).json()


def fetch_all_players(clan):
    tags = [member['tag'] for member in clan['memberList']]
    urls = ['https://api.clashofclans.com/v1/players/' + quote(tag) for tag in tags]
    return __get_with_threads(urls)
