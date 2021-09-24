from __future__ import annotations
from clashleaders.model.historical_player import HistoricalPlayer
from clashleaders.model.clan_war import ClanWar
from typing import Optional

import json
from codecs import decode, encode
from typing import Dict
from collections import namedtuple

import pandas as pd
from mongoengine import Document, BinaryField, signals, StringField, DictField
from slugify import slugify

import clashleaders.insights.troops
import clashleaders.model
from clashleaders.clash import api
from clashleaders.insights.player_activity import clan_history
from clashleaders.model import Clan
from clashleaders.util import correct_tag
from mongoengine.fields import BooleanField, ReferenceField


HEROS = {"home_barbarian_king", "home_archer_queen", "home_grand_warden", "builderbase_battle_machine", "home_royal_champion"}
LABELS = {
    "home_barbarian_king": "home/Barbarian King",
    "home_archer_queen": "home/Archer Queen",
    "home_grand_warden": "home/Grand Warden",
    "builderbase_battle_machine": "builderBase/Battle Machine",
    "home_royal_champion": "home/Royal Champion",
    "home_barbarian": "home/Barbarian",
    "home_archer": "home/Archer",
    "home_goblin": "home/Goblin",
    "home_giant": "home/Giant",
    "home_wall_breaker": "home/Wall Breaker",
    "home_balloon": "home/Balloon",
    "home_wizard": "home/Wizard",
    "home_healer": "home/Healer",
    "home_dragon": "home/Dragon",
    "home_pekka": "home/PEKKA",
    "home_minion": "home/Minion",
    "home_hog_rider": "home/Hog Rider",
    "home_valkyrie": "home/Valkyrie",
    "home_golem": "home/Golem",
    "home_witch": "home/Witch",
    "home_lava_hound": "home/Lava Hound",
    "home_bowler": "home/Bowler",
    "home_baby_dragon": "home/Baby Dragon",
    "home_miner": "home/Miner",
    "home_super_barbarian": "home/Super Barbarian",
    "home_super_archer": "home/Super Archer",
    "home_super_wall_breaker": "home/Super Wall Breaker",
    "home_super_giant": "home/Super Giant",
    "builderbase_raged_barbarian": "builderBase/Raged Barbarian",
    "builderbase_sneaky_archer": "builderBase/Sneaky Archer",
    "builderbase_beta_minion": "builderBase/Beta Minion",
    "builderbase_boxer_giant": "builderBase/Boxer Giant",
    "builderbase_bomber": "builderBase/Bomber",
    "builderbase_super_pekka": "builderBase/Super PEKKA",
    "builderbase_cannon_cart": "builderBase/Cannon Cart",
    "builderbase_drop_ship": "builderBase/Drop Ship",
    "builderbase_baby_dragon": "builderBase/Baby Dragon",
    "builderbase_night_witch": "builderBase/Night Witch",
    "home_wall_wrecker": "home/Wall Wrecker",
    "home_battle_blimp": "home/Battle Blimp",
    "home_yeti": "home/Yeti",
    "home_sneaky_goblin": "home/Sneaky Goblin",
    "home_rocket_balloon": "home/Rocket Balloon",
    "home_ice_golem": "home/Ice Golem",
    "home_electro_dragon": "home/Electro Dragon",
    "home_stone_slammer": "home/Stone Slammer",
    "home_inferno_dragon": "home/Inferno Dragon",
    "home_super_valkyrie": "home/Super Valkyrie",
    "home_dragon_rider": "home/Dragon Rider",
    "home_super_witch": "home/Super Witch",
    "builderbase_hog_glider": "builderBase/Hog Glider",
    "home_siege_barracks": "home/Siege Barracks",
    "home_ice_hound": "home/Ice Hound",
    "home_headhunter": "home/Headhunter",
    "home_super_wizard": "home/Super Wizard",
    "home_super_minion": "home/Super Minion",
    "home_log_launcher": "home/Log Launcher",
    "home_lassi": "home/LASSI",
    "home_mighty_yak": "home/Mighty Yak",
    "home_electro_owl": "home/Electro Owl",
    "home_unicorn": "home/Unicorn",
    "home_lightning_spell": "home/Lightning Spell",
    "home_healing_spell": "home/Healing Spell",
    "home_rage_spell": "home/Rage Spell",
    "home_jump_spell": "home/Jump Spell",
    "home_freeze_spell": "home/Freeze Spell",
    "home_poison_spell": "home/Poison Spell",
    "home_earthquake_spell": "home/Earthquake Spell",
    "home_haste_spell": "home/Haste Spell",
    "home_clone_spell": "home/Clone Spell",
    "home_skeleton_spell": "home/Skeleton Spell",
    "home_bat_spell": "home/Bat Spell",
    "home_invisibility_spell": "home/Invisibility Spell",
    "bigger_coffers": "Bigger Coffers",
    "get_those_goblins": "Get those Goblins!",
    "bigger_better": "Bigger & Better",
    "nice_and_tidy": "Nice and Tidy",
    "discover_new_troops": "Discover New Troops",
    "gold_grab": "Gold Grab",
    "elixir_escapade": "Elixir Escapade",
    "sweet_victory": "Sweet Victory!",
    "empire_builder": "Empire Builder",
    "wall_buster": "Wall Buster",
    "humiliator": "Humiliator",
    "union_buster": "Union Buster",
    "conqueror": "Conqueror",
    "unbreakable": "Unbreakable",
    "friend_in_need": "Friend in Need",
    "mortar_mauler": "Mortar Mauler",
    "heroic_heist": "Heroic Heist",
    "league_all_star": "League All-Star",
    "x_bow_exterminator": "X-Bow Exterminator",
    "firefighter": "Firefighter",
    "war_hero": "War Hero",
    "clan_war_wealth": "Clan War Wealth",
    "anti_artillery": "Anti-Artillery",
    "sharing_is_caring": "Sharing is caring",
    "keep_your_account_safe": "Keep Your Account Safe!",
    "master_engineering": "Master Engineering",
    "next_generation_model": "Next Generation Model",
    "un_build_it": "Un-Build It",
    "champion_builder": "Champion Builder",
    "high_gear": "High Gear",
    "hidden_treasures": "Hidden Treasures",
    "games_champion": "Games Champion",
    "dragon_slayer": "Dragon Slayer",
    "war_league_legend": "War League Legend",
    "well_seasoned": "Well Seasoned",
    "shattered_and_scattered": "Shattered and Scattered",
    "not_so_easy_this_time": "Not So Easy This Time",
    "bust_this": "Bust This!",
    "superb_work": "Superb Work",
    "siege_sharer": "Siege Sharer",
}


