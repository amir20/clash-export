

def test_clan_to_player_matrix(clan_with_players, snapshot):
    data = clan_with_players.to_player_matrix()
    snapshot.assert_match(data)
