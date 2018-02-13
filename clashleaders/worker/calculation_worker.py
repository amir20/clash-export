import asyncio
import logging
import threading
import gc
from datetime import datetime, timedelta

from clashleaders.model import ClanPreCalculated

logger = logging.getLogger(__name__)


def start_clan_worker_thread():
    def worker():
        # Creates an event loops for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

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
                        logger.info(f"gb.collect() {gc.collect()}")
                        del tags_indexed
                        tags_indexed = []
            except Exception:
                logger.exception(f"Error while fetching clan.")

    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()
