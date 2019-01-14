from flask import render_template, jsonify

from clashleaders import app, cache
from clashleaders.model import Player, Clan


@app.route("/player/<slug>")
def player_html(slug):
    player = Player.find_by_slug(slug)
    score = player_score(player)
    clan = player.most_recent_clan()
    return render_template('player.html',
                           player=player,
                           player_score=score,
                           clan=clan,
                           insights=player_troops_insights(player))


@cache.memoize(28800)
def player_score(player):
    return player.player_score()


player_score.make_cache_key = lambda f, p: f"player_score{p.tag}"


@app.route("/player/<tag>/attacks.json")
@cache.cached(timeout=1200, query_string=True)
def player_attacks_json(tag):
    df = Player.find_by_tag(tag).to_historical_df()['attack_wins']
    return df.resample('D').mean().diff().dropna().clip(lower=0).to_json(orient='columns', date_format='iso')


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

    if data['clan']:
        data['clan']['slug'] = Clan.find_by_tag(data['clan']['tag']).slug

    return jsonify(data)


@cache.memoize(28800)
def player_troops_insights(player):
    df = player.troop_insights().dropna()
    th_df = df.xs('home', level='base')
    th_total = len(th_df)
    th_completed = len(th_df[th_df['delta'] <= 0])

    bh_df = df.xs('builderBase', level='base')
    bh_total = len(bh_df)
    bh_completed = len(bh_df[bh_df['delta'] <= 0])

    df = df[df['delta'] > 0]

    if df.empty:
        return dict(builderBase={},
                    home={},
                    th_ratio=th_completed / th_total,
                    bh_ratio=bh_completed / bh_total,
                    th_level=player.townHallLevel)

    builder_troops = df.xs('builderBase', level='base').to_dict('i')
    for k, v in builder_troops.items():
        v['name'] = k
    builder_troops = list(builder_troops.values())

    home_troops = df.xs('home', level='base').to_dict('i')
    for k, v in home_troops.items():
        v['name'] = k
    home_troops = list(home_troops.values())

    return dict(
        builderBase=builder_troops,
        home=home_troops,
        th_ratio=th_completed / th_total,
        bh_ratio=bh_completed / bh_total,
        th_level=player.townHallLevel
    )


player_troops_insights.make_cache_key = lambda f, p: f"player_troops_insights_{p.tag}"
