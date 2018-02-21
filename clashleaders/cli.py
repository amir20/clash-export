import logging
import os

from mongoengine import connect

from clashleaders.model import ClanPreCalculated

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("clashleaders.clash.api").setLevel(logging.WARNING)

connect(db='clashstats', host=os.getenv('DB_HOST'), connect=False)


def update_all_calculations():
    total = ClanPreCalculated.objects.count()

    i = 0
    for clan in ClanPreCalculated.objects.no_cache():
        try:
            i += 1
            print(f"{i}/{total}")
            clan.update_without_fetching()
        except Exception:
            pass
