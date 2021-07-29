from __future__ import annotations

import asyncio
import logging
import os
from typing import List
from urllib.parse import quote

import aiohttp
import requests
from async_timeout import timeout

logger = logging.getLogger(__name__)


def headers():
    return dict(authorization=f"Bearer {os.getenv('API_TOKEN')}")


class ApiException(Exception):
    pass


class ClanNotFound(ApiException):
    pass


class WarNotFound(ApiException):
    pass


class PlayerNotFound(ApiException):
    pass


class TooManyRequests(ApiException):
    pass


class ApiTimeout(ApiException):
    pass


async def __fetch(url, params=None, loop=None):
    async with aiohttp.ClientSession(loop=loop, cookie_jar=aiohttp.DummyCookieJar(), headers=headers()) as session:
        return await __fetch_with_session(url, session=session, params=params)


async def __fetch_with_session(url, session, params=None):
    async with timeout(8):
        async with session.get(url, params=params) as response:
            data = await response.json()
            return response.status, data


async def __fetch_all(urls, loop=None):
    async with timeout(8):
        async with aiohttp.ClientSession(loop=loop, cookie_jar=aiohttp.DummyCookieJar(), headers=headers()) as session:
            futures = [__fetch_with_session(url, session) for url in urls]
            responses = await asyncio.gather(*futures)

            return [response for status, response in responses if status == 200]


def find_clan_by_tag(tag):
    tag = prepend_hash(tag)
    logger.info(f"Fetching clan from API {tag}.")

    future = __fetch(f"https://api.clashofclans.com/v1/clans/{quote(tag)}")

    try:

        code, response = asyncio.get_event_loop().run_until_complete(future)
    except asyncio.TimeoutError:
        raise ApiTimeout(f"API timed while fetching {tag} clan.")

    if code == 404:
        raise ClanNotFound(f"Clan [{tag}] not found.")

    if code == 429:
        raise TooManyRequests(f"Too many requests when fetching clan [{tag}].")

    if code != 200:
        raise ApiException(f"API returned non-200 status code: {code}")

    return response


def find_player_by_tag(tag):
    tag = prepend_hash(tag)
    logger.info(f"Fetching player from API {tag}.")

    future = __fetch(f"https://api.clashofclans.com/v1/players/{quote(tag)}")

    try:
        code, response = asyncio.get_event_loop().run_until_complete(future)
    except asyncio.TimeoutError:
        raise ApiTimeout(f"API timed while fetching {tag} clan.")

    if code == 404:
        raise PlayerNotFound(f"Player [{tag}] not found.")

    if code == 429:
        raise TooManyRequests(f"Too many requests when fetching clan [{tag}].")

    if code != 200:
        raise ApiException(f"API returned non-200 status code: {code}")

    return response


def search_by_name(name, limit=10):
    logger.info(f"Searching for clan name '{name}'.")
    future = __fetch("https://api.clashofclans.com/v1/clans", params={"name": name, "limit": limit})
    code, response = asyncio.get_event_loop().run_until_complete(future)

    if code != 200:
        return []
    else:
        return response["items"]


def top_players_and_clan():
    data = requests.get("https://clashofclans.com/api/leaderboards.json").json()
    leaderboards = data["hallOfFame"]["leaderboards"]
    players = leaderboards["topPlayers"]["players"]
    clans = leaderboards["topClans"]["clans"]
    return players, clans


def clan_warlog(tag):
    tag = prepend_hash(tag)
    logger.info(f"Fetching clan warlog from API {tag}.")
    future = __fetch(f"https://api.clashofclans.com/v1/clans/{quote(tag)}/warlog")
    code, response = asyncio.get_event_loop().run_until_complete(future)

    if code != 200:
        raise ClanNotFound(f"Clan [{tag}] not found.")

    return response


def clan_current_leaguegroup(tag):
    tag = prepend_hash(tag)
    logger.info(f"Fetching clan current leaguegroup from API {tag}.")
    future = __fetch(f"https://api.clashofclans.com/v1/clans/{quote(tag)}/currentwar/leaguegroup")
    code, response = asyncio.get_event_loop().run_until_complete(future)

    if code != 200:
        raise WarNotFound(f"Clan leaguegroup [{tag}] not found.")

    return response


def clan_current_war(tag):
    tag = prepend_hash(tag)
    logger.info(f"Fetching clan current war from API {tag}.")
    future = __fetch(f"https://api.clashofclans.com/v1/clans/{quote(tag)}/currentwar")
    code, response = asyncio.get_event_loop().run_until_complete(future)

    if code != 200:
        raise WarNotFound(f"War for clan [{tag}] not found.")

    return response


def cwl_war_by_tag(tag):
    tag = prepend_hash(tag)
    logger.info(f"Fetching war from API with {tag}.")
    future = __fetch(f"https://api.clashofclans.com/v1/clanwarleagues/wars/{quote(tag)}")
    code, response = asyncio.get_event_loop().run_until_complete(future)

    if code != 200:
        raise WarNotFound(f"War [{tag}] not found.")

    return response


def fetch_all_players(tags: List):
    urls = ["https://api.clashofclans.com/v1/players/" + quote(tag) for tag in tags]
    future = __fetch_all(urls, loop=asyncio.get_event_loop())
    return asyncio.get_event_loop().run_until_complete(future)


def prepend_hash(tag):
    return "#" + tag.lstrip("#").upper()
