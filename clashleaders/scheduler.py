import asyncio
import concurrent
import logging
import os
import queue
import threading
import time
from datetime import datetime, timedelta
from random import randrange

import bugsnag
import schedule
import uvloop
from bugsnag.handlers import BugsnagHandler
from mongoengine import connect

from clashleaders.batch.purge import delete_outdated, reset_stats
from clashleaders.batch.similar_clan import compute_similar_clans
from clashleaders.clash import api
from clashleaders.clash.api import ApiException, ClanNotFound, TooManyRequests
from clashleaders.model import Clan, ClanPreCalculated, Status

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

queue = queue.Queue(1)


def worker():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    tags_indexed = []

    while True:
        try:
            tag = queue.get()
            logger.debug(f"Fetching and updating clan {tag}.")
            Clan.fetch_and_save(tag).update_calculations()
            tags_indexed.append(tag)
            time.sleep(0.25)

            if len(tags_indexed) > 99:
                logger.info(f"Fetched {len(tags_indexed)} clans: {tags_indexed}")
                tags_indexed = []
        except ClanNotFound:
            logger.warning(f"Skipping not found clan [{tag}].")
        except TooManyRequests:
            logger.warning(f"Too many requests while fetching [{tag}]. Sleeping for one second.")
            time.sleep(1)
        except ApiException:
            logger.warning(f"API exception while fetching [{tag}].")
        except concurrent.futures.TimeoutError:
            logger.warning(f"Timeout error thrown [{tag}]. Skipping clan.")
        except Exception:
            logger.exception(f"Error while fetching clan {tag}.")


def update_clan_calculations():
    hour_ago = datetime.now() - timedelta(hours=1)
    recent_tags = set(Clan.from_now(hours=1).distinct('tag'))
    calculated_tags = set(ClanPreCalculated.objects(last_updated__gte=hour_ago).distinct('tag'))
    available_clan_tags = recent_tags - calculated_tags

    if available_clan_tags:
        logger.info(f"Updating {len(available_clan_tags)} clan calculations.")
        updated_tags = []
        for tag in available_clan_tags:
            try:
                clan = Clan.find_most_recent_by_tag(tag)
                logger.debug(f"Updating calculations for {clan.tag}.")
                clan.update_calculations()
                updated_tags.append(clan.tag)
            except TypeError:
                # Possibly a json error. Let's delete the instance
                logger.warning(f"TypeError exception thrown for {clan.tag}. Deleting most recent instance.")
                clan.delete()
            except Exception:
                logger.exception(f"Error during updating clan calculation for {tag}. Deleting instance of clan.")

        logger.info(f"Updated calculations: {updated_tags}")


def update_leaderboards():
    columns = ['week_delta.avg_donations',
               'week_delta.avg_attack_wins',
               'week_delta.avg_versus_wins',
               'week_delta.avg_gold_grab',
               'clanPoints',
               'clanVersusPoints',
               'week_delta.avg_trophies',
               'avg_bh_level']

    for column in columns:
        logger.info(f"Updating {column} leaderboard.")
        for c in ClanPreCalculated.objects(members__gt=20).order_by(f"-{column}").limit(15):
            queue.put(c.tag)


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
schedule.every().minute.do(update_clan_calculations)
schedule.every().day.do(reset_stats)
schedule.every().day.at("12:01").do(delete_outdated)
schedule.every().monday.do(compute_similar_clans)

schedule.every(6).hours.do(update_leaderboards)
schedule.every(6).hours.do(index_random_war_clan)
schedule.every(1).hours.do(fetch_clan_leaderboards)


def main():
    importer_thread = threading.Thread(target=worker)
    importer_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
