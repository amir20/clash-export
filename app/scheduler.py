import logging
import time

import os
import schedule
from mongoengine import connect
from raven import Client

from model import Clan

client = Client(os.getenv('SENTRY_DSN'))

logging.basicConfig(level=logging.INFO)

connect(db='clashstats', host=os.getenv('DB_HOST'), connect=False)
logger = logging.getLogger(__name__)
logging.getLogger("clash.api").setLevel(logging.WARNING)


def update_clans():
    all_tags = set(Clan.objects.distinct('tag'))
    already_done = set(Clan.from_now(hours=12).distinct('tag'))
    tags_to_fetch = list(all_tags - already_done)

    total = len(tags_to_fetch)
    tags_to_fetch = tags_to_fetch[:75]

    logger.info(f"Fetching {len(tags_to_fetch)} of total {total} eligible items.")

    for tag in tags_to_fetch:
        try:
            logger.info(f"Updating player stats for {tag}.")
            Clan.fetch_and_save(tag)
        except Exception:
            logger.exception(f"Error while fetching clan {tag}.")
            client.captureException()

    logger.info(f"Done fetching clans.")


def delete_old_clans():
    deleted = Clan.older_than(days=45).delete()
    logger.info(f"Deleted {deleted} clans that are older than 45 days.")


schedule.every().hour.do(update_clans)
schedule.every().day.do(delete_old_clans)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
