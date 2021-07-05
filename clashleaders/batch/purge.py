import logging
from datetime import datetime, timedelta

from clashleaders.model import Clan, HistoricalClan, HistoricalPlayer

logger = logging.getLogger(__name__)


def delete_outdated():
    logger.info("Deleting outdated historical clans...")
    dt = datetime.now() - timedelta(days=31)
    HistoricalClan.objects(created_on__lt=dt).delete()
    HistoricalPlayer.objects(created_on__lt=dt).delete()
    logger.info("Deleting 0 member clans...")
    Clan.objects(members=0).delete()
    HistoricalClan.objects(members=0).delete()


def reset_stats():
    logger.info("Resetting page views...")
    Clan.objects.update(set__page_views=0)