class Player(Document):
    binary_bytes = BinaryField()
    tag = StringField(required=True, unique=True)
    name = StringField(required=True)
    role = StringField()
    lab_levels = DictField()
    slug = StringField(unique=True)
    active = BooleanField(default=True)
    most_recent = ReferenceField(HistoricalPlayer)
    clan = DictField()
    league = DictField()

    meta = {
        "index_background": True,
        "indexes": [
            "tag",
            "slug",
            "active",
        ],
        "strict": False,
    }

    def most_recent_clan(self) -> Optional[Clan]:
        return Clan.find_by_tag(self.clan["tag"]) if hasattr(self, "clan") and "tag" in self.clan else None

    def player_score(self):
        clan = self.most_recent_clan()
        if clan:
            return clan.historical_near_now().activity_score_series().get(self.tag)
        else:
            return None

    def war_stats(self):
        tag = self.tag
        [result] = list(
            ClanWar.objects.aggregate(
                {"$match": {"clan.members.tag": tag}},
                {"$unwind": {"path": "$clan.members"}},
                {"$match": {"clan.members.tag": tag}},
                {"$unwind": {"path": "$clan.members.attacks"}},
                {
                    "$group": {
                        "_id": "$clan.members.tag",
                        "avg_stars": {"$avg": "$clan.members.attacks.stars"},
                        "avg_destruction": {"$avg": "$clan.members.attacks.destructionPercentage"},
                    }
                },
            )
        )
        del result["_id"]
        return result

    def to_historical_df(self) -> pd.DataFrame:
        series = clashleaders.model.HistoricalPlayer.objects(tag=self.tag)
        return pd.DataFrame(p.to_series() for p in series)

    def fetch_and_update(self) -> Player:
        return Player.fetch_and_save(self.tag)

    def troop_insights(self):
        return clashleaders.insights.troops.next_troop_recommendation(self)

    def fetch_troops(self):
        data = api.find_player_by_tag(self.tag)
        return namedtuple("PlayerResponse", data.keys())(*data.values())

    def clan_history(self):
        history = clan_history(self).to_dict()
        clans = {c.tag: c for c in Clan.objects(tag__in=list(history.values()))}
        history = {k: clans[v] for k, v in history.items()}

        return history

    def __repr__(self):
        return "<Player {0}>".format(self.tag)

    def to_dict(self, include_score=False) -> Dict:
        data = dict(self.to_mongo())
        del data["_id"]
        del data["binary_bytes"]

        if include_score:
            data["percentile"] = self.player_score()

        if data["clan"]:
            data["clan"]["slug"] = Clan.find_by_tag(data["clan"]["tag"]).slug

        return data

    @classmethod
    def upsert_player(cls, player_tag, **data):
        most_recent = HistoricalPlayer(**data).save()

        data = {
            "tag": player_tag,
            "name": data["name"],
            "lab_levels": lab_levels(most_recent),
            "most_recent": most_recent,
            "clan": data.get("clan"),
            "league": data.get("league"),
            "role": data.get("role"),
            "slug": slugify(f'{data["name"]}-{player_tag}', to_lower=True),
        }

        return Player.objects(tag=player_tag).upsert_one(**data)

    @classmethod
    def fetch_and_save(cls, tag):
        data = api.find_player_by_tag(tag)
        return Player.upsert_player(player_tag=data["tag"], **data)

    @classmethod
    def find_by_slug(cls, slug) -> Player:
        return Player.objects.get(slug=slug)

    @classmethod
    def find_by_tag(cls, tag) -> Player:
        tag = correct_tag(tag)
        player = Player.objects(tag=tag).first()

        if player is None:
            player = Player.fetch_and_save(tag)

        return player


def lab_levels(most_recent):
    return {key: value for key, value in most_recent.to_dict().items() if key.startswith("home_") or key.startswith("builderbase_")}
