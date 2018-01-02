from clashstats import app, cache
from clashstats.clash.transformer import clans_leaderboard
from clashstats.model import ClanPreCalculated
from flask import render_template


@app.route("/")
@cache.cached(timeout=30)
def index():
    return render_template('index.html',
                           most_donations=leaderboard('week_delta.avg_donations'),
                           most_attacks=leaderboard('week_delta.avg_attack_wins'),
                           most_bh_attacks=leaderboard('week_delta.avg_versus_wins'),
                           most_loot=leaderboard('week_delta.avg_gold_grab'),
                           most_points=leaderboard('clanPoints'),
                           most_vs_points=leaderboard('clanVersusPoints'),
                           most_win_streak=leaderboard('warWinStreak'),
                           most_war_stars=leaderboard('week_delta.avg_war_stars'),
                           most_trophies=leaderboard('week_delta.avg_trophies'),
                           avg_bh_level=leaderboard('avg_bh_level')
                           )


def leaderboard(field):
    return clans_leaderboard(ClanPreCalculated.objects(members__gt=20).order_by(f"-{field}").limit(10), field)
