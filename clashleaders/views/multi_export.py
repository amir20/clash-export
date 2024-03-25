from io import BytesIO

import pandas as pd
from flask import send_file

from clashleaders import app
from clashleaders.model import Clan


@app.route("/exportclans/<tags>")
def export_clans(tags):
    clans = [Clan.find_by_tag(tag) for tag in tags.split(",")]
    dfs = [clan.historical_near_days_ago(0).to_df(formatted=True) for clan in clans]
    merged = pd.concat(dfs)
    stream = BytesIO()
    writer = pd.ExcelWriter(
        stream,
        engine="xlsxwriter",
        options={"strings_to_urls": False, "strings_to_formulas": False},
    )
    merged.to_excel(writer, sheet_name="merged")
    writer.close()
    stream.seek(0)

    return send_file(
        stream, attachment_filename="merged_clans.xlsx", as_attachment=True
    )


@app.route("/exporttag/<tag>")
def export_tag(tag):
    tag = f"#{tag}"
    clans = list(Clan.objects.search_text(f'"{tag}"').order_by("name"))
    dfs = [clan.historical_near_days_ago(0).to_df(formatted=True) for clan in clans]
    merged = pd.concat(dfs)
    stream = BytesIO()
    writer = pd.ExcelWriter(
        stream,
        engine="xlsxwriter",
        options={"strings_to_urls": False, "strings_to_formulas": False},
    )
    merged.to_excel(writer, sheet_name="merged")
    writer.close()
    stream.seek(0)

    return send_file(
        stream, attachment_filename="merged_clans.xlsx", as_attachment=True
    )
