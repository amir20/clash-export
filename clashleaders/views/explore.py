from flask import render_template

from clashleaders import app
from clashleaders.model import Clan


@app.route("/explore/<field>")
def explore_clans(field):
    clans = Clan.objects(members__gt=20).order_by("-week_delta.avg_donations").limit(50)
    return render_template("explore.html", clans=clans)
