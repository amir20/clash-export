from datetime import datetime

from mongoengine import BooleanField, DateTimeField, DictField, Document, EmbeddedDocumentField, \
    FloatField, IntField, ListField, ReferenceField, StringField

from clashleaders.model.clan import Clan
from clashleaders.model.clan_delta import ClanDelta


class ClanPreCalculated(Document):
    last_updated = DateTimeField(default=datetime.now)
    page_views = IntField(required=True, default=0)
    tag = StringField(required=True, unique=True)
    slug = StringField(required=True)
    name = StringField(required=True)
    clanLevel = IntField()  # todo make this required
    description = StringField(required=True)
    clanPoints = IntField(required=True)
    clanVersusPoints = IntField(required=True)
    members = IntField(required=True)
    badgeUrls = DictField(required=True)
    location = DictField(required=False)
    isWarLogPublic = BooleanField(required=False)

    warWinStreak = IntField(required=True)
    warWins = IntField(required=True)
    warTies = IntField(required=True)
    warLosses = IntField(required=True)

    season_start = ReferenceField(Clan)
    most_recent = ReferenceField(Clan)
    least_recent = ReferenceField(Clan)
    days_span = IntField(default=0)

    avg_donations = FloatField(required=True)
    avg_gold_grab = FloatField(required=True)
    avg_elixir_grab = FloatField(required=True)
    avg_de_grab = FloatField(required=True)
    avg_war_stars = FloatField(required=True)
    avg_th_level = FloatField(required=True)
    avg_bh_level = FloatField(required=True)
    avg_xp_level = FloatField(required=True)
    avg_best_trophies = FloatField(required=True)
    avg_trophies = FloatField(required=True)
    avg_bh_trophies = FloatField(required=True)
    avg_bk_level = FloatField()
    avg_aq_level = FloatField()
    avg_gw_level = FloatField()
    avg_bm_level = FloatField()

    avg_attack_wins = FloatField(required=True)
    avg_versus_wins = FloatField(required=True)

    total_donations = IntField()
    total_attack_wins = IntField()
    total_versus_wins = IntField()

    season_delta = EmbeddedDocumentField(ClanDelta)
    week_delta = EmbeddedDocumentField(ClanDelta)
    day_delta = EmbeddedDocumentField(ClanDelta)

    cluster_label = IntField(required=True, default=-1)
    verified_accounts = ListField(StringField())

    meta = {
        'indexes': [
            'last_updated',
            'page_views',
            'slug',
            'tag',
            'members',
            'clanPoints',
            'clanVersusPoints',
            'location.countryCode',
            'isWarLogPublic',
            'cluster_label',
            'verified_accounts',
            'warWinStreak',
            'avg_bh_level',

            # Worker indexes
            ['week_delta.total_attack_wins', 'last_updated', 'members'],
        ]
    }
