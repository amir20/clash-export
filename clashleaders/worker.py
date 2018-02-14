import logging
import os

from datetime import datetime, timedelta

import bugsnag
from bugsnag.handlers import BugsnagHandler
from mongoengine import connect

from clashleaders.model import ClanPreCalculated

bugsnag.configure(
    api_key=os.getenv('BUGSNAG_API_KEY'),
    project_root="/app",
    release_stage=os.getenv('STAGE', 'development'),
    notify_release_stages=["production"]
)
handler = BugsnagHandler()
handler.setLevel(logging.ERROR)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("clashleaders.clash.api").setLevel(logging.WARNING)
logger.addHandler(handler)

connect(db='clashstats', host=os.getenv('DB_HOST'), connect=False)


def run_clan_worker():
    tags_indexed = []
    while True:
        try:
            twelve_hour_ago = datetime.now() - timedelta(hours=12)

            query_set = ClanPreCalculated.objects(last_updated__lte=twelve_hour_ago).no_cache()
            total = query_set.count()
            clan = query_set.first()
            if clan:
                logger.debug(f"Updating clan {clan.tag} with {total} eligible clans.")
                clan.fetch_and_update_calculations()
                tags_indexed.append(clan.tag)
                if len(tags_indexed) > 100:
                    logger.info(f"Indexed {len(tags_indexed)} clans: {tags_indexed}")
                    logger.info(f"Currently {total} eligible clans.")
                    del tags_indexed
                    tags_indexed = []
        except Exception:
            logger.exception(f"Error while fetching clan.")


if __name__ == "__main__":
    run_clan_worker()
