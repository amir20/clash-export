from __future__ import annotations

import csv

import clashleaders.model


def clans_to_csv(stream):
    writer = csv.writer(stream)
    writer.writerow(
        [
            "tag",
            "members",
            "clanLevel",
            "week_trophies",
            "week_donations",
            "week_attacks",
            "week_versus_wins",
            "week_gold_grab",
            "week_avg_war_stars",
        ]
    )

    for clan in clashleaders.model.Clan.objects(members__gte=5).no_cache():
        writer.writerow([clan.tag, *extract_features(clan)])


def extract_features(clan: clashleaders.model.Clan):
    return [
        clan.members,
        clan.clanLevel,
        clan.week_delta.total_trophies,
        clan.week_delta.total_donations,
        clan.week_delta.total_attack_wins,
        clan.week_delta.total_versus_wins,
        clan.week_delta.total_gold_grab,
        clan.week_delta.avg_war_stars,
    ]
