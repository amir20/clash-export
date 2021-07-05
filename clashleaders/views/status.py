import json
import os

from flask import jsonify, render_template

from clashleaders import app, site_root
from clashleaders.clash import uptime
from clashleaders.model import Clan, Player, Status


@app.route("/status")
def status():
    monitor = uptime.monitor()
    uptime_ratio = float(monitor["custom_uptime_ratio"])
    stats = Status.instance()

    return render_template(
        "status.html",
        uptime_ratio=uptime_ratio,
        total_clans=stats.total_clans,
        total_active_clans=stats.total_active_clans,
        ratio_indexed=stats.ratio_indexed,
        total_players=stats.total_members,
        total_active_players=stats.total_active_members,
    )


@app.route("/version.json")
def version_json():
    with open(os.path.join(site_root, "..", "package.json")) as f:
        data = json.load(f)
    version = data["version"]
    commit = os.getenv("SOURCE_COMMIT")

    return jsonify(dict(version=version, commit=commit))


@app.route("/healthcheck")
def healthcheck():
    with open(os.path.join(site_root, "..", "package.json")) as f:
        data = json.load(f)
    version = data["version"]
    commit = os.getenv("SOURCE_COMMIT")
    players = Player.objects.count()
    clans = Clan.objects.count()

    return f"""
Version: {version}
Commit: {commit}
Total players: {players}
Total clans: {clans}
"""
