import asyncio
import logging
import os
import time
from datetime import datetime, timedelta

import bugsnag
import uvloop
from bson.objectid import ObjectId
from bugsnag.handlers import BugsnagHandler
from mongoengine import connect
from pymongo.errors import BulkWriteError

from clashleaders.model import Clan, Player

bugsnag.configure(
    api_key=os.getenv('BUGSNAG_API_KEY'),
    project_root="/app",
    release_stage=os.getenv('STAGE', 'development'),
    notify_release_stages=["production"]
)
handler = BugsnagHandler()
handler.setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

DEBUG = os.getenv('DEBUG', False)

logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
logging.getLogger("clashleaders.clash.api").setLevel(logging.WARNING)
logger.addHandler(handler)

connect(db='clashstats', host=os.getenv('DB_HOST'), connect=False)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

marker = datetime.now() - timedelta(seconds=10)


def fetch_clans_since():
    global marker
    oid = ObjectId.from_datetime(marker)
    marker = datetime.now()
    for clan in Clan.objects(id__gte=oid):
        logger.debug(f"Saving all players for {clan.tag}.")
        try:
            bulk_operations = [Player(**data).as_replace_one() for data in clan.players_data()]
            Player._get_collection().bulk_write(bulk_operations)
        except BulkWriteError as bwe:
            logger.exception(f"Error thrown while saving [{bulk_operations}] {bwe.details}")
        except:
            logger.exception(f"Error while updating players in fetch_clans_since() with [{bulk_operations}]")


def main():
    while True:
        fetch_clans_since()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
