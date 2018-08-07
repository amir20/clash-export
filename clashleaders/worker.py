import asyncio
import logging
import os
import time
from datetime import datetime, timedelta

import bugsnag
import uvloop
from bugsnag.handlers import BugsnagHandler
from mongoengine import connect

from clashleaders.clash.api import ApiException, ApiTimeout, ClanNotFound, TooManyRequests
from clashleaders.model import Clan, ClanPreCalculated

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

tags_indexed = []


def update_single_clan():
    global tags_indexed
    twelve_hour_ago = datetime.now() - timedelta(hours=12)
    try:
        query_set = ClanPreCalculated.active_clans(twelve_hour_ago)
        total = query_set.count()
        clan = query_set.first()
        if clan:
            logger.debug(f"Updating clan {clan.tag} with {total} eligible clans.")
            clan = clan.fetch_and_update_calculations()
            tags_indexed.append(clan.tag)
            if len(tags_indexed) > 99:
                logger.info(f"Indexed {len(tags_indexed)} clans: {tags_indexed}")
                logger.info(f"Currently {total} eligible clans.")
                tags_indexed = []
        else:
            time.sleep(10)
    except ClanNotFound:
        logger.warning(f"Clan with tag {clan.tag} not found. Pausing for 1 second.")
        try_again_clan(clan)
        time.sleep(1)
    except TooManyRequests:
        logger.warning(f"Too many requests for {clan.tag}. Trying again in 3 seconds.")
        time.sleep(3)
    except ApiTimeout:
        logger.warning(f"Timeout error when fetching [{clan.tag}]. Waiting 1 second and trying again.")
        time.sleep(1)
    except ApiException:
        logger.warning(f"API exception when fetching {clan.tag}. Pausing for 10 seconds.")
        try_again_clan(clan)
        time.sleep(10)
    except TypeError:
        # Possibly a json error. Let's delete the instance
        logger.warning(f"TypeError exception thrown for {clan.tag}. Deleting most recent instance.")
        clan.most_recent.delete()
        eleven_hour_ago = twelve_hour_ago + timedelta(hours=1)
        clan.update(set__last_updated=eleven_hour_ago, set__most_recent=Clan.find_most_recent_by_tag(clan.tag))
        logger.info(f"Sleeping for 10 seconds.")
        time.sleep(10)
    except Exception:
        logger.exception(f"Error while fetching clan. Pausing for 5 seconds.")
        time.sleep(5)


def try_again_clan(clan):
    if clan:
        eleven_hour_ago = datetime.now() - timedelta(hours=11)
        clan.update(set__last_updated=eleven_hour_ago)


def main():
    while True:
        update_single_clan()
        time.sleep(0.05)


if __name__ == "__main__":
    main()
