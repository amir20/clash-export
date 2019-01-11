import json
import logging
from codecs import decode, encode
from datetime import datetime, timedelta

from bson.objectid import ObjectId
from mongoengine import DynamicDocument, DateTimeField, StringField, IntField, ListField, EmbeddedDocumentField
from slugify import slugify

import clashleaders.clash.clan_calculation
import clashleaders.clash.player_calculation
import clashleaders.clash.transformer
import clashleaders.model
import clashleaders.queue.calculation
import clashleaders.queue.player
from clashleaders.clash import api
from clashleaders.model.clan_delta import ClanDelta

logger = logging.getLogger(__name__)


class Clan(DynamicDocument):
    updated_on = DateTimeField(default=datetime.now)
    tag = StringField(required=True, unique=True)
    slug = StringField(required=True)
    cluster_label = IntField(default=-1)
    verified_accounts = ListField(StringField())
    computed = EmbeddedDocumentField(ClanDelta)
    week_delta = EmbeddedDocumentField(ClanDelta)

    meta = {
        'index_background': True,
        'indexes': [
            'name',
            'updated_on',
            'location.countryCode',
            'cluster_label',
            'verified_accounts'
            'clanPoints',
            'tag',
            'slug',
            'members'
        ]
    }

    def update_calculations(self):
        return clashleaders.clash.clan_calculation.update_calculations(self)

    def historical(self):
        return clashleaders.model.HistoricalClan.objects(tag=self.tag)

    def historical_near_time(self, dt):
        return clashleaders.model.HistoricalClan.find_by_tag_near_time(tag=self.tag, dt=dt)

    def historical_near_now(self):
        return clashleaders.model.HistoricalClan.find_by_tag_near_time(tag=self.tag, dt=datetime.now())

    def __repr__(self):
        return "<Clan {0}>".format(self.tag)

    @classmethod
    def find_by_tag(cls, tag):
        tag = prepend_hash(tag)
        return Clan.objects.get(tag=tag)

    @classmethod
    def find_by_slug(cls, slug):
        return Clan.objects.get(slug=slug)

    @classmethod
    def fetch_and_update(cls, tag):
        tag = prepend_hash(tag)

        # Fetch from API
        clan_response = api.find_clan_by_tag(tag)
        players_response = api.fetch_all_players(clan_response)

        # Store all players data using historical compressed format
        save_historical_clan(clan_response, players_response)

        # Enqueue player json to queue
        clashleaders.queue.player.update_players.delay(players_response)

        clan_response['clan_type'] = clan_response['type']
        del clan_response['type']
        clan_response['slug'] = slugify(f"{clan_response['name']}-{tag}", to_lower=True)
        clan_response['updated_on'] = datetime.now()

        # Update calculations in a queue
        clashleaders.queue.calculation.update_calculations.delay(tag)

        return Clan.objects(tag=tag).upsert_one(**clan_response)


def prepend_hash(tag):
    return "#" + tag.lstrip("#").upper()


def object_id_from_now(**kwargs):
    now = datetime.now()
    dt = now - timedelta(**kwargs)
    return ObjectId.from_datetime(dt)


def encode_players(players):
    s = json.dumps(players)
    return encode(s.encode('utf8'), 'zlib')


def decode_player_bytes(b):
    return json.loads(decode(b, 'zlib'))


def save_historical_clan(clan_json, player_json):
    try:
        players = [clashleaders.model.HistoricalPlayer(**p).save() for p in player_json]
        clashleaders.model.HistoricalClan(**clan_json, players=players).save()
    except:
        logging.exception("Error while saving save_historical_clan")
