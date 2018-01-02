from datetime import datetime, timedelta

from bson.objectid import ObjectId
from clashstats.clash import api
from mongoengine import *


class Clan(DynamicDocument):
    meta = {
        'indexes': [
            'name',
            'tag'
        ]
    }

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
        if not tag.startswith('#'):
            tag = '#' + tag

        object_id = object_id_from_now(**kwargs)
        return cls.objects(id__gte=object_id, tag=tag)

    @classmethod
    def fetch_and_save(cls, tag):
        if not tag.startswith('#'):
            tag = '#' + tag
        clan = api.find_clan_by_tag(tag)
        players = api.fetch_all_players(clan)
        clan['players'] = players
        del clan['memberList']

        clan = Clan(**clan).save()
        return clan


def object_id_from_now(**kwargs):
    now = datetime.now()
    dt = now - timedelta(**kwargs)
    return ObjectId.from_datetime(dt)
