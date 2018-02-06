import pandas as pd
import xlrd
from clashleaders.clash.excel import to_stream


def test_excel_to_stream(clan_with_players, snapshot):
    stream = to_stream(clan_with_players)
    df = pd.read_excel(stream)

    snapshot.assert_match(df.to_csv())


def test_sheet_name(clan_with_players):
    stream = to_stream(clan_with_players)
    book = xlrd.open_workbook(file_contents=stream.read())

    assert book.sheet_names() == ["#UGJPVJR"]