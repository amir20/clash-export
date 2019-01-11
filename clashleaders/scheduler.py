import logging
import os
import queue
import time
from random import randrange

import bugsnag
import schedule
from bugsnag.handlers import BugsnagHandler
from mongoengine import connect

from clashleaders.batch.purge import delete_outdated, reset_stats
from clashleaders.batch.similar_clan import compute_similar_clans
from clashleaders.clash import api
from clashleaders.model import ClanPreCalculated, Status, AverageTroop

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
logging.getLogger("schedule").setLevel(logging.WARNING)
logger.addHandler(handler)

connect(db='clashstats', host=os.getenv('DB_HOST'), connect=False)


def index_random_war_clan():
    count = ClanPreCalculated.objects(isWarLogPublic=True).count()
    random_clan = ClanPreCalculated.objects(isWarLogPublic=True)[randrange(0, count)]

    logger.info(f"Indexing random clan war log ({random_clan.tag}).")

    try:
        tags = [war['opponent']['tag'] for war in random_clan.warlog()]
    except Exception:
        logger.warning(f"Error while fetch war log for {random_clan.tag}.")
    else:
        for tag in tags:
            if not ClanPreCalculated.objects(tag=tag).first():
                queue.put(tag)


def fetch_clan_leaderboards():
    logger.info(f"Updating clan leaderboards from CoC website.")
    players, clans = api.top_players_and_clan()

    for player in players:
        tag = player['clanTag']
        if tag:
            queue.put(tag)

    for clan in clans:
        tag = clan['tag']
        if tag:
            queue.put(tag)


schedule.every().minute.do(Status.update_status)
schedule.every().day.do(reset_stats)
schedule.every().day.at("12:01").do(delete_outdated)
schedule.every().monday.do(compute_similar_clans)
schedule.every().friday.do(AverageTroop.update_all)
schedule.every(8).hours.do(index_random_war_clan)
schedule.every(1).hours.do(fetch_clan_leaderboards)


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
