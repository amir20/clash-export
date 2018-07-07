import logging

from clashleaders.model import Clan, ClanPreCalculated

logger = logging.getLogger(__name__)


def delete_outdated():
    deleted = Clan.older_than(days=31).delete()
    logger.info(f"Deleted {deleted} clans that are older than 31 days.")


def reset_stats():
    logger.info("Resetting page views...")
    ClanPreCalculated.objects.update(set__page_views=0)
