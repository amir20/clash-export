import logging

from rq.decorators import job

import clashleaders.model
from clashleaders import redis_connection

logger = logging.getLogger(__name__)


@job("calculation", connection=redis_connection, result_ttl=0, failure_ttl=None)
def update_calculations(tag):
    clashleaders.model.Clan.find_by_tag(tag).update_calculations()
