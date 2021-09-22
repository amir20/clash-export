from typing import TYPE_CHECKING, Dict

import pandas as pd

from re import sub


if TYPE_CHECKING:
    from clashleaders.model.clan import Clan


class ClanMembers(object):
    def __init__(self, clan: "Clan", compare_to_days: int = 7, include_player_activity: bool = True, include_war_activity: bool = True):
        self.include_player_activity = include_player_activity
        self.include_war_activity = include_war_activity
        self.now_df = clan.historical_near_now().to_df(player_activity=include_player_activity, war_activity=include_war_activity)
        self.days_ago = compare_to_days
        self.clan = clan

    def header(self) -> Dict[str, str]:
        headers = {camel_cased(col): col for col in self.now_df.reset_index().columns}
        tuples = list(headers.items())
        # put the name first
        tuples[0], tuples[1] = tuples[1], tuples[0]
        return dict(tuples)

    def most_recent(self) -> pd.DataFrame:
        df = self.now_df.reset_index().fillna("na")
        df.columns = [camel_cased(col) for col in df.columns]
        return df

    def delta(self) -> pd.DataFrame:
        now = self.now_df.drop(columns=["Name"])
        old = (
            self.clan.historical_near_days_ago(self.days_ago)
            .to_df(player_activity=self.include_player_activity, war_activity=self.include_war_activity)
            .drop(columns=["Name"])
        )

        delta = now - old
        delta = delta.fillna(0)
        delta.index.name = "tag"
        delta.columns = [camel_cased(col) for col in delta.columns]
        return delta


def camel_cased(s):
    s = sub(r"[_\-.]+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])
