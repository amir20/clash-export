from datetime import datetime

from mongoengine import BooleanField, DateTimeField, Document, FloatField, IntField, StringField

from clashleaders.model import Player


class AverageTroops(Document):
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

    @classmethod
    def update_all(cls):
        good_tag = Player._get_collection().find_one(
            {"lab_levels.home_Stone Slammer": {"$exists": True}, "lab_levels.home_Bat Spell": {"$exists": True}})['tag']
        good_player = Player.find_by_tag(good_tag)

        group = {"$group": {"_id": "$townHallLevel"}}
        for key in good_player.lab_levels.keys():
            group['$group'][f"avg_{key}"] = {"$avg": f"$lab_levels.{key}"}

        aggregated = list(Player.objects.aggregate(group))
