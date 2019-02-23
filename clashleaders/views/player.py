from flask import render_template, jsonify

from clashleaders import app, cache
from clashleaders.model import Player


@app.route("/player/<slug>")
def player_html(slug):
    player = Player.find_by_slug(slug)
    clan = player.most_recent_clan()
    return render_template('player.html',
                           player=player,
                           player_score=player.player_score(),
                           clan=clan,
                           insights=player_troops_insights(player))


@app.route("/player/<tag>/activity.json")
@cache.cached(timeout=1200, query_string=True)
def player_attacks_json(tag):
    player = Player.find_by_tag(tag)
    df = player.to_historical_df()[
        ['attack_wins', 'donations', 'gold_grab', 'elixir_escapade', 'heroic_heist', 'trophies']
    ]
    resampled = df.resample('D').mean()
    diffed = resampled.diff().dropna().clip(lower=0)
    diffed.rename(columns={'elixir_escapade': 'elixir_grab', 'heroic_heist': 'de_grab'}, inplace=True)
    diffed['trophies'] = resampled['trophies']  # Undo trophies
    return diffed.to_json(orient='columns', date_format='iso')


@app.route("/player/<tag>.json")
def player_json(tag):
    player = Player.find_by_tag(tag)
    return jsonify(player.to_dict(include_score=True))


@cache.memoize(28800)
def player_troops_insights(player):
    return player.troop_insights()


player_troops_insights.make_cache_key = lambda f, p: f"player_troops_insights_{p.tag}"
