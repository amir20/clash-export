import pandas as pd

import clashleaders.model


def next_troop_recommendation(tag):
    player = clashleaders.model.Player.find_by_tag(tag)
    troop_averages = clashleaders.model.AverageTroop.objects(th_level=player.townHallLevel)

    data = {
        'base': [t.base for t in troop_averages],
        'name': [t.name for t in troop_averages],
        'avg': [t.avg for t in troop_averages],
        'player': [player.lab_levels.get(troop.troop_id, 0) for troop in troop_averages],
    }

    df = pd.DataFrame(data).set_index(['name', 'base'])

    df['delta'] = df['avg'] - df['player']
    return df.sort_values(by='delta', ascending=False)
