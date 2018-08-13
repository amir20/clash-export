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
    ss_df = cpc.season_start.to_data_frame()
    mr_df = cpc.most_recent.to_data_frame()
    columns = ['Total Gold Grab', 'Total Elixir Grab', 'Total DE Grab', 'Total Donations', 'Total Spells Donated',
               'Total War Collected Gold', 'Clan Games XP']
    diff = mr_df[columns] - ss_df[columns]
    percentiles = diff.rank(ascending=True, pct=True, na_option='top').mean(axis=1)
    return percentiles[player_tag]
