from flask import render_template

from clashleaders import app, cache
from clashleaders.clash.transformer import to_short_clan
from clashleaders.model import Clan, Status


@app.route("/")
def index():
    latest_status = Status.instance()
    return render_template(
        "index.html",
        most_points=leaderboard("clanPoints"),
        most_vs_points=leaderboard("clanVersusPoints"),
        most_attacks=leaderboard("week_delta.total_attack_wins"),
        gained_trophies=leaderboard("week_delta.total_trophies"),
        grabbed_gold=leaderboard("week_delta.total_gold_grab"),
        most_trophies_country=latest_status.trophies_by_country,
        trophy_distribution=latest_status.trophy_distribution,
    )


@cache.memoize(1800)
def leaderboard(field):
    return clans_leaderboard(Clan.objects(members__gt=20).order_by(f"-{field}").limit(10), field)


def clans_leaderboard(clans, prop):
    return [to_short_clan(c, prop) for c in clans]
