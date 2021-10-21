from __future__ import annotations


from datetime import datetime

import pandas as pd
from mongoengine import Document, StringField, IntField, DateTimeField, ReferenceField, ListField

import clashleaders.clash.clan_calculation
import clashleaders.insights.player_activity
import clashleaders.model
from clashleaders.model import ClanDelta
from clashleaders.util import correct_tag
from clashleaders.model.historical_player import HistoricalPlayer
from clashleaders.model.clan_war import ClanWar
from .columns import COLUMNS


class HistoricalClan(Document):
    created_on = DateTimeField(default=datetime.now)
    tag: str = StringField(required=True)
    clanLevel: int = IntField()
    clanPoints: int = IntField()
    clanVersusPoints: int = IntField()
    members: int = IntField()
    warWinStreak: int = IntField()
    warWins: int = IntField()
    warTies: int = IntField()
    warLosses: int = IntField()
    players = ListField(ReferenceField(HistoricalPlayer))

    meta = {"index_background": True, "indexes": ["tag", "created_on", ("tag", "created_on"), "members"]}

    def __init__(self, *args, **kwargs):
        values = {k: v for k, v in kwargs.items() if k in self._fields_ordered}
        super().__init__(*args, **values)

    def to_df(self, formatted=True, player_activity=False, war_activity=False) -> pd.DataFrame:
        if len(self.players) == 0:
            return pd.DataFrame(columns=list(COLUMNS.values()))

        df = pd.DataFrame(p.to_series() for p in self.players)
        df = df.reset_index().drop(columns=["index"]).set_index("tag")

        if formatted:
            df = df.reset_index()[list(COLUMNS.keys())]
            df = df.rename(columns=COLUMNS).set_index("Tag")
            name = df.pop("Name")
            df.insert(0, value=name, column="Name")

        if war_activity:
            wars = self.avg_war_activity()
            if not wars.empty:
                df = df.join(wars)
                columns = df.columns.tolist()
                df = df[[columns[0]] + columns[-2:] + columns[1:-2]]

        if player_activity:
            scores = self.activity_score_series(days=7)
            df.insert(1, value=scores, column=scores.name)

        return df

    def to_dict(self):
        fields = set(self._fields_ordered)
        fields.remove("players")
        return {name: getattr(self, name) for name in fields}

    def __repr__(self):
        return "<HistoricalClan {0}>".format(self.tag)

    def __str__(self):
        return "<HistoricalClan {0}>".format(self.tag)

    def avg_war_activity(self):
        tags = [p.tag for p in self.players]
        aggregated = list(
            ClanWar.objects.aggregate(
                {"$match": {"clan.members.tag": {"$in": tags}}},
                {"$unwind": {"path": "$clan.members"}},
                {"$match": {"clan.members.tag": {"$in": tags}}},
                {"$unwind": {"path": "$clan.members.attacks"}},
                {
                    "$group": {
                        "_id": "$clan.members.tag",
                        "avg_stars": {"$avg": "$clan.members.attacks.stars"},
                        "avg_destruction": {"$avg": "$clan.members.attacks.destructionPercentage"},
                    }
                },
            )
        )
        df = pd.DataFrame.from_dict(aggregated)
        if not df.empty:
            df.columns = ["Tag", "Avg War Stars", "Avg War Destruction"]
            df = df.set_index("Tag")
        return df

    def to_matrix(self):
        df = self.to_df(formatted=True, player_activity=True)
        df = df.reset_index()
        columns = df.columns.tolist()
        columns[0], columns[1] = columns[1], columns[0]
        df = df[columns]
        return [columns, *df.values.tolist()]

    def activity_score_series(self, days=7) -> pd.Series:
        return clashleaders.insights.player_activity.player_activity_scores(self, days)

    def clan_delta(self, other: HistoricalClan) -> ClanDelta:
        return clashleaders.clash.clan_calculation.calculate_delta(self, other)

    @classmethod
    def find_by_tag_near_time(cls, tag, dt) -> HistoricalClan:
        tag = correct_tag(tag)
        clan = HistoricalClan.objects(tag=tag, created_on__lte=dt).order_by("-created_on").first()

        if clan is None:
            clan = HistoricalClan.objects(tag=tag).order_by("created_on").first()

        if clan is None:
            clashleaders.model.Clan.fetch_and_update(tag, sync_calculation=False)
            clan = HistoricalClan.objects(tag=tag).first()

        return clan
