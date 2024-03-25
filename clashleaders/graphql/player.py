import logging

import graphene

import clashleaders.graphql.clan

from .badge import BadgeUrls

logger = logging.getLogger(__name__)


class PlayerActivity(graphene.ObjectType):
    labels = graphene.List(graphene.String)
    attack_wins = graphene.List(graphene.Float)
    donations = graphene.List(graphene.Float)
    gold_grab = graphene.List(graphene.Float)
    elixir_grab = graphene.List(graphene.Float)
    de_grab = graphene.List(graphene.Float)
    trophies = graphene.List(graphene.Float)


class PlayerLeague(graphene.ObjectType):
    name = graphene.String()
    id = graphene.Int()
    iconUrls = graphene.Field(BadgeUrls)

    def resolve_iconUrls(parent, info):
        if hasattr(parent, "iconUrls"):
            return BadgeUrls(**parent.iconUrls)
        else:
            return BadgeUrls(**parent["iconUrls"])


class PlayerWarStats(graphene.ObjectType):
    avg_stars = graphene.Float()
    avg_destruction = graphene.Float()


class Player(graphene.ObjectType):
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
    clan = graphene.Field(lambda: clashleaders.graphql.clan.ShortClan)
    war_stats = graphene.Field(PlayerWarStats)

    def resolve_percentile(self, info):
        return self.player_score()

    def resolve_activity(self, info):
        df = self.to_historical_df()[
            [
                "attack_wins",
                "donations",
                "gold_grab",
                "elixir_escapade",
                "heroic_heist",
                "trophies",
            ]
        ]
        resampled = df.resample("D").mean().dropna()
        diffed = resampled.diff().dropna().clip(lower=0)

        if diffed.empty:
            return PlayerActivity(
                labels=[],
                attack_wins=[],
                donations=[],
                gold_grab=[],
                elixir_grab=[],
                de_grab=[],
                trophies=[],
            )

        diffed.rename(
            columns={"elixir_escapade": "elixir_grab", "heroic_heist": "de_grab"},
            inplace=True,
        )
        diffed["trophies"] = resampled["trophies"]  # Undo trophies

        return PlayerActivity(
            labels=diffed.index.strftime("%Y-%m-%d %H:%M:%S").tolist(),
            attack_wins=diffed["attack_wins"].tolist(),
            donations=diffed["donations"].tolist(),
            gold_grab=diffed["gold_grab"].tolist(),
            elixir_grab=diffed["elixir_grab"].tolist(),
            de_grab=diffed["de_grab"].tolist(),
            trophies=diffed["trophies"].tolist(),
        )

    def resolve_league(parent, info):
        return (
            PlayerLeague(**parent.league)
            if hasattr(parent, "league") and len(parent.league) > 0
            else None
        )

    def resolve_clan(parent, info):
        return parent.most_recent_clan()

    def resolve_war_stats(parent, info):
        return PlayerWarStats(**parent.war_stats())
