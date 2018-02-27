import concurrent
import logging
import os
import time
from datetime import datetime, timedelta
from random import randrange

import bugsnag
import schedule
from bugsnag.handlers import BugsnagHandler
from mongoengine import connect

from clashleaders.clash.api import ClanNotFound
from clashleaders.clustering.csv_export import clans_to_csv
from clashleaders.clustering.kmeans import train_model
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
logger.addHandler(handler)

connect(db='clashstats', host=os.getenv('DB_HOST'), connect=False)


def update_clan_calculations():
    hour_ago = datetime.now() - timedelta(hours=1)
    recent_tags = set(Clan.from_now(hours=1).distinct('tag'))
    calculated_tags = set(ClanPreCalculated.objects(last_updated__gte=hour_ago).distinct('tag'))
    available_clan_tags = recent_tags - calculated_tags

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


def delete_old_clans():
    deleted = Clan.older_than(days=31).delete()
    logger.info(f"Deleted {deleted} clans that are older than 31 days.")

    deleted = ClanPreCalculated.objects(members__lt=5).delete()
    Clan.objects(members__lt=5).delete()
    logger.info(f"Deleted {deleted} clans with less than 5 members.")


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
            try:
                logger.debug(f"Updating {column} leaderboard clan {c.tag}.")
                Clan.fetch_and_save(c.tag).update_calculations()
            except ClanNotFound:
                logger.warning(f"Skipping not found clan [{c.tag}].")
            except concurrent.futures.TimeoutError:
                logger.warning(f"Timeout error thrown [{c.tag}]. Skipping clan.")
            except Exception:
                logger.exception(f"Error while fetching leaderboard clan {c.tag}.")


def update_status():
    twelve_hour_ago = datetime.now() - timedelta(hours=12)
    total_clans = ClanPreCalculated.objects.count()
    ratio_indexed = 100 * (ClanPreCalculated.objects(last_updated__gt=twelve_hour_ago).count() / total_clans)
    Status.objects.update_one(
        set__ratio_indexed=ratio_indexed,
        set__total_clans=total_clans,
        set__last_updated=datetime.now(),
        set__total_members=ClanPreCalculated.objects.sum('members'),
        set__total_countries=len(ClanPreCalculated.objects.distinct('location.countryCode')),
        upsert=True
    )


def compute_similar_clans():
    filename = '/tmp/clans.csv'

    logger.info(f"Writing clans to csv file.")
    with open(filename, 'w') as f:
        clans_to_csv(f)

    logger.info(f"Computing kmeans for clans and saving model.")
    labels = train_model(filename)

    os.remove(filename)

    logger.info(f"Updating labels for {len(labels)} clans.")
    for tag, label in labels.items():
        ClanPreCalculated.objects(tag=tag).update_one(set__cluster_label=label)


def index_random_war_clan():
    count = ClanPreCalculated.objects(isWarLogPublic=True).count()
    random_clan = ClanPreCalculated.objects(isWarLogPublic=True)[randrange(0, count)]

    logger.info(f"Indexing random clan war log ({random_clan.tag}).")

    try:
        tags = [war['opponent']['tag'] for war in random_clan.warlog()]
    except Exception:
        logger.warning(f"Error while fetch war log for {random_clan.tag}.")
    else:
        updated_tags = []
        for tag in tags:
            if not ClanPreCalculated.objects(tag=tag).first():
                logger.debug(f"Fetching new clan with tag {tag}")
                try:
                    Clan.fetch_and_save(tag)
                    updated_tags.append(tag)
                except ClanNotFound:
                    logger.warning(f"Skipping clan [{tag}] not found.")
                except concurrent.futures.TimeoutError:
                    logger.warning(f"Timeout error when fetching [{tag}].")
                except Exception:
                    logger.exception(f"Error while updating clan from war log.")

        logger.info(f"Indexed new war clans: {updated_tags}")


def reset_page_views():
    logger.info("Resetting page views...")
    ClanPreCalculated.objects.update(set__page_views=0)


schedule.every().minute.do(update_status)
schedule.every().minute.do(update_clan_calculations)
schedule.every().day.do(reset_page_views)
schedule.every().day.at("12:01").do(delete_old_clans)
schedule.every().monday.do(compute_similar_clans)

schedule.every(6).hours.do(update_leaderboards)
schedule.every(12).hours.do(index_random_war_clan)


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
