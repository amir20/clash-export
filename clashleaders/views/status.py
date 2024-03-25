import os

from flask import render_template, jsonify

from clashleaders import app
from clashleaders.clash import uptime
from clashleaders.model import Status, Player, Clan


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
    version = os.getenv("VERSION_TAG")
    commit = os.getenv("SOURCE_COMMIT")

    return jsonify(dict(version=version, commit=commit))


@app.route("/healthcheck")
def healthcheck():
    version = os.getenv("VERSION_TAG")
    commit = os.getenv("SOURCE_COMMIT")
    players = Player.estimated_count()
    clans = Clan.estimated_count()

    return f"""
Version: {version}
Commit: {commit}
Total players: {players}
Total clans: {clans}
"""
