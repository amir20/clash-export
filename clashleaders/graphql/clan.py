from clashleaders.clash.transformer import tag_to_slug
import logging


import graphene
from graphene.types.generic import GenericScalar

import pandas as pd
from io import BytesIO
import base64
import clashleaders.model as model

from .badge import BadgeUrls

import clashleaders.graphql.player as player
import clashleaders.graphql.war as war

logger = logging.getLogger(__name__)


class ShortClan(graphene.ObjectType):
    name = graphene.String()
    tag = graphene.String()
    slug = graphene.String()
    members = graphene.Int()
    badge_urls = graphene.Field(BadgeUrls)

    def resolve_badge_urls(parent, info):
        if hasattr(parent, "badgeUrls"):
            return BadgeUrls(**parent.badgeUrls)
        else:
            return BadgeUrls(**parent["badgeUrls"])


class ClanDelta(graphene.ObjectType):
    avg_attack_wins = graphene.Float()
    avg_de_grab = graphene.Float()
    avg_donations = graphene.Float()
    avg_donations_received = graphene.Float()
    avg_elixir_grab = graphene.Float()
    avg_gold_grab = graphene.Float()
    avg_versus_wins = graphene.Float()
    avg_war_stars = graphene.Float()
    avg_games_xp = graphene.Float()
    avg_cwl_stars = graphene.Float()

    avg_donations_percentile = graphene.Float()
    avg_war_stars_percentile = graphene.Float()
    avg_attack_wins_percentile = graphene.Float()
    avg_versus_wins_percentile = graphene.Float()
    avg_games_xp_percentile = graphene.Float()
    avg_cwl_stars_percentile = graphene.Float()

    total_attack_wins = graphene.Int()
    total_bh_trophies = graphene.Int()
    total_de_grab = graphene.Int()
    total_donations = graphene.Float()
    total_elixir_grab = graphene.Float()
    total_gold_grab = graphene.Float()
    total_trophies = graphene.Float()
    total_versus_wins = graphene.Float()
    total_games_xp = graphene.Float()
    total_cwl_stars = graphene.Float()


class SimilarClanDelta(graphene.ObjectType):
    avg_de_grab = graphene.Float()
    avg_elixir_grab = graphene.Float()
    avg_gold_grab = graphene.Float()


class ClanActivity(graphene.ObjectType):
    labels = graphene.List(graphene.String)
    trophies = graphene.List(graphene.Float)
    members = graphene.List(graphene.Float)


