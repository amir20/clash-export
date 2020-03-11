from flask import render_template

from clashleaders import app, cache
from clashleaders.model import Clan

ORDER_MAPPING = {
    "most-popular": "-page_views",
    "most-attacks": "-week_delta.avg_attack_wins",
    "most-versus-attacks": "-week_delta.avg_versus_wins",
    "most-donations": "-week_delta.avg_donations",
    "most-war-stars": "-week_delta.avg_war_stars",
    "cwl": "-month_delta.avg_cwl_stars_percentile",
    "clan-games": "-month_delta.avg_games_xp_percentile",
    "wars": "-week_delta.avg_war_stars_percentile",
    "donations": "-week_delta.avg_donations_percentile",
    "attacks": "-week_delta.avg_attack_wins_percentile",
    "trophies": "-clanPoints",
}


TITLE_MAPPING = {
    "most-popular": "Most Popular",
    "most-attacks": "Most Attacks",
    "most-versus-attacks": "Most Versus Attacks",
    "most-donations": "Most Donations",
    "most-war-stars": "Most War Stars",
    "cwl": "Clan War League Acitivty",
    "clan-games": "Clan Games XP",
    "wars": "Clan Wars",
    "donations": "Most Donations",
    "attacks": "Most Attacks",
}


@app.route("/explore/<sort>")
@cache.cached(600)
def explore_clans(sort):
    clans = Clan.objects(members__gt=20).order_by(ORDER_MAPPING[sort]).limit(50)
    return render_template("explore.html", clans=clans, sort=sort, title=TITLE_MAPPING[sort])
