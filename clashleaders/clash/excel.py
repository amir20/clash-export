from io import BytesIO

from xlsxwriter import Workbook

from clashleaders.clash.transformer import transform_players


def to_stream(clan):
    stream = BytesIO()
    data = transform_players(clan.players)
    workbook = Workbook(stream)
    worksheet = workbook.add_worksheet(clan.tag)
    for row, data in enumerate(data):
        worksheet.write_row(row, 0, data)
    workbook.close()
    stream.seek(0)
    return stream
