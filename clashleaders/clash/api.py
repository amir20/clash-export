import asyncio
import logging
import os
from urllib.parse import quote

import aiohttp

API_TOKEN = os.getenv('API_TOKEN')
HEADERS = dict(authorization='Bearer ' + API_TOKEN)
logger = logging.getLogger(__name__)


class ClanNotFound(Exception):
    pass


async def __fetch(url, params=None, loop=None):
    with aiohttp.ClientSession(loop=loop, cookie_jar=aiohttp.DummyCookieJar(), headers=HEADERS) as session:
        return await __fetch_with_session(url, session=session, params=params)


async def __fetch_with_session(url, session, params=None):
    async with aiohttp.Timeout(2):
        async with session.get(url, params=params) as response:
            data = await response.json()
            return response.status, data


def __fetch_all(urls, loop=None):
    with aiohttp.ClientSession(loop=loop, cookie_jar=aiohttp.DummyCookieJar(), headers=HEADERS) as session:
        futures = [__fetch_with_session(url, session) for url in urls]
        responses = loop.run_until_complete(asyncio.gather(*futures))

        return [response for status, response in responses if status == 200]


def find_clan_by_tag(tag):
    tag = "#" + tag.lstrip("#")
    logger.info(f"Fetching clan from API {tag}.")

    future = __fetch(f'https://api.clashofclans.com/v1/clans/{quote(tag)}')
    code, response = asyncio.get_event_loop().run_until_complete(future)

    if code != 200:
        raise ClanNotFound(f"Clan [{tag}] not found.")

    return response


def search_by_name(name, limit=10):
    logger.info(f"Searching for clan name '{name}'.")
    future = __fetch('https://api.clashofclans.com/v1/clans', params={'name': name, 'limit': limit})
    code, response = asyncio.get_event_loop().run_until_complete(future)

    if code != 200:
        return []
    else:
        return response['items']


def clan_warlog(tag):
    tag = "#" + tag.lstrip("#")
    logger.info(f"Fetching clan warlog from API {tag}.")
    future = __fetch(f"https://api.clashofclans.com/v1/clans/{quote(tag)}/warlog")
    code, response = asyncio.get_event_loop().run_until_complete(future)

    if code != 200:
        raise ClanNotFound(f"Clan [{tag}] not found.")

    return response


def fetch_all_players(clan):
    logger.info(f"Fetching all player stats for {clan['tag']}.")
    tags = [member['tag'] for member in clan['memberList']]
    urls = ['https://api.clashofclans.com/v1/players/' + quote(tag) for tag in tags]
    return __fetch_all(urls, loop=asyncio.get_event_loop())
