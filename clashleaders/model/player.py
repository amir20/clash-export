import json
from codecs import decode, encode

import pandas as pd
from mongoengine import DynamicDocument, BinaryField, signals, StringField, DictField
from pymongo import ReplaceOne
from slugify import slugify

from clashleaders.clash import api, player_calculation
from clashleaders.model import Clan
import clashleaders.model
from clashleaders.model.clan import prepend_hash


class Player(DynamicDocument):
    COMPRESSED_FIELDS = ['achievements', 'clan', 'heroes', 'league', 'legendStatistics', 'spells', 'troops']

    binary_bytes = BinaryField()
    tag = StringField(required=True, unique=True)
    lab_levels = DictField()
    slug = StringField(unique=True)

    meta = {
        'index_background': True,
        'indexes': [
            'name',
            'tag',
            'townHallWeaponLevel',
            'townHallLevel',
            'trophies',
            'warStars',
            'expLevel',
            'builderHallLevel',
            'defenseWins',
            'attackWins',
            'donations',
            'slug'
        ]
    }

    def as_replace_one(self):
        return ReplaceOne({'tag': self.tag}, self.compressed_fields(), upsert=True)

    def most_recent_clan(self):
        return Clan.find_by_tag(self.clan['tag'])

    def player_score(self):
        return self.most_recent_clan().historical_near_now().activity_score_series()[self.tag]

    def to_historical_df(self):
        series = clashleaders.model.HistoricalPlayer.objects(tag=self.tag)
        return pd.DataFrame((p.to_series() for p in series))

    def compressed_fields(self):
        fields = vars(self).copy()

        for key in list(fields.keys()):
            if key.startswith('_'):
                del fields[key]

        fields['tag'] = self.tag
        fields['lab_levels'] = fields.get('lab_levels', {})
        for lab in fields.get('heroes', []) + fields.get('troops', []) + fields.get('spells', []):
            key = f"{lab['village']}_{lab['name'].replace('.', '')}"
            fields['lab_levels'][key] = lab['level']

        binary_bytes = dict()
        for f in Player.COMPRESSED_FIELDS:
            if f in fields:
                binary_bytes[f] = fields[f]
                del fields[f]

        fields['binary_bytes'] = encode_data(binary_bytes)

        fields['slug'] = slugify(f"{self.name}-{self.tag}", to_lower=True)

        return fields

    def fetch_and_update(self):
        return Player.fetch_and_save(self.tag)

    def troop_insights(self):
        return player_calculation.next_troop_recommendation(self.tag)

    def __repr__(self):
        return "<Player {0}>".format(self.tag)

    @classmethod
    def upsert_player(cls, player_tag, **kwargs):
        player = Player.objects(tag=player_tag).first()

        if not player:
            player = Player(**kwargs).save()
        else:
            # This is ugly but update() doesn't trigger pre_save
            for key, value in kwargs.items():
                setattr(player, key, value)
            player.save()

        return player

    @classmethod
    def fetch_and_save(cls, tag):
        data = api.find_player_by_tag(tag)
        return Player.upsert_player(player_tag=data['tag'], **data)

    @classmethod
    def find_by_slug(cls, slug):
        return Player.objects(slug=slug).first()

    @classmethod
    def find_by_tag(cls, tag):
        tag = prepend_hash(tag)
        player = Player.objects(tag=tag).first()

        if player is None:
            player = Player.fetch_and_save(tag)

        return player

    @classmethod
    def post_init(cls, sender, document, **kwargs):
        if document.binary_bytes:
            data = decode_data(document.binary_bytes)

            for f in cls.COMPRESSED_FIELDS:
                if f in data:
                    setattr(document, f, data[f])

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.heroes = document.heroes or []
        document.troops = document.troops or []
        document.spells = document.spells or []

        for lab in document.heroes + document.troops + document.spells:
            key = f"{lab['village']}_{lab['name'].replace('.', '')}"
            document.lab_levels[key] = lab['level']

        data = dict()
        for f in cls.COMPRESSED_FIELDS:
            if hasattr(document, f):
                data[f] = getattr(document, f)
                delattr(document, f)

        document.binary_bytes = encode_data(data)
        document.slug = slugify(f"{document.name}-{document.tag}", to_lower=True)


signals.post_init.connect(Player.post_init, sender=Player)
signals.pre_save.connect(Player.pre_save, sender=Player)
signals.post_save.connect(Player.post_init, sender=Player)


def encode_data(map):
    s = json.dumps(map)
    return encode(s.encode('utf8'), 'zlib')


def decode_data(b):
    return json.loads(decode(b, 'zlib'))
