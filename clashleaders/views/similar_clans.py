from flask import jsonify

from clashleaders import app, cache
from clashleaders.model import ClanPreCalculated


@app.route("/similar-clans/<cluster_id>/avg.json")
@cache.cached(timeout=1000)
def similar_clans_avg(cluster_id):
    gold = ClanPreCalculated.objects(cluster_label=cluster_id).average('week_delta.avg_gold_grab')
    elixir = ClanPreCalculated.objects(cluster_label=cluster_id).average('week_delta.avg_elixir_grab')
    de = ClanPreCalculated.objects(cluster_label=cluster_id).average('week_delta.avg_de_grab')

    data = {
        'gold_grab': gold,
        'elixir_grab': elixir,
        'de_grab': de,
    }

    return jsonify(data)
