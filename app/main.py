import os
import logging

from flask import Flask, request, redirect, url_for, send_file, render_template, jsonify, json
from mongoengine import connect
from raven.contrib.flask import Sentry
from clash import uptime as uptime_api, excel, api
from clash.transformer import transform_players
from model import Clan


app = Flask(__name__)
app.debug = os.getenv('DEBUG', False)
sentry = Sentry(app)
logging.basicConfig(level=logging.INFO)

# Set connect to False for pre-forking to work
connect(db='clashstats', host='db', connect=False)


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
    clan = api.find_clan_by_tag(tag)

    if 'tag' not in clan:
        return render_template('error.html'), 404
    elif ext == '.xlsx':
        clan = Clan.fetch_and_save(tag)
        return send_file(excel.to_stream(clan), attachment_filename=f"{tag}.xlsx", as_attachment=True)
    elif ext == '.json':
        days_ago = request.args.get('daysAgo')
        if days_ago:
            clans = Clan.from_now_with_tag(tag, days=int(days_ago))
            if not clans:
                clan = Clan.fetch_and_save(tag)
            else:
                clan = clans[0]
        else:
            clan = Clan.fetch_and_save(tag)

        return jsonify(transform_players(clan.players))
    else:
        return render_template('clan.html', clan=clan)


def javascript_path(file):
    SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
    manifest = os.path.join(SITE_ROOT, "static", "manifest.json")
    with open(manifest) as f:
        data = json.load(f)
    return data[file]


app.add_template_global(javascript_path, 'javascript_path')

if __name__ == "__main__":
    app.debug = os.getenv('DEBUG', False)
    if (app.debug):
        from werkzeug.debug import DebuggedApplication
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

    app.run(host='0.0.0.0', port=80)
