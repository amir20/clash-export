import asyncio
import logging
import os
import time
from datetime import datetime, timedelta

import uvloop
from bugsnag.handlers import BugsnagHandler

from clashleaders import app, influx_client
from clashleaders.clash.api import ApiException, ApiTimeout, ClanNotFound, TooManyRequests
from clashleaders.model import Clan

handler = BugsnagHandler()
handler.setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

WORKER_OFFSET = int(os.getenv('WORKER_OFFSET', 1))
INDEX = (WORKER_OFFSET - 1) * 10

logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
logging.getLogger("clashleaders.clash.api").setLevel(logging.WARNING)
logger.addHandler(handler)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

tags_indexed = []

start = time.time()


def update_single_clan():
    global tags_indexed, start
    twelve_hour_ago = datetime.now() - timedelta(hours=12)
    try:
        clan = Clan.active(twelve_hour_ago).skip(max(INDEX - 1, 0)).limit(1).first()
        if clan:
            logger.debug(f"Worker #{WORKER_OFFSET}: Updating clan {clan.tag}.")
            capture_duration(lambda: Clan.fetch_and_update(clan.tag, sync_calculation=True))
            tags_indexed.append(clan.tag)
            if len(tags_indexed) > 99:
                total = Clan.active(twelve_hour_ago).count()
                logger.info(f"Indexed {len(tags_indexed)} clans: {tags_indexed}")
                logger.info(f"Currently {total} eligible clans.")
                tags_indexed = []
                end = time.time()
                seconds = end - start
                start = time.time()
                logger.info(f"Processed {100 / seconds} clans per second.")

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
        clan.update(set__updated_on=eleven_hour_ago)
        logger.info(f"Sleeping for 10 seconds.")
        time.sleep(10)
    except Exception:
        logger.exception(f"Error while fetching clan. Pausing for 5 seconds.")
        time.sleep(5)


def try_again_clan(clan):
    if clan:
        eleven_hour_ago = datetime.now() - timedelta(hours=11)
        clan.update(set__updated_on=eleven_hour_ago)


def capture_duration(func):
    start_time = time.time()
    func()
    duration = (time.time() - start_time) * 1000
    json_body = [
        {
            "measurement": "clan_fetch",
            "fields": {
                "value": duration
            }
        }
    ]

    influx_client.write_points(json_body)


def main():
    while True:
        update_single_clan()
        time.sleep(0.025)


if __name__ == "__main__":
    main()
