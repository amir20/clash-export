import pandas as pd
from flask import render_template, jsonify

from clashleaders import app
from clashleaders.model import Player


@app.route("/player/<slug>")
def player_html(slug):
    player = Player.find_by_slug(slug).fetch_and_update()
    score = player.player_score()
    clan = player.pre_calculated_clan()
    return render_template('player.html', player=player, player_score=score, clan=clan)


@app.route("/player/<tag>/attacks.json")
def player_attacks_json(tag):
    player = Player.find_by_tag(tag)
    series = player.player_series()
    data = [{'created_on': s['created_on'], 'attackWins': s['attackWins']} for s in series if s]
    df = pd.DataFrame(data, index=pd.to_datetime([s['created_on'] for s in data]), columns=['attackWins'])
    resampled = df.resample('D').mean().dropna()
    data = dict(
        dates=[i.strftime("%Y-%m-%d") for i in resampled.index],
        attackWins=resampled['attackWins'].values.tolist()
    )

    return jsonify(data)


@app.route("/player/<tag>.json")
def player_json(tag):
    player = Player.find_by_tag(tag)
    score = player.player_score()
    fields = list(player._fields_ordered)
    fields.remove("id")
    fields.remove("binary_bytes")

    data = dict()
    for field in fields:
        data[field] = player[field]

    data['percentile'] = score

    return jsonify(data)
