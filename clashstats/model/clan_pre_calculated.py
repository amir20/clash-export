from datetime import datetime

from mongoengine import *

from clashstats.model.clan import Clan


class ClanDelta(EmbeddedDocument):
    avg_donations = FloatField(required=True)
    avg_donations_received = FloatField(required=True)

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

    avg_attack_wins = FloatField(required=True)
    avg_versus_wins = FloatField(required=True)


class ClanPreCalculated(Document):
    last_updated = DateTimeField(default=datetime.now)
    tag = StringField(required=True, unique=True)
    slug = StringField(required=True)
    name = StringField(required=True)
    description = StringField(required=True)
    clanPoints = IntField(required=True)
    clanVersusPoints = IntField(required=True)
    members = IntField(required=True)
    badgeUrls = DictField(required=True)

    warWinStreak = IntField(required=True)
    warWins = IntField(required=True)
    warTies = IntField(required=True)
    warLosses = IntField(required=True)

    season_start = ReferenceField(Clan)
    most_recent = ReferenceField(Clan)

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

    avg_attack_wins = FloatField(required=True)
    avg_versus_wins = FloatField(required=True)

    season_delta = EmbeddedDocumentField(ClanDelta)
    week_delta = EmbeddedDocumentField(ClanDelta)

    meta = {
        'indexes': [
            {
                'fields': ['$name', "$tag"],
                'default_language': 'english',
                'weights': {'name': 1, 'tag': 10}
            },
            'last_updated',
            'name',
            'slug',
            'tag',
            'members',
            'clanPoints',
            'clanVersusPoints',

            'warWinStreak',
            'warWins',
            'warTies',
            'warLosses',

            'avg_donations',
            'avg_gold_grab',
            'avg_elixir_grab',
            'avg_de_grab',
            'avg_war_stars',
            'avg_th_level',
            'avg_bh_level',
            'avg_xp_level',
            'avg_best_trophies',
            'avg_trophies',
            'avg_bh_trophies',
            'avg_attack_wins',
            'avg_versus_wins',

            'season_delta.avg_donations',
            'season_delta.avg_donations_received',
            'season_delta.avg_gold_grab',
            'season_delta.avg_elixir_grab',
            'season_delta.avg_de_grab',
            'season_delta.avg_war_stars',
            'season_delta.avg_th_level',
            'season_delta.avg_bh_level',
            'season_delta.avg_xp_level',
            'season_delta.avg_best_trophies',
            'season_delta.avg_trophies',
            'season_delta.avg_bh_trophies',
            'season_delta.avg_attack_wins',
            'season_delta.avg_versus_wins',

            'week_delta.avg_donations',
            'week_delta.avg_donations_received',
            'week_delta.avg_gold_grab',
            'week_delta.avg_elixir_grab',
            'week_delta.avg_de_grab',
            'week_delta.avg_war_stars',
            'week_delta.avg_th_level',
            'week_delta.avg_bh_level',
            'week_delta.avg_xp_level',
            'week_delta.avg_best_trophies',
            'week_delta.avg_trophies',
            'week_delta.avg_bh_trophies',
            'week_delta.avg_attack_wins',
            'week_delta.avg_versus_wins',

        ]
    }

    @classmethod
    def find_by_slug(cls, slug):
        return cls.objects.get(slug=slug)

    @classmethod
    def find_by_tag(cls, tag):
        if not tag.startswith('#'):
            tag = '#' + tag
        return cls.objects.get(tag=tag)
