import logging
from random import randrange
import sys

from clashleaders.clash import api
from clashleaders.model import Clan

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("clashleaders.clash.api").setLevel(logging.WARNING)


def update_all_calculations():
    total = Clan.objects.count()

    i = 0
    for clan in Clan.objects.no_cache():
        try:
            i += 1
            print(f"- {i}/{total}: {clan}")
            clan.update_calculations()
        except Exception:
            logger.exception("error while performing update_calculations")


def index_random_war_clan():
    count: Clan = Clan.objects(isWarLogPublic=True).count()
    random_clan: Clan = Clan.objects(isWarLogPublic=True)[randrange(0, count)]

    logger.info(f"Indexing random clan war log ({random_clan.tag}).")

    try:
        tags = [war["opponent"]["tag"] for war in random_clan.warlog()]
    except Exception:
        logger.warning(f"Error while fetch war log for {random_clan.tag}.")
    else:
        for tag in tags:
            if not Clan.objects(tag=tag).first():
                Clan.fetch_and_update(tag)


def fetch_clan_leaderboards():
    logger.info(f"Updating clan leaderboards from CoC website.")
    players, clans = api.top_players_and_clan()

    for player in players:
        tag = player["clanTag"]
        if tag:
            Clan.fetch_and_update(tag)

    for clan in clans:
        tag = clan["tag"]
        if tag:
            Clan.fetch_and_update(tag)


def fetch_tags():
    tags = set(line.rstrip("\n") for line in sys.stdin.readlines())
    existing = set(clan.tag for clan in Clan.objects(tag__in=tags).only("tag"))
    logging.info(f"Found {len(tags)} tags, {len(existing)} already exist.")

    new_tags = tags - existing
    success = 0
    for tag in new_tags:
        try:
            Clan.fetch_and_update(tag)
            success += 1
        except Exception:
            logger.exception(f"Error while fetching clan {tag}.")

    logger.info(f"Found {success} new tags.")
