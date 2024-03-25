from __future__ import annotations

from typing import Dict, List

import pandas as pd

import clashleaders.model


def clan_diff(
    previous: clashleaders.model.HistoricalClan,
    most_recent: clashleaders.model.HistoricalClan,
) -> pd.DataFrame:
    pd_df = previous.to_df()
    mr_df = most_recent.to_df()
    columns = [
        "Attack Wins",
        "Versus Battle Wins",
        "Total Gold Grab",
        "Total Elixir Grab",
        "Total DE Grab",
        "Total Donations",
        "Total Spells Donated",
        "Clan Games XP",
    ]
    diff = mr_df[columns] - pd_df[columns]

    return diff


def clan_new_players(clan: clashleaders.model.Clan) -> List[str]:
    pd_df = clan.historical_near_days_ago(days=2).to_df()
    mr_df = clan.historical_near_now().to_df()
    df = mr_df["Total Gold Grab"] - pd_df["Total Gold Grab"]
    return df[df.isnull()].index.tolist()


def clan_status(clan: clashleaders.model.Clan) -> Dict[str, str]:
    status = {}

    if clan.days_of_history() > 3:
        most_recent = clan.historical_near_now()
        previous = clan.historical_near_days_ago(days=7)

        diff = clan_diff(previous, most_recent)
        percentiles = most_recent.activity_score_series(days=7)

        if not percentiles.empty:
            most_active = percentiles.sort_values(ascending=False)
            status[most_active.index[0]] = "mvp"

            inactive = (diff == 0).all(axis=1)
            inactive = inactive[inactive]
            for p in inactive.index.tolist():
                status[p] = "inactive"

            for p in clan_new_players(clan):
                status[p] = "new"

    return status
