from datetime import datetime, timedelta

from mongoengine import DateTimeField, DictField, Document, FloatField, IntField, ListField, ReferenceField

from clashleaders.model import ClanPreCalculated
from clashleaders.views.index import aggregate_by_country


class Status(Document):
    last_updated = DateTimeField(default=datetime.now)
    total_clans = IntField(default=0)
    total_members = IntField(default=0)
    total_countries = IntField(default=0)
    ratio_indexed = FloatField(default=0)
    popular_clans = ListField(ReferenceField(ClanPreCalculated))
    top_countries = ListField(DictField())
    reddit_clans = ListField(ReferenceField(ClanPreCalculated))

    @classmethod
    def update_status(cls):
        twelve_hour_ago = datetime.now() - timedelta(hours=12)
        total_clans = ClanPreCalculated.objects.count()
        ratio_indexed = 100 * (ClanPreCalculated.objects(last_updated__gt=twelve_hour_ago).count() / total_clans)
        Status.objects.update_one(
            set__ratio_indexed=ratio_indexed,
            set__total_clans=total_clans,
            set__last_updated=datetime.now(),
            set__total_members=ClanPreCalculated.objects.sum('members'),
            set__total_countries=len(ClanPreCalculated.objects.distinct('location.countryCode')),
            set__popular_clans=ClanPreCalculated.objects.order_by('-page_views').limit(10),
            set__top_countries=aggregate_by_country("week_delta.avg_attack_wins"),
            set__reddit_clans=ClanPreCalculated.objects(verified_accounts='reddit').order_by('-clanPoints').limit(10),
            upsert=True
        )
