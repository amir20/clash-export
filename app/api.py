# coding: utf-8

import requests
import grequests
from urllib.parse import quote
from collections import OrderedDict
import xlsxwriter
import os

token = os.getenv('API_TOKEN')
headers = {'authorization': 'Bearer ' + token}


def search_by_tag(tag):
    return requests.get('https://api.clashofclans.com/v1/clans/' + quote(tag), headers=headers).json()


def export(clan, stream):
    tags = [member['tag'] for member in clan['memberList']]
    urls = ['https://api.clashofclans.com/v1/players/' + quote(tag) for tag in tags]
    rs = (grequests.get(u, headers=headers) for u in urls)
    responses = grequests.map(rs)

    def player_row(player_json):
        achievements = {i['name']: i for i in player_json['achievements']}
        row = player_json.copy()
        del row['achievements']
        row.update(achievements)
        return row

    rows = [player_row(r.json()) for r in responses]

    columns = OrderedDict((
        ('name', 'Player Name'),
        ('townHallLevel', 'TH Level'),
        ('expLevel', 'XP Level'),
        ('bestTrophies', 'Best Trophies'),
        ('trophies', 'Current Trophies'),
        ('attackWins', 'Attack Wins'),
        ('defenseWins', 'Defense Wins'),
        ('Gold Grab', 'Total Gold Grab'),
        ('Elixir Escapade', 'Total Elixer Grab'),
        ('Heroic Heist', 'Total DE Grab'),
        ('Friend in Need', 'Total Donations'),
        ('Treasurer', 'Total War Collected Gold'),
        ('War Hero', 'Total War Stars'),
        ('Sharing is caring', 'Total Spells Donated'),
        ('donations', 'Donations'),
        ('donationsReceived', 'Donations Received')
    ))

    column_keys = columns.keys()

    workbook = xlsxwriter.Workbook(stream)
    worksheet = workbook.add_worksheet()

    data = [
        [row[key]['value'] if type(row[key]) == dict and 'value' in row[key] else row[key] for key in column_keys]
        for row in rows]

    data.insert(0, list(columns.values()))

    for row, data in enumerate(data):
        worksheet.write_row(row, 0, data)

    workbook.close()
