from flask import jsonify

from clashleaders import app
from clashleaders.model import ClanPreCalculated
from clashleaders.model.clan import prepend_hash


@app.route("/clan/<clan_tag>/<player_tag>.json")
def clan_player_json(clan_tag, player_tag):
    clan = ClanPreCalculated.find_by_tag(clan_tag)
    player_tag = prepend_hash(player_tag)
    player = next((p for p in clan.players if p['tag'] == player_tag), dict(tag=player_tag))

    return jsonify(player)
