from io import BytesIO

import pandas as pd


def to_stream(clan):
    stream = BytesIO()
    writer = pd.ExcelWriter(stream, engine='xlsxwriter')
    clan.to_df(formatted=True).to_excel(writer, sheet_name=clan.tag)
    writer.close()
    stream.seek(0)
    return stream
