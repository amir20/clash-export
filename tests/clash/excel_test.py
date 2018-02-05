import pandas as pd
from clashleaders.clash.excel import to_stream


def test_excel_to_stream(clan_with_players, snapshot):
    stream = to_stream(clan_with_players)
    df = pd.read_excel(stream)

    snapshot.assert_match(df.to_json())
