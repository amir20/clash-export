from io import BytesIO

import pandas as pd
from flask import render_template, send_file, request
from mongoengine import DoesNotExist

from clashleaders import app
from clashleaders.model import Clan


@app.route("/clan/<slug>.xlsx")
def clan_detail_xlsx(slug):
    try:
        clan = Clan.find_by_slug(slug)
    except DoesNotExist:
        return render_template('error.html'), 404
    else:
        h = clan.historical_near_days_ago(request.args.get('daysAgo', 0))
        return send_file(to_stream(h), attachment_filename=f"{clan.tag}.xlsx", as_attachment=True)


def to_stream(clan):
    stream = BytesIO()
    writer = pd.ExcelWriter(stream, engine='xlsxwriter')
    clan.to_df(formatted=True).to_excel(writer, sheet_name=clan.tag)
    writer.close()
    stream.seek(0)
    return stream
