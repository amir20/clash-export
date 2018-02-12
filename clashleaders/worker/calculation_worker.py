import threading
import logging
import asyncio

logger = logging.getLogger(__name__)


def start_worker_thread(queue):
    def worker():
        # Creates an event loops for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        while True:
            clan = queue.get()
            try:
                logger.debug(f"Updating clan {clan.tag}. {queue.qsize()} items in queue.")
                clan.fetch_and_update_calculations()
            except Exception:
                logger.exception(f"Error while fetching clan {clan.tag}.")

    thread_1 = threading.Thread(target=worker)
    thread_1.daemon = True
    thread_1.start()

    thread_2 = threading.Thread(target=worker)
    thread_2.daemon = True
    thread_2.start()
