import logging

import os
import requests_cache
from flask import Flask, request, redirect, url_for, send_file, render_template, jsonify, json
from flask_caching import Cache
from raven.contrib.flask import Sentry

from clash import uptime, excel
from clash.transformer import transform_players, clans_leaderboard, to_short_clan
from model import *

app = Flask(__name__)
app.debug = os.getenv('DEBUG', False)
sentry = Sentry(app)
logging.basicConfig(level=logging.INFO)

# Cache settings
requests_cache.install_cache(expire_after=timedelta(seconds=10), backend='memory')
cache = Cache(app, config={'CACHE_TYPE': 'null' if app.debug else 'filesystem', 'CACHE_DIR': '/tmp'})

# Set connect to False for pre-forking to work
connect(db='clashstats', host=os.getenv('DB_HOST'), connect=False)


@app.route("/")
@cache.cached(timeout=30)
def index():
    return render_template('index.html',
                           most_donations=leaderboard('week_delta.avg_donations'),
                           most_attacks=leaderboard('week_delta.avg_attack_wins'),
                           most_bh_attacks=leaderboard('week_delta.avg_versus_wins'),
                           most_loot=leaderboard('week_delta.avg_gold_grab'),
                           most_points=leaderboard('clanPoints'),
                           most_vs_points=leaderboard('clanVersusPoints'),
                           most_win_streak=leaderboard('warWinStreak'),
                           most_war_stars=leaderboard('week_delta.avg_war_stars'),
                           most_trophies=leaderboard('week_delta.avg_trophies'),
                           avg_bh_level=leaderboard('avg_bh_level')
                           )


def leaderboard(field):
    return clans_leaderboard(ClanPreCalculated.objects(members__gt=20).order_by(f"-{field}").limit(10), field)


@app.route("/status")
@cache.cached(timeout=30)
def status():
    monitor = uptime.monitor()
    uptime_ratio = float(monitor['custom_uptime_ratio'])
    stats = Status.objects.first()

    return render_template('status.html',
                           uptime_ratio=uptime_ratio,
                           total_clans=stats.total_clans,
                           ratio_indexed=stats.ratio_indexed,
                           total_players=0)


@app.route("/search.json")
def search():
    return jsonify([to_short_clan(c)._asdict() for c in ClanPreCalculated.objects.search_text(request.args.get('q'))])    


@app.route("/clan/<tag>.json")
def clan_detail_json(tag):
    try:
        api.find_clan_by_tag(tag)
    except api.ClanNotFound:
        return render_template('error.html'), 404
    else:
        days_ago = request.args.get('daysAgo')
        clan = clan_from_days_ago(days_ago, tag)
        return jsonify(transform_players(clan.players))


@app.route("/clan/<tag>.xlsx")
def clan_detail_xlsx(tag):
    try:
        api.find_clan_by_tag(tag)
    except api.ClanNotFound:
        return render_template('error.html'), 404
    else:
        days_ago = request.args.get('daysAgo')
        clan = clan_from_days_ago(days_ago, tag)
        return send_file(excel.to_stream(clan), attachment_filename=f"{clan.tag}.xlsx", as_attachment=True)


@app.route("/clan/<tag>")
def clan_detail_page(tag):
    try:
        clan = api.find_clan_by_tag(tag)
    except api.ClanNotFound:
        return render_template('error.html'), 404
    else:
        return render_template('clan.html', clan=clan)


@app.route("/clan/<tag>/short.json")
@cache.cached(timeout=1000)
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
