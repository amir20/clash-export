from __future__ import annotations
from clashleaders.model.clan_war import ClanWar
from typing import Optional

import json
from codecs import decode, encode
from typing import Dict

import pandas as pd
from mongoengine import DynamicDocument, BinaryField, signals, StringField, DictField
from pymongo import ReplaceOne
from slugify import slugify

import clashleaders.insights.troops
import clashleaders.model
from clashleaders.clash import api
from clashleaders.insights.player_activity import clan_history
from clashleaders.model import Clan
from clashleaders.util import correct_tag
from mongoengine.fields import BooleanField


class Player(DynamicDocument):
    COMPRESSED_FIELDS = ["achievements", "clan", "heroes", "league", "legendStatistics", "spells", "troops"]

    binary_bytes = BinaryField()
    tag = StringField(required=True, unique=True)
    lab_levels = DictField()
    slug = StringField(unique=True)
    active = BooleanField(default=False)

    meta = {
        "index_background": True,
        "indexes": [
            "tag",
            "slug",
            "active",
        ],
    }

    def as_replace_one(self) -> ReplaceOne:
        return ReplaceOne({"tag": self.tag}, self.compressed_fields(), upsert=True)

    def most_recent_clan(self) -> Optional[Clan]:
        return Clan.find_by_tag(self.clan["tag"]) if "clan" in self else None

    def player_score(self):
        clan = self.most_recent_clan()
        if clan:
            return clan.historical_near_now().activity_score_series().get(self.tag)
        else:
            return None

    def war_stats(self):
        tag = self.tag
        [result] = list(
            ClanWar.objects.aggregate(
                {"$match": {"clan.members.tag": tag}},
                {"$unwind": {"path": "$clan.members"}},
                {"$match": {"clan.members.tag": tag}},
                {"$unwind": {"path": "$clan.members.attacks"}},
                {
                    "$group": {
                        "_id": "$clan.members.tag",
                        "avg_stars": {"$avg": "$clan.members.attacks.stars"},
                        "avg_destruction": {"$avg": "$clan.members.attacks.destructionPercentage"},
                    }
                },
            )
        )
        del result["_id"]
        return result

    def to_historical_df(self) -> pd.DataFrame:
        series = clashleaders.model.HistoricalPlayer.objects(tag=self.tag)
        return pd.DataFrame(p.to_series() for p in series)

    def compressed_fields(self):
        fields = vars(self).copy()

        for key in list(fields.keys()):
            if key.startswith("_"):
                del fields[key]

        fields["tag"] = self.tag
        fields["lab_levels"] = fields.get("lab_levels", {})
        for lab in fields.get("heroes", []) + fields.get("troops", []) + fields.get("spells", []):
            key = f"{lab['village']}_{lab['name'].replace('.', '')}"
            fields["lab_levels"][key] = lab["level"]

        binary_bytes = dict()
        for f in Player.COMPRESSED_FIELDS:
            if f in fields:
                binary_bytes[f] = fields[f]
                del fields[f]

        fields["binary_bytes"] = encode_data(binary_bytes)

        fields["slug"] = slugify(f"{self.name}-{self.tag}", to_lower=True)

        return fields

    def fetch_and_update(self) -> Player:
        return Player.fetch_and_save(self.tag)

    def troop_insights(self):
        return clashleaders.insights.troops.next_troop_recommendation(self)

    def clan_history(self):
        history = clan_history(self).to_dict()
        clans = {c.tag: c for c in Clan.objects(tag__in=list(history.values()))}
        history = {k: clans[v] for k, v in history.items()}

        return history

    def __repr__(self):
        return "<Player {0}>".format(self.tag)

    def to_dict(self, include_score=False) -> Dict:
        data = dict(self.to_mongo())
        del data["_id"]
        del data["binary_bytes"]

        if include_score:
            data["percentile"] = self.player_score()

        if data["clan"]:
            data["clan"]["slug"] = Clan.find_by_tag(data["clan"]["tag"]).slug

        return data

    @classmethod
    def upsert_player(cls, player_tag, **kwargs):
        player = Player.objects(tag=player_tag).first()

        if not player:
            player = Player(**kwargs).save()
        else:
            # This is ugly but update() doesn't trigger pre_save
            for key, value in kwargs.items():
                setattr(player, key, value)

            if "clan" not in kwargs:
                player.clan = None

            player.save()

        return player

    @classmethod
    def fetch_and_save(cls, tag):
        data = api.find_player_by_tag(tag)
        return Player.upsert_player(player_tag=data["tag"], **data)

    @classmethod
    def find_by_slug(cls, slug) -> Player:
        return Player.objects.get(slug=slug)

    @classmethod
    def find_by_tag(cls, tag) -> Player:
        tag = correct_tag(tag)
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
            document.lab_levels[key] = lab["level"]

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
    return encode(s.encode("utf8"), "zlib")


def decode_data(b):
    return json.loads(decode(b, "zlib"))
