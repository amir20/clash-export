from __future__ import annotations

from typing import Dict

import pandas as pd

import clashleaders.model


def next_troop_recommendation(player) -> Dict:
    troop_averages = clashleaders.model.AverageTroop.objects(th_level=player.townHallLevel)

    data = {
        "base": [t.base for t in troop_averages],
        "name": [t.name for t in troop_averages],
        "avg": [t.avg for t in troop_averages],
        "player": [player.lab_levels.get(troop.troop_id, 0) for troop in troop_averages],
    }

    df = pd.DataFrame(data).set_index(["name", "base"])
    df["delta"] = df["avg"] - df["player"]
    df = df.sort_values(by="delta", ascending=False).dropna()
    th_df = df.xs("home", level="base")
    th_total = len(th_df)
    th_completed = len(th_df[th_df["delta"] <= 0])

    bh_df = df.xs("builderBase", level="base")
    bh_total = len(bh_df)
    bh_completed = len(bh_df[bh_df["delta"] <= 0])

    df = df[df["delta"] > 0]

    if df.empty:
        return dict(builderBase={}, home={}, th_ratio=th_completed / th_total, bh_ratio=bh_completed / bh_total, th_level=player.townHallLevel)

    builder_troops = df.xs("builderBase", level="base").to_dict("i")
    for k, v in builder_troops.items():
        v["name"] = k
    builder_troops = list(builder_troops.values())

    home_troops = df.xs("home", level="base").to_dict("i")
    for k, v in home_troops.items():
        v["name"] = k
    home_troops = list(home_troops.values())

    return dict(builderBase=builder_troops, home=home_troops, th_ratio=th_completed / th_total, bh_ratio=bh_completed / bh_total, th_level=player.townHallLevel)
