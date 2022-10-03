import logging
from datetime import timedelta, datetime

from clashleaders.model import Clan, HistoricalClan, HistoricalPlayer, CWLWar, ClanWar

logger = logging.getLogger(__name__)


def delete_outdated():
    logger.info("Deleting outdated historical clans...")
    dt = datetime.now() - timedelta(days=7)
    HistoricalClan.objects(created_on__lt=dt).delete()
    HistoricalPlayer.objects(created_on__lt=dt).delete()
    logger.info("Deleting 0 active_members clans...")
    Clan.objects(active_members=0).delete()
    HistoricalClan.objects(members=0).delete()

    logger.info("Deleting outdated wars...")
    dt = datetime.now() - timedelta(days=180)
    CWLWar.objects(endTime__lt=dt).delete()
    ClanWar.objects(endTime__lt=dt).delete()


def reset_stats():
    logger.info("Resetting page views...")
    Clan.objects.update(set__page_views=0)
