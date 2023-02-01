import logging
from datetime import timedelta, datetime

from clashleaders.model import Clan, HistoricalClan, HistoricalPlayer, CWLWar, ClanWar

logger = logging.getLogger(__name__)


def delete_outdated():
    logger.info("Deleting outdated historical clans...")
    dt = datetime.now() - timedelta(days=7)
    while deleted := HistoricalClan.objects(created_on__lt=dt).limit(1000).delete():
        logging.info(f"Deleting {deleted} outdated historical clans...")
        pass

    while deleted := HistoricalPlayer.objects(created_on__lt=dt).limit(1000).delete():
        logging.info(f"Deleting {deleted} outdated historical players...")
        pass

    logger.info("Deleting 0 active_members clans...")
    Clan.objects(active_members=0).delete()
    HistoricalClan.objects(members=0).delete()

    logger.info("Deleting outdated wars...")
    dt = datetime.now() - timedelta(days=180)
    while deleted := ClanWar.objects(endTime__lt=dt).limit(1000).delete():
        logging.info(f"Deleting {deleted} outdated wars...")
        pass

    logger.info("Deleting outdated CWLs...")
    dt = datetime.now() - timedelta(days=90)
    while deleted := CWLWar.objects(endTime__lt=dt).limit(1000).delete():
        logging.info(f"Deleting {deleted} outdated CWLs...")
        pass


def reset_stats():
    logger.info("Resetting page views...")
    Clan.objects.update(set__page_views=0)
