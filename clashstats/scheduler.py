import logging
import os
import time
from datetime import datetime, timedelta

import schedule
from clashstats.clash.calculation import update_calculations
from clashstats.model import *
from mongoengine import connect
from raven import Client

client = Client(os.getenv('SENTRY_DSN'))

logging.basicConfig(level=logging.INFO)

connect(db='clashstats', host=os.getenv('DB_HOST'), connect=False)

logger = logging.getLogger(__name__)
logging.getLogger("clashstats.clash.api").setLevel(logging.WARNING)


def update_clans():
    twelve_hour_ago = datetime.now() - timedelta(hours=12)
    query_set = ClanPreCalculated.objects(last_updated__lte=twelve_hour_ago)
    total = query_set.count()
    clans = query_set.limit(50)

    logger.info(f"Fetching {len(clans)} of total {total} eligible clans.")

    for c in clans:
        try:
            logger.info(f"Updating clan {c.tag}.")
            update_calculations(Clan.fetch_and_save(c.tag))
        except Exception:
            logger.exception(f"Error while fetching clan {tag}.")
            client.captureException()

    logger.debug(f"Done fetching clans.")

    total_clans = ClanPreCalculated.objects.count()

    ratio_indexed = 100 * (ClanPreCalculated.objects(last_updated__lte=twelve_hour_ago).count() / total_clans)
    Status.objects.update_one(
        set__ratio_indexed=ratio_indexed,
        set__total_clans=total_clans,
        set__last_updated=datetime.now,
        upsert=True
    )


def update_clan_calculations():
    hour_ago = datetime.now() - timedelta(hours=1)
    recent_tags = set(Clan.from_now(hours=1).distinct('tag'))
    calculated_tags = set(ClanPreCalculated.objects(last_updated__gte=hour_ago).distinct('tag'))
    available_clan_tags = recent_tags - calculated_tags

    logger.info(f"Updating {len(available_clan_tags)} clan calculations.")
    for tag in available_clan_tags:
        try:
            logger.info(f"Updating calculations for {tag}.")
            update_calculations(Clan.objects(tag=tag).first())
        except Exception:
            logger.exception(f"Error during updating clan calculation for {tag}.")
            client.captureException()


def delete_old_clans():
    deleted = Clan.older_than(days=45).delete()
    logger.info(f"Deleted {deleted} clans that are older than 45 days.")

    tags = ClanPreCalculated.objects(members__lt=5).distinct('tag')
    deleted = Clan.objects(tag__in=tags).delete()
    logger.info(f"Deleted {deleted} clans with less than 5 members.")

    deleted = ClanPreCalculated.objects(members=0).delete()
    logger.info(f"Deleted {deleted} clans with 0 members.")


def update_leaderboards():
    columns = ['week_delta.avg_donations',
               'week_delta.avg_attack_wins',
               'week_delta.avg_versus_wins',
               'week_delta.avg_gold_grab',
               'clanPoints',
               'clanVersusPoints',
               'warWinStreak',
               'week_delta.avg_war_stars',
               'week_delta.avg_trophies',
               'avg_bh_level']

    for column in columns:
        for c in ClanPreCalculated.objects(members__gt=20).order_by(f"-{column}").limit(15):
            try:
                logger.info(f"Updating {column} leaderboard clan {c.tag}.")
                update_calculations(Clan.fetch_and_save(c.tag))
            except Exception:
                logger.exception(f"Error while fetching leaderboard clan {c.tag}.")
                client.captureException()


schedule.every().minutes.do(update_clans)
schedule.every().minutes.do(update_clan_calculations)
schedule.every().hour.do(update_leaderboards)
schedule.every().day.at("12:01").do(delete_old_clans)


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
