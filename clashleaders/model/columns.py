from collections import OrderedDict
from functools import lru_cache

COLUMNS = OrderedDict(
    (
        ("name", "Name"),
        ("tag", "Tag"),
        ("town_hall_level", "TH Level"),
        ("builder_hall_level", "BH Level"),
        ("exp_level", "XP Level"),
        ("best_trophies", "Best Trophies"),
        ("best_versus_trophies", "Best Versus Trophies"),
        ("trophies", "Current Trophies"),
        ("versus_trophies", "Builder Hall Trophies"),
        ("attack_wins", "Attack Wins"),
        ("versus_battle_win_count", "Versus Battle Wins"),
        ("defense_wins", "Defense Wins"),
        ("gold_grab", "Total Gold Grab"),
        ("elixir_escapade", "Total Elixir Grab"),
        ("heroic_heist", "Total DE Grab"),
        ("war_hero", "Total War Stars"),
        ("games_champion", "Clan Games XP"),
        ("war_league_legend", "CWL Stars"),
        ("friend_in_need", "Total Donations"),
        ("sharing_is_caring", "Total Spells Donated"),
        ("donations", "Donations"),
        ("donations_received", "Donations Received"),
        ("home_barbarian_king", "Barbarian King"),
        ("home_archer_queen", "Archer Queen"),
        ("home_grand_warden", "Grand Warden"),
        ("home_royal_champion", "Royal Champion"),
        ("home_lassi", "L.a.s.s.i."),
        ("home_electro_owl", "Electro Owl"),
        ("home_mighty_yak", "Mighty Yak"),
        ("home_unicorn", "Unicorn"),
        ("builderbase_battle_machine", "Battle Machine"),
    )
)

REVERSE_LABELS = {value: key for key, value in COLUMNS.items()}


@lru_cache(maxsize=None)
def column_group(column):
    column = REVERSE_LABELS.get(column, column).lower()
    if column in ("name", "tag", "town_hall_level", "builder_hall_level", "exp_level", "activity score"):
        return "basic"
    elif column in ("best_trophies", "best_versus_trophies", "trophies", "versus_trophies"):
        return "trophies"
    elif column in ("donations", "donations_received", "friend_in_need", "sharing_is_caring"):
        return "donations"
    elif column in (
        "home_barbarian_king",
        "home_archer_queen",
        "home_grand_warden",
        "home_royal_champion",
        "home_lassi",
        "home_electro_owl",
        "home_mighty_yak",
        "home_unicorn",
        "builderbase_battle_machine",
    ):
        return "heroes"
    elif column in ("attack_wins", "versus_battle_win_count", "defense_wins"):
        return "wins"
    elif column in ("gold_grab", "elixir_escapade", "heroic_heist"):
        return "loot"
    elif column in ("war_hero", "games_champion", "war_league_legend") or "war" in column:
        return "war"
    else:
        return "unknown"
