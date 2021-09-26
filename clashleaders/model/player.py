from __future__ import annotations
from clashleaders.model.historical_player import HistoricalPlayer
from clashleaders.model.clan_war import ClanWar
from typing import Optional

import json
from codecs import decode, encode
from typing import Dict
from collections import namedtuple

import pandas as pd
from mongoengine import Document, BinaryField, signals, StringField, DictField
from slugify import slugify

import clashleaders.insights.troops
import clashleaders.model
from clashleaders.clash import api
from clashleaders.insights.player_activity import clan_history
from clashleaders.model import Clan
from clashleaders.util import correct_tag
from mongoengine.fields import BooleanField, ReferenceField


class Player(Document):
    binary_bytes = BinaryField()
    tag = StringField(required=True, unique=True)
    name = StringField(required=True)
    role = StringField()
    lab_levels = DictField()
    slug = StringField(unique=True)
    active = BooleanField(default=True)
    most_recent = ReferenceField(HistoricalPlayer)
    clan = DictField()
    league = DictField()

    meta = {
        "index_background": True,
        "indexes": [
            "tag",
            "slug",
            "active",
        ],
        "strict": False,
    }

    def most_recent_clan(self) -> Optional[Clan]:
        return Clan.find_by_tag(self.clan["tag"]) if hasattr(self, "clan") and "tag" in self.clan else None

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

    def fetch_and_update(self) -> Player:
        return Player.fetch_and_save(self.tag)

    def troop_insights(self):
        return clashleaders.insights.troops.next_troop_recommendation(self)

    def fetch_troops(self):
        data = api.find_player_by_tag(self.tag)
        return namedtuple("PlayerResponse", data.keys())(*data.values())

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
    def upsert_player(cls, player_tag, **data):
        most_recent = HistoricalPlayer(**data).save()

        data = {
            "tag": player_tag,
            "name": data["name"],
            "lab_levels": lab_levels(most_recent),
            "most_recent": most_recent,
            "clan": data.get("clan"),
            "league": data.get("league"),
            "role": data.get("role"),
            "slug": slugify(f'{data["name"]}-{player_tag}', to_lower=True),
        }

        return Player.objects(tag=player_tag).upsert_one(**data)

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


def lab_levels(most_recent):
    return {key: value for key, value in most_recent.to_dict().items() if key.startswith("home_") or key.startswith("builderbase_")}
