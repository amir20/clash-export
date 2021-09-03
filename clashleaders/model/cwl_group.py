from __future__ import annotations

import pandas as pd
from clashleaders.model.cwl_war import CWLWar
from typing import Optional, TYPE_CHECKING
from mongoengine import DynamicDocument
from typing import List

from mongoengine.fields import ListField, ReferenceField, StringField
from clashleaders.util import correct_tag, from_timestamp


if TYPE_CHECKING:
    from clashleaders.model.clan import Clan


class CWLGroup(DynamicDocument):
    round_wars: List[CWLWar] = ListField(ReferenceField(CWLWar))

    meta = {
        "index_background": True,
        "indexes": [
            ("clans.tag", "season"),
        ],
    }

    def __repr__(self):
        return "<CWLGroup season={}>".format(self.season)

    def to_df_for_clan(self, clan: Clan) -> pd.DataFrame:
        cwl_wars = (war for war in self.round_wars if war.contains_clan(clan))
        tuples = ((war.startTime, war.to_df(clan)) for war in cwl_wars if war.state != "preparation")
        sorted_tuples = sorted(tuples, key=lambda tup: tup[0])
        dfs = (tup[1] for tup in sorted_tuples)
        data = {day: df for day, df in zip(range(1, 8), dfs)}
        return pd.concat(data, axis=1)

    def aggregate_stars_and_destruction(self, clan: Clan, flat=True) -> pd.DataFrame:
        df = self.to_df_for_clan(clan)
        stars = df.loc[:, (slice(None), "attack.stars")]
        stars = stars.droplevel(level=1, axis=1)
        stars.loc[:, "avg"] = stars.mean(axis=1)

        destruction = df.loc[:, (slice(None), "attack.destructionPercentage")]
        destruction = destruction.droplevel(level=1, axis=1)
        destruction.loc[:, "avg"] = destruction.mean(axis=1)

        name = df.droplevel(axis=1, level=0)["name"].fillna(method="bfill", axis=1).iloc[:, 0]

        df = pd.concat([name, stars, destruction], axis=1, keys=["name", "stars", "destruction"])
        if not flat:
            return df
        else:
            df.columns = [f"{column}_day_{day}" for column, day in df.columns.to_flat_index()]
            return df.rename(columns={"name_day_name": "name", "stars_day_avg": "stars_avg", "destruction_day_avg": "destruction_avg"})

    @classmethod
    def find_by_clan_and_season(cls, tag: str, season: str) -> Optional[CWLGroup]:
        tag = correct_tag(tag)
        return cls.objects(clans__tag=tag, season=season).first()
