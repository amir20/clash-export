import asyncio
import logging
import threading
from datetime import datetime, timedelta

from clashleaders.model import ClanPreCalculated

logger = logging.getLogger(__name__)


def start_worker_thread():
    def worker():
        # Creates an event loops for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        while True:

            try:
                twelve_hour_ago = datetime.now() - timedelta(hours=12)

                query_set = ClanPreCalculated.objects(last_updated__lte=twelve_hour_ago)
                total = query_set.count()
                clan = query_set.first()
                if clan:
                    logger.debug(f"Updating clan {clan.tag} with {total} eligible clans.")
                    clan.fetch_and_update_calculations()
            except Exception:
                logger.exception(f"Error while fetching clan.")

    thread_1 = threading.Thread(target=worker)
    thread_1.daemon = True
    thread_1.start()
