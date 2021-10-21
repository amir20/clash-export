import logging

from rq import Queue

import clashleaders.model
from clashleaders import redis_connection

logger = logging.getLogger(__name__)

queue = Queue(name="war", connection=redis_connection)


def schedule_war_update(datetime, tag):
    return queue.enqueue_at(datetime, update_wars, tag)


def update_wars(tag):
    clashleaders.model.Clan.fetch_and_update(tag, sync_calculation=True).update_wars()
