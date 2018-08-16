from flask import jsonify

from clashleaders import app
from clashleaders.clash.player_calculation import find_player_details
from clashleaders.model import ClanPreCalculated


@app.route("/clan/<clan_tag>/<player_tag>.json")
def clan_player_json(clan_tag, player_tag):
    clan = ClanPreCalculated.find_by_tag(clan_tag)
    player = find_player_details(clan, player_tag)

    return jsonify(player)
