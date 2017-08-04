from datetime import datetime, timedelta

from bson.objectid import ObjectId
from mongoengine import DynamicDocument
from clash import api


class Player(DynamicDocument):
    meta = {
        'indexes': [
            'clan.name',
            'clan.tag',
            'name',
            'tag'
        ]
    }


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
    def from_now_with_tag(cls, tag, **kwargs):
        object_id = object_id_from_now(**kwargs)
        return cls.objects(id__gte=object_id, tag=tag)

    @classmethod
    def fetch_and_save(cls, tag):
        clan = api.find_clan_by_tag(tag)
        responses = api.fetch_all_players(clan)
        players = [r.json() for r in responses]
        clan['players'] = players
        del clan['memberList']

        [Player(**r).save() for r in players]

        return Clan(**clan).save()


def object_id_from_now(**kwargs):
    now = datetime.now()
    dt = now - timedelta(**kwargs)
    return ObjectId.from_datetime(dt)
