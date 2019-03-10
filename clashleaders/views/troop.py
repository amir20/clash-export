import contentful
from flask import render_template

from clashleaders import cache, app
from clashleaders.model import AverageTroop

client = contentful.Client("zmnodi6xws9d", "8017b7370aaf68e6caefc204d56fc6f2b3cee22adc907ebf0b4fbc40d7d98799")


@app.route("/troop/<slug>")
def troop_html(slug):
    troop = fetch_troop(slug)
    averages = AverageTroop.objects(name=troop.name, is_builder_base=troop.base == "Builder Base")
    avg_data = [{"level": a.th_level, "avg": a.avg, "max": a.max} for a in averages]
    return render_template("troop.html", troop=troop, averages=avg_data)


@cache.memoize(900)
def fetch_troop(slug):
    return list(client.entries({"content_type": "lab", "fields.slug": slug}))[0]
