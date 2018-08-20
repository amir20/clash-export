from clashleaders.model.clan import prepend_hash


def find_player_details(cpc, player_tag):
    player_tag = prepend_hash(player_tag)
    player = next((p for p in cpc.players if p['tag'] == player_tag), None)

    if player:
        player['percentile'] = player_percentile(cpc, player['tag'])
        return player
    else:
        return dict(tag=player_tag)


def player_percentile(cpc, player_tag):
    percentiles = clan_percentiles(cpc)
    return percentiles[player_tag]


def clan_diff(cpc):
    pd_df = cpc.previous_data(days=7).to_data_frame()
    mr_df = cpc.most_recent.to_data_frame()
    columns = ['Total Gold Grab', 'Total Elixir Grab', 'Total DE Grab', 'Total Donations', 'Total Spells Donated',
               'Total War Collected Gold', 'Clan Games XP']
    diff = mr_df[columns] - pd_df[columns]

    return diff


def clan_percentiles(cpc):
    diff = clan_diff(cpc)
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

    if cpc.days_span > 3:
        diff = clan_diff(cpc)
        percentiles = clan_percentiles(cpc)

        most_active = percentiles.sort_values(ascending=False)

        status[most_active.index[0]] = 'mvp'

        inactive = (diff == 0).all(axis=1)
        inactive = inactive[inactive]
        for p in inactive.index.tolist():
            status[p] = 'inactive'

        for p in clan_new_players(cpc):
            status[p] = 'new'

    return status
