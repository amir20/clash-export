import logging
from datetime import datetime
from functools import lru_cache

import pandas as pd
from inflection import *
from mongoengine import Document, StringField, DateTimeField, BinaryField

from clashleaders.proto.player_stats_pb2 import PlayerStats

logger = logging.getLogger(__name__)

OTHER_STATS = [
    "attackWins"
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
    "expLevel"]


class HistoricalPlayer(Document):
    created_on = DateTimeField(default=datetime.now)
    tag = StringField(required=True)
    bytes = BinaryField(required=True)

    meta = {
        'index_background': True,
        'indexes': [
            'tag',
            'created_on',
            ('tag', 'created_on'),
        ]
    }

    def __init__(self, *args, **kwargs):
        if 'bytes' in kwargs:
            super().__init__(*args, **kwargs)
            self.stats = PlayerStats().FromString(self.bytes)
        else:
            player_stats = dict()
            for lab in kwargs['heroes'] + kwargs['troops'] + kwargs['spells']:
                key = to_mapping(f"{lab['village']}/{lab['name'].replace('.', '')}")
                player_stats[key] = lab['level']

            for a in kwargs['achievements']:
                key = to_mapping(a['name'])
                player_stats[key] = a['value']

            for k, v in kwargs.items():
                if k in OTHER_STATS:
                    key = to_mapping(k)
                    player_stats[key] = v

            stats = PlayerStats(**player_stats)
            super().__init__(tag=kwargs['tag'], bytes=stats.SerializeToString())

    def to_dict(self):
        return {f: getattr(self.stats, f) for f in self.stats.DESCRIPTOR.fields_by_name}

    def to_series(self):
        s = pd.Series(self.to_dict())
        s.name = self.tag
        return s


@lru_cache(maxsize=256)
def to_mapping(name):
    if name in OTHER_STATS:
        return underscore(name)
    else:
        return underscore(parameterize(name))
