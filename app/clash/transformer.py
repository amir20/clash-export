from collections import OrderedDict


def transform_players(players):
    def player_row(player_json):
        achievements = {i['name']: i for i in player_json['achievements']}
        heroes = {i['name']: i for i in player_json['heroes']}
        for k, hero in heroes.items():
            hero['value'] = hero['level']

        row = player_json.copy()
        del row['achievements']
        del row['heroes']
        row.update(achievements)
        row.update(heroes)

        return row

    rows = [player_row(r) for r in players]

    columns = OrderedDict((
        ('name', 'Name'),
        ('townHallLevel', 'TH Level'),
        ('builderHallLevel', 'BH Level'),
        ('expLevel', 'XP Level'),
        ('bestTrophies', 'Best Trophies'),
        ('bestVersusTrophies', 'Best Versus Trophies'),
        ('trophies', 'Current Trophies'),
        ('versusTrophies', 'Builder Hall Trophies'),
        ('attackWins', 'Attack Wins'),
        ('versusBattleWinCount', 'Versus Battle Wins'),
        ('defenseWins', 'Defense Wins'),
        ('Gold Grab', 'Total Gold Grab'),
        ('Elixir Escapade', 'Total Elixer Grab'),
        ('Heroic Heist', 'Total DE Grab'),
        ('Friend in Need', 'Total Donations'),
        ('Treasurer', 'Total War Collected Gold'),
        ('War Hero', 'Total War Stars'),
        ('Sharing is caring', 'Total Spells Donated'),
        ('donations', 'Donations'),
        ('donationsReceived', 'Donations Received'),
        ('Barbarian King', 'Barbarian King'),
        ('Archer Queen', 'Archer Queen'),
        ('Grand Warden', 'Grand Warden')
    ))

    data = []
    for row in rows:
        data_row = []

        for key in columns.keys():
            if key in row:
                if isinstance(row[key], dict) and 'value' in row[key]:
                    data_row.append(row[key]['value'])
                else:
                    data_row.append(row[key])
            else:
                data_row.append(0)

        data.append(data_row)

    data.insert(0, list(columns.values()))

    return data
