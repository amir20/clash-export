from flask import render_template

from clashleaders import app
from clashleaders.model import Clan

ORDER_MAPPING = {
    "most-popular": "-page_views",
    "most-attacks": "-week_delta.avg_attack_wins",
    "most-versus-trophies": "-week_delta.avg_versus_wins",
    "most-donations": "-week_delta.avg_donations",
    "most-war-stars": "-week.avg_war_stars",
}


@app.route("/explore/<sort>")
def explore_clans(sort):
    clans = Clan.objects(members__gt=20).order_by(ORDER_MAPPING[sort]).limit(50)
    return render_template("explore.html", clans=clans, sort=sort)