class IdNamePair(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()


class ClanLabel(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    iconUrls = graphene.Field(BadgeUrls)

    def resolve_iconUrls(self, info):
        return BadgeUrls(**self.iconUrls)


class ClanMembers(graphene.ObjectType):
    header = GenericScalar()
    most_recent = GenericScalar()
    delta = GenericScalar()
    groups = GenericScalar()

    def resolve_header(parent, info):
        return parent.header()

    def resolve_most_recent(parent, info):
        return parent.most_recent().to_dict(orient="records")

    def resolve_delta(parent, info):
        return parent.delta().fillna(0).to_dict(orient="index")

    def resolve_groups(parent, info):
        return parent.groups()


class Clan(graphene.ObjectType):
    name = graphene.String()
    slug = graphene.String()
    tag = graphene.String()
    description = graphene.String()
    badge_urls = graphene.Field(BadgeUrls)
    clanPoints = graphene.Int()
    clanLevel = graphene.Int()
    clanVersusPoints = graphene.Int()
    members = graphene.Int()
    updated_on = graphene.Float()
    labels = graphene.List(ClanLabel)

    computed = graphene.Field(ClanDelta)
    day_delta = graphene.Field(ClanDelta)
    week_delta = graphene.Field(ClanDelta)
    month_delta = graphene.Field(ClanDelta)
    delta = graphene.Field(ClanDelta, days=graphene.Int(required=True))

    player_matrix = GenericScalar(days=graphene.Int(required=False))
    players = graphene.List(lambda: player.Player)
    activity = graphene.Field(ClanActivity)
    similar = graphene.Field(SimilarClanDelta, days=graphene.Int(required=True))
    player_status = GenericScalar()
    xlsx_export = graphene.String(days=graphene.Int(required=True))
    trophy_history = GenericScalar()

    warLeague = graphene.Field(IdNamePair)
    isWarLogPublic = graphene.Boolean()
    requiredTrophies = graphene.Int()
    warFrequency = graphene.String()
    warLosses = graphene.Int()
    warTies = graphene.Int()
    warWinStreak = graphene.Int()
    warWins = graphene.Int()
    war_win_ratio = graphene.Float()
    war_total = graphene.Int()

    comparable_members = graphene.Field(ClanMembers, delta_days=graphene.Int(required=True))

    recent_cwl_group = graphene.Field(lambda: war.CWLGroup, update_wars=graphene.Boolean(required=False))
    wars = graphene.List(lambda: war.War)

    def resolve_delta(self, info, days):
        previous_clan = self.historical_near_days_ago(days)
        return self.historical_near_now().clan_delta(previous_clan)

    def resolve_badge_urls(self, info):
        return BadgeUrls(**self.badgeUrls)

    def resolve_labels(self, info):
        return [ClanLabel(**l) for l in self.labels]

    def resolve_updated_on(self, info):
        return self.updated_on.timestamp() * 1000

    def resolve_player_matrix(self, info, days=0):
        return self.historical_near_days_ago(days).to_matrix()

    def resolve_recent_cwl_group(self, info, update_wars=False):
        wars = self.cwl_wars()
        if wars:
            cwl_war = wars[0]
            cwl_war.clan = self
            return cwl_war
        else:
            return None

    def resolve_wars(self, info):
        return self.wars().limit(10)

    def resolve_comparable_members(self, info, delta_days):
        return self.comparable_members(delta_days)

    def resolve_players(self, info):
        df = self.historical_near_now().to_df(formatted=False).reset_index()
        df = df[["name", "tag", "town_hall_level", "exp_level", "trophies", "builder_hall_level", "defense_wins", "attack_wins", "donations"]].rename(
            columns={
                "town_hall_level": "townHallLevel",
                "exp_level": "expLevel",
                "builder_hall_level": "builderHallLevel",
                "defense_wins": "defenseWins",
                "attack_wins": "attackWins",
            }
        )
        return [player.Player(**p) for p in df.to_dict("index").values()]

    def resolve_similar(self, info, days):
        key = {1: "day_delta", 7: "week_delta"}[days]
        cluster_label = self.cluster_label
        gold = model.Clan.objects(cluster_label=cluster_label).average(f"{key}.avg_gold_grab")
        elixir = model.Clan.objects(cluster_label=cluster_label).average(f"{key}.avg_elixir_grab")
        de = model.Clan.objects(cluster_label=cluster_label).average(f"{key}.avg_de_grab")
        return SimilarClanDelta(avg_de_grab=de, avg_gold_grab=elixir, avg_elixir_grab=gold)

    def resolve_activity(self, info):
        df = self.to_historical_df()[["members", "clanPoints"]].resample("D").mean().dropna()
        df.index.name = "labels"
        df = df.reset_index().rename(columns={"clanPoints": "trophies"})
        df["labels"] = df["labels"].dt.strftime("%Y-%m-%dT%H:%M:%S+00:00Z")
        return ClanActivity(**df.to_dict("list"))

    def resolve_player_status(self, info):
        return self.player_activity()

    def resolve_xlsx_export(self, info, days):
        historical = self.historical_near_days_ago(days)

        stream = BytesIO()
        writer = pd.ExcelWriter(stream, engine="xlsxwriter", engine_kwargs=dict(options={"strings_to_urls": False, "strings_to_formulas": False}))
        historical.to_df(formatted=True).to_excel(writer, sheet_name=self.tag)
        writer.close()
        return "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64," + base64.b64encode(stream.getvalue()).decode()

    def resolve_trophy_history(self, info):
        return self.trophy_history()

    def resolve_warLeague(self, info):
        return IdNamePair(**self.warLeague)
