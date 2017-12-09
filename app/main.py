import os
import logging
import requests_cache

from flask import Flask, request, redirect, url_for, send_file, render_template, jsonify, json
from mongoengine import connect
from raven.contrib.flask import Sentry
from clash import uptime, excel, api
from clash.transformer import transform_players
from datetime import timedelta
from model import Clan, Player


app = Flask(__name__)
app.debug = os.getenv('DEBUG', False)
sentry = Sentry(app)
logging.basicConfig(level=logging.INFO)

requests_cache.install_cache(expire_after=timedelta(seconds=10), backend='memory')

# Set connect to False for pre-forking to work
connect(db='clashstats', host=os.getenv('DB_HOST'), connect=False)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/status")
def status():
    monitor = uptime.monitor()
    uptime_ratio = float(monitor['custom_uptime_ratio'])
    total_clans = len(Clan.objects.distinct('tag'))
    clans_indexed = len(Clan.from_now(hours=12).distinct('tag'))
    total_players = len(Player.objects.distinct('tag'))

    return render_template('status.html', uptime_ratio=uptime_ratio, total_clans=total_clans, clans_indexed=clans_indexed, total_players=total_players)


@app.route("/search")
def search():
    return redirect(url_for('clan_detail', tag=request.args.get('tag').replace('#', '')))


@app.route("/clan/<path:tag>")
def clan_detail(tag):
    tag, ext = os.path.splitext(tag)

    if not tag.startswith('#'):
        tag = '#' + tag

    clan = api.find_clan_by_tag(tag)

    if 'tag' not in clan:
        return render_template('error.html'), 404
    elif ext == '.xlsx':
        days_ago = request.args.get('daysAgo')
        clan = clan_from_days_ago(days_ago, tag)
        return send_file(excel.to_stream(clan), attachment_filename=f"{tag}.xlsx", as_attachment=True)
    elif ext == '.json':
        days_ago = request.args.get('daysAgo')
        clan = clan_from_days_ago(days_ago, tag)

        return jsonify(transform_players(clan.players))
    else:
        return render_template('clan.html', clan=clan)


@app.route("/clan/<path:tag>/short.json")
def clan_meta(tag):
    clan = clan_from_days_ago(1, tag)
    clan.id = None
    clan.players = None        
    return clan.to_json()


def clan_from_days_ago(days_ago, tag):
    if days_ago:
        return Clan.from_now_with_tag(tag, days=int(days_ago)).first() or Clan.fetch_and_save(tag)
    else:
        return Clan.fetch_and_save(tag)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


def manifest_path(file):
    SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
    manifest = os.path.join(SITE_ROOT, "static", "manifest.json")
    with open(manifest) as f:
        data = json.load(f)
    return data[file]


app.add_template_global(manifest_path, 'manifest_path')

if __name__ == "__main__":
    if (app.debug):
        from werkzeug.debug import DebuggedApplication
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

    app.run(host='0.0.0.0', port=80)
