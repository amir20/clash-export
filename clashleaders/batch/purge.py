import logging

from clashleaders.model import Clan, ClanPreCalculated

logger = logging.getLogger(__name__)


def delete_outdated():
    deleted = Clan.older_than(days=31).delete()
    logger.info(f"Deleted {deleted} clans that are older than 31 days.")

    deleted = ClanPreCalculated.objects(members__lt=5).delete()
    Clan.objects(members__lt=5).delete()
    logger.info(f"Deleted {deleted} clans with less than 5 members.")

    not_active_tags = [c.tag for c in ClanPreCalculated.objects(week_delta__total_donations=0, week_delta__total_attack_wins=0).only('tag')]
    Clan.objects(tag__in=not_active_tags).delete()
    not_active_deleted = ClanPreCalculated.objects(week_delta__total_donations=0, week_delta__total_attack_wins=0).delete()
    logger.info(f"Deleted {not_active_deleted} clans with zero attacks.")


def reset_stats():
    logger.info("Resetting page views...")
    ClanPreCalculated.objects.update(set__page_views=0)