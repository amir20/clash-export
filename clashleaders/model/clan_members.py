from typing import TYPE_CHECKING, Dict

import pandas as pd

from re import sub


if TYPE_CHECKING:
    from clashleaders.model.clan import Clan


class ClanMembers(object):
    def __init__(self, clan: "Clan", compare_to_days: int = 7):
        self.now_df = clan.historical_near_now().to_df()
        self.days_ago = compare_to_days
        self.clan = clan

    def header(self) -> Dict[str, str]:
        return {camel_cased(col): col for col in self.now_df.reset_index().columns}

    def most_recent(self) -> pd.DataFrame:
        df = self.now_df.reset_index()
        df.columns = [camel_cased(col) for col in df.columns]
        return df

    def delta(self) -> pd.DataFrame:
        now = self.now_df.reset_index().set_index(["Tag", "Name"])
        old = self.clan.historical_near_days_ago(self.days_ago).to_df().reset_index().set_index(["Tag", "Name"])

        delta = now - old
        delta = delta.reset_index().set_index("Tag").drop(["Name"], axis=1)
        delta.index.name = "tag"
        delta.columns = [camel_cased(col) for col in delta.columns]
        return delta


def camel_cased(s):
    s = sub(r"[_\-.]+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])
