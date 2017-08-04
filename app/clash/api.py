import concurrent.futures
from urllib.parse import quote

import os
import logging
import requests

token = os.getenv('API_TOKEN')
headers = {'authorization': 'Bearer ' + token}
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def __get_with_threads(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        return list(executor.map(lambda url: requests.get(url, headers=headers), urls))


def find_clan_by_tag(tag):
    logger.info(f"Fetching clan from API {tag}.")
    return requests.get('https://api.clashofclans.com/v1/clans/' + quote(tag), headers=headers).json()


def fetch_all_players(clan):
    logger.info(f"Fetching all player stats for {clan['tag']}.")
    tags = [member['tag'] for member in clan['memberList']]
    urls = ['https://api.clashofclans.com/v1/players/' + quote(tag) for tag in tags]
    return __get_with_threads(urls)
