import json
import os.path

from flask import render_template

from clashleaders import app, cache
from clashleaders.clash.transformer import to_short_clan
from clashleaders.model import Clan

parent = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(parent, "../data/countries.json")) as f:
    data = json.load(f)
    COUNTRIES = {c['countryCode']: c for c in data if c['isCountry']}


@app.route("/")
def index():
    return render_template('index.html',
                           most_points=leaderboard('clanPoints'),
                           most_vs_points=leaderboard('clanVersusPoints'),
                           most_trophies_country=aggregate_by_country('clanPoints'),
                           trophy_distribution=trophy_distribution()
                           )


@cache.memoize(28800)
def leaderboard(field):
    return clans_leaderboard(Clan.objects(members__gt=20).order_by(f"-{field}").limit(10), field)


@cache.memoize(28800)
def aggregate_by_country(score_column="week_delta.avg_attack_wins"):
    group = {"$group": {"_id": "$location.countryCode", "score": {"$sum": f"${score_column}"}}}
    sort = {'$sort': {'score': -1}}
    aggregated = list(Clan.objects(location__countryCode__ne=None).aggregate(group, sort))
    aggregated = [{'code': c['_id'].lower(), 'name': COUNTRIES[c['_id']]['name'], 'score': c['score']}
                  for c in aggregated[:10]]
    return aggregated


@cache.memoize(28800)
def trophy_distribution():
    counts = list(Clan.objects.aggregate({
        '$group': {
            '_id': {'$subtract': ['$clanPoints', {'$mod': ['$clanPoints', 500]}]},
            'count': {'$sum': 1}}},
        {'$sort': {'_id': 1}}
    ))

    labels = [c['_id'] for c in counts]
    values = [c['count'] for c in counts]

    return dict(labels=labels, values=values)


def clans_leaderboard(clans, prop):
    return [to_short_clan(c, prop) for c in clans]
