import xlsxwriter
from io import BytesIO

from clash import transformer


def to_stream(clan):
    stream = BytesIO()
    data = transformer.transform_players(clan.players)
    workbook = xlsxwriter.Workbook(stream)
    worksheet = workbook.add_worksheet()
    for row, data in enumerate(data):
        worksheet.write_row(row, 0, data)
    workbook.close()
    stream.seek(0)
    return stream
