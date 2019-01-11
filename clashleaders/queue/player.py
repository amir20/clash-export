import logging

from pymongo.errors import BulkWriteError
from rq.decorators import job

import clashleaders.model
from clashleaders import redis_connection

logger = logging.getLogger(__name__)


@job('player', connection=redis_connection, result_ttl=0)
def update_players(json_list):
    try:
        bulk_operations = [clashleaders.model.Player(**data).as_replace_one() for data in json_list]
        if bulk_operations:
            clashleaders.model.Player._get_collection().bulk_write(bulk_operations)
    except BulkWriteError as bwe:
        logger.exception(f"Error thrown while saving [{bulk_operations}] {bwe.details}")
    except:
        logger.exception(f"Error while updating players in fetch_clans_since() with [{bulk_operations}]")
