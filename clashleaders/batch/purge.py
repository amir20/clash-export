import logging

from clashleaders.model import Clan

logger = logging.getLogger(__name__)


def delete_outdated():
    logger.info("Deleting outdated historical clans...")
    pass  # todo


def reset_stats():
    logger.info("Resetting page views...")
    Clan.objects.update(set__page_views=0)
