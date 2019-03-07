from datetime import datetime
from time import sleep

import graphene
from graphene.types.generic import GenericScalar
from rq.exceptions import NoSuchJobError

import clashleaders.model as model
from clashleaders.insights.clan_activity import clan_status


class PlayerActivity(graphene.ObjectType):
    labels = graphene.List(graphene.String)
    attack_wins = graphene.List(graphene.Float)
    donations = graphene.List(graphene.Float)
    gold_grab = graphene.List(graphene.Float)
    elixir_grab = graphene.List(graphene.Float)
    de_grab = graphene.List(graphene.Float)
    trophies = graphene.List(graphene.Float)


class BadgeUrls(graphene.ObjectType):
    large = graphene.String()
    medium = graphene.String()
    small = graphene.String()
    tiny = graphene.String()


class PlayerLeague(graphene.ObjectType):
    name = graphene.String()
    id = graphene.Int()
    iconUrls = graphene.Field(BadgeUrls)

    def resolve_iconUrls(self, info):
        return BadgeUrls(**self.iconUrls)


class ShortClan(graphene.ObjectType):
    name = graphene.String()
    tag = graphene.String()
    slug = graphene.String()


class Player(graphene.ObjectType):
    role = graphene.String()
    name = graphene.String()
    tag = graphene.String()
    slug = graphene.String()
    role = graphene.String()
    townHallLevel = graphene.Int()
    trophies = graphene.Int()
    builderHallLevel = graphene.Int()
    expLevel = graphene.Int()
    defenseWins = graphene.Int()
    attackWins = graphene.Int()
    donations = graphene.Int()
    percentile = graphene.Int()
    activity = graphene.Field(PlayerActivity)
    league = graphene.Field(PlayerLeague)
    clan = graphene.Field(ShortClan)

    def resolve_percentile(self, info):
        return self.player_score()

    def resolve_activity(self, info):
        df = self.to_historical_df()[
            ['attack_wins', 'donations', 'gold_grab', 'elixir_escapade', 'heroic_heist', 'trophies']
        ]
        resampled = df.resample('D').mean()
        diffed = resampled.diff().dropna().clip(lower=0)
        diffed.rename(columns={'elixir_escapade': 'elixir_grab', 'heroic_heist': 'de_grab'}, inplace=True)
        diffed['trophies'] = resampled['trophies']  # Undo trophies

        return PlayerActivity(labels=diffed.index.strftime('%Y-%m-%d %H:%M:%S').tolist(),
                              attack_wins=diffed['attack_wins'].tolist(),
                              donations=diffed['donations'].tolist(),
                              gold_grab=diffed['gold_grab'].tolist(),
                              elixir_grab=diffed['elixir_grab'].tolist(),
                              de_grab=diffed['de_grab'].tolist(),
                              trophies=diffed['trophies'].tolist())

    def resolve_league(self, info):
        return PlayerLeague(**self.league)

    def resolve_clan(self, info):
        return self.most_recent_clan()


class ClanDelta(graphene.ObjectType):
    avg_attack_wins = graphene.Float()
    avg_de_grab = graphene.Float()
    avg_donations = graphene.Float()
    avg_donations_received = graphene.Float()
    avg_elixir_grab = graphene.Float()
    avg_gold_grab = graphene.Float()
    avg_versus_wins = graphene.Float()
    avg_war_stars = graphene.Float()
    total_attack_wins = graphene.Int()
    total_bh_trophies = graphene.Int()
    total_de_grab = graphene.Int()
    total_donations = graphene.Float()
    total_elixir_grab = graphene.Float()
    total_gold_grab = graphene.Float()
    total_trophies = graphene.Float()
    total_versus_wins = graphene.Float()


class SimilarClanDelta(graphene.ObjectType):
    avg_de_grab = graphene.Float()
    avg_elixir_grab = graphene.Float()
    avg_gold_grab = graphene.Float()


