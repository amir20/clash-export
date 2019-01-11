import pandas as pd

import numpy as np

import clashleaders.model


def find_player_details(cpc, player_tag):
    player_tag = clashleaders.model.clan.prepend_hash(player_tag)
    player = next((p for p in cpc.players if p['tag'] == player_tag), None)

    if player:
        player['percentile'] = player_percentile(cpc, player['tag'])
        return player
    else:
        return dict(tag=player_tag)


def player_percentile(cpc, player_tag):
    most_recent = cpc.most_recent
    previous = cpc.previous_data(days=7)

    percentiles = clan_percentiles(previous, most_recent)
    return percentiles[player_tag]


def clan_diff(previous, most_recent):
    pd_df = previous.to_data_frame()
    mr_df = most_recent.to_data_frame()
    columns = ['Total Gold Grab', 'Total Elixir Grab', 'Total DE Grab', 'Total Donations', 'Total Spells Donated',
               'Total War Collected Gold', 'Clan Games XP']
    diff = mr_df[columns] - pd_df[columns]

    return diff


def clan_percentiles(previous, most_recent):
    diff = clan_diff(previous, most_recent)
    ranks = diff.rank(ascending=True, pct=True, na_option='top')

    for c in ['Total Gold Grab', 'Total Elixir Grab']:
        ranks.loc[diff[c] == 0, c] = ranks.loc[diff[c] == 0, 'Total DE Grab']

    return ranks.mean(axis=1)


def clan_new_players(cpc):
    pd_df = cpc.previous_data(days=2).to_data_frame()
    mr_df = cpc.most_recent.to_data_frame()
    df = mr_df['Total Gold Grab'] - pd_df['Total Gold Grab']
    return df[df.isnull()].index.tolist()


def clan_status(cpc):
    status = {}

    most_recent = cpc.most_recent
    previous = cpc.previous_data(days=7)

    if cpc.days_span > 3:
        diff = clan_diff(previous, most_recent)
        percentiles = clan_percentiles(previous, most_recent)

        if not percentiles.empty:
            most_active = percentiles.sort_values(ascending=False)
            status[most_active.index[0]] = 'mvp'

            inactive = (diff == 0).all(axis=1)
            inactive = inactive[inactive]
            for p in inactive.index.tolist():
                status[p] = 'inactive'

            for p in clan_new_players(cpc):
                status[p] = 'new'

    return status


def augment_with_percentiles(clan):
    df = clan.to_data_frame()
    df_p = clan_percentiles(previous=clan.from_before(days=7), most_recent=clan).to_frame('Activity Score')
    df_p['Activity Score'] = np.ceil(df_p['Activity Score'] * 100)
    df['Tag'] = df.index
    joined = df.join(df_p)
    columns = joined.columns.tolist()
    new_order = columns[:-2]
    new_order[1:1] = columns[-2:]
    joined = joined[new_order]
    return joined


def df_to_matrix(df):
    return [df.columns.tolist()] + df.values.tolist()


def next_troop_recommendation(tag):
    player = clashleaders.model.player.Player.find_by_tag(tag)
    troop_averages = clashleaders.model.avg_troop.AverageTroop.objects(th_level=player.townHallLevel)

    data = {
        'base': [t.base for t in troop_averages],
        'name': [t.name for t in troop_averages],
        'avg': [t.avg for t in troop_averages],
        'queue': [player.lab_levels.get(troop.troop_id, 0) for troop in troop_averages],
    }

    df = pd.DataFrame(data).set_index(['name', 'base'])

    df['delta'] = df['avg'] - df['queue']
    return df.sort_values(by='delta', ascending=False)




