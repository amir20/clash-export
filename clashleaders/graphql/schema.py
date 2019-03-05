import graphene
from graphene.types.generic import GenericScalar

from clashleaders.model import Clan, Player


class PlayerActivityType(graphene.ObjectType):
    labels = graphene.List(graphene.String)
    attack_wins = graphene.List(graphene.Float)
    donations = graphene.List(graphene.Float)
    gold_grab = graphene.List(graphene.Float)
    elixir_grab = graphene.List(graphene.Float)
    de_grab = graphene.List(graphene.Float)
    trophies = graphene.List(graphene.Float)


class PlayerType(graphene.ObjectType):
    role = graphene.String()
    name = graphene.String()
    tag = graphene.String()
    slug = graphene.String()
    townHallLevel = graphene.Int()
    trophies = graphene.Int()
    builderHallLevel = graphene.Int()
    expLevel = graphene.Int()
    defenseWins = graphene.Int()
    attackWins = graphene.Int()
    donations = graphene.Int()
    activity = graphene.Field(PlayerActivityType)

    def resolve_activity(self, info):
        df = self.to_historical_df()[
            ['attack_wins', 'donations', 'gold_grab', 'elixir_escapade', 'heroic_heist', 'trophies']
        ]
        resampled = df.resample('D').mean()
        diffed = resampled.diff().dropna().clip(lower=0)
        diffed.rename(columns={'elixir_escapade': 'elixir_grab', 'heroic_heist': 'de_grab'}, inplace=True)
        diffed['trophies'] = resampled['trophies']  # Undo trophies

        return PlayerActivityType(labels=diffed.index.strftime('%Y-%m-%dT%H:%M:%S+00:00Z').tolist(),
                                  attack_wins=diffed['attack_wins'].tolist(),
                                  donations=diffed['donations'].tolist(),
                                  gold_grab=diffed['gold_grab'].tolist(),
                                  elixir_grab=diffed['elixir_grab'].tolist(),
                                  de_grab=diffed['de_grab'].tolist(),
                                  trophies=diffed['trophies'].tolist())


class ClanDeltaType(graphene.ObjectType):
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


class ClanActivityType(graphene.ObjectType):
    labels = graphene.List(graphene.String)
    trophies = graphene.List(graphene.Float)
    members = graphene.List(graphene.Float)


class ClanType(graphene.ObjectType):
    name = graphene.String()
    slug = graphene.String()
    tag = graphene.String()
    description = graphene.String()
    clanPoints = graphene.Int()
    clanVersusPoints = graphene.Int()
    members = graphene.Int()
    week_delta = graphene.Field(ClanDeltaType)
    day_delta = graphene.Field(ClanDeltaType)
    delta = graphene.Field(ClanDeltaType, days=graphene.Int(required=True))
    player_matrix = GenericScalar(days=graphene.Int(required=False))
    players = graphene.List(PlayerType)
    activity = graphene.Field(ClanActivityType)

    def resolve_delta(self, info, days):
        previous_clan = self.historical_near_days_ago(days)
        return self.historical_near_now().clan_delta(previous_clan)

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
        return [PlayerType(**p) for p in df.to_dict('i').values()]

    def resolve_activity(self, info):
        df = self.to_historical_df()[['members', 'clanPoints']].resample('D').mean().dropna()
        df.index.name = 'labels'
        df = df.reset_index().rename(columns={'clanPoints': 'trophies'})
        df['labels'] = df['labels'].dt.strftime('%Y-%m-%dT%H:%M:%S+00:00Z')
        return ClanActivityType(**df.to_dict('l'))


class Query(graphene.ObjectType):
    player = graphene.Field(PlayerType, tag=graphene.String(required=True))
    clan = graphene.Field(ClanType, tag=graphene.String(required=True), refresh=graphene.Boolean(required=False))
    players = graphene.List(PlayerType, tags=graphene.List(graphene.String, required=False))

    def resolve_clan(self, info, tag, refresh=False):
        if refresh:
            return Clan.fetch_and_update(tag, sync_calculation=False)
        else:
            return Clan.find_by_tag(tag)

    def resolve_player(self, info, tag):
        return Player.find_by_tag(tag)

    def resolve_players(self, info, tags=[]):
        return list(Player.objects(tag__in=tags))
