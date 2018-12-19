from collections import OrderedDict, namedtuple
from functools import reduce

import pandas as pd

ShortClan = namedtuple('ShortClan', 'name tag badge slug members score')


def transform_players(players):
    def player_row(player_json):
        row = player_json.copy()

        if 'achievements' in player_json:
            achievements = {i['name']: i for i in player_json['achievements']}
            del row['achievements']
            row.update(achievements)

        if 'heroes' in player_json:
            heroes = {i['name']: i for i in player_json['heroes']}
            for k, hero in heroes.items():
                hero['value'] = hero['level']

            del row['heroes']
            row.update(heroes)

        return row

    rows = [player_row(r) for r in players]

    columns = OrderedDict((
        ('name', 'Name'),
        ('tag', 'Tag'),
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
        ('Elixir Escapade', 'Total Elixir Grab'),
        ('Heroic Heist', 'Total DE Grab'),
        ('Friend in Need', 'Total Donations'),
        ('Treasurer', 'Total War Collected Gold'),
        ('War Hero', 'Total War Stars'),
        ('Games Champion', 'Clan Games XP'),
        ('War League Legend', 'CWL Stars'),
        ('Sharing is caring', 'Total Spells Donated'),
        ('donations', 'Donations'),
        ('donationsReceived', 'Donations Received'),
        ('Barbarian King', 'Barbarian King'),
        ('Archer Queen', 'Archer Queen'),
        ('Grand Warden', 'Grand Warden'),
        ('Battle Machine', 'Battle Machine')
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


def deepgetattr(obj, attr):
    return reduce(getattr, attr.split('.'), obj)


def to_short_clan(clan, prop=None):
    score = None if prop is None else deepgetattr(clan, prop)
    return ShortClan(name=clan.name, tag=clan.tag, badge=clan.badgeUrls.get('small'), members=clan.members,
                     slug=getattr(clan, 'slug', None), score=score)


def to_data_frame(clan):
    tf = transform_players(clan.players_data())
    df = pd.DataFrame(data=tf, columns=tf[0])
    df = df.set_index('Tag')
    df = df.iloc[1:]
    return df


def clans_leaderboard(clans, prop):
    return [to_short_clan(c, prop) for c in clans]
