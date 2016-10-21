# coding: utf-8

import requests
import grequests
from urllib.parse import quote
import xlsxwriter

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijk2MTEyYTU0LWZiZTktNGI5MS1hNGU2LTBlMjY5MmI5MGI0YSIsImlhdCI6MTQ3NzA2NTI5NCwic3ViIjoiZGV2ZWxvcGVyL2EzZjUxMmFlLTVmZWQtM2Q0MC00Y2E3LTdhYzc0ZTQ0YjQyOCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjIxNi4zOC4xMzkuMTAwIiwiNzEuMjAyLjIyMS4xMzciXSwidHlwZSI6ImNsaWVudCJ9XX0.7Ph05Uu6aG39DauBo6ysaOAQSoD-bizstcLVjHDsDovKleASB17QOc7EM2GwsL8ECxg0GQw1nKz6KPzH8wkdOw"

headers = {'authorization': 'Bearer ' + token}

r = requests.get('https://api.clashofclans.com/v1/clans/%23UGJPVJR', headers=headers)

tags = [member['tag'] for member in r.json()['memberList']]

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

workbook = xlsxwriter.Workbook('clan.xlsx')
worksheet = workbook.add_worksheet()

data = [
    [row[key]['value'] if type(row[key]) == dict and 'value' in row[key] else row[key] for key in column_keys]
    for row in rows]

data.insert(0, ['Player Name', 'TH Level', 'Best Trophines', 'Total Gold Grab', 'Total Exliser Grab', 'Total DE Grab',
                'Total Donations', 'Total Spells Donated'])

for row, data in enumerate(data):
    worksheet.write_row(row + 1, 0, data)

workbook.close()
