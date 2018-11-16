from datetime import datetime

from mongoengine import BooleanField, DateTimeField, DictField, Document, DoesNotExist, EmbeddedDocument, \
    EmbeddedDocumentField, \
    FloatField, IntField, ListField, ReferenceField, StringField, Q

from clashleaders.clash.api import clan_warlog
from clashleaders.model.clan import Clan


class ClanDelta(EmbeddedDocument):
    avg_donations = FloatField(required=True)
    avg_donations_received = FloatField(required=True)

    avg_gold_grab = FloatField(required=True)
    avg_elixir_grab = FloatField(required=True)
    avg_de_grab = FloatField(required=True)
    avg_war_stars = FloatField(required=True)

    avg_th_level = FloatField()
    avg_bh_level = FloatField()
    avg_xp_level = FloatField()
    avg_best_trophies = FloatField()
    avg_trophies = FloatField()
    avg_bh_trophies = FloatField()

    avg_attack_wins = FloatField(required=True)
    avg_versus_wins = FloatField(required=True)

    total_trophies = IntField()
    total_bh_trophies = IntField()
    total_gold_grab = IntField()
    total_elixir_grab = IntField()
    total_de_grab = IntField()
    total_donations = IntField()
    total_attack_wins = IntField()
    total_versus_wins = IntField()


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
            'week_delta.avg_donations',
            'week_delta.avg_gold_grab',
            'week_delta.avg_trophies',
            'week_delta.avg_attack_wins',
            'week_delta.avg_versus_wins',
            'week_delta.total_attack_wins',

            # Worker indexes
            ['week_delta.total_attack_wins', 'last_updated', 'members'],
        ]
    }

    def warlog(self):
        return clan_warlog(self.tag)['items']

    def previous_data(self, **kwargs):
        return Clan.from_now_with_tag(self.tag, **kwargs).first()

    @property
    def created_on(self):
        return self.id.generation_time

    @property
    def players(self):
        return self.most_recent.players_data()

    def similar_clan(self):
        return ClanPreCalculated.objects(cluster_label=self.cluster_label)

    def fetch_and_update_calculations(self):
        return Clan.fetch_and_save(self.tag).update_calculations()

    def update_without_fetching(self):
        try:
            return self.most_recent.update_calculations()
        except DoesNotExist:
            return Clan.find_most_recent_by_tag(self.tag).update_calculations()

    @classmethod
    def find_by_slug(cls, slug):
        return cls.objects.get(slug=slug)

    @classmethod
    def find_by_tag(cls, tag):
        tag = "#" + tag.lstrip("#").upper()
        return cls.objects.get(tag=tag)

    @classmethod
    def active_clans(cls, update_before=None):
        query = Q(members__gte=5) & Q(week_delta__total_attack_wins__ne=0)
        if update_before:
            query = Q(last_updated__lte=update_before) & query

        return cls.objects(query).no_cache()
