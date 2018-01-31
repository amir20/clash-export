from clashleaders.model import ClanPreCalculated
import csv


def clans_to_csv(stream):
    writer = csv.writer(stream)

    for clan in ClanPreCalculated.objects.no_cache():
        writer.writerow([clan.tag,
                         clan.members,
                         clan.week_delta.total_trophies,
                         clan.week_delta.total_bh_trophies,
                         clan.week_delta.total_donations,
                         clan.week_delta.total_attack_wins,
                         clan.week_delta.total_versus_wins,
                         clan.week_delta.total_gold_grab,
                         clan.week_delta.avg_war_stars])
