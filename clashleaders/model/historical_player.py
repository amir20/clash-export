import logging
from datetime import datetime
from functools import lru_cache

import pandas as pd
from inflection import *
from mongoengine import BinaryField, DateTimeField, Document, StringField

from clashleaders.proto.player_stats_pb2 import PlayerStats

logger = logging.getLogger(__name__)

OTHER_STATS = [
    "attackWins",
    "bestTrophies",
    "bestVersusTrophies",
    "builderHallLevel",
    "townHallLevel",
    "townHallWeaponLevel",
    "trophies",
    "versusBattleWinCount",
    "versusBattleWins",
    "versusTrophies",
    "warStars",
    "defenseWins",
    "donations",
    "donationsReceived",
    "expLevel",
]


VALID_NAMES = {f.name for f in PlayerStats.DESCRIPTOR.fields}


class HistoricalPlayer(Document):
    created_on = DateTimeField(default=datetime.now)
    tag = StringField(required=True)
    clan_tag = StringField()
    name = StringField(required=True)
    bytes = BinaryField(required=True)

    meta = {"index_background": True, "indexes": ["tag", "clan_tag", "created_on", ("tag", "created_on")]}

    def __init__(self, *args, **kwargs):
        if "bytes" in kwargs:
            super().__init__(*args, **kwargs)
            self.stats = PlayerStats().FromString(self.bytes)
        else:
            player_stats = dict()
            for lab in kwargs["heroes"] + kwargs["troops"] + kwargs["spells"]:
                key = to_mapping(f"{lab['village']}/{lab['name'].replace('.', '')}")
                player_stats[key] = lab["level"]

            for a in kwargs["achievements"]:
                key = to_mapping(a["name"])
                player_stats[key] = a["value"]

            for k, v in kwargs.items():
                if k in OTHER_STATS:
                    key = to_mapping(k)
                    player_stats[key] = v

            valid_stats = {k: v for k, v in player_stats.items() if k in VALID_NAMES}
            if new_keys := (player_stats.keys() - valid_stats.keys()):
                logger.info("Unrecognized keys for player: %s", new_keys)
            self.stats = PlayerStats(**valid_stats)
            super().__init__(tag=kwargs["tag"], clan_tag=kwargs["clan"]["tag"], name=kwargs["name"], bytes=self.stats.SerializeToString())

    def __repr__(self):
        return "<HistoricalPlayer {0}>".format(self.tag)

    def __str__(self):
        return "<HistoricalPlayer {0}>".format(self.tag)

    def to_dict(self):
        d = {f: getattr(self.stats, f) for f in self.stats.DESCRIPTOR.fields_by_name}
        d["name"] = self.name
        d["tag"] = self.tag
        d["clan_tag"] = self.clan_tag
        return d

    def to_series(self):
        return pd.Series(self.to_dict(), name=self.created_on)


@lru_cache(maxsize=256)
def to_mapping(name):
    if name in OTHER_STATS:
        return underscore(name)
    else:
        return underscore(parameterize(name))