class ClanActivity(graphene.ObjectType):
    labels = graphene.List(graphene.String)
    trophies = graphene.List(graphene.Float)
    members = graphene.List(graphene.Float)


class Clan(graphene.ObjectType):
    name = graphene.String()
    slug = graphene.String()
    tag = graphene.String()
    description = graphene.String()
    badge_urls = graphene.Field(BadgeUrls)
    clanPoints = graphene.Int()
    clanVersusPoints = graphene.Int()
    members = graphene.Int()
    updated_on = graphene.Float()
    week_delta = graphene.Field(ClanDelta)
    day_delta = graphene.Field(ClanDelta)
    computed = graphene.Field(ClanDelta)
    delta = graphene.Field(ClanDelta, days=graphene.Int(required=True))
    player_matrix = GenericScalar(days=graphene.Int(required=False))
    players = graphene.List(Player)
    activity = graphene.Field(ClanActivity)
    similar = graphene.Field(SimilarClanDelta, days=graphene.Int(required=True))
    player_status = GenericScalar()

    def resolve_delta(self, info, days):
        previous_clan = self.historical_near_days_ago(days)
        return self.historical_near_now().clan_delta(previous_clan)

    def resolve_badge_urls(self, info):
        return BadgeUrls(**self.badgeUrls)

    def resolve_updated_on(self, info):
        return self.updated_on.timestamp() * 1000

    def resolve_player_matrix(self, info, days=0):
        return self.historical_near_days_ago(days).to_matrix()

    def resolve_players(self, info):
        df = self.historical_near_now().to_df(formatted=False).reset_index()
        df = df[
            ['name',
             'tag',
             'town_hall_level',
             'exp_level',
             'trophies',
             'builder_hall_level',
             'defense_wins',
             'attack_wins',
             'donations']
        ].rename(
            columns={
                'town_hall_level': 'townHallLevel',
                'exp_level': 'expLevel',
                'builder_hall_level': 'builderHallLevel',
                'defense_wins': 'defenseWins',
                'attack_wins': 'attackWins'
            }
        )
        return [Player(**p) for p in df.to_dict('i').values()]

    def resolve_similar(self, info, days):
        key = {1: 'day_delta', 7: 'week_delta'}[days]
        cluster_label = self.cluster_label
        gold = model.Clan.objects(cluster_label=cluster_label).average(f"{key}.avg_gold_grab")
        elixir = model.Clan.objects(cluster_label=cluster_label).average(f"{key}.avg_elixir_grab")
        de = model.Clan.objects(cluster_label=cluster_label).average(f"{key}.avg_de_grab")
        return SimilarClanDelta(avg_de_grab=de, avg_gold_grab=elixir, avg_elixir_grab=gold)

    def resolve_activity(self, info):
        df = self.to_historical_df()[['members', 'clanPoints']].resample('D').mean().dropna()
        df.index.name = 'labels'
        df = df.reset_index().rename(columns={'clanPoints': 'trophies'})
        df['labels'] = df['labels'].dt.strftime('%Y-%m-%dT%H:%M:%S+00:00Z')
        return ClanActivity(**df.to_dict('l'))

    def resolve_player_status(self, info):
        return clan_status(self)


class Query(graphene.ObjectType):
    player = graphene.Field(Player, tag=graphene.String(required=True))
    clan = graphene.Field(Clan, tag=graphene.String(required=True), refresh=graphene.Boolean(required=False))

    def resolve_clan(self, info, tag, refresh=False):
        if refresh:
            clan = model.Clan.fetch_and_update(tag, sync_calculation=False)
            wait_for_job(clan.job)

        return model.Clan.find_by_tag(tag)

    def resolve_player(self, info, tag):
        return model.Player.find_by_tag(tag)


def wait_for_job(job, wait_time=3):
    start = datetime.now()
    while (datetime.now() - start).total_seconds() < wait_time:
        sleep(0.2)
        try:
            job.refresh()
        except NoSuchJobError:
            break
