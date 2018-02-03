import csv

from clashleaders.model import ClanPreCalculated


def clans_to_csv(stream):
    writer = csv.writer(stream)
    writer.writerow(['tag',
                     'members',
                     'clanLevel',
                     'avg_xp_level',
                     'avg_bk_level',
                     'avg_aq_level',
                     'avg_bm_level',
                     'week_trophies',
                     'week_bh_trophies',
                     'week_total_donations',
                     'week_attacks_wins',
                     'week_versus_wins',
                     'week_gold_grab',
                     'week_avg_war_stars'])

    for clan in ClanPreCalculated.objects.no_cache():
        writer.writerow([clan.tag,
                         clan.members,
                         clan.clanLevel,
                         clan.avg_xp_level,
                         clan.avg_bk_level,
                         clan.avg_aq_level,
                         clan.avg_bm_level,
                         clan.week_delta.total_trophies,
                         clan.week_delta.total_bh_trophies,
                         clan.week_delta.total_donations,
                         clan.week_delta.total_attack_wins,
                         clan.week_delta.total_versus_wins,
                         clan.week_delta.total_gold_grab,
                         clan.week_delta.avg_war_stars])
