import json
import logging
from codecs import decode, encode
from datetime import datetime, timedelta

from bson.objectid import ObjectId
from mongoengine import BinaryField, DynamicDocument, DoesNotExist

import clashleaders.clash.clan_calculation
import clashleaders.clash.player_calculation
import clashleaders.clash.transformer
import clashleaders.model
from clashleaders.clash import api

logger = logging.getLogger(__name__)


class Clan(DynamicDocument):
    players_bytes = BinaryField()
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
        return clashleaders.clash.clan_calculation.update_calculations(self)

    def players_data(self):
        return self.players if 'players' in self else decode_player_bytes(self.players_bytes)

    def to_data_frame(self):
        return clashleaders.clash.transformer.to_data_frame(self)

    def series(self, columns=None):
        if columns is None:
            columns = ['players_bytes']
        return Clan.from_now_with_tag(self.tag, days=28).no_cache().only(*columns)

    def to_player_matrix(self):
        return clashleaders.clash.player_calculation.df_to_matrix(
            clashleaders.clash.player_calculation.augment_with_percentiles(self))

    def from_before(self, **kwargs):
        dt = self.created_on - timedelta(**kwargs)
        object_id = ObjectId.from_datetime(dt)
        return Clan.objects(tag=self.tag, id__gte=object_id).order_by('id').first()

    @property
    def created_on(self):
        return self.id.generation_time

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
    def find_most_recent_by_tag(cls, tag):
        return cls.from_now_with_tag(tag=prepend_hash(tag), hours=13).order_by('-id').first()

    @classmethod
    def find_least_recent_by_tag(cls, tag):
        return cls.objects(tag=prepend_hash(tag)).first()

    @classmethod
    def fetch_and_save(cls, tag):
        tag = prepend_hash(tag)
        clan = api.find_clan_by_tag(tag)
        players = api.fetch_all_players(clan)
        save_historical_clan(clan, players)
        clan['players_bytes'] = encode_players(players)
        del clan['memberList']

        clan = Clan(**clan).save()

        try:
            cpc = clan.pre_calculated()
            cpc.most_recent = clan
            cpc.save()
        except DoesNotExist:
            # don't do anything
            pass

        try:
            df = clan.to_data_frame()
            clan['avg_gold_grab'] = df['Total Gold Grab'].mean()
            clan['avg_elixir_grab'] = df['Total Elixir Grab'].mean()
            clan['avg_de_grab'] = df['Total DE Grab'].mean()
            clan.save()
        except:
            logging.exception("Error while saving averages for loot in clan#fetch_and_save()")

        return clan


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
