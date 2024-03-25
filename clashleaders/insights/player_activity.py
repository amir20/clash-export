from __future__ import annotations

from datetime import timedelta

import numpy as np
import pandas as pd

import clashleaders.model
from clashleaders.insights.clan_activity import clan_diff


def clan_percentiles(previous, most_recent):
    diff = clan_diff(previous, most_recent)
    ranks = diff.rank(ascending=True, pct=True, na_option="top")

    for c in ["Total Gold Grab", "Total Elixir Grab"]:
        ranks.loc[diff[c] == 0, c] = ranks.loc[diff[c] == 0, "Total DE Grab"]

    return ranks.mean(axis=1)


def player_activity_scores(
    clan: clashleaders.model.HistoricalClan, days: int = 7
) -> pd.Series:
    previous_dt = clan.created_on - timedelta(days=days)
    previous_clan = clashleaders.model.HistoricalClan.find_by_tag_near_time(
        clan.tag, previous_dt
    )
    score_series = clan_percentiles(most_recent=clan, previous=previous_clan).to_frame(
        "Activity Score"
    )
    return np.ceil(score_series["Activity Score"] * 100)


def clan_history(player: clashleaders.model.Player) -> pd.DataFrame:
    df = player.to_historical_df()
    df = df[["clan_tag"]].dropna()
    df["clan_changed"] = df["clan_tag"].ne(df["clan_tag"].shift().fillna(True))
    return df[df["clan_changed"]]["clan_tag"]
