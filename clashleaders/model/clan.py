from datetime import datetime, timedelta

from bson.objectid import ObjectId
from mongoengine import DynamicDocument

import clashleaders.clash.calculation
import clashleaders.model
from clashleaders.clash import api


class Clan(DynamicDocument):
    meta = {
        'index_background': True,
        'indexes': [
            'name',
            'tag',
            ('tag', '_id'),
            'members'
        ]
    }

    def pre_calculated(self):
        return clashleaders.model.ClanPreCalculated.find_by_tag(self.tag)

    def update_calculations(self):
        return clashleaders.clash.calculation.update_calculations(self)

    @classmethod
    def from_now(cls, **kwargs):
        object_id = object_id_from_now(**kwargs)
        return cls.objects(id__gte=object_id)

    @classmethod
    def older_than(cls, **kwargs):
        object_id = object_id_from_now(**kwargs)
        return cls.objects(id__lt=object_id)

    @classmethod
    def from_now_with_tag(cls, tag, **kwargs):
        object_id = object_id_from_now(**kwargs)
        return cls.objects(id__gte=object_id, tag=prepend_hash(tag))

    @classmethod
    def find_first_by_tag(cls, tag):
        return cls.from_now_with_tag(tag=prepend_hash(tag), hours=13).order_by('-id').first()

    @classmethod
    def find_last_by_tag(cls, tag):
        return cls.objects(tag=prepend_hash(tag)).first()

    @classmethod
    def fetch_and_save(cls, tag):
        tag = prepend_hash(tag)
        clan = api.find_clan_by_tag(tag)
        players = api.fetch_all_players(clan)
        clan['players'] = players
        del clan['memberList']

        clan = Clan(**clan).save()
        return clan


def prepend_hash(tag):
    return "#" + tag.lstrip("#")


def object_id_from_now(**kwargs):
    now = datetime.now()
    dt = now - timedelta(**kwargs)
    return ObjectId.from_datetime(dt)
