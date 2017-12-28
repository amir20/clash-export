import asyncio
import logging
from urllib.parse import quote

import aiohttp
import os
import requests

token = os.getenv('API_TOKEN')
headers = {'authorization': 'Bearer ' + token}
logger = logging.getLogger(__name__)


class ClanNotFound(Exception):
    pass


async def __fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


def __get_all(urls):
    loop = asyncio.get_event_loop()
    futures = [__fetch(url) for url in urls]
    responses = loop.run_until_complete(asyncio.gather(*futures))
    return responses


def find_clan_by_tag(tag):
    if not tag.startswith('#'):
        tag = '#' + tag
    logger.info(f"Fetching clan from API {tag}.")
    r = requests.get('https://api.clashofclans.com/v1/clans/' + quote(tag), headers=headers)

    if r.status_code != 200:
        raise ClanNotFound('Clan not found')

    return r.json()


def search_by_name(name):
    logger.info(f"Searching for clan name {name}.")
    r = requests.get('https://api.clashofclans.com/v1/clans', headers=headers, params={'name': name})
    return r.json()


def fetch_all_players(clan):
    logger.info(f"Fetching all player stats for {clan['tag']}.")
    tags = [member['tag'] for member in clan['memberList']]
    urls = ['https://api.clashofclans.com/v1/players/' + quote(tag) for tag in tags]
    return __get_all(urls)
