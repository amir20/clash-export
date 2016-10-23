# coding: utf-8

import requests
import grequests
from urllib.parse import quote
import xlsxwriter
import os


token = os.getenv('API_TOKEN')
headers = {'authorization': 'Bearer ' + token}


def clan(tag):
    return requests.get('https://api.clashofclans.com/v1/clans/' + quote(tag), headers=headers).json()


def export(tag, stream):
    c = clan(tag)
    tags = [member['tag'] for member in c['memberList']]
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

    column_keys = ['name', 'townHallLevel', 'bestTrophies', 'Gold Grab', 'Elixir Escapade', 'Heroic Heist',
                   'Friend in Need', 'Sharing is caring']

    workbook = xlsxwriter.Workbook(stream)
    worksheet = workbook.add_worksheet()

    data = [
        [row[key]['value'] if type(row[key]) == dict and 'value' in row[key] else row[key] for key in column_keys]
        for row in rows]

    data.insert(0,
                ['Player Name', 'TH Level', 'Best Trophines', 'Total Gold Grab', 'Total Exliser Grab', 'Total DE Grab',
                 'Total Donations', 'Total Spells Donated'])

    for row, data in enumerate(data):
        worksheet.write_row(row, 0, data)

    workbook.close()


