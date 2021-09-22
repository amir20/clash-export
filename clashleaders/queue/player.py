from __future__ import annotations

import logging
from typing import List

from rq.decorators import job

import clashleaders.model
import asyncio
from clashleaders import redis_connection
from clashleaders.clash import api

logger = logging.getLogger(__name__)


@job("player_request", connection=redis_connection, result_ttl=0)
def fetch_players(tags: List):
    try:
        for tag in tags:
            clashleaders.model.Player.fetch_and_save(tag)
    except asyncio.TimeoutError:
        logger.exception(f"Received TimeoutError while fetching players in fetch_players()")
