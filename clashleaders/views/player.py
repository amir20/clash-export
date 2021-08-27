from flask import render_template
from mongoengine import DoesNotExist

from clashleaders import app, cache
from clashleaders.model import Player
from clashleaders.queue.player import fetch_players


@app.route("/player/<slug>")
def player_html(slug):
    try:
        player = Player.find_by_slug(slug)
        fetch_players.delay([player.tag])
        clan = player.most_recent_clan()
        initial_state = dict(
            tag=player.tag,
            troops=player.troops,
            heroes=player.heroes,
            spells=player.spells,
            insights=player_troops_insights(player),
            war_stats=player.war_stats(),
        )
    except DoesNotExist:
        return render_template("404.html"), 404
    else:
        return render_template(
            "player.html",
            player=player,
            clan=clan,
            initial_state=initial_state,
        )


@cache.memoize(28800)
def player_troops_insights(player):
    return player.troop_insights()


player_troops_insights.make_cache_key = lambda f, p: f"player_troops_insights_{p.tag}"
