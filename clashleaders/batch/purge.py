import logging
from datetime import timedelta, datetime

from clashleaders.model import Clan, HistoricalClan, HistoricalPlayer

logger = logging.getLogger(__name__)


def delete_outdated():
    logger.info("Deleting outdated historical clans...")
    dt = datetime.now() - timedelta(days=31)
    HistoricalPlayer.objects(created_on__lt=dt).delete()
    HistoricalClan.objects(created_on__lt=dt).delete()


def reset_stats():
    logger.info("Resetting page views...")
    Clan.objects.update(set__page_views=0)
