from flask import render_template

from clashleaders import app
from clashleaders.model import ClanPreCalculated


@app.route("/verified/<tag>")
def verified_clans(tag):
    clans = ClanPreCalculated.objects(verified_accounts=tag).order_by('-clanPoints')
    return render_template('verified.html', clans=clans)
