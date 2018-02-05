from clashleaders.clash import calculation


def test_to_data_frame(clan_with_players):
    df = calculation.to_data_frame(clan_with_players)

    columns = ['Name', 'TH Level', 'BH Level', 'XP Level', 'Best Trophies', 'Best Versus Trophies',
               'Current Trophies', 'Builder Hall Trophies', 'Attack Wins', 'Versus Battle Wins', 'Defense Wins',
               'Total Gold Grab', 'Total Elixir Grab', 'Total DE Grab', 'Total Donations',
               'Total War Collected Gold', 'Total War Stars', 'Total Spells Donated', 'Donations',
               'Donations Received', 'Barbarian King', 'Archer Queen', 'Grand Warden', 'Battle Machine']

    assert df.columns.tolist() == columns
    assert df.shape == (50, 24)
