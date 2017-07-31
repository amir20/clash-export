import logging
import time

import os
import schedule
from mongoengine import connect
from raven import Client
from bson.objectid import ObjectId
from datetime import datetime, timedelta

import api
from model import Player, Clan

client = Client(os.getenv('SENTRY_DSN'))

logging.basicConfig(level=logging.INFO)

connect(db='clashstats', host='db', connect=False)
logger = logging.getLogger(__name__)


def object_id_from_now(**kargs):
    now = datetime.now()
    dt = now - timedelta(**kargs)
    return ObjectId.from_datetime(dt)


def update_clans():
    all_tags = set(Clan.objects.distinct('tag'))
    already_done = set(Clan.objects(id__gte=object_id_from_now(hours=12)).distinct('tag'))
    tags_to_fetch = list(all_tags - already_done)

    total = len(tags_to_fetch)
    tags_to_fetch = tags_to_fetch[:15]

    logger.info(f"Fetching {len(tags_to_fetch)} of total {total} eligible items.")

    for tag in tags_to_fetch:
        try:
            logger.info(f"Updating player stats for {tag}.")
            clan = api.find_clan_by_tag(tag)
            responses = api.fetch_all_players(clan)
            players = [r.json() for r in responses]
            clan['players'] = players

            [Player(**r).save() for r in players]
            Clan(**clan).save()

        except Exception:
            logger.exception(f"Error while fetching clan {tag}.")
            client.captureException()

    logger.info(f"Done fetching clans.")


schedule.every().hour.do(update_clans)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
