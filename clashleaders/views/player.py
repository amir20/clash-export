from flask import render_template, jsonify

from clashleaders import app
from clashleaders.model import Player


@app.route("/player/<tag>")
def player_html(tag):
    player = Player.fetch_and_save(tag)
    score = player.player_score()
    return render_template('player.html', player=player, player_score=score)


@app.route("/player/<tag>/attacks.json")
def player_attacks_json(tag):
    player = Player.find_by_tag(tag)
    series = player.player_series()
    data = [s['attackWins'] for s in series if s]
    return jsonify(data)
