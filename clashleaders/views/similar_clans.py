from flask import jsonify, request

from clashleaders import app
from clashleaders.model import ClanPreCalculated


@app.route("/clan/<tag>/similar/avg.json")
def similar_clans_avg(tag):
    days = int(request.args.get('daysAgo', 7))
    key = {1: 'day_delta', 7: 'week_delta'}[days]

    cluster_label = ClanPreCalculated.find_by_tag(tag).cluster_label
    gold = ClanPreCalculated.objects(cluster_label=cluster_label).average(f"{key}.avg_gold_grab")
    elixir = ClanPreCalculated.objects(cluster_label=cluster_label).average(f"{key}.avg_elixir_grab")
    de = ClanPreCalculated.objects(cluster_label=cluster_label).average(f"{key}.avg_de_grab")

    data = dict(gold_grab=gold, elixir_grab=elixir, de_grab=de)
    return jsonify(data)
