import json
import os.path

from flask import render_template

from clashleaders import app, cache
from clashleaders.clash.transformer import clans_leaderboard
from clashleaders.model import ClanPreCalculated

parent = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(parent, "../data/countries.json")) as f:
    data = json.load(f)
    COUNTRIES = {c['countryCode']: c for c in data if c['isCountry']}


@app.route("/")
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
                           avg_bh_level=leaderboard('avg_bh_level'),
                           most_active_country=aggregate_by_country('week_delta.avg_attack_wins'),
                           most_trophies_country=aggregate_by_country('clanPoints'),
                           trophy_distribution=trophy_distribution()
                           )


@cache.memoize(28800)
def leaderboard(field):
    return clans_leaderboard(ClanPreCalculated.objects(members__gt=20).order_by(f"-{field}").limit(10), field)


@cache.memoize(28800)
def aggregate_by_country(score_column="week_delta.avg_attack_wins"):
    group = {"$group": {"_id": "$location.countryCode", "score": {"$sum": f"${score_column}"}}}
    sort = {'$sort': {'score': -1}}
    aggregated = list(ClanPreCalculated.objects(location__countryCode__ne=None).aggregate(group, sort))
    aggregated = [{'code': c['_id'].lower(), 'name': COUNTRIES[c['_id']]['name'], 'score': c['score']} for c in aggregated[:10]]
    return aggregated


@cache.memoize(28800)
def trophy_distribution():
    counts = list(ClanPreCalculated.objects.aggregate({
        '$group': {
            '_id': {'$subtract': ['$clanPoints', {'$mod': ['$clanPoints', 500]}]},
            'count': {'$sum': 1}}},
        {'$sort': {'_id': 1}}
    ))

    labels = [c['_id'] for c in counts]
    values = [c['count'] for c in counts]

    return dict(labels=labels, values=values)
