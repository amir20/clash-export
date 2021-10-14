from __future__ import annotations

import asyncio
import json
from datetime import timedelta
import logging
import os
from typing import List
from urllib.parse import quote

import aiohttp
import requests
from async_timeout import timeout
from clashleaders.util import correct_tag
from clashleaders import redis_connection
from dataclasses import dataclass

logger = logging.getLogger(__name__)

WORKER_OFFSET = int(os.getenv("WORKER_OFFSET", 1)) - 1
API_TOKEN = os.getenv("API_TOKEN", "").split(",")[WORKER_OFFSET]

if not API_TOKEN:
    raise ValueError("API_TOKEN is not set.")


def headers():
    return dict(authorization=f"Bearer {API_TOKEN}")


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


@dataclass
class ApiResponse:
    status: int
    data: dict


async def __fetch(url, params=None, loop=None, enable_cache=True):
    async with aiohttp.ClientSession(loop=loop, cookie_jar=aiohttp.DummyCookieJar(), headers=headers()) as session:
        return await __fetch_with_session(url, session=session, params=params, enable_cache=enable_cache)


async def __fetch_with_session(url, session, params=None, enable_cache=True) -> ApiResponse:
    cache_key = f"api:{url}:{params}"
    if enable_cache:
        if data := redis_connection.get(cache_key):
            logger.debug(f"Fetching {url} from cache with key {cache_key}.")
            return ApiResponse(200, json.loads(data))

    async with timeout(8):
        async with session.get(url, params=params) as response:
            data = await response.json()
            if response.status == 200:
                delta = int(response.headers["Cache-Control"].strip("public ").strip("max-age="))
                if enable_cache and delta > 0:
                    redis_connection.setex(cache_key, timedelta(seconds=delta), json.dumps(data))
            return ApiResponse(response.status, data)


async def __fetch_all(urls, loop=None) -> List[ApiResponse]:
    async with aiohttp.ClientSession(loop=loop, cookie_jar=aiohttp.DummyCookieJar(), headers=headers()) as session:
        futures = [__fetch_with_session(url, session) for url in urls]
        return await asyncio.gather(*futures, return_exceptions=True)


def find_clan_by_tag(tag):
    tag = correct_tag(tag)
    logger.info(f"Fetching clan from API {tag}.")

    try:
        response = asyncio.run(__fetch(f"https://api.clashofclans.com/v1/clans/{quote(tag)}"))
    except asyncio.TimeoutError:
        raise ApiTimeout(f"API timed while fetching {tag} clan.")

    code = response.status

    if code == 404:
        raise ClanNotFound(f"Clan [{tag}] not found.")

    if code == 429:
        raise TooManyRequests(f"Too many requests when fetching clan [{tag}].")

    if code != 200:
        raise ApiException(f"API returned non-200 status code: {code}")

    return response.data


def find_player_by_tag(tag):
    tag = correct_tag(tag)
    logger.info(f"Fetching player from API {tag}.")

    try:
        response = asyncio.run(__fetch(f"https://api.clashofclans.com/v1/players/{quote(tag)}"))
    except asyncio.TimeoutError:
        raise ApiTimeout(f"API timed while fetching {tag} clan.")

    code = response.status

    if code == 404:
        raise PlayerNotFound(f"Player [{tag}] not found.")

    if code == 429:
        raise TooManyRequests(f"Too many requests when fetching clan [{tag}].")

    if code != 200:
        raise ApiException(f"API returned non-200 status code: {code}")

    return response.data


def search_by_name(name, limit=10):
    logger.info(f"Searching for clan name '{name}'.")
    response = asyncio.run(__fetch("https://api.clashofclans.com/v1/clans", params={"name": name, "limit": limit}, enable_cache=False))

    if response.status != 200:
        return []
    else:
        return response.data["items"]


def top_players_and_clan():
    data = requests.get("https://clashofclans.com/api/leaderboards.json").json()
    leaderboards = data["hallOfFame"]["leaderboards"]
    players = leaderboards["topPlayers"]["players"]
    clans = leaderboards["topClans"]["clans"]
    return players, clans


def clan_warlog(tag):
    tag = correct_tag(tag)
    logger.info(f"Fetching clan warlog from API {tag}.")
    response = asyncio.run(__fetch(f"https://api.clashofclans.com/v1/clans/{quote(tag)}/warlog"))

    if response.status != 200:
        raise ClanNotFound(f"Clan [{tag}] not found.")

    return response.data


def clan_current_leaguegroup(tag):
    tag = correct_tag(tag)
    logger.info(f"Fetching clan current leaguegroup from API {tag}.")
    response = asyncio.run(__fetch(f"https://api.clashofclans.com/v1/clans/{quote(tag)}/currentwar/leaguegroup"))

    if response.status != 200:
        raise WarNotFound(f"Clan leaguegroup [{tag}] not found.")

    return response.data


def clan_current_war(tag):
    tag = correct_tag(tag)
    logger.info(f"Fetching clan current war from API {tag}.")
    response = asyncio.run(__fetch(f"https://api.clashofclans.com/v1/clans/{quote(tag)}/currentwar"))

    if response.status != 200:
        raise WarNotFound(f"War for clan [{tag}] not found.")

    return response.data


def clan_current_war_and_leaguegroup(tag):
    tag = correct_tag(tag)
    logger.info(f"Fetching clan current war and leaguegroup from API {tag}.")

    current_war_url = f"https://api.clashofclans.com/v1/clans/{quote(tag)}/currentwar"
    current_league_url = f"https://api.clashofclans.com/v1/clans/{quote(tag)}/currentwar/leaguegroup"
    current_war_response, current_league_response = asyncio.run(__fetch_all([current_war_url, current_league_url]))

    return [
        response.data if response.status == 200 else None for response in [current_war_response, current_league_response] if isinstance(response, ApiResponse)
    ]


def cwl_war_by_tags(tags):
    logger.info(f"Fetching war from API with {tags}.")
    urls = [f"https://api.clashofclans.com/v1/clanwarleagues/wars/{quote(tag)}" for tag in tags]
    responses = asyncio.run(__fetch_all(urls))
    return [response.data if response.status == 200 else None for response in responses if isinstance(response, ApiResponse)]


def fetch_all_players(tags: List):
    urls = [f"https://api.clashofclans.com/v1/players/{quote(tag)}" for tag in tags]
    responses = asyncio.run(__fetch_all(urls))
    return [response.data for response in responses if isinstance(response, ApiResponse) and response.status == 200]
