from flask import render_template

from clashleaders import app
from clashleaders.model import Player


@app.route("/player/<tag>")
def player_html(tag):
    player = Player.fetch_and_save(tag)
    return render_template('player.html', player=player)
