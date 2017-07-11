import concurrent.futures
import os
from collections import OrderedDict
from urllib.parse import quote

import requests
import xlsxwriter
from model import Player

token = os.getenv('API_TOKEN')
headers = {'authorization': 'Bearer ' + token}


def __get_with_threads(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        return list(executor.map(lambda url: requests.get(url, headers=headers), urls))


def find_clan_by_tag(tag):
    return requests.get('https://api.clashofclans.com/v1/clans/' + quote(tag), headers=headers).json()


def fetch_all_players(clan):
    tags = [member['tag'] for member in clan['memberList']]
    urls = ['https://api.clashofclans.com/v1/players/' + quote(tag) for tag in tags]
    return __get_with_threads(urls)


def export_clan(clan, stream):
    responses = fetch_all_players(clan)
    [Player(**r.json()).save() for r in responses]

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

    rows = [player_row(r.json()) for r in responses]

    columns = OrderedDict((
        ('name', 'Player Name'),
        ('townHallLevel', 'TH Level'),
        ('builderHallLevel', 'BH Level'),
        ('expLevel', 'XP Level'),
        ('bestTrophies', 'Best Trophies'),
        ('bestVersusTrophies', 'Best Versus Trophies'),
        ('trophies', 'Current Trophies'),
        ('Champion Builder', 'Builder Hall Trophies'),
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

    workbook = xlsxwriter.Workbook(stream)
    worksheet = workbook.add_worksheet()

    data = []
    for row in rows:
        data_row = []

        for key in columns.keys():
            if key in row:
                if type(row[key]) == dict and 'value' in row[key]:
                    data_row.append(row[key]['value'])
                else:
                    data_row.append(row[key])
            else:
                data_row.append(0)

        data.append(data_row)

    data.insert(0, list(columns.values()))

    for row, data in enumerate(data):
        worksheet.write_row(row, 0, data)

    workbook.close()
