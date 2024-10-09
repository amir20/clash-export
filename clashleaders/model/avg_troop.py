import re
from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    FloatField,
    IntField,
    StringField,
)

import clashleaders.model.player


class AverageTroop(Document):
    last_updated = DateTimeField(default=datetime.now)
    th_level = IntField(required=True)
    name = StringField(required=True)
    is_builder_base = BooleanField(required=True)
    avg = FloatField(required=True)
    max = FloatField()

    meta = {"indexes": ["last_updated", "th_level", "name"]}

    @property
    def base(self):
        return "builderbase" if self.is_builder_base else "home"

    @property
    def troop_id(self):
        return f"{self.base}_{self.name}"

    @classmethod
    def update_all(cls):
        good_tag = clashleaders.model.player.Player._get_collection().find_one(
            {
                "lab_levels.home_unicorn": {"$exists": True},
                "lab_levels.builderbase_battle_machine": {"$exists": True},
                "lab_levels.builderbase_super_pekka": {"$exists": True},
            }
        )["tag"]
        good_player = clashleaders.model.player.Player.find_by_tag(good_tag)

        group = {"$group": {"_id": "$townHallLevel"}}
        for key in good_player.lab_levels.keys():
            group["$group"][f"avg_{key}"] = {"$avg": f"$lab_levels.{key}"}
            group["$group"][f"max_{key}"] = {"$max": f"$lab_levels.{key}"}

        aggregated = list(clashleaders.model.player.Player.objects.aggregate(group))

        for th_avg in aggregated:
            th_level = th_avg["_id"]
            for key, value in th_avg.items():
                if key.startswith("avg_"):
                    splits = re.split(r"_(builderBase|home)_", key)
                    is_builder_base = "builderbase" == splits[1]
                    name = splits[2]
                    AverageTroop.objects(
                        th_level=th_level, is_builder_base=is_builder_base, name=name
                    ).update_one(
                        set__th_level=th_level,
                        set__is_builder_base=is_builder_base,
                        set__name=name,
                        set__avg=value,
                        set__max=th_avg[key.replace("avg_", "max_", 1)],
                        set__last_updated=datetime.now(),
                        upsert=True,
                    )
