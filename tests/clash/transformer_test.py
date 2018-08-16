from clashleaders.clash.transformer import transform_players


def test_transform_players(clan_with_players, snapshot):
    data = transform_players(clan_with_players.players_data())

    snapshot.assert_match(data)


def test_to_data_frame(clan_with_players):
    df = clan_with_players.to_data_frame()

    columns = ['Name', 'TH Level', 'BH Level', 'XP Level', 'Best Trophies', 'Best Versus Trophies',
               'Current Trophies', 'Builder Hall Trophies', 'Attack Wins', 'Versus Battle Wins', 'Defense Wins',
               'Total Gold Grab', 'Total Elixir Grab', 'Total DE Grab', 'Total Donations',
               'Total War Collected Gold', 'Total War Stars', 'Clan Games XP', 'Total Spells Donated', 'Donations',
               'Donations Received', 'Barbarian King', 'Archer Queen', 'Grand Warden', 'Battle Machine']

    assert df.columns.tolist() == columns
    assert df.shape == (50, 25)
