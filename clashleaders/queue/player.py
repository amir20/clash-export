from __future__ import annotations

import logging
from typing import List

from pymongo.errors import BulkWriteError
from rq.decorators import job

import clashleaders.model
import asyncio
from clashleaders import redis_connection
from clashleaders.clash import api

logger = logging.getLogger(__name__)


@job("player", connection=redis_connection, result_ttl=0)
def update_players(json_list: List):
    try:
        bulk_operations = [clashleaders.model.Player(**data).as_replace_one() for data in json_list]
        if bulk_operations:
            clashleaders.model.Player._get_collection().bulk_write(bulk_operations)
    except BulkWriteError as bwe:
        logger.exception(f"Error thrown while saving [{bulk_operations}] {bwe.details}")


@job("player_request", connection=redis_connection, result_ttl=0)
def fetch_players(tags: List):
    try:
        response = api.fetch_all_players(tags)
        update_players(response)
    except asyncio.TimeoutError:
        logger.exception(f"Received TimeoutError while fetching players in fetch_players()")
