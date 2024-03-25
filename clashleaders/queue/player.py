from __future__ import annotations

import asyncio
import logging
import time
from typing import List

import clashleaders.model

logger = logging.getLogger(__name__)

import queue
import threading

q: queue.Queue = queue.Queue()


def worker():
    while True:
        tag = q.get()
        try:
            clashleaders.model.Player.fetch_and_save(tag)
        except asyncio.TimeoutError:
            logger.exception(
                "Received TimeoutError while fetching players in fetch_players()"
            )
        except:
            logger.exception("Unexpected error while updating players")
        finally:
            q.task_done()
            time.sleep(0.100)


threading.Thread(target=worker, daemon=True).start()


def fetch_players(tags: List[str]):
    for tag in tags:
        q.put(tag)
