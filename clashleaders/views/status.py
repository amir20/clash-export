from flask import render_template

from clashleaders import app, cache
from clashleaders.clash import uptime
from clashleaders.model import Status


@app.route("/status")
@cache.cached(timeout=30)
def status():
    monitor = uptime.monitor()
    uptime_ratio = float(monitor['custom_uptime_ratio'])
    stats = Status.get_instance()

    return render_template('status.html',
                           uptime_ratio=uptime_ratio,
                           total_clans=stats.total_clans,
                           total_active_clans=stats.total_active_clans,
                           ratio_indexed=stats.ratio_indexed,
                           total_players=stats.total_members,
                           total_active_players=stats.total_active_members)
