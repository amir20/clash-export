import logging
import time

import os
import schedule
from mongoengine import connect
from raven import Client

import api
from model import Player, Clan

client = Client(os.getenv('SENTRY_DSN'))

logging.basicConfig(level=logging.INFO)

connect(db='clashstats', host='db', connect=False)
logger = logging.getLogger(__name__)


def update_clans():
    logger.info("Updating all clans.")
    for tag in Clan.objects.distinct('tag'):
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


schedule.every().day.at("1:30").do(update_clans)
schedule.every().day.at("9:30").do(update_clans)
schedule.every().day.at("17:30").do(update_clans)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
