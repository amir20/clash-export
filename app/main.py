import os
import xlsxwriter
from flask import Flask, request, redirect, url_for, send_file, render_template, jsonify
from io import BytesIO
from mongoengine import connect
from raven.contrib.flask import Sentry
from uwsgidecorators import postfork

import api
import uptime as uptime_api
from model import Clan


@postfork
def connect_mongo():
    connect(db='clashstats', host='db')


app = Flask(__name__)
sentry = Sentry(app)
app.debug = os.getenv('DEBUG', False)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/uptime")
def uptime():
    monitor = uptime_api.monitor()
    uptime_ratio = float(monitor['custom_uptime_ratio'])
    return render_template('uptime.html', uptime_ratio=uptime_ratio)


@app.route("/search")
def search():
    return redirect(url_for('clan_detail', tag=request.args.get('tag')))


@app.route("/clan/<path:tag>")
def clan_detail(tag):
    tag, ext = os.path.splitext(tag)
    days_ago = request.args.get('daysAgo')
    clan = Clan.from_now_with_tag(tag, days=int(days_ago))[0] if days_ago else api.find_clan_by_tag(tag)

    if 'tag' not in clan:
        return render_template('error.html'), 404
    elif ext == '.xlsx':
        return export(clan=clan, filename='%s.xlsx' % tag)
    elif ext == '.json':
        if isinstance(clan, Clan):
            clan.memberList = None
            json = jsonify(api.transform_players(clan.players))
        else:
            json = jsonify(api.fetch_transform_clan(clan))

        return json
    else:
        return render_template('clan.html', clan=clan)


def export(clan, filename):
    stream = BytesIO()
    data = api.fetch_transform_clan(clan)
    workbook = xlsxwriter.Workbook(stream)
    worksheet = workbook.add_worksheet()
    for row, data in enumerate(data): worksheet.write_row(row, 0, data)
    workbook.close()
    stream.seek(0)
    return send_file(stream, attachment_filename=filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
