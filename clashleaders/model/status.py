from datetime import datetime, timedelta

from mongoengine import DateTimeField, DictField, Document, FloatField, IntField, ListField, ReferenceField

from clashleaders.model import ClanPreCalculated, Player, Clan
from clashleaders.views.index import aggregate_by_country


class Status(Document):
    last_updated = DateTimeField(default=datetime.now)
    total_clans = IntField(default=0)
    total_active_clans = IntField(default=0)
    total_members = IntField(default=0)
    total_active_members = IntField(default=0)
    total_countries = IntField(default=0)
    ratio_indexed = FloatField(default=0)
    popular_clans = ListField(ReferenceField(ClanPreCalculated))
    top_countries = ListField(DictField())
    reddit_clans = ListField(ReferenceField(ClanPreCalculated))

    @classmethod
    def get_instance(cls):
        return Status.objects.first()

    @classmethod
    def update_status(cls):
        twelve_hour_ago = datetime.now() - timedelta(hours=12)
        total_clans = Clan.objects.count()
        total_eligible_clans = ClanPreCalculated.active_clans().count()
        not_indexed_clans = ClanPreCalculated.active_clans(twelve_hour_ago).count()
        ratio_indexed = 100 * ((total_eligible_clans - not_indexed_clans) / total_eligible_clans)
        Status.objects.upsert_one(
            set__ratio_indexed=ratio_indexed,
            set__total_clans=total_clans,
            set__total_active_clans=total_eligible_clans,
            set__last_updated=datetime.now(),
            set__total_members=Player.objects.count(),
            set__total_active_members=ClanPreCalculated.active_clans().sum('members'),
            set__total_countries=len(Clan.objects.distinct('location.countryCode')),
            set__popular_clans=Clan.objects.order_by('-page_views').limit(10),
            set__top_countries=aggregate_by_country("week_delta.avg_attack_wins"),
            set__reddit_clans=Clan.objects(verified_accounts='reddit').order_by('-clanPoints').limit(10),
        )
