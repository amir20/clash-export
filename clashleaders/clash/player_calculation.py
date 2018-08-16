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
    pd_df = cpc.previous_data(days=7).to_data_frame()
    mr_df = cpc.most_recent.to_data_frame()
    columns = ['Total Gold Grab', 'Total Elixir Grab', 'Total DE Grab', 'Total Donations', 'Total Spells Donated',
               'Total War Collected Gold', 'Clan Games XP']
    diff = mr_df[columns] - pd_df[columns]
    ranks = diff.rank(ascending=True, pct=True, na_option='top')

    for c in ['Total Gold Grab', 'Total Elixir Grab']:
        ranks.loc[diff[c] == 0, c] = ranks.loc[diff[c] == 0, 'Total DE Grab']

    percentiles = ranks.mean(axis=1)
    return percentiles[player_tag]
