from flask import jsonify, request

from clashleaders import app
from clashleaders.model import ClanPreCalculated


@app.route("/clan/<tag>/similar/avg.json")
def similar_clans_avg(tag):
    ratio = int(request.args.get('daysAgo', 7)) / 7
    cluster_label = ClanPreCalculated.find_by_tag(tag).cluster_label
    gold = ClanPreCalculated.objects(cluster_label=cluster_label).average('week_delta.avg_gold_grab')
    elixir = ClanPreCalculated.objects(cluster_label=cluster_label).average('week_delta.avg_elixir_grab')
    de = ClanPreCalculated.objects(cluster_label=cluster_label).average('week_delta.avg_de_grab')

    data = {
        'gold_grab': gold * ratio,
        'elixir_grab': elixir * ratio,
        'de_grab': de * ratio,
    }

    return jsonify(data)
