from flask import render_template

from clashleaders import app, cache
from clashleaders.clash.transformer import to_short_clan
from clashleaders.model import Clan, Status, ClanWar, CWLGroup


@app.route("/")
@cache.cached(600)
def index():
    latest_status = Status.instance()
    return render_template(
        "index.html",
        most_points=leaderboard("clanPoints"),
        most_vs_points=leaderboard("clanVersusPoints"),
        most_attacks=leaderboard("week_delta.total_attack_wins"),
        gained_trophies=leaderboard("week_delta.total_trophies"),
        grabbed_gold=leaderboard("week_delta.total_gold_grab"),
        total_wars=ClanWar.objects().count(),
        total_cwl_groups=CWLGroup.objects().count(),
        most_trophies_country=latest_status.trophies_by_country,
    )


def leaderboard(field):
    return clans_leaderboard(Clan.objects(members__gt=20).order_by(f"-{field}").limit(10), field)


def clans_leaderboard(clans, prop):
    return [to_short_clan(c, prop) for c in clans]
