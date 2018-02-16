import logging
import os
import time
from datetime import datetime, timedelta

import bugsnag
import schedule
from bugsnag.handlers import BugsnagHandler
from mongoengine import connect

from clashleaders.clash.api import ClanNotFound
from clashleaders.model import ClanPreCalculated

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

if DEBUG:
    logger.setLevel(logging.DEBUG)

logging.getLogger("clashleaders.clash.api").setLevel(logging.WARNING)
logging.getLogger("schedule").setLevel(logging.WARNING)

logger.addHandler(handler)

connect(db='clashstats', host=os.getenv('DB_HOST'), connect=False)

tags_indexed = []


def update_single_clan():
    global tags_indexed
    try:
        twelve_hour_ago = datetime.now() - timedelta(hours=12)

        query_set = ClanPreCalculated.objects(last_updated__lte=twelve_hour_ago).no_cache()
        total = query_set.count()
        clans = query_set.limit(3)
        if clans:
            for clan in clans:
                logger.debug(f"Updating clan {clan.tag} with {total} eligible clans.")
                clan.fetch_and_update_calculations()
                tags_indexed.append(clan.tag)
            if len(tags_indexed) > 99:
                logger.info(f"Indexed {len(tags_indexed)} clans: {tags_indexed}")
                logger.info(f"Currently {total} eligible clans.")
                tags_indexed = []
    except ClanNotFound:
        logger.exception(f"Clan not found when fetching {clan.tag}. Pausing for 5 seconds.")
        eleven_hour_ago = twelve_hour_ago + timedelta(hours=1)
        clan.update(set__last_updated=eleven_hour_ago)
        time.sleep(5)
    except Exception:
        logger.exception(f"Error while fetching clan. Pausing for 5 seconds.")
        time.sleep(5)


schedule.every().second.do(update_single_clan)


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
