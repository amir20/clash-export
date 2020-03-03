from flask import render_template

from clashleaders import app, cache
from clashleaders.model import Clan

ORDER_MAPPING = {
    "most-popular": "-page_views",
    "most-attacks": "-week_delta.avg_attack_wins",
    "most-versus-attacks": "-week_delta.avg_versus_wins",
    "most-donations": "-week_delta.avg_donations",
    "most-war-stars": "-week_delta.avg_war_stars",
}

TITLE_MAPPING = {
    "most-popular": "Most Popular",
    "most-attacks": "Most Attacks",
    "most-versus-attacks": "Most Versus Attacks",
    "most-donations": "Most Donations",
    "most-war-stars": "Most War Stars",
}


@app.route("/explore/<sort>")
@cache.cached(600)
def explore_clans(sort):
    clans = Clan.objects(members__gt=20).order_by(ORDER_MAPPING[sort]).limit(50)
    return render_template("explore.html", clans=clans, sort=sort, title=TITLE_MAPPING[sort])
