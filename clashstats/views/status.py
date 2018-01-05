from flask import render_template

from clashstats import app, cache
from clashstats.clash import uptime
from clashstats.model import Status


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
