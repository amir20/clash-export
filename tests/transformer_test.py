from clashleaders.clash.transformer import transform_players


def test_transform_players(clan_with_players, snapshot):
    data = transform_players(clan_with_players.players)

    snapshot.assert_match(data)

