import re
from datetime import datetime

from mongoengine import BooleanField, DateTimeField, Document, FloatField, IntField, StringField

from clashleaders.model import Player


class AverageTroop(Document):
    last_updated = DateTimeField(default=datetime.now)
    th_level = IntField(required=True)
    name = StringField(required=True)
    is_builder_base = BooleanField(required=True)
    avg = FloatField(required=True)

    meta = {
        'indexes': [
            'last_updated',
            'th_level',
            'name',
        ]
    }

    @property
    def base(self):
        return "builderBase" if self.is_builder_base else "home"

    @property
    def troop_id(self):
        return f"{self.base}_{self.name}"

    @classmethod
    def update_all(cls):
        good_tag = Player._get_collection().find_one({"lab_levels.home_Stone Slammer": {"$exists": True},
                                                      "lab_levels.home_Bat Spell": {"$exists": True}}
                                                     )['tag']
        good_player = Player.find_by_tag(good_tag)

        group = {"$group": {"_id": "$townHallLevel"}}
        for key in good_player.lab_levels.keys():
            group['$group'][f"avg_{key}"] = {"$avg": f"$lab_levels.{key}"}

        aggregated = list(Player.objects.aggregate(group))

        for th_avg in aggregated:
            th_level = th_avg['_id']
            for key, value in th_avg.items():
                if key.startswith('avg_'):
                    splits = re.split(r'_(builderBase|home)_', key)
                    is_builder_base = "builderBase" == splits[1]
                    name = splits[2]
                    AverageTroop.objects(th_level=th_level, is_builder_base=is_builder_base, name=name).update_one(
                        set__th_level=th_level,
                        set__is_builder_base=is_builder_base,
                        set__name=name,
                        set__avg=value,
                        set__last_updated=datetime.now(),
                        upsert=True
                    )

