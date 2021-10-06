from __future__ import annotations

import json
import logging
import os
from os.path import join
from datetime import datetime, timedelta

from mongoengine import DateTimeField, DictField, Document, FloatField, IntField, ListField, ReferenceField

from clashleaders.model import Player, Clan

logger = logging.getLogger(__name__)

from clashleaders import site_root

with open(join(site_root, "data", "countries.json")) as f:
    data = json.load(f)
    COUNTRIES = {c["countryCode"]: c for c in data if c["isCountry"]}


class Status(Document):
    last_updated = DateTimeField(default=datetime.now)
    total_clans = IntField(default=0)
    total_active_clans = IntField(default=0)
    total_members = IntField(default=0)
    total_active_members = IntField(default=0)
    total_countries = IntField(default=0)
    ratio_indexed = FloatField(default=0)
    popular_clans = ListField(ReferenceField(Clan))
    top_countries = ListField(DictField())
    reddit_clans = ListField(ReferenceField(Clan))
    trophy_distribution = DictField()
    trophies_by_country = DictField()

    @classmethod
    def instance(cls) -> Status:
        return Status.objects.first()

    @classmethod
    def update_status(cls):
        logging.info("Updating status calculations...")
        twenty_hours_ago = datetime.now() - timedelta(hours=20)
        total_clans = Clan.objects.count()
        total_eligible_clans = Clan.active().count()
        not_indexed_clans = Clan.active(twenty_hours_ago).count()
        ratio_indexed = 100 * ((total_eligible_clans - not_indexed_clans) / total_eligible_clans)
        Status.objects.upsert_one(
            set__ratio_indexed=ratio_indexed,
            set__total_clans=total_clans,
            set__total_active_clans=total_eligible_clans,
            set__last_updated=datetime.now(),
            set__total_members=Player.objects.count(),
            set__total_active_members=Clan.active().sum("members"),
            set__total_countries=len(Clan.objects.distinct("location.countryCode")),
            set__popular_clans=Clan.objects.order_by("-page_views").limit(10),
            set__top_countries=_aggregate_by_country("week_delta.avg_attack_wins"),
            set__reddit_clans=Clan.objects(verified_accounts="reddit").order_by("-clanPoints").limit(10),
            set__trophy_distribution=_trophy_distribution(),
            set__trophies_by_country=_aggregate_by_country("clanPoints"),
        )


def _trophy_distribution():
    counts = list(
        Clan.objects.aggregate({"$group": {"_id": {"$subtract": ["$clanPoints", {"$mod": ["$clanPoints", 500]}]}, "count": {"$sum": 1}}}, {"$sort": {"_id": 1}})
    )
    labels = [c["_id"] for c in counts]
    values = [c["count"] for c in counts]
    return dict(labels=labels, values=values)


def _aggregate_by_country(score_column):
    group = {"$group": {"_id": "$location.countryCode", "score": {"$sum": f"${score_column}"}}}
    sort = {"$sort": {"score": -1}}
    aggregated = list(Clan.objects(location__countryCode__ne=None).aggregate(group, sort))
    return [{"code": c["_id"].lower(), "name": COUNTRIES[c["_id"]]["name"], "score": c["score"]} for c in aggregated[:10]]
