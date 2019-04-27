from __future__ import annotations

from inflection import camelize
from mongoengine import EmbeddedDocument, FloatField, IntField
from typing import Dict


class ClanDelta(EmbeddedDocument):
    avg_donations = FloatField(default=0)
    avg_donations_received = FloatField(default=0)
    avg_gold_grab = FloatField(default=0)
    avg_elixir_grab = FloatField(default=0)
    avg_de_grab = FloatField(default=0)
    avg_war_stars = FloatField(default=0)
    avg_attack_wins = FloatField(default=0)
    avg_versus_wins = FloatField(default=0)
    total_trophies = IntField(default=0)
    total_bh_trophies = IntField(default=0)
    total_gold_grab = IntField(default=0)
    total_elixir_grab = IntField(default=0)
    total_de_grab = IntField(default=0)
    total_donations = IntField(default=0)
    total_attack_wins = IntField(default=0)
    total_versus_wins = IntField(default=0)

    def to_dict(self, camel_case=False) -> Dict:
        data: Dict = dict(self.to_mongo())

        if camel_case:
            data = {camelize(k, False): v for k, v in data.items()}

        return data
