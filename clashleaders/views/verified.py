from flask import render_template

from clashleaders import app, cache
from clashleaders.model import Clan


@app.route("/verified/<tag>")
@cache.cached(600)
def verified_clans(tag):
    clans = list(Clan.objects(verified_accounts=tag).order_by("-clanPoints"))

    return render_template("verified.html", clans=clans)
