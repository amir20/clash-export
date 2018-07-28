from flask import jsonify

from clashleaders import app
from clashleaders.model import Clan
from clashleaders.model.clan import prepend_hash


@app.route("/clan/<clan_tag>/<player_tag>.json")
def clan_player_json(clan_tag, player_tag):
    clan = Clan.find_most_recent_by_tag(clan_tag)
    players = clan.players_data()
    player_tag = prepend_hash(player_tag)
    player = next((p for p in players if p['tag'] == player_tag))

    return jsonify(player)
