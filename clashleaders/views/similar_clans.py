from flask import jsonify

from clashleaders import app, cache
from clashleaders.model import ClanPreCalculated


@app.route("/clan/<tag>/similar/avg.json")
@cache.cached(timeout=1000)
def similar_clans_avg(tag):
    cluster_label = ClanPreCalculated.find_by_tag(tag).cluster_label
    gold = ClanPreCalculated.objects(cluster_label=cluster_label).average('week_delta.avg_gold_grab')
    elixir = ClanPreCalculated.objects(cluster_label=cluster_label).average('week_delta.avg_elixir_grab')
    de = ClanPreCalculated.objects(cluster_label=cluster_label).average('week_delta.avg_de_grab')

    data = {
        'gold_grab': gold,
        'elixir_grab': elixir,
        'de_grab': de,
    }

    return jsonify(data)
